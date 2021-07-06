from datetime import datetime
import logging
from time import time
from typing import Any, Dict, List, Tuple, Union

from gurux_dlms import GXDLMSClient
from gurux_dlms.GXByteBuffer import GXByteBuffer
from gurux_dlms.GXDateTime import GXDateTime
from gurux_dlms.GXReplyData import GXReplyData
from gurux_dlms.enums.ObjectType import ObjectType
from gurux_dlms.objects import GXDLMSObject, GXDLMSClock
from gurux_dlms.objects.GXDLMSData import GXDLMSData
from gurux_dlms.objects.GXDLMSRegister import GXDLMSRegister

from .reader_data import ReaderDataPoint, ReaderDataPointType

LOGGER = logging.getLogger("smartmeter")


class HdlcDlmsParser:
    def __init__(self, selected_obis: Dict[str, ReaderDataPointType], id_obis: str, clock_obis: str) -> None:
        self._client = GXDLMSClient(True)
        self._hdlc_buffer = GXByteBuffer()
        self._dlms_data = GXReplyData()
        self._selected_obis = selected_obis
        self._id_obis = id_obis
        self._clock_obis = clock_obis
        self._meter_id:str = None

    def append_to_hdlc_buffer(self, data: bytes) -> None:
        self._hdlc_buffer.set(data)

    def clear_hdlc_buffer(self) -> None:
        self._hdlc_buffer.clear()

    def extract_data_from_hdlc_frames(self) -> bool:
        """
        Try to extract data fragments from HDLC frame-buffer and store it into DLMS buffer.
        HDLC buffer is being cleared.
        Returns: True if data is complete for parsing.
        """
        tmp = GXReplyData()
        try:
            self._client.getData(self._hdlc_buffer, tmp, self._dlms_data)
        except ValueError as ex:
            LOGGER.debug("Unable to extract data from hdlc frame: '%s'", ex)
            self._hdlc_buffer.clear()
            self._dlms_data.clear()
            return False

        self._hdlc_buffer.clear()
        if not self._dlms_data.isComplete():
            LOGGER.debug("Incomplete HDLC frame. DLMS buffer is cleared.")
            self._dlms_data.clear()
            return False

        if not self._dlms_data.isMoreData():
            LOGGER.debug("DLMS packet complete and ready for parsing.")
            return True
        return False

    def parse_to_dlms_objects(self) -> Dict[str, GXDLMSObject]:
        parsed_objects: List[Tuple[GXDLMSObject, int]] = []
        if isinstance(self._dlms_data.value, list):
            parsed_objects = self._client.parsePushObjects(self._dlms_data.value[0])
            for index, (obj, attr_ind) in enumerate(parsed_objects):
                if index == 0:
                    # Skip first (meta-data) object
                    continue
                self._client.updateValue(obj, attr_ind, self._dlms_data.value[index])
                LOGGER.debug(str(obj.objectType) + " " + obj.logicalName + " " + str(attr_ind) + ": " + str(obj.getValues()[attr_ind - 1]))
        self._dlms_data.clear()
        return {obj.getName(): obj for obj, _ in parsed_objects}

    def convert_dlms_bundle_to_reader_data(self, dlms_objects: Dict[str, GXDLMSObject]) -> List[ReaderDataPoint]:
        clock_obj = dlms_objects.get(self._clock_obis, None)
        ts = None
        if clock_obj:
            ts = self._extract_datetime(clock_obj)
        
        id_obj = dlms_objects.get(self._id_obis, None)
        id = None
        if id_obj:
            id = self._extract_value_from_data_object(id_obj)
        if isinstance(id, str) and len(id) > 0:
            self._meter_id = id

        data_points: List[ReaderDataPoint] = []
        for obis, obj in filter(lambda o: o[1].getObjectType() == ObjectType.REGISTER, dlms_objects.items()):
            if obis in self._selected_obis:
                raw_value = self._extract_register_value(obj)
                if raw_value is None:
                    LOGGER.warning("No value received for %s.", obis)
                    continue
                type = self._selected_obis[obis]
                value = float(raw_value) # TODO add value scaling
                data_points.append(ReaderDataPoint(type, value, self._meter_id, ts))
        return data_points

    @staticmethod
    def _extract_datetime(clock_object: GXDLMSClock) -> Union[datetime, None]:
        assert isinstance(clock_object, GXDLMSClock)
        time_obj: GXDateTime = clock_object.getValues()[1]
        if isinstance(time_obj, GXDateTime):
            return time_obj.value
        return None

    @staticmethod
    def _extract_value_from_data_object(data_object: GXDLMSData) -> Union[Any, None]:
        assert isinstance(data_object, GXDLMSData)
        return data_object.getValues()[1]

    @staticmethod
    def _extract_register_value(register: GXDLMSRegister) -> Union[Any, None]:
        assert isinstance(register, GXDLMSRegister)
        return register.getValues()[1]
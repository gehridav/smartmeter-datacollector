#
# Copyright (C) 2024 Supercomputing Systems AG
# This file is part of smartmeter-datacollector.
#
# SPDX-License-Identifier: GPL-2.0-only
# See LICENSES/README.md for more information.
#
import logging
from typing import Optional

import serial

from .cosem import Cosem, RegisterCosem
from .meter import MeterError, SerialHdlcDlmsMeter
from .meter_data import MeterDataPointTypes
from .obis import OBISCode
from .reader import ReaderError
from .serial_reader import SerialConfig

LOGGER = logging.getLogger("smartmeter")

EXTENDED_REGISTER_MAPPING = [
    RegisterCosem(OBISCode(0, 1, 24, 2, 1), MeterDataPointTypes.WATER.value)
]

EXTENDED_REGISTER_IDS = [
    OBISCode(0, 1, 24, 1, 0)
]

class LGE450(SerialHdlcDlmsMeter):
    BAUDRATE = 2400

    def __init__(self, port: str,
                 baudrate: int = BAUDRATE,
                 decryption_key: Optional[str] = None,
                 use_system_time: bool = False) -> None:
        serial_config = SerialConfig(
            port=port,
            baudrate=baudrate,
            data_bits=serial.EIGHTBITS,
            parity=serial.PARITY_EVEN,
            stop_bits=serial.STOPBITS_ONE,
            termination=SerialHdlcDlmsMeter.HDLC_FLAG
        )
        cosem = Cosem(fallback_id=port, id_obis_override=EXTENDED_REGISTER_IDS, register_obis_extended=EXTENDED_REGISTER_MAPPING)
        try:
            super().__init__(serial_config, cosem, decryption_key, use_system_time)
        except ReaderError as ex:
            LOGGER.fatal("Unable to setup serial reader for L+G E450. '%s'", ex)
            raise MeterError("Failed setting up L+G E450.") from ex

        LOGGER.info("Successfully set up L+G E450 smart meter on '%s'.", port)

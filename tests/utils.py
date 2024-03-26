#
# Copyright (C) 2022 Supercomputing Systems AG
# This file is part of smartmeter-datacollector.
#
# SPDX-License-Identifier: GPL-2.0-only
# See LICENSES/README.md for more information.
#
from typing import List, Optional

import pytest

from smartmeter_datacollector.smartmeter.cosem import Cosem, RegisterCosem
from smartmeter_datacollector.smartmeter.hdlc_dlms_parser import HdlcDlmsParser
from smartmeter_datacollector.smartmeter.meter_data import MeterDataPointTypes
from smartmeter_datacollector.smartmeter.obis import OBISCode


def prepare_parser(data: List[bytes], cosem_config: Cosem, cipher_key: Optional[str] = None) -> HdlcDlmsParser:
    parser = HdlcDlmsParser(cosem_config, cipher_key)
    for frame in data:
        parser.append_to_hdlc_buffer(frame)
        parser.extract_data_from_hdlc_frames()
    return parser


@pytest.fixture
def cosem_config_lg() -> Cosem:
    return Cosem(
        fallback_id="fallback_id",
        id_obis_override=[OBISCode(0, 1, 24, 1, 0)],
        register_obis_extended=[RegisterCosem(OBISCode(0, 1, 24, 2, 1), MeterDataPointTypes.WATER.value)]
    )


@pytest.fixture
def unencrypted_valid_data_lg() -> List[bytes]:
    data_str: List[str] = []
    data_str.append("7E A0 84 CE FF 03 13 12 8B E6 E7 00 E0 40 00 01 00 00 70 0F 00 00 CB C2 0C 07 E5 07 06 02 0E 3A 05 FF 80 00 00 02 10 01 10 02 04 12 00 28 09 06 00 08 19 09 00 FF 0F 02 12 00 00 02 04 12 00 28 09 06 00 08 19 09 00 FF 0F 01 12 00 00 02 04 12 00 01 09 06 00 00 2A 00 00 FF 0F 02 12 00 00 02 04 12 00 01 09 06 00 00 60 01 01 FF 0F 02 12 00 00 02 04 12 00 08 09 06 00 00 01 00 00 FF 0F 02 12 00 00 77 C8 7E")
    data_str.append("7E A0 7D CE FF 03 13 D0 45 E0 40 00 02 00 00 6C 02 04 12 00 03 09 06 01 00 01 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 02 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 03 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 04 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 01 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 08 00 FF 0F 02 12 00 00 B3 98 7E")
    data_str.append("7E A0 84 CE FF 03 13 12 8B E6 E7 00 E0 40 00 01 00 00 70 0F 00 00 CB C6 0C 07 E5 07 06 02 0E 3A 10 FF 80 00 00 02 10 01 10 02 04 12 00 28 09 06 00 08 19 09 00 FF 0F 02 12 00 00 02 04 12 00 28 09 06 00 08 19 09 00 FF 0F 01 12 00 00 02 04 12 00 01 09 06 00 00 2A 00 00 FF 0F 02 12 00 00 02 04 12 00 01 09 06 00 00 60 01 01 FF 0F 02 12 00 00 02 04 12 00 08 09 06 00 00 01 00 00 FF 0F 02 12 00 00 27 73 7E")
    data_str.append("7E A0 7D CE FF 03 13 D0 45 E0 40 00 02 00 00 6C 02 04 12 00 03 09 06 01 00 01 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 02 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 03 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 04 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 01 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 08 00 FF 0F 02 12 00 00 B3 98 7E")
    data_str.append("7E A0 8B CE FF 03 13 EE E1 E0 40 00 03 00 00 7A 02 04 12 00 03 09 06 01 01 05 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 06 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 07 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 08 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 0D 07 00 FF 0F 02 12 00 00 09 06 00 08 19 09 00 FF 09 10 4C 47 5A 31 30 33 30 36 35 35 39 33 33 35 31 32 09 07 31 39 33 35 3B 2A 7E")
    data_str.append("7E A0 57 CE FF 03 13 E9 69 E0 C0 00 04 00 00 46 39 31 32 09 0C 07 E5 07 06 02 0E 3A 12 FF 80 00 81 06 00 00 00 1C 06 00 00 00 00 06 00 00 00 00 06 00 00 00 0A 06 00 0D 88 C1 06 00 00 00 00 06 00 00 00 12 06 00 00 00 01 06 00 00 00 00 06 00 04 72 0D 12 03 AD C2 CE 7E")
    data = list(map(lambda frag: bytes.fromhex(frag.replace(" ", "")), data_str))
    return data

@pytest.fixture
def unencrypted_valid_data_extended_register_lg() -> List[bytes]:
    data_str: List[str] = []
    data_str.append("7E A0 83 CF 03 13 3F 65 E6 E7 00 E0 40 00 01 00 00 70 0F 00 08 A6 2F 0C 07 E6 0A 13 03 0B 00 00 FF 80 00 00 02 0E 01 0E 02 04 12 00 28 09 06 00 0B 19 09 00 FF 0F 02 12 00 00 02 04 12 00 28 09 06 00 0B 19 09 00 FF 0F 01 12 00 00 02 04 12 00 48 09 06 00 01 18 01 00 FF 0F 06 12 00 00 02 04 12 00 48 09 06 00 02 18 01 00 FF 0F 06 12 00 00 02 04 12 00 48 09 06 00 03 18 01 00 FF 0F 06 12 00 00 BA 2E 7E")
    data_str.append("7E A0 7C CF 03 13 ED A0 E0 40 00 02 00 00 6C 02 04 12 00 04 09 06 00 01 18 02 01 FF 0F 02 12 00 00 02 04 12 00 04 09 06 00 02 18 02 01 FF 0F 02 12 00 00 02 04 12 00 04 09 06 00 03 18 02 01 FF 0F 02 12 00 00 02 04 12 00 48 09 06 00 01 18 01 00 FF 0F 09 12 00 00 02 04 12 00 48 09 06 00 02 18 01 00 FF 0F 09 12 00 00 02 04 12 00 48 09 06 00 03 18 01 00 FF 0F 09 12 00 00 D8 C3 7E") 
    data_str.append("7E A0 84 CF 03 13 1E 32 E0 C0 00 03 00 00 74 02 04 12 00 04 09 06 00 01 18 02 01 FF 0F 03 12 00 00 02 04 12 00 04 09 06 00 02 18 02 01 FF 0F 03 12 00 00 02 04 12 00 04 09 06 00 03 18 02 01 FF 0F 03 12 00 00 09 06 00 0B 19 09 00 FF 06 01 48 A6 1D 06 00 00 00 00 06 00 00 00 00 06 00 02 C0 EF 06 00 00 00 00 06 00 00 00 00 11 07 11 00 11 00 02 02 0F FD 16 0E 02 02 0F 00 16 0E 02 02 0F FE 16 0E 96 96 7E")
    data = list(map(lambda frag: bytes.fromhex(frag.replace(" ", "")), data_str))
    return data

@pytest.fixture
def unencrypted_invalid_data_lg() -> List[bytes]:
    data_str: List[str] = []
    data_str.append("7E A0 84 CE FF 03 13 12 8B E6 E7 00 E0 40 00 01 00 00 70 0F 00 00 C9 60 0C 07 E5 07 06 02 0E 07 37 FF 80 00 00 02 10 01 10 02 04 12 00 28 09 06 00 08 19 09 00 FF 0F 02 12 00 00 02 04 12 00 28 09 06 00 08 19 09 00 FF 0F 01 12 00 00 02 04 12 00 01 09 06 00 00 2A 00 00 FF 0F 02 12 00 00 02 04 12 00 01 09 06 00 00 60 01 01 FF 0F 02 12 00 00 02 04 12 00 08 09 06 00 00 01 00 00 FF 0F 02 12 00 00 35 37 7E")
    data_str.append("7E A0 7D CE FF 03 13 D0 45 E0 40 00 02 00 00 6C 02 04 12 00 03 09 06 01 00 01 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 02 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 03 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 04 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 01 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 08 00 FF 0F 02 12 00 00 B3 98 7E")
    data_str.append("7E A0 7D CE FF 03 13 D0 45 E0 40 00 02 00 00 6C 02 04 12 00 03 09 06 01 00 01 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 02 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 03 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 04 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 01 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 08 00 FF 0F 02 12 00 00 B3 98 7E")
    data_str.append("7E A0 8B CE FF 03 13 EE E1 E0 40 00 03 00 00 7A 02 04 12 00 03 09 06 01 01 05 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 06 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 07 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 08 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 0D 07 00 FF 0F 02 12 00 00 09 06 00 08 19 09 00 FF 09 10 4C 47 5A 31 30 33 30 36 35 35 39 33 33 35 31 32 09 07 31 39 33 35 3B 2A 7E")
    data_str.append("7E A0 57 CE FF 03 13 E9 69 E0 C0 00 04 00 00 46 39 31 32 09 0C 07 E5 07 06 02 0E 08 13 FF 80 00 81 06 00 00 00 00 06 00 00 00 00 06 00 00 00 00 06 00 00 00 00 06 00 0D 88 C1 06 00 00 00 00 06 00 00 00 12 06 00 00 00 01 06 00 00 00 00 06 00 04 72 0D 12 03 E8 AD 29 7E")
    data = list(map(lambda frag: bytes.fromhex(frag.replace(" ", "")), data_str))
    return data


@pytest.fixture
def unencrypted_valid_data_lg2() -> List[bytes]:
    data_str: List[str] = []
    data_str.append("7E A0 84 CE FF 03 13 12 8B E6 E7 00 E0 40 00 01 00 00 70 0F 00 03 B5 33 0C 07 E6 0B 16 02 10 25 1E FF 80 00 00 02 0B 01 0B 02 04 12 00 28 09 06 00 08 19 09 00 FF 0F 02 12 00 00 02 04 12 00 28 09 06 00 08 19 09 00 FF 0F 01 12 00 00 02 04 12 00 01 09 06 00 00 60 01 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 01 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 02 07 00 FF 0F 02 12 00 00 4C 21 7E")
    data_str.append("7E A0 8B CE FF 03 13 EE E1 E0 40 00 02 00 00 7A 02 04 12 00 03 09 06 01 01 01 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 05 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 06 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 07 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 08 08 00 FF 0F 02 12 00 00 09 06 00 08 19 09 00 FF 09 08 34 34 33 33 8B 52 7E")
    data_str.append("7E A0 3D CE FF 03 13 F2 84 E0 C0 00 03 00 00 2C 37 38 31 31 06 00 00 03 09 06 00 00 00 00 06 01 7F BF EB 06 00 43 7A DE 06 00 2F CD AE 06 00 00 33 BF 06 00 37 70 2E 06 00 F0 41 58 40 EF 7E")
    data = list(map(lambda frag: bytes.fromhex(frag.replace(" ", "")), data_str))
    return data


@pytest.fixture
def unencrypted_valid_data_iskra() -> List[bytes]:
    data_str: List[str] = []
    data_str.append("7E A8 A4 CF 02 23 03 99 96 E6 E7 00 0F 00 00 04 33 0C 07 E4 08 0F 06 06 13 2D 00 FF 88 80 02 1C 01 1C 02 04 12 00 28 09 06 00 06 19 09 00 FF 0F 02 12 00 00 02 04 12 00 28 09 06 00 06 19 09 00 FF 0F 01 12 00 00 02 04 12 00 01 09 06 00 00 2A 00 00 FF 0F 02 12 00 00 02 04 12 00 01 09 06 00 00 60 01 01 FF 0F 02 12 00 00 02 04 12 00 08 09 06 00 00 01 00 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 01 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 07 00 FF 0F 02 12 00 00 02 04 12 37 4F 7E")
    data_str.append("7E A8 A4 CF 02 23 03 99 96 00 03 09 06 01 01 03 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 04 07 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 01 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 01 08 01 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 01 08 02 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 08 01 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 02 08 02 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 05 08 00 FF 00 00 7E")
    data_str.append("7E A8 A4 CF 02 23 03 99 96 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 05 08 01 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 05 08 02 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 06 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 06 08 01 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 06 08 02 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 07 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 07 08 01 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 07 08 02 FF 0F 02 12 00 00 02 04 12 00 03 B2 E4 7E")
    data_str.append("7E A8 A4 CF 02 23 03 99 96 09 06 01 01 08 08 00 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 08 08 01 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 01 08 08 02 FF 0F 02 12 00 00 02 04 12 00 03 09 06 01 00 0D 07 00 FF 0F 02 12 00 00 09 06 00 06 19 09 00 FF 09 10 49 53 4B 31 30 33 30 37 37 35 32 31 33 38 35 39 09 07 31 38 37 36 33 35 30 09 0C 07 E4 08 0F 06 06 13 2D 00 FF 88 80 06 00 00 00 00 06 00 00 00 00 06 00 00 00 00 06 00 00 00 00 06 00 5F 0E A5 06 00 2F 44 2F 06 00 2F CA 76 06 00 00 BE FE 7E")
    data_str.append("7E A0 55 CF 02 23 13 A2 33 00 00 06 00 00 00 00 06 00 00 00 00 06 00 05 47 7C 06 00 03 84 3F 06 00 01 C3 3D 06 00 00 00 09 06 00 00 00 09 06 00 00 00 00 06 00 00 00 00 06 00 00 00 00 06 00 00 00 00 06 00 01 0A F7 06 00 00 94 B0 06 00 00 76 47 12 00 00 12 7B 7E")
    data = list(map(lambda frag: bytes.fromhex(frag.replace(" ", "")), data_str))
    return data


@pytest.fixture
def encrypted_data_no_pushlist_lg() -> List[bytes]:
    data_str: List[str] = []
    data_str.append("7E A0 8B CE FF 03 13 EE E1 E6 E7 00 E0 40 00 01 00 00 77 DB 08 4C 47 5A 67 73 78 1F D0 82 01 03 30 00 06 90 3C EB 7B E1 75 48 BF D7 C3 6E DF 96 48 93 7D 7C 78 26 2B E5 FC FE E3 6B 41 D0 61 CF F3 FA 3A E6 91 8B FD C6 1F 95 67 19 E2 95 91 FC D6 D0 A1 98 D6 CA 49 CC DD 56 5F D3 8A 5F 9A 6C 8E AC 3A BE EE 11 0D 2E C4 EB B6 DC 10 43 D3 5A 8B C8 7D 42 0E 75 A2 3C 44 F4 08 B7 A7 31 F1 62 1F 84 86 F3 50 C3 A4 9D 02 06 B1 3A 7E")
    data_str.append("7E A0 8B CE FF 03 13 EE E1 E0 40 00 02 00 00 7A 48 44 3E 98 6B 54 C0 4A 4E 84 AE 52 EC F1 89 4A CC 58 67 52 28 E2 45 6F 9B ED CD 22 79 03 FE 91 16 50 5C 90 02 A6 9A C4 5E F7 35 40 9B 4D 7E CE 2D 89 CD 86 F6 5B FB DF E6 1C 94 3F CE A4 CA 64 6C 3E EC BD 8C 38 BA 05 7B C5 21 DA 2C 08 E5 9B E8 FB B3 FE 59 27 94 D5 80 41 AF 33 2D C0 ED 7A 51 19 06 ED A5 24 07 95 81 9C 85 39 68 52 D7 9D 3A B7 B8 3B C7 30 23 F7 4B 5F 01 FE 7E")
    data_str.append(
        "7E A0 30 CE FF 03 13 86 F8 E0 C0 00 03 00 00 1F 1F FE C7 27 11 0F 74 B7 EF F4 1B 48 F7 47 B6 B6 A2 39 5B 42 BD 61 EA 18 7E D9 A0 99 8B 81 45 44 78 7E")
    data = list(map(lambda frag: bytes.fromhex(frag.replace(" ", "")), data_str))
    return data

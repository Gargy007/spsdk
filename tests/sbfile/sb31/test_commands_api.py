#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2019-2020 NXP
#
# SPDX-License-Identifier: BSD-3-Clause
"""Test of commands."""

import pytest

from spsdk.sbfile.sb31.constants import EnumCmdTag
from spsdk.sbfile.sb31.commands import CmdErase, CmdLoad, CmdExecute, CmdCall, CmdProgFuses, CmdProgIfr, \
    CmdLoadCmac, CmdLoadHashLocking, CmdCopy, CmdFillMemory, parse_command, CmdLoadKeyBlob, CmdConfigureMemory, \
    CmdSectionHeader, CmdFwVersionCheck
from spsdk.sbfile.sb31.functions import BaseCmd


def test_cmd_erase():
    """Test address, length, memory_id, info value, size after export and parsing of CmdErase command."""
    cmd = CmdErase(address=100, length=0, memory_id=0)
    assert cmd.address == 100
    assert cmd.length == 0
    assert cmd.memory_id == 0
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdErase.parse(data=data)
    assert cmd.address == cmd_parsed.address
    assert cmd.length == cmd_parsed.length
    assert cmd.memory_id == cmd_parsed.memory_id

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF
    assert 0x00000000 <= cmd.length <= 0xFFFFFFFF


def test_parse_invalid_cmd_erase_cmd_tag():
    """CmdErase tag validity test."""
    cmd = CmdErase(address=0, length=0, memory_id=0)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdErase.parse(data=data)


def test_cmd_load():
    """Test address, len, memory_id, info value, size after append, export and parsing of CmdLoad command."""
    cmd = CmdLoad(address=100, length=0, memory_id=0)
    assert cmd.address == 100
    assert cmd.length == 0
    assert cmd.memory_id == 0
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdLoad.parse(data=data)
    assert cmd.address == cmd_parsed.address
    assert cmd.length == cmd_parsed.length
    assert cmd.memory_id == cmd_parsed.memory_id

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF
    assert 0x00000000 <= cmd.length <= 0xFFFFFFFF


def test_parse_invalid_cmd_load_cmd_tag():
    """CmdLoad tag validity test."""
    cmd = CmdLoad(address=0, length=0, memory_id=0)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdLoad.parse(data=data)


def test_cmd_execute():
    """Test address, info value, size after export and parsing of CmdExecute command."""
    cmd = CmdExecute(address=100)
    assert cmd.address == 100
    assert cmd.info()

    data = cmd.export()
    assert len(data) == BaseCmd.SIZE

    cmd_parsed = CmdExecute.parse(data=data)
    assert cmd == cmd_parsed

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF


def test_parse_invalid_cmd_execute_cmd_tag():
    """CmdExecute tag validity test."""
    cmd = CmdExecute(address=0)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdExecute.parse(data)


def test_cmd_call():
    """Test address, info value, size after export and parsing of CmdCall command."""
    cmd = CmdCall(address=100)
    assert cmd.address == 100
    assert cmd.info()

    data = cmd.export()
    assert len(data) == BaseCmd.SIZE

    cmd_parsed = CmdCall.parse(data=data)
    assert cmd == cmd_parsed

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF


def test_parse_invalid_cmd_call_cmd_tag():
    """CmdCall tag validity test."""
    cmd = CmdCall(address=0)
    cmd.cmd_tag = EnumCmdTag.ERASE
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdCall.parse(data=data)


def test_program_cmd_progfuses():
    """Test address, values, info value, size after export and parsing of CmdProgFuses command."""
    cmd = CmdProgFuses(address=100, data=[0, 1, 2, 3])
    assert cmd.address == 100
    assert cmd.data == [0, 1, 2, 3]
    assert cmd.length == 4
    assert cmd.info()

    cmd.data = [0, 1, 2, 3, 4]
    assert cmd.length == 5

    data = cmd.export()
    assert len(data) == BaseCmd.SIZE + 5 * 4

    cmd_parsed = CmdProgFuses.parse(data=data)
    assert cmd == cmd_parsed

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF


def test_parse_invalid_cmd_progfuses_cmd_tag():
    """CmdProgFuses tag validity test."""
    cmd = CmdProgFuses(address=0, data=[0, 1, 2, 3])
    cmd.cmd_tag = EnumCmdTag.LOAD
    data = cmd.export()
    with pytest.raises(Exception):
        CmdProgFuses.parse(data=data)


def test_cmd_progifr():
    """Test address, data, info value, size after export and parsing of CmdProgIfr command."""
    cmd = CmdProgIfr(address=100, data=bytes([0] * 100))
    assert cmd.address == 100
    assert cmd.data == bytes([0] * 100)
    assert cmd.info()

    data = cmd.export()
    assert len(data) == BaseCmd.SIZE + len(cmd.data)

    cmd_parsed = CmdProgIfr.parse(data=data)
    assert cmd == cmd_parsed

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF


def test_parse_invalid_cmd_progifr_cmd_tag():
    """CmdProgFuses tag validity test."""
    cmd = CmdProgIfr(address=100, data=bytes([0] * 100))
    cmd.cmd_tag = EnumCmdTag.LOAD
    data = cmd.export()
    with pytest.raises(Exception):
        CmdProgFuses.parse(data=data)


def test_cmd_loadcmac():
    """Test address, length, memory_id, info value, size after export and parsing of CmdLoadCmac command."""
    cmd = CmdLoadCmac(address=100, length=0, memory_id=0)
    assert cmd.address == 100
    assert cmd.length == 0
    assert cmd.memory_id == 0
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdLoadCmac.parse(data=data)
    assert cmd.address == cmd_parsed.address
    assert cmd.length == cmd_parsed.length
    assert cmd.memory_id == cmd_parsed.memory_id

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF
    assert 0x00000000 <= cmd.length <= 0xFFFFFFFF


def test_parse_invalid_cmd_loadcmac_cmd_tag():
    """CmdLoadCmac tag validity test."""
    cmd = CmdLoadCmac(address=0, length=0, memory_id=0)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdLoadCmac.parse(data=data)


def test_cmd_copy():
    """Test address, length, destination_address, memory_id_from, memory_id_to, info value,
    size after export and parsing of CmdCopy command."""
    cmd = CmdCopy(address=100, length=0, destination_address=0, memory_id_from=0, memory_id_to=0)
    assert cmd.address == 100
    assert cmd.length == 0
    assert cmd.destination_address == 0
    assert cmd.memory_id_from == 0
    assert cmd.memory_id_to == 0
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdCopy.parse(data=data)
    assert cmd.address == cmd_parsed.address
    assert cmd.length == cmd_parsed.length
    assert cmd.destination_address == cmd_parsed.destination_address
    assert cmd.memory_id_from == cmd_parsed.memory_id_from
    assert cmd.memory_id_to == cmd_parsed.memory_id_to

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF
    assert 0x00000000 <= cmd.length <= 0xFFFFFFFF


def test_parse_invalid_cmd_copy_cmd_tag():
    """CmdCopy tag validity test."""
    cmd = CmdCopy(address=100, length=0, destination_address=0, memory_id_from=0, memory_id_to=0)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdLoadCmac.parse(data=data)


def test_cmd_loadhashlocking():
    """Test address, length, memory_id, info value, size after export and parsing of CmdHashLocking command."""
    cmd = CmdLoadHashLocking(address=100, length=0, memory_id=0)
    assert cmd.address == 100
    assert cmd.length == 0
    assert cmd.memory_id == 0
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdLoadHashLocking.parse(data=data)
    assert cmd.address == cmd_parsed.address
    assert cmd.length == cmd_parsed.length
    assert cmd.memory_id == cmd_parsed.memory_id

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF
    assert 0x00000000 <= cmd.length <= 0xFFFFFFFF


def test_parse_invalid_cmd_loadhashlocking_cmd_tag():
    """CmdLoadCmac tag validity test."""
    cmd = CmdLoadHashLocking(address=0, length=0, memory_id=0)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdLoadHashLocking.parse(data=data)


def test_cmd_loadkeyblob():
    """Test offset, length, key_wrap, data info value, size after export and parsing of CmdLoadKeyBlob command."""
    cmd = CmdLoadKeyBlob(offset=100, key_wrap_id=CmdLoadKeyBlob.NXP_CUST_KEK_EXT_SK, data=10 * b"x")
    assert cmd.address == 100
    assert cmd.length == 10
    assert cmd.key_wrap_id == 17
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdLoadKeyBlob.parse(data=data)
    assert cmd == cmd_parsed
    assert cmd.data == cmd_parsed.data == 10 * b"x"


def test_parse_invalid_cmd_loadkeyblob_cmd_tag():
    """CmdLoadKeyBlob tag validity test."""
    cmd = CmdLoadKeyBlob(offset=100,  key_wrap_id=CmdLoadKeyBlob.NXP_CUST_KEK_EXT_SK, data=bytes(10))
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdErase.parse(data=data)


def test_cmd_configurememory():
    """Test address, memory_id, info value, size after export and parsing of CmdConfigureMemory command."""
    cmd = CmdConfigureMemory(address=100, memory_id=0)
    assert cmd.address == 100
    assert cmd.memory_id == 0
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdConfigureMemory.parse(data=data)
    assert cmd.address == cmd_parsed.address
    assert cmd.memory_id == cmd_parsed.memory_id

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF


def test_parse_invalid_cmd_configurememory_cmd_tag():
    """CmdConfigureMemory tag validity test."""
    cmd = CmdConfigureMemory(address=0, memory_id=0)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdConfigureMemory.parse(data=data)


def test_cmd_fillmemory():
    """Test address, length, info value, size after export and parsing of CmdFillMemory command."""
    cmd = CmdFillMemory(address=100, length=0, memory_id=0)
    assert cmd.address == 100
    assert cmd.length == 0
    assert cmd.memory_id == 0
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdFillMemory.parse(data=data)
    assert cmd.address == cmd_parsed.address
    assert cmd.length == cmd_parsed.length
    assert cmd.memory_id == cmd_parsed.memory_id

    assert 0x00000000 <= cmd.address <= 0xFFFFFFFF
    assert 0x00000000 <= cmd.length <= 0xFFFFFFFF


def test_parse_invalid_cmd_fillmemory_cmd_tag():
    """CmdFillMemory tag validity test."""
    cmd = CmdFillMemory(address=0, length=0, memory_id=0)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdFillMemory.parse(data=data)


def test_cmd_fwversioncheck():
    """Test value, counter_id, info value, size after export and parsing of CmdFwVersionCheck command."""
    cmd = CmdFwVersionCheck(value=100, counter_id=CmdFwVersionCheck.SECURE)
    assert cmd.value == 100
    assert cmd.counter_id == 2
    assert cmd.info()

    data = cmd.export()
    assert len(data) % 16 == 0

    cmd_parsed = CmdFwVersionCheck.parse(data=data)
    assert cmd.value == cmd_parsed.value
    assert cmd.counter_id == cmd_parsed.counter_id

    assert 0x00000000 <= cmd.value <= 0xFFFFFFFF


def test_parse_invalid_cmd_fwversioncheck_cmd_tag():
    """CmdFwVersionCheck tag validity test."""
    cmd = CmdFwVersionCheck(value=100, counter_id=CmdFwVersionCheck.SECURE)
    cmd.cmd_tag = EnumCmdTag.CALL
    data = cmd.export()
    with pytest.raises(ValueError):
        CmdFwVersionCheck.parse(data=data)


def test_section_header_cmd():
    """Test section uid, section type, length, info value, size after append, export and parsing of
    CmdSectionHeader command."""
    cmd = CmdSectionHeader(section_uid=10, section_type=10, length=100)
    assert cmd.section_uid == 10
    assert cmd.section_type == 10
    assert cmd.length == 100

    data = cmd.export()
    assert len(data) == BaseCmd.SIZE

    cmd_parsed = CmdSectionHeader.parse(data=data)
    assert cmd_parsed.section_uid == 10
    assert cmd_parsed.section_type == 10
    assert cmd_parsed.length == 100


def test_section_cmd_header_basic():
    """Test whether two section headers cmd are identical."""
    section_header = CmdSectionHeader(section_uid=10)
    section_header2 = CmdSectionHeader(section_uid=500)

    assert section_header != section_header2, "Two different images are the same!"


def test_section_cmd_header_info():
    """Test presence of all keywords in info() method of section header cmd."""
    section_header = CmdSectionHeader()
    output = section_header.info()
    required_strings = ["UID", "Type"]
    for required_string in required_strings:
        assert required_string in output, f"String {required_string} is not in output"


def test_section_cmd_header_offset():
    """Section header cmd size validity test."""
    section_header = CmdSectionHeader()
    data = section_header.export()
    with pytest.raises(ValueError):
        CmdSectionHeader.parse(data=data, offset=50)


def test_parse_command_function():
    """Test parse command function."""
    # CmdErase(address=100, length=0, memory_id=0)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdErase)

    # CmdLoad(address=100, length=0, memory_id=0)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdLoad)

    # CmdExecute(address=100)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdExecute)

    # CmdCall(address=100)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdCall)

    # CmdProgFuses(address=100, data=[0, 1, 2, 3])
    data = b'U\xaa\xaaUd\x00\x00\x00\x05\x00\x00\x00\x05\x00\x00\x00' \
           b'\x00\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00' \
           b'\x00\x00\x04\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdProgFuses)

    # CmdProgIfr(address=100, data=(b"\x00" * 100))
    data = b'U\xaa\xaaUd\x00\x00\x00d\x00\x00\x00\x06\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdProgIfr)

    # CmdLoadCmac(address=100, length=0, memory_id=0)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdLoadCmac)

    # CmdCopy(address=100, length=0, destination_address=0, memory_id_from=0, memory_id_to=0)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdCopy)

    # CmdLoadHashLocking(address=100, length=0, memory_id=0)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdLoadHashLocking)

    # CmdLoadKeyBlob(offset=100, key_wrap_id=CmdLoadKeyBlob.NXP_CUST_KEK_EXT_SK, data=10 * b"x")
    data = b'U\xaa\xaaUd\x00\x11\x00\n\x00\x00\x00\n\x00\x00\x00xxxxxxxxxx' \
           b'\x00\x00\x00\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdLoadKeyBlob)

    # CmdConfigureMemory(address=100, memory_id=0)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\x0b\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdConfigureMemory)

    # CmdFillMemory(address=100, memory_id=0)
    data = b'U\xaa\xaaUd\x00\x00\x00\x00\x00\x00\x00\x0c\x00\x00\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdFillMemory)

    # CmdFwVersionCheck(value=100, counter_id=CmdFwVersionCheck.SECURE)
    data = b'U\xaa\xaaUd\x00\x00\x00\x02\x00\x00\x00\r\x00\x00\x00'
    parse = parse_command(data)
    assert isinstance(parse, CmdFwVersionCheck)


def test_invalid_parse_command_function():
    """Test invalid parse command function."""
    invalid_data = b'U\xaa\xaaUd\x00\x00\x00\t\x00\x00\x00\x00\x00\x00\x00'
    with pytest.raises(ValueError):
        parse_command(invalid_data)
    invalid_data = bytes(CmdSectionHeader.SIZE)
    with pytest.raises(AssertionError):
        parse_command(invalid_data)

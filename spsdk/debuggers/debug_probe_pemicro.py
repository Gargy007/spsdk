#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright 2020 NXP
#
# SPDX-License-Identifier: BSD-3-Clause
"""Module for DebugMailbox Pemicro Debug probes support."""

import logging
from typing import List, Dict, Optional

from pypemicro import PyPemicro, PEMicroException, PEMicroInterfaces

from .debug_probe import (DebugProbe,
                          ProbeDescription,
                          DebugProbeTransferError,
                          DebugProbeNotOpenError,
                          DebugProbeError)

logger = logging.getLogger(__name__)
logger.setLevel(logging.CRITICAL)
PEMICRO_LOGGER = logger.getChild("PyPemicro")


class DebugProbePemicro(DebugProbe):
    """Class to define Pemicro package interface for NXP SPSDK."""

    @classmethod
    def get_pemicro_lib(cls) -> PyPemicro:
        """Get J-Link object.

        :return: The J-Link Object
        :raises DebugProbeError: The J-Link object get function failed.
        """
        return PyPemicro(log_info=PEMICRO_LOGGER.info, log_debug=PEMICRO_LOGGER.debug,
                         log_err=PEMICRO_LOGGER.error, log_war=PEMICRO_LOGGER.warn)

    def __init__(self, hardware_id: str, user_params: Dict = None) -> None:
        """The Pemicro class initialization.

        The Pemicro initialization function for SPSDK library to support various DEBUG PROBES.
        """
        super().__init__(hardware_id, user_params)

        self.pemicro: Optional[PyPemicro] = None

        logger.debug(f"The SPSDK Pemicro Interface has been initialized")

    @classmethod
    def get_connected_probes(cls, hardware_id: str = None, user_params: Dict = None) -> List[ProbeDescription]:
        """Get all connected probes over Pemicro.

        This functions returns the list of all connected probes in system by Pemicro package.
        :param hardware_id: None to list all probes, otherwice the the only probe with matching
            hardware id is listed.
        :param user_params: The user params dictionary
        :return: probe_description
        """
        #TODO fix problems with cyclic import
        from .utils import DebugProbes

        pemicro = DebugProbePemicro.get_pemicro_lib()

        probes = DebugProbes()
        connected_probes = pemicro.list_ports()
        for probe in connected_probes:
            probes.append(ProbeDescription("PEMicro",
                                           probe["id"],
                                           probe["description"],
                                           DebugProbePemicro))

        return probes

    def open(self) -> None:
        """Open Pemicro interface for NXP SPSDK.

        The Pemicro opening function for SPSDK library to support various DEBUG PROBES.
        The function is used to initialize the connection to target and enable using debug probe
        for DAT purposes.
        :raises ProbeNotFoundError: The probe has not found
        :raises DebugMailBoxAPNotFoundError: The debug mailbox access port NOT found
        :raises DebugProbeError: The Pemicro cannot establish communication with target
        """
        try:
            self.pemicro = DebugProbePemicro.get_pemicro_lib()
            if self.pemicro is None:
                raise DebugProbeError(f"Getting of J-Link library failed.")
        except DebugProbeError as exc:
            raise DebugProbeError(f"Getting of J-Link library failed({str(exc)}).")
        try:
            self.pemicro.open(debug_hardware_name_ip_or_serialnum=self.hardware_id)
            self.pemicro.connect(PEMicroInterfaces.SWD)  # type: ignore
            debugmb_dbgmlbx_ap_ix = self._get_dmbox_ap()
        except PEMicroException as exc:
            raise DebugProbeError(f"Pemicro cannot establish communication with target({str(exc)}).")

        if self.dbgmlbx_ap_ix == -1:
            if debugmb_dbgmlbx_ap_ix == -1:
                raise DebugProbeError(f"The Debug mailbox access port is not available!")
            self.dbgmlbx_ap_ix = debugmb_dbgmlbx_ap_ix
        else:
            if debugmb_dbgmlbx_ap_ix != self.dbgmlbx_ap_ix:
                logger.info(f"The detected debug mailbox accessport index is different to specified.")

    def close(self) -> None:
        """Close Pemicro interface.

        The Pemicro closing function for SPSDK library to support various DEBUG PROBES.
        """
        if self.pemicro:
            self.pemicro.close()

    def dbgmlbx_reg_read(self, addr: int = 0) -> int:
        """Read debug mailbox access port register.

        This is read debug mailbox register function for SPSDK library to support various DEBUG PROBES.
        :param addr: the register address
        :return: The read value of addressed register (4 bytes)
        :raises NotImplementedError: The dbgmlbx_reg_read is NOT implemented
        """
        return self._coresight_reg_read(addr=addr)

    def dbgmlbx_reg_write(self, addr: int = 0, data: int = 0) -> None:
        """Write debug mailbox access port register.

        This is write debug mailbox register function for SPSDK library to support various DEBUG PROBES.
        :param addr: the register address
        :param data: the data to be written into register
        :raises NotImplementedError: The dbgmlbx_reg_write is NOT implemented
        """
        self._coresight_reg_write(addr=addr, data=data)

    def _coresight_reg_read(self, access_port: bool = True, addr: int = 0) -> int:
        """Read coresight register over Pemicro interface.

        The Pemicro read coresight register function for SPSDK library to support various DEBUG PROBES.
        :param access_port: if True, the Access Port (AP) register will be read(default), otherwise the Debug Port
        :param addr: the register address
        :return: The read value of addressed register (4 bytes)
        :raises DebugProbeTransferError: The IO operation failed
        :raises DebugProbeNotOpenError: The Pemicro probe is NOT opened

        """
        if self.pemicro is None:
            raise DebugProbeNotOpenError("The Pemicro debug probe is not opened yet")

        try:
            if access_port:
                addr_ap = addr | ((self.dbgmlbx_ap_ix << self.APSEL_SHIFT) & self.APSEL_APBANKSEL)
                ret = self.pemicro.read_ap_register(apselect=self.dbgmlbx_ap_ix,
                                                    addr=addr_ap)
            else:
                ret = self.pemicro.read_dp_register(addr=addr)
            return ret
        except PEMicroException as exc:
            raise DebugProbeTransferError(f"The Coresight read operation failed({str(exc)}).")

    def _coresight_reg_write(self, access_port: bool = True, addr: int = 0, data: int = 0) -> None:
        """Write coresight register over Pemicro interface.

        The Pemicro write coresight register function for SPSDK library to support various DEBUG PROBES.
        :param access_port: if True, the Access Port (AP) register will be write(default), otherwise the Debug Port
        :param addr: the register address
        :param data: the data to be written into register
        :raises DebugProbeTransferError: The IO operation failed
        :raises DebugProbeNotOpenError: The Pemicro probe is NOT opened
        """
        if self.pemicro is None:
            raise DebugProbeNotOpenError("The Pemicro debug probe is not opened yet")

        try:
            if access_port:
                addr_ap = addr | ((self.dbgmlbx_ap_ix << self.APSEL_SHIFT) & self.APSEL_APBANKSEL)
                self.pemicro.write_ap_register(apselect=self.dbgmlbx_ap_ix,
                                               addr=addr_ap,
                                               value=data)
            else:
                self.pemicro.write_dp_register(addr=addr, value=data)

        except PEMicroException as exc:
            raise DebugProbeTransferError(f"The Coresight write operation failed({str(exc)}).")

    def _get_dmbox_ap(self) -> int:
        """Search for Debug Mailbox Access Point.

        This is helper function to find and return the debug mailbox access port index.
        :return: Debug MailBox Access Port Index if found, otherwise -1
        :raises DebugProbeNotOpenError: The PEMicro probe is NOT opened
        """
        idr_expected = 0x002A0000
        idr_address = 0xFC

        if self.pemicro is None:
            raise DebugProbeNotOpenError("The Pemicro debug probe is not opened yet")

        logger.debug(f"Looking for debug mailbox access port")

        for access_port_ix in range(256):
            try:
                address = idr_address | ((access_port_ix << self.APSEL_SHIFT) & self.APSEL_APBANKSEL)
                ret = self.pemicro.read_ap_register(apselect=access_port_ix,
                                                    addr=address)

                if ret == idr_expected:
                    logger.debug(f"Found debug mailbox ix:{access_port_ix}")
                    return access_port_ix
                if ret != 0:
                    logger.debug(f"Found general access port ix:{access_port_ix}")
                else:
                    logger.debug(f"The AP({access_port_ix}) is not available")
            except PEMicroException:
                logger.debug(f"The AP({access_port_ix}) is not available")

        return -1

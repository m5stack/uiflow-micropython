# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


from driver.drf1609h import DRF1609H
from driver.soft_timer import SoftTimer
import machine
import sys

if sys.platform != "esp32":
    from typing import Literal


class ZigbeeUnit(DRF1609H):
    DEVICE_TYPE_COORDINATOR = 0x01
    DEVICE_TYPE_ROUTER = 0x02
    DEVICE_TYPE_END_DEVICE = 0x03

    ANT_TYPRE_ON_BOARD = 0x00
    ANT_TYPRE_EXTERNAL = 0x01

    TRANSFER_MODE_PASS_THROUGH = 0x01
    TRANSFER_MODE_PASS_THROUGH_AND_CUSTOM_ADDRESS = 0x02
    TRANSFER_MODE_PASS_THROUGH_AND_SHORT_ADDRESS = 0x03
    TRANSFER_MODE_PASS_THROUGH_AND_MAC_ADDRESS = 0x04
    TRANSFER_MODE_P2P = 0x05

    ENCRYPTION_ENABLE = 0xA1
    ENCRYPTION_DISABLE = 0xA0

    def __init__(self, id: Literal[0, 1, 2], port: list | tuple, verbose: bool = True) -> None:
        uart1 = machine.UART(id, 38400, tx=port[1], rx=port[0])
        super().__init__(uart1, verbose=verbose)
        self._timer = SoftTimer()
        self._receive_callback = None

    def set_module_param(
        self,
        device_type,
        pan_id,
        channel,
        transfer_mode,
        custom_address,
        ant_type=ANT_TYPRE_EXTERNAL,
        encryption_enable=ENCRYPTION_ENABLE,
        encryption_key=b"\x11\x12\x13\x14",
        node_type=DEVICE_TYPE_ROUTER,
        node_ant_type=ANT_TYPRE_EXTERNAL,
        node_transfer_mode=TRANSFER_MODE_PASS_THROUGH,
        node_custom_address=0x0066,
    ):
        parameter = self.parameter.deepcopy()
        router = self.router.deepcopy()
        self.parameter.device_type = device_type
        self.parameter.pan_id = pan_id
        self.parameter.channel = channel
        self.parameter.transfer_mode = transfer_mode
        self.parameter.custom_address = custom_address
        self.parameter.ant_type = ant_type
        self.parameter.encryption_enable = encryption_enable
        self.parameter.password = encryption_key
        self.router.device_type = node_type
        self.router.ant_type = node_ant_type
        self.router.transfer_mode = node_transfer_mode
        self.router.custom_address = node_custom_address
        if self.write_module_param_command():
            self.restart_command()
        else:
            self.parameter.device_type = parameter.device_type
            self.parameter.device_type = parameter.pan_id
            self.parameter.channel = parameter.channel
            self.parameter.transfer_mode = parameter.transfer_mode
            self.parameter.custom_address = parameter.custom_address
            self.parameter.ant_type = parameter.ant_type
            self.parameter.encryption_enable = parameter.encryption_enable
            self.parameter.password = parameter.password
            self.router.device_type = router.device_type
            self.router.ant_type = router.ant_type
            self.router.transfer_mode = router.transfer_mode
            self.router.custom_address = router.custom_address
        del parameter, router

    def set_device_type(self, device_type):
        t = self.parameter.device_type
        self.parameter.device_type = device_type
        if self.write_module_param_command():
            self.restart_command()
        else:
            self.parameter.device_type = t

    def set_pan_id(self, pan_id):
        t = self.parameter.pan_id
        self.parameter.pan_id = pan_id
        if self.write_module_param_command():
            self.restart_command()
        else:
            self.parameter.pan_id = t

    def set_channel(self, channel):
        t = self.parameter.channel
        self.parameter.channel = channel
        if self.write_module_param_command():
            self.restart_command()
        else:
            self.parameter.channel = t

    def set_transfer_mode(self, transfer_mode):
        t = self.parameter.transfer_mode
        self.parameter.transfer_mode = transfer_mode
        if self.write_module_param_command():
            self.restart_command()
        else:
            self.parameter.transfer_mode = t

    def set_custom_address(self, address):
        t = self.parameter.custom_address
        self.parameter.custom_address = address
        if self.write_module_param_command():
            self.restart_command()
        else:
            self.parameter.custom_address = t

    def set_ant_type(self, ant_type):
        t = self.parameter.ant_type
        self.parameter.ant_type = ant_type
        if self.write_module_param_command():
            self.restart_command()
        else:
            self.parameter.ant_type = t

    def get_short_address(self):
        self.read_module_param_command()
        return self.router.short_address

    def get_custom_address(self):
        self.read_module_param_command()
        return self.parameter.custom_address

    def isconnected(self) -> bool:
        self.read_module_param_command()
        return True if self.router.short_address != 0xFFFE else False

    def receive_none_block(self, receive_callback):
        self._receive_callback = receive_callback
        self._timer.init(period=1000, mode=SoftTimer.PERIODIC, callback=self.receive_task)

    def receive_task(self):
        msg = self.receive()
        msg and self._receive_callback(msg[0], msg[2], msg[1])

    def stop_receive(self):
        self._timer.deinit()

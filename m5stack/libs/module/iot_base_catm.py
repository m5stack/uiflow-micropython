# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.sim7080 import SIM7080
from driver.modbus.master.uSerial import uSerial
import M5
from collections import namedtuple
from .module_helper import ModuleError
import time

AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])
MBusIO = namedtuple("MBusIO", ["modem_tx", "modem_rx", "rs485_tx", "rs485_rx", "pwr_ctrl"])

iomap = {
    M5.BOARD.M5Stack: MBusIO(0, 35, 15, 13, 12),
    M5.BOARD.M5StackCore2: MBusIO(0, 35, 2, 19, 27),
    M5.BOARD.M5StackCoreS3: MBusIO(0, 10, 13, 7, 6),
    M5.BOARD.M5Tough: MBusIO(0, 35, 2, 19, 27),
    M5.BOARD.M5Tab5: MBusIO(35, 16, 47, 48, 2),
}.get(M5.getBoard())


class IotBaseCatmModule(SIM7080, uSerial):
    def __init__(self) -> None:
        self.modem_uart = machine.UART(
            1,
            tx=iomap.modem_tx,
            rx=iomap.modem_rx,
            baudrate=115200,
            bits=8,
            parity=None,
            stop=1,
            rxbuf=1024,
        )
        SIM7080.__init__(self, uart=self.modem_uart)
        self.pwr_ctrl = machine.Pin(iomap.pwr_ctrl, machine.Pin.OUT)
        self.modem_power_ctrl(1)
        if not self.check_modem_is_ready():
            raise ModuleError("IoT Base CATM Module maybe not connect")
        self.set_command_echo_mode(0)

    def rs485_init(
        self,
        baudrate=9600,
        data_bits=8,
        stop_bits=1,
        parity=None,
    ):
        uSerial.__init__(
            self, 2, iomap.rs485_tx, iomap.rs485_rx, baudrate, data_bits, stop_bits, parity
        )

    def modem_power_ctrl(self, ctrl=1):
        if ctrl:
            self.pwr_ctrl.value(0)
            time.sleep_ms(500)
            self.pwr_ctrl.value(1)
            time.sleep_ms(1000)
            self.pwr_ctrl.value(0)
            time.sleep_ms(500)
        else:
            self.check_modem_is_ready()
            CPOWD = AT_CMD("AT+CPOWD=1", "NORMAL POWER DOWN", 3)  # noqa: N806
            output, error = self.execute_at_command(CPOWD)
            return not error

    def write(self, payload):
        self._mdbus_uart.write(payload)

    def read(self, byte=None):
        if byte is not None:
            return self._mdbus_uart.read(byte)
        else:
            return self._mdbus_uart.read()

    def readline(self):
        return self._mdbus_uart.readline()

    def any(self):
        return self._mdbus_uart.any()

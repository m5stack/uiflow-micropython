# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C, UART
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time
import sys

if sys.platform != "esp32":
    from typing import Literal

# I2C Register Map
QRCODE_ADDR = 0x21
QRCODE_TRIGGER_REG = 0x0000
QRCODE_READY_REG = 0x0010
QRCODE_LENGTH_REG = 0x0020
QRCODE_TRIGGER_MODE_REG = 0x0030
QRCODE_TRIGGER_BUTTON_REG = 0x0040
FIRMWARE_VERSION_REG = 0x00FE
I2C_ADDRESS_REG = 0x00FF
QRCODE_DATA_REG = 0x1000

# UART Send Command
QRCODE_TX_CONFIG = [0x21, 0x61, 0x41, 0x00]
QRCODE_TX_CONTROL = [0x32, 0x75, 0x01]

# UART Resp Command
QRCODE_RX_CONFIG = [0x22, 0x61, 0x41, 0x00, 0x00]
QRCODE_RX_CONTROL = [0x33, 0x75, 0x02, 0x00, 0x00]

I2C_MODE = 0
UART_MODE = 1


class QRCodeUnit:
    def __init__(
        self,
        mode: int = I2C_MODE,
        i2c: I2C | PAHUBUnit = None,
        address: int | list | tuple = QRCODE_ADDR,
        id: Literal[0, 1, 2] = 1,
        port: list | tuple = None,
    ) -> None:
        #! initialize the I2C or UART mode
        self.mode = mode
        if mode == I2C_MODE:
            self._i2c = i2c
            self.i2c_addr = address
            self.device_available()
        elif mode == UART_MODE:
            self._uart = UART(id, tx=port[1], rx=port[0])
            self._uart.init(115200, bits=8, parity=None, stop=1)

    def device_available(self):
        #! check the device is available or not
        if self.i2c_addr not in self._i2c.scan():
            raise UnitError("QR Code unit maybe not found in Grove")

    def set_manual_scan(self, ctrl: int = 0) -> None:
        #! set the manual scanning control ON or OFF
        if self.mode == I2C_MODE:
            self._i2c.writeto(
                self.i2c_addr, QRCODE_TRIGGER_REG.to_bytes(2, "little") + bytes([ctrl])
            )

        elif self.mode == UART_MODE:
            QRCODE_TX_CONTROL[2] = 1 if ctrl else 2
            self.cmd_send_resp(QRCODE_TX_CONTROL, (None if ctrl else QRCODE_RX_CONTROL))

    def get_qrcode_data_status(self) -> int:
        #! get the qr code data status
        if self.mode == I2C_MODE:
            self._i2c.writeto(self.i2c_addr, QRCODE_READY_REG.to_bytes(2, "little"))
            return self._i2c.readfrom(self.i2c_addr, 1)[0]

    def clear_qrcode_data_status(self) -> None:
        #! clear the data status
        if self.mode == I2C_MODE:
            self._i2c.writeto(self.i2c_addr, QRCODE_READY_REG.to_bytes(2, "little") + bytes([0]))

    def get_qrcode_data_length(self) -> int:
        #! get the qr code data length
        if self.mode == I2C_MODE:
            self._i2c.writeto(self.i2c_addr, QRCODE_LENGTH_REG.to_bytes(2, "little"))
            self.qr_code_len = self._i2c.readfrom(self.i2c_addr, 2)
            self.qr_code_len = int.from_bytes(self.qr_code_len, "little")
            return self.qr_code_len

        elif self.mode == UART_MODE:
            return self._uart.any()

    def get_qrcode_data(self, decode: bool = False) -> int:
        #! get the qr code data
        if self.get_qrcode_data_length():
            if self.mode == I2C_MODE:
                self._i2c.writeto(self.i2c_addr, QRCODE_DATA_REG.to_bytes(2, "little"))
                qr_data = self._i2c.readfrom(self.i2c_addr, self.qr_code_len)
                return qr_data.decode() if decode else qr_data

            elif self.mode == UART_MODE:
                return self._uart.read().decode() if decode else self._uart.read()

    def get_trigger_mode(self) -> int:
        #! get the auto or manual trigger mode status
        if self.mode == I2C_MODE:
            self._i2c.writeto(self.i2c_addr, QRCODE_TRIGGER_MODE_REG.to_bytes(2, "little"))
            return self._i2c.readfrom(self.i2c_addr, 1)[0]

    def set_trigger_mode(self, mode: int = 0) -> None:
        #! set the auto or manual trigger mode
        if self.mode == I2C_MODE:
            self._i2c.writeto(
                self.i2c_addr, QRCODE_TRIGGER_MODE_REG.to_bytes(2, "little") + bytes([mode])
            )

        elif self.mode == UART_MODE:
            QRCODE_TX_CONFIG[3] = 0 if mode else 5
            QRCODE_RX_CONFIG[3] = 0 if mode else 5
            self.cmd_send_resp(QRCODE_TX_CONFIG, QRCODE_RX_CONFIG)

    def get_trigger_button_status(self) -> bool:
        #! get the trigger button status
        if self.mode == I2C_MODE:
            self._i2c.writeto(self.i2c_addr, QRCODE_TRIGGER_BUTTON_REG.to_bytes(2, "little"))
            return not bool(self._i2c.readfrom(self.i2c_addr, 1)[0])

    def get_device_info(self, info: int = FIRMWARE_VERSION_REG) -> int:
        #! get the device information
        if self.mode == I2C_MODE:
            self._i2c.writeto(self.i2c_addr, info.to_bytes(2, "little"))
            return self._i2c.readfrom(self.i2c_addr, 1)[0]

    def set_device_i2c_address(self, addr: int = QRCODE_ADDR) -> None:
        #! set the device i2c address
        if self.mode == I2C_MODE:
            addr = max(1, min(addr, 127))
            self._i2c.writeto(self.i2c_addr, I2C_ADDRESS_REG.to_bytes(2, "little") + bytes([addr]))
            self.i2c_addr = addr
            time.sleep_ms(100)

    def set_event_cb(self, callback) -> None:
        #! set event callback function
        self.event_callback = callback

    def event_poll_loop(self) -> None:
        #! event polling inside the loop
        if self.mode == I2C_MODE:
            if self.get_qrcode_data_status():
                self.event_callback(self.get_qrcode_data(True))
                self.clear_qrcode_data_status()

        elif self.mode == UART_MODE:
            if self._uart.any():
                self.event_callback(self.get_qrcode_data(True))

    def cmd_send_resp(self, tx_cmd, rx_cmd=None, timeout=2000) -> list:
        self._uart.read()  # clear uart rx buffer
        self._uart.write(bytes(tx_cmd))
        if rx_cmd is not None:
            return self.wait_resp_cmd(bytes(rx_cmd), timeout)

    def wait_resp_cmd(self, keyword, timeout=2000) -> None:
        time.sleep(0.1)
        time_out = time.time() + int(timeout / 1000)
        while time.time() < time_out:
            time.sleep_ms(50)
            if self._uart.any():
                line = self._uart.read()
                if keyword in line:
                    return True
                else:
                    raise UnitError("QRCode Wrong Response:", line)

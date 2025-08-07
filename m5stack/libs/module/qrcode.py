# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
from driver.qrcode.qrcode_m14 import QRCodeM14
from module.mbus import i2c1


class QRCodeModule(QRCodeM14):
    # PI4IOE register
    PI4IO_REG_CHIP_RESET = const(0x01)
    PI4IO_REG_IO_DIR = const(0x03)
    PI4IO_REG_OUT_SET = const(0x05)
    PI4IO_REG_OUT_H_IM = const(0x07)
    PI4IO_REG_IN_DEF_STA = const(0x09)
    PI4IO_REG_PULL_EN = const(0x0B)
    PI4IO_REG_PULL_SEL = const(0x0D)
    PI4IO_REG_IN_STA = const(0x0F)
    PI4IO_REG_INT_MASK = const(0x11)
    PI4IO_REG_IRQ_STA = const(0x13)

    """Create an AtomicQRCode2Base object.

    :param int id: UART id.
    :param int tx: the UART TX pin.
    :param int rx: the UART RX pin.
    :param int trig: the trigger pin.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import QRCodeModule

            module_qrcode = QRCodeModule(id = 1, tx = 17, rx = 18)
    """

    def __init__(self, id: int = 1, tx: int = 17, rx: int = 18):
        super().__init__(id, tx=rx, rx=tx)  # ???
        self.i2c = i2c1
        self.address = 0x43
        if self.address not in self.i2c.scan():
            raise RuntimeError("PI4IOE not found!")
        self.init_device()
        self.set_power(True)  # 默认开启电源
        time.sleep_ms(1000)  # wait for module startup.
        # Check Version
        if self.get_version() != "1.0":
            raise RuntimeError("Module13.2 QRCode not found!")

    def _write_reg(self, reg, value):
        self.i2c.writeto(self.address, bytes([reg, value]))

    def _read_reg(self, reg):
        self.i2c.writeto(self.address, bytes([reg]))
        return self.i2c.readfrom(self.address, 1)[0]

    def init_device(self):
        self._write_reg(self.PI4IO_REG_CHIP_RESET, 0xFF)  # 复位
        chip_id = self._read_reg(PI4IO_REG_CHIP_RESET)
        # print(f"Chip ID: {chip_id:#04x}")
        self._write_reg(self.PI4IO_REG_IO_DIR, 0b00010001)  # P4--QR_TRIG P0--PWR_EN 输出
        self._write_reg(self.PI4IO_REG_OUT_H_IM, 0b00000000)  # 关闭高阻态
        self._write_reg(self.PI4IO_REG_PULL_SEL, 0b11111111)  # 上拉配置
        self._write_reg(self.PI4IO_REG_PULL_EN, 0b11111111)  # 使能上拉
        self._write_reg(self.PI4IO_REG_OUT_SET, 0b00010001)  # 设定默认输出值

    def set_power(self, enable: bool = True) -> None:
        """Set power. 设置电源。

        :param enable: True - power on. 开启
                       False - power off. 关闭

        UiFlow2 Code Block:

            |set_power.png|

        MicroPython Code Block:

            .. code-block:: python

                module_qrcode.set_power(enable)
        """
        tmp = self._read_reg(self.PI4IO_REG_OUT_SET)
        if enable:
            tmp |= 0x01
        else:
            tmp &= 0xFE
        self._write_reg(self.PI4IO_REG_OUT_SET, tmp)

    def set_trig(self, value: int) -> None:
        """Set trigger value.

        :param int value: ``0`` - Low level, ``1`` - High level.

        UiFlow2 Code Block:

            |set_trig.png|

        MicroPython Code Block:

            .. code-block:: python

                module_qrcode.set_trig(value)
        """
        tmp = self._read_reg(self.PI4IO_REG_OUT_SET)
        if value:
            tmp |= 0x10
        else:
            tmp &= 0xEF
        self._write_reg(self.PI4IO_REG_OUT_SET, tmp)

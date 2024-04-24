# -*- encoding: utf-8 -*-
"""
@File    :   _dac2.py
@Time    :   2024/4/24
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import Pin, ADC
from driver.neopixel.sk6812 import SK6812

_PALETTE_HEX = (
    0xF80000,
    0xF00400,
    0xF00800,
    0xF00C00,
    0xF01000,
    0xF01400,
    0xF01800,
    0xF01C00,
    0xF02000,
    0xF02800,
    0xF02C00,
    0xF03000,
    0xF03400,
    0xF03800,
    0xF03C00,
    0xF04000,
    0xF04400,
    0xE84800,
    0xE84C00,
    0xE85000,
    0xE85400,
    0xE85800,
    0xE85C00,
    0xE86000,
    0xE86400,
    0xE86800,
    0xE86C00,
    0xE87000,
    0xE87400,
    0xE87800,
    0xE87C00,
    0xE88000,
    0xE88400,
    0xE88800,
    0xE08C00,
    0xE09000,
    0xE09400,
    0xE09800,
    0xE09C00,
    0xE0A000,
    0xE0A400,
    0xE0A800,
    0xE0AC00,
    0xE0B000,
    0xE0B400,
    0xE0B800,
    0xE0BC00,
    0xE0C000,
    0xE0C400,
    0xE0C800,
    0xE0CC00,
    0xDCCD00,
    0xD8D000,
    0xD8D400,
    0xD8D800,
    0xD8DC00,
    0xD8E000,
    0xD0E000,
    0xD0DC00,
    0xCCDC00,
    0xC8DC00,
    0xC4DC00,
    0xC0DC00,
    0xBCDC00,
    0xB8DC00,
    0xB4DC00,
    0xB0DC00,
    0xACDA00,
    0xA8D800,
    0xA0D800,
    0x9CD800,
    0x98D800,
    0x94D800,
    0x90D800,
    0x88D800,
    0x88D400,
    0x84D400,
    0x80D400,
    0x7CD400,
    0x78D400,
    0x74D400,
    0x70D400,
    0x68D400,
    0x68D000,
    0x64D000,
    0x60D000,
    0x5CD000,
    0x58D000,
    0x54D000,
    0x50D000,
    0x48D000,
    0x48CC00,
    0x44CC00,
    0x40CC00,
    0x3DCC00,
    0x3ACC00,
    0x38CC00,
    0x34CC00,
    0x30CC00,
    0x28CC00,
    0x28C800,
    0x24C800,
    0x20C800,
    0x1CC800,
    0x18C800,
    0x14C800,
    0x10C800,
    0x08C800,
    0x08C600,
    0x08C400,
    0x06C400,
    0x04C400,
    0x02C400,
    0x00C400,
    0x00C404,
    0x00C408,
    0x00C008,
    0x00C00C,
    0x00C010,
    0x00C014,
    0x00C018,
    0x00C01A,
    0x00C01D,
    0x00C020,
    0x00BE24,
    0x00BC28,
    0x00BC2A,
    0x00BC2D,
    0x00BC30,
    0x00BC34,
    0x00BC38,
    0x00BC3C,
    0x00BC40,
    0x00B840,
    0x00B844,
    0x00B848,
    0x00B84A,
    0x00B84D,
    0x00B850,
    0x00B854,
    0x00B858,
    0x00B458,
    0x00B45C,
    0x00B460,
    0x00B462,
    0x00B465,
    0x00B468,
    0x00B46C,
    0x00B470,
    0x00B070,
    0x00B072,
    0x00B075,
    0x00B078,
    0x00B07C,
    0x00B080,
    0x00B084,
    0x00B088,
    0x00AC88,
    0x00AC8A,
    0x00AC8D,
    0x00AC90,
    0x00AC92,
    0x00AC95,
    0x00AC98,
    0x00AC9C,
    0x00ACA0,
    0x00AAA0,
    0x00A8A0,
    0x00A6A0,
    0x00A4A0,
    0x00A0A0,
    0x009CA0,
    0x0098A0,
    0x0094A0,
    0x0090A0,
    0x008EA0,
    0x008CA0,
    0x0088A0,
    0x0084A0,
    0x0080A0,
    0x007CA0,
    0x007AA0,
    0x0078A0,
    0x0074A0,
    0x0070A0,
    0x006C98,
    0x006898,
    0x006698,
    0x006498,
    0x006098,
    0x005C98,
    0x005A98,
    0x005898,
    0x005498,
    0x005098,
    0x004C98,
    0x004A98,
    0x004898,
    0x004498,
    0x004098,
    0x003E98,
    0x003C98,
    0x003890,
    0x003490,
    0x003290,
    0x003090,
    0x002C90,
    0x002A90,
    0x002890,
    0x002490,
    0x002090,
    0x001E90,
    0x001C90,
    0x001890,
    0x001690,
    0x001490,
    0x001090,
    0x000E90,
    0x000C90,
    0x000888,
    0x000688,
    0x000488,
    0x000388,
    0x000288,
    0x000188,
    0x000088,
    0x000088,
    0x020088,
    0x050088,
    0x080088,
    0x0A0088,
    0x0D0088,
    0x100088,
    0x140088,
    0x180088,
    0x180084,
    0x180080,
    0x1A0080,
    0x1D0080,
    0x200080,
    0x220080,
    0x240080,
    0x260080,
    0x280080,
    0x2A0080,
    0x2D0080,
    0x300080,
    0x320080,
    0x340080,
    0x360080,
    0x380080,
    0x400080,
    0x40007D,
    0x40007A,
    0x400078,
    0x480078,
)


class FaderUnit(SK6812):
    """! UNIT FADER is a Slide Potentiometer with color indicator.

    @en UNIT FADER is a Slide Potentiometer with color indicator, employ a 35mm slide potentiometer + 14x SK6812 programmable RGB lights. The fader has its own center point positioning, and excellent slide appliances for stable, reliable performance and precise control. The integrated beads support digital addressing, which means you can adjust the brightness and color of each LED light. The product is suitable for lighting, music control, and other applications.
    @cn UNIT FADER是一款带有颜色指示灯的滑动电位器，采用35mm滑动电位器+14x SK6812可编程RGB灯。滑块具有自己的中心点定位，以及出色的滑动应用，以实现稳定、可靠的性能和精确控制。集成的珠子支持数字寻址，这意味着您可以调整每个LED灯的亮度和颜色。该产品适用于照明、音乐控制等应用。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/fader
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/fader/fader_01.webp
    @category unit

    @example
        from unit import FaderUnit
        fader = FaderUnit((33,32)) # for core2
        fader.update_color()

    """

    def __init__(self, port: tuple):
        """! Initialize the Fader.

        @param port The port to which the Fader is connected. port[0]: adc pin, port[1]: LEDs pin.
        """
        super().__init__(port[1], 14)
        self.port = port
        self._adc = ADC(Pin(port[0]), atten=ADC.ATTN_11DB)
        self.set_brightness(10)

    def get_voltage(self) -> float:
        """! Get the voltage of the Fader.

        @en %1 Get the voltage of the Fader.
        @cn %1 获取Fader的电压。
        @return: float, The voltage of the Fader.

        """

        return self._adc.read_uv() / 1000 / 1000

    def get_raw(self) -> int:
        """! Read the raw value of the ADC.

        @en %1 Read the raw value of the ADC.
        @cn %1 读取ADC的原始值。
        @return: int from 0 to 65535

        """

        return self._adc.read_u16()

    def update_color(self):
        """! Update the color based on adc value.

        @en %1 Update the color based on adc value.
        @cn %1 根据adc值更新颜色。

        """

        index = self._map(self.get_raw(), 0, 0xFFFF, 0, len(_PALETTE_HEX) - 1)
        self.fill_color(_PALETTE_HEX[index])

    def update_brightness(self):
        """! Update the brightness based on adc value.

        @en %1 Update the brightness based on adc value.
        @cn %1 根据adc值更新亮度。

        """
        self.fill(0xFFFFFF)
        self.set_brightness(self._map(self.get_raw(), 0, 0xFFFF, 0, 0xFF))

    def _map(self, val, in_min, in_max, out_min, out_max):
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

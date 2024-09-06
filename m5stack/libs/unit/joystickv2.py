# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import I2C
import struct
import time


class JoystickV2Unit:
    """
    note:
        en: The joystick is an input unit for control, utilizing an I2C communication interface and supporting three-axis control signals (X/Y-axis analog input for displacement and Z-axis digital input for key presses). It is ideal for applications like gaming and robot control.
        cn: 操纵杆是一种控制输入单元，采用I2C通信接口，支持三轴控制信号输入（X/Y轴位移的模拟输入和Z轴按键的数字输入）。适用于游戏、机器人控制等应用场景。

    details:
        color: "#0FE6D7"
        link: ""
        image: ""
        category: Unit

    example: |
        from unit import JoystickV2Unit
        from hardware import *
        i2c = I2C(1, scl=22, sda=21)
        joystick = JoystickV2Unit(i2c)
        joystick.read_adc_value()
        joystick.read_button_status()
        joystick.set_rgb_led(255, 0, 0)
        joystick.get_rgb_led()
        joystick.set_deadzone_position(200, 200)
        while True:
            joystick.read_axis_position()
    """

    def __init__(self, i2c: I2C, address: int | list | tuple = 0x63):
        """
        note: Initialize the JoystickV2 Unit.

        label:
            en: "%1 initialize JoystickV2 Unit with I2C %2, address %3"
            cn: "%1 初始化 JoystickV2 Unit，使用I2C %2，地址 %3"

        params:
            i2c:
              note: I2C port to use.
            address:
              note: I2C address of the JoystickV2 Unit.
        """
        self._color = [0, 0, 0]
        self._br = 1
        self._i2c = i2c
        self._addr = address
        self._x_inv = False
        self._y_inv = False
        self._swap = False
        self._x_mapping = [0, 0, 0, 0]
        self._y_mapping = [0, 0, 0, 0]
        if self._addr not in self._i2c.scan():
            raise Exception("JoystickV2Unit not found, please check if it's properly connected.")

    def _read_reg_data(self, reg: int = 0, num: int = 0) -> bytearray:
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self._i2c.writeto(self._addr, buf)
        buf = bytearray(num)
        self._i2c.readfrom_into(self._addr, buf)
        return buf

    def _write_reg_data(self, reg, byte_lst):
        buf = bytearray(1 + len(byte_lst))
        buf[0] = reg
        buf[1:] = bytes(byte_lst)
        time.sleep_ms(1)
        self._i2c.writeto(self._addr, buf)

    def set_axis_x_invert(self, invert: bool = True) -> None:
        """
        note: Invert the X-axis of the joystick.

        label:
            en: "%1 invert X-axis %2"
            cn: "%1 反转 X 轴 %2"

        params:
            invert:
              note: Whether to invert the X-axis.
        """
        self._x_inv = invert

    def set_axis_y_invert(self, invert: bool = True) -> None:
        """
        note: Invert the Y-axis of the joystick.

        label:
            en: "%1 invert Y-axis %2"
            cn: "%1 反转 Y 轴 %2"

        params:
            invert:
              note: Whether to invert the Y-axis.
        """
        self._y_inv = invert

    def set_axis_swap(self, swap: bool = True) -> None:
        """
        note: Swap the X-axis and Y-axis of the joystick.

        label:
            en: "%1 swap X and Y-axis %2"
            cn: "%1 交换 X 和 Y 轴 %2"

        params:
            swap:
              note: Whether to swap the X-axis and Y-axis.
        """
        self._swap = swap

    def get_adc_value(self) -> tuple:
        """
        note: Read the ADC value of the joystick.

        label:
            en: "%1 read ADC value"
            cn: "%1 读取ADC 值"

        return:
            note: Returns a tuple of the X-axis and Y-axis ADC values, from 0 to 65535
        """
        buf = self._read_reg_data(0x00, 4)
        x, y = struct.unpack("<hh", buf)
        if self._x_inv:
            x = 65535 - x
        if self._y_inv:
            y = 65535 - y
        if self._swap:
            x, y = y, x
        return (x, y)

    def get_button_status(self) -> bool:
        """
        note: Read the button status of the joystick.

        label:
            en: "%1 read button status of JoystickV2 Unit"
            cn: "%1 读取 JoystickV2 Unit 的按键状态"

        return:
            note: Returns the button status. True if pressed, False if not pressed.
        """
        return not bool(self._read_reg_data(0x20, 1)[0])

    def set_led_brightness(self, brightness: float) -> None:
        """
        note: Set the brightness of the RGB LED.

        label:
            en: "%1 set RGB LED brightness to %2"
            cn: "%1 设置 RGB LED 亮度为 %2"

        params:
            brightness:
              note: The brightness value (0-100).
        """
        self._br = brightness / 100
        self._write_reg_data(0x30, [int(c * self._br) for c in self._color])

    def fill_color(self, v) -> None:
        """
        note: Set the RGB LED color of the joystick.

        label:
            en: "%1 set RGB LED color of JoystickV2 Unit to (%2)"
            cn: "%1 设置 JoystickV2 Unit 的 RGB LED 颜色为 (%2)"

        params:
            v:
              note: The RGB value (0x000000-0xFFFFFF).
        """

        def color_to_bgr(c: int) -> tuple:
            # color: (R << 16 | G << 8 | B)
            v = []
            v.append(int(((c >> 0) & 0xFF) * self._br))  # B
            v.append(int(((c >> 8) & 0xFF) * self._br))  # G
            v.append(int(((c >> 16) & 0xFF) * self._br))  # R
            return list(v)

        self._color = color_to_bgr(v)
        self._write_reg_data(0x30, [int(c * self._br) for c in self._color])

    def fill_color_rgb(self, r: int, g: int, b: int) -> None:
        """
        note: Set the RGB LED color of the joystick.

        label:
            en: "%1 set RGB LED color of JoystickV2 Unit to (%2, %3, %4)"
            cn: "%1 设置 JoystickV2 Unit 的 RGB LED 颜色为 (%2, %3, %4)"

        params:
            r:
              note: The red value (0-255).
            g:
              note: The green value (0-255).
            b:
              note: The blue value (0-255).
        """
        self._color = [b, g, r]
        self._write_reg_data(0x30, [int(c * self._br) for c in self._color])

    def _set_mapping(
        self, adc_neg_min: int, adc_neg_max: int, adc_pos_min: int, adc_pos_max: int, axis_x=True
    ):
        buf = bytearray(8)
        struct.pack_into("<HHHH", buf, 0, adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max)
        if axis_x:
            self._write_reg_data(0x40, buf)
        else:
            self._write_reg_data(0x48, buf)

    def set_axis_x_mapping(
        self, adc_neg_min: int, adc_neg_max: int, adc_pos_min: int, adc_pos_max: int
    ) -> None:
        """
        note: |
            Set the mapping parameters of the X-axis.

            ADC Raw     0                                                    65536
                        |------------------------------------------------------|
            Mapped    -4096                   0           0                   4096
                        |---------------------|-dead zone-|--------------------|
                  adc_neg_min        adc_neg_max        adc_pos_min         adc_pos_max

        label:
            en: "%1 set mapping range neg min %2, neg max %3, pos min %4, pos max %5 of X-axis"
            cn: "%1 设置 X 轴的映射范围 负最小值 %2，负最大值 %3，正最小值 %4，正最大值 %5"

        params:
            adc_neg_min:
              note: The minimum ADC value of the negative range.
            adc_neg_max:
              note: The maximum ADC value of the negative range.
            adc_pos_min:
              note: The minimum ADC value of the positive range.
            adc_pos_max:
              note: The maximum ADC value of the positive range.
        """
        self._x_mapping = [adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max]
        self._set_mapping(adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max, True)

    def set_axis_y_mapping(
        self, adc_neg_min: int, adc_neg_max: int, adc_pos_min: int, adc_pos_max: int
    ) -> None:
        """
        note: |
            Set the mapping parameters of the Y-axis.

            ADC Raw     0                                                    65536
                        |------------------------------------------------------|
            Mapped    -4096                   0           0                   4096
                        |---------------------|-dead zone-|--------------------|
                  adc_neg_min        adc_neg_max        adc_pos_min         adc_pos_max

        label:
            en: "%1 set mapping range neg min %2, neg max %3, pos min %4, pos max %5 of Y-axis"
            cn: "%1 设置 Y 轴的映射范围 负最小值 %2，负最大值 %3，正最小值 %4，正最大值 %5"

        params:
            adc_neg_min:
              note: The minimum ADC value of the negative range.
            adc_neg_max:
              note: The maximum ADC value of the negative range.
            adc_pos_min:
              note: The minimum ADC value of the positive range.
            adc_pos_max:
              note: The maximum ADC value of the positive range.
        """
        self._y_mapping = [adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max]
        self._set_mapping(adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max, False)

    def set_deadzone_adc(self, x_adc_raw: int, y_adc_raw: int) -> None:
        """
        note: Set the dead zone of the joystick.

        label:
            en: "%1 set dead zone x %2, y %3"
            cn: "%1 设置死区 X %2，Y %3"

        params:
            x_adc_raw:
              note: The dead zone of the X-axis. Range is 0 to 32768.
            y_adc_raw:
              note: The dead zone of the Y-axis. Range is 0 to 32768.
        """
        half_x_adc_raw = x_adc_raw // 2
        half_y_adc_raw = y_adc_raw // 2
        self._x_mapping = [0, 32768 - half_x_adc_raw, 32768 + half_x_adc_raw, 65535]
        self._y_mapping = [0, 32768 - half_y_adc_raw, 32768 + half_y_adc_raw, 65535]
        self._set_mapping(*self._x_mapping, True)
        time.sleep_ms(100)
        self._set_mapping(*self._y_mapping, False)

    def set_deadzone_position(self, x_pos: int, y_pos: int) -> None:
        """
        note: Set the dead zone of the joystick.

        label:
            en: "%1 set dead zone x %2, y %3"
            cn: "%1 设置死区 X %2，Y %3"

        params:
            x_pos:
              note: The dead zone of the X-axis. Range is 0 to 4096.
            y_pos:
              note: The dead zone of the Y-axis. Range is 0 to 4096.
        """
        x_pct = x_pos / 4096
        y_pct = y_pos / 4096
        x_val = int(32768 * x_pct)
        y_val = int(32768 * y_pct)  # remap from 4096 to 0-32768
        self._x_mapping = [0, 32768 - x_val, 32768 + x_val, 65535]
        self._y_mapping = [0, 32768 - y_val, 32768 + y_val, 65535]
        self._set_mapping(*self._x_mapping, True)
        time.sleep_ms(100)
        self._set_mapping(*self._y_mapping, False)

    def get_axis_position(self) -> tuple:
        """
        note: Read the position of the joystick.

        label:
            en: "%1 read position of Joystick"
            cn: "%1 读取 Joystick 的位置"

        return:
            note: Returns a tuple of the X-axis and Y-axis positions. The range is -4096 to 4096.
        """
        buf = self._read_reg_data(0x50, 4)
        x, y = struct.unpack("<hh", buf)
        if self._x_inv:
            x = -x
        if self._y_inv:
            y = -y
        if self._swap:
            x, y = y, x
        return (x, y)

    def set_address(self, address: int) -> None:
        """
        note: Set the I2C address of the JoystickV2 Unit.

        label:
            en: "%1 set I2C address to %2"
            cn: "%1 设置 I2C 地址为 %2"

        params:
            address:
              note: The I2C address to set.
        """
        self._write_reg_data(0xFF, [address])
        self._addr = address

    def get_firmware_version(self) -> int:
        """
        note: Read the firmware version of the JoystickV2 Unit.

        label:
            en: "%1 read firmware version"
            cn: "%1 读取固件版本"

        return:
            note: Returns the firmware version.
        """
        return self._read_reg_data(0xFE, 1)[0]

    def get_x_raw(self) -> int:
        """
        note: Read the raw X-axis value of the joystick.

        label:
            en: "%1 read raw X-axis ADC value"
            cn: "%1 读取原始X轴ADC值"

        return:
            note: Returns the raw X-axis value.
        """
        return self.get_adc_value()[0]

    def get_y_raw(self) -> int:
        """
        note: Read the raw Y-axis value of the joystick.

        label:
            en: "%1 read raw Y-axis ADC value"
            cn: "%1 读取原始Y轴ADC值"

        return:
            note: Returns the raw Y-axis value.
        """
        return self.get_adc_value()[1]

    def get_x_position(self) -> int:
        """
        note: Read the X-axis position of the joystick.

        label:
            en: "%1 read X-axis position"
            cn: "%1 读取X轴位置"

        return:
            note: Returns the X-axis position.
        """
        return self.get_axis_position()[0]

    def get_y_position(self) -> int:
        """
        note: Read the Y-axis position of the joystick.

        label:
            en: "%1 read Y-axis position"
            cn: "%1 读取Y轴位置"

        return:
            note: Returns the Y-axis position.
        """
        return self.get_axis_position()[1]

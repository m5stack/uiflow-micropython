# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from micropython import const
from .pahub import PAHUBUnit
import time



class Step16Unit:
    """Create an Step16Unit object.

    :param I2C i2c: I2C port,
    :param int | list | tuple addr: Step16Unit Slave Address

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import Step16Unit

            unit_step16_0 = Step16Unit(i2c0, 0x48)
    """
    REG_ENCODER_VALUE = const(0x00) # Step16 编码器当前数值（有符号增量）
    REG_LED_WORK_MODE = const(0x10) # LED 工作模式
    REG_LED_BRIGHTNESS = const(0x20) # LED 全局亮度（0~100）
    REG_ENCODER_DIR_CFG = const(0x30) # 编码器方向配置（顺时针为加/减）
    REG_RGB_POWER = const(0x40) # RGB 灯电源控制
    REG_RGB_BRIGHTNESS = const(0x41) # RGB 灯亮度（0~255，用作 r/g/b 的亮度乘权）
    REG_RGB_R = const(0x50) # RGB 红色通道值（0~255）
    REG_RGB_G = const(0x51) # RGB 绿色通道值（0~255）
    REG_RGB_B = const(0x52) # RGB 蓝色通道值（0~255）
    REG_SAVE_CFG = const(0xF0) # 保存 LED 设置（模式、亮度等）/ RGB 设置（颜色、电源、亮度）
    REG_DEVICE_ADDR = const(0xFF) # 修改设备 I2C 地址
    REG_DEVICE_VERSION = const(0xFE) # 固件版本
    ALWAYS_OFF = const(0) # 常灭
    ALWAYS_ON = const(1) # 常亮
    AUTO_OFF = const(2) # 自动关闭
    def __init__(self, i2c: machine.I2C, addr: int | list | tuple = 0x48):
        self.i2c = i2c
        self.dev_addr = addr
        if self.dev_addr not in self.i2c.scan():
            raise OSError("Step16Unit not found on I2C bus")

    def get_encoder_value(self) -> int:
        """Get the current encoder value (0~15).

        :returns: Encoder value.
        :rtype: int

        UiFlow2 Code Block:

            |get_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                value = unit_step16_0.get_encoder_value()
        """
        return self.i2c.readfrom_mem(self.dev_addr, REG_ENCODER_VALUE, 1)[0]

    def set_encoder_cw_increase(self, enable: bool) -> None:
        """Configure whether clockwise rotation increases encoder value.

        :param enable:
            - True: Clockwise rotation increases the encoder value.
            - False: Clockwise rotation decreases the encoder value.
        :type enable: bool

        UiFlow2 Code Block:

            |set_encoder_cw_increase.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.set_encoder_cw_increase(True)
                unit_step16_0.set_encoder_cw_increase(False)
        """
        self.i2c.writeto_mem(
            self.dev_addr, REG_ENCODER_DIR_CFG, bytearray([1 if enable else 0])
        )

    def get_encoder_cw_increase(self) -> int:
        """Get current encoder direction mode.

        :returns: 1 for increasing clockwise, 0 for decreasing.
        :rtype: int

        UiFlow2 Code Block:

            |get_encoder_cw_increase.png|

        MicroPython Code Block:

            .. code-block:: python

                direction = unit_step16_0.get_encoder_cw_increase()
        """
        return self.i2c.readfrom_mem(self.dev_addr, REG_ENCODER_DIR_CFG, 1)[0]

    def set_led_mode(self, mode: int, seconds: int = 5) -> None:
        """Set LED display mode.

        :param mode: LED mode type.
            0 = always off,
            1 = always on,
            2 = auto-off mode with `seconds` as timeout.
        :type mode: int
        :param seconds: Timeout in seconds if `mode` is 2 (auto-off).
        :type seconds: int

        UiFlow2 Code Block:

            |set_led_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.set_led_mode(0)         # Always off
                unit_step16_0.set_led_mode(1)         # Always on
                unit_step16_0.set_led_mode(2, 10)     # Auto-off after 10 seconds
        """
        if mode == 0:
            value = 0
        elif mode == 1:
            value = 0xFE
        elif mode == 2:
            value = max(1, min(0xFD, seconds))  # Clamp to valid range
        else:
            raise ValueError("Invalid mode: must be 0 (on), 1 (off), or 2 (auto-off)")
        self.i2c.writeto_mem(self.dev_addr, REG_LED_WORK_MODE, bytearray([value]))

    def get_led_mode(self) -> int:
        """Get LED display mode.

        The LED mode values:

        - `0x00` : Always Off.
        - `0xFE` : Always On.
        - `0x00` ~ `0xFD` : Auto off times in seconds.

        :returns: LED display mode.
        :rtype: int

        UiFlow2 Code Block:

            |get_led_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.get_led_mode()
        """
        return self.i2c.readfrom_mem(self.dev_addr, REG_LED_WORK_MODE, 1)[0]

    def set_led_brightness(self, brightness: int) -> None:
        """Set LED brightness (0~100).

        :param brightness int: Brightness level.
        :type brightness: int

        UiFlow2 Code Block:

            |set_led_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.set_led_brightness(80)
        """
        brightness = max(0, min(100, brightness))
        self.i2c.writeto_mem(self.dev_addr, REG_LED_BRIGHTNESS, bytearray([brightness]))

    def get_led_brightness(self) -> int:
        """Get current LED brightness.

        :returns: Brightness level.
        :rtype: int

        UiFlow2 Code Block:

            |get_led_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                brightness = unit_step16_0.get_led_brightness()
                print("Brightness:", brightness)
        """
        return self.i2c.readfrom_mem(self.dev_addr, REG_LED_BRIGHTNESS, 1)[0]

    def set_rgb_power(self, enable: bool) -> None:
        """Turn the RGB light power ON or OFF.

        :param enable: True to turn on the RGB light, False to turn it off.
        :type enable: bool

        UiFlow2 Code Block:

            |set_rgb_power.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.set_rgb_power(True)   # Turn ON RGB light
                unit_step16_0.set_rgb_power(False)  # Turn OFF RGB light
        """
        val = 1 if enable else 0
        self.i2c.writeto_mem(self.dev_addr, REG_RGB_POWER, bytearray([val]))

    def get_rgb_power(self) -> bool:
        """Get the current power status of the RGB light.

        :returns: True if the RGB light is ON, False if OFF.
        :rtype: bool

        UiFlow2 Code Block:

            |get_rgb_power.png|

        MicroPython Code Block:

            .. code-block:: python

                power_on = unit_step16_0.get_rgb_power()
        """
        return self.i2c.readfrom_mem(self.dev_addr, REG_RGB_POWER, 1)[0] == 1

    def set_rgb_brightness(self, brightness) -> None:
        """Set the brightness of the RGB light (0~100%).

        :param brightness: Brightness percentage (0~100).
        :type brightness: int

        UiFlow2 Code Block:

            |set_rgb_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.set_rgb_brightness(80)  # Set RGB brightness to 80%
        """
        brightness = max(0, min(100, brightness))
        self.i2c.writeto_mem(self.dev_addr, REG_RGB_BRIGHTNESS, bytearray([brightness]))

    def get_rgb_brightness(self) -> int:
        """Get the current RGB brightness level (0~100%).

        :returns: Current RGB brightness percentage (0~100).
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                brightness = unit_step16_0.get_rgb_brightness()
                print("RGB Brightness:", brightness)
        """
        return self.i2c.readfrom_mem(self.dev_addr, REG_RGB_BRIGHTNESS, 1)[0]

    def set_rgb_value(self, color: int = 0) -> None:
        """Set RGB LED color using a 24-bit integer.

        :param color: A 24-bit integer representing the RGB color (e.g., 0xFF8040 for R=255, G=128, B=64).
                      Format is (R << 16) | (G << 8) | B.

        UiFlow2 Code Block:

            |set_rgb_value.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.set_rgb_value()
        """
        self.i2c.writeto_mem(self.dev_addr, REG_RGB_R, color.to_bytes(3, "big"))

    def get_rgb_value(self) -> tuple:
        """Get current RGB LED color.

        :returns: Tuple of (r, g, b)
        :rtype: tuple

        UiFlow2 Code Block:

            |get_rgb_value.png|

        MicroPython Code Block:

            .. code-block:: python

                r, g, b = unit_step16_0.get_rgb_value()
        """
        data = self.i2c.readfrom_mem(self.dev_addr, REG_RGB_R, 3)
        return tuple(data)

    def save_led_config(self) -> None:
        """Save current LED mode and brightness settings.

        UiFlow2 Code Block:

            |save_led_config.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.save_led_config()
        """
        self.i2c.writeto_mem(self.dev_addr, REG_SAVE_CFG, bytearray([1]))

    def save_rgb_config(self) -> None:
        """Save current RGB color settings.

        UiFlow2 Code Block:

            |save_rgb_config.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.save_rgb_config()
        """
        self.i2c.writeto_mem(self.dev_addr, REG_SAVE_CFG, bytearray([2]))

    def set_addr(self, new_addr: int) -> None:
        """Set the device's I2C address.

        :param new_addr: New I2C address (0x08~0x77).
        :type new_addr: int

        UiFlow2 Code Block:

            |set_addr.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_step16_0.set_addr(0x49)
        """
        new_addr = max(0x08, min(0x77, new_addr))
        self.i2c.writeto_mem(self.dev_addr, REG_DEVICE_ADDR, bytearray([new_addr]))
        self.dev_addr = new_addr
        time.sleep_ms(30)

    def get_addr(self) -> int:
        """Get the current I2C device address.

        :returns: I2C address.
        :rtype: int

        UiFlow2 Code Block:

            |get_addr.png|

        MicroPython Code Block:

            .. code-block:: python

                addr = unit_step16_0.get_addr()
        """
        return self.i2c.readfrom_mem(self.dev_addr, REG_DEVICE_ADDR, 1)[0]

    def get_firmware_version(self) -> int:
        """Get the firmware version.

        :returns:  firmware version.
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                addr = unit_step16_0.get_firmware_version()
        """
        return self.i2c.readfrom_mem(self.dev_addr, REG_DEVICE_VERSION, 1)[0]


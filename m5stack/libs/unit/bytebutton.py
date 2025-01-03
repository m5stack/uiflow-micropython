from machine import I2C


class ByteUnit:
    BYTESWITCH_I2C_ADDRESS = 0x46
    BYTEBUTTON_I2C_ADDRESS = 0x47

    # LED show modes
    BYTEBUTTON_LED_USER_MODE = 0
    BYTEBUTTON_LED_SYS_MODE = 1

    _BYTEUNIT_BYTE_BUTTON_STATUS_REG = 0x00
    _BYTEUNIT_BUTTON_STATUS_REG = 0x60
    _BYTEUNIT_LED_BRIGHTNESS_REG = 0x10
    _BYTEUNIT_LED_SHOW_MODE_REG = 0x19
    _BYTEUNIT_LED_USER_RGB888_REG = 0x20
    _BYTEUNIT_LED_USER_RGB232_REG = 0x50
    _BYTEUNIT_LED_SYS_RGB888_REG = 0x70
    _BYTEUNIT_LED_SYS_RGB888_UNPRESED_REG = 0x90
    _BYTEUNIT_IRQ_ENABLE_REG = 0xF1
    _BYTEUNIT_FLASH_WRITE_BACK_REG = 0xF0
    _BYTEUNIT_I2C_ADDRESS_REG = 0xFF
    _BYTEUNIT_FIRMWARE_VERSION_REG = 0xFE
    """
    note:
        en: Unit ByteButton is an 8-button touch switch input unit equipped with 8 button inputs and 9 WS2812C RGB LEDs. It uses the STM32 microcontroller and supports I2C communication. The board includes two Port A interfaces and supports cascading multiple Unit ByteButton modules, making it suitable for complex systems. It can achieve button input detection and dynamic lighting feedback, ideal for smart home control, gaming devices, educational platforms, industrial status displays, and interactive exhibitions.

    details:
        link: https://docs.m5stack.com/en/unit/Unit%20ByteButton
        image: https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/Unit%20ByteButton/4.webp
        category: Unit

    example:
        - ../../../examples/unit/bytebutton_cores3_example.py

    m5f2:
        - unit/bytebutton/bytebutton_cores3_example.m5f2
    """

    def __init__(self, i2c: I2C, address: int = BYTEBUTTON_I2C_ADDRESS):
        """
        note:
            en: Initialize the ByteButtonUnit with a specified I2C address.

        params:
            i2c:
                note: The I2C interface instance for communication.
            address:
                note: The I2C address of the ByteButtonUnit, default is 0x47.
        """
        self.i2c = i2c
        self.address = address
        self.set_led_show_mode(self.BYTEBUTTON_LED_SYS_MODE)

    def get_byte_button_status(self) -> int:
        """
        note:
            en: Get the status of all buttons as an integer, where each bit represents the state of each button.

        params:
            note:
        """
        return self.i2c.readfrom_mem(self.address, self._BYTEUNIT_BYTE_BUTTON_STATUS_REG, 1)[0]

    def get_button_state(self, num: int) -> bool:
        """
        note:
            en: Get the statue of a specific button.

        params:
            num:
                note: The index of the button (0-7).
        """
        return (
            self.i2c.readfrom_mem(self.address, self._BYTEUNIT_BUTTON_STATUS_REG + num, 1)[0] == 0
        )

    def get_led_show_mode(self) -> int:
        """
        note:
            en: Get the current LED show mode.

        params:
            note:
        """
        return self.i2c.readfrom_mem(self.address, self._BYTEUNIT_LED_SHOW_MODE_REG, 1)[0]

    def set_led_show_mode(self, mode: int) -> None:
        """
        note:
            en: Set the LED show mode.

        params:
            mode:
                note: The LED show mode to set. (BYTEBUTTON_LED_USER_MODE or _BYTEUNIT_LED_SYS_MODE)
        """
        self.i2c.writeto_mem(self.address, self._BYTEUNIT_LED_SHOW_MODE_REG, bytes([mode]))

    def set_led_brightness(self, num: int, brightness: int) -> None:
        """
        note:
            en: Set the brightness of a specific LED.

        params:
            num:
                note: The index of the LED (0-7).
            brightness:
                note: The brightness level (0-255).
        """
        self.i2c.writeto_mem(
            self.address, self._BYTEUNIT_LED_BRIGHTNESS_REG + num, bytes([brightness])
        )

    def get_led_brightness(self, num: int) -> int:
        """
        note:
            en: Get the brightness of a specific LED.

        params:
            num:
                note: The index of the LED (0-7).
        """
        return self.i2c.readfrom_mem(self.address, self._BYTEUNIT_LED_BRIGHTNESS_REG + num, 1)[0]

    def set_led_color(
        self,
        num: int,
        color: int,
        led_show_mode: int = BYTEBUTTON_LED_SYS_MODE,
        btn_is_pressed: bool = True,
    ):
        """
        note:
            en: Set the color of a specific LED.

        params:
            num:
                note: The index of the LED (0-7).
            color:
                note: The RGB888 color value to set.
            led_show_mode:
                note: The LED show mode, default is BYTEBUTTON_LED_SYS_MODE.
            btn_is_pressed:
                note: Whether the button is pressed (affects color in SYS mode).
        """
        color_bytes = color.to_bytes(3, "little")
        if led_show_mode == self.BYTEBUTTON_LED_USER_MODE:
            reg_addr = self._BYTEUNIT_LED_USER_RGB888_REG
        else:
            reg_addr = (
                self._BYTEUNIT_LED_SYS_RGB888_REG
                if btn_is_pressed
                else self._BYTEUNIT_LED_SYS_RGB888_UNPRESED_REG
            )

        self.i2c.writeto_mem(
            self.address, reg_addr + ((num // 4) * 0x10 + (num % 4) * 4), color_bytes
        )

    def get_led_color(
        self, num: int, led_show_mode: int = BYTEBUTTON_LED_SYS_MODE, btn_is_pressed: bool = True
    ):
        """
        note:
            en: Get the color of a specific LED.

        params:
            num:
                note: The index of the LED (0-7).
            led_show_mode:
                note: The LED show mode, default is BYTEBUTTON_LED_SYS_MODE.
            btn_is_pressed:
                note: Whether the button is pressed (affects color in SYS mode).
        """
        if led_show_mode == self.BYTEBUTTON_LED_USER_MODE:
            reg_addr = self._BYTEUNIT_LED_USER_RGB888_REG
        else:
            reg_addr = (
                self._BYTEUNIT_LED_SYS_RGB888_REG
                if btn_is_pressed
                else self._BYTEUNIT_LED_SYS_RGB888_UNPRESED_REG
            )
        color_bytes = self.i2c.readfrom_mem(
            self.address, reg_addr + ((num // 4) * 0x10 + (num % 4) * 4), 3
        )
        return int.from_bytes(color_bytes, "little")

    def set_indicator_brightness(self, brightness: int):
        """
        note:
            en: Set the brightness of the indicator LED.

        params:
            brightness:
                note: The brightness level (0-255).
        """
        self.set_led_brightness(8, brightness)

    def get_indicator_brightness(self):
        """
        note:
            en: Get the brightness of the indicator LED.

        params:
            note:
        """
        return self.get_led_brightness(8)

    def set_indicator_color(self, color: int):
        """
        note:
            en: Set the color of the indicator LED in RGB888 format.

        params:
            color:
                note: The RGB888 color value to set.
        """
        self.set_led_color(8, color, self.BYTEBUTTON_LED_USER_MODE)

    def get_indicator_color(self):
        """
        note:
            en: Get the color of the indicator LED in RGB888 format.

        params:
            note:
        """
        return self.get_led_color(8, self.BYTEBUTTON_LED_USER_MODE)

    def rgb888_to_rgb233(self, color: int):
        """
        note:
            en: Convert an RGB888 color value to RGB233 format.

        params:
            color:
                note: The RGB888 color value as a 32-bit integer.
        """
        r = (color >> 16) & 0xFF
        g = (color >> 8) & 0xFF
        b = color & 0xFF
        return (r & 0xC0) | ((g & 0xE0) >> 2) | ((b & 0xE0) >> 5)

    def set_rgb233(self, num: int, color: int):
        """
        note:
            en: Set the color of a specific LED in RGB233 format.

        params:
            num:
                note: The index of the LED (0-7).
            color:
                note: The RGB233 color value to set.
        """
        color_bytes = bytes([self.rgb888_to_rgb233(color)])
        self.i2c.writeto_mem(self.address, self._BYTEUNIT_LED_USER_RGB232_REG + num, color_bytes)

    def get_rgb233(self, num: int):
        """
        note:
            en: Get the color of a specific LED in RGB233 format.

        params:
            num:
                note: The index of the LED (0-7).
        """
        return self.i2c.readfrom_mem(self.address, self._BYTEUNIT_LED_USER_RGB232_REG + num, 1)[0]

    def set_irq_enable(self, enable: bool):
        """
        note:
            en: Enable or disable IRQ functionality.

        params:
            enable:
                note: Whether to enable (True) or disable (False) IRQ.
        """
        self.i2c.writeto_mem(
            self.address, self._BYTEUNIT_IRQ_ENABLE_REG, bytes([1 if enable else 0])
        )

    def get_irq_enable(self):
        """
        note:
            en: Get the current IRQ enable status.

        params:
            note:
        """
        return self.i2c.readfrom_mem(self.address, self._BYTEUNIT_IRQ_ENABLE_REG, 1)[0]

    def save_to_flash(self):
        """
        note:
            en: Save the current user settings to flash.

        params:
            note:
        """
        self.i2c.writeto_mem(self.address, self._BYTEUNIT_FLASH_WRITE_BACK_REG, bytes([0x01]))

    def get_firmware_version(self):
        """
        note:
            en: Get the firmware version of the ByteButtonUnit.

        params:
            note:
        """
        return self.i2c.readfrom_mem(self.address, self._BYTEUNIT_FIRMWARE_VERSION_REG, 1)[0]

    def set_i2c_address(self, new_addr: int):
        """
        note:
            en: Set a new I2C address for the ByteButtonUnit.

        params:
            new_addr:
                note: The new I2C address to set. Must be in the range 0x08 to 0x78.
        """
        if new_addr >= 0x08 and new_addr <= 0x78:
            if new_addr != self.address:
                self.i2c.writeto_mem(
                    self.address, self._BYTEUNIT_I2C_ADDRESS_REG, bytearray([new_addr])
                )
                self.address = new_addr
        else:
            raise ValueError("I2C address error, range:0x08~0x78")

    def get_i2c_address(self):
        """
        note:
            en: Get the current I2C address of the ByteButtonUnit.

        params:
            note:
        """
        return self.i2c.readfrom_mem(self.address, self._BYTEUNIT_I2C_ADDRESS_REG, 1)[0]


class ByteButtonUnit(ByteUnit):
    def __init__(self, i2c: I2C, address: int = ByteUnit.BYTEBUTTON_I2C_ADDRESS):
        super().__init__(i2c, address)
        if self.address not in self.i2c.scan():
            raise ValueError("UnitByteButton not found in I2C bus.")


class ByteSwitchUnit(ByteUnit):
    BYTESWITCH_LED_USER_MODE = 0
    BYTESWITCH_LED_SYS_MODE = 1

    def __init__(self, i2c: I2C, address: int = ByteUnit.BYTESWITCH_I2C_ADDRESS):
        super().__init__(i2c, address)
        if self.address not in self.i2c.scan():
            raise ValueError("UnitByteSwitch not found in I2C bus.")

    def get_byte_switch_status(self) -> int:
        return super().get_byte_button_status()

    def get_switch_state(self, num: int) -> bool:
        return super().get_button_state(num)

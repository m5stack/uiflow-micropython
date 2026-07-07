# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
from micropython import schedule


class Keyboard:
    """Create a Tab5 keyboard controller object.

    :param I2C i2c: The I2C bus the Tab5 keyboard is connected to.
    :param int address: The I2C address of the keyboard controller. Default is ``0x6D``.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from tab5 import Keyboard
            from hardware import Pin, SoftI2C

            softi2c_0 = SoftI2C(scl=Pin(1), sda=Pin(0), freq=100000)
            keyboard = Keyboard(softi2c_0, 0x6D)
    """

    KEYBOARD_ADDR = 0x6D
    KEYBOARD_I2C_FREQ = 100000

    INT_NORMAL = 1 << 0
    INT_CHAR = 1 << 2
    INT_ALL = INT_NORMAL | INT_CHAR

    MODE_NORMAL = 0
    MODE_CHAR = 2

    RGB_MODE_BOUND = 0
    RGB_MODE_CUSTOM = 1

    EVENT_TYPE_KEY = "key"
    EVENT_TYPE_CHAR = "char"

    INT_CFG_REG = 0x00
    INT_STAT_REG = 0x01
    EVENT_NUM_REG = 0x02
    BRIGHTNESS_REG = 0x03
    KEYBOARD_MODE_REG = 0x10
    RGB_MODE_REG = 0x11
    KEY_EVENT_REG = 0x20
    CHAR_EVENT_LENGTH_REG = 0x40
    CHAR_EVENT_REG = 0x50
    RGB_COLOR_REG = 0x60
    FW_VERSION_REG = 0xFE
    I2C_ADDR_REG = 0xFF

    def __init__(self, i2c, address: int = KEYBOARD_ADDR):
        self._i2c = i2c
        self._i2c_addr = address
        self._handler = None
        self._callback_scheduled = False
        self._available()

    def _available(self):
        # Probe the configured I2C address once at init time so later reads fail fast.
        if self._i2c_addr not in self._i2c.scan():
            raise Exception("Tab5 keyboard maybe not connect")

    def available(self) -> bool:
        """Check whether unread keyboard events are queued.

        :returns: ``True`` if the controller has pending events.
        :rtype: bool
        """
        return self.get_event_count() > 0

    def set_int_enable(self, mask: int) -> None:
        """Enable keyboard interrupt sources.

        :param int mask: Interrupt mask composed from ``INT_NORMAL`` and ``INT_CHAR``.
        """
        self._i2c.writeto_mem(self._i2c_addr, self.INT_CFG_REG, bytes([mask & self.INT_ALL]))

    def get_int_status(self) -> int:
        """Get the current keyboard interrupt status.

        :returns: The latched interrupt status bits.
        :rtype: int
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.INT_STAT_REG, 1)[0] & self.INT_ALL

    def clear_int(self) -> None:
        """Clear the current keyboard interrupt status."""
        self._i2c.writeto_mem(self._i2c_addr, self.INT_STAT_REG, b"\x00")

    def get_event_count(self) -> int:
        """Get the number of unread keyboard events.

        :returns: The number of queued events.
        :rtype: int
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.EVENT_NUM_REG, 1)[0]

    def set_brightness(self, brightness: int) -> None:
        """Set the keyboard backlight brightness.

        :param int brightness: Brightness value in the range ``0`` to ``255``.

        UiFlow2 Code Block:

            |set_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.set_brightness(20)
        """
        self._i2c.writeto_mem(self._i2c_addr, self.BRIGHTNESS_REG, bytes([brightness & 0xFF]))

    def get_brightness(self) -> int:
        """Get the keyboard backlight brightness.

        :returns: The current brightness value.
        :rtype: int

        UiFlow2 Code Block:

            |get_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.get_brightness()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.BRIGHTNESS_REG, 1)[0]

    def set_keyboard_mode(self, mode: int) -> None:
        """Set the keyboard event mode.

        :param int mode: Event mode such as ``MODE_NORMAL`` or ``MODE_CHAR``.

        UiFlow2 Code Block:

            |set_keyboard_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.set_keyboard_mode(keyboard.MODE_CHAR)
        """
        self._i2c.writeto_mem(self._i2c_addr, self.KEYBOARD_MODE_REG, bytes([mode & 0xFF]))

    def get_keyboard_mode(self) -> int:
        """Get the current keyboard event mode.

        :returns: The current keyboard mode.
        :rtype: int
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.KEYBOARD_MODE_REG, 1)[0]

    def set_rgb_mode(self, mode: int) -> None:
        """Set the RGB LED control mode.

        :param int mode: RGB mode such as ``RGB_MODE_BOUND`` or ``RGB_MODE_CUSTOM``.

        UiFlow2 Code Block:

            |set_rgb_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.set_rgb_mode(keyboard.RGB_MODE_BOUND)
        """
        self._i2c.writeto_mem(self._i2c_addr, self.RGB_MODE_REG, bytes([mode & 0xFF]))

    def get_rgb_mode(self) -> int:
        """Get the RGB LED control mode.

        :returns: The current RGB mode.
        :rtype: int
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.RGB_MODE_REG, 1)[0]

    def _read_key_event_internal(self):
        value = self._i2c.readfrom_mem(self._i2c_addr, self.KEY_EVENT_REG, 1)[0]
        if value == 0xFF:
            return None
        pressed = bool((value >> 7) & 0x01)
        row = (value >> 4) & 0x07
        col = value & 0x0F
        return (self.EVENT_TYPE_KEY, row, col, pressed)

    def read_key_event(self):
        """Read one key matrix event.

        :returns: A tuple of ``(row, col, pressed)`` or ``None`` when no event is available.
        :rtype: tuple | None
        """
        event = self._read_key_event_internal()
        if event is None:
            return None
        return event[1], event[2], event[3]

    def get_char_event_length(self) -> int:
        """Get the byte length of the queued character event.

        :returns: The length of the character payload.
        :rtype: int
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.CHAR_EVENT_LENGTH_REG, 1)[0]

    def _read_char_event_internal(self):
        char_len = self.get_char_event_length()
        if char_len == 0:
            return None
        raw = self._i2c.readfrom_mem(self._i2c_addr, self.CHAR_EVENT_REG, min(char_len + 1, 10))
        modifier = raw[0]
        text = bytes(raw[1:]).decode("utf-8", "ignore")
        return (self.EVENT_TYPE_CHAR, modifier, text)

    def read_char_event(self):
        """Read one decoded character event.

        :returns: A tuple of ``(modifier, text)`` or ``None`` when no event is available.
        :rtype: tuple | None
        """
        event = self._read_char_event_internal()
        if event is None:
            return None
        return event[1], event[2]

    def is_pressed(self) -> bool:
        """Check whether the keyboard has pending input.

        :returns: ``True`` if unread input is available.
        :rtype: bool
        """
        return self.available()

    def _get_callback_data(self):
        if self.get_keyboard_mode() == self.MODE_CHAR:
            event = self.read_char_event()
            if event is None:
                return None
            return event[1]
        return self.read_key_event()

    def set_callback(self, handler):
        """Register the callback used by :meth:`tick`.

        :param callable handler: Callback that receives the keyboard event payload.

        MicroPython Code Block:

            .. code-block:: python

                def on_keyboard(data):
                    print(data)

                keyboard.set_callback(on_keyboard)
        """
        self._handler = handler
        self._callback_scheduled = False

    def _run_callback(self, arg) -> None:
        self._callback_scheduled = False
        if self._handler is not None:
            self._handler(arg)

    def tick(self):
        """Dispatch one pending keyboard event to the registered callback."""
        if self._handler is None or self._callback_scheduled:
            return

        data = self._get_callback_data()
        if data is None:
            return

        if schedule is None:
            self._run_callback(data)
            return

        self._callback_scheduled = True
        try:
            schedule(self._run_callback, data)
        except RuntimeError:
            self._callback_scheduled = False

    def set_rgb_color(self, led_num: int, color: int) -> None:
        """Set the color of a keyboard RGB LED.

        :param int led_num: The LED index to update.
        :param int color: The 24-bit RGB color value.

        UiFlow2 Code Block:

            |set_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.set_rgb_color(0, 0x6600CC)
        """
        reg = self.RGB_COLOR_REG + (4 if led_num else 0)
        data = bytes((color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF))
        self._i2c.writeto_mem(self._i2c_addr, reg, data)

    def get_rgb_color(self, led_num: int) -> int:
        """Get the color of a keyboard RGB LED.

        :param int led_num: The LED index to read.
        :returns: The 24-bit RGB color value.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_color.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.get_rgb_color(0)
        """
        reg = self.RGB_COLOR_REG + (4 if led_num else 0)
        data = self._i2c.readfrom_mem(self._i2c_addr, reg, 3)
        return (data[2] << 16) | (data[1] << 8) | data[0]

    def get_firmware_version(self) -> int:
        """Get the firmware version of the keyboard controller.

        :returns: The firmware version byte.
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.get_firmware_version()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.FW_VERSION_REG, 1)[0]

    def set_i2c_address(self, addr: int) -> int:
        """Set a new I2C address for the keyboard controller.

        :param int addr: The new I2C address. Valid range is ``0x08`` to ``0x77``.
        :returns: The active I2C address after the update.
        :rtype: int

        UiFlow2 Code Block:

            |set_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.set_i2c_address(0x6D)
        """
        if 0x08 <= addr <= 0x77:
            if addr != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, self.I2C_ADDR_REG, bytearray([addr]))
                self._i2c_addr = addr
                time.sleep_ms(200)
            return self._i2c_addr
        raise ValueError("I2C address error, range:0x08~0x77")

    def get_i2c_address(self) -> int:
        """Get the current I2C address of the keyboard controller.

        :returns: The current I2C address.
        :rtype: int

        UiFlow2 Code Block:

            |get_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                keyboard.get_i2c_address()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.I2C_ADDR_REG, 1)[0]

# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time

import M5
from machine import Pin
from micropython import schedule
from module.mbus import i2c1


class _FacesModule:
    _DEFAULT_ADDRESS = 0x08
    _DEVICE_ID_REG = 0xD0
    _UID_REG = 0xE0
    _FIRMWARE_VERSION_REG = 0xFE
    _I2C_ADDRESS_REG = 0xFF
    _IRQ_PIN = {
        M5.BOARD.M5Stack: 35,
        M5.BOARD.M5StackCore2: 35,
        M5.BOARD.M5StackCoreS3: 10,
        M5.BOARD.M5Tough: 35,
        M5.BOARD.M5Tab5: 16,
    }.get(M5.getBoard())

    _DEVICE_ID = None
    _PRODUCT_NAME = "Faces"

    def __init__(self, address: int = _DEFAULT_ADDRESS) -> None:
        self._i2c = i2c1
        self._i2c_addr = address
        if self._IRQ_PIN is None:
            raise RuntimeError("Faces Module IRQ pin is not defined for this board")
        self._irq = Pin(self._IRQ_PIN, Pin.IN)
        if address not in self._i2c.scan():
            raise RuntimeError("%s Module not found" % self._PRODUCT_NAME)

        device_id = self.get_device_id()
        if device_id != self._DEVICE_ID:
            raise RuntimeError(
                "%s Module device ID mismatch: expected 0x%02X, got 0x%02X"
                % (self._PRODUCT_NAME, self._DEVICE_ID, device_id)
            )

    def get_device_id(self) -> int:
        """Get the Faces module device type ID.

        :returns: The device type ID.
        :rtype: int

        UiFlow2 Code Block:

            |get_device_id.png|

        MicroPython Code Block:

            .. code-block:: python

                device.get_device_id()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._DEVICE_ID_REG, 1)[0]

    def get_uid(self) -> bytes:
        """Get the 96-bit MCU unique identifier.

        :returns: The 12-byte unique identifier.
        :rtype: bytes

        UiFlow2 Code Block:

            |get_uid.png|

        MicroPython Code Block:

            .. code-block:: python

                device.get_uid()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._UID_REG, 12)

    def get_firmware_version(self) -> int:
        """Get the firmware version.

        :returns: The firmware version.
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                device.get_firmware_version()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._FIRMWARE_VERSION_REG, 1)[0]

    def get_i2c_address(self) -> int:
        """Get the current 7-bit I2C address.

        :returns: The current I2C address.
        :rtype: int

        UiFlow2 Code Block:

            |get_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                device.get_i2c_address()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._I2C_ADDRESS_REG, 1)[0]

    def set_i2c_address(self, address: int) -> None:
        """Set and persist a new 7-bit I2C address.

        :param int address: New address in the range ``0x08`` to ``0x77``.

        UiFlow2 Code Block:

            |set_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_i2c_address(0x08)
        """
        if not 0x08 <= address <= 0x77:
            raise ValueError("I2C address must be in range 0x08~0x77")
        if address == self._i2c_addr:
            return
        self._i2c.writeto_mem(self._i2c_addr, self._I2C_ADDRESS_REG, bytes([address]))
        self._i2c_addr = address
        time.sleep_ms(20)


class FacesCalculator3Module(_FacesModule):
    """Create a Faces Calculator3 Module object.

    :param int address: I2C address. Default is ``0x08``.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import FacesCalculator3Module

            faces_calculator3 = FacesCalculator3Module()
    """

    DEVICE_ID = 0x01

    KEY_BACKSPACE = 0x08
    KEY_ENTER = 0x0D
    KEY_AC = 0x41
    KEY_MEMORY = 0x4D
    KEY_PERCENT = 0x25
    KEY_DIVIDE = 0x2F
    KEY_MULTIPLY = 0x2A
    KEY_MINUS = 0x2D
    KEY_PLUS = 0x2B
    KEY_SIGN = 0x60
    KEY_EQUAL = 0x3D

    _DEVICE_ID = DEVICE_ID
    _PRODUCT_NAME = "Faces Calculator3"

    def __init__(self, address: int = _FacesModule._DEFAULT_ADDRESS) -> None:
        super().__init__(address)
        self._handler = None

    def _read_key(self):
        key = self._i2c.readfrom(self._i2c_addr, 1)[0]
        return None if key == 0 else key

    def set_callback(self, handler) -> None:
        """Set the callback for key events.

        The callback receives the released key code. Pass ``None`` to disable it.

        :param handler: Callable accepting one key code, or ``None``.
        """
        if handler is not None and not callable(handler):
            raise TypeError("handler must be callable or None")
        self._handler = handler

    def tick(self) -> None:
        """Poll once and invoke the callback when a key event is available.

        UiFlow2 Code Block:

            |tick.png|

        MicroPython Code Block:

            .. code-block:: python

                faces_calculator3.tick()
        """
        if self._handler is None:
            return
        key = self._read_key()
        if key is not None:
            self._handler(key)


class FacesGamepad3Module(_FacesModule):
    """Create a Faces Gamepad3 Module object.

    :param int address: I2C address. Default is ``0x08``.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import FacesGamepad3Module

            faces_gamepad3 = FacesGamepad3Module()
    """

    DEVICE_ID = 0x03

    BUTTON_UP = 0x01
    BUTTON_DOWN = 0x02
    BUTTON_LEFT = 0x04
    BUTTON_RIGHT = 0x08
    BUTTON_A = 0x10
    BUTTON_B = 0x20
    BUTTON_SELECT = 0x40
    BUTTON_START = 0x80

    _DEVICE_ID = DEVICE_ID
    _PRODUCT_NAME = "Faces Gamepad3"
    _BUTTON_MASKS = (
        BUTTON_UP,
        BUTTON_DOWN,
        BUTTON_LEFT,
        BUTTON_RIGHT,
        BUTTON_A,
        BUTTON_B,
        BUTTON_SELECT,
        BUTTON_START,
    )

    def __init__(self, address: int = _FacesModule._DEFAULT_ADDRESS) -> None:
        super().__init__(address)
        self._key_state = 0xFF
        self._callback_state = 0xFF
        self._handlers = {}

    def get_key_state(self) -> int:
        """Read the active-low state of all eight buttons.

        :returns: Button state bitmask. A cleared bit means that button is pressed.
        :rtype: int

        UiFlow2 Code Block:

            |get_key_state.png|

        MicroPython Code Block:

            .. code-block:: python

                faces_gamepad3.get_key_state()
        """
        if self._irq.value() == 0:
            self._key_state = self._i2c.readfrom(self._i2c_addr, 1)[0]
        return self._key_state

    def is_pressed(self, button: int, state=None) -> bool:
        """Check whether a button or button combination is pressed.

        :param int button: One or more ``BUTTON_*`` masks.
        :param int state: Optional state previously returned by :meth:`get_key_state`.
        :returns: ``True`` when every selected button is pressed.
        :rtype: bool
        """
        if not 0 < button <= 0xFF:
            raise ValueError("button mask must be in range 0x01~0xFF")
        if state is None:
            state = self.get_key_state()
        return state & button == 0

    def set_callback(self, button: int, handler) -> None:
        """Set the callback for one button's state changes.

        The callback receives ``pressed``. Pass ``None`` to remove the callback.

        :param int button: One ``BUTTON_*`` constant.
        :param handler: Callable accepting the pressed state, or ``None``.
        """
        if button not in self._BUTTON_MASKS:
            raise ValueError("button must be a single BUTTON_* constant")
        if handler is not None and not callable(handler):
            raise TypeError("handler must be callable or None")
        if handler is None:
            self._handlers.pop(button, None)
            return
        if not self._handlers:
            self._callback_state = self._key_state
        self._handlers[button] = handler

    def tick(self) -> None:
        """Poll once and invoke the callback for each changed button.

        UiFlow2 Code Block:

            |tick.png|

        MicroPython Code Block:

            .. code-block:: python

                faces_gamepad3.tick()
        """
        if not self._handlers:
            return
        state = self.get_key_state()
        changed = self._callback_state ^ state
        self._callback_state = state
        for button in self._BUTTON_MASKS:
            handler = self._handlers.get(button)
            if changed & button and handler is not None:
                handler(state & button == 0)


class FacesKeyboard3Module(_FacesModule):
    """Create a Faces Keyboard3 Module object.

    :param int address: I2C address. Default is ``0x08``.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import FacesKeyboard3Module

            faces_keyboard3 = FacesKeyboard3Module()
    """

    DEVICE_ID = 0x02

    NORMAL = 0x00
    DIRECT = 0x01

    LED_EFFECT_OFF = 0x00
    LED_EFFECT_1 = 0x01
    LED_EFFECT_2 = 0x02
    LED_EFFECT_3 = 0x03
    LED_EFFECT_4 = 0x04
    LED_EFFECT_5 = 0x05
    LED_EFFECT_6 = 0x06
    LED_EFFECT_7 = 0x07
    LED_EFFECT_8 = 0x08

    KEY_BACKSPACE = 0x08
    KEY_ENTER = 0x0D
    KEY_DELETE = 0x7F

    _MODE_REG = 0xF0
    _LED_REG = 0xF1
    _LED_MANUAL = 0x80
    _DIRECT_PACKET_LENGTH = 10

    _DEVICE_ID = DEVICE_ID
    _PRODUCT_NAME = "Faces Keyboard3"

    _DIRECT_KEY_NAMES = (
        ("P", "O", "I", "U", "Y", "T", "R", "E", "W", "Q"),
        ("DEL", "L", "K", "J", "H", "G", "F", "D", "S", "A"),
        ("SPACE", "$", "M", "N", "B", "V", "C", "X", "Z", "0"),
    )
    _DIRECT_MODIFIER_NAMES = ("aA", "ALT", "ENTER", "SYM", "FN")

    def __init__(self, address: int = _FacesModule._DEFAULT_ADDRESS) -> None:
        super().__init__(address)
        self._mode = self.get_mode()
        self._handler = None

    def get_mode(self) -> int:
        """Get the current keyboard operating mode.

        ``NORMAL`` (``0x00``) maps key presses to characters; ``DIRECT``
        (``0x01``) reports matrix key names.

        UiFlow2 Code Block:

            |get_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                faces_keyboard3.get_mode()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._MODE_REG, 1)[0]

    def set_mode(self, mode: int) -> None:
        """Set mapped-character or raw-matrix operating mode.

        :param int mode: ``NORMAL`` or ``DIRECT``.

        UiFlow2 Code Block:

            |set_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                faces_keyboard3.set_mode(faces_keyboard3.DIRECT)
        """
        if mode not in (self.NORMAL, self.DIRECT):
            raise ValueError("mode must be NORMAL or DIRECT")
        current_mode = self.get_mode()
        if current_mode == mode:
            self._mode = mode
            return
        if current_mode == self.NORMAL:
            self._read_key()
        elif current_mode == self.DIRECT:
            self._read_direct()
        else:
            raise RuntimeError("invalid Faces Keyboard3 operating mode")
        self._i2c.writeto_mem(self._i2c_addr, self._MODE_REG, bytes([mode]))
        self._mode = mode

    def set_led_effect(self, effect: int) -> None:
        """Set a keyboard LED effect in Direct mode.

        Effects correspond to the keyboard firmware states and LED patterns:

        - ``LED_EFFECT_1``: ``aA`` single press; left LED stays on.
        - ``LED_EFFECT_2``: ``aA`` double-press lock; left LED blinks every 500 ms.
        - ``LED_EFFECT_3``: ``ALT`` active; left LED blinks every 150 ms.
        - ``LED_EFFECT_4``: ``FN`` single press; right LED stays on.
        - ``LED_EFFECT_5``: ``FN`` double-press lock; right LED blinks every 500 ms.
        - ``LED_EFFECT_6``: ``SYM`` double-press lock; right LED blinks every 150 ms.
        - ``LED_EFFECT_7``: ``SYM`` single press; LEDs alternate every 500 ms.
        - ``LED_EFFECT_8``: External effect; LEDs alternate every 200 ms.

        :param int effect: One of the ``LED_EFFECT_*`` constants.

        UiFlow2 Code Block:

            |set_led_effect.png|

        MicroPython Code Block:

            .. code-block:: python

                faces_keyboard3.set_led_effect(faces_keyboard3.LED_EFFECT_1)
        """
        if not self.LED_EFFECT_OFF <= effect <= self.LED_EFFECT_8:
            raise ValueError("effect must be an LED_EFFECT_* constant")
        if self.get_mode() != self.DIRECT:
            print("LED effects can only be controlled in Direct mode")
            return
        self._i2c.writeto_mem(self._i2c_addr, self._LED_REG, bytes([effect]))

    def set_led(self, left: bool, right: bool) -> None:
        """Set the left and right LEDs directly in Direct mode.

        UiFlow2 Code Block:

            |set_led.png|

        MicroPython Code Block:

            .. code-block:: python

                faces_keyboard3.set_led(True, False)
        """
        if self.get_mode() != self.DIRECT:
            print("LEDs can only be controlled in Direct mode")
            return
        mode = self._LED_MANUAL
        if left:
            mode |= 0x10
        if right:
            mode |= 0x20
        self._i2c.writeto_mem(self._i2c_addr, self._LED_REG, bytes([mode]))

    def _read_key(self):
        if self._irq.value() != 0:
            return None
        key = self._i2c.readfrom(self._i2c_addr, 1)[0]
        if key in (0x00, 0xFF):
            return None
        if key == self.KEY_ENTER:
            line_feed = self._i2c.readfrom(self._i2c_addr, 1)[0]
            if line_feed != 0x0A:
                raise RuntimeError("invalid Faces Keyboard3 Enter sequence")
            return b"\r\n"
        return bytes([key])

    def set_callback(self, handler) -> None:
        """Set the key callback.

        In Normal mode, the callback receives an integer key code. In Direct
        mode, it receives a tuple containing the currently pressed key names.
        Pass ``None`` to disable the callback.

        :param handler: Callable accepting the key event value, or ``None``.
        """
        if handler is not None and not callable(handler):
            raise TypeError("handler must be callable or None")
        self._handler = handler

    def tick(self) -> None:
        """Poll once and schedule the callback for a new key event.

        UiFlow2 Code Block:

            |tick.png|

        MicroPython Code Block:

            .. code-block:: python

                faces_keyboard3.tick()
        """
        if self._handler is None:
            return
        if self._mode == self.NORMAL:
            data = self._read_key()
            if data is None:
                return
            event = data[0]
        else:
            packet = self._read_direct()
            if packet is None:
                return
            event = self._decode_direct(packet)
        schedule(self._handler, event)

    @classmethod
    def _validate_direct_packet(cls, packet: bytes) -> None:
        if len(packet) != cls._DIRECT_PACKET_LENGTH or packet[0] != cls._DIRECT_PACKET_LENGTH:
            raise ValueError("invalid Faces Keyboard3 Direct packet length")
        if sum(packet) & 0xFF:
            raise ValueError("invalid Faces Keyboard3 Direct packet checksum")
        for row, offset in enumerate((1, 3, 5, 7)):
            if packet[offset] >> 4 & 0x07 != row:
                raise ValueError("invalid Faces Keyboard3 Direct packet row")

    def _read_direct(self):
        if self._irq.value() != 0:
            return None
        packet = self._i2c.readfrom(self._i2c_addr, self._DIRECT_PACKET_LENGTH)
        if not any(packet):
            return None
        self._validate_direct_packet(packet)
        return packet

    @classmethod
    def _decode_direct(cls, packet: bytes) -> tuple:
        cls._validate_direct_packet(packet)
        pressed = []
        for row, names in enumerate(cls._DIRECT_KEY_NAMES):
            offset = 1 + row * 2
            state = (packet[offset] & 0x03) << 8 | packet[offset + 1]
            for bit, name in enumerate(names):
                if state & (1 << bit) == 0:
                    pressed.append(name)

        modifier_state = (packet[7] & 0x03) << 8 | packet[8]
        for bit, name in enumerate(cls._DIRECT_MODIFIER_NAMES):
            if modifier_state & (1 << bit) == 0:
                pressed.append(name)
        return tuple(pressed)


# def _print_faces_info(device) -> None:
#     print("Device ID: 0x%02X" % device.get_device_id())
#     print("Firmware: 0x%02X" % device.get_firmware_version())
#     print("I2C address: 0x%02X" % device.get_i2c_address())
#     print("UID:", device.get_uid().hex())


# def test_faces_calculator3(address: int = _FacesModule._DEFAULT_ADDRESS, interval_ms: int = 20):
#     """Run the Faces Calculator3 key test from the REPL.

#     Press ``Ctrl-C`` to stop. The initialized module object is returned after the test.
#     """
#     device = FacesCalculator3Module(address)
#     _print_faces_info(device)

#     def calculator_event(args, get_char=False):
#         if get_char:
#             print("Pressed char:", chr(args))
#         else:
#             print("Pressed key:", args)

#     device.set_callback(calculator_event)
#     print("Calculator3 key test started. Press Ctrl-C to stop.")
#     try:
#         while True:
#             device.tick()
#             time.sleep_ms(interval_ms)
#     except KeyboardInterrupt:
#         print("Calculator3 key test stopped.")
#     finally:
#         device.set_callback(None)
#     return device


# def test_faces_gamepad3(address: int = _FacesModule._DEFAULT_ADDRESS, interval_ms: int = 20):
#     """Run the Faces Gamepad3 callback test from the REPL.

#     Press and release the A button. Press ``Ctrl-C`` to stop.
#     """
#     device = FacesGamepad3Module(address)
#     _print_faces_info(device)

#     def gamepad_key_a_event(key_state):
#         if key_state:
#             print("Gamepad3 A button pressed.")
#         else:
#             print("Gamepad3 A button released.")

#     device.set_callback(device.BUTTON_A, gamepad_key_a_event)
#     print("Gamepad3 A button test started. Press Ctrl-C to stop.")
#     try:
#         while True:
#             device.tick()
#             time.sleep_ms(interval_ms)
#     except KeyboardInterrupt:
#         print("Gamepad3 button test stopped.")
#     finally:
#         device.set_callback(device.BUTTON_A, None)
#     return device


# def test_faces_keyboard3(
#     address: int = _FacesModule._DEFAULT_ADDRESS,
#     direct: bool = True,
#     interval_ms: int = 20,
# ) -> FacesKeyboard3Module:
#     """Run the Faces Keyboard3 LED and key test from the REPL.

#     Set ``direct=True`` to inspect the matrix key state. Press ``Ctrl-C`` to stop;
#     the test then turns both LEDs off and restores Normal mode.
#     """
#     device = FacesKeyboard3Module(address)
#     _print_faces_info(device)

#     def on_key(args, get_char=not direct):
#         if get_char:
#             print("Pressed char:", chr(args))
#         else:
#             print("Pressed keys:", args)

#     try:
#         device.set_mode(device.DIRECT)

#         print("Testing LED effects 1-8, then off.")
#         for effect in range(device.LED_EFFECT_1, device.LED_EFFECT_8 + 1):
#             print("LED effect:", effect)
#             device.set_led_effect(effect)
#             time.sleep_ms(1000)
#         device.set_led_effect(device.LED_EFFECT_OFF)

#         print("Testing LEDs: left, right, both, off.")
#         for left, right in ((True, False), (False, True), (True, True), (False, False)):
#             device.set_led(left, right)
#             time.sleep_ms(500)

#         device.set_mode(device.DIRECT if direct else device.NORMAL)
#         device.set_callback(on_key)
#         print(
#             "Keyboard3 %s test started. Press Ctrl-C to stop." % ("Direct" if direct else "Normal")
#         )
#         while True:
#             device.tick()
#             time.sleep_ms(interval_ms)
#     except KeyboardInterrupt:
#         print("Keyboard3 key test stopped.")
#     finally:
#         device.set_callback(None)
#         cleanup = (
#             (device.set_mode, (device.DIRECT,)),
#             (device.set_led, (False, False)),
#             (device.set_mode, (device.NORMAL,)),
#         )
#         for operation, args in cleanup:
#             try:
#                 operation(*args)
#             except Exception as error:
#                 print("Keyboard3 cleanup failed:", error)
#     return device


# keyboard = FacesKeyboard3Module()

# keyboard_mode = keyboard.NORMAL

# if keyboard_mode == keyboard.NORMAL:
#     keyboard.set_mode(keyboard.NORMAL)


#     def keyboard_normal_event(args, get_char=False):
#         if get_char:
#             print("Pressed char:", chr(args))
#         else:
#             print("Pressed keys:", args)

#     keyboard.set_callback(keyboard_normal_event)
# else:
#     keyboard.set_mode(keyboard.DIRECT)


#     def keyboard_direct_event(args):
#         print("Pressed keys:", args)


#     keyboard.set_callback(keyboard_direct_event)

# while True:
#     keyboard.tick()
#     time.sleep_ms(20)

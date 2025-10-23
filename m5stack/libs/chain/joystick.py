# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct


class JoystickChain(KeyChain):
    """Joystick Chain class for interacting with joystick devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the joystick on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import JoystickChain

            chainbus_0 = ChainBus(2, 32, 33, verbose=True)
            joystick_0 = JoystickChain(chainbus_0, 1)
    """

    CMD_GET_POSITION_16ADC = 0x30
    CMD_GET_POSITION_8ADC = 0x31
    CMD_GET_MAPPING = 0x32
    CMD_SET_MAPPING = 0x33
    CMD_GET_POSITION_16BIT = 0x34
    CMD_GET_POSITION_8BIT = 0x35

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def get_x(self) -> int:
        """Get the X position of the joystick.

        :return: X position (-128 to 127).
        :rtype: int

        UiFlow2 Code Block:

            |get_8bit_value.png|

        MicroPython Code Block:

            .. code-block:: python

                x = joystick_0.get_x()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_POSITION_8BIT, bytes()
        )
        if state:
            return response[0]
        return 0

    def get_y(self) -> int:
        """Get the Y position of the joystick.

        :return: Y position (-128 to 127).
        :rtype: int

        UiFlow2 Code Block:

            |get_8bit_value.png|

        MicroPython Code Block:

            .. code-block:: python

                y = joystick_0.get_y()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_POSITION_8BIT, bytes()
        )
        if state:
            return response[1]
        return 0

    def get_x_16bit(self) -> int:
        """Get the X position of the joystick in 16-bit resolution.

        :return: X position (-4095 to 4095).
        :rtype: int

        UiFlow2 Code Block:

            |get_16bit_value.png|

        MicroPython Code Block:

            .. code-block:: python

                x = joystick_0.get_x_16bit()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_POSITION_16BIT, bytes()
        )
        if state:
            return struct.unpack(">HH", response)[0]
        return 0

    def get_y_16bit(self) -> int:
        """Get the Y position of the joystick in 16-bit resolution.

        :return: Y position (-4095 to 4095).
        :rtype: int

        UiFlow2 Code Block:

            |get_16bit_value.png|

        MicroPython Code Block:

            .. code-block:: python

                y = joystick_0.get_y_16bit()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_POSITION_16BIT, bytes()
        )
        if state:
            return struct.unpack(">HH", response)[1]
        return 0

    def get_x_raw(self) -> int:
        """Get the raw X ADC value of the joystick.

        :return: Raw X ADC value (0-255).
        :rtype: int

        UiFlow2 Code Block:

            |get_raw_value.png|

        MicroPython Code Block:

            .. code-block:: python

                x = joystick_0.get_x_raw()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_POSITION_8ADC, bytes()
        )
        if state:
            return response[0]
        return 0

    def get_y_raw(self) -> int:
        """Get the raw Y ADC value of the joystick.

        :return: Raw Y ADC value (0-255).
        :rtype: int

        UiFlow2 Code Block:

            |get_raw_value.png|

        MicroPython Code Block:

            .. code-block:: python

                y = joystick_0.get_y_raw()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_POSITION_8ADC, bytes()
        )
        if state:
            return response[1]
        return 0

    def get_x_16bit_raw(self) -> int:
        """Get the raw X ADC value of the joystick in 16-bit resolution.

        :return: Raw X ADC value (0-65535).
        :rtype: int

        UiFlow2 Code Block:

            |get_raw_16bit_value.png|

        MicroPython Code Block:

            .. code-block:: python

                x = joystick_0.get_x_16bit_raw()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_POSITION_16ADC, bytes()
        )
        if state:
            return struct.unpack(">HH", response)[0]
        return 0

    def get_y_16bit_raw(self) -> int:
        """Get the raw Y ADC value of the joystick in 16-bit resolution.

        :return: Raw Y ADC value (0-65535).
        :rtype: int

        UiFlow2 Code Block:

            |get_raw_16bit_value.png|

        MicroPython Code Block:

            .. code-block:: python

                y = joystick_0.get_y_16bit_raw()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_POSITION_16ADC, bytes()
        )
        if state:
            return struct.unpack(">HH", response)[1]
        return 0

    def get_mapping_value(self) -> tuple:
        """Get the mapping values of the joystick.

        :return: A tuple containing the mapping values (x_negative_min, x_negative_max, x_positive_min, x_positive_max, y_negative_min, y_negative_max, y_positive_min, y_positive_max).
        :rtype: tuple

        UiFlow2 Code Block:

            |get_mapping_value.png|

        MicroPython Code Block:

            .. code-block:: python

                mapping = joystick_0.get_mapping_value()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_MAPPING, bytes())
        if state:
            return struct.unpack(">HHHHHHHH", response)
        return (0, 0, 0, 0, 0, 0, 0, 0)

    def set_mapping_value(self, value: tuple, save=False) -> bool:
        """Set the mapping values of the joystick.

        :param tuple value: A tuple containing the mapping values (x_negative_min, x_negative_max, x_positive_min, x_positive_max, y_negative_min, y_negative_max, y_positive_min, y_positive_max).
        :param bool save: Whether to save the mapping values to non-volatile memory.
        :return: True if the mapping values were set successfully, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_mapping_value.png|

        MicroPython Code Block:

            .. code-block:: python

                success = joystick_0.set_mapping_value((100, 200, 300, 400, 100, 200, 300, 400), True)
        """
        data = struct.pack(">HHHHHHHHB", *value, 1 if save else 0)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_MAPPING, data)
        if state:
            return response[0] == 1
        return False

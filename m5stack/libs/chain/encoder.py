# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct


class EncoderChain(KeyChain):
    """Encoder Chain class for interacting with encoder devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the encoder on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import EncoderChain

            chainbus_0 = ChainBus(2, 32, 33, verbose=True)
            encoder_0 = EncoderChain(chainbus_0, 1)
    """

    CMD_GET_VALUE = 0x10
    CMD_GET_INCREMENT = 0x11
    CMD_RESET_VALUE = 0x13
    CMD_RESET_INCREMENT = 0x14
    CMD_SET_CLOCKWISE_INCREASE = 0x15
    CMD_GET_CLOCKWISE_INCREASE = 0x16

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def get_encoder_value(self) -> int:
        """Get the encoder value.

        :return: Encoder value as int16_t (-32768 to 32767), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                value = encoder_0.get_encoder_value()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_VALUE, bytes())
        if state:
            if len(response) >= 2:
                return struct.unpack("<h", bytes([response[0], response[1]]))[0]
        return None

    def get_encoder_increment(self) -> int:
        """Get the encoder increment value.

        :return: Encoder increment value as int16_t (-32768 to 32767), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_encoder_increment.png|

        MicroPython Code Block:

            .. code-block:: python

                increment = encoder_0.get_encoder_increment()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_INCREMENT, bytes())
        if state:
            if len(response) >= 2:
                return struct.unpack("<h", bytes([response[0], response[1]]))[0]
        return None

    def reset_encoder_value(self) -> bool:
        """Reset the encoder value.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |reset_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                success = encoder_0.reset_encoder_value()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_RESET_VALUE, bytes())
        if state:
            return response[0] == 1
        return False

    def reset_encoder_increment(self) -> bool:
        """Reset the encoder increment value.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |reset_encoder_increment.png|

        MicroPython Code Block:

            .. code-block:: python

                success = encoder_0.reset_increment()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_RESET_INCREMENT, bytes())
        if state:
            return response[0] == 1
        return False

    def set_cw_increase(self, clockwise_increase: bool = False, save: bool = False) -> bool:
        """Set whether clockwise rotation increases the encoder value.

        :param bool clockwise_increase: Whether clockwise rotation increases. True means clockwise increases (sends 0), False means clockwise decreases (sends 1).
        :param bool save: Whether to save to flash. False means don't save, True means save.
        :return: True if the setting was set successfully, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_cw_increase.png|

        MicroPython Code Block:

            .. code-block:: python

                success = encoder_0.set_cw_increase(True, True)
        """
        payload = struct.pack("<BB", 0 if clockwise_increase else 1, 1 if save else 0)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_CLOCKWISE_INCREASE, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_cw_increase(self) -> bool:
        """Get whether clockwise rotation increases the encoder value.

        :return: Whether clockwise rotation increases. True means clockwise increases, False means clockwise decreases. Returns False if failed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_cw_increase.png|

        MicroPython Code Block:

            .. code-block:: python

                increase = encoder_0.get_cw_increase()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_CLOCKWISE_INCREASE, bytes()
        )
        if state:
            # Device returns 0 for clockwise increase, 1 for clockwise decrease
            # Convert to bool: 0 -> True (clockwise increase), 1 -> False (clockwise decrease)
            return response[0] == 0
        return False

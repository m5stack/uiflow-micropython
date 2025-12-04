# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct


class AngleChain(KeyChain):
    """Angle Chain class for interacting with angle devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the angle sensor on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import AngleChain

            chainbus_0 = ChainBus(2, 32, 33, verbose=True)
            angle_0 = AngleChain(chainbus_0, 1)
    """

    CMD_GET_ANGLE_12ADC = 0x30
    CMD_GET_ANGLE_8ADC = 0x31
    CMD_SET_CLOCKWISE_INCREASE = 0x32
    CMD_GET_CLOCKWISE_INCREASE = 0x33

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def get_adc12(self) -> int:
        """Get the angle value in 12-bit ADC resolution.

        :return: Angle value in 12-bit ADC (0-4095), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_adc12.png|

        MicroPython Code Block:

            .. code-block:: python

                angle = angle_0.get_adc12()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_ANGLE_12ADC, bytes())
        if state:
            return (response[1] << 8) | response[0]
        return None

    def get_adc8(self) -> int:
        """Get the angle value in 8-bit ADC resolution.

        :return: Angle value in 8-bit ADC (0-255), or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_adc8.png|

        MicroPython Code Block:

            .. code-block:: python

                angle = angle_0.get_adc8()
        """
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_ANGLE_8ADC, bytes())
        if state:
            return response[0]
        return None

    def set_cw_increase(self, increase: bool = True, save: bool = False) -> bool:
        """Set whether clockwise rotation increases the angle value.

        :param bool increase: Whether clockwise rotation increases. False means clockwise decreases, True means clockwise increases.
        :param bool save: Whether to save to flash. False means don't save, True means save.
        :return: True if the setting was set successfully, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_cw_increase.png|

        MicroPython Code Block:

            .. code-block:: python

                success = angle_0.set_cw_increase(True, False)
        """
        payload = struct.pack("<BB", 1 if increase else 0, 1 if save else 0)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_CLOCKWISE_INCREASE, payload
        )
        if state:
            return response[0] == 1
        return False

    def get_cw_increase(self) -> bool:
        """Get whether clockwise rotation increases the angle value.

        :return: Whether clockwise rotation increases. False means clockwise decreases, True means clockwise increases. Returns False if failed.
        :rtype: bool

        UiFlow2 Code Block:

            |get_cw_increase.png|

        MicroPython Code Block:

            .. code-block:: python

                increase = angle_0.get_cw_increase()
        """
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_CLOCKWISE_INCREASE, bytes()
        )
        if state:
            return response[0] == 1
        return False

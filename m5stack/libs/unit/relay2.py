# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import Pin


class Relay2Unit:
    """Create an Relay2Unit object.

    :param tuple port: The port of the relay.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import Relay2Unit

            relay2_0 = Relay2Unit((32, 26))
    """

    def __init__(self, port: tuple) -> None:
        self._relay1 = Pin(port[0], Pin.OUT)
        self._relay2 = Pin(port[1], Pin.OUT)

    def set_relay_cntrl(self, num: int = 1, control: int = 0) -> None:
        """Set the on/off status of a relay

        :param int num: The relay number(the range is 1-2).
        :param int control: The control value(0: off, 1: on).

        UiFlow2 Code Block:

            |set_relay_cntrl.png|

        MicroPython Code Block:

            .. code-block:: python

                relay2_0.set_relay_cntrl(1, 1)
        """
        self._relay1(control) if num == 1 else self._relay2(control)

    def get_relay_status(self, num: int = 1) -> bool:
        """Getting the on/off status of a relay

        :param int num: The relay number.
        :returns: relay status.
        :rtype: bool

        UiFlow2 Code Block:

            |get_relay_status.png|

        MicroPython Code Block:

            .. code-block:: python

                relay2_0.get_relay_status()
        """
        return bool(self._relay1() if num == 1 else self._relay2())

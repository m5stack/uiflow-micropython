# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import rf433


class RF433TUnit:
    """Create an RF433TUnit object.

    :param list|tuple port: Tuple containing grove port pin numbers.

     UiFlow2 Code Block:

         |init.png|

     MicroPython Code Block:

         .. code-block:: python

             from unit import RF433TUnit

             unit_rf433t = RF433TUnit(port=(8, 9))
    """

    def __init__(self, port: list | tuple = None):
        self.tx = rf433.Tx(out_pin=port[1])

    def send(self, data: bytes | bytearray) -> None:
        """Send data.

        :param data: The data to send.
        :type data: bytes | bytearray

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_rf433t.send(data)
        """
        self.tx.send(data)

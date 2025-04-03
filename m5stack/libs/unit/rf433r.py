# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import rf433
from micropython import schedule


class RF433RUnit:
    """Create an RF433RUnit object.

    :param list|tuple port: Tuple containing grove port pin numbers.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import RF433RUnit

            unit_rf433r = RF433RUnit(port=(36, 26))
    """

    def __init__(self, port: list | tuple = None):
        self.rx = rf433.Rx(in_pin=port[0])
        self.callback = None

    def set_recv_callback(self, callback):
        """Set receive data callback function.

        :param callback: A function that will be called when data is received.

        UiFlow2 Code Block:

            |set_recv_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def unit_rf433r_receive_event(received_data):
                    rf433r_data = received_data

                unit_rf433r.set_recv_callback(unit_rf433r_receive_event)
        """
        self.callback = callback

        def _irq_callback(t):
            if self.callback:
                data = self.read()
                if data:
                    schedule(self.callback, data)

        self.rx.set_recv_callback(_irq_callback)

    def start_recv(self) -> None:
        """Start receive data.

        UiFlow2 Code Block:

            |start_recv.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_rf433r.start_recv()
        """
        self.rx.start_recv()

    def stop_recv(self) -> None:
        """Stop receive data.

        UiFlow2 Code Block:

            |stop_recv.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_rf433r.stop_recv()
        """
        self.rx.stop_recv()

    def read(self) -> bytes | None:
        """Read data.

        :returns: receive data.
        :rtype: bytes | None

        If no data is received, return None.

        UiFlow2 Code Block:

            |read.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_rf433r.read()
        """
        return self.rx.read()

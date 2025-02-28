# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine


class AtomicPWMBase:
    """Create an AtomicPWMBase object.

    :param int out_pin: The PWM output pin. Default is 5.
    :param int freq: The PWM frequency. Default is 1000.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomicPWMBase

            base_pwm = AtomicPWMBase(out_pin=5, freq=1000)
    """

    def __init__(self, out_pin: int = 5, freq: int = 1000) -> None:
        self.pwm = machine.PWM(machine.Pin(out_pin), freq=freq, duty=0)

    def set_freq(self, freq: int = 1000) -> None:
        """Set PWM frequency.

        :param int freq: The PWM frequency. Default is 1000.

        UiFlow2 Code Block:

            |set_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                base_pwm.set_freq()
        """
        self.pwm.freq(freq)

    def get_freq(self) -> int:
        """Get PWM frequency.

        :returns: PWM frequency.
        :rtype: int

        UiFlow2 Code Block:

            |get_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                base_pwm.get_freq()
        """
        return self.pwm.freq()

    def set_duty_u16(self, duty: int = 0):
        """Set PWM duty cycle.

        set the current duty cycle of the PWM output, as an unsigned 16-bit value in the range 0 to 65535 inclusive.

        :param int duty: The PWM duty cycle. Range: 0 ~ 65535. Default is 0.

        UiFlow2 Code Block:

            |set_duty_u16.png|

        MicroPython Code Block:

            .. code-block:: python

                base_pwm.set_duty_u16()
        """
        self.pwm.duty_u16(duty)

    def get_duty_u16(self) -> int:
        """Get PWM duty cycle.

        :returns: PWM duty cycle. Range: 0~65535.
        :rtype: int

        UiFlow2 Code Block:

            |get_duty_u16.png|

        MicroPython Code Block:

            .. code-block:: python

                base_pwm.get_duty_u16()
        """
        return self.pwm.duty_u16()

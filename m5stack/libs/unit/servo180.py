# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import time
import sys

if sys.platform != "esp32":
    from typing import Optional


class Servo180Unit:
    """Control a 180-degree servo motor.

    :param port: The port the servo is connected to.
    :type port: tuple
    :param int pin: The pin the servo is connected to (if not using a port).
    :param int freq: The PWM frequency. Default is 50Hz.
    :param int count_low: The duty cycle microseconds count for 0 degrees. Default is 500.
    :param int count_high: The duty cycle microseconds count for 180 degrees. Default is 2500.

    UiFlow2 Code Block:

        |init.png|

        |init_advanced.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import Servo180Unit
            servo_0 = Servo180Unit((33, 32)) # Adjust the port as needed
            servo_1 = Servo180Unit(None, pin=15)  # Directly specify the pin
    """

    def __init__(
        self, port: Optional[tuple] = None, pin=0, freq=50, count_low=500, count_high=2500
    ):
        if port:
            pin = port[1]

        self._count_low = count_low
        self._count_high = count_high
        self._last_duty = self._count_low
        self.pwm = machine.PWM(pin, freq=freq, duty_ns=self._count_low * 1000)

    def set_angle(self, angle: int, wait=True) -> None:
        """Set the servo to a specific angle.

        :param int angle: Angle in degrees (0 to 180).
        :param bool wait: Whether to wait for the servo to reach the position.

        UiFlow2 Code Block:

            |set_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                servo_0.set_angle(90)  # Set servo to 90 degrees
        """
        if angle < 0:
            angle = 0
        elif angle > 180:
            angle = 180
        # 0.5ms(500000ns) - 2.5ms(2500000ns)
        duty = self._count_low + int((angle / 180) * (self._count_high - self._count_low))
        self.set_duty(duty, wait)

    def set_duty(self, duty: int, wait=True) -> None:
        """Set the duty cycle in microseconds.

        :param int duty: Duty cycle in microseconds (500 to 2500).
        :param bool wait: Whether to wait for the servo to reach the position.

        UiFlow2 Code Block:

            |set_duty.png|

        MicroPython Code Block:

        .. code-block:: python

            servo_0.set_duty(1500)  # Set duty to 1500 microseconds
        """
        print(f"Setting duty_ns: {duty}")
        self.pwm.duty_ns(duty * 1000)
        if wait:
            # 60 degree = 0.1s
            # 0.3s(180 degree) / 2000 = 0.00015
            time.sleep(abs(duty - self._last_duty) * 0.00015)
        self._last_duty = duty

    def set_percent(self, percent: int, wait=True) -> None:
        """Set the servo position as a percentage.

        :param int percent: Position as a percentage (0 to 100).
        :param bool wait: Whether to wait for the servo to reach the position.

        UiFlow2 Code Block:

            |set_percent.png|

        MicroPython Code Block:

            .. code-block:: python

                servo_0.set_percent(50)  # Set servo to 50% position
        """
        if percent < 0:
            percent = 0
        elif percent > 100:
            percent = 100
        self.set_angle(int(percent / 100 * 180), wait)

    def set_radian(self, radian: float, wait=True) -> None:
        """Set the servo position in radians.

        :param float radian: Position in radians (0 to π).
        :param bool wait: Whether to wait for the servo to reach the position.

        UiFlow2 Code Block:

            |set_radian.png|

        MicroPython Code Block:

            .. code-block:: python

                servo_0.set_radian(1.57)  # Set servo to π/2 radians
        """
        if radian < 0:
            radian = 0
        elif radian > 3.1415926535:
            radian = 3.1415926535
        self.set_angle(int(radian * 57.29577951), wait)

    def deinit(self):
        """Deinitialize the servo motor."""
        self.pwm.deinit()

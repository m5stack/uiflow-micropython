# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .servo180 import Servo180Unit
import sys

if sys.platform != "esp32":
    from typing import Optional


class Servo360Unit(Servo180Unit):
    """Control a 360-degree continuous rotation servo motor.

    .. note::

        For Servo Kit 360°, the duty cycle microseconds count controls rotation
        speed and direction: **count_low** corresponds to maximum
        clockwise speed, **count_high** to maximum counterclockwise speed, and
        the **midpoint** value indicates stop. Values in
        **count_low** ~ **midpoint** rotate clockwise
        (smaller values = faster speed), while values in
        **midpoint** ~ **count_high** rotate counterclockwise
        (larger values = faster speed). **midpoint** controls the stop position.

    :param port: The port the servo is connected to.
    :type port: tuple
    :param int pin: The pin the servo is connected to (if not using a port).
    :param int freq: The PWM frequency. Default is 50Hz.
    :param int count_low: The duty cycle microseconds count for the lowest range. Default is 500.
    :param int count_high: The duty cycle microseconds count for the highest range. Default is 2500.

    UiFlow2 Code Block:

        |init.png|

        |init_advanced.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import Servo360Unit

            servo_0 = Servo360Unit((33, 32)) # Adjust the port as needed
            servo_1 = Servo360Unit(None, pin=15)  # Directly specify the pin
    """

    def __init__(
        self, port: Optional[tuple] = None, pin=0, freq=50, count_low=500, count_high=2500
    ):
        super().__init__(port, pin, freq, count_low, count_high)
        self._median_duty = (self._count_low + self._count_high) // 2
        self._duty_range = (self._count_high - self._count_low) // 2

    def clockwise(self, speed: int, wait=True) -> None:
        """Rotate the servo clockwise at a specified speed.

        :param int speed: Speed percentage (0 to 100).
        :param bool wait: Whether to wait for the operation to complete.


        UiFlow2 Code Block:

            |clockwise.png|

        MicroPython Code Block:

            .. code-block:: python

                servo_0.clockwise(50)  # Rotate clockwise at 50% speed
        """
        if speed < 0:
            speed = 0
        elif speed > 100:
            speed = 100

        # Ensure a minimum speed to overcome static friction
        if 0 < speed < 10:
            speed = 10

        duty = self._median_duty - int((speed / 100) * self._duty_range)
        self.set_duty(duty, wait)

    def counterclockwise(self, speed: int, wait=True) -> None:
        """Rotate the servo counterclockwise at a specified speed.

        :param int speed: Speed percentage (0 to 100).
        :param bool wait: Whether to wait for the operation to complete.

        UiFlow2 Code Block:

            |counterclockwise.png|

        MicroPython Code Block:

            .. code-block:: python

                servo_0.counterclockwise(50)  # Rotate counterclockwise at 50% speed
        """
        if speed < 0:
            speed = 0
        elif speed > 100:
            speed = 100

        # Ensure a minimum speed to overcome static friction
        if 0 < speed < 10:
            speed = 10

        duty = self._median_duty + int((speed / 100) * self._duty_range)
        self.set_duty(duty, wait)

    def stop(self, wait=True) -> None:
        """Stop the servo rotation.

        :param bool wait: Whether to wait for the operation to complete.

        UiFlow2 Code Block:

            |stop.png|

        MicroPython Code Block:

            .. code-block:: python

                servo_0.stop()  # Stop the servo
        """
        self.set_duty(self._median_duty, wait)

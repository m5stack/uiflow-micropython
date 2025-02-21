# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   motion.py
@Time    :   2024/4/28
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

from machine import I2C
import struct
from driver.ina226 import INA226


class Motion:
    """Create an Motion object.

    :param I2C i2c: The I2C port to use.
    :param int address: The device address.  Default is 0x38.

    UiFlow2 Code Block:

        |__init__.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import Motion
            from machine import I2C

            i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)
            motion = Motion(i2c0, 0x38)
    """

    def __init__(self, i2c: I2C, address: int | list | tuple = 0x38) -> None:
        self.i2c = i2c
        self.addr = address
        self._available()
        self.ina = None
        self.addr_ina266 = 0x40
        if self.addr_ina266 in self.i2c.scan():
            self.ina = INA226(
                self.i2c, addr=self.addr_ina266, shunt_resistor=0.02
            )  # shunt resistor 20mΩ
            self.ina.configure(
                avg=self.ina.CFG_AVGMODE_16SAMPLES,
                vbus_conv_time=self.ina.CFG_VBUSCT_1100us,
                vshunt_conv_time=self.ina.CFG_VSHUNTCT_1100us,
                mode=self.ina.CFG_MODE_SANDBVOLT_CONTINUOUS,
            )
            self.ina.calibrate(max_expected_current=3.6)  # max expected current 3.6A

    def _available(self) -> None:
        """! Check if sensor is available on the I2C bus.

        Raises:
            Exception: If the sensor is not found.
        """
        if self.addr not in self.i2c.scan():
            raise Exception("Motion Base not found, please check your connection.")

    def get_servo_angle(self, ch: int) -> int:
        """Get the angle of the servo.

        :param int ch: The servo channel. Range: 1~4.
        :returns: Specify the servo angle for the specified channel. Range: 0~180.
        :rtype: int

        UiFlow2 Code Block:

            |get_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.get_servo_angle()
        """
        ch = int(min(4, ch))
        ch = int(max(1, ch))
        ch -= 1
        return self.i2c.readfrom_mem(self.addr, ch, 1)[0]

    def set_servo_angle(self, ch, angle) -> None:
        """Set the angle of the servo.

        :param int ch: The servo channel. Range: 1~4.
        :param int angle: The servo angle. Range: 0~180.

        UiFlow2 Code Block:

            |set_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.set_servo_angle()
        """
        ch = int(min(4, ch))
        ch = int(max(1, ch))
        ch -= 1
        angle = int(min(180, angle))
        angle = int(max(0, angle))
        self.i2c.writeto_mem(self.addr, ch, struct.pack("b", angle))

    def get_servo_pulse(self, ch) -> int:
        """Get the pulse of the servo.

        :param int ch: The servo channel. Range: 1~4.
        :returns: Specify the servo pulse for the specified channel. Range: 500~2500.
        :rtype: int

        UiFlow2 Code Block:

            |get_servo_pulse.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.get_servo_pulse()
        """
        ch = int(min(4, ch))
        ch = int(max(1, ch))
        ch -= 1
        return struct.unpack(">h", self.i2c.readfrom_mem(self.addr, ch * 2 + 0x10, 2))[0]

    def write_servo_pulse(self, ch, pulse) -> None:
        """Write the pulse of the servo.

        :param int ch: The servo channel. Range: 1~4.
        :param int pulse: The servo pulse. Range: 500~2500.

        UiFlow2 Code Block:

            |write_servo_pulse.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.write_servo_pulse()
        """
        ch = int(min(4, ch))
        ch = int(max(1, ch))
        ch -= 1
        pulse = int(min(2500, pulse))
        pulse = int(max(500, pulse))
        self.i2c.writeto_mem(self.addr, ch * 2 + 0x10, struct.pack(">h", pulse))

    def get_motor_speed(self, ch) -> int:
        """Get the speed of the motor.

        :param int ch: The motor id. Range: 1~2.
        :returns: Specify the speed for the specified channel. Range: -127~127.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.get_motor_speed()
        """
        ch = int(min(2, ch))
        ch = int(max(1, ch))
        ch -= 1
        speed = self.i2c.readfrom_mem(self.addr, ch + 0x20, 1)[0]
        if speed > 128:
            return speed - 256
        return speed

    def set_motor_speed(self, ch, speed) -> None:
        """Set motor speed.

        :param int ch: The motor channel. Range: 1~2.
        :param int speed: The motor speed. Range: -127~127.

        UiFlow2 Code Block:

            |set_motor_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.set_motor_speed()
        """
        ch = int(min(2, ch))
        ch = int(max(1, ch))
        ch -= 1
        speed = int(min(127, speed))
        speed = int(max(-127, speed))
        self.i2c.writeto_mem(self.addr, ch + 0x20, struct.pack("b", speed))

    def read_voltage(self) -> float:
        """Read voltage (unit: V).

        :returns: The voltage value in volts.
        :rtype: float

        .. note::
            This method is supported only on Motion Base v1.1 and later versions.

        UiFlow2 Code Block:

            |read_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.read_voltage()
        """
        return self.ina.read_bus_voltage()

    def read_current(self) -> float:
        """Read current (unit: A).

        :returns: The current value in amperes.
        :rtype: float

        .. note::
            This method is supported only on Motion Base v1.1 and later versions.

        UiFlow2 Code Block:

            |read_current.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.read_current()
        """
        return self.ina.read_current()

    def read_power(self) -> float:
        """Read power (unit: W).

        :returns: The power value in watts.
        :rtype: float

        .. note::
            This method is supported only on Motion Base v1.1 and later versions.

        UiFlow2 Code Block:

            |read_power.png|

        MicroPython Code Block:

            .. code-block:: python

                motion.read_power()
        """
        return self.ina.read_power()

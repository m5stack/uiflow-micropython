# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from module.mbus import i2c1
import struct
from micropython import const


SLAVE_ADDR = const(0x56)  # I2C slave address
MOTOR_ADDR_BASE = const(0x00)  # Motor control base register
ENCODER_ADDR_BASE = const(0x08)  # Encoder register base
MOTOR_COUNT = const(4)  # Number of motors


class DCMotorModule:
    """Create an DCMotorModule object.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import DCMotorModule

            dcmotor_module = DCMotorModule()
    """

    def __init__(self):
        self.i2c = i2c1
        self.addr = SLAVE_ADDR
        self.encoder_offset = [0] * MOTOR_COUNT  # store clear offset

    def set_motor_speed(self, id: int, speed: int) -> None:
        """Set speed of motor.

        :param int id: port num, range: 1~4
        :param int speed: motor speed, range: -255~255

        UiFlow2 Code Block:

            |set_motor_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                dcmotor_module.set_motor_speed(id, speed)
        """
        if not 1 <= id <= MOTOR_COUNT:
            raise ValueError("id must be 1~4")
        speed = max(-255, min(255, speed))  # Clamp speed
        reg = MOTOR_ADDR_BASE + (id - 1) * 2
        val = struct.pack("<h", speed)
        try:
            self.i2c.writeto_mem(self.addr, reg, val)
        except Exception as e:
            print("I2C write error:", e)

    def set_motor_speed_percent(self, id: int, percent: float) -> None:
        """Set motor speed as a percentage.

        :param int id: port num, range: 1~4.
        :param float percent: motor speed percent, range: -100.0% ~ +100.0%.

        UiFlow2 Code Block:

            |set_motor_speed_percent.png|

        MicroPython Code Block:

            .. code-block:: python

                dcmotor_module.set_motor_speed_percent(id, percent)
        """
        if not -100.0 <= percent <= 100.0:
            raise ValueError("percent must be in -100.0 to 100.0")
        speed = int(percent * 255 / 100)
        self.set_motor_speed(id, speed)

    def get_encoder(self, id: int) -> int:
        """Get encoder count.

        :param int id: port num, range: 1~4.
        :returns: encoder count.
        :rtype: int

        UiFlow2 Code Block:

            |get_encoder.png|

        MicroPython Code Block:

            .. code-block:: python

                dcmotor_module.get_encoder()
        """
        if not 1 <= id <= MOTOR_COUNT:
            raise ValueError("id must be 1~4")
        reg = ENCODER_ADDR_BASE + (id - 1) * 4
        try:
            val = self.i2c.readfrom_mem(self.addr, reg, 4)
            raw_value = struct.unpack("<i", val)[0]
            return raw_value - self.encoder_offset[id - 1]
        except Exception as e:
            print("I2C read error:", e)
            return 0

    def clear_encoder(self, id: int) -> bool:
        """Clear encoder value.

        UiFlow2 Code Block:

            |clear_encoder.png|

        MicroPython Code Block:

            .. code-block:: python

                dcmotor_module.clear_encoder()
        """
        if not 1 <= id <= MOTOR_COUNT:
            raise ValueError("id must be 1~4")
        current = self.get_encoder(id) + self.encoder_offset[id - 1]
        self.encoder_offset[id - 1] = current
        return True

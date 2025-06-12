# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import machine


class AtomicStepmotorBase:
    """Create an AtomicStepmotorBase object.

    :param int en: Enable pin, used to enable or disable the stepper motor.
    :param int dir: Direction pin, used to control the rotation direction of the motor.
    :param int stp: Step pin, used for step control of the motor.
    :param int flt: Fault pin, used to monitor the motor's fault status.
    :param int rst: Reset pin, used to reset the motor driver.
    :param int pwr_adc: Power ADC monitoring pin, used to measure the input power supply voltage.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomicStepmotorBase

            base_stepmotor = AtomicStepmotorBase(en=5, dir=7, stp=6, flt=38, rst=39, pwr_adc=8)
    """

    def __init__(
        self,
        en: int = 5,
        dir: int = 7,
        stp: int = 6,
        flt: int = 38,
        rst: int = 39,
        pwr_adc: int = 8,
    ):
        self.en_pin = machine.Pin(en, machine.Pin.OUT)
        self.dir_pin = machine.Pin(dir, machine.Pin.OUT)
        self.stp_pin = machine.Pin(stp, machine.Pin.OUT)
        self.flt_pin = machine.Pin(flt, machine.Pin.IN) if flt else None
        self.rst_pin = machine.Pin(rst, machine.Pin.OUT) if rst else None
        self.adc = machine.ADC(machine.Pin(pwr_adc), atten=machine.ADC.ATTN_11DB)
        self.use_read_uv = hasattr(self.adc, "read_uv")
        self.enable()

    def enable(self) -> None:
        """Enable the stepper motor driver.

        UiFlow2 Code Block:

            |enable.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.enable()
        """
        self.en_pin.value(0)

    def disable(self):
        """Disable the stepper motor driver.

        UiFlow2 Code Block:

            |disable.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.disable()
        """
        self.en_pin.value(1)

    def set_direction(self, direction: bool = True) -> None:
        """Set direction.

        :param bool direction: Rotation direction. True or False.

        UiFlow2 Code Block:

            |set_direction.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.set_direction(direction)
        """
        self.dir_pin.value(1 if direction else 0)

    def step(self) -> None:
        """Move the stepper motor one step.

        UiFlow2 Code Block:

            |step.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.step()
        """
        self.stp_pin.value(1)
        time.sleep_us(500)
        self.stp_pin.value(0)
        time.sleep_us(500)

    def rotate(self, steps: int, delay_ms: int = 0, direction: bool = True) -> None:
        """Rotate the stepper motor for a specified number of steps.

        :param int steps: Number of steps to rotate.
        :param int delay_ms: Delay between steps (in milliseconds), default is 0ms.
        :param bool direction: Rotation direction (True or False).

        The actual rotation direction (clockwise or counterclockwise) depends on the motor wiring.

        UiFlow2 Code Block:

            |rotate.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.rotate(steps, delay_ms, direction)
        """
        self.set_direction(direction)
        for _ in range(steps):
            self.step()
            if delay_ms > 0:
                time.sleep_ms(delay_ms)

    def stop(self) -> None:
        """Stop motor.

        UiFlow2 Code Block:

            |stop.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.stop()
        """
        self.stp_pin.value(0)

    def get_status(self) -> bool:
        """Get motor driver status.

        :returns: Returns True if the driver is operating normally, or False if a fault is detected.
        :rtype: bool

        UiFlow2 Code Block:

            |get_status.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.get_status()
        """
        return (self.flt_pin.value() != 0) if self.flt_pin else True

    def reset(self) -> None:
        """Reset the stepper motor driver.

        UiFlow2 Code Block:

            |reset.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.reset()
        """
        if self.rst_pin:
            self.rst_pin.value(0)
            time.sleep_ms(10)
            self.rst_pin.value(1)

    def get_voltage(self) -> float:
        """Get voltage.

        :returns: The driver input voltage. unit: V
        :rtype: float

        UiFlow2 Code Block:

            |get_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                base_stepmotor.get_voltage()
        """
        if self.use_read_uv:
            return self.adc.read_uv() * (6 / 1_000_000.0)  # x6 是因为输入为 VIN 的 1/ 6
        else:
            return ((self.adc.read() / 4096) * 3.6) / (1.5 / 9) * 0.99

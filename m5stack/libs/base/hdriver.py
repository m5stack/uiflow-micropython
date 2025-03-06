# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine


class AtomicHDriverBase:
    """Create an AtomicHDriverBase object.

    :param int in1: PWM control pin1.
    :param int in2: PWM control pin2.
    :param int fault: driver status.
    :param int vin: driver input voltage detect.
    :param int freq: The PWM frequency.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomicHDriverBase

            base_hdriver = AtomicHDriverBase(in1 = 6, in2 = 7, fault = 5, vin = 8, freq = 1000)
    """

    def __init__(
        self, in1: int = 6, in2: int = 7, fault: int = 5, vin: int = 8, freq: int = 1000
    ) -> None:
        self.pwm_freq = freq
        self.pwm_in1 = machine.PWM(machine.Pin(in1), freq=self.pwm_freq, duty=0)
        self.pwm_in2 = machine.PWM(machine.Pin(in2), freq=self.pwm_freq, duty=0)
        self.fault = machine.Pin(fault, machine.Pin.IN)
        self.adc = machine.ADC(machine.Pin(vin), atten=machine.ADC.ATTN_11DB)
        self.adc.atten(machine.ADC.ATTN_6DB)  # 设置 ADC 采样范围（输入电压为：9~24V 的 1/10）

    def set_freq(self, freq: int = 1000) -> None:
        """Set PWM frequency.

        :param int freq: The PWM frequency. Default is 1000.

        UiFlow2 Code Block:

            |set_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                base_hdriver.set_freq()
        """
        self.pwm_freq = freq
        self.pwm_in1.freq(self.pwm_freq)
        self.pwm_in2.freq(self.pwm_freq)

    def get_freq(self) -> int:
        """Get PWM frequency.

        :returns: PWM frequency.
        :rtype: int

        UiFlow2 Code Block:

            |get_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                base_hdriver.get_freq()
        """
        return self.pwm_freq

    def set_speed(self, speed: float = 0) -> None:
        """Set motor speed.

        :param float speed: The motor speed. Range -100~100. Default is 0.

        UiFlow2 Code Block:

            |set_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                base_hdriver.set_speed()
        """
        speed = max(-100, min(speed, 100))
        if speed > 0:
            self.pwm_in1.duty_u16(int(speed / 100.0 * 65535))
            self.pwm_in2.duty_u16(0)
        elif speed < 0:
            self.pwm_in1.duty_u16(0)
            self.pwm_in2.duty_u16(int(-speed / 100.0 * 65535))
        else:
            self.pwm_in1.duty_u16(0)
            self.pwm_in2.duty_u16(0)

    def get_status(self) -> bool:
        """Get driver status.

        :returns: The driver status. Returns True if the driver is operating normally, or False if a fault is detected.
        :rtype: bool

        UiFlow2 Code Block:

            |get_status.png|

        MicroPython Code Block:

            .. code-block:: python

                base_hdriver.get_status()
        """
        return self.fault.value() != 0  # 在故障状况期间下拉为低电平。

    def get_voltage(self) -> float:
        """Get voltage.

        :returns: The driver input voltage. unit: V
        :rtype: float

        UiFlow2 Code Block:

            |get_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                base_hdriver.get_voltage()
        """
        return self.adc.read_uv() * 10 / 1_000_000.0  # x10 是因为输入为 VIN 的 1/10

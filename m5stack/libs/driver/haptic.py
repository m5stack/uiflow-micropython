# SPDX-FileCopyrightText: 2022 lbuque
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import PWM
from .soft_timer import SoftTimer


class Haptic:
    """A simple haptic feedback motor driver module.
    Control the motor through pwm and timer to simulate the effect of haptic feedback.

    :param Pin pin: pin is the entity on which the PWM is output, which is usually a machine.Pin object
    :param int freq: Frequency of PWM output
    """

    _timer = None

    def __init__(self, pin, freq: int = 100) -> None:
        self._pwm = PWM(pin, freq=freq, duty_u16=0)
        if self._timer is None:
            self._timer = SoftTimer()

    def once(self, freq=10, duty=50, duration: int = 50) -> None:
        """Play the haptic effect once on the motor.
        :param int duration: The duration of the haptic effect, in milliseconds.
        """
        self._timer.init(period=duration, mode=SoftTimer.ONE_SHOT, callback=self._cb)
        self._pwm.init(freq=freq, duty_u16=duty * 65535 // 100)

    def _cb(self) -> None:
        self._pwm.duty_u16(0)

    def set_freq(self, freq):
        self._pwm.freq(freq)

    def set_duty(self, duty):
        self._pwm.duty_u16(duty * 65535 // 100)

    def turn_off(self):
        self._pwm.duty_u16(0)

    def deinit(self) -> None:
        """Disabled Haptic Driver."""
        self._timer.deinit()
        self._pwm.deinit()

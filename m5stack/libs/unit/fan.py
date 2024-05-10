# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import PWM


class FanUnit:
    def __init__(self, port: tuple):
        self._pwm = PWM(port[1], freq=250, duty=0)

    def set_pwm_freq(self, freq):
        self._pwm.freq(freq)

    def set_speed_ctrl(self, speed):
        duty = self.map(speed, 1, 100, 70, 1023) if speed else 0
        self._pwm.duty(duty)

    def map(self, x, in_min, in_max, out_min, out_max):
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

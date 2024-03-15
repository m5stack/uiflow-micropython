# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# the sound speed on air (343.2 m/s), that It's equivalent to 0.34320 mm/us that is 1mm each 2.91us
# pulse_time // 2 // 2.91 -> pulse_time // 5.82 -> pulse_time * 100 // 582
# echo timeout -> max=4500mm, 4500 * 2.91us -> 0.0131 * 2 -> 0.0262 or 26.2ms
# echo timeout -> 1000000us or 1s

import machine
from machine import Pin
import time


class ULTRASONIC_IOUnit:
    def __init__(self, port, echo_timeout_us=1000000):
        self.echo_timeout_us = echo_timeout_us
        # trigger pin (out)
        self.trigger = Pin(port[1], mode=Pin.OUT, pull=None)
        self.trigger.value(0)
        # echo pin (in)
        self.echo = Pin(port[0], mode=Pin.IN, pull=None)

    def tx_pulse_rx_echo(self):
        self.trigger.value(0)
        time.sleep_us(5)
        # Send a 10us pulse.
        self.trigger.value(1)
        time.sleep_us(10)
        self.trigger.value(0)
        try:
            echo_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return echo_time
        except:
            pass

    def get_target_distance(self, mode=1):
        """
        Get the distance in milimeters or centimeters.
        """
        echo_time = self.tx_pulse_rx_echo()
        time.sleep_ms(50)
        if mode == 1:
            mm = echo_time * 100 // 582
            return mm
        elif mode == 2:
            cm = (echo_time * 100 // 582) / 10
            return cm

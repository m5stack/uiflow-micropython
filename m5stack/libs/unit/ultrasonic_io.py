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
    """
    note:
        en: UNIT SONIC IO is a GPIO interface ultrasonic range sensor. This module features an RCWL-9620 ultrasonic distance measurement chip with a 16mm probe, which the ranging accuracy can reach 2cm-450cm (accuracy up to ±2%). This sensor determines the distance to a target by measuring time lapses between the transmitting and receiving of the pulse signal, users can directly obtain the distance value through IO control mode. It is ideal to apply in robotics obstacle avoidance, fluid level detection, and other applications that require you to perform measurements.

    details:
        link: https://docs.m5stack.com/en/unit/UNIT%20SONIC%20IO
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/UNIT%20SONIC%20IO/img-4ba90df3-6a11-4870-b605-c55983992d76.webp
        category: Unit

    example:
        - ../../../examples/unit/ultrasonic/ultrasonic_cores3_example.py

    m5f2:
        - unit/ultrasonic/ultrasonic_cores3_example.m5f2
    """

    def __init__(self, port, echo_timeout_us=1000000):
        """
        note:
            en: Initialize the ultrasonic unit with the specified port and echo timeout.

        params:
            port:
                note: A tuple representing the port pins for trigger (output) and echo (input).
            echo_timeout_us:
                note: Timeout for the echo signal in microseconds, default is 1,000,000.
        """
        self.echo_timeout_us = echo_timeout_us
        # trigger pin (out)
        self.trigger = Pin(port[1], mode=Pin.OUT, pull=None)
        self.trigger.value(0)
        # echo pin (in)
        self.echo = Pin(port[0], mode=Pin.IN, pull=None)

    def tx_pulse_rx_echo(self):
        """
        note:
            en: Send a trigger pulse and wait to receive the echo response.

        params:
            note:

        returns:
            note: The duration of the echo response in microseconds or None if a timeout occurs.
        """
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
        note:
            en: Calculate the distance to the target based on echo response time.

        params:
            mode:
                note: The unit of measurement for the distance. Use 1 for millimeters, 2 for centimeters.

        returns:
            note: The distance to the target in the specified unit.
        """
        echo_time = self.tx_pulse_rx_echo()
        time.sleep_ms(50)
        if mode == 1:
            mm = echo_time * 100 // 582
            return mm
        elif mode == 2:
            cm = (echo_time * 100 // 582) / 10
            return cm


class UltrasoundIOUnit(ULTRASONIC_IOUnit):
    def __init__(self, port, echo_timeout_us=1000000):
        super().__init__(port, echo_timeout_us)

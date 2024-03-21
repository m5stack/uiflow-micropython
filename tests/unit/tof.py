# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
from machine import I2C, Pin
from unit import ToFUnit

# Initialize I2C bus and sensor.
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
tof = ToFUnit(i2c, io_timeout_ms=500)

# Main loop will read the range and print it every second.
while True:
    print("Range: {0}mm".format(tof.get_range()))
    time.sleep(1.0)

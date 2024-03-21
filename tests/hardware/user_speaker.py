# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from M5 import Speaker


# User buzzer only need data out pin and set buzzer flag.
Speaker.config(dout=3, buzzer=True)
Speaker.setVolume(100)
Speaker.tone(freq=6000, msec=100)

# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from addon import DisplayIn


def setup():
    display_in = DisplayIn()
    size = display_in.capture("/flash/lt6911_capture.jpg", quality=75, timeout_ms=2000)
    print("saved /flash/lt6911_capture.jpg ({} bytes)".format(size))
    display_in.deinit()


if __name__ == "__main__":
    setup()

# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# PowerHub RGB driver
from . import NeoPixel
from machine import Pin
from M5 import Led


class PowerHubRGB(NeoPixel):
    def __init__(self) -> None:
        print("PowerHubRGB initialized")
        pass

    def _map(self, x: int, in_min: int, in_max: int, out_min: int, out_max: int) -> int:
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def set_color(self, index: int, color: int) -> None:
        if index < 0:
            return
        Led.setColor(index, color)
        Led.display()

    def fill_color(self, color: int) -> None:
        Led.setAllColor(color)
        Led.display()

    def set_brightness(self, br: int) -> None:
        br = self._map(br, 0, 100, 0, 255)
        Led.setBrightness(br)

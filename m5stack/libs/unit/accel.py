# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.adxl34x import ADXL345


class AccelUnit(ADXL345):
    def __init__(self, i2c, address=0x53):
        super().__init__(i2c, address=address)

    def get_accel(self) -> tuple[float, float, float]:
        return self.acceleration

    def get_data_rate(self) -> int:
        return self.data_rate

    def set_data_rate(self, rate: int):
        self.data_rate = rate

    def get_range(self) -> int:
        return self.range

    def set_range(self, range: int):
        self.range = range

    def is_tap(self) -> bool:
        ret = self.events.get("tap")
        return ret if ret else False

    def is_motion(self) -> bool:
        ret = self.events.get("motion")
        return ret if ret else False

    def is_freefall(self) -> bool:
        ret = self.events.get("freefall")
        return ret if ret else False

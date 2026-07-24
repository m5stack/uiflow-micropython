# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.nfc import NFCReader


class NFCUnit(NFCReader):
    """Unit NFC: pass a pre-built ``I2C`` (e.g. ``SoftI2C``)."""

    def __init__(self, i2c):
        super().__init__(i2c)

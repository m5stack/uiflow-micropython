# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .stamps3 import StampS3_Startup


class AtomS3Lite_Startup(StampS3_Startup):
    """AtomS3 Lite startup menu"""

    def __init__(self) -> None:
        super().__init__()

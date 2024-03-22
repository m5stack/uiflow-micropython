# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .stamps3 import StampS3_Startup


class AtomS3U_Startup(StampS3_Startup):
    """AtomS3U startup menu"""

    def __init__(self) -> None:
        super().__init__()

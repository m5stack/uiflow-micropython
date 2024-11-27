# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from typing import Union, Literal

RGB565: int
GRAYSCALE: int
YUV422: int
FRAME_96X96: int
FRAME_QQVGA: int
FRAME_QCIF: int
FRAME_HQVGA: int
FRAME_240X240: int
FRAME_QVGA: int
FRAME_CIF: int
FRAME_HVGA: int
FRAME_VGA: int

DRAM: int
PSRAM: int

def init(
    pixformat: int = RGB565,
    framesize: int = FRAME_QVGA,
    fb_count: int = 2,
    fb_location: int = PSRAM,
) -> bool: ...
def deinit() -> bool: ...
def skip_frames(time: int = 300) -> None: ...
def capture() -> bytes: ...
def capture_to_jpg(quality=int) -> bytes: ...
def capture_to_bmp() -> bytes: ...
def pixformat(format: RGB565 | GRAYSCALE | YUV422) -> bool: ...
def framesize(
    size: FRAME_96X96
    | FRAME_QQVGA
    | FRAME_QCIF
    | FRAME_HQVGA
    | FRAME_240X240
    | FRAME_QVGA
    | FRAME_CIF
    | FRAME_HVGA
    | FRAME_VGA,
) -> bool: ...
def contrast(value: -2 | -1 | 0 | 1 | 2) -> bool: ...
def global_gain(value: Union[Literal[0], Literal[1], ..., Literal[0x3F]]) -> bool: ...
def hmirror(direction: Union[Literal[0], Literal[1]]) -> bool: ...
def vflip(direction: Union[Literal[0], Literal[1]]) -> bool: ...
def colorbar(enable: Union[Literal[0], Literal[1]]) -> bool: ...

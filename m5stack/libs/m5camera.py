import camera
from camera import (
    deinit,
    skip_frames,
    capture,
    capture_to_jpg,
    capture_to_bmp,
    pixformat,
    contrast,
    global_gain,
    hmirror,
    vflip,
    colorbar,
)
import M5
from collections import namedtuple
import gc

YUV422 = camera.YUV422
GRAYSCALE = camera.GRAYSCALE
RGB565 = camera.RGB565

FRAME_96X96 = camera.FRAME_96X96
FRAME_QQVGA = camera.FRAME_QQVGA
FRAME_QCIF = camera.FRAME_QCIF
FRAME_HQVGA = camera.FRAME_HQVGA
FRAME_240X240 = camera.FRAME_240X240
FRAME_QVGA = camera.FRAME_QVGA
FRAME_CIF = camera.FRAME_CIF
FRAME_HVGA = camera.FRAME_HVGA
FRAME_VGA = camera.FRAME_VGA

IN_DRAM = camera.DRAM
IN_PSRAM = camera.PSRAM

FrameSize = namedtuple("FrameSize", ["width", "height"])

_frame_size_table = {
    FRAME_96X96: FrameSize(width=96, height=96),
    FRAME_QQVGA: FrameSize(width=160, height=120),
    FRAME_QCIF: FrameSize(width=176, height=144),
    FRAME_HQVGA: FrameSize(width=240, height=176),
    FRAME_240X240: FrameSize(width=240, height=240),
    FRAME_QVGA: FrameSize(width=320, height=240),
    FRAME_CIF: FrameSize(width=400, height=296),
    FRAME_HVGA: FrameSize(width=480, height=320),
    FRAME_VGA: FrameSize(width=640, height=480),
}


_x = 0
_y = 0
_width = 0
_height = 0
_max_width = 0
_max_height = 0
_frame_size = None
_visible = True


def init(
    x, y, width, height, pixformat=RGB565, framesize=FRAME_QVGA, fb_count=2, fb_location=IN_PSRAM
) -> None:
    global _x, _y, _width, _height, _max_width, _max_height, _frame_size
    _x = x
    _y = y
    _max_width = width
    _max_height = height
    _frame_size = _frame_size_table.get(framesize)
    _width = _frame_size.width if _frame_size.width < _max_width else _max_width
    _height = _frame_size.height if _frame_size.height < _max_height else _max_height
    camera.init(
        pixformat=pixformat, framesize=framesize, fb_count=fb_count, fb_location=fb_location
    )
    # camera.skip_frames(10)


def framesize(size) -> None:
    frame_size = _frame_size_table.get(size)
    if frame_size is None:
        return
    global _width, _height, _max_width, _max_height
    _width = frame_size.width if frame_size.width < _max_width else _max_width
    _height = frame_size.height if frame_size.height < _max_height else _max_height
    camera.framesize(size)


def disp_to_screen():
    global _visible
    if _visible:
        raw = camera.capture_to_bmp()
        if raw:
            M5.Lcd.drawBmp(raw, _x, _y, _width, _height)
            del raw
            gc.collect()


def setCursor(x=0, y=0, w=0, h=0):
    global _x, _y, _max_width, _width, _max_height, _height, _frame_size
    _x = x
    _y = y
    frame_size = _frame_size_table.get(_frame_size)
    if w is not 0:
        _max_width = w
        _width = frame_size.width if frame_size.width < _max_width else _max_width
    if h is not 0:
        _max_height = h
        _height = frame_size.height if frame_size.height < _max_height else _max_height


def setVisible(enable: bool):
    global _visible
    _visible = enable

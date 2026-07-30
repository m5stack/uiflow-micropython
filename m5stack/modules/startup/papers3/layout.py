# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5


REFERENCE_WIDTH = 540
REFERENCE_HEIGHT = 960

WIDTH = M5.Lcd.width()
HEIGHT = M5.Lcd.height()
IS_PAPERMONO = M5.getBoard() == M5.BOARD.M5PaperMono
RESOURCE_DIR = "/system/papermono" if IS_PAPERMONO else "/system/papers3"
SCALE = min(WIDTH / REFERENCE_WIDTH, HEIGHT / REFERENCE_HEIGHT)
SCALE_X = SCALE
SCALE_Y = SCALE
CONTENT_WIDTH = int(REFERENCE_WIDTH * SCALE + 0.5)
CONTENT_HEIGHT = int(REFERENCE_HEIGHT * SCALE + 0.5)
OFFSET_X = int((WIDTH - CONTENT_WIDTH) / 2 + 0.5)
OFFSET_Y = int((HEIGHT - CONTENT_HEIGHT) / 2 + 0.5)
DYNAMIC_BG_COLOR = 0xAAAAAA if IS_PAPERMONO else 0xE3E3E3


def x(value):
    return OFFSET_X + size(value)


def y(value):
    return OFFSET_Y + size(value)


def size(value):
    return int(value * SCALE + 0.5)


def resource_path(name):
    return RESOURCE_DIR + "/" + name


def image_source(path):
    if not IS_PAPERMONO or not path:
        return path
    with open(path, "rb") as image_file:
        image_data = image_file.read()
    print("PaperMono image loaded: {}, {} bytes".format(path, len(image_data)))
    return image_data


def draw_background(path):
    M5.Lcd.drawImage(image_source(path), 0, 0)
    if IS_PAPERMONO:
        print("PaperMono background drawn:", path)


def begin_full_refresh():
    if IS_PAPERMONO:
        M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_TEXT)
        M5.Lcd.startWrite()


def end_full_refresh():
    if IS_PAPERMONO:
        M5.Lcd.endWrite()
        M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_FASTEST)


def set_full_refresh_mode():
    if IS_PAPERMONO:
        M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_TEXT)


def touch_point(x_pos, y_pos):
    if not IS_PAPERMONO:
        return x_pos, y_pos
    return (
        int(y_pos * WIDTH / HEIGHT + 0.5),
        int((WIDTH - 1 - x_pos) * HEIGHT / WIDTH + 0.5),
    )


def large_font():
    if IS_PAPERMONO:
        return M5.Lcd.FONTS.Montserrat36
    return M5.Lcd.FONTS.Montserrat40


def app_list_font():
    if IS_PAPERMONO:
        return M5.Lcd.FONTS.Montserrat24
    return M5.Lcd.FONTS.Montserrat40


def settings_font():
    if IS_PAPERMONO:
        return M5.Lcd.FONTS.Montserrat20
    return M5.Lcd.FONTS.Montserrat24

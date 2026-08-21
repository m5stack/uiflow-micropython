# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import sys, io, M5


def print_error_msg(e: Exception, lcd=M5.Lcd) -> None:
    e_msg = io.StringIO()
    sys.print_exception(e, e_msg)
    e_msg.seek(0)
    error_str = e_msg.read()
    board_id = M5.getBoard()

    # CoreMatrix has a 16x16 LED matrix; reuse the startup error indicator
    # instead of trying to render a full traceback with a large LCD font.
    if board_id == M5.BOARD.M5CoreMatrix:
        from startup.corematrix import MatrixStatusDisplay

        MatrixStatusDisplay().set_color(0, 0xFF0000)
    else:
        # print error message to lcd
        lcd.setCursor(0, 0)
        if board_id != M5.BOARD.M5PaperColor:
            lcd.setTextColor(0xFF0000, 0x000000)
        else:
            lcd.setTextColor(0x000000, 0xFFFFFF)
        if board_id == M5.BOARD.M5StopWatch:
            lcd.setFont(lcd.FONTS.Montserrat16)
            lcd.clear()
            _print_wrapped(lcd, error_str, 68, 68, 330, 330)
        else:
            lcd.setFont(lcd.FONTS.Montserrat12)
            lcd.clear()
            lcd.print(error_str)
    # print error message to repl
    print(error_str)
    e_msg.close()
    # deinit
    M5.end()


def _print_wrapped(lcd, text, x, y, w, h):
    line_h = lcd.fontHeight()
    cur_x = x
    cur_y = y
    lcd.setCursor(cur_x, cur_y)

    for ch in text:
        if ch == "\n":
            cur_x = x
            cur_y += line_h
            if cur_y + line_h > y + h:
                break
            lcd.setCursor(cur_x, cur_y)
            continue

        ch_w = lcd.textWidth(ch)
        if cur_x + ch_w > x + w:
            cur_x = x
            cur_y += line_h
            if cur_y + line_h > y + h:
                break
            lcd.setCursor(cur_x, cur_y)

        lcd.print(ch)
        cur_x += ch_w

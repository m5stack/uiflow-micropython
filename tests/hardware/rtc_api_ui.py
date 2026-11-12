# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
# SPDX-License-Identifier: MIT
"""StopWatch: show expected/actual RTC readings on one M5UI page."""

import sys
import time

import M5
import m5ui
import lvgl as lv
from hardware import RTC


page = None
labels = []


def label(text, y, color=0xFFFFFF, font=None):
    if font is None:
        font = lv.font_montserrat_24
    item = m5ui.M5Label(text, text_c=color, font=font, parent=page)
    item.align_to(page, lv.ALIGN.TOP_MID, 0, y)
    labels.append(item)
    return item


def show_readings(utc_label, local_label, rtc):
    utc = rtc.datetime()
    local = rtc.local_datetime()
    utc_label.set_text("UTC: %02d:%02d:%02d" % (utc[4], utc[5], utc[6]))
    local_label.set_text("Local: %02d:%02d:%02d" % (local[4], local[5], local[6]))
    # Recenter after replacing the shorter placeholder strings.
    utc_label.align_to(page, lv.ALIGN.TOP_MID, 0, utc_label.get_y())
    local_label.align_to(page, lv.ALIGN.TOP_MID, 0, local_label.get_y())
    print("UTC tuple:", utc)
    print("Local tuple:", local)


def setup():
    global page
    M5.begin()
    m5ui.init()
    page = m5ui.M5Page(bg_c=0x101820)
    label("RTC comparison", 57, 0x59C7EE)

    label("1. init()", 110, 0x59C7EE)
    label("Expect UTC 10:20:30 / Local 18:20:30", 146, font=lv.font_montserrat_18)
    init_utc = label("UTC: waiting", 178)
    init_local = label("Local: waiting", 210)

    label("2. datetime()", 264, 0x59C7EE)
    label("Expect UTC 01:02:03 / Local 09:02:03", 300, font=lv.font_montserrat_18)
    datetime_utc = label("UTC: waiting", 332)
    datetime_local = label("Local: waiting", 364)
    status = label("Starting...", 404, 0xFFD479, lv.font_montserrat_18)
    page.screen_load()
    time.sleep_ms(100)

    rtc = RTC()
    saved_epoch = time.time()
    saved_ticks = time.ticks_ms()
    saved_zone = rtc.timezone()
    try:
        rtc.timezone("GMT+8")
        print("init input: (2026, 11, 12, 10, 20, 30, 99, 123456)")
        rtc.init((2026, 11, 12, 10, 20, 30, 99, 123456))
        show_readings(init_utc, init_local, rtc)

        print("datetime input: (2026, 11, 12, 99, 1, 2, 3, 654321)")
        rtc.datetime((2026, 11, 12, 99, 1, 2, 3, 654321))
        show_readings(datetime_utc, datetime_local, rtc)
        status.set_text("Readings frozen for comparison")
    except Exception as exc:
        status.set_text("RTC error - see serial log")
        sys.print_exception(exc)
    finally:
        try:
            rtc.timezone(saved_zone if saved_zone is not None else "GMT+0")
            elapsed = time.ticks_diff(time.ticks_ms(), saved_ticks) // 1000
            now = time.gmtime(saved_epoch + elapsed)
            rtc.datetime((now[0], now[1], now[2], now[6], now[3], now[4], now[5], 0))
            print("Original clock restored (within 1s).")
            if saved_zone is None:
                print("Timezone was unset; left at GMT+0.")
        except Exception as exc:
            status.set_text("Restore error - see serial log")
            sys.print_exception(exc)
    status.align_to(page, lv.ALIGN.TOP_MID, 0, 404)


if __name__ == "__main__":
    setup()
    while True:
        M5.update()
        time.sleep_ms(20)

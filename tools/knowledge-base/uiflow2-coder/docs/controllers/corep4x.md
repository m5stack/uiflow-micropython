# CoreP4X

Support the following products:

    CoreP4X

## Supported Components

CoreP4X supports the following components:

- `M5UI`: The `m5ui` LVGL component library.

- `Unit`: The `unit` package containing Unit drivers.

- `Module`: The `module` package for expansion modules.

- `Chain`: The `chain` package for Chain devices.

- `USB`: The `usb.device` package for HID devices.

## Supported Display Fonts

The CoreP4X firmware includes the following Montserrat fonts for LVGL and M5UI: `lv.font_montserrat_12`, `lv.font_montserrat_14`, `lv.font_montserrat_16`, `lv.font_montserrat_18`, `lv.font_montserrat_20`, `lv.font_montserrat_22`, `lv.font_montserrat_24`, `lv.font_montserrat_30`, `lv.font_montserrat_36`, `lv.font_montserrat_40`, `lv.font_montserrat_44`, `lv.font_montserrat_48`.

For `M5.Lcd.FONTS`, the firmware also provides `AlibabaPuHuiTiCN24`, `AlibabaSansJA24`, and `AlibabaSansKR24` for Chinese, Japanese, and Korean text respectively.

## Board Features

CoreP4X supports the following built-in functions and peripherals:

- 480 x 480 display and capacitive touch input.

- [IMU](../hardware/imu.md) accelerometer and gyroscope readings.

- RTC date and time display and adjustment.

- USB and battery voltage monitoring, charging status, and Port A 5 V output control.

- [Speaker](../hardware/speaker.md) tone playback, volume adjustment, and PA control.

- [Microphone](../hardware/mic.md) recording and speaker playback.

- [Infrared](../hardware/ir.md) NEC transmission and reception.

## MicroPython Example

#### RTC Clock

Display the date and a blue HH:MM:SS clock from the built-in RTC, using UTC. Tap **SET TIME** to adjust hours, minutes, and seconds with the **+** and **-** buttons. Tap **SAVE** to update the RTC while preserving the date, or **CANCEL** to discard the changes.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import RTC
import time

page_live = None
page_edit = None
label_title = None
label_date = None
label_live_hour = None
label_live_colon_1 = None
label_live_min = None
label_live_colon_2 = None
label_live_sec = None
button_set = None
label_edit_title = None
label_hour_name = None
label_min_name = None
label_sec_name = None
label_hour = None
label_min = None
label_sec = None
button_hour_plus = None
button_hour_minus = None
button_min_plus = None
button_min_minus = None
button_sec_plus = None
button_sec_minus = None
button_cancel = None
button_save = None
rtc = None

edit_hour = None
edit_min = None
edit_sec = None

def button_set_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    page_edit.screen_load()
    edit_hour = (rtc.datetime())[4]
    edit_min = (rtc.datetime())[5]
    edit_sec = (rtc.datetime())[6]
    if edit_hour < 10:
        label_hour.set_text(str((str("0") + str(edit_hour))))
    else:
        label_hour.set_text(str(edit_hour))
    if edit_min < 10:
        label_min.set_text(str((str("0") + str(edit_min))))
    else:
        label_min.set_text(str(edit_min))
    if edit_sec < 10:
        label_sec.set_text(str((str("0") + str(edit_sec))))
    else:
        label_sec.set_text(str(edit_sec))

def button_hour_plus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_hour = (edit_hour + 1) % 24
    if edit_hour < 10:
        label_hour.set_text(str((str("0") + str(edit_hour))))
    else:
        label_hour.set_text(str(edit_hour))

def button_hour_minus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_hour = (edit_hour + -1) % 24
    if edit_hour < 10:
        label_hour.set_text(str((str("0") + str(edit_hour))))
    else:
        label_hour.set_text(str(edit_hour))

def button_min_plus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_min = (edit_min + 1) % 60
    if edit_min < 10:
        label_min.set_text(str((str("0") + str(edit_min))))
    else:
        label_min.set_text(str(edit_min))

def button_min_minus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_min = (edit_min + -1) % 60
    if edit_min < 10:
        label_min.set_text(str((str("0") + str(edit_min))))
    else:
        label_min.set_text(str(edit_min))

def button_sec_plus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_sec = (edit_sec + 1) % 60
    if edit_sec < 10:
        label_sec.set_text(str((str("0") + str(edit_sec))))
    else:
        label_sec.set_text(str(edit_sec))

def button_sec_minus_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    edit_sec = (edit_sec + -1) % 60
    if edit_sec < 10:
        label_sec.set_text(str((str("0") + str(edit_sec))))
    else:
        label_sec.set_text(str(edit_sec))

def button_cancel_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    page_live.screen_load()

def button_save_clicked_event(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    rtc.init(
        (
            ((rtc.datetime())[0]),
            ((rtc.datetime())[1]),
            ((rtc.datetime())[2]),
            edit_hour,
            edit_min,
            edit_sec,
            0,
            0,
        )
    )
    page_live.screen_load()

def button_set_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_set_clicked_event(event_struct)
    return

def button_hour_plus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_hour_plus_clicked_event(event_struct)
    return

def button_hour_minus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_hour_minus_clicked_event(event_struct)
    return

def button_min_plus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_min_plus_clicked_event(event_struct)
    return

def button_min_minus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_min_minus_clicked_event(event_struct)
    return

def button_sec_plus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_sec_plus_clicked_event(event_struct)
    return

def button_sec_minus_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_sec_minus_clicked_event(event_struct)
    return

def button_cancel_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_cancel_clicked_event(event_struct)
    return

def button_save_event_handler(event_struct):
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_save_clicked_event(event_struct)
    return

def setup():
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page_live = m5ui.M5Page(bg_c=0x080808)
    page_edit = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "RTC (UTC)",
        x=24,
        y=22,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page_live,
    )
    label_date = m5ui.M5Label(
        "---- -- --",
        x=175,
        y=104,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page_live,
    )
    label_live_hour = m5ui.M5Label(
        "--",
        x=105,
        y=160,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    label_live_colon_1 = m5ui.M5Label(
        ":",
        x=175,
        y=156,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    label_live_min = m5ui.M5Label(
        "--",
        x=205,
        y=160,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    label_live_colon_2 = m5ui.M5Label(
        ":",
        x=275,
        y=156,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    label_live_sec = m5ui.M5Label(
        "--",
        x=305,
        y=160,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_live,
    )
    button_set = m5ui.M5Button(
        text="SET TIME",
        x=32,
        y=368,
        bg_c=0x245A85,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_live,
    )
    label_edit_title = m5ui.M5Label(
        "Set UTC Time",
        x=158,
        y=22,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page_edit,
    )
    label_hour_name = m5ui.M5Label(
        "HOUR",
        x=62,
        y=72,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    label_min_name = m5ui.M5Label(
        "MIN",
        x=212,
        y=72,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    label_sec_name = m5ui.M5Label(
        "SEC",
        x=362,
        y=72,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    label_hour = m5ui.M5Label(
        "00",
        x=56,
        y=190,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_edit,
    )
    label_min = m5ui.M5Label(
        "00",
        x=206,
        y=190,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_edit,
    )
    label_sec = m5ui.M5Label(
        "00",
        x=356,
        y=190,
        text_c=0x4DA6FF,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page_edit,
    )
    button_hour_plus = m5ui.M5Button(
        text="+",
        x=36,
        y=106,
        bg_c=0x176C48,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_hour_minus = m5ui.M5Button(
        text="-",
        x=36,
        y=270,
        bg_c=0x7A2731,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_min_plus = m5ui.M5Button(
        text="+",
        x=186,
        y=106,
        bg_c=0x176C48,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_min_minus = m5ui.M5Button(
        text="-",
        x=186,
        y=270,
        bg_c=0x7A2731,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_sec_plus = m5ui.M5Button(
        text="+",
        x=336,
        y=106,
        bg_c=0x176C48,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_sec_minus = m5ui.M5Button(
        text="-",
        x=336,
        y=270,
        bg_c=0x7A2731,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_cancel = m5ui.M5Button(
        text="CANCEL",
        x=32,
        y=368,
        bg_c=0x3B4850,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )
    button_save = m5ui.M5Button(
        text="SAVE",
        x=252,
        y=368,
        bg_c=0x245A85,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_18,
        parent=page_edit,
    )

    button_set.add_event_cb(button_set_event_handler, lv.EVENT.ALL, None)
    button_hour_plus.add_event_cb(button_hour_plus_event_handler, lv.EVENT.ALL, None)
    button_hour_minus.add_event_cb(button_hour_minus_event_handler, lv.EVENT.ALL, None)
    button_min_plus.add_event_cb(button_min_plus_event_handler, lv.EVENT.ALL, None)
    button_min_minus.add_event_cb(button_min_minus_event_handler, lv.EVENT.ALL, None)
    button_sec_plus.add_event_cb(button_sec_plus_event_handler, lv.EVENT.ALL, None)
    button_sec_minus.add_event_cb(button_sec_minus_event_handler, lv.EVENT.ALL, None)
    button_cancel.add_event_cb(button_cancel_event_handler, lv.EVENT.ALL, None)
    button_save.add_event_cb(button_save_event_handler, lv.EVENT.ALL, None)

    page_live.screen_load()
    rtc = RTC()
    button_set.set_size(416, 72)
    button_hour_plus.set_size(108, 54)
    button_hour_minus.set_size(108, 54)
    button_min_plus.set_size(108, 54)
    button_min_minus.set_size(108, 54)
    button_sec_plus.set_size(108, 54)
    button_sec_minus.set_size(108, 54)
    button_cancel.set_size(196, 72)
    button_save.set_size(196, 72)
    label_date.align_to(page_live, lv.ALIGN.TOP_MID, 0, 104)

def loop():
    global \
        page_live, \
        page_edit, \
        label_title, \
        label_date, \
        label_live_hour, \
        label_live_colon_1, \
        label_live_min, \
        label_live_colon_2, \
        label_live_sec, \
        button_set, \
        label_edit_title, \
        label_hour_name, \
        label_min_name, \
        label_sec_name, \
        label_hour, \
        label_min, \
        label_sec, \
        button_hour_plus, \
        button_hour_minus, \
        button_min_plus, \
        button_min_minus, \
        button_sec_plus, \
        button_sec_minus, \
        button_cancel, \
        button_save, \
        rtc, \
        edit_hour, \
        edit_min, \
        edit_sec
    M5.update()
    label_date.set_text(
        str(
            (
                str(
                    (
                        str((str((str("") + str(((rtc.datetime())[0])))) + str("-")))
                        + str(((rtc.datetime())[1]))
                    )
                )
                + str((str("-") + str(((rtc.datetime())[2]))))
            )
        )
    )
    if (rtc.datetime())[4] < 10:
        label_live_hour.set_text(str((str("0") + str(((rtc.datetime())[4])))))
    else:
        label_live_hour.set_text(str((rtc.datetime())[4]))
    if (rtc.datetime())[5] < 10:
        label_live_min.set_text(str((str("0") + str(((rtc.datetime())[5])))))
    else:
        label_live_min.set_text(str((rtc.datetime())[5]))
    if (rtc.datetime())[6] < 10:
        label_live_sec.set_text(str((str("0") + str(((rtc.datetime())[6])))))
    else:
        label_live_sec.set_text(str((rtc.datetime())[6]))
    label_date.align_to(page_live, lv.ALIGN.TOP_MID, 0, 104)
    time.sleep_ms(100)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### IMU Sensor

Display the X, Y, and Z readings from the built-in accelerometer and gyroscope. Acceleration is shown in g, and angular velocity in degrees per second (dps). Tilt or rotate the device to observe the readings.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time

page0 = None
label_title = None
label_subtitle = None
label_acc_x = None
label_acc_y = None
label_acc_z = None
label_gyro_x = None
label_gyro_y = None
label_gyro_z = None
label_gyro_title = None
accel = None
gyro = None
acc_x = None
acc_y = None
acc_z = None
gyro_x = None
gyro_y = None
gyro_z = None

def setup():
    global \
        page0, \
        label_title, \
        label_subtitle, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_x, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_title, \
        accel, \
        gyro, \
        acc_x, \
        acc_y, \
        acc_z, \
        gyro_x, \
        gyro_y, \
        gyro_z

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "IMU",
        x=24,
        y=18,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_subtitle = m5ui.M5Label(
        "Accel (g)",
        x=199,
        y=82,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_acc_x = m5ui.M5Label(
        "X: -- g",
        x=48,
        y=116,
        text_c=0x45D483,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_acc_y = m5ui.M5Label(
        "Y: -- g",
        x=48,
        y=156,
        text_c=0x45D483,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_acc_z = m5ui.M5Label(
        "Z: -- g",
        x=48,
        y=196,
        text_c=0x45D483,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_gyro_x = m5ui.M5Label(
        "X: -- dps",
        x=48,
        y=300,
        text_c=0xFFD04D,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_gyro_y = m5ui.M5Label(
        "Y: -- dps",
        x=48,
        y=340,
        text_c=0xFFD04D,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_gyro_z = m5ui.M5Label(
        "Z: -- dps",
        x=48,
        y=380,
        text_c=0xFFD04D,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_gyro_title = m5ui.M5Label(
        "Gyro (dps)",
        x=192,
        y=266,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    page0.screen_load()

def loop():
    global \
        page0, \
        label_title, \
        label_subtitle, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_x, \
        label_gyro_y, \
        label_gyro_z, \
        label_gyro_title, \
        accel, \
        gyro, \
        acc_x, \
        acc_y, \
        acc_z, \
        gyro_x, \
        gyro_y, \
        gyro_z
    M5.update()
    accel = Imu.getAccel()
    gyro = Imu.getGyro()
    acc_x = accel[0]
    acc_y = accel[1]
    acc_z = accel[2]
    gyro_x = gyro[0]
    gyro_y = gyro[1]
    gyro_z = gyro[2]
    label_acc_x.set_text(str((str("X: ") + str((str(acc_x) + str(" g"))))))
    label_acc_y.set_text(str((str("Y: ") + str((str(acc_y) + str(" g"))))))
    label_acc_z.set_text(str((str("Z: ") + str((str(acc_z) + str(" g"))))))
    label_gyro_x.set_text(str((str("X: ") + str((str(gyro_x) + str(" dps"))))))
    label_gyro_y.set_text(str((str("Y: ") + str((str(gyro_y) + str(" dps"))))))
    label_gyro_z.set_text(str((str("Z: ") + str((str(gyro_z) + str(" dps"))))))
    time.sleep_ms(200)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Power Management

Display USB VBUS and battery voltages in mV, charging status, Port A 5 V output, and charge control. The battery voltage turns green while the battery is charging. Tap **PORT A** to toggle external output and **CHARGE** to enable or disable charging. Battery percentage is not displayed.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time

page0 = None
label_title = None
label_vbus = None
label_battery = None
label_charging = None
label_port_a = None
label_charge_control = None
label_action = None
label_vbus_name = None
label_battery_name = None
label_charging_name = None
label_port_a_name = None
label_charge_control_name = None
button_port_a = None
button_charge = None

port_a_enabled = None
charge_enabled = None

def button_port_a_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    port_a_enabled = not port_a_enabled
    if port_a_enabled:
        Power.setExtOutput(True, 1)
    else:
        Power.setExtOutput(False, 1)
    if port_a_enabled:
        button_port_a.set_btn_text(str("PORT A: ON"))
        label_port_a.set_text(str("ON"))
    else:
        button_port_a.set_btn_text(str("PORT A: OFF"))
        label_port_a.set_text(str("OFF"))
    label_action.set_text(str("Port A 5V updated"))

def button_charge_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    charge_enabled = not charge_enabled
    if charge_enabled:
        Power.setBatteryCharge(True)
    else:
        Power.setBatteryCharge(False)
    if charge_enabled:
        button_charge.set_btn_text(str("CHARGE: ON"))
        label_charge_control.set_text(str("ON"))
    else:
        button_charge.set_btn_text(str("CHARGE: OFF"))
        label_charge_control.set_text(str("OFF"))
    label_action.set_text(str("Charge control updated"))

def button_port_a_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_port_a_clicked_event(event_struct)
    return

def button_charge_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button_charge_clicked_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "Power",
        x=24,
        y=18,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_vbus = m5ui.M5Label(
        "---- mV",
        x=284,
        y=82,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_battery = m5ui.M5Label(
        "---- mV",
        x=284,
        y=124,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_charging = m5ui.M5Label(
        "--",
        x=284,
        y=166,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_port_a = m5ui.M5Label(
        "OFF",
        x=284,
        y=208,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_charge_control = m5ui.M5Label(
        "ON",
        x=284,
        y=250,
        text_c=0xF1F5F7,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_action = m5ui.M5Label(
        "Power controls ready",
        x=24,
        y=342,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_vbus_name = m5ui.M5Label(
        "USB VBUS",
        x=24,
        y=82,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_battery_name = m5ui.M5Label(
        "Battery",
        x=24,
        y=124,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_charging_name = m5ui.M5Label(
        "Charging",
        x=24,
        y=166,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_port_a_name = m5ui.M5Label(
        "Port A 5 V",
        x=24,
        y=208,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_charge_control_name = m5ui.M5Label(
        "Charge control",
        x=24,
        y=250,
        text_c=0xA9BAC4,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    button_port_a = m5ui.M5Button(
        text="PORT A: OFF",
        x=24,
        y=388,
        bg_c=0x245A85,
        text_c=0xF1F5F7,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    button_charge = m5ui.M5Button(
        text="CHARGE: ON",
        x=252,
        y=388,
        bg_c=0x245A85,
        text_c=0xF1F5F7,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    button_port_a.add_event_cb(button_port_a_event_handler, lv.EVENT.ALL, None)
    button_charge.add_event_cb(button_charge_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Power.setExtOutput(False, 1)
    Power.setBatteryCharge(True)
    port_a_enabled = False
    charge_enabled = True
    button_port_a.set_size(204, 64)
    button_charge.set_size(204, 64)

def loop():
    global \
        page0, \
        label_title, \
        label_vbus, \
        label_battery, \
        label_charging, \
        label_port_a, \
        label_charge_control, \
        label_action, \
        label_vbus_name, \
        label_battery_name, \
        label_charging_name, \
        label_port_a_name, \
        label_charge_control_name, \
        button_port_a, \
        button_charge, \
        port_a_enabled, \
        charge_enabled
    M5.update()
    label_vbus.set_text(str((str("") + str((str((Power.getVBUSVoltage())) + str(" mV"))))))
    label_battery.set_text(str((str("") + str((str((Power.getBatteryVoltage())) + str(" mV"))))))
    if Power.isCharging():
        label_charging.set_text(str("YES"))
        label_battery.set_text_color(0x8EDA91, 255, 0)
    else:
        label_charging.set_text(str("NO"))
        label_battery.set_text_color(0xF1F5F7, 255, 0)
    time.sleep_ms(500)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Speaker Tone

Use separate sliders to adjust frequency from 200 to 4000 Hz and volume from 0 to 100%. The default values are 1000 Hz and 70%. Tap **Start tone** or **Stop tone** to control playback. The PA switch controls the amplifier independently; it is enabled at startup, while tone playback is stopped. Turning PA off mutes the output without stopping the tone.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time

page0 = None
label_title = None
label_output = None
label_pa = None
pa_switch = None
label_frequency_title = None
label_frequency = None
frequency_slider = None
label_frequency_min = None
label_frequency_max = None
label_volume_title = None
label_volume = None
volume_slider = None
label_volume_min = None
label_volume_max = None
tone_button = None

pa_requested = None
frequency = None
tone_toggle_pending = None
volume = None
pa_change_pending = None
frequency_change_pending = None
volume_change_pending = None
tone_enabled = None
pa_enabled = None

def pa_switch_checked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    pa_requested = pa_switch.has_state(lv.STATE.CHECKED)
    pa_change_pending = True

def pa_switch_unchecked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    pa_requested = pa_switch.has_state(lv.STATE.CHECKED)
    pa_change_pending = True

def frequency_slider_value_changed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    frequency = frequency_slider.get_value()
    label_frequency.set_text(str((str(frequency) + str(" Hz"))))
    label_frequency.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 152)
    frequency_change_pending = True

def tone_button_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    tone_toggle_pending = True

def volume_slider_value_changed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    volume = volume_slider.get_value()
    label_volume.set_text(str((str(volume) + str("%"))))
    label_volume.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 272)
    volume_change_pending = True

def pa_switch_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            pa_switch_checked_event(event_struct)
        else:
            pa_switch_unchecked_event(event_struct)
    return

def frequency_slider_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        frequency_slider_value_changed_event(event_struct)
    return

def tone_button_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        tone_button_clicked_event(event_struct)
    return

def volume_slider_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        volume_slider_value_changed_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "Speaker",
        x=24,
        y=24,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_output = m5ui.M5Label(
        "Stopped",
        x=384,
        y=28,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_pa = m5ui.M5Label(
        "Amplifier on",
        x=24,
        y=96,
        text_c=0x8EDA91,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    pa_switch = m5ui.M5Switch(
        x=384,
        y=84,
        w=72,
        h=40,
        bg_c=0x38383C,
        bg_c_checked=0x8EDA91,
        circle_c=0xF4F4F5,
        parent=page0,
    )
    label_frequency_title = m5ui.M5Label(
        "Frequency",
        x=24,
        y=158,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_frequency = m5ui.M5Label(
        "1000 Hz",
        x=320,
        y=152,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    frequency_slider = m5ui.M5Slider(
        x=40,
        y=206,
        w=400,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=200,
        max_value=4000,
        value=1000,
        bg_c=0x38383C,
        color=0x4DA6FF,
        parent=page0,
    )
    label_frequency_min = m5ui.M5Label(
        "200",
        x=40,
        y=232,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_frequency_max = m5ui.M5Label(
        "4000",
        x=384,
        y=232,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume_title = m5ui.M5Label(
        "Volume",
        x=24,
        y=278,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume = m5ui.M5Label(
        "70%",
        x=320,
        y=272,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    volume_slider = m5ui.M5Slider(
        x=40,
        y=326,
        w=400,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=70,
        bg_c=0x38383C,
        color=0x4DA6FF,
        parent=page0,
    )
    label_volume_min = m5ui.M5Label(
        "0",
        x=40,
        y=352,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume_max = m5ui.M5Label(
        "100%",
        x=384,
        y=352,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    tone_button = m5ui.M5Button(
        text="Start tone",
        x=24,
        y=388,
        bg_c=0x245A85,
        text_c=0xF4F4F5,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    pa_switch.add_event_cb(pa_switch_event_handler, lv.EVENT.ALL, None)
    frequency_slider.add_event_cb(frequency_slider_event_handler, lv.EVENT.ALL, None)
    tone_button.add_event_cb(tone_button_event_handler, lv.EVENT.ALL, None)
    volume_slider.add_event_cb(volume_slider_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Speaker.stop()
    frequency = 1000
    frequency_change_pending = False
    pa_requested = True
    pa_change_pending = False
    Speaker.setPA(True)
    pa_enabled = True
    tone_toggle_pending = False
    tone_enabled = False
    volume = 70
    volume_change_pending = False
    pa_requested = pa_enabled
    pa_switch.set_state(lv.STATE.CHECKED, pa_enabled)
    Speaker.setVolume(int((volume * 255 + 50) / 100))
    if pa_enabled:
        label_pa.set_text(str("Amplifier on"))
        label_pa.set_text_color(0x8EDA91, 255, 0)
    else:
        label_pa.set_text(str("Amplifier off"))
        label_pa.set_text_color(0x9A9A9F, 255, 0)
    if tone_enabled and (Speaker.isPlaying()):
        label_output.set_text(str("Playing"))
        label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
        label_output.set_text_color(0x8EDA91, 255, 0)
    else:
        label_output.set_text(str("Stopped"))
        label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
        label_output.set_text_color(0x9A9A9F, 255, 0)
    if tone_enabled:
        tone_button.set_btn_text(str("Stop tone"))
        tone_button.set_bg_color(0x8EDA91, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        tone_button.set_text_color(0x000000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        tone_button.set_btn_text(str("Start tone"))
        tone_button.set_bg_color(0x245A85, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        tone_button.set_text_color(0xF4F4F5, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    tone_button.set_size(432, 64)
    label_frequency.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 152)
    label_volume.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 272)
    label_frequency_max.align_to(page0, lv.ALIGN.TOP_RIGHT, -40, 232)
    label_volume_max.align_to(page0, lv.ALIGN.TOP_RIGHT, -40, 352)
    frequency_slider.set_bg_color(0x4DA6FF, 255, lv.PART.KNOB | lv.STATE.DEFAULT)
    volume_slider.set_bg_color(0x4DA6FF, 255, lv.PART.KNOB | lv.STATE.DEFAULT)
    frequency_slider.set_bg_color(0x38383C, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    volume_slider.set_bg_color(0x38383C, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

def loop():
    global \
        page0, \
        label_title, \
        label_output, \
        label_pa, \
        pa_switch, \
        label_frequency_title, \
        label_frequency, \
        frequency_slider, \
        label_frequency_min, \
        label_frequency_max, \
        label_volume_title, \
        label_volume, \
        volume_slider, \
        label_volume_min, \
        label_volume_max, \
        tone_button, \
        pa_requested, \
        frequency, \
        tone_toggle_pending, \
        volume, \
        pa_change_pending, \
        frequency_change_pending, \
        volume_change_pending, \
        tone_enabled, \
        pa_enabled
    M5.update()
    if pa_change_pending:
        pa_change_pending = False
        if pa_requested:
            Speaker.setPA(True)
            pa_enabled = True
        else:
            Speaker.setPA(False)
            pa_enabled = False
        if pa_enabled:
            label_pa.set_text(str("Amplifier on"))
            label_pa.set_text_color(0x8EDA91, 255, 0)
        else:
            label_pa.set_text(str("Amplifier off"))
            label_pa.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled and (Speaker.isPlaying()):
            label_output.set_text(str("Playing"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x8EDA91, 255, 0)
        else:
            label_output.set_text(str("Stopped"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled:
            tone_button.set_btn_text(str("Stop tone"))
            tone_button.set_bg_color(0x8EDA91, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0x000000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        else:
            tone_button.set_btn_text(str("Start tone"))
            tone_button.set_bg_color(0x245A85, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0xF4F4F5, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    if tone_toggle_pending:
        tone_toggle_pending = False
        tone_enabled = not tone_enabled
        if tone_enabled:
            Speaker.tone(frequency, 60000)
        else:
            Speaker.stop()
        if pa_enabled:
            label_pa.set_text(str("Amplifier on"))
            label_pa.set_text_color(0x8EDA91, 255, 0)
        else:
            label_pa.set_text(str("Amplifier off"))
            label_pa.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled and (Speaker.isPlaying()):
            label_output.set_text(str("Playing"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x8EDA91, 255, 0)
        else:
            label_output.set_text(str("Stopped"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled:
            tone_button.set_btn_text(str("Stop tone"))
            tone_button.set_bg_color(0x8EDA91, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0x000000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        else:
            tone_button.set_btn_text(str("Start tone"))
            tone_button.set_bg_color(0x245A85, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0xF4F4F5, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    if frequency_change_pending:
        frequency_change_pending = False
        if tone_enabled:
            Speaker.stop()
            Speaker.tone(frequency, 60000)
        if pa_enabled:
            label_pa.set_text(str("Amplifier on"))
            label_pa.set_text_color(0x8EDA91, 255, 0)
        else:
            label_pa.set_text(str("Amplifier off"))
            label_pa.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled and (Speaker.isPlaying()):
            label_output.set_text(str("Playing"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x8EDA91, 255, 0)
        else:
            label_output.set_text(str("Stopped"))
            label_output.align_to(page0, lv.ALIGN.TOP_RIGHT, -24, 28)
            label_output.set_text_color(0x9A9A9F, 255, 0)
        if tone_enabled:
            tone_button.set_btn_text(str("Stop tone"))
            tone_button.set_bg_color(0x8EDA91, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0x000000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        else:
            tone_button.set_btn_text(str("Start tone"))
            tone_button.set_bg_color(0x245A85, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
            tone_button.set_text_color(0xF4F4F5, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    if tone_enabled and not (Speaker.isPlaying()):
        Speaker.tone(frequency, 60000)
    time.sleep_ms(10)
    if volume_change_pending:
        volume_change_pending = False
        Speaker.setVolume(int((volume * 255 + 50) / 100))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Audio Recording and Playback

Record audio in memory at 8 kHz, mono, 16 bit. Tap **RECORD** to start and **STOP REC** to finish, with a maximum duration of 30 seconds. Tap **PLAY** to play the recording or **STOP PLAY** to stop playback. The volume slider ranges from 0 to 100%, with a default of 70%. PA is enabled automatically for playback.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time

page0 = None
label_title = None
label_state = None
label_duration = None
label_message = None
label_volume_name = None
label_volume = None
volume_slider = None
record_button = None
play_button = None

record_pending = None
play_pending = None
volume = None
volume_pending = None
stop_requested = None
record_buffer = None
state = None
queued_chunks = None
next_is_a = None
recorded_bytes = None
buffer_a = None
buffer_b = None
record_start = None
speaker_ready = None
play_started = None

def record_button_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    record_pending = True

def play_button_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    play_pending = True

def volume_slider_value_changed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    volume = volume_slider.get_value()
    label_volume.set_text(str((str(volume) + str("%"))))
    volume_pending = True

def record_button_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        record_button_clicked_event(event_struct)
    return

def play_button_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        play_button_clicked_event(event_struct)
    return

def volume_slider_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        volume_slider_value_changed_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x080808)
    label_title = m5ui.M5Label(
        "Audio",
        x=24,
        y=24,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_state = m5ui.M5Label(
        "IDLE",
        x=48,
        y=90,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_duration = m5ui.M5Label(
        "0.0 / 30 s",
        x=48,
        y=170,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_message = m5ui.M5Label(
        "Tap RECORD to start",
        x=48,
        y=227,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume_name = m5ui.M5Label(
        "Volume",
        x=24,
        y=280,
        text_c=0x9A9A9F,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_volume = m5ui.M5Label(
        "70%",
        x=384,
        y=280,
        text_c=0xF4F4F5,
        bg_c=0x080808,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    volume_slider = m5ui.M5Slider(
        x=40,
        y=335,
        w=400,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=70,
        bg_c=0x38383C,
        color=0x8EDA91,
        parent=page0,
    )
    record_button = m5ui.M5Button(
        text="RECORD",
        x=24,
        y=388,
        bg_c=0x7A2731,
        text_c=0xF4F4F5,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    play_button = m5ui.M5Button(
        text="PLAY",
        x=252,
        y=388,
        bg_c=0x303034,
        text_c=0xF4F4F5,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    record_button.add_event_cb(record_button_event_handler, lv.EVENT.ALL, None)
    play_button.add_event_cb(play_button_event_handler, lv.EVENT.ALL, None)
    volume_slider.add_event_cb(volume_slider_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Speaker.stop()
    Speaker.end()
    Mic.end()
    record_buffer = bytearray(0)
    buffer_a = bytearray(4000)
    buffer_b = bytearray(4000)
    Speaker.setPA(True)
    state = "IDLE"
    volume = 70
    record_pending = False
    play_pending = False
    volume_pending = False
    next_is_a = True
    queued_chunks = 0
    stop_requested = False
    record_start = 0
    recorded_bytes = 0
    speaker_ready = False
    play_started = False
    record_button.set_size(204, 64)
    play_button.set_size(204, 64)

def loop():
    global \
        page0, \
        label_title, \
        label_state, \
        label_duration, \
        label_message, \
        label_volume_name, \
        label_volume, \
        volume_slider, \
        record_button, \
        play_button, \
        record_pending, \
        play_pending, \
        volume, \
        volume_pending, \
        stop_requested, \
        record_buffer, \
        state, \
        queued_chunks, \
        next_is_a, \
        recorded_bytes, \
        buffer_a, \
        buffer_b, \
        record_start, \
        speaker_ready, \
        play_started
    M5.update()
    if record_pending:
        record_pending = False
        if state == "RECORDING":
            stop_requested = True
            state = "STOPPING"
            label_state.set_text(str(state))
            label_message.set_text(str("Finishing recording..."))
        else:
            if state != "STOPPING":
                Speaker.stop()
                Speaker.end()
                play_button.set_btn_text(str("PLAY"))
                Mic.end()
                Mic.setSampleRate(8000)
                Mic.begin()
                record_buffer = bytearray(0)
                recorded_bytes = 0
                queued_chunks = 0
                next_is_a = True
                stop_requested = False
                label_duration.set_text(str((str((recorded_bytes / 16000)) + str(" / 30 s"))))
                if Mic.isRunning():
                    Mic.record(buffer_a, 8000, False)
                    Mic.record(buffer_b, 8000, False)
                    if (Mic.isRecording()) == 2:
                        queued_chunks = 2
                        record_start = time.ticks_ms()
                        state = "RECORDING"
                        label_state.set_text(str(state))
                        label_message.set_text(str("Tap STOP REC to finish"))
                        record_button.set_btn_text(str("STOP REC"))
                    else:
                        Mic.end()
                        queued_chunks = 0
                        state = "IDLE"
                        label_state.set_text(str(state))
                        label_message.set_text(str("Recorder failed"))
                        record_button.set_btn_text(str("RECORD"))
                else:
                    state = "IDLE"
                    label_state.set_text(str(state))
                    label_message.set_text(str("Microphone failed"))
                    record_button.set_btn_text(str("RECORD"))
    if state == "RECORDING" or state == "STOPPING":
        if (Mic.isRecording()) < queued_chunks:
            if next_is_a:
                record_buffer.extend(buffer_a)
            else:
                record_buffer.extend(buffer_b)
            recorded_bytes = recorded_bytes + 4000
            queued_chunks = queued_chunks - 1
            record_start = time.ticks_ms()
            if not stop_requested and recorded_bytes + queued_chunks * 4000 < 480000:
                if next_is_a:
                    Mic.record(buffer_a, 8000, False)
                else:
                    Mic.record(buffer_b, 8000, False)
                queued_chunks = queued_chunks + 1
            next_is_a = not next_is_a
            label_duration.set_text(str((str((recorded_bytes / 16000)) + str(" / 30 s"))))
            if queued_chunks == 0:
                Mic.end()
                state = "READY"
                label_state.set_text(str(state))
                if recorded_bytes >= 480000:
                    label_message.set_text(str("30 s limit reached"))
                else:
                    label_message.set_text(str("Recording ready"))
                record_button.set_btn_text(str("RECORD"))
                play_button.set_btn_text(str("PLAY"))
        if (state == "RECORDING" or state == "STOPPING") and (
            time.ticks_diff((time.ticks_ms()), record_start)
        ) > 2000:
            Mic.end()
            if recorded_bytes > 0:
                state = "READY"
            else:
                state = "IDLE"
            label_state.set_text(str(state))
            queued_chunks = 0
            label_message.set_text(str("Recording timed out"))
            record_button.set_btn_text(str("RECORD"))
    if play_pending:
        play_pending = False
        if state == "PLAYING":
            Speaker.stop()
            Speaker.end()
            state = "READY"
            label_state.set_text(str(state))
            play_button.set_btn_text(str("PLAY"))
        else:
            if state == "READY":
                Mic.end()
                speaker_ready = Speaker.begin()
                if speaker_ready:
                    Speaker.setVolume(int((volume * 255 + 50) / 100))
                    Speaker.setPA(True)
                    play_started = Speaker.playRaw(record_buffer, 8000)
                    if play_started:
                        state = "PLAYING"
                        label_state.set_text(str(state))
                        label_message.set_text(str(""))
                        play_button.set_btn_text(str("STOP PLAY"))
                    else:
                        label_message.set_text(str("Playback failed"))
                else:
                    label_message.set_text(str("Speaker failed"))
    if state == "PLAYING" and (Speaker.isPlaying()) == 0:
        Speaker.stop()
        Speaker.end()
        state = "READY"
        label_state.set_text(str(state))
        play_button.set_btn_text(str("PLAY"))
    if volume_pending:
        volume_pending = False
        if state == "PLAYING":
            Speaker.setVolume(int((volume * 255 + 50) / 100))
    time.sleep_ms(10)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Infrared Transmission and Reception

Use the built-in infrared receiver on G13 and transmitter on G49. Tap the send button to transmit an NEC frame with address 0x08 and an incrementing data byte. The screen shows transmitted data, received address and data, and the receive count. Use an NEC-compatible infrared remote control to test reception.

```python
import time

import lvgl as lv
import M5
from M5 import *
import m5ui
from unit import IRUnit

BACKGROUND = 0x080808
PANEL = 0x222224
TEXT = 0xF4F4F5
MUTED = 0x9A9A9F
GOOD = 0x8EDA91

BUTTON_X = 24
BUTTON_Y = 388
BUTTON_W = 432
BUTTON_H = 64
TX_TONE_HZ = 1800
RX_TONE_HZ = 900
TONE_DURATION_MS = 55
TONE_GAP_MS = 25

ir = None
page = None
label_tx = None
label_rx = None
label_count = None
tx_data = 0
rx_count = 0
rx_pending = False
rx_data = 0
rx_addr = 0
tx_pending = False
speaker_ready = False
tone_queue = []
tone_ready_ms = 0

def make_label(parent, text, x, y, width, font, color=TEXT, align=lv.TEXT_ALIGN.LEFT):
    label = m5ui.M5Label(text, x, y, color, BACKGROUND, 0, font, parent)
    label.set_width(width)
    label.set_style_text_align(align, lv.PART.MAIN)
    label.remove_flag(lv.obj.FLAG.CLICKABLE)
    return label

def make_page(title):
    screen = m5ui.M5Page(bg_c=BACKGROUND)
    screen.set_style_pad_all(0, lv.PART.MAIN)
    screen.set_style_border_width(0, lv.PART.MAIN)
    screen.set_style_shadow_width(0, lv.PART.MAIN)
    screen.remove_flag(lv.obj.FLAG.SCROLLABLE)
    make_label(screen, title, 24, 24, 432, lv.font_montserrat_24)
    return screen

def make_panel(parent, x, y, width, height, color=PANEL):
    panel = lv.obj(parent)
    panel.remove_style_all()
    panel.set_pos(x, y)
    panel.set_size(width, height)
    panel.set_style_radius(24, lv.PART.MAIN)
    panel.set_style_pad_all(0, lv.PART.MAIN)
    panel.set_style_bg_color(lv.color_hex(color), lv.PART.MAIN)
    panel.set_style_bg_opa(255, lv.PART.MAIN)
    panel.remove_flag(lv.obj.FLAG.SCROLLABLE)
    panel.remove_flag(lv.obj.FLAG.CLICKABLE)
    return panel

def make_button(parent, text, x, y, width, height, color=0x303034):
    button = m5ui.M5Button(text, x, y, width, height, color, TEXT, lv.font_montserrat_18, parent)
    button.set_style_radius(18, lv.PART.MAIN)
    button.set_style_pad_all(0, lv.PART.MAIN)
    button.set_style_shadow_width(0, lv.PART.MAIN)
    button.set_style_shadow_width(0, lv.PART.MAIN | lv.STATE.PRESSED)
    button.label.set_width(width - 16)
    button.label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)
    button.label.center()
    return button

def ir_rx_event(data, addr, ctrl):
    global rx_count, rx_pending, rx_data, rx_addr

    rx_count += 1
    rx_data = data
    rx_addr = addr
    rx_pending = True

def queue_tone(frequency):
    if speaker_ready and len(tone_queue) < 4:
        tone_queue.append(frequency)

def update_tone():
    global tone_ready_ms

    if not speaker_ready or not tone_queue:
        return
    now = time.ticks_ms()
    if time.ticks_diff(now, tone_ready_ms) >= 0:
        Speaker.tone(tone_queue.pop(0), TONE_DURATION_MS)
        tone_ready_ms = time.ticks_add(now, TONE_DURATION_MS + TONE_GAP_MS)

def send_button_event(event_struct):
    global tx_pending

    if event_struct.code == lv.EVENT.CLICKED:
        tx_pending = True

def setup():
    global ir, page, label_tx, label_rx, label_count
    global speaker_ready, tone_ready_ms

    M5.begin()
    m5ui.init()
    page = make_page("Infrared")
    panel = make_panel(page, 24, 84, 432, 260)
    make_label(
        panel, "Addr / Data", 140, 20, 272, lv.font_montserrat_18, MUTED, lv.TEXT_ALIGN.RIGHT
    )
    values = []
    for index, name in enumerate(("TX", "RX", "Received")):
        y = 64 + index * 68
        make_label(panel, name, 20, y + 4, 112, lv.font_montserrat_18, MUTED)
        values.append(
            make_label(panel, "--", 140, y, 272, lv.font_montserrat_24, TEXT, lv.TEXT_ALIGN.RIGHT)
        )
    label_tx, label_rx, label_count = values
    label_tx.set_text("Ready")
    label_rx.set_text("Waiting")
    label_count.set_text("0")
    send_button = make_button(page, "SEND NEC", BUTTON_X, BUTTON_Y, BUTTON_W, BUTTON_H)
    send_button.add_event_cb(send_button_event, lv.EVENT.ALL, None)
    page.screen_load()
    # Use the same explicit board IR pins as the graphical IR Unit example.
    ir = IRUnit((13, 49))
    ir.rx_cb(ir_rx_event)
    speaker_ready = Speaker.begin()
    if speaker_ready:
        Speaker.setVolume(128)
    tone_ready_ms = time.ticks_ms()

def loop():
    global tx_data, rx_pending, tx_pending

    M5.update()
    if tx_pending:
        tx_pending = False
        tx_data = (tx_data + 1) & 0xFF
        ir.tx(0x08, tx_data)
        queue_tone(TX_TONE_HZ)
        label_tx.set_text("08 / %02X" % tx_data)
    if rx_pending:
        rx_pending = False
        label_rx.set_text("%02X / %02X" % (rx_addr, rx_data))
        label_count.set_text("%d" % rx_count)
        queue_tone(RX_TONE_HZ)
    update_tone()
    time.sleep_ms(10)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt):
        Speaker.stop()
        Speaker.end()
        m5ui.deinit()
        raise
```

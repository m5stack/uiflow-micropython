#########
###### StopWatch

<!-- .. include:: ../refs/controllers.stopwatch.ref -->

Support the following products:

    |StopWatch|

## UiFlow2 Example

#### RTC Clock

Open the |stopwatch_rtc_example.m5f2| project in UiFlow2.

This example displays a digital clock (HH:MM:SS) on the round screen, reading time from the built-in RTC. Press **BtnA** to cycle through hour, minute, and second adjustment modes (the active field is highlighted in red). Press **BtnB** to increment the selected field. After adjusting seconds, press **BtnA** again to write the new time to the RTC.

UiFlow2 Code Block:

Example output:

    None

#### Power Management

Open the |stopwatch_power_example.m5f2| project in UiFlow2.

This example monitors USB, battery, and Grove port voltages, and shows charging status (battery text turns green while charging). Press **BtnA** to toggle Grove external output (5V OUT). Press **BtnB** to toggle battery charging.

UiFlow2 Code Block:

Example output:

    None

#### Audio Recording and Playback

Open the |stopwatch_aduio_example.m5f2| project in UiFlow2.

This example demonstrates audio recording and playback. Press **BtnA** to start a 5-second recording (countdown shown on screen). Press **BtnB** to play back the recorded file when not recording. The UI shows **Idle**, **Recording...**, or **Playing...** status.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### RTC Clock

This example displays a digital clock (HH:MM:SS) on the round screen, reading time from the built-in RTC. Press **BtnA** to cycle through hour, minute, and second adjustment modes (the active field is highlighted in red). Press **BtnB** to increment the selected field. After adjusting seconds, press **BtnA** again to write the new time to the RTC.

MicroPython Code Block:

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import RTC
import time

page0 = None
label_tip = None
label_hour = None
label_min = None
label_second = None
label_dot1 = None
label_dot2 = None
rtc = None

sw = None
hour = None
minute = None
second = None
last_time = None

def btna_was_click_event(state):
    global \
        page0, \
        label_tip, \
        label_hour, \
        label_min, \
        label_second, \
        label_dot1, \
        label_dot2, \
        rtc, \
        sw, \
        hour, \
        minute, \
        second, \
        last_time
    Speaker.tone(1000, 200)
    sw = (sw if isinstance(sw, (int, float)) else 0) + 1
    if sw == 1:
        label_hour.set_text_color(0xFF0000, 255, 0)
    elif sw == 2:
        label_hour.set_text_color(0x00CCCC, 255, 0)
        label_min.set_text_color(0xFF0000, 255, 0)
    elif sw == 3:
        label_min.set_text_color(0x00CCCC, 255, 0)
        label_second.set_text_color(0xFF0000, 255, 0)
    else:
        label_second.set_text_color(0x00CCCC, 255, 0)
        sw = 0
        rtc.init((2026, 5, 21, hour, minute, second, 339, 0))

def btnb_was_click_event(state):
    global \
        page0, \
        label_tip, \
        label_hour, \
        label_min, \
        label_second, \
        label_dot1, \
        label_dot2, \
        rtc, \
        sw, \
        hour, \
        minute, \
        second, \
        last_time
    Speaker.tone(1000, 200)
    if sw == 1:
        hour = (hour if isinstance(hour, (int, float)) else 0) + 1
        if hour > 23:
            hour = 0
    elif sw == 2:
        minute = (minute if isinstance(minute, (int, float)) else 0) + 1
        if minute > 59:
            minute = 0
    elif sw == 3:
        second = (second if isinstance(second, (int, float)) else 0) + 1
        if second > 59:
            second = 0
    else:
        sw = 0

def setup():
    global \
        page0, \
        label_tip, \
        label_hour, \
        label_min, \
        label_second, \
        label_dot1, \
        label_dot2, \
        rtc, \
        sw, \
        hour, \
        minute, \
        second, \
        last_time

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_tip = m5ui.M5Label(
        "Clock",
        x=176,
        y=40,
        text_c=0x10AACD,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_hour = m5ui.M5Label(
        "00",
        x=100,
        y=208,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_min = m5ui.M5Label(
        "00",
        x=200,
        y=206,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_second = m5ui.M5Label(
        "00",
        x=300,
        y=205,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_dot1 = m5ui.M5Label(
        ":",
        x=177,
        y=202,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_dot2 = m5ui.M5Label(
        ":",
        x=275,
        y=202,
        text_c=0x03C4E3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_click_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_click_event)

    page0.screen_load()
    rtc = RTC()
    hour = 11
    minute = 10
    second = 0
    sw = 0
    label_dot1.align_to(page0, lv.ALIGN.TOP_MID, -45, 201)
    label_dot2.align_to(page0, lv.ALIGN.TOP_MID, 45, 201)
    Speaker.begin()
    Speaker.setVolumePercentage(0.9)
    Speaker.tone(1000, 300)

def loop():
    global \
        page0, \
        label_tip, \
        label_hour, \
        label_min, \
        label_second, \
        label_dot1, \
        label_dot2, \
        rtc, \
        sw, \
        hour, \
        minute, \
        second, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 500:
        last_time = time.ticks_ms()
        if sw == 0:
            hour = (rtc.local_datetime())[4]
            minute = (rtc.local_datetime())[5]
            second = (rtc.local_datetime())[6]
        if hour < 10:
            label_hour.set_text(str((str("0") + str(hour))))
        else:
            label_hour.set_text(str(hour))
        label_hour.align_to(page0, lv.ALIGN.TOP_MID, -90, 205)
        if minute < 10:
            label_min.set_text(str((str("0") + str(minute))))
        else:
            label_min.set_text(str(minute))
        label_min.align_to(page0, lv.ALIGN.TOP_MID, 0, 205)
        if second < 10:
            label_second.set_text(str((str("0") + str(second))))
        else:
            label_second.set_text(str(second))
        label_second.align_to(page0, lv.ALIGN.TOP_MID, 90, 205)

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

Example output:

    None

#### Power Management

This example monitors USB, battery, and Grove port voltages, and shows charging status (battery text turns green while charging). Press **BtnA** to toggle Grove external output (5V OUT). Press **BtnB** to toggle battery charging.

MicroPython Code Block:

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time

page0 = None
label_title = None
label_usb = None
label_bat = None
label_grove = None
label_tip1 = None
label_tip2 = None

grove_en = None
charge_en = None
last_time = None

def btna_was_click_event(state):
    global \
        page0, \
        label_title, \
        label_usb, \
        label_bat, \
        label_grove, \
        label_tip1, \
        label_tip2, \
        grove_en, \
        charge_en, \
        last_time
    Speaker.tone(1000, 200)
    grove_en = not grove_en
    if grove_en:
        Power.setExtOutput(True)
        label_grove.set_text_color(0xFF0000, 255, 0)
    else:
        Power.setExtOutput(False)
        label_grove.set_text_color(0xFFFFFF, 255, 0)

def btnb_was_click_event(state):
    global \
        page0, \
        label_title, \
        label_usb, \
        label_bat, \
        label_grove, \
        label_tip1, \
        label_tip2, \
        grove_en, \
        charge_en, \
        last_time
    Speaker.tone(1000, 200)
    charge_en = not charge_en
    if charge_en:
        Power.setBatteryCharge(True)
    else:
        Power.setBatteryCharge(False)

def setup():
    global \
        page0, \
        label_title, \
        label_usb, \
        label_bat, \
        label_grove, \
        label_tip1, \
        label_tip2, \
        grove_en, \
        charge_en, \
        last_time

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Power test",
        x=123,
        y=40,
        text_c=0x10AACD,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_usb = m5ui.M5Label(
        "USB: --mV",
        x=170,
        y=135,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_bat = m5ui.M5Label(
        "Battery: --mV",
        x=151,
        y=170,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_grove = m5ui.M5Label(
        "Grove: --mV",
        x=160,
        y=205,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_tip1 = m5ui.M5Label(
        "Botton A Control Grove",
        x=94,
        y=330,
        text_c=0xE9E20E,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_tip2 = m5ui.M5Label(
        "Botton B Control Charge",
        x=82,
        y=366,
        text_c=0xE9E20E,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_click_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_click_event)

    page0.screen_load()
    Power.setBatteryCharge(True)
    Power.setExtOutput(False)
    grove_en = False
    charge_en = False
    Speaker.begin()
    Speaker.setVolumePercentage(0.8)

def loop():
    global \
        page0, \
        label_title, \
        label_usb, \
        label_bat, \
        label_grove, \
        label_tip1, \
        label_tip2, \
        grove_en, \
        charge_en, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 500:
        last_time = time.ticks_ms()
        label_usb.set_text(str((str("USB: ") + str((str((Power.getVBUSVoltage())) + str("mV"))))))
        label_usb.align_to(page0, lv.ALIGN.TOP_MID, 0, 135)
        label_bat.set_text(
            str((str("Battery: ") + str((str((Power.getBatteryVoltage())) + str("mV")))))
        )
        label_bat.align_to(page0, lv.ALIGN.TOP_MID, 0, 170)
        label_grove.set_text(
            str((str("Grove: ") + str((str((Power.getExtVoltage(M5.Power.PORT.A))) + str("mV")))))
        )
        label_grove.align_to(page0, lv.ALIGN.TOP_MID, 0, 205)
        if Power.isCharging():
            label_bat.set_text_color(0x33FF33, 255, 0)
        else:
            label_bat.set_text_color(0xFFFFFF, 255, 0)

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

Example output:

    None

#### Audio Recording and Playback

This example demonstrates audio recording and playback. Press **BtnA** to start a 5-second recording (countdown shown on screen). Press **BtnB** to play back the recorded file when not recording. The UI shows **Idle**, **Recording...**, or **Playing...** status.

MicroPython Code Block:

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from audio import Recorder
import time
from audio import Player

page0 = None
label_title = None
label_count = None
label_state = None
label_tip1 = None
label_tip2 = None
recorder = None
player = None

flag_record = None
flag_play = None
record_start_time = None
remaining = None
RECORD_TIME = None
record_file_path = None

def btna_was_click_event(state):
    global \
        page0, \
        label_title, \
        label_count, \
        label_state, \
        label_tip1, \
        label_tip2, \
        recorder, \
        player, \
        flag_record, \
        flag_play, \
        record_start_time, \
        remaining, \
        RECORD_TIME, \
        record_file_path
    flag_record = True

def btnb_was_click_event(state):
    global \
        page0, \
        label_title, \
        label_count, \
        label_state, \
        label_tip1, \
        label_tip2, \
        recorder, \
        player, \
        flag_record, \
        flag_play, \
        record_start_time, \
        remaining, \
        RECORD_TIME, \
        record_file_path
    if not (recorder.is_recording()):
        flag_play = True

def setup():
    global \
        page0, \
        label_title, \
        label_count, \
        label_state, \
        label_tip1, \
        label_tip2, \
        recorder, \
        player, \
        flag_record, \
        flag_play, \
        record_start_time, \
        remaining, \
        RECORD_TIME, \
        record_file_path

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Audio Test",
        x=128,
        y=40,
        text_c=0x10AACD,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_count = m5ui.M5Label(
        "5",
        x=218,
        y=205,
        text_c=0x10AACD,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_state = m5ui.M5Label(
        "Idle",
        x=194,
        y=116,
        text_c=0x10CD53,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_tip1 = m5ui.M5Label(
        "Button B Play",
        x=148,
        y=366,
        text_c=0xE9E20E,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_tip2 = m5ui.M5Label(
        "Button A Record",
        x=131,
        y=330,
        text_c=0xE9E20E,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_click_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_click_event)

    page0.screen_load()
    Mic.end()
    Speaker.end()
    recorder = Recorder(8000, 16, True)
    player = Player(None)
    player.set_vol(80)
    RECORD_TIME = 5
    record_file_path = "rec1.amr"
    flag_record = False
    flag_play = False

def loop():
    global \
        page0, \
        label_title, \
        label_count, \
        label_state, \
        label_tip1, \
        label_tip2, \
        recorder, \
        player, \
        flag_record, \
        flag_play, \
        record_start_time, \
        remaining, \
        RECORD_TIME, \
        record_file_path
    M5.update()
    if flag_record:
        if not (recorder.is_recording()):
            record_start_time = time.ticks_ms()
            label_state.set_text(str("Recording..."))
            label_state.set_text_color(0xFF0000, 255, 0)
            label_state.align_to(page0, lv.ALIGN.TOP_MID, 0, 116)
            Speaker.setPA(False)
            recorder.record("file://flash/res/audio/" + str(record_file_path), RECORD_TIME, False)
        else:
            remaining = (
                RECORD_TIME - (time.ticks_diff((time.ticks_ms()), record_start_time)) / 1000
            )
            if remaining > 0:
                label_count.set_text(str(int(remaining)))
            else:
                label_count.set_text(str("0"))
                flag_record = False
                label_state.set_text(str("Idle"))
                label_state.align_to(page0, lv.ALIGN.TOP_MID, 0, 116)
                label_state.set_text_color(0x33CC00, 255, 0)
    if not (recorder.is_recording()):
        if flag_play:
            flag_play = False
            label_count.set_text(str(""))
            label_state.set_text(str("Playing..."))
            label_state.align_to(page0, lv.ALIGN.TOP_MID, 0, 116)
            label_state.set_text_color(0xFF0000, 255, 0)
            Speaker.setPA(True)
            player.play(
                "file://flash/res/audio/" + str(record_file_path), pos=0, volume=-1, sync=False
            )
        else:
            if not (player.pos()):
                label_state.align_to(page0, lv.ALIGN.TOP_MID, 0, 116)
                label_count.set_text(str(RECORD_TIME))
                label_state.set_text(str("Idle"))
                label_state.set_text_color(0x33CC00, 255, 0)

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

Example output:

    None

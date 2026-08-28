# Tab5X

Support the following products:

    Tab5X

## Supported Components

Tab5X inherits the Tab5 manifest and includes these user-facing packages:

- `M5UI`: The `m5ui` LVGL component library, including `m5ui.M5Keyboard`.
- `Module`: The `module` package for M-BUS expansion modules.
- `Unit`: The `unit` package for Unit drivers.
- `USB`: The `usb.device` package, including HID, mouse, and keyboard support.
- `Chain`: The `chain` package for Chain devices.
- `Tab5`: The `tab5` package for Tab5 and Tab5X keyboard support.

## Supported Display Fonts

The Tab5X firmware includes the following Montserrat fonts for LVGL and M5UI:
`lv.font_montserrat_12`, `lv.font_montserrat_14`, `lv.font_montserrat_16`,
`lv.font_montserrat_18`, `lv.font_montserrat_20`, `lv.font_montserrat_22`,
`lv.font_montserrat_24`, `lv.font_montserrat_30`, `lv.font_montserrat_36`,
`lv.font_montserrat_40`, `lv.font_montserrat_44`, and
`lv.font_montserrat_48`.

For `M5.Lcd.FONTS`, the firmware also provides `AlibabaPuHuiTiCN24`,
`AlibabaSansJA24`, and `AlibabaSansKR24` for Chinese, Japanese, and Korean
text respectively.

## MicroPython Example

#### Power Management

This example controls PORT.A, USB Type-A, and battery charging while displaying
battery level, voltage, current, and charging state.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
label_title = None
button_port_a = None
button_port_usb = None
button_charge = None
label_battery = None
label_current = None
label_charging = None

port_a = None
port_usb = None
charge_enabled = None
battery_level = None
battery_voltage = None
battery_current = None

def button_port_a_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    if port_a:
        port_a = False
        Power.setExtOutput(False, M5.Power.PORT.A)
        button_port_a.set_btn_text(str("PORT.A OFF"))
        button_port_a.set_bg_color(0x5F6B75, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        port_a = True
        Power.setExtOutput(True, M5.Power.PORT.A)
        button_port_a.set_btn_text(str("PORT.A ON"))
        button_port_a.set_bg_color(0x2EAD65, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

def button_port_usb_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    if port_usb:
        port_usb = False
        Power.setExtOutput(False, M5.Power.PORT.USB)
        button_port_usb.set_btn_text(str("USB Type-A OFF"))
        button_port_usb.set_bg_color(0x5F6B75, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        port_usb = True
        Power.setExtOutput(True, M5.Power.PORT.USB)
        button_port_usb.set_btn_text(str("USB Type-A ON"))
        button_port_usb.set_bg_color(0x2EAD65, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

def button_charge_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    if charge_enabled:
        charge_enabled = False
        Power.setBatteryCharge(False)
        button_charge.set_btn_text(str("CHARGE OFF"))
        button_charge.set_bg_color(0x5F6B75, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        charge_enabled = True
        Power.setBatteryCharge(True)
        button_charge.set_btn_text(str("CHARGE ON"))
        button_charge.set_bg_color(0x2EAD65, 255, lv.PART.MAIN | lv.STATE.DEFAULT)

def button_port_a_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_port_a_pressed_event(event_struct)
    return

def button_port_usb_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_port_usb_pressed_event(event_struct)
    return

def button_charge_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_charge_pressed_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x101820)
    label_title = m5ui.M5Label(
        "Power Example",
        x=465,
        y=35,
        text_c=0x1976D2,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_port_a = m5ui.M5Button(
        text="PORT.A OFF",
        x=70,
        y=160,
        bg_c=0x5F6B75,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    button_port_usb = m5ui.M5Button(
        text="USB Type-A OFF",
        x=70,
        y=310,
        bg_c=0x5F6B75,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    button_charge = m5ui.M5Button(
        text="CHARGE ON",
        x=70,
        y=460,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_40,
        parent=page0,
    )
    label_battery = m5ui.M5Label(
        "Battery: --%   -.--- V",
        x=600,
        y=210,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_current = m5ui.M5Label(
        "Current: -- mA",
        x=600,
        y=330,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_charging = m5ui.M5Label(
        "Charging: --",
        x=600,
        y=450,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    button_port_a.add_event_cb(button_port_a_event_handler, lv.EVENT.ALL, None)
    button_port_usb.add_event_cb(button_port_usb_event_handler, lv.EVENT.ALL, None)
    button_charge.add_event_cb(button_charge_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Power.setBatteryCharge(True)
    port_a = False
    port_usb = False
    charge_enabled = True
    battery_level = Power.getBatteryLevel()
    battery_voltage = Power.getBatteryVoltage()
    battery_current = Power.getBatteryCurrent()
    label_current.set_text(str((str("Current: ") + str((str(battery_current) + str(" mA"))))))
    label_battery.set_text(
        str(
            (
                str("Battery: ")
                + str(
                    (
                        str(battery_level)
                        + str((str("%   ") + str((str((battery_voltage / 1000)) + str(" V")))))
                    )
                )
            )
        )
    )
    if battery_current > 10:
        label_charging.set_text(str("Charging: YES"))
        label_battery.set_text_color(0x2EAD65, 255, 0)
        label_charging.set_text_color(0x2EAD65, 255, 0)
    else:
        label_charging.set_text(str("Charging: NO"))
        label_battery.set_text_color(0xF4F7FA, 255, 0)
        label_charging.set_text_color(0x9FB3C8, 255, 0)

def loop():
    global \
        page0, \
        label_title, \
        button_port_a, \
        button_port_usb, \
        button_charge, \
        label_battery, \
        label_current, \
        label_charging, \
        port_a, \
        port_usb, \
        charge_enabled, \
        battery_level, \
        battery_voltage, \
        battery_current
    M5.update()
    battery_level = Power.getBatteryLevel()
    battery_voltage = Power.getBatteryVoltage()
    battery_current = Power.getBatteryCurrent()
    label_current.set_text(str((str("Current: ") + str((str(battery_current) + str(" mA"))))))
    label_battery.set_text(
        str(
            (
                str("Battery: ")
                + str(
                    (
                        str(battery_level)
                        + str((str("%   ") + str((str((battery_voltage / 1000)) + str(" V")))))
                    )
                )
            )
        )
    )
    if battery_current > 10:
        label_charging.set_text(str("Charging: YES"))
        label_battery.set_text_color(0x2EAD65, 255, 0)
        label_charging.set_text_color(0x2EAD65, 255, 0)
    else:
        label_charging.set_text(str("Charging: NO"))
        label_battery.set_text_color(0xF4F7FA, 255, 0)
        label_charging.set_text_color(0x9FB3C8, 255, 0)

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

This example records up to 10 seconds of PCM audio and plays the recorded buffer.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from audio import Recorder
from audio import Player
import time

page0 = None
label_title = None
button_record = None
button_play = None
label_status = None
label_format = None
recorder = None
player = None

recordDuration = None
playing = None
recordStart = None
recording = None
hasRecording = None
playStart = None
audioBuffer = None
recordTime = None

def button_record_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    if recorder.is_recording():
        recordDuration = time.ticks_diff((time.ticks_ms()), recordStart)
        recorder.stop()
        recording = False
        hasRecording = True
        button_record.set_btn_text(str("START RECORD"))
        label_status.set_text(str("Recording stopped"))
    else:
        if playing:
            player.stop()
            playing = False
            button_play.set_btn_text(str("START PLAY"))
        Speaker.setPA(False)
        hasRecording = False
        recordStart = time.ticks_ms()
        button_record.set_btn_text(str("STOP RECORD"))
        label_status.set_text(str("Recording... maximum 10 seconds"))
        audioBuffer = recorder.create_pcm_buf(recordTime)
        recorder.record_into(audioBuffer, False)
        recording = True

def button_play_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    if playing:
        player.stop()
        playing = False
        button_play.set_btn_text(str("START PLAY"))
        label_status.set_text(str("Playback stopped"))
    else:
        if recorder.is_recording():
            label_status.set_text(str("Wait for recording to stop"))
        else:
            if hasRecording:
                Speaker.setPA(True)
                time.sleep_ms(100)
                button_play.set_btn_text(str("STOP PLAY"))
                label_status.set_text(str("Playing..."))
                player.play_raw(
                    audioBuffer, sample=16000, stereo=False, bits=16, pos=0, volume=80, sync=False
                )
                playStart = time.ticks_ms()
                playing = True
            else:
                label_status.set_text(str("Record audio first"))

def button_record_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_record_pressed_event(event_struct)
    return

def button_play_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_play_pressed_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x101820)
    label_title = m5ui.M5Label(
        "Audio Example",
        x=480,
        y=35,
        text_c=0xE99628,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_record = m5ui.M5Button(
        text="START RECORD",
        x=70,
        y=175,
        bg_c=0xD84545,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_play = m5ui.M5Button(
        text="START PLAY",
        x=710,
        y=175,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_status = m5ui.M5Label(
        "Ready. Maximum recording length: 10s",
        x=70,
        y=420,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_format = m5ui.M5Label(
        "16 kHz / 16-bit / mono PCM",
        x=70,
        y=535,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    button_record.add_event_cb(button_record_event_handler, lv.EVENT.ALL, None)
    button_play.add_event_cb(button_play_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    button_record.set_size(500, 140)
    button_play.set_size(500, 140)
    Mic.end()
    recorder = Recorder(16000, 16, False)
    player = Player(None)
    player.stop()
    player.set_vol(100)
    recordTime = 10
    audioBuffer = recorder.create_pcm_buf(recordTime)
    recording = False
    playing = False
    hasRecording = False
    recordStart = 0
    recordDuration = 10000
    playStart = 0

def loop():
    global \
        page0, \
        label_title, \
        button_record, \
        button_play, \
        label_status, \
        label_format, \
        recorder, \
        player, \
        recordDuration, \
        playing, \
        recordStart, \
        recording, \
        hasRecording, \
        playStart, \
        audioBuffer, \
        recordTime
    M5.update()
    if recording and not (recorder.is_recording()):
        recordDuration = time.ticks_diff((time.ticks_ms()), recordStart)
        recording = False
        hasRecording = True
        button_record.set_btn_text(str("START RECORD"))
        label_status.set_text(str("Recording complete"))
    if playing and (time.ticks_diff((time.ticks_ms()), playStart)) >= recordDuration:
        player.stop()
        Speaker.setPA(False)
        playing = False
        button_play.set_btn_text(str("START PLAY"))
        label_status.set_text(str("Playback complete"))

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

This example reads and displays the three accelerometer and three gyroscope axes.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
label_title = None
label_acc_title = None
label_acc_x = None
label_acc_y = None
label_acc_z = None
label_gyro_title = None
label_gyro_x = None
label_gyro_y = None
label_gyro_z = None
label_footer = None

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
        label_acc_title, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_title, \
        label_gyro_x, \
        label_gyro_y, \
        label_gyro_z, \
        label_footer, \
        accel, \
        gyro, \
        acc_x, \
        acc_y, \
        acc_z, \
        gyro_x, \
        gyro_y, \
        gyro_z

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x101820)
    label_title = m5ui.M5Label(
        "IMU Example",
        x=465,
        y=30,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_acc_title = m5ui.M5Label(
        "Accelerometer",
        x=140,
        y=125,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_acc_x = m5ui.M5Label(
        "X: -- g",
        x=120,
        y=220,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_acc_y = m5ui.M5Label(
        "Y: -- g",
        x=120,
        y=350,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_acc_z = m5ui.M5Label(
        "Z: -- g",
        x=120,
        y=480,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_gyro_title = m5ui.M5Label(
        "Gyroscope",
        x=825,
        y=125,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_gyro_x = m5ui.M5Label(
        "X: -- dps",
        x=760,
        y=220,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_gyro_y = m5ui.M5Label(
        "Y: -- dps",
        x=760,
        y=350,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_gyro_z = m5ui.M5Label(
        "Z: -- dps",
        x=760,
        y=480,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_footer = m5ui.M5Label(
        "Live data",
        x=535,
        y=610,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    page0.screen_load()

def loop():
    global \
        page0, \
        label_title, \
        label_acc_title, \
        label_acc_x, \
        label_acc_y, \
        label_acc_z, \
        label_gyro_title, \
        label_gyro_x, \
        label_gyro_y, \
        label_gyro_z, \
        label_footer, \
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

#### RTC

This example displays and updates the hardware RTC date and time.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import RTC

page0 = None
label_title = None
label_date = None
label_hour = None
label_colon_1 = None
label_minute = None
label_colon_2 = None
label_second = None
button_hour_minus = None
button_hour_plus = None
button_minute_minus = None
button_minute_plus = None
button_second_minus = None
button_second_plus = None
label_hour_control = None
label_minute_control = None
label_second_control = None
rtc = None

editing = None
hour = None
minute = None
second = None
now = None
year = None
month = None
day = None

def button_hour_minus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    hour = hour - 1
    if hour < 0:
        hour = 23
    label_hour.set_text(str(hour))

def button_hour_plus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    hour = hour + 1
    if hour > 23:
        hour = 0
    label_hour.set_text(str(hour))

def button_minute_minus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    minute = minute - 1
    if minute < 0:
        minute = 59
    label_minute.set_text(str(minute))

def button_minute_plus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    minute = minute + 1
    if minute > 59:
        minute = 0
    label_minute.set_text(str(minute))

def button_second_minus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    second = second - 1
    if second < 0:
        second = 59
    label_second.set_text(str(second))

def button_second_plus_pressed_event(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    editing = True
    second = second + 1
    if second > 59:
        second = 0
    label_second.set_text(str(second))

def button_hour_minus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_hour_minus_pressed_event(event_struct)
    return

def button_hour_plus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_hour_plus_pressed_event(event_struct)
    return

def button_minute_minus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_minute_minus_pressed_event(event_struct)
    return

def button_minute_plus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_minute_plus_pressed_event(event_struct)
    return

def button_second_minus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_second_minus_pressed_event(event_struct)
    return

def button_second_plus_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        button_second_plus_pressed_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x101820)
    label_title = m5ui.M5Label(
        "RTC Example",
        x=480,
        y=35,
        text_c=0xE99628,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_date = m5ui.M5Label(
        "2026-01-01",
        x=510,
        y=125,
        text_c=0xF4F7FA,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_hour = m5ui.M5Label(
        "00",
        x=440,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_colon_1 = m5ui.M5Label(
        ":",
        x=565,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_minute = m5ui.M5Label(
        "00",
        x=635,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_colon_2 = m5ui.M5Label(
        ":",
        x=760,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_second = m5ui.M5Label(
        "00",
        x=830,
        y=220,
        text_c=0x2EAD65,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_hour_minus = m5ui.M5Button(
        text="-",
        x=100,
        y=390,
        bg_c=0xD84545,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_hour_plus = m5ui.M5Button(
        text="+",
        x=290,
        y=390,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_minute_minus = m5ui.M5Button(
        text="-",
        x=480,
        y=390,
        bg_c=0xD84545,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_minute_plus = m5ui.M5Button(
        text="+",
        x=670,
        y=390,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_second_minus = m5ui.M5Button(
        text="-",
        x=860,
        y=390,
        bg_c=0xD84545,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    button_second_plus = m5ui.M5Button(
        text="+",
        x=1050,
        y=390,
        bg_c=0x2EAD65,
        text_c=0xF4F7FA,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_hour_control = m5ui.M5Label(
        "HOUR",
        x=195,
        y=320,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_minute_control = m5ui.M5Label(
        "MIN",
        x=618,
        y=320,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )
    label_second_control = m5ui.M5Label(
        "SEC",
        x=998,
        y=320,
        text_c=0x9FB3C8,
        bg_c=0x101820,
        bg_opa=0,
        font=lv.font_montserrat_48,
        parent=page0,
    )

    button_hour_minus.add_event_cb(button_hour_minus_event_handler, lv.EVENT.ALL, None)
    button_hour_plus.add_event_cb(button_hour_plus_event_handler, lv.EVENT.ALL, None)
    button_minute_minus.add_event_cb(button_minute_minus_event_handler, lv.EVENT.ALL, None)
    button_minute_plus.add_event_cb(button_minute_plus_event_handler, lv.EVENT.ALL, None)
    button_second_minus.add_event_cb(button_second_minus_event_handler, lv.EVENT.ALL, None)
    button_second_plus.add_event_cb(button_second_plus_event_handler, lv.EVENT.ALL, None)

    rtc = RTC()
    page0.screen_load()
    now = rtc.datetime()
    year = now[0]
    month = now[1]
    day = now[2]
    hour = now[4]
    minute = now[5]
    second = now[6]
    editing = False
    label_date.set_text(
        str((str((str(year) + str("-"))) + str((str((str(month) + str("-"))) + str(day)))))
    )
    label_hour.set_text(str(hour))
    label_minute.set_text(str(minute))
    label_second.set_text(str(second))
    button_hour_minus.set_pos(100, 390)
    button_hour_minus.set_size(170, 90)
    button_hour_plus.set_pos(290, 390)
    button_hour_plus.set_size(170, 90)
    button_minute_minus.set_pos(480, 390)
    button_minute_minus.set_size(170, 90)
    button_minute_plus.set_pos(670, 390)
    button_minute_plus.set_size(170, 90)
    button_second_minus.set_pos(860, 390)
    button_second_minus.set_size(170, 90)
    button_second_plus.set_pos(1050, 390)
    button_second_plus.set_size(170, 90)

def loop():
    global \
        page0, \
        label_title, \
        label_date, \
        label_hour, \
        label_colon_1, \
        label_minute, \
        label_colon_2, \
        label_second, \
        button_hour_minus, \
        button_hour_plus, \
        button_minute_minus, \
        button_minute_plus, \
        button_second_minus, \
        button_second_plus, \
        label_hour_control, \
        label_minute_control, \
        label_second_control, \
        rtc, \
        editing, \
        hour, \
        minute, \
        second, \
        now, \
        year, \
        month, \
        day
    M5.update()
    now = rtc.datetime()
    if not editing:
        year = now[0]
        month = now[1]
        day = now[2]
        hour = now[4]
        minute = now[5]
        second = now[6]
        label_date.set_text(
            str((str((str(year) + str("-"))) + str((str((str(month) + str("-"))) + str(day)))))
        )
        label_hour.set_text(str(hour))
        label_minute.set_text(str(minute))
        label_second.set_text(str(second))
    else:
        rtc.init((year, month, day, hour, minute, second, 0, 0))
        editing = False

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

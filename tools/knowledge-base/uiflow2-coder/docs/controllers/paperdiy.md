# PaperDIY

PaperDIY is an ESP32-S3 controller with a 4.7-inch, 960x540 monochrome e-paper display, 16MB Flash, and 8MB PSRAM.

Support the following products:

    PaperDIY

## Supported Components

PaperDIY supports the following components:

- [Display](../hardware/display.md): Screen drawing through `M5.Lcd`.
- `Widgets`: Labels and basic UI components through `M5.Widgets` and the `widgets` package.
- `Unit`: The `unit` package containing Unit drivers.
- `Chain`: The `chain` package for Chain devices.
- `usb.device`: USB HID keyboard and mouse support.

The PaperDIY firmware uses M5GFX for display rendering. LVGL and M5UI are not enabled in this firmware.

## Supported Display Fonts

The PaperDIY firmware provides the following Montserrat fonts through `M5.Lcd.FONTS` and `M5.Widgets.FONTS`: `Montserrat12`, `Montserrat14`, `Montserrat16`, `Montserrat18`, `Montserrat24`, `Montserrat40`, `Montserrat44`, and `Montserrat48`.

The firmware also provides `AlibabaPuHuiTiCN24`, `AlibabaSansJA24`, and `AlibabaSansKR24` for Chinese, Japanese, and Korean text respectively.

## Board Features

PaperDIY supports the following built-in functions and peripherals:

- A 4.7-inch monochrome e-paper display with portrait and landscape orientations.
- [Button](../hardware/button.md) input through `BtnA` and `BtnB`.
- [Power](../system/power.md) monitoring through M5PM1: USB and battery voltages, charging status, and battery-charging control.
- TF (microSD) card storage.
- Wi-Fi networking and native USB programming.

The e-paper display has no touch panel or backlight.

## MicroPython Example

#### Button Counter

This example displays two independent button counters in portrait orientation. Press **BtnA** or **BtnB** to increment its own counter. Both counters start at 0 when the example starts.

```python
import os
import sys
import io
import time

import M5
from M5 import *

label_title = None
label_btn_a = None
label_btn_b = None
label_hint = None

button_a_count = None
button_b_count = None

def btna_was_pressed_event(state):
    global button_a_count

    button_a_count = button_a_count + 1
    label_btn_a.setText(str("Button A: " + str(button_a_count)))

def btnb_was_pressed_event(state):
    global button_b_count

    button_b_count = button_b_count + 1
    label_btn_b.setText(str("Button B: " + str(button_b_count)))

def setup():
    global label_title, label_btn_a, label_btn_b, label_hint
    global button_a_count, button_b_count

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0xFFFFFF)
    label_title = Widgets.Label(
        "PaperDIY Button Counter",
        30,
        40,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat24,
    )
    label_btn_a = Widgets.Label(
        "Button A: 0",
        30,
        240,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat40,
    )
    label_btn_b = Widgets.Label(
        "Button B: 0",
        30,
        400,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat40,
    )
    label_hint = Widgets.Label(
        "Press Button A or Button B",
        30,
        600,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat24,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_PRESSED, cb=btna_was_pressed_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_PRESSED, cb=btnb_was_pressed_event)

    M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FASTEST)
    button_a_count = 0
    button_b_count = 0

def loop():
    M5.update()
    time.sleep_ms(10)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as error:
        try:
            from utility import print_error_msg

            print_error_msg(error)
        except ImportError:
            print(error)
```

#### Charge Detection

This example displays battery voltage and USB voltage in millivolts (mV), together with charging status. Battery charging starts enabled. Press **BtnA** to enable or disable it. The readings refresh every 15 seconds and immediately after a button press.

```python
import os, sys, io
import M5
from M5 import *
import time

label_title = None
label_vbat = None
label_vbus = None
label_enable = None
label_state = None
label_hint = None

charge_enabled = None
vbat = None
vbus = None
next_refresh = None

def btna_was_pressed_event(state):
    global \
        label_title, \
        label_vbat, \
        label_vbus, \
        label_enable, \
        label_state, \
        label_hint, \
        charge_enabled, \
        vbat, \
        vbus, \
        next_refresh
    charge_enabled = not charge_enabled
    if charge_enabled:
        Power.setBatteryCharge(True)
        label_enable.setText(str("Charge enable: ON"))
    else:
        Power.setBatteryCharge(False)
        label_enable.setText(str("Charge enable: OFF"))
    vbat = Power.getBatteryVoltage()
    vbus = Power.getVBUSVoltage()
    label_vbat.setText(str((str((str("VBAT: ") + str(vbat))) + str(" mV"))))
    label_vbus.setText(str((str((str("VBUS: ") + str(vbus))) + str(" mV"))))
    if Power.isCharging():
        label_state.setText(str("Charge state: charging"))
    else:
        label_state.setText(str("Charge state: not charging"))

def setup():
    global \
        label_title, \
        label_vbat, \
        label_vbus, \
        label_enable, \
        label_state, \
        label_hint, \
        charge_enabled, \
        vbat, \
        vbus, \
        next_refresh

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0xFFFFFF)
    label_title = Widgets.Label(
        "PaperDIY charge detection", 30, 30, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.Montserrat24
    )
    label_vbat = Widgets.Label(
        "VBAT: -- mV", 30, 240, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.Montserrat24
    )
    label_vbus = Widgets.Label(
        "VBUS: -- mV", 30, 310, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.Montserrat24
    )
    label_enable = Widgets.Label(
        "Charge enable: ON", 30, 390, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.Montserrat24
    )
    label_state = Widgets.Label(
        "Charge state: --", 30, 470, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.Montserrat24
    )
    label_hint = Widgets.Label(
        "Button A toggles battery charge",
        30,
        600,
        1.0,
        0x000000,
        0xFFFFFF,
        Widgets.FONTS.Montserrat24,
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_PRESSED, cb=btna_was_pressed_event)

    M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FASTEST)
    charge_enabled = True
    Power.setBatteryCharge(True)
    vbat = Power.getBatteryVoltage()
    vbus = Power.getVBUSVoltage()
    label_vbat.setText(str((str((str("VBAT: ") + str(vbat))) + str(" mV"))))
    label_vbus.setText(str((str((str("VBUS: ") + str(vbus))) + str(" mV"))))
    if Power.isCharging():
        label_state.setText(str("Charge state: charging"))
    else:
        label_state.setText(str("Charge state: not charging"))
    next_refresh = time.ticks_add((time.ticks_ms()), 15000)

def loop():
    global \
        label_title, \
        label_vbat, \
        label_vbus, \
        label_enable, \
        label_state, \
        label_hint, \
        charge_enabled, \
        vbat, \
        vbus, \
        next_refresh
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), next_refresh)) >= 0:
        vbat = Power.getBatteryVoltage()
        vbus = Power.getVBUSVoltage()
        label_vbat.setText(str((str((str("VBAT: ") + str(vbat))) + str(" mV"))))
        label_vbus.setText(str((str((str("VBUS: ") + str(vbus))) + str(" mV"))))
        if Power.isCharging():
            label_state.setText(str("Charge state: charging"))
        else:
            label_state.setText(str("Charge state: not charging"))
        next_refresh = time.ticks_add((time.ticks_ms()), 15000)
    time.sleep_ms(10)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

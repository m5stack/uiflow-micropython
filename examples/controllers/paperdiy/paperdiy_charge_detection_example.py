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

# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import BtnA, BtnB, BtnC, Widgets
from hardware import I2C, Pin
from stamp import StampTimerPower2

stp2 = None
label_hold = None
label_on = None
label_status = None
ldo_hold = False
on_delay_s = 5
phase = 0
phase_start = 0
last_refresh = 0


def btna_was_clicked_event(state):
    global ldo_hold
    if phase == 0:
        ldo_hold = not ldo_hold
        label_hold.setText("On" if ldo_hold else "Off")


def btnb_was_clicked_event(state):
    global on_delay_s
    if phase == 0:
        on_delay_s = on_delay_s % 15 + 5
        label_on.setText(str(on_delay_s) + " s")


def btnc_was_clicked_event(state):
    global phase, phase_start
    if phase != 0:
        return
    if ldo_hold:
        stp2.enable_ldo_power_hold()
    else:
        stp2.disable_ldo_power_hold()
    stp2.clear_wake_source(StampTimerPower2.WAKE_SOURCE_TIMER)
    # Arm the power-on timer before shutting down STP2.
    stp2.set_timer(on_delay_s, StampTimerPower2.TIMER_ACTION_POWER_ON)
    stp2.power_off()
    phase_start = time.ticks_ms()
    phase = 1
    label_status.setText("Power on in " + str(on_delay_s) + " s")
    print("Shutdown requested; LDO hold:", ldo_hold, "; power on after", on_delay_s, "s")


def setup():
    global stp2, label_hold, label_on, label_status, last_refresh
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    Widgets.Label("Power-on Timer", 80, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18)
    Widgets.Label(
        "Keep LDO output during shutdown",
        12,
        38,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    Widgets.Label("LDO keep on", 12, 80, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14)
    label_hold = Widgets.Label("Off", 190, 76, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    Widgets.Label("Power on after", 12, 125, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14)
    label_on = Widgets.Label("5 s", 190, 121, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_status = Widgets.Label(
        "Ready", 12, 164, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("LDO keep", 30, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("On +5 s", 125, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("Shutdown", 217, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14)
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c)
    stp2.wake()
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)
    last_refresh = time.ticks_ms()


def loop():
    global phase, phase_start, last_refresh
    M5.update()
    now = time.ticks_ms()
    if time.ticks_diff(now, last_refresh) < 100:
        return
    last_refresh = now
    if phase == 1:
        # Keep I2C idle while STP2 is off; BASIC stays independently powered.
        elapsed = time.ticks_diff(now, phase_start)
        remaining = max(0, on_delay_s * 1000 - elapsed)
        label_status.setText("Power on in " + str((remaining + 999) // 1000) + " s")
        if elapsed >= on_delay_s * 1000 + 500:
            stp2.wake()
            source = stp2.get_wake_source()
            if source & StampTimerPower2.WAKE_SOURCE_TIMER:
                label_status.setText("Timer wake confirmed")
            else:
                label_status.setText("Timer wake not detected")
            print("Wake source:", source)
            phase = 0


if __name__ == "__main__":
    setup()
    while True:
        loop()

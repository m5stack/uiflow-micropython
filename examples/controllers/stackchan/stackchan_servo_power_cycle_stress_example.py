# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import *
from hardware.stackchan import StackChan


CYCLES = 30
POWER_OFF_MS = 500
POWER_ON_SETTLE_MS = 500

stackchan = None
lines = []
fail_count = 0


def log(msg):
    print(msg)
    lines.append(msg)
    if len(lines) > 10:
        lines.pop(0)
    M5.Lcd.fillRect(0, 28, 320, 212, 0x000000)
    y = 30
    for line in lines:
        M5.Lcd.setCursor(0, y)
        M5.Lcd.printf(line[:44] + "\n")
        y += 20


def ping_pair():
    px = stackchan.servo.ping(stackchan.SERVO_ID_X)
    py = stackchan.servo.ping(stackchan.SERVO_ID_Y)
    return px, py


def run_power_cycle_stress():
    global fail_count
    for cycle in range(CYCLES):
        stackchan.set_servo_power(enable=False)
        time.sleep_ms(POWER_OFF_MS)
        stackchan.set_servo_power(enable=True, settle_ms=POWER_ON_SETTLE_MS)
        px, py = ping_pair()
        ok = px == stackchan.SERVO_ID_X and py == stackchan.SERVO_ID_Y
        if ok:
            stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=True)
            stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=True)
            stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 400, 20)
            stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 0, 400, 20)
            time.sleep_ms(500)
            ax = stackchan.get_servo_angle(stackchan.SERVO_ID_X)
            ay = stackchan.get_servo_angle(stackchan.SERVO_ID_Y)
            ok = ax is not None and ay is not None
        else:
            ax = None
            ay = None
        if not ok:
            fail_count += 1
        log("cycle=%02d ping X=%s Y=%s %s" % (cycle + 1, px, py, "OK" if ok else "FAIL"))
        log("   angle X=%s Y=%s fail=%d" % (ax, ay, fail_count))
        time.sleep_ms(500)


def setup():
    global stackchan
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(0, 4)
    M5.Lcd.printf("StackChan power cycle stress\n")
    stackchan = StackChan(i2c=1, uart=1)
    run_power_cycle_stress()
    log("Done. fail_count=%d" % fail_count)


def loop():
    M5.update()
    time.sleep_ms(20)


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
            print(e)

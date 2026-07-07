# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import *
from hardware.stackchan import StackChan


MOVE_PATTERN = ((0, 0), (20, 10), (-20, -10), (35, 20), (-35, -20), (0, 0))
CYCLES = 20
SETTLE_MS = 800
READBACK_TOLERANCE_DEG = 12

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


def angle_ok(target, actual):
    if actual is None:
        return False
    return abs(float(actual) - float(target)) <= READBACK_TOLERANCE_DEG


def run_repeat_move_test():
    global fail_count
    stackchan.set_servo_power(enable=True, settle_ms=SETTLE_MS)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=True)
    for cycle in range(CYCLES):
        for x_target, y_target in MOVE_PATTERN:
            stackchan.set_servo_angle(stackchan.SERVO_ID_X, x_target, 500, 30)
            stackchan.set_servo_angle(stackchan.SERVO_ID_Y, y_target, 500, 30)
            time.sleep_ms(650)
            x_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_X)
            y_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_Y)
            x_cur = stackchan.get_servo_current(stackchan.SERVO_ID_X)
            y_cur = stackchan.get_servo_current(stackchan.SERVO_ID_Y)
            ok = angle_ok(x_target, x_angle) and angle_ok(y_target, y_angle)
            if not ok:
                fail_count += 1
            log(
                "%02d X %s->%s Y %s->%s %s"
                % (cycle + 1, x_target, x_angle, y_target, y_angle, "OK" if ok else "FAIL")
            )
            log("   current X=%s Y=%s fail=%d" % (x_cur, y_cur, fail_count))
            time.sleep_ms(250)
    stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 500, 30)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 0, 500, 30)


def setup():
    global stackchan
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(0, 4)
    M5.Lcd.printf("StackChan repeat move test\n")
    stackchan = StackChan(i2c=1, uart=1)
    run_repeat_move_test()
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

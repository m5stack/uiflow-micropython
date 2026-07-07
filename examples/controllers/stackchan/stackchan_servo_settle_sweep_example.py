# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import *
from hardware.stackchan import StackChan


SETTLE_DELAYS_MS = (100, 200, 300, 500, 800, 1200)

stackchan = None
lines = []


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


def read_servo_status(servo_id):
    ping = stackchan.servo.ping(servo_id)
    mode = stackchan.servo.read_mode(servo_id)
    pos = stackchan.servo.read_pos(servo_id)
    volt = stackchan.get_servo_voltage(servo_id)
    angle = stackchan.get_servo_angle(servo_id)
    return ping, mode, pos, volt, angle


def run_sweep():
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=False)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=False)
    for delay_ms in SETTLE_DELAYS_MS:
        stackchan.set_servo_power(enable=False)
        time.sleep_ms(500)
        stackchan.set_servo_power(enable=True, settle_ms=delay_ms)
        x = read_servo_status(stackchan.SERVO_ID_X)
        y = read_servo_status(stackchan.SERVO_ID_Y)
        ok = x[0] == stackchan.SERVO_ID_X and y[0] == stackchan.SERVO_ID_Y
        log("settle=%4dms %s" % (delay_ms, "OK" if ok else "FAIL"))
        log("  X ping=%s mode=%s pos=%s v=%s a=%s" % x)
        log("  Y ping=%s mode=%s pos=%s v=%s a=%s" % y)
        time.sleep_ms(1200)


def setup():
    global stackchan
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(0, 4)
    M5.Lcd.printf("StackChan servo settle sweep\n")
    stackchan = StackChan(i2c=1, uart=1)
    run_sweep()
    log("Done. Reboot to run again.")


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

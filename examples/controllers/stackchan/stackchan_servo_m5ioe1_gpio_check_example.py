# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import *
from driver.m5ioe1 import (
    REG_GPIO_MODE_L,
    REG_GPIO_OUT_L,
    REG_GPIO_IN_L,
    REG_GPIO_PU_L,
    REG_GPIO_PD_L,
    REG_GPIO_DRV_L,
)
from hardware.stackchan import StackChan


SERVO_POWER_BIT = 0  # StackChan servo power is M5IOE1 G1, bit 0 in the GPIO bitmap.

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


def read16(reg):
    return stackchan.ioe1._read_reg16(reg)


def dump_gpio(tag):
    mode = read16(REG_GPIO_MODE_L)
    out = read16(REG_GPIO_OUT_L)
    inn = read16(REG_GPIO_IN_L)
    pu = read16(REG_GPIO_PU_L)
    pd = read16(REG_GPIO_PD_L)
    drv = read16(REG_GPIO_DRV_L)
    pwr = 1 if (out & (1 << SERVO_POWER_BIT)) else 0
    log("%s pwr_bit=%d mode=%04x out=%04x in=%04x" % (tag, pwr, mode, out, inn))
    log("   pu=%04x pd=%04x drv=%04x" % (pu, pd, drv))


def run_gpio_check():
    log("i2c scan: %s" % ([hex(i) for i in stackchan.i2c.scan()],))
    dump_gpio("boot")
    stackchan.set_servo_power(enable=False)
    time.sleep_ms(300)
    dump_gpio("power off")
    stackchan.set_servo_power(enable=True, settle_ms=800)
    dump_gpio("power on")
    px = stackchan.servo.ping(stackchan.SERVO_ID_X)
    py = stackchan.servo.ping(stackchan.SERVO_ID_Y)
    log("servo ping X=%s Y=%s" % (px, py))
    stackchan.set_servo_power(enable=False)
    time.sleep_ms(300)
    dump_gpio("final off")


def setup():
    global stackchan
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(0, 4)
    M5.Lcd.printf("StackChan M5IOE1 GPIO check\n")
    stackchan = StackChan(i2c=1, uart=1)
    run_gpio_check()
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

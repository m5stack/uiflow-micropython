# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import *
from driver.m5ioe1 import REG_LED_CFG, REG_LED_RAM_START
from hardware.stackchan import StackChan


COLORS = (0x33CC00, 0x00CCCC, 0x000099)
GROUPS = (
    ((0, 0), (0, 1), (1, 0), (1, 1)),
    ((0, 2), (0, 3), (1, 2), (1, 3)),
    ((0, 4), (0, 5), (1, 4), (1, 5)),
)
HOLD_MS = 300

stackchan = None
lines = []
active = [False, False, False]
last_touch = [0, 0, 0]
press_count = [0, 0, 0]
last_sample = 0


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


def set_group(group, color):
    for strip, led in GROUPS[group]:
        stackchan.set_rgb_color(strip, led, color)


def led_ram_word(index):
    reg = REG_LED_RAM_START + index * 2
    data = stackchan.i2c.readfrom_mem(stackchan.ioe1.addr, reg, 2)
    return (data[1] << 8) | data[0]


def rgb_self_test():
    log("i2c scan: %s" % ([hex(i) for i in stackchan.i2c.scan()],))
    for color in (0x330000, 0x003300, 0x000033, 0x000000):
        stackchan.set_rgb_color(color)
        time.sleep_ms(250)
    cfg = stackchan.ioe1._read_reg8(REG_LED_CFG)
    log("led_cfg=0x%02x led0=0x%04x" % (cfg, led_ram_word(0)))


def setup():
    global stackchan, last_touch, last_sample
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(0, 4)
    M5.Lcd.printf("StackChan touch RGB diagnostic\n")
    stackchan = StackChan(i2c=1, uart=1)
    now = time.ticks_ms()
    last_touch = [now, now, now]
    last_sample = now
    rgb_self_test()
    log("Touch pads to light paired LEDs")


def loop():
    global last_sample
    M5.update()
    now = time.ticks_ms()
    tp = stackchan.get_touch()
    if tp is None:
        tp = [0, 0, 0]

    for index in range(3):
        if tp[index]:
            last_touch[index] = now
            if not active[index]:
                active[index] = True
                press_count[index] += 1
                set_group(index, COLORS[index])
        elif active[index] and time.ticks_diff(now, last_touch[index]) > HOLD_MS:
            active[index] = False
            set_group(index, 0x000000)

    if time.ticks_diff(now, last_sample) >= 200:
        last_sample = now
        log("tp=%s active=%s" % (tp, active))
        log("count=%s led0=0x%04x" % (press_count, led_ram_word(0)))
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

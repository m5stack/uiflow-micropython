# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
# SPDX-License-Identifier: MIT

import M5
import usbhost

M5.begin()
M5.Lcd.fillScreen(0x202020)
M5.Lcd.drawString("USB-A keyboard / mouse test", 8, 8)
x = M5.Lcd.width() // 2
y = M5.Lcd.height() // 2
host = usbhost.HIDHost()
last_dropped = 0
try:
    while True:
        M5.update()
        event = host.read(timeout=10)
        if event is not None:
            if event["event"] == "input" and event["protocol"] == "mouse":
                M5.Lcd.fillCircle(x, y, 4, 0x202020)
                x = max(4, min(M5.Lcd.width() - 5, x + event["dx"]))
                y = max(32, min(M5.Lcd.height() - 5, y + event["dy"]))
                M5.Lcd.fillCircle(x, y, 4, 0x00FF00 if event["buttons"] else 0xFFFFFF)
            else:
                print(event)
        dropped = host.dropped()
        if dropped != last_dropped:
            print("USB HID queue overflow; dropped:", dropped)
            print("Connected interfaces:", host.devices())
            last_dropped = dropped
finally:
    host.deinit()

# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
# SPDX-License-Identifier: MIT
"""Tab5/Tab5X: USB-A mouse dashboard + USB-C touchscreen mouse, with CDC retained.

Copy this file and tab5_mouse_transport.py to the device, then import this module.
USB HID is added alongside CDC. Touch STOP to release and exit.
"""

import json
import time
import M5
import usbhost
from usb.device.mouse import Mouse
from tab5_mouse_transport import MouseTransport, Touchpad

BG = 0x11141A
PANEL = 0x1C222D
PAD = 0x252E3D
INK = 0xEFF3F8
MUTED = 0x97A8BC
RED = 0xE52335
GREEN = 0x55D6A3
BLUE = 0x67B7FF


def text(value, x, y, color=INK, size=2):
    M5.Lcd.setTextSize(size)
    M5.Lcd.setTextColor(color)
    M5.Lcd.drawString(str(value), x, y)


def box(rect, color):
    M5.Lcd.fillRoundRect(*rect, 12, color)


def run():
    M5.begin()
    lcd = M5.Lcd
    w, h = lcd.width(), lcd.height()
    margin = 20
    lcd.fillScreen(BG)
    text("TAB5 / TAB5X / USB MOUSE", 24, 26, INK, 3)
    text("A: physical mouse   C: touchpad + CDC", 24, 66, MUTED)
    if h >= w:
        host_rect = (margin, 105, w - 40, 430)
        device_rect = (margin, 555, w - 40, h - 645)
    else:
        host_rect = (margin, 105, w // 2 - 30, h - 195)
        device_rect = (w // 2 + 10, 105, w // 2 - 30, h - 195)
    hx, hy, hw, hh = host_rect
    ux, uy, uw, uh = device_rect
    canvas = (hx + 16, hy + 112, hw - 32, hh - 190)
    pad = (ux + 16, uy + 142, uw - 32, uh - 265)
    bw = (uw - 52) // 4
    buttons = {
        name: (ux + 16 + i * (bw + 6), uy + uh - 102, bw, 64)
        for i, name in enumerate(("left", "right", "up", "down"))
    }
    start = (w // 2 - 110, h - 70, 220, 50)
    box(host_rect, PANEL)
    box(device_rect, PANEL)
    text("USB-A / HOST", hx + 16, hy + 18, GREEN, 3)
    text("USB-C / DEVICE", ux + 16, uy + 18, BLUE, 3)
    import usb.device

    try:
        mouse = Mouse(interface_str="M5 Touchpad", builtin_driver=True)
        host = usbhost.HIDHost()
    except Exception:
        try:
            usbhost.deinit()
        finally:
            usb.device.get().init(builtin_driver=True)
        raise
    tx = MouseTransport(mouse)
    touchpad = Touchpad(tx, pad, buttons)
    x, y = canvas[0] + canvas[2] // 2, canvas[1] + canvas[3] // 2
    mask = 0
    rx = errors = 0
    clicks = [0, 0, 0]
    last_delta = (0, 0)
    connected = []
    last_key = "--"
    elapsed = 0
    previous = time.ticks_ms()
    paint_at = log_at = 0
    box(start, RED)
    text("STOP", start[0] + 76, start[1] + 16)
    try:
        while True:
            now = time.ticks_ms()
            elapsed += time.ticks_diff(now, previous)
            previous = now
            M5.update()
            count = M5.Touch.getCount()
            px, py = M5.Touch.getX(), M5.Touch.getY()
            if count == 1 and Touchpad.inside(start, px, py):
                break
            tx.poll()
            touchpad.update(count, px, py, elapsed)
            for _ in range(32):
                event = host.read()
                if event is None:
                    break
                kind = event["event"]
                if kind in ("connected", "disconnected"):
                    connected = host.devices()
                    if kind == "disconnected" and event["protocol"] == "mouse":
                        mask = 0
                elif kind == "error":
                    errors += 1
                elif kind == "input":
                    rx += 1
                    if event["protocol"] == "mouse":
                        old = mask
                        mask = event["buttons"]
                        for i in range(3):
                            if mask & (1 << i) and not old & (1 << i):
                                clicks[i] += 1
                        dx, dy = event["dx"], event["dy"]
                        last_delta = (dx, dy)
                        x = max(canvas[0] + 10, min(canvas[0] + canvas[2] - 27, x + dx))
                        y = max(canvas[1] + 10, min(canvas[1] + canvas[3] - 27, y + dy))
                    elif event["protocol"] == "keyboard":
                        last_key = str(event["keys"])
            if elapsed >= paint_at:
                paint_at = elapsed + 50
                lcd.fillRect(hx + 12, hy + 58, hw - 24, 50, PANEL)
                identity = " / ".join("%04X:%04X" % (d["vid"], d["pid"]) for d in connected)
                text(identity or "Waiting for a USB-A mouse...", hx + 16, hy + 60, MUTED)
                text("RX %d   drop %d   err %d" % (rx, host.dropped(), errors), hx + 16, hy + 85)
                box(canvas, PAD)
                lcd.drawLine(x, y, x + 16, y + 20, GREEN)
                lcd.drawLine(x, y, x + 3, y + 25, GREEN)
                lcd.drawLine(x + 3, y + 25, x + 16, y + 20, GREEN)
                lcd.fillRect(hx + 12, hy + hh - 72, hw - 24, 64, PANEL)
                text("L %d   R %d   M %d" % tuple(clicks), hx + 16, hy + hh - 68, GREEN)
                text(
                    "dX %d  dY %d   keys %s" % (last_delta[0], last_delta[1], last_key),
                    hx + 16,
                    hy + hh - 38,
                    MUTED,
                )
                lcd.fillRect(ux + 12, uy + 60, uw - 24, 77, PANEL)
                text(
                    "READY" if tx.connected else "Waiting for USB-C host",
                    ux + 16,
                    uy + 60,
                    GREEN if tx.connected else MUTED,
                )
                text(
                    "TX %d  ACK %d  queued %d" % (tx.sent, tx.completed, len(tx.queue)),
                    ux + 16,
                    uy + 86,
                )
                text("Slide / tap / hold still to drag", ux + 16, uy + 112, MUTED)
                box(pad, PAD)
                text("TOUCHPAD", pad[0] + 20, pad[1] + 20, MUTED, 3)
                if count == 1 and Touchpad.inside(pad, px, py):
                    lcd.fillCircle(px, py, 12, RED if touchpad.dragging else BLUE)
                for name, rect in buttons.items():
                    box(rect, BLUE if touchpad.mode == name else PAD)
                    label = {"left": "LEFT", "right": "RIGHT", "up": "UP", "down": "DOWN"}[name]
                    text(label, rect[0] + 12, rect[1] + 24)
            if elapsed >= log_at:
                log_at = elapsed + 2000
                print(
                    "@@USBDEMO "
                    + json.dumps(
                        {
                            "rx": rx,
                            "clicks": clicks,
                            "dropped": host.dropped(),
                            "errors": errors,
                            "usb_open": tx.connected,
                            "tx": tx.sent,
                            "completed": tx.completed,
                            "queued": len(tx.queue),
                            "tx_overflows": tx.overflows,
                            "touch": count,
                            "send_errors": tx.send_errors,
                        }
                    )
                )
            time.sleep_ms(2)
    finally:
        tx.enqueue(0)
        for _ in range(100):
            tx.poll()
            if not tx.queue and not tx.inflight:
                break
            time.sleep_ms(2)
        try:
            host.deinit()
        finally:
            # Restore the original built-in CDC configuration on exit.
            usb.device.get().init(builtin_driver=True)
        lcd.fillScreen(BG)
        text("Demo stopped / CDC restored", 24, 40, GREEN, 3)


if __name__ == "__main__":
    run()

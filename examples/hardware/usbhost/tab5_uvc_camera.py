# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
# SPDX-License-Identifier: MIT
"""Tab5 USB-A UVC MJPEG preview. Run manually with a directly connected camera."""

import os
import time
import M5
import usbhost


def _save_frame(frame, sequence):
    while sequence < 10000:
        path = "/flash/uvc-%04d.jpg" % sequence
        sequence += 1
        try:
            os.stat(path)
        except OSError as error:
            if error.args[0] != 2:
                raise
            with open(path, "wb") as output:
                output.write(frame)
            return path, sequence
    raise OSError("No free UVC capture filename")


def run(width=640, height=480, fps=0, frame_size=512 * 1024):
    M5.begin()
    lcd = M5.Lcd
    w, h = lcd.width(), lcd.height()
    background = 0x11141A
    lcd.fillScreen(background)
    lcd.setTextSize(2)
    lcd.setTextColor(0xFFFFFF)
    lcd.drawString("TAB5 / USB-A UVC CAMERA", 16, 16)
    lcd.drawString("Connect an MJPEG USB camera directly.", 16, 48)
    buttons = {
        "capture": (16, h - 70, (w - 48) // 2, 52),
        "stop": ((w + 16) // 2, h - 70, (w - 48) // 2, 52),
    }
    for label, rect in buttons.items():
        lcd.fillRoundRect(*rect, 10, 0xE52335 if label == "stop" else 0x255E85)
        lcd.drawString(label.upper(), rect[0] + 20, rect[1] + 17)
    buffer = bytearray(frame_size)
    view = memoryview(buffer)
    scale = min((w - 32) / width, (h - 200) / height)
    x = (w - int(width * scale)) // 2
    y = 100 + (h - 200 - int(height * scale)) // 2
    camera = usbhost.UVCCamera(width=width, height=height, fps=fps, frame_size=frame_size)
    sequence = 1
    capture = touched = False
    delivered = 0
    last_stats = time.ticks_ms()
    try:
        print("UVC formats:", camera.formats())
        camera.start()
        while True:
            M5.update()
            pressed = M5.Touch.getCount() == 1
            tx, ty = M5.Touch.getX(), M5.Touch.getY()
            if pressed and not touched:
                for label, (bx, by, bw, bh) in buttons.items():
                    if bx <= tx < bx + bw and by <= ty < by + bh:
                        if label == "stop":
                            return
                        capture = True
            touched = pressed
            length = camera.readinto(buffer, timeout=20)
            if length:
                image = view[:length]
                lcd.drawJpg(image, x, y, scaleX=scale, scaleY=scale)
                delivered += 1
                if capture:
                    path, sequence = _save_frame(image, sequence)
                    capture = False
                    print("Saved:", path, "bytes:", length)
            now = time.ticks_ms()
            elapsed = time.ticks_diff(now, last_stats)
            if elapsed >= 1000:
                stats = camera.info()
                rate = delivered * 1000 / elapsed
                lcd.fillRect(0, 74, w, 22, background)
                lcd.drawString(
                    "%.1f fps  drop %d  overflow %d  error %d"
                    % (rate, stats["dropped"], stats["overflows"], stats["errors"]),
                    16,
                    74,
                )
                print("UVC:", stats, "preview_fps:", rate)
                delivered = 0
                last_stats = now
    finally:
        camera.deinit()
        lcd.fillScreen(background)
        lcd.drawString("UVC stopped / USB-C REPL retained", 16, 40)


if __name__ == "__main__":
    run()

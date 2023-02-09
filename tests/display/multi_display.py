# -*- encoding: utf-8 -*-
# multi display
import M5
import time
import random


index = 0


def setup():
    M5.begin()
    time.sleep(1)


def loop():
    global index
    index = index + 1
    if index > 2:  # screen number - 1
        index = 0
    M5.setPrimaryDisplay(index)
    if M5.Lcd.width() == 64:
        M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu12)
    else:
        M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu24)

    M5.Lcd.fillCircle(
        random.randint(10, M5.Lcd.width()),
        random.randint(10, M5.Lcd.height()),
        random.randint(5, 20),
        random.randint(0, 0xFFFFFF),
    )
    M5.Lcd.drawString("Screen:" + str(index), 0, 0)


if __name__ == "__main__":
    setup()
    while True:
        loop()

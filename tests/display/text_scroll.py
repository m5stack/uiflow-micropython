# -*- encoding: utf-8 -*-
# text scroll
import M5
import gc
import time
import random

text0 = "hello world"
text1 = "this"
text2 = "is"
text3 = "text"
text4 = "log"
text5 = "vertical"
text6 = "scroll"
text7 = "sample"


text = [text0, text1, text2, text3, text4, text5, text6, text7]
fonts = [
    M5.Lcd.FONTS.ASCII7,
    M5.Lcd.FONTS.DejaVu9,
    M5.Lcd.FONTS.DejaVu12,
    M5.Lcd.FONTS.DejaVu18,
    M5.Lcd.FONTS.DejaVu24,
    M5.Lcd.FONTS.DejaVu40,
    M5.Lcd.FONTS.DejaVu56,
    M5.Lcd.FONTS.DejaVu72,
    M5.Lcd.FONTS.EFontCN24,
    M5.Lcd.FONTS.EFontJA24,
    M5.Lcd.FONTS.EFontKR24,
]

count = 0
canvas = None


def setup():
    global canvas
    M5.begin()
    canvas = M5.Display.newCanvas(M5.Display.width(), M5.Display.height(), 1, 1)
    canvas.setTextScroll(True)


def loop():
    global count, canvas, text
    text_str = "%s\r\n" % (text[count & 7])
    canvas.setFont(fonts[random.randint(0, 10)])
    canvas.print(text_str)
    canvas.push(0, 0)
    count = count + 1


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except:
        # error handler
        # if use canvas, need manual delete it to free allocated memory for now
        if canvas:
            canvas.delete()

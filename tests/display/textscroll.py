# -*- encoding: utf-8 -*-
# text scroll
import m5
import gc
import time

text0 = "hello world"
text1 = "this"
text2 = "is"
text3 = "text"
text4 = "log"
text5 = "vertical"
text6 = "scroll"
text7 = "sample"

text = [text0, text1, text2, text3, text4, text5, text6, text7]

count = 0
canvas = None


def setup():
    global canvas
    m5.begin()
    canvas = m5.lcd.newCanvas(128, 128, 1, 1)
    canvas.setTextScroll(True)


def loop():
    global count, canvas, text
    text_str = "%04d:%s\r\n" % (count, text[count & 7])
    canvas.print(text_str)
    canvas.push(0, 0)
    count = count + 1


if __name__ == "__main__":
    setup()
    try:
        while True:
            loop()
    except Exception as e:
        # if use canvas, need manual delete it for now :)
        canvas.delete()

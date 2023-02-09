# -*- encoding: utf-8 -*-
# text scroll
import M5
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
    M5.begin()
    canvas = M5.Display.newCanvas(M5.Display.width(), M5.Display.height(), 1, 1)
    canvas.setTextScroll(True)


def loop():
    global count, canvas, text
    text_str = "%04d:%s\r\n" % (count, text[count & 7])
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

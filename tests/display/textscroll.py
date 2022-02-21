import m5
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

m5.begin()
canvas = m5.lcd.newCanvas(320, 240, 1, 1)
canvas.setTextScroll(True)

count = 0
while True:
    text_str = "%04d:%s\r\n" % (count, text[count & 7])
    canvas.print(text_str)
    canvas.push(0, 0)
    count = count + 1

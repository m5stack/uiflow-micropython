# -*- encoding: utf-8 -*-
# draw image test
import m5
from m5 import lcd
import random
import time

m5.begin()

jpg = open("res/img/m5stack_80x60.jpg", "b")
lcd.drawImage(jpg.read(), 0, 0)
jpg.seek(0)
lcd.drawJpg(jpg.read(), 0, 180)
jpg.close()

bmp = open("res/img/m5stack_80x60.bmp", "b")
lcd.drawImage(bmp.read(), 240, 0)
bmp.seek(0)
lcd.drawBmp(bmp.read(), 240, 180)
bmp.close()

png = open("res/img/uiflow_44x44.png", "b")
lcd.drawImage(png.read(), 116, 98)
png.seek(0)
lcd.drawPng(png.read(), 160, 98)
png.close()

time.sleep(1)
lcd.clear(0x8BF5CE)

lcd.drawImage("res/img/m5stack_80x60.bmp", 0, 0)
lcd.drawImage("res/img/m5stack_80x60.jpg", 240, 0)
lcd.drawImage("res/img/uiflow_44x44.png", 138, 98)
lcd.drawImage("res/img/m5stack.png", 0, 0)
lcd.drawBmp("res/img/m5stack_80x60.bmp", 240, 180)
lcd.drawJpg("res/img/m5stack_80x60.jpg", 0, 180)

time.sleep(1)
lcd.clear(0x8BF5CE)
lcd.drawPng("res/img/m5stack.png", 0, 0)

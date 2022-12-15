# -*- encoding: utf-8 -*-
# draw image test
import M5
from M5 import Display
import random
import time

M5.begin()

jpg = open("res/img/M5stack_80x60.jpg", "b")
Display.drawImage(jpg.read(), 0, 0)
jpg.seek(0)
Display.drawJpg(jpg.read(), 0, 180)
jpg.close()

bmp = open("res/img/M5stack_80x60.bmp", "b")
Display.drawImage(bmp.read(), 240, 0)
bmp.seek(0)
Display.drawBmp(bmp.read(), 240, 180)
bmp.close()

png = open("res/img/uiflow_44x44.png", "b")
Display.drawImage(png.read(), 116, 98)
png.seek(0)
Display.drawPng(png.read(), 160, 98)
png.close()

time.sleep(1)
Display.clear(0x8BF5CE)

Display.drawImage("res/img/M5stack_80x60.bmp", 0, 0)
Display.drawImage("res/img/M5stack_80x60.jpg", 240, 0)
Display.drawImage("res/img/uiflow_44x44.png", 138, 98)
Display.drawImage("res/img/M5stack.png", 0, 0)
Display.drawBmp("res/img/M5stack_80x60.bmp", 240, 180)
Display.drawJpg("res/img/M5stack_80x60.jpg", 0, 180)

time.sleep(1)
Display.clear(0x8BF5CE)
Display.drawPng("res/img/M5stack.png", 0, 0)

# Camera test for CoreS3
import m5
from m5 import lcd
import camera

m5.begin()
camera.init(framesize=camera.FRAME_96X96)

while True:
    buf = camera.capture()
    if buf:
        lcd.drawRawBuf(buf, 8, 16, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 112, 16, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 216, 16, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 8, 128, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 112, 128, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 216, 128, 96, 96, 96 * 96)

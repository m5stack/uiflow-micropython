# Camera test for CoreS3
import m5
from m5 import lcd
import camera


def setup():
    m5.begin()
    camera.init(framesize=camera.FRAME_96X96)


def loop():
    buf = camera.capture()
    if buf:
        lcd.drawRawBuf(buf, 8, 16, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 112, 16, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 216, 16, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 8, 128, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 112, 128, 96, 96, 96 * 96)
        lcd.drawRawBuf(buf, 216, 128, 96, 96, 96 * 96)


if __name__ == "__main__":
    setup()
    try:
        while True:
            loop()
    except Exception as e:
        pass

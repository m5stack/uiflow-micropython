# Camera test for CoreS3
import M5
from M5 import Display
import camera


def setup():
    M5.begin()
    camera.init(framesize=camera.FRAME_96X96)


def loop():
    buf = camera.capture()
    if buf:
        Display.drawRawBuf(buf, 8, 16, 96, 96, 96 * 96)
        Display.drawRawBuf(buf, 112, 16, 96, 96, 96 * 96)
        Display.drawRawBuf(buf, 216, 16, 96, 96, 96 * 96)
        Display.drawRawBuf(buf, 8, 128, 96, 96, 96 * 96)
        Display.drawRawBuf(buf, 112, 128, 96, 96, 96 * 96)
        Display.drawRawBuf(buf, 216, 128, 96, 96, 96 * 96)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except:
        # error handler
        # if use canvas, need manual delete it to free allocated memory for now
        pass

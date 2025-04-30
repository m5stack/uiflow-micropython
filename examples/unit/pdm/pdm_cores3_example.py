import os, sys, io
import M5
from M5 import *
from unit import PDMUnit
import time


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
pdm_0 = None


rec_data = None


def setup():
    global title0, label0, label1, label2, label3, pdm_0, rec_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("PDMUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Is Start:", 20, 54, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Is Done:", 20, 119, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 131, 52, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 133, 121, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pdm_0 = PDMUnit((1, 2), i2s_port=2, sample_rate=44100)
    Speaker.begin()
    Speaker.setVolumePercentage(1)
    Speaker.end()
    pdm_0.begin()
    label2.setText(str("waiting..."))
    time.sleep(2)
    rec_data = bytearray(44100 * 15)
    pdm_0.record(rec_data, 44100, False)
    time.sleep_ms(150)
    while pdm_0.isRecording():
        label2.setText(str("recording..."))
        time.sleep_ms(100)
    pdm_0.end()
    label2.setText(str("ending..."))
    Speaker.begin()
    label3.setText(str("playing..."))
    Speaker.playRaw(rec_data, 44100)
    while Speaker.isPlaying():
        time.sleep_ms(150)
    label3.setText(str("done"))


def loop():
    global title0, label0, label1, label2, label3, pdm_0, rec_data
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

import os, sys, io
import M5
from M5 import *
from module import GPSModule


GPST = None
label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
label9 = None
label10 = None
label11 = None
com_gps_0 = None


def setup():
    global \
        GPST, \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label10, \
        label11, \
        com_gps_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    GPST = Widgets.Title(
        "             GPS Module Demo", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "Locate status:", 10, 27, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Satellite nums:", 2, 52, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Longitude:", 40, 105, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Latitude:", 56, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Date:", 85, 131, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("Time:", 83, 159, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 150, 28, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 150, 52, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 150, 79, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label9 = Widgets.Label("label9", 150, 107, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label10 = Widgets.Label("label10", 150, 134, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label11 = Widgets.Label("label11", 150, 160, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    com_gps_0 = GPSModule(2, 13, 14)
    com_gps_0.set_time_zone(8)


def loop():
    global \
        GPST, \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label10, \
        label11, \
        com_gps_0
    M5.update()
    if com_gps_0.is_locate_valid():
        label6.setText(str("OK"))
    else:
        label6.setText(str("False"))
    label7.setText(str(com_gps_0.get_satellite_num()))
    label8.setText(str(com_gps_0.get_latitude()))
    label9.setText(str(com_gps_0.get_longitude()))
    label10.setText(str(com_gps_0.get_date()))
    label11.setText(str(com_gps_0.get_time()))


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


# GPS Module

<!-- .. include:: ../refs/module.gps.ref -->

COM.GPS is a satellite positioning module in the M5Stack stacking module series. It is developed based on the NEO-M8N module.

Support the following products:
######

###### | |GPSModule|             | |COM.GPSModule|         |

Micropython Example:

```python
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

```

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |gps_core2_example.m5f2|

## class GPSModule

## Constructors

<!-- .. class:: GPSModule(id, rx, tx) -->

    initialize Function.

    :param int id: UART controllers id, the range is 0 to 2.
    :param int rx: UART rx pin.
    :param int tx: UART tx pin.

    UIFLOW2:

## Methods

<!-- .. method:: GPSModule.set_time_zone(value) -->

    set timezone function.

    :param int value: timezone value

    UIFLOW2:

<!-- .. method:: GPSModule.get_time_zone() -->

    get timezone function.

    :return (int): timezone value

    UIFLOW2:

<!-- .. method:: GPSModule.get_satellite_num() -->

    get satellite numbers.

    :return (str): satellite numbers value.

    UIFLOW2:

<!-- .. method:: GPSModule.get_altitude() -->

    get altitude.

    :return (str): altitude unit is meter.

    UIFLOW2:

<!-- .. method:: GPSModule.get_time() -->

    get time.

    :return (str): time(hh:mm:ss)

    UIFLOW2:

<!-- .. method:: GPSModule.get_date() -->

    get date.

    :return (str): date(dd/mm/yy)

    UIFLOW2:

<!-- .. method:: GPSModule.get_latitude() -->

    get latitude.

    :return (str): latitude, using degrees minutes format (ddmm.mmmmmN/S).

    UIFLOW2:

<!-- .. method:: GPSModule.get_longitude() -->

    get longitude.

    :return (str): longitude, using degrees minutes format (ddmm.mmmmmE/W).

    UIFLOW2:

<!-- .. method:: GPSModule.get_latitude_decimal() -->

    get latitude decimal.

    :return (float): latitude decimal(dd.dddd).

    UIFLOW2:

<!-- .. method:: GPSModule.get_longitude_decimal() -->

    get longitude decimal.

    :return (float): longitude decimal(dd.dddd).

    UIFLOW2:

<!-- .. method:: GPSModule.get_speed(type) -->

    get speed.

    :return (str): speed.
    :param int type: speed type, 0 km/h, 1 knot/h
        Options:
        - ``km/h``: 0
        - ``knot/h``: 1

    UIFLOW2:

<!-- .. method:: GPSModule.get_course() -->

    get course.

    :return (str): course unit is °.

    UIFLOW2:

<!-- .. method:: GPSModule.is_locate_valid() -->

    get locate status.

    :return (bool): locate status, true is locate, false is not locate.

    UIFLOW2:

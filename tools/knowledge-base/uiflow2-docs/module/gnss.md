
# GNSS Module

<!-- .. include:: ../refs/module.gnss.ref -->

GNSS Module is a global positioning wireless communication module featuring the NEO-M9N-00B GPS module. It incorporates BMI270, BMM150 and a barometric pressure sensor.

Support the following products:

|GNSSModule|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import GNSSModule

title0 = None
label3 = None
label4 = None
label5 = None
label6 = None
label10 = None
label11 = None
label12 = None
label13 = None
label14 = None
label15 = None
label16 = None
label17 = None
label18 = None
label19 = None
label20 = None
label21 = None
label22 = None
label23 = None
line0 = None
gnss_0 = None

list2 = None

def setup():
    global \
        title0, \
        label3, \
        label4, \
        label5, \
        label6, \
        label10, \
        label11, \
        label12, \
        label13, \
        label14, \
        label15, \
        label16, \
        label17, \
        label18, \
        label19, \
        label20, \
        label21, \
        label22, \
        label23, \
        line0, \
        gnss_0, \
        list2

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "            M135 GNSS Demo", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label3 = Widgets.Label("angle:", 2, 23, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label(
        "attitude(yaw):", 1, 73, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label5 = Widgets.Label("temp:", 4, 128, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("pressure:", 2, 180, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label10 = Widgets.Label("label10", 4, 46, 1.0, 0x3EF815, 0x222222, Widgets.FONTS.DejaVu18)
    label11 = Widgets.Label("label11", 5, 102, 1.0, 0xF60505, 0x222222, Widgets.FONTS.DejaVu18)
    label12 = Widgets.Label("label12", 5, 154, 1.0, 0x3EF815, 0x222222, Widgets.FONTS.DejaVu18)
    label13 = Widgets.Label("label13", 5, 208, 1.0, 0xF60505, 0x222222, Widgets.FONTS.DejaVu18)
    label14 = Widgets.Label("lat:", 158, 51, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label15 = Widgets.Label("long:", 157, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label16 = Widgets.Label("sta:", 158, 24, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label17 = Widgets.Label("date:", 158, 108, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label18 = Widgets.Label("time:", 159, 168, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label19 = Widgets.Label("label19", 159, 138, 1.0, 0x15F0FF, 0x222222, Widgets.FONTS.DejaVu18)
    label20 = Widgets.Label("label20", 159, 197, 1.0, 0xEAFF00, 0x222222, Widgets.FONTS.DejaVu18)
    label21 = Widgets.Label("label21", 205, 25, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label22 = Widgets.Label("label22", 205, 52, 1.0, 0x15F0FF, 0x222222, Widgets.FONTS.DejaVu18)
    label23 = Widgets.Label("label23", 205, 81, 1.0, 0xEAFF00, 0x222222, Widgets.FONTS.DejaVu18)
    line0 = Widgets.Line(142, 27, 142, 232, 0xFFFFFF)

    gnss_0 = GNSSModule(2, 13, 14, 0x69)

def loop():
    global \
        title0, \
        label3, \
        label4, \
        label5, \
        label6, \
        label10, \
        label11, \
        label12, \
        label13, \
        label14, \
        label15, \
        label16, \
        label17, \
        label18, \
        label19, \
        label20, \
        label21, \
        label22, \
        label23, \
        line0, \
        gnss_0, \
        list2
    M5.update()
    label10.setText(str(gnss_0.get_compass()))
    label11.setText(str((gnss_0.get_attitude())[0]))
    label12.setText(str(gnss_0.get_temperature()))
    label13.setText(str(gnss_0.get_pressure()))
    if gnss_0.is_locate_valid():
        label21.setText(str("OK"))
    else:
        label21.setText(str("Failed"))
    label22.setText(str(gnss_0.get_latitude()))
    label23.setText(str(gnss_0.get_longitude()))
    label19.setText(str(gnss_0.get_date()))
    label20.setText(str(gnss_0.get_time()))

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

    |gnss_core2_example.m5f2|

## class GNSSModule

## Constructors

<!-- .. class:: GNSSModule(id, rx, tx, address) -->

    initialize Function.

    :param int id: UART controllers id, the range is 0 to 2.
    :param int rx: UART rx pin.
    :param int tx: UART tx pin.
    :param int address:

    UIFLOW2:

## Methods

<!-- .. method:: GNSSModule.set_accel_gyro_odr(accel_odr, gyro_odr) -->

    Set the accelerometer and gyroscope output data rate.

    :param  accel_odr: range of 0.78 Hz … 1.6 kHz.
        Options:
        - ``25``: 25
        - ``50``: 50
        - ``100``: 100
        - ``200``: 200
        - ``400``: 400
        - ``800``: 800
        - ``1600``: 1600
        - ``0.78``: 0.78
        - ``1.5``: 1.5
        - ``3.1``: 3.1
        - ``6.25``: 6.25
        - ``12.5``: 12.5
    :param  gyro_odr: range of 25 Hz … 6.4 kHz.
        Options:
        - ``25``: 25
        - ``50``: 50
        - ``100``: 100
        - ``200``: 200
        - ``400``: 400
        - ``800``: 800
        - ``1600``: 1600
        - ``3200``: 3200

    UIFLOW2:

<!-- .. method:: GNSSModule.set_accel_range(accel_scale) -->

    Set the accelerometer scale range.

    :param  accel_scale: scale range of ±2g, ±4g, ±8g and ±16g.
        Options:
        - ``2``: 2
        - ``4``: 4
        - ``8``: 8
        - ``16``: 16

    UIFLOW2:

<!-- .. method:: GNSSModule.set_gyro_range(gyro_scale) -->

    Set the gyroscope scale range.

    :param  gyro_scale:
        Options:
        - ``125``: 125
        - ``250``: 250
        - ``500``: 500
        - ``1000``: 1000
        - ``2000``: 2000

    UIFLOW2:

<!-- .. method:: GNSSModule.set_magnet_odr(magnet_odr) -->

    :param  magnet_odr:
        Options:
        - ``2``: 2
        - ``6``: 6
        - ``8``: 8
        - ``10``: 10
        - ``15``: 15
        - ``20``: 20
        - ``25``: 25
        - ``30``: 30

    UIFLOW2:

<!-- .. method:: GNSSModule.set_gyro_offsets(x, y, z) -->

    Set the manual gyro calibrations offsets value.

    :param  x: gyro calibrations offsets value of X-axis
    :param  y: gyro calibrations offsets value of Y-axis
    :param  z: gyro calibrations offsets value of Z-axis

    UIFLOW2:

<!-- .. method:: GNSSModule.get_gyroscope() -->

    Get the tuple of x, y, and z values of the gyroscope and gyroscope vector in rad/sec.

    :return (tuple): gyroscope tuple (float, float, float)

    UIFLOW2:

<!-- .. method:: GNSSModule.get_accelerometer() -->

    Get the tuple of x, y, and z values of the accelerometer and acceleration vector in gravity units (9.81m/s^2).

    :return (tuple): accelerometer tuple (float, float, float)

    UIFLOW2:

<!-- .. method:: GNSSModule.get_magnetometer() -->

    Get the tuple of x, y, and z values of the magnetometer and magnetometer vector in uT.

    :return (tuple): magnetometer tuple (float, float, float)

    UIFLOW2:

<!-- .. method:: GNSSModule.get_compass() -->

    Get the compass heading value is in range of 0º ~ 360º.

    :return (float): range is 0 to 360 degree

    UIFLOW2:

<!-- .. method:: GNSSModule.get_attitude() -->

    Get the attitude angles as yaw, pitch, and roll in degrees.

    :return (tuple): tuple of yaw, pitch, and roll (float, float, float)

    UIFLOW2:

<!-- .. method:: GNSSModule.get_temperature() -->

    Get the temperature value in degrees celsius from the BMP280 sensor.

    :return (float): range is -40 ~ +85 °C.

    UIFLOW2:

<!-- .. method:: GNSSModule.get_pressure() -->

    Get the pressure value in pascals from the BMP280 sensor.

    :return (float): range is 300 ~ 1100 hPa.

    UIFLOW2:

<!-- .. method:: GNSSModule.set_time_zone(value) -->

    set timezone function.

    :param int value: timezone value

    UIFLOW2:

<!-- .. method:: GNSSModule.get_time_zone() -->

    get timezone function.

    :return (int): timezone value

    UIFLOW2:

<!-- .. method:: GNSSModule.get_satellite_num() -->

    get satellite numbers.

    :return (str): satellite numbers value.

    UIFLOW2:

<!-- .. method:: GNSSModule.get_altitude() -->

    get altitude.

    :return (str): altitude unit is meter.

    UIFLOW2:

<!-- .. method:: GNSSModule.get_time() -->

    get time.

    :return (str): time(hh:mm:ss)

    UIFLOW2:

<!-- .. method:: GNSSModule.get_date() -->

    get date.

    :return (str): date(dd/mm/yy)

    UIFLOW2:

<!-- .. method:: GNSSModule.get_latitude() -->

    get latitude.

    :return (str): latitude, using degrees minutes format (ddmm.mmmmmN/S).

    UIFLOW2:

<!-- .. method:: GNSSModule.get_longitude() -->

    get longitude.

    :return (str): longitude, using degrees minutes format (ddmm.mmmmmE/W).

    UIFLOW2:

<!-- .. method:: GNSSModule.get_latitude_decimal() -->

    get latitude decimal.

    :return (float): latitude decimal(dd.dddd).

    UIFLOW2:

<!-- .. method:: GNSSModule.get_longitude_decimal() -->

    get longitude decimal.

    :return (float): longitude decimal(dd.dddd).

    UIFLOW2:

<!-- .. method:: GNSSModule.get_speed(type) -->

    get speed.

    :return (str): speed.
    :param int type: speed type, 0 km/h, 1 knot/h
        Options:
        - ``km/h``: 0
        - ``knot/h``: 1

    UIFLOW2:

<!-- .. method:: GNSSModule.get_course() -->

    get course.

    :return (str): course unit is °.

    UIFLOW2:

<!-- .. method:: GNSSModule.is_locate_valid() -->

    get locate status.

    :return (bool): locate status, true is locate, false is not locate.

    UIFLOW2:

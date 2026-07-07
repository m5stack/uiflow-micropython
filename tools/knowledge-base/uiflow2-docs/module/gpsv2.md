
# GPS V2.0 Module

<!-- .. include:: ../refs/module.gpsv2.ref -->

Module GPS v2.0 is a high-performance GNSS global positioning module, integrated with the high-performance AT6668 chip to provide precise and reliable satellite positioning services. This module supports multi-frequency, multi-mode GNSS signal reception and is compatible with various satellite navigation systems, including GPS, BD2, BD3, GLONASS, GALILEO, and QZSS, enabling high-precision, multi-system joint positioning or single-system independent positioning, and offering excellent anti-jamming capabilities. In weak signal areas, it can quickly acquire higher precision positioning information.
The module comes equipped with an external SMA antenna, and also features a dip switch to allow users to flexibly switch TX/RX communication pins, with PPS signal output for precise timing adjustments. It supports multi-stack usage, offering more customization and flexibility, making it suitable for high-precision positioning applications such as in-vehicle navigation, IoT positioning devices, remote monitoring, smart cities, and home and industrial automation.

Support the following products:

    |GPSV2Module|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import GPSV2Module
import time

label0 = None
title0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
module_gpsv2_0 = None

power_on_time = None

def setup():
    global \
        label0, \
        title0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        module_gpsv2_0, \
        power_on_time

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Power On:", 1, 33, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title(
        "GPSV2Module Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Satellite Num:", 1, 66, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Timestamp:", 1, 202, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("GPS Data:", -6, 526, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Latitude:", 1, 104, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("Longitude:", 1, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("Altitude:", 1, 170, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    module_gpsv2_0 = GPSV2Module(2, 13, 14, 25)
    power_on_time = time.time()
    module_gpsv2_0.set_work_mode(7)

def loop():
    global \
        label0, \
        title0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        module_gpsv2_0, \
        power_on_time
    M5.update()
    label0.setText(str((str("Power On:") + str(((time.time()) - power_on_time)))))
    label1.setText(str((str("Satellite Num:") + str((module_gpsv2_0.get_satellite_num())))))
    label2.setText(str((str("Timestamp:") + str((module_gpsv2_0.get_timestamp())))))
    label4.setText(str((str("Latitude:") + str((module_gpsv2_0.get_latitude())))))
    label5.setText(str((str("Longitude:") + str((module_gpsv2_0.get_longitude())))))
    label6.setText(str((str("Altitude:") + str((module_gpsv2_0.get_altitude())))))
    time.sleep(1)

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

    |gpsv2_core2_example.m5f2|

## class GPSV2Module

## Constructors

<!-- .. class:: GPSV2Module(id, rx, tx) -->

    Initialize the GPSV2Module with a specific UART id and port for communication.

    :param int id: The UART ID for communication with the GPS module. It can be 0, 1, or 2.
    :param  rx: The RX pin of the UART.
    :param  tx: The TX pin of the UART.

    UIFLOW2:

## Methods

<!-- .. method:: GPSV2Module.set_work_mode(mode) -->

    Set the working mode of the GPS module.

    :param int mode: The mode to set, defined by the GPS module.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_work_mode() -->

    Get the current working mode of the GPS module.

    :return: The current working mode of the GPS module.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_antenna_state() -->

    Get the state of the antenna.

    :return: The antenna state.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_gps_time() -->

    Get the current GPS time.

    :return: The GPS time as a list of strings [hour, minute, second].

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_gps_date() -->

    Get the current GPS date.

    :return: The GPS date as a list of strings [day, month, year].

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_gps_date_time() -->

    Get the current GPS date and time combined.

    :return: The GPS date and time as a list of strings [year, month, day, hour, minute, second].

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_timestamp() -->

    Get the timestamp of the current GPS time.

    :return: The timestamp representing the current GPS time.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_latitude() -->

    Get the current latitude.

    :return: The current latitude in string format.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_longitude() -->

    Get the current longitude.

    :return: The current longitude in string format.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_altitude() -->

    Get the current altitude.

    :return: The current altitude in string format.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_satellite_num() -->

    Get the number of satellites used for positioning.

    :return: The number of satellites.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_pos_quality() -->

    Get the quality of the GPS position.

    :return: The position quality indicator.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_corse_over_ground() -->

    Get the course over ground (COG).

    :return: The course over ground in degrees.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_speed_over_ground() -->

    Get the speed over ground (SOG).

    :return: The speed over ground in knots.

    UIFLOW2:

<!-- .. method:: GPSV2Module.set_time_zone(value) -->

    Set the time zone offset for the GPS time.

    :param value: The time zone offset value to set.

    UIFLOW2:

<!-- .. method:: GPSV2Module.get_time_zone() -->

    Get the current time zone offset.

    :return: The current time zone offset.

    UIFLOW2:

<!-- .. method:: GPSV2Module.deinit() -->

    Deinitialize the GPS unit, stopping any running tasks and releasing resources.

    UIFLOW2:

<!-- .. method:: GPSV2Module._add_checksum(message) -->

    Add checksum to the message for communication with the GPS module.

    :param str message: The message to which the checksum will be added.

    :return: The message with added checksum.

<!-- .. method:: GPSV2Module._decode_gga(data) -->

    Decode the GGA sentence to extract GPS quality, number of satellites, and altitude.

    :param str data: The GGA sentence to decode.

<!-- .. method:: GPSV2Module._decode_rmc(data) -->

    Decode the RMC sentence to extract GPS time, latitude, longitude, speed, course, and date.

    :param str data: The RMC sentence to decode.

<!-- .. method:: GPSV2Module._decode_txt(data) -->

    Decode the TXT sentence to extract antenna state.

    :param str data: The TXT sentence to decode.

<!-- .. method:: GPSV2Module._monitor() -->

    Monitor the GPS data and decode incoming sentences.

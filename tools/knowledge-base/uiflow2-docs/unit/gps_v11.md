
# GPS V1.1(SMA) Unit

<!-- .. include:: ../refs/unit.gps_v11.ref -->

GPS Unit v1.1 is a GNSS global positioning navigation unit, integrating the high-performance CASIC navigation chip AT6668 and signal amplifier chip MAX2659, with a built-in ceramic antenna, providing more precise and reliable satellite positioning services.

GPS SMA Unit is a GNSS global positioning navigation unit that integrates the high-performance CASIC navigation chip AT6668 and the signal amplifier chip MAX2659. It uses an external antenna to provide more accurate and reliable satellite positioning services.

Support the following products:

    |GPSV11Unit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import GPSV11Unit
import time

label0 = None
title0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
gpsv11_0 = None

power_on_time = None

def setup():
    global label0, title0, label1, label2, label3, label4, label5, label6, gpsv11_0, power_on_time

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Power On:", 1, 33, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title(
        "GPSV11Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Satellite Num:", 1, 66, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Timestamp:", 1, 202, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("GPS Data:", -6, 526, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Latitude:", 1, 104, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("Longitude:", 1, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("Altitude:", 1, 170, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    gpsv11_0 = GPSV11Unit(2, port=(33, 32))
    gpsv11_0.set_work_mode(7)
    power_on_time = time.time()

def loop():
    global label0, title0, label1, label2, label3, label4, label5, label6, gpsv11_0, power_on_time
    M5.update()
    label0.setText(str((str("Power On:") + str(((time.time()) - power_on_time)))))
    label1.setText(str((str("Satellite Num:") + str((gpsv11_0.get_satellite_num())))))
    label2.setText(str((str("Timestamp:") + str((gpsv11_0.get_timestamp())))))
    label4.setText(str((str("Latitude:") + str((gpsv11_0.get_latitude())))))
    label5.setText(str((str("Longitude:") + str((gpsv11_0.get_longitude())))))
    label6.setText(str((str("Altitude:") + str((gpsv11_0.get_altitude())))))
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

    |gpsv11_core2_example.m5f2|

## class GPSV11Unit

## Constructors

<!-- .. class:: GPSV11Unit(id, port) -->

    Initialize the GPSV11Unit with a specific UART id and port for communication.

    :param int id: The UART ID for communication with the GPS module. It can be 0, 1, or 2.
    :param  port: A list or tuple containing the TX and RX pins for UART communication.

    UIFLOW2:

## Methods

<!-- .. method:: GPSV11Unit.set_work_mode(mode) -->

    Set the working mode of the GPS module.

    :param int mode: The mode to set, defined by the GPS module.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_work_mode() -->

    Get the current working mode of the GPS module.

    :return: The current working mode of the GPS module.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_antenna_state() -->

    Get the state of the antenna.

    :return: The antenna state.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_gps_time() -->

    Get the current GPS time.

    :return: The GPS time as a list of strings [hour, minute, second].

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_gps_date() -->

    Get the current GPS date.

    :return: The GPS date as a list of strings [day, month, year].

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_gps_date_time() -->

    Get the current GPS date and time combined.

    :return: The GPS date and time as a list of strings [year, month, day, hour, minute, second].

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_timestamp() -->

    Get the timestamp of the current GPS time.

    :return: The timestamp representing the current GPS time.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_latitude() -->

    Get the current latitude.

    :return: The current latitude in string format.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_longitude() -->

    Get the current longitude.

    :return: The current longitude in string format.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_altitude() -->

    Get the current altitude.

    :return: The current altitude in string format.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_satellite_num() -->

    Get the number of satellites used for positioning.

    :return: The number of satellites.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_pos_quality() -->

    Get the quality of the GPS position.

    :return: The position quality indicator.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_corse_over_ground() -->

    Get the course over ground (COG).

    :return: The course over ground in degrees.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_speed_over_ground() -->

    Get the speed over ground (SOG).

    :return: The speed over ground in knots.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.set_time_zone(value) -->

    Set the time zone offset for the GPS time.

    :param value: The time zone offset value to set.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.get_time_zone() -->

    Get the current time zone offset.

    :return: The current time zone offset.

    UIFLOW2:

<!-- .. method:: GPSV11Unit.deinit() -->

    Deinitialize the GPS unit, stopping any running tasks and releasing resources.

    UIFLOW2:

<!-- .. method:: GPSV11Unit._add_checksum(message) -->

    Add checksum to the message for communication with the GPS module.

    :param str message: The message to which the checksum will be added.

    :return: The message with added checksum.

<!-- .. method:: GPSV11Unit._decode_gga(data) -->

    Decode the GGA sentence to extract GPS quality, number of satellites, and altitude.

    :param str data: The GGA sentence to decode.

<!-- .. method:: GPSV11Unit._decode_rmc(data) -->

    Decode the RMC sentence to extract GPS time, latitude, longitude, speed, course, and date.

    :param str data: The RMC sentence to decode.

<!-- .. method:: GPSV11Unit._decode_txt(data) -->

    Decode the TXT sentence to extract antenna state.

    :param str data: The TXT sentence to decode.

<!-- .. method:: GPSV11Unit._monitor() -->

    Monitor the GPS data and decode incoming sentences.

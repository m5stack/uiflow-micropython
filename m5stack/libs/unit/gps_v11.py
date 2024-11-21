# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import UART
from driver.timer_thread import TimerThread
import time
import sys

if sys.platform != "esp32":
    from typing import Literal

timTh = TimerThread()


class GPSV11Unit:
    """
    note:
        en: GPS Unit v1.1 is a GNSS global positioning navigation unit, integrating the high-performance CASIC navigation chip AT6668 and signal amplifier chip MAX2659, with a built-in ceramic antenna, providing more precise and reliable satellite positioning services.
        link: https://docs.m5stack.com/en/unit/Unit-GPS%20v1.1
        image: https://m5stack.oss-cn-shenzhen.aliyuncs.com/resource/docs/products/unit/Unit-GPS%20v1.1/4.webp
        category: Unit

    example:
        - ../../../examples/unit/gps_example.py

    m5f2:
        - unit/gps_example.m5f2
    """

    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None):
        """
        note:
            en: Initialize the GPSUnit with a specific UART id and port for communication.

        params:
            id:
                note: The UART ID for communication with the GPS module. It can be 0, 1, or 2.
            port:
                note: A list or tuple containing the TX and RX pins for UART communication.
        """
        self.mode = 0
        self.antenna_state = "0"
        self.gps_time = ["00", "00", "00"]
        self.gps_date = ["00", "00", "00"]
        self.gps_date_time = ["00", "00", "00", "00", "00", "00"]
        self.timestamp = 0
        self.latitude = "0N"
        self.longitude = "0E"
        self.altitude = "0"
        self.satellite_num = "0"
        self.pos_quality = "0"
        self.corse_ground_degree = "0"
        self.speed_ground_knot = "0"
        self.time_offset = 0
        self.uart = UART(id, tx=port[1], rx=port[0])
        self.uart.init(115200, bits=8, parity=None, stop=1, rxbuf=1024)
        self._timer = timTh.add_timer(200, timTh.PERIODIC, self._monitor)
        self.set_work_mode(7)

    def set_work_mode(self, mode: int):
        """
        note:
            en: Set the working mode of the GPS module.

        params:
            mode:
                note: The mode to set, defined by the GPS module.
        """
        self.mode = mode
        buf = self._add_checksum(f"PCAS04,{mode}")
        self.uart.write(buf.encode())

    def get_work_mode(self):
        """
        note:
            en: Get the current working mode of the GPS module.

        return:
            note: The current working mode of the GPS module.
        """
        return self.mode

    def get_antenna_state(self) -> str:
        """
        note:
            en: Get the state of the antenna.

        return:
            note: The antenna state.
        """
        return self.antenna_state

    def get_gps_time(self):
        """
        note:
            en: Get the current GPS time.

        return:
            note: The GPS time as a list of strings [hour, minute, second].
        """
        return self.gps_time

    def get_gps_date(self):
        """
        note:
            en: Get the current GPS date.

        return:
            note: The GPS date as a list of strings [day, month, year].
        """
        return self.gps_date

    def get_gps_date_time(self):
        """
        note:
            en: Get the current GPS date and time combined.

        return:
            note: The GPS date and time as a list of strings [year, month, day, hour, minute, second].
        """
        return self.gps_date_time

    def get_timestamp(self) -> int | float:
        """
        note:
            en: Get the timestamp of the current GPS time.

        return:
            note: The timestamp representing the current GPS time.
        """
        return self.timestamp

    def get_latitude(self):
        """
        note:
            en: Get the current latitude.

        return:
            note: The current latitude in string format.
        """
        return self.latitude

    def get_longitude(self):
        """
        note:
            en: Get the current longitude.

        return:
            note: The current longitude in string format.
        """
        return self.longitude

    def get_altitude(self):
        """
        note:
            en: Get the current altitude.

        return:
            note: The current altitude in string format.
        """
        return self.altitude

    def get_satellite_num(self):
        """
        note:
            en: Get the number of satellites used for positioning.

        return:
            note: The number of satellites.
        """
        return self.satellite_num

    def get_pos_quality(self):
        """
        note:
            en: Get the quality of the GPS position.

        return:
            note: The position quality indicator.
        """
        return self.pos_quality

    def get_corse_over_ground(self) -> str:
        """
        note:
            en: Get the course over ground (COG).

        return:
            note: The course over ground in degrees.
        """
        return self.corse_ground_degree

    def get_speed_over_ground(self) -> str:
        """
        note:
            en: Get the speed over ground (SOG).

        return:
            note: The speed over ground in knots.
        """
        return self.speed_ground_knot

    def set_time_zone(self, value):
        """
        note:
            en: Set the time zone offset for the GPS time.

        params:
            value:
                note: The time zone offset value to set.
        """
        self.time_offset = value

    def get_time_zone(self):
        """
        note:
            en: Get the current time zone offset.

        return:
            note: The current time zone offset.
        """
        return self.time_offset

    def deinit(self):
        """
        note:
            en: Deinitialize the GPS unit, stopping any running tasks and releasing resources.
        """
        self._timer.deinit()
        try:
            self.uart.deinit()
        except:
            pass

    def _add_checksum(self, message: str) -> str:
        """
        note:
            en: Add checksum to the message for communication with the GPS module.

        params:
            message:
                note: The message to which the checksum will be added.

        return:
            note: The message with added checksum.
        """
        checksum = 0
        for char in message:
            checksum ^= ord(char)
        return f"${message}*{checksum:02X}\r\n"

    def _decode_gga(self, data: str):
        """
        note:
            en: Decode the GGA sentence to extract GPS quality, number of satellites, and altitude.

        params:
            data:
                note: The GGA sentence to decode.
        """
        gps_list = data.split(",")
        self.pos_quality = gps_list[6]
        if self.pos_quality == "0":
            return
        self.satellite_num = gps_list[7]
        if gps_list[9]:
            self.altitude = gps_list[9] + gps_list[10]

    def _decode_rmc(self, data: str):
        """
        note:
            en: Decode the RMC sentence to extract GPS time, latitude, longitude, speed, course, and date.

        params:
            data:
                note: The RMC sentence to decode.
        """
        gps_list = data.split(",")
        if gps_list[2] == "A":
            time_buf = gps_list[1]
            self.gps_time = [
                int(time_buf[0:2]) + self.time_offset,
                int(time_buf[2:4]),
                int(time_buf[4:6]),
            ]
            self.latitude = gps_list[3] + gps_list[4]
            self.longitude = gps_list[5] + gps_list[6]
            self.speed_ground_knot = gps_list[7]
            self.corse_ground_degree = gps_list[8]
            data_buf = gps_list[9]
            self.gps_date = [int(data_buf[4:7]) + 2000, int(data_buf[2:4]), int(data_buf[0:2])]
            t = (
                self.gps_date[0],
                self.gps_date[1],
                self.gps_date[2],
                self.gps_time[0] - self.time_offset,
                self.gps_time[1],
                self.gps_time[2],
                0,
                0,
            )
            self.gps_date_time = self.gps_date + self.gps_time
            buf = time.mktime(t)
            self.timestamp = buf

    def _decode_txt(self, data: str):
        """
        note:
            en: Decode the TXT sentence to extract antenna state.

        params:
            data:
                note: The TXT sentence to decode.
        """
        gps_list = data.split(",")
        if gps_list[4] is not None and gps_list[4][0:7] == "ANTENNA":
            self.antenna_state = gps_list[4][8:].split("*")[0]

    def _monitor(self):
        """
        note:
            en: Monitor the GPS data and decode incoming sentences.
        """
        while True:
            if self.uart.any() < 25:
                break

            gps_data = self.uart.readline()
            if gps_data is not None:
                if gps_data[3:6] == b"GGA" and gps_data[-1] == b"\n"[0]:
                    self._decode_gga(gps_data.decode())
                elif gps_data[3:6] == b"RMC" and gps_data[-1] == b"\n"[0]:
                    self._decode_rmc(gps_data.decode())
                elif gps_data[3:6] == b"TXT" and gps_data[-1] == b"\n"[0]:
                    self._decode_txt(gps_data.decode())

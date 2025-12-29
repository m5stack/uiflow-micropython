# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import UART
from machine import Pin
from driver.timer_thread import TimerThread
import time
import sys

if sys.platform != "esp32":
    from typing import Literal

timTh = TimerThread()


class ATGM336H:
    """
    Create an ATGM336H object.

    :param int id: The UART ID for communication with the GPS module. It can be 1, or 2.
    :param int tx: The TX pin is the pin that sends data to the GPS module.
    :param int rx: The RX pin is the pin that receives data from the GPS module.
    :param int pps: The PPS pin is the pin that receives the PPS signal from the GPS module.
    :param bool verbose: Whether to print verbose output.

    MicroPython Code Block:

        .. code-block:: python

            from driver.atgm336h import ATGM336H

            gps_0 = ATGM336H(id=2, tx=5, rx=6)
    """

    def __init__(self, id: Literal[0, 1, 2], tx: int, rx: int, pps=None, rst=None, verbose=False):
        self.mode = 0
        self.antenna_state = "0"
        self.utc_time = ["00", "00", "00"]
        self.utc_date = ["00", "00", "00"]
        self.utc_date_time = ["00", "00", "00", "00", "00", "00"]
        self.timestamp = 0
        self.latitude = "0N"
        self.longitude = "0E"
        self.altitude = "0"
        self.satellite_num = "0"
        self.pos_quality = "0"
        self.course_ground_degree = "0"
        self.speed_ground_knot = "0"
        self.time_offset = 0
        self.local_dt = ["00", "00", "00", "00", "00", "00"]
        self.verbose = verbose
        self.rst = rst
        if self.rst:
            print(self.rst)
            self.rst = Pin(self.rst, Pin.OUT)
            self.rst.value(1)
            time.sleep(1)
            self.rst.value(0)
        self.uart = UART(id, tx=tx, rx=rx)
        self.uart.init(115200, bits=8, parity=None, stop=1, rxbuf=1024)
        self._timer = timTh.add_timer(200, timTh.PERIODIC, self._monitor)
        self.set_work_mode(7)

    def set_work_mode(self, mode: int):
        """
        Set the working mode of the GPS module.

        :param int mode: The mode to set, defined by the GPS module.

        UiFlow2 Code Block:

            |set_work_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.set_work_mode(7)
        """
        self.mode = mode
        buf = self._add_checksum(f"PCAS04,{mode}")
        self.uart.write(buf.encode())

    def get_work_mode(self):
        """
        Get the current working mode of the GPS module.

        :returns: The current working mode of the GPS module.
        :rtype: int

        UiFlow2 Code Block:

            |get_work_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_work_mode()
        """
        return self.mode

    def get_antenna_state(self) -> str:
        """
        Get the state of the antenna.

        :returns: The antenna state.
        :rtype: str

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_antenna_state()
        """
        return self.antenna_state

    def get_gps_time(self):
        """
        Get the current GPS time.

        :returns: The GPS time as a list of strings [hour, minute, second].
        :rtype: list[str]

        UiFlow2 Code Block:

            |get_gps_time.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_gps_time()
        """
        return self.local_dt[3:6]

    def get_gps_date(self):
        """
        Get the current GPS date.

        :returns: The GPS date as a list of strings [year, month, day].
        :rtype: list[str]

        UiFlow2 Code Block:

            |get_gps_date.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_gps_date()
        """
        return self.local_dt[0:3]

    def get_gps_date_time(self):
        """
        Get the current GPS date and time combined.

        :returns: The GPS date and time as a list of strings [year, month, day, hour, minute, second].
        :rtype: list[str]

        UiFlow2 Code Block:

            |get_gps_date_time.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_gps_date_time()
        """
        return self.get_gps_date() + self.get_gps_time()

    def get_timestamp(self) -> int | float:
        """
        Get the timestamp of the current GPS time.

        :returns: The timestamp representing the current GPS time.
        :rtype: int | float

        UiFlow2 Code Block:

            |get_timestamp.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_timestamp()
        """
        return self.timestamp

    def get_latitude(self):
        """
        Get the current latitude.

        :returns: The current latitude in string format.
        :rtype: str

        UiFlow2 Code Block:

            |get_latitude.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_latitude()
        """
        return self.latitude

    def get_longitude(self):
        """
        Get the current longitude.

        :returns: The current longitude in string format.
        :rtype: str

        UiFlow2 Code Block:

            |get_longitude.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_longitude()
        """
        return self.longitude

    def get_altitude(self):
        """
        Get the current altitude.

        :returns: The current altitude in string format.
        :rtype: str

        UiFlow2 Code Block:

            |get_altitude.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_altitude()
        """
        return self.altitude

    def get_satellite_num(self):
        """
        Get the number of satellites used for positioning.

        :returns: The number of satellites.
        :rtype: str

        UiFlow2 Code Block:

            |get_satellite_num.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_satellite_num()
        """
        return self.satellite_num

    def get_pos_quality(self):
        """
        Get the quality of the GPS position.

        :returns: The position quality indicator.
        :rtype: str

        UiFlow2 Code Block:

            |get_pos_quality.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_pos_quality()
        """
        return self.pos_quality

    def get_corse_over_ground(self) -> str:
        return self.get_course_over_ground()

    def get_course_over_ground(self) -> str:
        """
        Get the course over ground (COG).

        Note: Only data returned by the satellite is extracted. If the data does not display properly, it indicates that the satellite did not actually return that data.

        :returns: The course over ground in degrees.
        :rtype: str

        UiFlow2 Code Block:

            |get_course_over_ground.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_course_over_ground()
        """
        return self.course_ground_degree

    def get_speed_over_ground(self) -> str:
        """
        Get the speed over ground (SOG).

        :returns: The speed over ground in knots.
        :rtype: str

        UiFlow2 Code Block:

            |get_speed_over_ground.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_speed_over_ground()
        """
        return self.speed_ground_knot

    def set_time_zone(self, value):
        """
        Set the time zone offset for the GPS time.

        :param int value: The time zone offset value to set.

        UiFlow2 Code Block:

            |set_time_zone.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.set_time_zone(1)
        """
        self.time_offset = value

    def get_time_zone(self):
        """
        Get the current time zone offset.

        :returns: The current time zone offset.
        :rtype: int

        UiFlow2 Code Block:

            |get_time_zone.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.get_time_zone()
        """
        return self.time_offset

    def deinit(self):
        """
        Deinitialize the GPS unit, stopping any running tasks and releasing resources.

        UiFlow2 Code Block:

            |deinit.png|

        MicroPython Code Block:

            .. code-block:: python

                gps_0.deinit()
        """
        self._timer.deinit()
        try:
            self.uart.deinit()
        except:
            pass

    def _add_checksum(self, message: str) -> str:
        checksum = 0
        for char in message:
            checksum ^= ord(char)
        return f"${message}*{checksum:02X}\r\n"

    def _decode_gga(self, data: str):
        gps_list = data.split(",")
        self.pos_quality = gps_list[6]
        self.satellite_num = gps_list[7]
        if gps_list[9]:
            self.altitude = gps_list[9] + gps_list[10]

    def _decode_rmc(self, data: str):
        gps_list = data.split(",")
        if gps_list[2] == "A":
            time_buf = gps_list[1]
            self.utc_time = [
                int(time_buf[0:2]),
                int(time_buf[2:4]),
                int(time_buf[4:6]),
            ]
            self.latitude = self._convert_to_decimal(gps_list[3], gps_list[4])
            self.longitude = self._convert_to_decimal(gps_list[5], gps_list[6], False)
            self.speed_ground_knot = gps_list[7]
            self.course_ground_degree = gps_list[8]
            data_buf = gps_list[9]
            self.utc_date = [int(data_buf[4:7]) + 2000, int(data_buf[2:4]), int(data_buf[0:2])]
            t = (
                self.utc_date[0],
                self.utc_date[1],
                self.utc_date[2],
                self.utc_time[0],
                self.utc_time[1],
                self.utc_time[2],
                0,
                0,
            )
            self.utc_date_time = self.utc_date + self.utc_time
            self.timestamp = time.mktime(t)
            self.local_dt = time.localtime(self.timestamp + self.time_offset * 3600)

    def _convert_to_decimal(self, degrees_minutes, direction, latitude: bool = True) -> float:
        if latitude:
            degrees = degrees_minutes[:2]  # First two digits are degrees
            minutes = degrees_minutes[2:]  # The rest are minutes
        else:
            degrees = degrees_minutes[:3]
            minutes = degrees_minutes[3:]
        decimal = int(degrees) + round(float(minutes) / 60.0, 6)
        if direction in ["S", "W"]:
            decimal = -decimal
        return decimal

    def _decode_txt(self, data: str):
        gps_list = data.split(",")
        if gps_list[4] is not None and gps_list[4][0:7] == "ANTENNA":
            self.antenna_state = gps_list[4][8:].split("*")[0]

    def _monitor(self):
        while True:
            if self.uart.any() < 25:
                break

            gps_data = self.uart.readline()
            self.verbose and print(gps_data)
            if gps_data is not None and isinstance(gps_data, bytes):
                if gps_data[3:6] == b"GGA" and gps_data[-1] == b"\n"[0]:
                    self._decode_gga(gps_data.decode())
                elif gps_data[3:6] == b"RMC" and gps_data[-1] == b"\n"[0]:
                    self._decode_rmc(gps_data.decode())
                elif gps_data[3:6] == b"TXT" and gps_data[-1] == b"\n"[0]:
                    self._decode_txt(gps_data.decode())

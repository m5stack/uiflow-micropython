# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import UART
import time
from driver.timer_thread import TimerThread
import sys

if sys.platform != "esp32":
    from typing import Literal

timTh = TimerThread()


class ATOMGPSBase:
    """Create an ATOMGPSBase object.

    :param int id: The UART ID to use (0, 1, or 2). Default is 2.
    :param port: A list or tuple containing the TX and RX pin numbers.
    :type port: list | tuple
    :param bool debug: Whether to enable debug mode. Default is False.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from machine import UART
            from base import ATOMGPSBase

            gps = ATOMGPSBase(id=1, port=(16, 17))
    """

    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None, debug=False):
        self.debug = debug
        self.antenna_state = "ANTENNA OPEN"
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
        self.uart.init(9600, bits=8, parity=None, stop=1, rxbuf=1024)
        self._timer = timTh.add_timer(200, timTh.PERIODIC, self._monitor)
        print("debug", self.debug)

    def get_antenna_state(self) -> str:
        """Get the state of the antenna.

        :returns: The current antenna state.
        :rtype: str

        UiFlow2 Code Block:

            |get_antenna_state.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_antenna_state()
        """
        return self.antenna_state

    def get_gps_time(self) -> list[str]:
        """Get the current GPS time.

        :returns: The GPS time as a list of strings [hour, minute, second].
        :rtype: list[str]

        UiFlow2 Code Block:

            |get_gps_time.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_gps_time()
        """
        return self.gps_time

    def get_gps_date(self) -> list[str]:
        """Get the current GPS date.

        :returns: The GPS date as a list of strings [day, month, year].
        :rtype: list[str]

        UiFlow2 Code Block:

            |get_gps_date.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_gps_date()
        """
        return self.gps_date

    def get_gps_date_time(self) -> list[str]:
        """Get the current GPS date and time combined.

        :returns: The GPS date and time as a list of strings [year, month, day, hour, minute, second].
        :rtype: list[str]

        UiFlow2 Code Block:

            |get_gps_date_time.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_gps_date_time()
        """
        return self.gps_date_time

    def get_timestamp(self) -> int | float:
        """Get the timestamp of the current GPS time.

        :returns: The timestamp representing the current GPS time.
        :rtype: int | float

        UiFlow2 Code Block:

            |get_timestamp.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_timestamp()
        """
        return self.timestamp

    def get_latitude(self) -> str:
        """Get the current latitude.

        :returns: The current latitude.
        :rtype: str

        UiFlow2 Code Block:

            |get_latitude.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_latitude()
        """
        return self.latitude

    def get_longitude(self) -> str:
        """Get the current longitude.

        :returns: The current longitude.
        :rtype: str

        UiFlow2 Code Block:

            |get_longitude.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_longitude()
        """
        return self.longitude

    def get_altitude(self) -> str:
        """Get the current altitude.

        :returns: The current altitude.
        :rtype: str

        UiFlow2 Code Block:

            |get_altitude.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_altitude()
        """
        return self.altitude

    def get_satellite_num(self) -> str:
        """Get the number of satellites used for positioning.

        :returns: The number of satellites.
        :rtype: str

        UiFlow2 Code Block:

            |get_satellite_num.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_satellite_num()
        """
        return self.satellite_num

    def get_pos_quality(self) -> str:
        """Get the quality of the GPS position.

        :returns: The position quality indicator.
        :rtype: str

        UiFlow2 Code Block:

            |get_pos_quality.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_pos_quality()
        """
        return self.pos_quality

    def get_corse_over_ground(self) -> str:
        """Get the course over ground (COG).

        :returns: The course over ground in degrees.
        :rtype: str

        UiFlow2 Code Block:

            |get_corse_over_ground.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_corse_over_ground()
        """
        return self.corse_ground_degree

    def get_speed_over_ground(self) -> str:
        """Get the speed over ground (SOG).

        :returns: The speed over ground in knots.
        :rtype: str

        UiFlow2 Code Block:

            |get_speed_over_ground.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_speed_over_ground()
        """
        return self.speed_ground_knot

    def set_time_zone(self, value: int) -> None:
        """Set the time zone offset for the GPS time.

        :param int value: The time zone offset value to set.

        UiFlow2 Code Block:

            |set_time_zone.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.set_time_zone(8)
        """
        self.time_offset = value

    def get_time_zone(self) -> int:
        """Get the current time zone offset.

        :returns: The current time zone offset.
        :rtype: int

        UiFlow2 Code Block:

            |get_time_zone.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.get_time_zone()
        """
        return self.time_offset

    def deinit(self) -> None:
        """Deinitialize the GPS unit, stopping any running tasks and releasing resources.

        UiFlow2 Code Block:

            |deinit.png|

        MicroPython Code Block:

            .. code-block:: python

                gps.deinit()
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
            self.latitude = self._convert_to_decimal(gps_list[3], gps_list[4])
            self.longitude = self._convert_to_decimal(gps_list[5], gps_list[6], False)
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

    def _convert_to_decimal(self, degrees_minutes, direction, latitude: bool = True) -> float:
        """
        note:
            en: Convert latitude or longitude from degrees minutes format to decimal format.

        params:
            degrees_minutes:
                note: Latitude or Longitude in DDMM.MMMM format (e.g., "2242.10772").
            direction:
                note: Direction of the coordinate ("N", "S", "E", "W").
            latitude:
                note: True if latitude, False if longitude.

        returns:
            note: The decimal value of the coordinate.
        """
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
            if self.debug:
                print(f"gps_data: {gps_data}")
            if gps_data is not None and isinstance(gps_data, bytes):
                if gps_data[3:6] == b"GGA" and gps_data[-1] == b"\n"[0]:
                    self._decode_gga(gps_data.decode())
                elif gps_data[3:6] == b"RMC" and gps_data[-1] == b"\n"[0]:
                    self._decode_rmc(gps_data.decode())
                elif gps_data[3:6] == b"TXT" and gps_data[-1] == b"\n"[0]:
                    self._decode_txt(gps_data.decode())

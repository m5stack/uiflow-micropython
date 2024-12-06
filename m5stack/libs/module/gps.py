# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import machine
from driver.timer_thread import TimerThread
import sys

if sys.platform != "esp32":
    from typing import Literal

_timTh = TimerThread()


class GPSModule:
    """

    note:
        en: COM.GPS is a satellite positioning module in the M5Stack stacking module series. It is developed based on the NEO-M8N module.
        cn: COM.GPS 是M5Stack堆叠模块系列中的一款,卫星定位模块.基于NEO-M8N模组开发。

    details:
        color: "#0f2fe6"
        link: https://docs.m5stack.com/en/module/comx_gps
        image: https://static-cdn.m5stack.com/resource/docs/products/module/comx_gps/comx_gps_03.webp
        category: module

    """

    def __init__(self, id: Literal[0, 1, 2] = 1, rx: int = 13, tx: int = 14) -> None:
        """
        note:
            en: initialize Function.
        label:
            en: 'Init %1 with UART %2 RX: %3 TX: %4'
        params:
            id:
                name: id
                type: int
                default: '1'
                note:
                    en: UART controllers id, the range is 0 to 2.
                field: slider
                step: '1'
                min: '0'
                max: '2'
                precision: '1'
            rx:
                name: rx
                type: int
                default: '13'
                note:
                    en: UART rx pin.
            tx:
                name: tx
                type: int
                default: '14'
                note:
                    en: UART tx pin.
        """
        self.uart_data = ""
        self.gps_time = "00:00:00"
        self.gps_date = "01/01/20"
        self.latitude = "0000.00000N"
        self.longitude = "0000.00000E"
        self.altitude = "0"
        self.latitude_decimal = 0
        self.longitude_decimal = 0
        self.satellite_num = "0"
        self.pos_quality = "0"
        self.speed_knot = "0.0"
        self.speed_kph = "0.0"
        self.course = "0.0"
        self.locate_status = False
        self.uart = machine.UART(id, tx=tx, rx=rx)
        self.uart.init(9600, bits=0, parity=None, stop=1, rxbuf=1024)
        self.tx = tx
        self.rx = rx
        self._timer = _timTh.add_timer(50, _timTh.PERIODIC, self._monitor)
        self._state = ""
        self.time_offset = 8

    def set_time_zone(self, value: int) -> None:
        """
        note:
            en: set timezone function.
        label:
            en: Set %1 timezone %2
        params:
            value:
                name: value
                type: int
                default: '8'
                note:
                    en: timezone value
                field: number
        """
        self.time_offset = value

    def get_time_zone(self) -> int:
        """
        note:
            en: get timezone function.
        label:
            en: Get %1 timezone (return int)

        return:
            note: timezone value
        """
        return self.time_offset

    def get_satellite_num(self) -> str:
        """
        note:
            en: get satellite numbers.
        label:
            en: Get %1 satellite numbers (return string)

        return:
            note: satellite numbers value.
        """
        return self.satellite_num

    def get_altitude(self) -> str:
        """
        note:
            en: get altitude.
        label:
            en: Get %1 altitude (return string, unit is meter)

        return:
            note: altitude unit is meter.
        """
        return self.altitude

    def get_time(self) -> str:
        """
        note:
            en: get time.
        label:
            en: Get %1 time (return string, format is hh:mm:ss)

        return:
            note: time(hh:mm:ss)
        """
        return self.gps_time

    def get_date(self) -> str:
        """
        note:
            en: get date.
        label:
            en: Get %1 date (return string, format is dd/mm/yy)

        return:
            note: date(dd/mm/yy)
        """
        return self.gps_date

    def get_latitude(self) -> str:
        """
        note:
            en: get latitude.
        label:
            en: Get %1 latitude (return string, format is ddmm.mmmmmN/S)

        return:
            note: latitude, using degrees minutes format (ddmm.mmmmmN/S).
        """
        return self.latitude

    def get_longitude(self) -> str:
        """
        note:
            en: get longitude.
        label:
            en: Get %1 longitude (return string, format is ddmm.mmmmmE/W)

        return:
            note: longitude, using degrees minutes format (ddmm.mmmmmE/W).
        """
        return self.longitude

    def get_latitude_decimal(self) -> float:
        """
        note:
            en: get latitude decimal.
        label:
            en: Get %1 latitude decimal (return float, format is dd.dddd)

        return:
            note: latitude decimal(dd.dddd).
        """
        return self.latitude_decimal

    def get_longitude_decimal(self) -> float:
        """
        note:
            en: get longitude decimal.
        label:
            en: Get %1 longitude decimal (return float, format is dd.dddd)

        return:
            note: longitude decimal(dd.dddd).
        """
        return self.longitude

    def get_speed(self, type=0) -> str:
        """
        note:
            en: get speed.
        label:
            en: Get %1 speed %2(return string)
        params:
            type:
                name: type
                note:
                    en: speed type, 0 km/h, 1 knot/h
                field: dropdown
                options:
                    km/h: '0'
                    knot/h: '1'

        return:
            note: speed.
        """
        if type == 0:
            return self.speed_kph
        else:
            return self.speed_knot

    def get_course(self) -> str:
        """
        note:
            en: get course.
        label:
            en: Get %1 course (return string, 0 to 360 degree)

        return:
            note: course unit is °.
        """
        return self.course

    def is_locate_valid(self) -> bool:
        """
        note:
            en: get locate status.
        label:
            en: Get %1 locate status (return True or False)

        return:
            note: locate status, true is locate, false is not locate.
        """
        return self.locate_status

    def _decode_gga(self, data) -> None:
        gps_list = data.split(",")
        self.uart_data = data
        self.pos_quality = gps_list[6]

        self.satellite_num = gps_list[7]
        if gps_list[1]:
            now_time = gps_list[1]
            gps_hour = int(now_time[:2]) + self.time_offset
            if gps_hour > 23:
                gps_hour = gps_hour - 24
            if gps_hour < 0:
                gps_hour = gps_hour + 24
            self.gps_time = "{:0>2d}".format(gps_hour) + ":" + now_time[2:4] + ":" + now_time[4:6]

        if self.pos_quality == "0":
            return

        # b'$GNGGA,024423.000,2242.10772,N,11348.64472,E,1,14,1.2,52.1,M,0.0,M,,*48\r\n'
        if gps_list[2]:
            self.latitude = gps_list[2]
            if gps_list[3]:
                self.latitude = self.latitude + gps_list[3]
            degree = gps_list[2][0 : gps_list[2].find(".") - 2]
            minute = gps_list[2][gps_list[2].find(".") - 2 :]
            self.latitude_decimal = self._convert_to_decimal(degree, minute, gps_list[3])
        if gps_list[4]:
            self.longitude = gps_list[4]
            if gps_list[5]:
                self.longitude = self.longitude + gps_list[5]
            degree = gps_list[4][0 : gps_list[4].find(".") - 2]
            minute = gps_list[4][gps_list[4].find(".") - 2 :]
            self.longitude_decimal = self._convert_to_decimal(degree, minute, gps_list[5])
        if gps_list[9]:
            self.altitude = gps_list[9]

    def _convert_to_decimal(self, degrees, minutes, direction) -> float:
        decimal = int(degrees) + round(float(minutes) / 60.0, 6)
        if direction in ["S", "W"]:
            decimal = -decimal
        return decimal

    def _decode_rmc(self, data) -> None:
        gps_list = data.split(",")
        if gps_list[9]:
            now_date = gps_list[9]
            self.gps_date = now_date[:2] + "/" + now_date[2:4] + "/" + now_date[4:6]
        if gps_list[2] == "A":
            self.locate_status = True
        else:
            self.locate_status = False

    def _decode_vtg(self, data) -> None:
        gps_list = data.split(",")
        # self.uart_data = data
        if gps_list[1]:
            self.course = gps_list[1]
        if gps_list[5]:
            self.speed_knot = gps_list[5]
        if gps_list[7]:
            self.speed_kph = gps_list[7]

    def _monitor(self) -> None:
        while True:
            if self.uart.any() < 25:
                break

            gps_data = self.uart.readline()
            gps_data_mem = memoryview(gps_data)

            if gps_data_mem[0:6] == "$GNGGA" and gps_data_mem[-1] == b"\n"[0]:
                self._decode_gga(gps_data.decode())
            elif gps_data_mem[0:6] == "$GNVTG" and gps_data_mem[-1] == b"\n"[0]:
                self._decode_vtg(gps_data.decode())
            elif gps_data_mem[0:6] == "$GNRMC" and gps_data_mem[-1] == b"\n"[0]:
                self._decode_rmc(gps_data.decode())

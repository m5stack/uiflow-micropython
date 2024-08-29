# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import UART
from driver.timer_thread import TimerThread
import sys

if sys.platform != "esp32":
    from typing import Literal

timTh = TimerThread()


class GPSUnit:
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None):
        self.uart_data = ""
        self.gps_time = "00:00:00"
        self.gps_date = "01/01/20"
        self.latitude = "0N"
        self.longitude = "0E"
        self.altitude = "0"
        self.latitude_decimal = 0
        self.longitude_decimal = 0
        self.satellite_num = "0"
        self.pos_quality = "0"
        self.speed_knot = "0.0"
        self.speed_kph = "0.0"
        self.course = "0.0"
        self.uart = UART(id, tx=port[1], rx=port[0])
        self.uart.init(9600, bits=0, parity=None, stop=1, rxbuf=1024)
        self.tx = port[1]
        self.rx = port[0]
        self._timer = timTh.add_timer(50, timTh.PERIODIC, self._monitor)
        self._state = ""
        self.time_offset = 8

    def uart_port_id(self, id_num):
        self.uart = UART(id_num, tx=self.tx, rx=self.rx)
        self.uart.init(9600, bits=0, parity=None, stop=1, rxbuf=1024)

    def set_time_zone(self, value):
        self.time_offset = value

    def decode_gga(self, data):
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
            self.latitude_decimal = self.convert_to_decimal(degree, minute, gps_list[3])
        if gps_list[4]:
            self.longitude = gps_list[4]
            if gps_list[5]:
                self.longitude = self.longitude + gps_list[5]
            degree = gps_list[4][0 : gps_list[4].find(".") - 2]
            minute = gps_list[4][gps_list[4].find(".") - 2 :]
            self.longitude_decimal = self.convert_to_decimal(degree, minute, gps_list[5])
        if gps_list[9]:
            self.altitude = gps_list[9]

    def convert_to_decimal(degrees, minutes, direction) -> float:
        decimal = int(degrees) + round(float(minutes) / 60.0, 6)
        if direction in ["S", "W"]:
            decimal = -decimal
        return decimal

    def decode_rmc(self, data):
        gps_list = data.split(",")
        # self.uart_data = data
        if gps_list[9]:
            now_date = gps_list[9]
            self.gps_date = now_date[:2] + "/" + now_date[2:4] + "/" + now_date[4:6]

    def decode_vtg(self, data):
        gps_list = data.split(",")
        # self.uart_data = data
        if gps_list[1]:
            self.course = gps_list[1]
        if gps_list[5]:
            self.speed_knot = gps_list[5]
        if gps_list[7]:
            self.speed_kph = gps_list[7]

    def _monitor(self):
        while True:
            if self.uart.any() < 25:
                break

            gps_data = self.uart.readline()
            gps_data_mem = memoryview(gps_data)

            if gps_data_mem[0:6] == "$GNGGA" and gps_data_mem[-1] == b"\n"[0]:
                self.decode_gga(gps_data.decode())
            elif gps_data_mem[0:6] == "$GNVTG" and gps_data_mem[-1] == b"\n"[0]:
                self.decode_vtg(gps_data.decode())
            elif gps_data_mem[0:6] == "$GNRMC" and gps_data_mem[-1] == b"\n"[0]:
                self.decode_rmc(gps_data.decode())

    def deinit(self):
        self._timer.deinit()
        try:
            self.uart.deinit()
        except:
            pass

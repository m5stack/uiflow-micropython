# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import machine
from .mbus import i2c1
from .module_helper import ModuleError
from driver.bmi270_bmm150 import BMI270_BMM150
from driver.bmp280 import BMP280
from driver.timer_thread import TimerThread
import sys
import math
import time

if sys.platform != "esp32":
    from typing import Literal

_timTh = TimerThread()

_BMI270_ADDR = 0x69

# Constants for unit conversion
_SF_G = 1
_SF_M_S2 = 9.80665  # Standard gravity, 1 g = 9.80665 m/s²
_SF_DEG_S = 1
_SF_RAD_S = 57.295779513082  # Radian to degree conversion factor, 1 rad/s = 57.295779578552 deg/s


class GNSSModule(BMI270_BMM150, BMP280):
    """

    note:
        en: GNSS Module is a global positioning wireless communication module featuring the NEO-M9N-00B GPS module. It incorporates BMI270, BMM150 and a barometric pressure sensor.
        cn: GNSS Module是一款多功能全球定位通信模块, 内置NEO-M9N-OOB高精度GNSS定位模组, 同时集成六轴姿态传感器BMI270、三轴地磁计BMM150和气压传感器。

    details:
        color: "#e60f4c"
        link: https://docs.m5stack.com/en/module/GNSS%20Module
        image: https://static-cdn.m5stack.com/resource/docs/products/module/GNSS%20Module/img-b0cdbc6c-d5d5-42bb-bdf6-69016e003b14.webp
        category: module

    """

    def __init__(
        self, id: Literal[0, 1, 2] = 1, rx: int = 13, tx: int = 14, address: int = _BMI270_ADDR
    ) -> None:
        """
        note:
            en: initialize Function.
        label:
            en: 'Init %1 with UART %2 RX: %3 TX: %4 BMI270 I2C address %5'
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
            address:
                name: address
                field: dropdown
                options:
                    '0x69': '0x69'
                    '0x68': '0x68'
        """
        self._i2c = i2c1
        self._addr = address
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
        self.uart.init(38400, bits=0, parity=None, stop=1, rxbuf=1024)
        self.tx = tx
        self.rx = rx
        self._timer = _timTh.add_timer(50, _timTh.PERIODIC, self._monitor)
        self._state = ""
        self.time_offset = 8

        # Check if the devices are connected and accessible
        if address not in self._i2c.scan():
            raise ModuleError(
                "GNSS module maybe not connect or the address not set to 0x%x" % (self._addr)
            )

        BMI270_BMM150.__init__(self, self._i2c, bmi270_address=self._addr)
        BMP280.__init__(self, self._i2c)

        # for attitude computing
        self.accCoef = 0.02
        self.gyroCoef = 0.98
        self.angleGyroX = 0
        self.angleGyroY = 0
        self.angleGyroZ = 0
        self.angleX = 0
        self.angleZ = 0
        self.angleY = 0
        self.gyroXoffset = 0
        self.gyroYoffset = 0
        self.gyroZoffset = 0
        self.preInterval = time.ticks_us()

    def _available(self):
        print(self._i2c.scan())
        if self._addr not in self._i2c.scan():
            raise ModuleError("GNSS module maybe not connect")

    def set_accel_gyro_odr(self, accel_odr, gyro_odr) -> None:
        """
        note:
            en: Set the accelerometer and gyroscope output data rate.
        label:
            en: Set %1 accelerometer ODR (Hz) %2 gyroscrope ODR (Hz) %3
        params:
            accel_odr:
                name: accel_odr
                note:
                    en: range of 0.78 Hz … 1.6 kHz.
                field: dropdown
                options:
                    '0.78': '0.78'
                    '1.5': '1.5'
                    '3.1': '3.1'
                    '6.25': '6.25'
                    '12.5': '12.5'
                    '25': '25'
                    '50': '50'
                    '100': '100'
                    '200': '200'
                    '400': '400'
                    '800': '800'
                    '1600': '1600'
            gyro_odr:
                name: gyro_odr
                note:
                    en: range of 25 Hz … 6.4 kHz.
                field: dropdown
                options:
                    '25': '25'
                    '50': '50'
                    '100': '100'
                    '200': '200'
                    '400': '400'
                    '800': '800'
                    '1600': '1600'
                    '3200': '3200'
        """
        self.accel_gyro_odr(accel_odr, gyro_odr)

    def set_accel_range(self, accel_scale) -> None:
        """
        note:
            en: Set the accelerometer scale range.
        label:
            en: Set %1 accelerometer scale %2 g
        params:
            accel_scale:
                name: accel_scale
                note:
                    en: scale range of ±2g, ±4g, ±8g and ±16g.
                field: dropdown
                options:
                    '2': '2'
                    '4': '4'
                    '8': '8'
                    '16': '16'
        """
        self.accel_range(accel_scale)

    def set_gyro_range(self, gyro_scale) -> None:
        """
        note:
            en: Set the gyroscope scale range.
        label:
            en: Set %1 gyroscrope scale %2 dps
        params:
            gyro_scale:
                name: gyro_scale
                field: dropdown
                options:
                    '125': '125'
                    '250': '250'
                    '500': '500'
                    '1000': '1000'
                    '2000': '2000'
        """
        self.gyro_range(gyro_scale)

    def set_magnet_odr(self, magnet_odr) -> None:
        """
        label:
            en: Set %1 magnetometer ODR %2 Hz
        params:
            magnet_odr:
                name: magnet_odr
                field: dropdown
                options:
                    '2': '2'
                    '6': '6'
                    '8': '8'
                    '10': '10'
                    '15': '15'
                    '20': '20'
                    '25': '25'
                    '30': '30'
        """
        self.magnet_odr(magnet_odr)

    def set_gyro_offsets(self, x, y, z) -> None:
        """
        note:
            en: Set the manual gyro calibrations offsets value.
        label:
            en: Set %1 gyroscrope offset calibration x %2 y %3 z %4
        params:
            x:
                name: x
                type: float
                default: '0'
                note:
                    en: gyro calibrations offsets value of X-axis
                field: number
            y:
                name: y
                type: float
                default: '0'
                note:
                    en: gyro calibrations offsets value of Y-axis
                field: number
            z:
                name: z
                type: float
                default: '0'
                note:
                    en: gyro calibrations offsets value of Z-axis
                field: number
        """
        self.gyroXoffset = x
        self.gyroYoffset = y
        self.gyroZoffset = z

    def get_gyroscope(self) -> tuple:
        """
        note:
            en: Get the tuple of x, y, and z values of the gyroscope and gyroscope vector
                in rad/sec.
        label:
            en: Get %1 gyroscope value (return tuple)
        return:
            note: gyroscope tuple (float, float, float)
        """
        return self.gyro()

    def get_accelerometer(self) -> tuple:
        """
        note:
            en: Get the tuple of x, y, and z values of the accelerometer and acceleration
                vector in gravity units (9.81m/s^2).
        label:
            en: Get %1 accelerometer value (m/s^2, return tuple)
        return:
            note: accelerometer tuple (float, float, float)
        """
        return self.accel()

    def get_magnetometer(self) -> tuple:
        """
        note:
            en: Get the tuple of x, y, and z values of the magnetometer and magnetometer vector in uT.
        label:
            en: Get %1 magnetometer value (uT, return tuple)
        return:
            note: magnetometer tuple (float, float, float)
        """
        return self.magnet()

    def get_compass(self) -> float:
        """
        note:
            en: Get the compass heading value is in range of 0º ~ 360º.
        label:
            en: Get %1 compass heading angle (0 to 360 degree, return float)
        return:
            note: range is 0 to 360 degree
        """
        raw = self.get_magnetometer()
        xyHeading = math.atan2(raw[0], raw[1])  # noqa: N806
        if xyHeading < 0:
            xyHeading += 2 * math.pi  # noqa: N806
        if xyHeading > 2 * math.pi:
            xyHeading -= 2 * math.pi  # noqa: N806
        return xyHeading * 180 / math.pi

    def get_attitude(self) -> tuple:
        """
        note:
            en: Get the attitude angles as yaw, pitch, and roll in degrees.
        label:
            en: Get %1 attitude (return tuple, [yaw, pitch, roll])
        return:
            note: tuple of yaw, pitch, and roll (float, float, float)
        """
        (
            accX,  # noqa: N806
            accY,  # noqa: N806
            accZ,  # noqa: N806
        ) = self.get_accelerometer()  # Get processed acceleration data

        # Compute tilt angles from the accelerometer data
        angleAccX = math.atan2(accY, accZ + abs(accX)) * _SF_RAD_S  # noqa: N806
        angleAccY = math.atan2(accX, accZ + abs(accY)) * (-_SF_RAD_S)  # noqa: N806

        # Get processed gyro data and remove offsets
        gyroX, gyroY, gyroZ = self.get_gyroscope()  # noqa: N806
        gyroX -= self.gyroXoffset  # noqa: N806
        gyroY -= self.gyroYoffset  # noqa: N806
        gyroZ -= self.gyroZoffset  # noqa: N806

        # Calculate the time elapsed since the last measurement
        interval = (time.ticks_us() - self.preInterval) / 1000000
        self.preInterval = time.ticks_us()

        # Compute the change in angles from the gyro data
        self.angleGyroX += gyroX * interval
        self.angleGyroY += gyroY * interval
        self.angleGyroZ += gyroZ * interval

        # Combine accelerometer and gyro angles using complementary filter
        self.angleX = (self.gyroCoef * (self.angleX + gyroX * interval)) + (
            self.accCoef * angleAccX
        )
        self.angleY = (self.gyroCoef * (self.angleY + gyroY * interval)) + (
            self.accCoef * angleAccY
        )
        self.angleZ = self.angleGyroZ  # Z angle is taken from the gyro only

        return tuple([round(self.angleZ, 3), round(angleAccX, 3), round(angleAccY, 3)])

    def get_temperature(self) -> float:
        """
        note:
            en: Get the temperature value in degrees celsius from the BMP280 sensor.
        label:
            en: Get %1 temperature (°C, return float)
        return:
            note: range is -40 ~ +85 °C.
        """
        return self.measure()[0]

    def get_pressure(self) -> float:
        """
        note:
            en: Get the pressure value in pascals from the BMP280 sensor.
        label:
            en: Get %1 pressure (hPa, return float)
        return:
            note: range is 300 ~ 1100 hPa.
        """
        return round((self.measure()[1] / 100), 2)

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

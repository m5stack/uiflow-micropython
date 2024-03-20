from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct
import sys

if sys.platform != "esp32":
    from typing import Union


THERMAL_CAM_ADDR = 0x32

BUTTON_REG = 0x00
TEMP_ALARM_REG = 0x01
DEVICE_INFO_REG = 0x04
I2C_ADDR_REG = 0x08
FUNC_CTRL_REG = 0x0A
REFRESH_RATE_REG = 0x0B
NOISE_FILTER_REG = 0x0C
TEMP_MONITOR_REG = 0x10
TEMP_ALARM_EN_REG = 0x11
BUZZER_FREQ_REG = 0x12
BUZZER_DUTY_REG = 0x14
RGB_LED_REG = 0x15
LOW_TEMP_THRES_REG = 0x20
HIGH_TEMP_THRES_REG = 0x30
LOW_TEMP_ALARM_REG = 0x22
HIGH_TEMP_ALARM_REG = 0x32
LOW_ALARM_INTER_REG = 0x24
HIGH_ALARM_INTER_REG = 0x34
LOW_ALARM_LED_REG = 0x25
HIGH_ALARM_LED_REG = 0x35
REFRESH_CTRL_REG = 0x6E
SUB_PAGE_INFO_REG = 0x6F
MEDIAN_TEMP_REG = 0x70
DIFFERENT_TEMP_REG = 0x76
TEMP_DATA_BUFFFER_REG = 0x80

TOTAL_BUFFER = 32 * 24

color_table = [
    0x0000FF,
    0x0003FF,
    0x0006FF,
    0x0009FF,
    0x000CFF,
    0x000FFF,
    0x0012FF,
    0x0016FF,
    0x0019FE,
    0x001CFE,
    0x001FFE,
    0x0022FD,
    0x0025FD,
    0x0028FC,
    0x002BFC,
    0x002FFB,
    0x0032FB,
    0x0035FA,
    0x0038F9,
    0x003BF9,
    0x003EF8,
    0x0041F7,
    0x0044F6,
    0x0047F6,
    0x004AF5,
    0x004DF4,
    0x0050F3,
    0x0053F2,
    0x0056F1,
    0x0059F0,
    0x005CEF,
    0x005FEE,
    0x0062EC,
    0x0065EB,
    0x0068EA,
    0x006AE9,
    0x006DE7,
    0x0070E6,
    0x0073E5,
    0x0076E3,
    0x0079E2,
    0x007BE0,
    0x007EDF,
    0x0081DD,
    0x0084DC,
    0x0086DA,
    0x0089D8,
    0x008CD7,
    0x008ED5,
    0x0091D3,
    0x0093D1,
    0x0096CF,
    0x0098CE,
    0x009BCC,
    0x009DCA,
    0x00A0C8,
    0x00A2C6,
    0x00A5C4,
    0x00A7C2,
    0x00AAC0,
    0x00ACBE,
    0x00AEBC,
    0x00B1B9,
    0x00B3B7,
    0x00B5B5,
    0x00B7B3,
    0x00B9B1,
    0x00BCAE,
    0x00BEAC,
    0x00C0AA,
    0x00C2A7,
    0x00C4A5,
    0x00C6A2,
    0x00C8A0,
    0x00CA9D,
    0x00CC9B,
    0x00CE98,
    0x00CF96,
    0x00D193,
    0x00D391,
    0x00D58E,
    0x00D78C,
    0x00D889,
    0x00DA86,
    0x00DC84,
    0x00DD81,
    0x00DF7E,
    0x00E07B,
    0x00E279,
    0x00E376,
    0x00E573,
    0x00E670,
    0x00E76D,
    0x00E96A,
    0x00EA68,
    0x00EB65,
    0x00EC62,
    0x00EE5F,
    0x00EF5C,
    0x00F059,
    0x00F156,
    0x00F253,
    0x00F350,
    0x00F44D,
    0x00F54A,
    0x00F647,
    0x00F644,
    0x00F741,
    0x00F83E,
    0x00F93B,
    0x00F938,
    0x00FA35,
    0x00FB32,
    0x00FB2F,
    0x00FC2B,
    0x00FC28,
    0x00FD25,
    0x00FD22,
    0x00FE1F,
    0x00FE1C,
    0x00FE19,
    0x00FF16,
    0x00FF12,
    0x00FF0F,
    0x00FF0C,
    0x00FF09,
    0x00FF06,
    0x00FF03,
    0x03FF00,
    0x06FF00,
    0x09FF00,
    0x0CFF00,
    0x0FFF00,
    0x12FF00,
    0x16FF00,
    0x19FE00,
    0x1CFE00,
    0x1FFE00,
    0x22FD00,
    0x25FD00,
    0x28FC00,
    0x2BFC00,
    0x2FFB00,
    0x32FB00,
    0x35FA00,
    0x38F900,
    0x3BF900,
    0x3EF800,
    0x41F700,
    0x44F600,
    0x47F600,
    0x4AF500,
    0x4DF400,
    0x50F300,
    0x53F200,
    0x56F100,
    0x59F000,
    0x5CEF00,
    0x5FEE00,
    0x62EC00,
    0x65EB00,
    0x68EA00,
    0x6AE900,
    0x6DE700,
    0x70E600,
    0x73E500,
    0x76E300,
    0x79E200,
    0x7BE000,
    0x7EDF00,
    0x81DD00,
    0x84DC00,
    0x86DA00,
    0x89D800,
    0x8CD700,
    0x8ED500,
    0x91D300,
    0x93D100,
    0x96CF00,
    0x98CE00,
    0x9BCC00,
    0x9DCA00,
    0xA0C800,
    0xA2C600,
    0xA5C400,
    0xA7C200,
    0xAAC000,
    0xACBE00,
    0xAEBC00,
    0xB1B900,
    0xB3B700,
    0xB5B500,
    0xB7B300,
    0xB9B100,
    0xBCAE00,
    0xBEAC00,
    0xC0AA00,
    0xC2A700,
    0xC4A500,
    0xC6A200,
    0xC8A000,
    0xCA9D00,
    0xCC9B00,
    0xCE9800,
    0xCF9600,
    0xD19300,
    0xD39100,
    0xD58E00,
    0xD78C00,
    0xD88900,
    0xDA8600,
    0xDC8400,
    0xDD8100,
    0xDF7E00,
    0xE07B00,
    0xE27900,
    0xE37600,
    0xE57300,
    0xE67000,
    0xE76D00,
    0xE96A00,
    0xEA6800,
    0xEB6500,
    0xEC6200,
    0xEE5F00,
    0xEF5C00,
    0xF05900,
    0xF15600,
    0xF25300,
    0xF35000,
    0xF44D00,
    0xF54A00,
    0xF64700,
    0xF64400,
    0xF74100,
    0xF83E00,
    0xF93B00,
    0xF93800,
    0xFA3500,
    0xFB3200,
    0xFB2F00,
    0xFC2B00,
    0xFC2800,
    0xFD2500,
    0xFD2200,
    0xFE1F00,
    0xFE1C00,
    0xFE1900,
    0xFF1600,
    0xFF1200,
    0xFF0F00,
    0xFF0C00,
    0xFF0900,
    0xFF0600,
    0xFF0300,
    0xFF0000,
]


class THERMAL2Unit:
    def __init__(self, i2c: Union[I2C, PAHUBUnit], addr=THERMAL_CAM_ADDR):
        self.thermal_i2c = i2c
        self.unit_addr = addr
        self.available()
        self.min_temp = 0
        self.max_temp = 128 << 6

    def available(self):
        if self.unit_addr not in self.thermal_i2c.scan():
            raise UnitError("Thermal2 Camera unit maybe not connect")

    def get_button_state(self, state):
        """! get button status.
        state: 0x01 ~ 0x1f
        return: True or False
        """
        data = self.thermal_i2c.readfrom_mem(self.unit_addr, BUTTON_REG, 1)[0] & 0x1F
        self.thermal_i2c.writeto_mem(self.unit_addr, BUTTON_REG, bytearray([data]))
        data &= state
        return data == state

    @property
    def get_temp_alarm_status(self):
        """! get temperature alarm status."""
        return self.thermal_i2c.readfrom_mem(self.unit_addr, TEMP_ALARM_REG, 1)[0]

    def get_device_detail(self, dev_info=0):
        """! get device status.
        return device id or version
        """
        if dev_info:
            return "{0}.{1}".format(
                self.thermal_i2c.readfrom_mem(self.unit_addr, (DEVICE_INFO_REG + dev_info), 1)[0],
                self.thermal_i2c.readfrom_mem(self.unit_addr, (DEVICE_INFO_REG + dev_info + 1), 1)[
                    0
                ],
            )
        else:
            return hex(
                struct.unpack(
                    ">H", self.thermal_i2c.readfrom_mem(self.unit_addr, DEVICE_INFO_REG, 2)
                )[0]
            )

    def get_i2c_addr(self, addr=0):
        """
        device i2c address.
        return i2c normal addr or bit invert address
        """
        return hex(self.thermal_i2c.readfrom_mem(self.unit_addr, (I2C_ADDR_REG + addr), 1)[0])

    @property
    def get_func_ctrl(self):
        """! get function control"""
        return self.thermal_i2c.readfrom_mem(self.unit_addr, FUNC_CTRL_REG, 1)[0] & 0x07

    def set_func_ctrl(self, ctrl, enable=True):
        """! set function control.
        ctrl: 0 to 7
        enable : True or False
        """
        data = self.thermal_i2c.readfrom_mem(self.unit_addr, FUNC_CTRL_REG, 1)[0] & 0x07
        if enable:
            data |= ctrl
        else:
            data &= ~(ctrl & 0xFF)
        self.thermal_i2c.writeto_mem(self.unit_addr, FUNC_CTRL_REG, bytearray([data & 0x07]))

    @property
    def get_refresh_rate(self):
        """! get refresh rate.
        return: 0 ~ 7
        """
        return self.thermal_i2c.readfrom_mem(self.unit_addr, REFRESH_RATE_REG, 1)[0]

    def set_refresh_rate(self, rate):
        """! set refresh rate.
        rate: 0 to 7
        """
        if rate >= 0 and rate <= 7:
            self.thermal_i2c.writeto_mem(self.unit_addr, REFRESH_RATE_REG, bytearray([rate]))

    @property
    def get_noise_filter(self):
        """! get noise filter.
        return: 0 ~ 15
        """
        return self.thermal_i2c.readfrom_mem(self.unit_addr, NOISE_FILTER_REG, 1)[0] & 0x0F

    def set_noise_filter(self, filter):
        """! set noise filter.
        filter: 0 ~ 15
        """
        if filter >= 0 and filter <= 15:
            self.thermal_i2c.writeto_mem(self.unit_addr, NOISE_FILTER_REG, bytearray([filter]))

    def get_temp_monitor(self, size=1):
        """
        get temp monitor.
        size : 0 to 1
        return: 0~15
        """
        return (
            self.thermal_i2c.readfrom_mem(self.unit_addr, TEMP_MONITOR_REG, 1)[0] >> (4 * size)
        ) & 0x0F

    def set_temp_monitor(self, width, height):
        """
        set temp monitor.
        width or height : 0 to 15
        """
        width = min(15, max(0, width))
        height = min(15, max(0, height))
        data = (height << 4 | width) & 0xFF
        self.thermal_i2c.writeto_mem(self.unit_addr, TEMP_MONITOR_REG, bytearray([data]))

    def set_temp_alarm_ctrl(self, state=0x00, enable=True):
        """
        temp alarm control.
        state : 0x00 to 0xff
        """
        data = self.thermal_i2c.readfrom_mem(self.unit_addr, TEMP_ALARM_EN_REG, 1)[0] & 0xFF
        if enable:
            data |= state
        else:
            data &= ~(state & 0xFF)
        self.thermal_i2c.writeto_mem(self.unit_addr, TEMP_ALARM_EN_REG, bytearray([data]))

    @property
    def get_buzzer_freq(self):
        """! get buzzer frequency.
        freq : 20 to 20000
        """
        return struct.unpack(
            "<H", self.thermal_i2c.readfrom_mem(self.unit_addr, BUZZER_FREQ_REG, 2)
        )[0]

    def set_buzzer_freq(self, freq):
        """
        buzzer frequency.
        freq : 20 to 20000
        """
        freq = min(20000, max(0, freq))
        self.thermal_i2c.writeto_mem(self.unit_addr, BUZZER_FREQ_REG, struct.pack("<H", freq))

    @property
    def get_buzzer_duty(self):
        """! buzzer duty.
        return: 0 ~ 255
        """
        return self.thermal_i2c.readfrom_mem(self.unit_addr, BUZZER_DUTY_REG, 1)[0]

    def set_buzzer_duty(self, duty):
        """! buzzer duty.
        duty: 0 to 256
        """
        self.thermal_i2c.writeto_mem(self.unit_addr, BUZZER_DUTY_REG, bytearray([duty]))

    def set_rgb_led(self, rgb):
        """! set rgb led.
        rgb : 0 to 0xffffff
        """
        self.thermal_i2c.writeto_mem(self.unit_addr, RGB_LED_REG, rgb.to_bytes(3, "big"))

    def get_temp_threshold(self, temp_reg=LOW_TEMP_THRES_REG):
        """! high or low temp threshold.
        return C*
        """
        data = struct.unpack("<H", self.thermal_i2c.readfrom_mem(self.unit_addr, temp_reg, 2))[0]
        return (data - 8192) / 128

    def set_temp_threshold(self, temp_reg=LOW_TEMP_THRES_REG, temp=0):
        """! set high or low temp threshold.
        temp_reg: 0x20 or 0x30
        temp: C
        """
        data = int((temp + 64) * 128)
        self.thermal_i2c.writeto_mem(self.unit_addr, temp_reg, struct.pack("<H", data))

    def get_temp_alarm_buzzer_freq(self, alarm_reg=LOW_TEMP_ALARM_REG):
        """! high or low temp alarm freq."""
        return struct.unpack("<H", self.thermal_i2c.readfrom_mem(self.unit_addr, alarm_reg, 2))[0]

    def set_alarm_buzzer_freq(self, alarm_reg=LOW_TEMP_ALARM_REG, freq=0):
        """! high or low temp alarm freq.
        alarm_reg: 0x22 or 0x32
        """
        freq = min(20000, max(0, freq))
        self.thermal_i2c.writeto_mem(self.unit_addr, alarm_reg, struct.pack("<H", freq))

    def get_temp_alarm_interval(self, alarm_reg=LOW_ALARM_INTER_REG):
        """! get high or low temp alarm interval."""
        return self.thermal_i2c.readfrom_mem(self.unit_addr, alarm_reg, 1)[0] * 10

    def set_temp_alarm_interval(self, alarm_reg=LOW_ALARM_INTER_REG, value=None):
        """! set high or low temp alarm interval.
        alarm_reg: 0x24 or 0x34
        value: 50 ~ 2550 ms
        """
        value = int(value / 10)
        self.thermal_i2c.writeto_mem(self.unit_addr, alarm_reg, bytearray([value]))

    def get_temp_alarm_led(self, alarm_reg=LOW_ALARM_LED_REG):
        """! get high or low temp alarm LED Color."""
        return list(self.thermal_i2c.readfrom_mem(self.unit_addr, alarm_reg, 3))

    def set_temp_alarm_led(self, alarm_reg=LOW_ALARM_LED_REG, rgb=0):
        """! set high or low temp alarm LED Color."""
        self.thermal_i2c.writeto_mem(self.unit_addr, alarm_reg, rgb.to_bytes(3, "big"))

    @property
    def get_data_refresh_ctrl(self):
        """! get data refresh control."""
        data = self.thermal_i2c.readfrom_mem(self.unit_addr, REFRESH_CTRL_REG, 1)[0]
        self.thermal_i2c.writeto_mem(self.unit_addr, REFRESH_CTRL_REG, b"\x00")
        return data

    @property
    def get_subpage_info(self):
        """! get sub page inform."""
        return self.thermal_i2c.readfrom_mem(self.unit_addr, SUB_PAGE_INFO_REG, 1)[0]

    def get_temp_measure(self, temp_reg=0):
        """! get temp measure of median, avg, differential."""
        data = struct.unpack(
            "<H", self.thermal_i2c.readfrom_mem(self.unit_addr, (MEDIAN_TEMP_REG + temp_reg), 2)
        )[0]
        return round((data - 8192) / 128, 2)

    def get_temp_differential(self, temp_reg=0, x=0):
        """! get temp differential x, y position."""
        return self.thermal_i2c.readfrom_mem(self.unit_addr, DIFFERENT_TEMP_REG + temp_reg + x, 1)[
            0
        ]

    @property
    def get_temp_data_buffer(self):
        """! get temperature data buffer array(little endian)."""
        buf = self.thermal_i2c.readfrom_mem(self.unit_addr, TEMP_DATA_BUFFFER_REG, TOTAL_BUFFER)
        return list(struct.unpack("<{}".format("H" * int(TOTAL_BUFFER / 2)), buf))

    def convert_to_map(self, val, in_min, in_max, out_min, out_max):
        return int((val - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

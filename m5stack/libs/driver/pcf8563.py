# Copyright (c) 2020 Sebastian Wicki
# Copyright (c) 2020 Mika Tuupola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# Based on https://github.com/tuupola/pcf8563
#
# Unimplemented:
#   - Timer support
#   - CLKOUT configuration
"""
Driver for the PCF8563/BM8563 real-time clock module.
"""

from micropython import const

_PCF8563_I2C_DEFAULT_ADDR = const(0x51)

_PCF8563_CONTROL_STATUS1 = const(0x00)
_PCF8563_CONTROL_STATUS1_TEST1 = const(0b1000_0000)
_PCF8563_CONTROL_STATUS1_STOP = const(0b0010_0000)
_PCF8563_CONTROL_STATUS1_TESTC = const(0b0000_1000)

_PCF8563_CONTROL_STATUS2 = const(0x01)
_PCF8563_CONTROL_STATUS2_TI_TP = const(0b0001_0000)
_PCF8563_CONTROL_STATUS2_AF = const(0b0000_1000)
_PCF8563_CONTROL_STATUS2_TF = const(0b0000_0100)
_PCF8563_CONTROL_STATUS2_AIE = const(0b0000_0010)
_PCF8563_CONTROL_STATUS2_TIE = const(0b0000_0001)

_PCF8563_SECONDS = const(0x02)
_PCF8563_MINUTES = const(0x03)
_PCF8563_HOURS = const(0x04)
_PCF8563_DAY = const(0x05)
_PCF8563_WEEKDAY = const(0x06)
_PCF8563_MONTH = const(0x07)
_PCF8563_YEAR = const(0x08)
_PCF8563_TIME_SIZE = const(7)

_PCF8563_CENTURY_BIT = const(0b1000_0000)

_PCF8563_MINUTE_ALARM = const(0x09)
_PCF8563_HOUR_ALARM = const(0x0A)
_PCF8563_DAY_ALARM = const(0x0B)
_PCF8563_WEEKDAY_ALARM = const(0x0C)
_PCF8563_ALARM_SIZE = const(4)

_PCF8563_ALARM_DISABLE = const(0b1000_0000)

_PCF8563_TIMER_CONTROL = const(0x0E)
_PCF8563_TIMER_CONTROL_ENABLE = const(0b1000_0000)
_PCF8563_TIMER_CONTROL_FREQ_4_096KHZ = const(0b0000_0000)
_PCF8563_TIMER_CONTROL_FREQ_64HZ = const(0b0000_0001)
_PCF8563_TIMER_CONTROL_FREQ_1HZ = const(0b0000_0010)
_PCF8563_TIMER_CONTROL_FREQ_1_60HZ = const(0b0000_0011)
_PCF8563_TIMER = const(0x0F)


def _dec2bcd(decimal):
    high, low = divmod(decimal, 10)
    return (high << 4) | low


def _bcd2dec(bcd):
    return (((bcd & 0xFF) >> 4) * 10) + (bcd & 0x0F)


class PCF8563:
    def __init__(self, i2c, *, addr=_PCF8563_I2C_DEFAULT_ADDR, alarm_irq=True):
        self.i2c = i2c
        self.addr = addr

        status = bytearray(1)
        self.i2c.writeto_mem(self.addr, _PCF8563_CONTROL_STATUS1, status)
        if alarm_irq:
            status[0] |= _PCF8563_CONTROL_STATUS2_AIE
        self.i2c.writeto_mem(self.addr, _PCF8563_CONTROL_STATUS2, status)

    def datetime(self, datetime=None):
        """
        With no arguments, this method returns an 7-tuple with the current
        date and time. With 1 argument (being an 7-tuple) it sets the date and
        time. The 7-tuple has the following format:

        (year, month, mday, hour, minute, second, weekday)

        `year` is 1900..2099
        `month` is 1..12
        `mday` is 1..31
        `hour` is 0..23
        `minute` is 0..59
        `second` is 0..59
        `weekday` is 0..6
        """
        if datetime is None:
            data = self.i2c.readfrom_mem(self.addr, _PCF8563_SECONDS, _PCF8563_TIME_SIZE)
            # 0..59
            bcd = data[0] & 0b01111111
            second = _bcd2dec(bcd)
            # 0..59
            bcd = data[1] & 0b01111111
            minute = _bcd2dec(bcd)
            # 0..23
            bcd = data[2] & 0b00111111
            hour = _bcd2dec(bcd)
            # 1..31
            bcd = data[3] & 0b00111111
            mday = _bcd2dec(bcd)
            # 0..6
            bcd = data[4] & 0b00000111
            weekday = _bcd2dec(bcd)
            # 1..12
            bcd = data[5] & 0b00011111
            month = _bcd2dec(bcd)
            # If the century bit set, assume it is 2000. Note that it seems
            # that unlike PCF8563, the BM8563 does NOT automatically
            # toggle the century bit when year overflows from 99 to 00.
            # The BM8563 also wrongly treats 1900/2100 as leap years.
            century = 100 if (data[5] & _PCF8563_CENTURY_BIT) else 0
            # Number of years since the start of the century
            bcd = data[6] & 0b11111111
            year = _bcd2dec(bcd) + century + 1900

            return (year, month, mday, hour, minute, second, weekday)

        (year, month, mday, hour, minute, second, weekday) = datetime
        data = bytearray(_PCF8563_TIME_SIZE)
        # 0..59
        bcd = _dec2bcd(second)
        data[0] = bcd & 0b01111111
        # 0..59
        bcd = _dec2bcd(minute)
        data[1] = bcd & 0b01111111
        # 0..23
        bcd = _dec2bcd(hour)
        data[2] = bcd & 0b00111111
        # 1..31
        bcd = _dec2bcd(mday)
        data[3] = bcd & 0b00111111
        # 0..6
        bcd = _dec2bcd(weekday)
        data[4] = bcd & 0b00000111
        # 1..12
        bcd = _dec2bcd(month)
        data[5] = bcd & 0b00011111
        # after 2000 set the century bit
        if year >= 2000:
            data[5] |= _PCF8563_CENTURY_BIT
        # 0..99
        bcd = _dec2bcd(year % 100)
        data[6] = bcd & 0b11111111

        return self.i2c.writeto_mem(self.addr, _PCF8563_SECONDS, data)

    def alarm(self, alarm=None):
        """
        Sets or gets the alarm. If no arguments are provided, it returns
        the currently set alarm in the form of a 4-tuple. If 1 argument is
        provided (being a 4-tuple), the alarm is set.

        (hour, minute, mday, weekday)

        `hour` is 0..23 or None
        `minute` is 0..59 or None
        `mday` is 1..31 or None
        `weekday` is 0..6 or None

        If a tuple field is set to None then it is not considered for triggering
        the alarm. If all four fields are set to None, the alarm is disabled.
        """
        if alarm is None:
            data = self.i2c.readfrom_mem(self.addr, _PCF8563_MINUTE_ALARM, _PCF8563_ALARM_SIZE)
            # 0..59
            if _PCF8563_ALARM_DISABLE & data[0]:
                minute = None
            else:
                bcd = data[0] & 0b01111111
                minute = _bcd2dec(bcd)
            # 0..23
            if _PCF8563_ALARM_DISABLE & data[1]:
                hour = None
            else:
                bcd = data[1] & 0b00111111
                hour = _bcd2dec(bcd)
            # 1..31
            if _PCF8563_ALARM_DISABLE & data[2]:
                mday = None
            else:
                bcd = data[2] & 0b00111111
                mday = _bcd2dec(bcd)
            # 0..6
            if _PCF8563_ALARM_DISABLE & data[3]:
                weekday = None
            else:
                bcd = data[3] & 0b00000111
                weekday = _bcd2dec(bcd)

            return (hour, minute, mday, weekday)

        (hour, minute, mday, weekday) = alarm
        data = bytearray(_PCF8563_ALARM_SIZE)
        # 0..59
        if minute is None:
            data[0] = _PCF8563_ALARM_DISABLE
        else:
            data[0] = _dec2bcd(minute)
            data[0] &= 0b01111111
        # 0..23
        if hour is None:
            data[1] = _PCF8563_ALARM_DISABLE
        else:
            data[1] = _dec2bcd(hour)
            data[1] &= 0b00111111
        # 1..31
        if mday is None:
            data[2] = _PCF8563_ALARM_DISABLE
        else:
            data[2] = _dec2bcd(mday)
            data[2] &= 0b00111111
        # 0..6
        if weekday is None:
            data[3] = _PCF8563_ALARM_DISABLE
        else:
            data[3] = _dec2bcd(weekday)
            data[3] &= 0b00000111
        return self.i2c.writeto_mem(self.addr, _PCF8563_MINUTE_ALARM, data)

    def alarm_active(self, clear=False):
        """
        Returns True if the alarm is currently active. An active alarm can be
        cleared by setting the clear argument to True.
        """
        data = bytearray(1)
        self.i2c.readfrom_mem_into(self.addr, _PCF8563_CONTROL_STATUS2, data)
        active = bool(data[0] & _PCF8563_CONTROL_STATUS2_AF)
        if clear:
            data[0] &= ~_PCF8563_CONTROL_STATUS2_AF  # AF=0 means alarm cleared
            data[0] |= _PCF8563_CONTROL_STATUS2_TF  # TF=1 mean timer unchanged
            self.i2c.writeto_mem(self.addr, _PCF8563_CONTROL_STATUS2, data)
        return active

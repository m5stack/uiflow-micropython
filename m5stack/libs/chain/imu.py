# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import math
import struct
from .chain import ChainBus
from .key import KeyChain


class IMUChain(KeyChain):
    """Driver for Chain IMU."""

    CMD_GET_I2C_MEM = 0x13
    CMD_WRITE_I2C_MEM = 0x14
    CMD_GET_ACCEL = 0x30
    CMD_GET_GYRO = 0x31
    CMD_GET_ACCEL_RAW = 0x32
    CMD_GET_GYRO_RAW = 0x33
    CMD_GET_TEMPERATURE = 0x34
    CMD_SET_ACCEL_RANGE = 0x35
    CMD_GET_ACCEL_RANGE = 0x36
    CMD_SET_GYRO_RANGE = 0x37
    CMD_GET_GYRO_RANGE = 0x38
    CMD_SET_ACCEL_ODR = 0x39
    CMD_GET_ACCEL_ODR = 0x3A
    CMD_SET_GYRO_ODR = 0x3B
    CMD_GET_GYRO_ODR = 0x3C
    CMD_REPORT_EVENT = 0xE0
    CMD_SET_ALARM_MODE = 0xE1
    CMD_GET_ALARM_MODE = 0xE2
    CMD_SET_MOTION_ALARM_THRESH = 0xE3
    CMD_GET_MOTION_ALARM_THRESH = 0xE4
    CMD_SET_TEMPERATURE_ALARM_THRESH = 0xE5
    CMD_GET_TEMPERATURE_ALARM_THRESH = 0xE6
    UID_4_BYTES = 0
    UID_12_BYTES = 1

    ACCEL_RANGE_2G = 2
    ACCEL_RANGE_4G = 4
    ACCEL_RANGE_8G = 8
    ACCEL_RANGE_16G = 16
    GYRO_RANGE_125DPS = 125
    GYRO_RANGE_250DPS = 250
    GYRO_RANGE_500DPS = 500
    GYRO_RANGE_1000DPS = 1000
    GYRO_RANGE_2000DPS = 2000
    ODR_POWER_DOWN = 0
    ODR_1_6HZ = 1.6
    ODR_12_5HZ = 12.5
    ODR_26HZ = 26
    ODR_52HZ = 52
    ODR_104HZ = 104
    ODR_208HZ = 208
    ODR_416HZ = 416
    ODR_833HZ = 833
    ODR_1660HZ = 1660
    ODR_3330HZ = 3330
    ODR_6660HZ = 6660
    ACCEL_RANGES = (2, 4, 8, 16)
    GYRO_RANGES = (125, 250, 500, 1000, 2000)
    ACCEL_ODR_VALUES = (0, 1.6, 12.5, 26, 52, 104, 208, 416, 833, 1660, 3330, 6660)
    GYRO_ODR_VALUES = (0, 12.5, 26, 52, 104, 208, 416, 833, 1660, 3330, 6660)
    ALARM_NONE = 0
    ALARM_ACCEL = 1
    ALARM_GYRO = 2
    ALARM_TEMPERATURE = 4
    ALARM_ALL = 7

    # Event callback selectors used by the UiFlow2 event block.  The
    # callback still receives the complete status bit field so combined
    # IMU events are preserved.
    EVENT_ACCEL = ALARM_ACCEL
    EVENT_GYRO = ALARM_GYRO
    EVENT_TEMPERATURE = ALARM_TEMPERATURE
    _SOURCE_EVENTS = (EVENT_ACCEL, EVENT_GYRO, EVENT_TEMPERATURE)

    EVENT_ACCEL_CLEAR = 0x10
    EVENT_ACCEL_TRIGGER = 0x11
    EVENT_GYRO_CLEAR = 0x20
    EVENT_GYRO_TRIGGER = 0x21
    EVENT_TEMPERATURE_HIGH_CLEAR = 0x30
    EVENT_TEMPERATURE_HIGH = 0x31
    EVENT_TEMPERATURE_LOW = 0x32
    EVENT_TEMPERATURE_LOW_CLEAR = 0x33
    EVENT_TYPES = _SOURCE_EVENTS + (
        EVENT_ACCEL_CLEAR,
        EVENT_ACCEL_TRIGGER,
        EVENT_GYRO_CLEAR,
        EVENT_GYRO_TRIGGER,
        EVENT_TEMPERATURE_HIGH_CLEAR,
        EVENT_TEMPERATURE_HIGH,
        EVENT_TEMPERATURE_LOW,
        EVENT_TEMPERATURE_LOW_CLEAR,
    )
    _EVENT_FILTERS = {
        EVENT_ACCEL_CLEAR: (0x01, 0),
        EVENT_ACCEL_TRIGGER: (0x01, 1),
        EVENT_GYRO_CLEAR: (0x02, 0),
        EVENT_GYRO_TRIGGER: (0x02, 2),
    }

    _REPORT_TYPE = 0x10
    _I2C_MAX_LENGTH = 64
    _I2C_ADDR_MIN = 0x08
    _I2C_ADDR_MAX = 0x77
    _ACCEL_RANGE = (ACCEL_RANGE_2G, ACCEL_RANGE_16G, ACCEL_RANGE_4G, ACCEL_RANGE_8G)
    _ACCEL_ODR = (
        ODR_POWER_DOWN,
        ODR_12_5HZ,
        ODR_26HZ,
        ODR_52HZ,
        ODR_104HZ,
        ODR_208HZ,
        ODR_416HZ,
        ODR_833HZ,
        ODR_1660HZ,
        ODR_3330HZ,
        ODR_6660HZ,
        ODR_1_6HZ,
    )
    _GYRO_RANGE = (
        GYRO_RANGE_250DPS,
        GYRO_RANGE_125DPS,
        GYRO_RANGE_500DPS,
        GYRO_RANGE_1000DPS,
        GYRO_RANGE_2000DPS,
    )
    _GYRO_RANGE_CODES = (0, 1, 2, 4, 6)
    _GYRO_ODR = (
        ODR_POWER_DOWN,
        ODR_12_5HZ,
        ODR_26HZ,
        ODR_52HZ,
        ODR_104HZ,
        ODR_208HZ,
        ODR_416HZ,
        ODR_833HZ,
        ODR_1660HZ,
        ODR_3330HZ,
        ODR_6660HZ,
    )

    def __init__(self, bus: ChainBus, device_id: int):
        """Create a IMUChain on an existing ChainBus. Registration performs no device configuration. The caller owns the bus and must close it after all devices are detached.

        :param bus: An open shared ChainBus instance.
        :type bus: ChainBus
        :param device_id: Enumerated Chain position, 1..254.
        :type device_id: int
        :returns: A registered IMUChain object.
        :rtype: IMUChain

        UiFlow2 Code Block:

            |init.png|

        MicroPython Code Block:

            .. code-block:: python

                device = IMUChain(bus, 1)
        """
        if not isinstance(device_id, int) or isinstance(device_id, bool):
            raise TypeError("device_id must be an integer")
        if not 1 <= device_id <= 254:
            raise ValueError("device_id is out of range")
        if not getattr(bus, "_running", True):
            raise RuntimeError("ChainBus is closed")
        super().__init__(bus, device_id)
        self._closed = False
        self._callback = None
        self._event_callbacks = {}
        self._last_event_status = 0

    def read_accel(self):
        """Read three-axis acceleration in m/s^2, using standard gravity 9.80665 m/s^2.

        :returns: Tuple (x, y, z) of floats in m/s^2, resolution 0.00980665 m/s^2.
        :rtype: tuple

        UiFlow2 Code Block:

            |read_accel.png|

        MicroPython Code Block:

            .. code-block:: python

                x, y, z = device.read_accel()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_ACCEL, b"")
        if not state or response is None or len(response) != 6:
            raise OSError("Invalid Chain response")
        return tuple((value * 0.00980665 for value in struct.unpack("<hhh", response)))

    def read_gyro(self):
        """Read the latest IMU sample. Firmware refreshes the sensor but can return the previous sample if that refresh fails.

        :returns: Tuple (x, y, z) of floats in rad/s, resolution pi/180 rad/s (about 0.0174533 rad/s).
        :rtype: tuple

        UiFlow2 Code Block:

            |read_gyro.png|

        MicroPython Code Block:

            .. code-block:: python

                xyz = device.read_gyro()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_GYRO, b"")
        if not state or response is None or len(response) != 6:
            raise OSError("Invalid Chain response")
        return tuple((value * (math.pi / 180.0) for value in struct.unpack("<hhh", response)))

    def read_accel_raw(self):
        """Read the latest IMU sample. Firmware refreshes the sensor but can return the previous sample if that refresh fails.

        :returns: Tuple (x, y, z) of signed 16-bit raw sensor counts.
        :rtype: tuple

        UiFlow2 Code Block:

            |read_accel_raw.png|

        MicroPython Code Block:

            .. code-block:: python

                xyz = device.read_accel_raw()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_ACCEL_RAW, b"")
        if not state or response is None or len(response) != 6:
            raise OSError("Invalid Chain response")
        return struct.unpack("<hhh", response)

    def read_gyro_raw(self):
        """Read the latest IMU sample. Firmware refreshes the sensor but can return the previous sample if that refresh fails.

        :returns: Tuple (x, y, z) of signed 16-bit raw sensor counts.
        :rtype: tuple

        UiFlow2 Code Block:

            |read_gyro_raw.png|

        MicroPython Code Block:

            .. code-block:: python

                xyz = device.read_gyro_raw()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_GYRO_RAW, b"")
        if not state or response is None or len(response) != 6:
            raise OSError("Invalid Chain response")
        return struct.unpack("<hhh", response)

    def read_temperature(self):
        """Read IMU temperature. Firmware clamps temperatures below zero to 0 degrees Celsius; negative temperatures cannot be recovered through this command.

        :returns: Temperature in degrees Celsius, 0..655.35, resolution 0.01 degrees.
        :rtype: float

        UiFlow2 Code Block:

            |read_temperature.png|

        MicroPython Code Block:

            .. code-block:: python

                temperature = device.read_temperature()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_TEMPERATURE, b"")
        if not state or response is None or len(response) != 2:
            raise OSError("Invalid Chain response")
        return struct.unpack("<H", response)[0] / 100.0

    def set_accel_range(self, accel_scale):
        """Set acceleration full-scale range. The setting is volatile.

        :param accel_scale: An ACCEL_RANGE_* constant in ACCEL_RANGES, in g (2, 4, 8 or 16). Samples from read_accel() remain in m/s^2.
        :type accel_scale: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_accel_range.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_accel_range(IMUChain.ACCEL_RANGE_2G)
        """
        if type(accel_scale) not in (int, float):
            raise TypeError("accel_scale must be a number")
        if accel_scale not in self._ACCEL_RANGE:
            raise ValueError("accel_scale is not a supported setting")
        index = self._ACCEL_RANGE.index(accel_scale)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_ACCEL_RANGE, bytes((index,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_accel_range(self):
        """Get acceleration full-scale range.

        :returns: An ACCEL_RANGE_* constant in ACCEL_RANGES, in g (2, 4, 8 or 16). Samples from read_accel() remain in m/s^2.
        :rtype: int or float

        UiFlow2 Code Block:

            |get_accel_range.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_accel_range()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_ACCEL_RANGE, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] >= len(self._ACCEL_RANGE):
            raise OSError("Chain returned an unknown setting")
        return self._ACCEL_RANGE[response[0]]

    def set_gyro_range(self, gyro_scale):
        """Set the gyroscope full-scale range. The setting is volatile.

        :param gyro_scale: A GYRO_RANGE_* constant in GYRO_RANGES, in degrees/s (125, 250, 500, 1000 or 2000). Samples from read_gyro() remain in rad/s.
        :type gyro_scale: int
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_gyro_range.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_gyro_range(IMUChain.GYRO_RANGE_500DPS)
        """
        if type(gyro_scale) not in (int, float):
            raise TypeError("gyro_scale must be a number")
        if gyro_scale not in self._GYRO_RANGE:
            raise ValueError("gyro_scale is not a supported setting")
        index = self._GYRO_RANGE.index(gyro_scale)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_GYRO_RANGE, bytes((self._GYRO_RANGE_CODES[index],))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_gyro_range(self):
        """Get the gyroscope full-scale range.

        :returns: Full-scale magnitude in degrees per second.
        :rtype: int

        UiFlow2 Code Block:

            |get_gyro_range.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_gyro_range()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_GYRO_RANGE, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        code = response[0]
        if code not in self._GYRO_RANGE_CODES:
            raise OSError("Unknown gyroscope range")
        return self._GYRO_RANGE[self._GYRO_RANGE_CODES.index(code)]

    def set_accel_odr(self, accel_odr):
        """Set acceleration sampling rate. The setting is volatile.

        :param accel_odr: An ODR_* constant in ACCEL_ODR_VALUES, in Hz; ODR_POWER_DOWN (0) disables this channel.
        :type accel_odr: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_accel_odr.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_accel_odr(IMUChain.ODR_104HZ)
        """
        if type(accel_odr) not in (int, float):
            raise TypeError("accel_odr must be a number")
        if accel_odr not in self._ACCEL_ODR:
            raise ValueError("accel_odr is not a supported setting")
        index = self._ACCEL_ODR.index(accel_odr)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_ACCEL_ODR, bytes((index,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_accel_odr(self):
        """Get acceleration sampling rate.

        :returns: An ODR_* constant in ACCEL_ODR_VALUES, in Hz; ODR_POWER_DOWN (0) disables this channel.
        :rtype: int or float

        UiFlow2 Code Block:

            |get_accel_odr.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_accel_odr()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_ACCEL_ODR, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] >= len(self._ACCEL_ODR):
            raise OSError("Chain returned an unknown setting")
        return self._ACCEL_ODR[response[0]]

    def set_gyro_odr(self, gyro_odr):
        """Set gyroscope sampling rate. The setting is volatile.

        :param gyro_odr: An ODR_* constant in GYRO_ODR_VALUES, in Hz; ODR_POWER_DOWN (0) disables this channel.
        :type gyro_odr: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_gyro_odr.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_gyro_odr(IMUChain.ODR_104HZ)
        """
        if type(gyro_odr) not in (int, float):
            raise TypeError("gyro_odr must be a number")
        if gyro_odr not in self._GYRO_ODR:
            raise ValueError("gyro_odr is not a supported setting")
        index = self._GYRO_ODR.index(gyro_odr)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_GYRO_ODR, bytes((index,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_gyro_odr(self):
        """Get gyroscope sampling rate.

        :returns: An ODR_* constant in GYRO_ODR_VALUES, in Hz; ODR_POWER_DOWN (0) disables this channel.
        :rtype: int or float

        UiFlow2 Code Block:

            |get_gyro_odr.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_gyro_odr()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_GYRO_ODR, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] >= len(self._GYRO_ODR):
            raise OSError("Chain returned an unknown setting")
        return self._GYRO_ODR[response[0]]

    def set_alarm_mode(self, mode):
        """Select the enabled alarm sources. Zero disables all alarms. The setting is volatile. Bits: 1 acceleration, 2 gyroscope, 4 temperature.

        :param mode: Alarm bitmask, 0..7; combine ALARM_* bits with ``|``, use ALARM_NONE to disable or ALARM_ALL to enable all sources.
        :type mode: int
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_alarm_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_alarm_mode(IMUChain.ALARM_ALL)
        """
        if not isinstance(mode, int) or isinstance(mode, bool):
            raise TypeError("mode must be an integer")
        if not 0 <= mode <= 7:
            raise ValueError("mode is out of range")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_ALARM_MODE, bytes((mode,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_alarm_mode(self):
        """Get the enabled alarm sources.

        :returns: Alarm bitmask, 0..7; combine ALARM_* bits with ``|``, use ALARM_NONE to disable or ALARM_ALL to enable all sources.
        :rtype: int

        UiFlow2 Code Block:

            |get_alarm_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = device.get_alarm_mode()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_ALARM_MODE, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        return response[0]

    def set_motion_alarm_thresh(self, accel_mg, gyro_dps):
        """Set motion delta thresholds. Firmware compares each axis against its moving reference and debounces transitions over five samples. The setting is volatile.

        :param accel_mg: Acceleration delta in mg, 0..255.
        :type accel_mg: int
        :param gyro_dps: Angular velocity delta in degrees per second, 0..255.
        :type gyro_dps: int
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_motion_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_motion_alarm_thresh(100, 20)
        """
        if not isinstance(accel_mg, int) or isinstance(accel_mg, bool):
            raise TypeError("accel_mg must be an integer")
        if not 0 <= accel_mg <= 255:
            raise ValueError("accel_mg is out of range")
        if not isinstance(gyro_dps, int) or isinstance(gyro_dps, bool):
            raise TypeError("gyro_dps must be an integer")
        if not 0 <= gyro_dps <= 255:
            raise ValueError("gyro_dps is out of range")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_MOTION_ALARM_THRESH, bytes((accel_mg, gyro_dps))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_motion_alarm_thresh(self):
        """Get motion delta thresholds.

        :returns: Tuple (accel_mg, gyro_dps), each 0..255.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_motion_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                accel_mg, gyro_dps = device.get_motion_alarm_thresh()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_MOTION_ALARM_THRESH, b""
        )
        if not state or response is None or len(response) != 2:
            raise OSError("Invalid Chain response")
        return struct.unpack("<BB", response)

    def set_temperature_alarm_thresh(self, low, high):
        """Set the temperature alarm window. The setting is volatile.

        :param low: Temperature in degrees Celsius. Range: 0..255; low must be less than high.
        :type low: int
        :param high: Temperature in degrees Celsius. Range: 0..255; low must be less than high.
        :type high: int
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_temperature_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_temperature_alarm_thresh(10, 40)
        """
        if not isinstance(low, int) or isinstance(low, bool):
            raise TypeError("low must be an integer")
        if not 0 <= low <= 255:
            raise ValueError("low is out of range")
        low_raw = low
        if not isinstance(high, int) or isinstance(high, bool):
            raise TypeError("high must be an integer")
        if not 0 <= high <= 255:
            raise ValueError("high is out of range")
        high_raw = high
        if low_raw >= high_raw:
            raise ValueError("low must be less than high")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id,
            self.CMD_SET_TEMPERATURE_ALARM_THRESH,
            struct.pack("<BB", low_raw, high_raw),
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_temperature_alarm_thresh(self):
        """Get the temperature alarm window.

        :returns: Tuple (low, high). Temperature in degrees Celsius.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_temperature_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                low, high = device.get_temperature_alarm_thresh()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_TEMPERATURE_ALARM_THRESH, b""
        )
        if not state or response is None or len(response) != 2:
            raise OSError("Invalid Chain response")
        low, high = struct.unpack("<BB", response)
        return (low, high)

    def deinit(self):
        """Detach the device and release all event callbacks; the shared bus stays open.

        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |deinit.png|
        """
        self._closed = True
        self._callback = None
        self.bus._event.pop(self, None)
        if self in self.bus._device:
            self.bus._device.remove(self)
        self._event_callbacks.clear()
        self._last_event_status = 0

    def _dispatch_imu_event(self, event):
        changed = event ^ self._last_event_status
        previous_temperature = self._last_event_status & 0x0C
        temperature = event & 0x0C
        temperature_event = None
        if changed & 0x0C:
            if temperature == 0x04:
                temperature_event = self.EVENT_TEMPERATURE_HIGH
            elif temperature == 0x08:
                temperature_event = self.EVENT_TEMPERATURE_LOW
            elif temperature == 0:
                if previous_temperature == 0x04:
                    temperature_event = self.EVENT_TEMPERATURE_HIGH_CLEAR
                elif previous_temperature == 0x08:
                    temperature_event = self.EVENT_TEMPERATURE_LOW_CLEAR
        # Temperature code 3 is a release transition, not a persistent alarm.
        temperature_released = (event & 0x0C) == 0x0C
        if temperature_released:
            temperature_event = self.EVENT_TEMPERATURE_LOW_CLEAR
        self._last_event_status = event & (0x03 if temperature_released else 0x0F)
        for event_type, callback in tuple(self._event_callbacks.items()):
            if event_type in self._EVENT_FILTERS:
                mask, value = self._EVENT_FILTERS[event_type]
                matches = bool(changed & mask) and (event & mask) == value
            elif event_type >= self.EVENT_TEMPERATURE_HIGH_CLEAR:
                matches = event_type == temperature_event
            elif event_type == self.EVENT_TEMPERATURE:
                matches = bool(changed & 0x0C) or temperature_released
            else:
                matches = bool(changed & event_type)
            if matches:
                callback(event if event_type in self._SOURCE_EVENTS else event_type)

    def set_event_callback(self, event=None, callback=None):
        """Register a specific IMU alarm or recovery callback.

        Use EVENT_ACCEL_TRIGGER/CLEAR, EVENT_GYRO_TRIGGER/CLEAR, or
        EVENT_TEMPERATURE_HIGH/LOW/HIGH_CLEAR/LOW_CLEAR. Each handler receives
        its selected event constant. None removes only that event handler.
        Registration does not change alarm reporting. Enable alarms afterwards.
        State tracking starts at zero when the first source is registered.
        Recovery requires a prior alarm report, except explicit low recovery.
        Legacy source selectors and the single-callback form receive raw status.
        set_event_callback(None) removes all handlers.

        :param event: An EVENT_* constant, legacy callback or None. Default: None.
        :type event: int or callable or None
        :param callback: Handler receiving the selected event constant. Default: None.
        :type callback: callable or None
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |event_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def on_accel(event):
                    print(event)

                device.set_event_callback(IMUChain.EVENT_ACCEL_TRIGGER, on_accel)
        """
        self._check_open()
        if event is None or callable(event):
            if callable(event):
                if callback is not None:
                    raise TypeError("legacy callback accepts one handler")
                callback = event
            if callback is not None and (not callable(callback)):
                raise TypeError("callback must be callable or None")
            self._event_callbacks.clear()
            self._last_event_status = 0
            self._callback = callback
        else:
            if not isinstance(event, int) or isinstance(event, bool):
                raise TypeError("event must be an integer")
            if event not in self.EVENT_TYPES:
                raise ValueError("event is not a supported IMU event type")
            if callback is not None and (not callable(callback)):
                raise TypeError("callback must be callable or None")
            if callback is None:
                self._event_callbacks.pop(event, None)
            else:
                if not self._event_callbacks:
                    self._last_event_status = 0
                self._event_callbacks[event] = callback
            self._callback = self._dispatch_imu_event if self._event_callbacks else None
        if self._callback is None:
            events = self.bus._event.get(self)
            if events is not None:
                events.pop(self.CMD_REPORT_EVENT, None)
                if not events:
                    self.bus._event.pop(self, None)
        else:
            self.bus.register_event(self, self.CMD_REPORT_EVENT, None, self._on_event)

    def read_i2c_mem(self, address, register, length, addrsize=8):
        """Read the internal sensor I2C register space through Chain. This may clear sensor status registers.

        :param address: Seven-bit internal I2C address, 0x08..0x77.
        :type address: int
        :param register: Register address, 0..255 for addrsize=8 or 0..65535 for addrsize=16.
        :type register: int
        :param length: Number of bytes, 1..64.
        :type length: int
        :param addrsize: Register address width in bits, 8 or 16. Default: 8.
        :type addrsize: int
        :returns: Requested register bytes.
        :rtype: bytes

        UiFlow2 Code Block:

            |read_i2c_mem.png|

        MicroPython Code Block:

            .. code-block:: python

                data = device.read_i2c_mem(address, register, 1)
        """
        header = self._i2c_header(address, register, length, addrsize)
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_I2C_MEM, header)
        if not state or response is None or len(response) != length + 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")
        response = response[1:]
        return bytes(response)

    def write_i2c_mem(self, address, register, data, addrsize=8):
        """Write the internal sensor I2C register space through Chain. Direct register writes can change measurement and alarm configuration; use sensor-specific configuration methods for normal operation.

        :param address: Seven-bit internal I2C address, 0x08..0x77.
        :type address: int
        :param register: Register address, 0..255 for addrsize=8 or 0..65535 for addrsize=16.
        :type register: int
        :param data: Buffer containing 1..64 bytes.
        :type data: bytes or bytearray or memoryview
        :param addrsize: Register address width in bits, 8 or 16. Default: 8.
        :type addrsize: int
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |write_i2c_mem.png|

        MicroPython Code Block:

            .. code-block:: python

                device.write_i2c_mem(address, register, data)
        """
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be a bytes-like buffer")
        header = self._i2c_header(address, register, len(data), addrsize)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_WRITE_I2C_MEM, header + bytes(data)
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def _check_open(self):
        if self._closed or not getattr(self.bus, "_running", True):
            raise RuntimeError("Chain device or bus is closed")

    def _i2c_header(self, address, register, length, addrsize):
        if not isinstance(address, int) or isinstance(address, bool):
            raise TypeError("address must be an integer")
        if not self._I2C_ADDR_MIN <= address <= self._I2C_ADDR_MAX:
            raise ValueError("address is out of range")
        if not isinstance(addrsize, int) or isinstance(addrsize, bool):
            raise TypeError("addrsize must be an integer")
        if not 8 <= addrsize <= 16:
            raise ValueError("addrsize is out of range")
        if addrsize not in (8, 16):
            raise ValueError("addrsize must be 8 or 16")
        if not isinstance(register, int) or isinstance(register, bool):
            raise TypeError("register must be an integer")
        if not 0 <= register <= (1 << addrsize) - 1:
            raise ValueError("register is out of range")
        if not isinstance(length, int) or isinstance(length, bool):
            raise TypeError("length must be an integer")
        if not 1 <= length <= self._I2C_MAX_LENGTH:
            raise ValueError("length is out of range")
        return struct.pack("<BBHB", address, addrsize // 8, register, length)

    def _on_event(self, payload):
        if self._closed or self._callback is None or len(payload) != 2:
            return
        if payload[1] == self._REPORT_TYPE:
            self._callback(payload[0])

    def get_uid(self, uid_type=0):
        """Read the device UID as bytes.

        :param int uid_type: 0 for four bytes, 1 for twelve bytes. Default: 0.
        :returns: UID bytes, or empty bytes if communication fails.
        :rtype: bytes
        """
        self._check_open()
        if not isinstance(uid_type, int) or isinstance(uid_type, bool):
            raise TypeError("uid_type must be an integer")
        if uid_type not in (0, 1):
            raise ValueError("uid_type must be 0 or 1")
        return bytes(self.get_device_uid(uid_type))

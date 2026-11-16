# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
from .chain import ChainBus
from .key import KeyChain


class ENVChain(KeyChain):
    """Driver for Chain ENV."""

    CMD_GET_I2C_MEM = 0x13
    CMD_WRITE_I2C_MEM = 0x14
    CMD_GET_TEMPERATURE_HUMIDITY = 0x30
    CMD_GET_PRESSURE_TEMPERATURE_ALTITUDE = 0x31
    CMD_SET_TEMPERATURE_RATE = 0x32
    CMD_GET_TEMPERATURE_RATE = 0x33
    CMD_SET_PRESSURE_RATE = 0x34
    CMD_GET_PRESSURE_RATE = 0x35
    CMD_SET_SEA_LEVEL_PRESSURE = 0x36
    CMD_GET_SEA_LEVEL_PRESSURE = 0x37
    CMD_REPORT_EVENT = 0xE0
    CMD_SET_ALARM_MODE = 0xE1
    CMD_GET_ALARM_MODE = 0xE2
    CMD_SET_TEMPERATURE_ALARM_THRESH = 0xE3
    CMD_GET_TEMPERATURE_ALARM_THRESH = 0xE4
    CMD_SET_HUMIDITY_ALARM_THRESH = 0xE5
    CMD_GET_HUMIDITY_ALARM_THRESH = 0xE6
    CMD_SET_PRESSURE_ALARM_THRESH = 0xE7
    CMD_GET_PRESSURE_ALARM_THRESH = 0xE8
    CMD_SET_ALTITUDE_ALARM_THRESH = 0xE9
    CMD_GET_ALTITUDE_ALARM_THRESH = 0xEA
    UID_4_BYTES = 0
    UID_12_BYTES = 1

    ODR_1HZ = 1
    ODR_1_5625HZ = 1.5625
    ODR_2HZ = 2
    ODR_3_125HZ = 3.125
    ODR_4HZ = 4
    ODR_6_25HZ = 6.25
    ODR_8HZ = 8
    ODR_12_5HZ = 12.5
    ODR_16HZ = 16
    ODR_25HZ = 25
    ODR_32HZ = 32
    ODR_50HZ = 50
    ODR_64HZ = 64
    ODR_100HZ = 100
    ODR_128HZ = 128
    ODR_200HZ = 200
    ODR_VALUES = (1, 1.5625, 2, 3.125, 4, 6.25, 8, 12.5, 16, 25, 32, 50, 64, 100, 128, 200)
    SENSOR_AHT20 = 0
    SENSOR_SPA06 = 1
    ALARM_NONE = 0
    ALARM_TEMPERATURE = 1
    ALARM_HUMIDITY = 2
    ALARM_PRESSURE = 4
    ALARM_ALTITUDE = 8
    ALARM_ALL = 15

    # Callback source selectors, not values from the 0xE0 status byte.
    EVENT_TEMPERATURE = ALARM_TEMPERATURE
    EVENT_HUMIDITY = ALARM_HUMIDITY
    EVENT_PRESSURE = ALARM_PRESSURE
    EVENT_ALTITUDE = ALARM_ALTITUDE
    _EVENT_MASKS = {1: 0x03, 2: 0x0C, 4: 0x30, 8: 0xC0}

    EVENT_TEMPERATURE_HIGH_CLEAR = 0x10
    EVENT_TEMPERATURE_HIGH = 0x11
    EVENT_TEMPERATURE_LOW = 0x12
    EVENT_TEMPERATURE_LOW_CLEAR = 0x13
    EVENT_HUMIDITY_HIGH_CLEAR = 0x20
    EVENT_HUMIDITY_HIGH = 0x21
    EVENT_HUMIDITY_LOW = 0x22
    EVENT_HUMIDITY_LOW_CLEAR = 0x23
    EVENT_PRESSURE_HIGH_CLEAR = 0x30
    EVENT_PRESSURE_HIGH = 0x31
    EVENT_PRESSURE_LOW = 0x32
    EVENT_PRESSURE_LOW_CLEAR = 0x33
    EVENT_ALTITUDE_HIGH_CLEAR = 0x40
    EVENT_ALTITUDE_HIGH = 0x41
    EVENT_ALTITUDE_LOW = 0x42
    EVENT_ALTITUDE_LOW_CLEAR = 0x43
    _EVENT_SOURCES = (ALARM_TEMPERATURE, ALARM_HUMIDITY, ALARM_PRESSURE, ALARM_ALTITUDE)

    _REPORT_TYPE = 0x0F
    _I2C_MAX_LENGTH = 32
    _I2C_ADDR_MIN = 0
    _I2C_ADDR_MAX = 127
    _TEMPERATURE_RATE = (
        ODR_1HZ,
        ODR_2HZ,
        ODR_4HZ,
        ODR_8HZ,
        ODR_16HZ,
        ODR_32HZ,
        ODR_64HZ,
        ODR_128HZ,
        ODR_1_5625HZ,
        ODR_3_125HZ,
        ODR_6_25HZ,
        ODR_12_5HZ,
        ODR_25HZ,
        ODR_50HZ,
        ODR_100HZ,
        ODR_200HZ,
    )
    _PRESSURE_RATE = (
        ODR_1HZ,
        ODR_2HZ,
        ODR_4HZ,
        ODR_8HZ,
        ODR_16HZ,
        ODR_32HZ,
        ODR_64HZ,
        ODR_128HZ,
        ODR_1_5625HZ,
        ODR_3_125HZ,
        ODR_6_25HZ,
        ODR_12_5HZ,
        ODR_25HZ,
        ODR_50HZ,
        ODR_100HZ,
        ODR_200HZ,
    )

    def __init__(self, bus: ChainBus, device_id: int):
        """Create a ENVChain on an existing ChainBus. Registration performs no device configuration. The caller owns the bus and must close it after all devices are detached.

        :param bus: An open shared ChainBus instance.
        :type bus: ChainBus
        :param device_id: Enumerated Chain position, 1..254.
        :type device_id: int
        :returns: A registered ENVChain object.
        :rtype: ENVChain

        UiFlow2 Code Block:

            |init.png|

        MicroPython Code Block:

            .. code-block:: python

                device = ENVChain(bus, 1)
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
        self._alarm_mode = None

    def read_temperature_humidity(self):
        """Read one AHT20 temperature and humidity sample.

        :returns: Tuple (temperature, humidity), in degrees Celsius and percent.
        :rtype: tuple

        UiFlow2 Code Block:

            |read_temperature_humidity.png|

        MicroPython Code Block:

            .. code-block:: python

                temperature, humidity = device.read_temperature_humidity()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_TEMPERATURE_HUMIDITY, b""
        )
        if not state or response is None or len(response) != 3:
            raise OSError("Invalid Chain response")
        temperature, humidity = struct.unpack("<hB", response)
        return (temperature / 100.0, humidity)

    def read_pressure_temperature_altitude(self):
        """Read one SPA06 sample. Altitude uses the configured sea-level pressure.

        :returns: Tuple (temperature, pressure, altitude), in degrees Celsius, Pa and metres. Pressure resolution is 10 Pa; altitude resolution is 0.01 m.
        :rtype: tuple

        UiFlow2 Code Block:

            |read_pressure_temperature_altitude.png|

        MicroPython Code Block:

            .. code-block:: python

                temperature, pressure, altitude = device.read_pressure_temperature_altitude()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_PRESSURE_TEMPERATURE_ALTITUDE, b""
        )
        if not state or response is None or len(response) != 8:
            raise OSError("Invalid Chain response")
        temperature, pressure, altitude = struct.unpack("<hHi", response)
        return (temperature / 100.0, pressure * 10, altitude / 100.0)

    def read_temperature(self, sensor=0):
        """Read temperature from the selected sensor.

        :param sensor: Temperature source: SENSOR_AHT20 (0) or SENSOR_SPA06 (1). Default: SENSOR_AHT20 (0).
        :type sensor: int
        :returns: Temperature in degrees Celsius, resolution 0.01 degrees.
        :rtype: float

        UiFlow2 Code Block:

            |read_temperature.png|

        MicroPython Code Block:

            .. code-block:: python

                temperature = device.read_temperature(ENVChain.SENSOR_AHT20)
        """
        if not isinstance(sensor, int) or isinstance(sensor, bool):
            raise TypeError("sensor must be an integer")
        if not 0 <= sensor <= 1:
            raise ValueError("sensor is out of range")
        return (
            self.read_temperature_humidity()[0]
            if sensor == self.SENSOR_AHT20
            else self.read_pressure_temperature_altitude()[0]
        )

    def read_humidity(self):
        """Read humidity.

        :returns: Relative humidity in percent, 0..100.
        :rtype: int

        UiFlow2 Code Block:

            |read_humidity.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.read_humidity()
        """
        return self.read_temperature_humidity()[1]

    def read_pressure(self):
        """Read pressure.

        :returns: Pressure in Pa, resolution 10 Pa.
        :rtype: int

        UiFlow2 Code Block:

            |read_pressure.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.read_pressure()
        """
        return self.read_pressure_temperature_altitude()[1]

    def read_altitude(self):
        """Read altitude.

        :returns: Altitude in metres, resolution 0.01 m.
        :rtype: float

        UiFlow2 Code Block:

            |read_altitude.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.read_altitude()
        """
        return self.read_pressure_temperature_altitude()[2]

    def set_temperature_rate(self, value):
        """Set SPA06 temperature sampling rate.

        :param value: An ODR_* constant in ODR_VALUES, in Hz; applies to SPA06 only.
        :type value: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_temperature_rate.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_temperature_rate(ENVChain.ODR_16HZ)
        """
        if type(value) not in (int, float):
            raise TypeError("value must be a number")
        if value not in self._TEMPERATURE_RATE:
            raise ValueError("value is not a supported setting")
        index = self._TEMPERATURE_RATE.index(value)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_TEMPERATURE_RATE, bytes((index,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_temperature_rate(self):
        """Get SPA06 temperature sampling rate.

        :returns: An ODR_* constant in ODR_VALUES, in Hz; applies to SPA06 only.
        :rtype: int or float

        UiFlow2 Code Block:

            |get_temperature_rate.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_temperature_rate()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_TEMPERATURE_RATE, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] >= len(self._TEMPERATURE_RATE):
            raise OSError("Chain returned an unknown setting")
        return self._TEMPERATURE_RATE[response[0]]

    def set_pressure_rate(self, value):
        """Set SPA06 pressure sampling rate.

        :param value: An ODR_* constant in ODR_VALUES, in Hz; applies to SPA06 only.
        :type value: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_pressure_rate.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_pressure_rate(ENVChain.ODR_16HZ)
        """
        if type(value) not in (int, float):
            raise TypeError("value must be a number")
        if value not in self._PRESSURE_RATE:
            raise ValueError("value is not a supported setting")
        index = self._PRESSURE_RATE.index(value)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_PRESSURE_RATE, bytes((index,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_pressure_rate(self):
        """Get SPA06 pressure sampling rate.

        :returns: An ODR_* constant in ODR_VALUES, in Hz; applies to SPA06 only.
        :rtype: int or float

        UiFlow2 Code Block:

            |get_pressure_rate.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_pressure_rate()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_PRESSURE_RATE, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] >= len(self._PRESSURE_RATE):
            raise OSError("Chain returned an unknown setting")
        return self._PRESSURE_RATE[response[0]]

    def set_sea_level_pressure(self, pressure):
        """Set the reference pressure for altitude calculation.

        :param pressure: Sea-level pressure in Pa, 70000..120000, in steps of 10 Pa.
        :type pressure: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_sea_level_pressure.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_sea_level_pressure(101330)
        """
        if type(pressure) not in (int, float):
            raise TypeError("pressure must be a number")
        if not 70000 <= pressure <= 120000:
            raise ValueError("pressure is out of range")
        if abs(pressure * 0.1 - round(pressure * 0.1)) > 1e-05:
            raise ValueError("pressure is not representable at the device resolution")
        raw = round(pressure * 0.1)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_SEA_LEVEL_PRESSURE, struct.pack("<H", raw)
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_sea_level_pressure(self):
        """Get the reference pressure for altitude calculation.

        :returns: Sea-level pressure in Pa, resolution 10 Pa.
        :rtype: int

        UiFlow2 Code Block:

            |get_sea_level_pressure.png|

        MicroPython Code Block:

            .. code-block:: python

                pressure = device.get_sea_level_pressure()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_SEA_LEVEL_PRESSURE, b""
        )
        if not state or response is None or len(response) != 2:
            raise OSError("Invalid Chain response")
        return struct.unpack("<H", response)[0] * 10

    def set_alarm_mode(self, mode):
        """Select the enabled alarm sources. Zero disables all alarms. Bits: 1 temperature, 2 humidity, 4 pressure, 8 altitude.

        :param mode: Alarm bitmask, 0..15; combine ALARM_* bits with ``|``, use ALARM_NONE to disable or ALARM_ALL to enable all sources.
        :type mode: int
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_alarm_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_alarm_mode(ENVChain.ALARM_ALL)
        """
        if not isinstance(mode, int) or isinstance(mode, bool):
            raise TypeError("mode must be an integer")
        if not 0 <= mode <= 15:
            raise ValueError("mode is out of range")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_ALARM_MODE, bytes((mode,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")
        self._alarm_mode = mode

    def get_alarm_mode(self):
        """Get the enabled alarm sources.

        :returns: Alarm bitmask, 0..15; combine ALARM_* bits with ``|``, use ALARM_NONE to disable or ALARM_ALL to enable all sources.
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
        mode = response[0]
        self._alarm_mode = mode
        return mode

    def set_temperature_alarm_thresh(self, low, high, sensor=0):
        """Set the temperature alarm window and source.

        :param low: Lower temperature in degrees Celsius, 0..255; less than high.
        :type low: int
        :param high: Upper temperature in degrees Celsius, 0..255; greater than low.
        :type high: int
        :param sensor: Temperature source: SENSOR_AHT20 (0) or SENSOR_SPA06 (1). Default: SENSOR_AHT20 (0).
        :type sensor: int
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
        if not isinstance(high, int) or isinstance(high, bool):
            raise TypeError("high must be an integer")
        if not 0 <= high <= 255:
            raise ValueError("high is out of range")
        if not isinstance(sensor, int) or isinstance(sensor, bool):
            raise TypeError("sensor must be an integer")
        if not 0 <= sensor <= 1:
            raise ValueError("sensor is out of range")
        if low >= high:
            raise ValueError("low must be less than high")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_TEMPERATURE_ALARM_THRESH, bytes((sensor, low, high))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_temperature_alarm_thresh(self):
        """Get the temperature alarm window and source.

        :returns: Tuple (low, high, sensor); temperatures in degrees Celsius.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_temperature_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                low, high, sensor = device.get_temperature_alarm_thresh()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_TEMPERATURE_ALARM_THRESH, b""
        )
        if not state or response is None or len(response) != 3:
            raise OSError("Invalid Chain response")
        sensor, low, high = struct.unpack("<BBB", response)
        return (low, high, sensor)

    def set_humidity_alarm_thresh(self, low, high):
        """Set the humidity alarm window.

        :param low: Relative humidity in percent. Range: 0..100; low must be less than high.
        :type low: int
        :param high: Relative humidity in percent. Range: 0..100; low must be less than high.
        :type high: int
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_humidity_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_humidity_alarm_thresh(20, 80)
        """
        if not isinstance(low, int) or isinstance(low, bool):
            raise TypeError("low must be an integer")
        if not 0 <= low <= 100:
            raise ValueError("low is out of range")
        low_raw = low
        if not isinstance(high, int) or isinstance(high, bool):
            raise TypeError("high must be an integer")
        if not 0 <= high <= 100:
            raise ValueError("high is out of range")
        high_raw = high
        if low_raw >= high_raw:
            raise ValueError("low must be less than high")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id,
            self.CMD_SET_HUMIDITY_ALARM_THRESH,
            struct.pack("<BB", low_raw, high_raw),
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_humidity_alarm_thresh(self):
        """Get the humidity alarm window.

        :returns: Tuple (low, high). Relative humidity in percent.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_humidity_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                low, high = device.get_humidity_alarm_thresh()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_HUMIDITY_ALARM_THRESH, b""
        )
        if not state or response is None or len(response) != 2:
            raise OSError("Invalid Chain response")
        low, high = struct.unpack("<BB", response)
        return (low, high)

    def set_pressure_alarm_thresh(self, low, high):
        """Set the pressure alarm window.

        :param low: Pressure in Pa, resolution 10 Pa. Range: 70000..120000; low must be less than high.
        :type low: int or float
        :param high: Pressure in Pa, resolution 10 Pa. Range: 70000..120000; low must be less than high.
        :type high: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_pressure_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_pressure_alarm_thresh(95000, 105000)
        """
        if type(low) not in (int, float):
            raise TypeError("low must be a number")
        if not 70000 <= low <= 120000:
            raise ValueError("low is out of range")
        if abs(low * 0.1 - round(low * 0.1)) > 1e-05:
            raise ValueError("low is not representable at the device resolution")
        low_raw = round(low * 0.1)
        if type(high) not in (int, float):
            raise TypeError("high must be a number")
        if not 70000 <= high <= 120000:
            raise ValueError("high is out of range")
        if abs(high * 0.1 - round(high * 0.1)) > 1e-05:
            raise ValueError("high is not representable at the device resolution")
        high_raw = round(high * 0.1)
        if low_raw >= high_raw:
            raise ValueError("low must be less than high")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id,
            self.CMD_SET_PRESSURE_ALARM_THRESH,
            struct.pack("<HH", low_raw, high_raw),
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_pressure_alarm_thresh(self):
        """Get the pressure alarm window.

        :returns: Tuple (low, high). Pressure in Pa, resolution 10 Pa.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_pressure_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                low, high = device.get_pressure_alarm_thresh()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_PRESSURE_ALARM_THRESH, b""
        )
        if not state or response is None or len(response) != 4:
            raise OSError("Invalid Chain response")
        low, high = struct.unpack("<HH", response)
        return (low / 0.1, high / 0.1)

    def set_altitude_alarm_thresh(self, low, high):
        """Set the altitude alarm window.

        :param low: Altitude in metres, resolution 0.01 m. Range: -21474836.48..21474836.47; low must be less than high.
        :type low: int or float
        :param high: Altitude in metres, resolution 0.01 m. Range: -21474836.48..21474836.47; low must be less than high.
        :type high: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_altitude_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_altitude_alarm_thresh(0, 1000)
        """
        if type(low) not in (int, float):
            raise TypeError("low must be a number")
        if not -21474836.48 <= low <= 21474836.47:
            raise ValueError("low is out of range")
        if abs(low * 100 - round(low * 100)) > 1e-05:
            raise ValueError("low is not representable at the device resolution")
        low_raw = round(low * 100)
        if type(high) not in (int, float):
            raise TypeError("high must be a number")
        if not -21474836.48 <= high <= 21474836.47:
            raise ValueError("high is out of range")
        if abs(high * 100 - round(high * 100)) > 1e-05:
            raise ValueError("high is not representable at the device resolution")
        high_raw = round(high * 100)
        if low_raw >= high_raw:
            raise ValueError("low must be less than high")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id,
            self.CMD_SET_ALTITUDE_ALARM_THRESH,
            struct.pack("<ii", low_raw, high_raw),
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_altitude_alarm_thresh(self):
        """Get the altitude alarm window.

        :returns: Tuple (low, high). Altitude in metres, resolution 0.01 m.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_altitude_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                low, high = device.get_altitude_alarm_thresh()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_ALTITUDE_ALARM_THRESH, b""
        )
        if not state or response is None or len(response) != 8:
            raise OSError("Invalid Chain response")
        low, high = struct.unpack("<ii", response)
        return (low / 100, high / 100)

    def deinit(self):
        """Detach the device and release its callbacks; the shared bus stays open.

        :returns: None. Repeated calls are safe.
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

    def _dispatch_env_event(self, status):
        # A zero field is indistinguishable from an unchanged source. A zero
        # report can be routed only when exactly one alarm source is enabled.
        for event, callback in tuple(self._event_callbacks.items()):
            if event in self._EVENT_MASKS:
                if status & self._EVENT_MASKS[event] or (
                    status == 0 and self._alarm_mode == event
                ):
                    callback(status)
            else:
                source_index = (event >> 4) - 1
                code = (status >> (source_index * 2)) & 3
                if code == (event & 3) and (
                    code != 0
                    or (status == 0 and self._alarm_mode == self._EVENT_SOURCES[source_index])
                ):
                    callback(event)

    def set_event_callback(self, event=None, callback=None):
        """Register a high, low, high-clear or low-clear alarm callback.

        Use EVENT_<SOURCE>_HIGH, LOW, HIGH_CLEAR or LOW_CLEAR. Each handler
        receives its selected event constant. Register before enabling alarms.
        Registration does not change hardware settings. Perform I/O in the loop.
        HIGH_CLEAR requires only that source enabled via set/get_alarm_mode();
        its source cannot be identified with multiple alarms enabled.
        Legacy source selectors and the single-callback form receive raw status.

        :param event: An EVENT_* constant, legacy callback or None. Default None.
            None clears all handlers.
        :type event: int or callable or None
        :param callback: Handler receiving the selected event constant.
            Default None removes the selected source's handler.
        :type callback: callable or None
        :returns: None. Each source's handler can be replaced independently.
        :rtype: None

        UiFlow2 Code Block:

            |event_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_event_callback(ENVChain.EVENT_HUMIDITY_HIGH, on_humidity)
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
            self._callback = callback
        else:
            if not isinstance(event, int) or isinstance(event, bool):
                raise TypeError("event must be an integer")
            if event not in self._EVENT_MASKS and (
                not (1 <= event >> 4 <= 4 and 0 <= event & 15 <= 3)
            ):
                raise ValueError("event is not a supported ENV event type")
            if callback is not None and (not callable(callback)):
                raise TypeError("callback must be callable or None")
            if callback is None:
                self._event_callbacks.pop(event, None)
            else:
                self._event_callbacks[event] = callback
            self._callback = self._dispatch_env_event if self._event_callbacks else None
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

        :param address: Seven-bit internal I2C address, 0..127.
        :type address: int
        :param register: Register address, 0..255 for addrsize=8 or 0..65535 for addrsize=16.
        :type register: int
        :param length: Number of bytes, 1..32.
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

        :param address: Seven-bit internal I2C address, 0..127.
        :type address: int
        :param register: Register address, 0..255 for addrsize=8 or 0..65535 for addrsize=16.
        :type register: int
        :param data: Buffer containing 1..32 bytes.
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

    set_temperature_thresholds = set_temperature_alarm_thresh

    get_temperature_thresholds = get_temperature_alarm_thresh

    set_humidity_thresholds = set_humidity_alarm_thresh

    get_humidity_thresholds = get_humidity_alarm_thresh

    set_pressure_thresholds = set_pressure_alarm_thresh

    get_pressure_thresholds = get_pressure_alarm_thresh

    set_altitude_thresholds = set_altitude_alarm_thresh

    get_altitude_thresholds = get_altitude_alarm_thresh

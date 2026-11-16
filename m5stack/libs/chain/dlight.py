# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
from .chain import ChainBus
from .key import KeyChain


class DLightChain(KeyChain):
    """Driver for Chain DLight."""

    CMD_GET_I2C_MEM = 0x13
    CMD_WRITE_I2C_MEM = 0x14
    CMD_GET_LUX = 0x30
    CMD_SET_THRESHOLD_DETECTION = 0x31
    CMD_GET_THRESHOLD_DETECTION_ENABLED = 0x32
    CMD_SET_ALARM_THRESH = 0x33
    CMD_GET_ALARM_THRESH = 0x34
    CMD_SET_GAIN = 0x35
    CMD_GET_GAIN = 0x36
    CMD_SET_RESOLUTION = 0x37
    CMD_GET_RESOLUTION = 0x38
    CMD_SET_MEASUREMENT_INTERVAL_MS = 0x39
    CMD_GET_MEASUREMENT_INTERVAL_MS = 0x3A
    CMD_REPORT_EVENT = 0xE0
    CMD_SET_EVENT_REPORTING = 0xE1
    CMD_GET_EVENT_REPORTING_ENABLED = 0xE2
    UID_4_BYTES = 0
    UID_12_BYTES = 1

    GAIN_1X = 1
    GAIN_3X = 3
    GAIN_6X = 6
    GAIN_9X = 9
    GAIN_18X = 18
    RESOLUTION_16BIT = 16
    RESOLUTION_17BIT = 17
    RESOLUTION_18BIT = 18
    RESOLUTION_19BIT = 19
    RESOLUTION_20BIT = 20
    MEASUREMENT_INTERVAL_50MS = 50
    MEASUREMENT_INTERVAL_100MS = 100
    MEASUREMENT_INTERVAL_500MS = 500
    MEASUREMENT_INTERVAL_1000MS = 1000
    MEASUREMENT_INTERVAL_2000MS = 2000
    EVENT_LOW = 0
    EVENT_HIGH = 1

    _REPORT_TYPE = 0x11
    _I2C_MAX_LENGTH = 64
    _I2C_ADDR_MIN = 0x08
    _I2C_ADDR_MAX = 0x77
    _GAIN = (GAIN_1X, GAIN_3X, GAIN_6X, GAIN_9X, GAIN_18X)
    _RESOLUTION = (
        RESOLUTION_20BIT,
        RESOLUTION_19BIT,
        RESOLUTION_18BIT,
        RESOLUTION_17BIT,
        RESOLUTION_16BIT,
    )
    _MEASUREMENT_INTERVAL_MS = (
        25,
        MEASUREMENT_INTERVAL_50MS,
        MEASUREMENT_INTERVAL_100MS,
        MEASUREMENT_INTERVAL_500MS,
        MEASUREMENT_INTERVAL_1000MS,
        MEASUREMENT_INTERVAL_2000MS,
    )

    def __init__(self, bus: ChainBus, device_id: int):
        """Create a DLightChain on an existing ChainBus. Registration performs no device configuration. The caller owns the bus and must close it after all devices are detached.

        :param bus: An open shared ChainBus instance.
        :type bus: ChainBus
        :param device_id: Enumerated Chain position, 1..254.
        :type device_id: int
        :returns: A registered DLightChain object.
        :rtype: DLightChain

        UiFlow2 Code Block:

            |init.png|

        MicroPython Code Block:

            .. code-block:: python

                device = DLightChain(bus, 1)
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

    def deinit(self):
        """Detach the device and release all callbacks; the shared bus stays open.

        Repeated calls are safe. Returns None.

        UiFlow2 Code Block:

            |deinit.png|
        """
        self._closed = True
        self._callback = None
        self.bus._event.pop(self, None)
        if self in self.bus._device:
            self.bus._device.remove(self)
        self._event_callbacks.clear()

    def _dispatch_threshold_event(self, event):
        callback = self._event_callbacks.get(event)
        if callback is not None:
            callback(event)

    def read_lux(self):
        """Read the most recent illuminance sample. The firmware returns its cached sample.

        :returns: Illuminance in lux, 0..2516580.
        :rtype: int

        UiFlow2 Code Block:

            |read_lux.png|

        MicroPython Code Block:

            .. code-block:: python

                lux = device.read_lux()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_LUX, b"")
        if not state or response is None or len(response) != 4:
            raise OSError("Invalid Chain response")
        return struct.unpack("<I", response)[0]

    def enable_threshold_detection(self):
        """Enable sensor threshold detection; changing this gate resets the firmware threshold history. Repeated calls are safe. The setting is volatile.

        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |enable_threshold_detection.png|

        MicroPython Code Block:

            .. code-block:: python

                device.enable_threshold_detection()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_THRESHOLD_DETECTION, b"\x01"
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def disable_threshold_detection(self):
        """Disable sensor threshold detection; changing this gate resets the firmware threshold history. Repeated calls are safe. The setting is volatile.

        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |enable_threshold_detection.png|

        MicroPython Code Block:

            .. code-block:: python

                device.disable_threshold_detection()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_THRESHOLD_DETECTION, b"\x00"
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def is_threshold_detection_enabled(self):
        """Check whether sensor threshold detection is enabled.

        :returns: True if enabled, otherwise False.
        :rtype: bool

        UiFlow2 Code Block:

            |is_threshold_detection_enabled.png|

        MicroPython Code Block:

            .. code-block:: python

                enabled = device.is_threshold_detection_enabled()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_THRESHOLD_DETECTION_ENABLED, b""
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] not in (0, 1):
            raise OSError("Chain returned an invalid boolean state")
        return bool(response[0])

    def set_alarm_thresh(self, low, high):
        """Set the illuminance alarm threshold window. The firmware briefly restarts measurement and resets the threshold history. The setting is volatile.

        :param low: Lower threshold in lux, 0..2516580; must be less than high.
        :type low: int
        :param high: Upper threshold in lux, 0..2516580; must be greater than low.
        :type high: int
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_alarm_thresh(100, 1000)
        """
        if not isinstance(low, int) or isinstance(low, bool):
            raise TypeError("low must be an integer")
        if not 0 <= low <= 2516580:
            raise ValueError("low is out of range")
        if not isinstance(high, int) or isinstance(high, bool):
            raise TypeError("high must be an integer")
        if not 0 <= high <= 2516580:
            raise ValueError("high is out of range")
        if low >= high:
            raise ValueError("low must be less than high")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_ALARM_THRESH, struct.pack("<II", high, low)
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_alarm_thresh(self):
        """Get the configured illuminance alarm threshold window.

        :returns: Tuple (low, high), in lux.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_alarm_thresh.png|

        MicroPython Code Block:

            .. code-block:: python

                low, high = device.get_alarm_thresh()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_ALARM_THRESH, b"")
        if not state or response is None or len(response) != 8:
            raise OSError("Invalid Chain response")
        high, low = struct.unpack("<II", response)
        return (low, high)

    def set_gain(self, value):
        """Set measurement gain. The setting is volatile. Measurement restarts and thresholds are reapplied.

        :param value: Gain multiplier: GAIN_1X, GAIN_3X, GAIN_6X, GAIN_9X or GAIN_18X.
        :type value: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_gain.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_gain(DLightChain.GAIN_1X)
        """
        if type(value) not in (int, float):
            raise TypeError("value must be a number")
        if value not in self._GAIN:
            raise ValueError("value is not a supported setting")
        index = self._GAIN.index(value)
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_SET_GAIN, bytes((index,)))
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_gain(self):
        """Get measurement gain.

        :returns: Gain multiplier: GAIN_1X, GAIN_3X, GAIN_6X, GAIN_9X or GAIN_18X.
        :rtype: int

        UiFlow2 Code Block:

            |get_gain.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_gain()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_GAIN, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] >= len(self._GAIN):
            raise OSError("Chain returned an unknown setting")
        return self._GAIN[response[0]]

    def set_resolution(self, value):
        """Set measurement resolution. The setting is volatile. The current interval must strictly exceed the conversion time: 16/17/18/19/20 bits require 25/50/100/200/400 ms respectively. The firmware rejects incompatible combinations.

        :param value: A RESOLUTION_*BIT constant, in bits: 16, 17, 18, 19 or 20.
        :type value: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_resolution.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_measurement_interval_ms(DLightChain.MEASUREMENT_INTERVAL_500MS)
                device.set_resolution(DLightChain.RESOLUTION_20BIT)
        """
        if type(value) not in (int, float):
            raise TypeError("value must be a number")
        if value not in self._RESOLUTION:
            raise ValueError("value is not a supported setting")
        index = self._RESOLUTION.index(value)
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_RESOLUTION, bytes((index,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_resolution(self):
        """Get measurement resolution.

        :returns: A RESOLUTION_*BIT constant, in bits: 16, 17, 18, 19 or 20.
        :rtype: int

        UiFlow2 Code Block:

            |get_resolution.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_resolution()
        """
        self._check_open()
        state, response = self.bus.chainll.send(self.device_id, self.CMD_GET_RESOLUTION, b"")
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] >= len(self._RESOLUTION):
            raise OSError("Chain returned an unknown setting")
        return self._RESOLUTION[response[0]]

    def set_measurement_interval_ms(self, value):
        """Set measurement interval. The setting is volatile. The interval must strictly exceed the conversion time: 20/19/18/17/16 bits require 400/200/100/50/25 ms respectively. Use 500 ms or longer for any resolution. The unsupported 25 ms setting is rejected before I/O.

        :param value: A MEASUREMENT_INTERVAL_*MS constant: 50, 100, 500, 1000 or 2000 ms.
        :type value: int or float
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |set_measurement_interval_ms.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_measurement_interval_ms(DLightChain.MEASUREMENT_INTERVAL_500MS)
        """
        if type(value) not in (int, float):
            raise TypeError("value must be a number")
        if value not in self._MEASUREMENT_INTERVAL_MS:
            raise ValueError("value is not a supported setting")
        index = self._MEASUREMENT_INTERVAL_MS.index(value)
        if index == 0:
            raise ValueError("25 ms is not supported by the DLight firmware")
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_MEASUREMENT_INTERVAL_MS, bytes((index,))
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def get_measurement_interval_ms(self):
        """Get measurement interval.

        :returns: Interval in milliseconds. Allowed: (25, 50, 100, 500, 1000, 2000).
        :rtype: int

        UiFlow2 Code Block:

            |get_measurement_interval_ms.png|

        MicroPython Code Block:

            .. code-block:: python

                value = device.get_measurement_interval_ms()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_MEASUREMENT_INTERVAL_MS, b""
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] >= len(self._MEASUREMENT_INTERVAL_MS):
            raise OSError("Chain returned an unknown setting")
        return self._MEASUREMENT_INTERVAL_MS[response[0]]

    def enable_event_reporting(self):
        """Enable threshold event reporting; sensor threshold detection must also be enabled. Repeated calls are safe. The setting is volatile.

        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |enable_event_reporting.png|

        MicroPython Code Block:

            .. code-block:: python

                device.enable_event_reporting()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_EVENT_REPORTING, b"\x01"
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def disable_event_reporting(self):
        """Disable threshold event reporting. Repeated calls are safe. The setting is volatile.

        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |enable_event_reporting.png|

        MicroPython Code Block:

            .. code-block:: python

                device.disable_event_reporting()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_SET_EVENT_REPORTING, b"\x00"
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] != 1:
            raise OSError("Chain command failed")

    def is_event_reporting_enabled(self):
        """Check whether threshold event reporting is enabled. Events require both reporting and threshold detection to be enabled.

        :returns: True if enabled, otherwise False.
        :rtype: bool

        UiFlow2 Code Block:

            |is_event_reporting_enabled.png|

        MicroPython Code Block:

            .. code-block:: python

                enabled = device.is_event_reporting_enabled()
        """
        self._check_open()
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_GET_EVENT_REPORTING_ENABLED, b""
        )
        if not state or response is None or len(response) != 1:
            raise OSError("Invalid Chain response")
        if response[0] not in (0, 1):
            raise OSError("Chain returned an invalid boolean state")
        return bool(response[0])

    def set_event_callback(self, event=None, callback=None):
        """Register a threshold callback without changing hardware reporting gates.

        set_event_callback(EVENT_LOW/HIGH, callback) replaces only that event's
        handler; None removes it. Callbacks receive the event integer. The legacy
        set_event_callback(callback) form replaces all handlers with one handler
        for both events; set_event_callback(None) removes all handlers. The two
        forms replace one another. Do not call Chain methods inside a callback.

        :param event: EVENT_LOW (0), EVENT_HIGH (1), or a legacy callback/None.
        :type event: int or callable or None
        :param callback: Event handler, or the legacy keyword handler when event is None.
        :type callback: callable or None
        :returns: No return value.
        :rtype: None

        UiFlow2 Code Block:

            |event_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                device.set_event_callback(lambda event: print(event))
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
            if event not in (self.EVENT_LOW, self.EVENT_HIGH):
                raise ValueError("event is not a supported DLight event type")
            if callback is not None and (not callable(callback)):
                raise TypeError("callback must be callable or None")
            if callback is None:
                self._event_callbacks.pop(event, None)
            else:
                self._event_callbacks[event] = callback
            self._callback = self._dispatch_threshold_event if self._event_callbacks else None
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

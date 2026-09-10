# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
from .chain import ChainBus
from .key import KeyChain


class Servos8V2Chain(KeyChain):
    """Unit 8Servos2 Chain device.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import Servos8V2Chain

            bus2 = ChainBus(2, tx=21, rx=22)
            servos8v2_0 = Servos8V2Chain(bus2, 1)
    """

    CMD_SET_MODE = 0x10                # Set one channel mode.
    CMD_GET_MODE = 0x12                # Get one channel mode.
    CMD_SET_INPUT_PULL = 0x30          # Set one input pull-up/down config.
    CMD_GET_INPUT_PULL = 0x32          # Get one input pull-up/down config.
    CMD_GET_INPUT_LEVEL = 0x34         # Get one input level.
    CMD_SET_OUTPUT_LEVEL = 0x40        # Set one output level.
    CMD_GET_OUTPUT_LEVEL = 0x42        # Get one output level.
    CMD_GET_ADC = 0x50                 # Get one 12-bit ADC value.
    CMD_SET_SERVO_ANGLE = 0x60         # Set one servo angle.
    CMD_GET_SERVO_ANGLE = 0x62         # Get one servo angle.
    CMD_SET_RGB_CONFIG = 0x70          # Set one WS2812 count/refresh config.
    CMD_GET_RGB_CONFIG = 0x72          # Get one WS2812 count/refresh config.
    CMD_SET_RGB_BUFFER = 0x74          # Set one WS2812 color buffer entry.
    CMD_GET_RGB_BUFFER = 0x76          # Get one WS2812 color buffer entry.
    CMD_SET_PWM_DUTY = 0x80            # Set one PWM duty value.
    CMD_GET_PWM_DUTY = 0x82            # Get one PWM duty value.
    CMD_SET_TIMER_FREQ = 0x90          # Set one timer group frequency.
    CMD_GET_TIMER_FREQ = 0x92          # Get one timer group frequency.
    CMD_GET_REFERENCE_VOLTAGE = 0xA0   # Get reference voltage in mV.
    CMD_GET_GROVE_VOLTAGE = 0xA1       # Get Grove voltage in mV.
    CMD_GET_DC_VOLTAGE = 0xA2          # Get DC input voltage in mV.
    CMD_GET_CURRENT = 0xA3             # Get system current in mA.
    CMD_GET_UID = 0xF8                 # Get 4-byte or 12-byte device UID.
    CMD_GET_BOOTLOADER_VERSION = 0xF9  # Get bootloader version.
    CMD_GET_FIRMWARE_VERSION = 0xFA    # Get firmware version.
    CMD_GET_DEVICE_TYPE = 0xFB         # Get Chain device type.

    DEVICE_TYPE = 0x000C  # Unit 8Servos2 Chain device type.

    MODE_INPUT = 0x00   # GPIO input mode.
    MODE_OUTPUT = 0x01  # GPIO output mode.
    MODE_ADC = 0x02     # ADC input mode.
    MODE_SERVO = 0x03   # Servo angle output mode.
    MODE_RGB = 0x04     # RGB WS2812 data output mode.
    MODE_PWM = 0x05     # PWM duty output mode.

    PULL_NONE = 0  # Disable input pull resistor.
    PULL_UP = 1    # Enable input pull-up.
    PULL_DOWN = 2  # Enable input pull-down.

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    def _limit(self, value: int, minimum: int, maximum: int) -> int:
        value = int(value)
        if value < minimum:
            return minimum
        if value > maximum:
            return maximum
        return value

    def _check_channel(self, channel: int) -> int:
        if not 0 <= channel <= 7:
            raise ValueError("channel must be in range 0-7")
        return channel

    def _timer_for_channel(self, channel: int) -> int:
        channel = self._check_channel(channel)
        return 0 if channel < 4 else 1

    def _send_status(self, cmd: int, payload: bytes = bytes()) -> bool:
        state, response = self.bus.chainll.send(self.device_id, cmd, payload)
        return bool(state and response and response[0] == 1)

    def _send_status_payload(self, cmd: int, payload: bytes = bytes()):
        state, response = self.bus.chainll.send(self.device_id, cmd, payload)
        if state and response and response[0] == 1:
            return response[1:]
        return None

    def _send_payload(self, cmd: int, payload: bytes = bytes()):
        state, response = self.bus.chainll.send(self.device_id, cmd, payload)
        if state:
            return response
        return None

    def get_channel_mode(self, channel: int) -> int:
        """Get the current mode of a specific channel.

        The channel mode values:

        - ``MODE_INPUT``: ``0x00``
        - ``MODE_OUTPUT``: ``0x01``
        - ``MODE_ADC``: ``0x02``
        - ``MODE_SERVO``: ``0x03``
        - ``MODE_RGB``: ``0x04``
        - ``MODE_PWM``: ``0x05``

        :param int channel: The channel number (0 to 7).
        :return: The mode of the specified channel.
        :rtype: int

        UiFlow2 Code Block:

            |get_channel_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = servos8v2_0.get_channel_mode(0)
        """
        channel = self._check_channel(channel)
        response = self._send_status_payload(self.CMD_GET_MODE, bytes([channel]))
        if response and len(response) >= 1:
            return response[0]
        return None

    def set_channel_mode(self, channel: int, mode: int) -> bool:
        """Set the mode of a specific channel.

        The channel mode values:

        - ``MODE_INPUT``: ``0x00``
        - ``MODE_OUTPUT``: ``0x01``
        - ``MODE_ADC``: ``0x02``
        - ``MODE_SERVO``: ``0x03``
        - ``MODE_RGB``: ``0x04``
        - ``MODE_PWM``: ``0x05``

        When a channel is set to ``MODE_SERVO``, the driver automatically sets
        its shared frequency group to 50 Hz. Channels 0-3 share one frequency,
        and channels 4-7 share another frequency.

        :param int channel: The channel number (0 to 7).
        :param int mode: The channel mode to set.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_channel_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_channel_mode(0, Servos8V2Chain.MODE_SERVO)
        """
        channel = self._check_channel(channel)
        mode = self._limit(mode, self.MODE_INPUT, self.MODE_PWM)
        if not self._send_status(self.CMD_SET_MODE, bytes([channel, mode])):
            return False
        if mode == self.MODE_SERVO:
            return self._set_timer_freq(self._timer_for_channel(channel), 50)
        return True

    def set_input_pull(self, channel: int, pull: int) -> bool:
        """Set the input pull configuration of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param int pull: Pull configuration. Use PULL_NONE, PULL_UP, or PULL_DOWN.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_input_pull.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_input_pull(0, Servos8V2Chain.PULL_UP)
        """
        channel = self._check_channel(channel)
        pull = self._limit(pull, self.PULL_NONE, self.PULL_DOWN)
        return self._send_status(self.CMD_SET_INPUT_PULL, bytes([channel, pull]))

    def get_input_pull(self, channel: int) -> int:
        """Get the input pull configuration of a specific channel.

        :param int channel: The channel number (0 to 7).
        :return: Pull configuration of the specified channel.
        :rtype: int

        UiFlow2 Code Block:

            |get_input_pull.png|

        MicroPython Code Block:

            .. code-block:: python

                pull = servos8v2_0.get_input_pull(0)
        """
        channel = self._check_channel(channel)
        response = self._send_status_payload(self.CMD_GET_INPUT_PULL, bytes([channel]))
        if response and len(response) >= 1:
            return response[0]
        return None

    def get_gpio_input_value(self, channel: int) -> bool:
        """Get the GPIO input value of a specific channel.

        :param int channel: The channel number (0 to 7).
        :return: True for high level, False for low level.
        :rtype: bool

        UiFlow2 Code Block:

            |get_gpio_input_value.png|

        MicroPython Code Block:

            .. code-block:: python

                level = servos8v2_0.get_gpio_input_value(0)
        """
        channel = self._check_channel(channel)
        response = self._send_status_payload(self.CMD_GET_INPUT_LEVEL, bytes([channel]))
        if response and len(response) >= 1:
            return response[0] == 1
        return None

    def set_gpio_output_value(self, channel: int, value: bool) -> bool:
        """Set the GPIO output value of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param bool value: Output value, False for low level or True for high level.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_gpio_output_value.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_gpio_output_value(0, True)
        """
        channel = self._check_channel(channel)
        return self._send_status(self.CMD_SET_OUTPUT_LEVEL, bytes([channel, 1 if value else 0]))

    def get_gpio_output_value(self, channel: int) -> bool:
        """Get the GPIO output value of a specific channel.

        :param int channel: The channel number (0 to 7).
        :return: True for high level, False for low level.
        :rtype: bool

        UiFlow2 Code Block:

            |get_gpio_output_value.png|

        MicroPython Code Block:

            .. code-block:: python

                level = servos8v2_0.get_gpio_output_value(0)
        """
        channel = self._check_channel(channel)
        response = self._send_status_payload(self.CMD_GET_OUTPUT_LEVEL, bytes([channel]))
        if response and len(response) >= 1:
            return response[0] == 1
        return None

    def get_adc_input(self, channel: int) -> int:
        """Get the 12-bit ADC input value of a specific channel.

        :param int channel: The channel number (0 to 7).
        :return: ADC value, range 0 to 4095.
        :rtype: int

        UiFlow2 Code Block:

            |get_adc_input.png|

        MicroPython Code Block:

            .. code-block:: python

                adc = servos8v2_0.get_adc_input(0)
        """
        channel = self._check_channel(channel)
        response = self._send_status_payload(self.CMD_GET_ADC, bytes([channel]))
        if response and len(response) >= 2:
            return struct.unpack("<H", response[:2])[0]
        return None

    def set_servo_angle(self, channel: int, angle: int) -> bool:
        """Set the servo angle of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param int angle: Servo angle, range 0 to 180.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_servo_angle(0, 90)
        """
        channel = self._check_channel(channel)
        angle = self._limit(angle, 0, 180)
        return self._send_status(self.CMD_SET_SERVO_ANGLE, bytes([channel, angle]))

    def get_servo_angle(self, channel: int) -> int:
        """Get the servo angle of a specific channel.

        :param int channel: The channel number (0 to 7).
        :return: Servo angle, range 0 to 180.
        :rtype: int

        UiFlow2 Code Block:

            |get_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                angle = servos8v2_0.get_servo_angle(0)
        """
        channel = self._check_channel(channel)
        response = self._send_status_payload(self.CMD_GET_SERVO_ANGLE, bytes([channel]))
        if response and len(response) >= 1:
            return response[0]
        return None

    def _pack_rgb_config(self, count: int, refresh: bool = False) -> int:
        count = self._limit(count, 0, 16)
        return (0x20 if refresh else 0x00) | (count & 0x1F)

    def set_rgb_config(self, channel: int, count: int, refresh: bool = False) -> bool:
        """Set the WS2812 LED count and refresh flag of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param int count: WS2812 LED count, range 0 to 16.
        :param bool refresh: Whether to trigger an RGB refresh. Default is False.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_rgb_config.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_rgb_config(0, 4, refresh=True)
        """
        channel = self._check_channel(channel)
        return self._send_status(
            self.CMD_SET_RGB_CONFIG, bytes([channel, self._pack_rgb_config(count, refresh)])
        )

    def get_rgb_config(self, channel: int) -> int:
        """Get the raw WS2812 config value of a specific channel.

        :param int channel: The channel number (0 to 7).
        :return: Raw RGB config byte.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_config.png|

        MicroPython Code Block:

            .. code-block:: python

                config = servos8v2_0.get_rgb_config(0)
        """
        channel = self._check_channel(channel)
        response = self._send_status_payload(self.CMD_GET_RGB_CONFIG, bytes([channel]))
        if response and len(response) >= 1:
            return response[0]
        return None

    def get_rgb_count(self, channel: int) -> int:
        """Get the configured WS2812 LED count of a specific channel.

        :param int channel: The channel number (0 to 7).
        :return: WS2812 LED count, range 0 to 16.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_count.png|

        MicroPython Code Block:

            .. code-block:: python

                count = servos8v2_0.get_rgb_count(0)
        """
        config = self.get_rgb_config(channel)
        if config is None:
            return None
        return config & 0x1F

    def refresh_rgb(self, channel: int) -> bool:
        """Trigger WS2812 refresh for a specific channel.

        :param int channel: The channel number (0 to 7).

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |refresh_rgb.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.refresh_rgb(0)
        """
        count = self.get_rgb_count(channel)
        if count is None:
            return False
        return self.set_rgb_config(channel, count, refresh=True)

    def _color_to_rgb(self, color: int) -> tuple:
        color = self._limit(color, 0, 0xFFFFFF)
        return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)

    def _rgb_to_color(self, data) -> int:
        return (data[0] << 16) | (data[1] << 8) | data[2]

    def set_rgb_buffer(self, index: int, color: int) -> bool:
        """Set one WS2812 color buffer entry.

        :param int index: WS2812 color buffer index, range 0 to 15.
        :param int color: RGB888 color value in ``0xRRGGBB`` format.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_rgb_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_rgb_buffer(0, 0xFF0000)
        """
        if not 0 <= index <= 15:
            raise ValueError("index must be in range 0-15")
        return self._send_status(
            self.CMD_SET_RGB_BUFFER, bytes([index]) + bytes(self._color_to_rgb(color))
        )

    def get_rgb_buffer(self, index: int) -> int:
        """Get one WS2812 color buffer entry.

        :param int index: WS2812 color buffer index, range 0 to 15.
        :return: RGB888 color value in ``0xRRGGBB`` format.
        :rtype: int

        UiFlow2 Code Block:

            |get_rgb_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                color = servos8v2_0.get_rgb_buffer(0)
        """
        if not 0 <= index <= 15:
            raise ValueError("index must be in range 0-15")
        response = self._send_status_payload(self.CMD_GET_RGB_BUFFER, bytes([index]))
        if response and len(response) >= 3:
            return self._rgb_to_color(response[:3])
        return None

    def set_pwm_duty(self, channel: int, duty: int) -> bool:
        """Set the PWM duty of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param int duty: PWM duty, range 0 to 100.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_pwm_duty.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_pwm_duty(0, 50)
        """
        channel = self._check_channel(channel)
        duty = self._limit(duty, 0, 100)
        return self._send_status(self.CMD_SET_PWM_DUTY, bytes([channel, duty]))

    def get_pwm_duty(self, channel: int) -> int:
        """Get the PWM duty of a specific channel.

        :param int channel: The channel number (0 to 7).
        :return: PWM duty, range 0 to 100.
        :rtype: int

        UiFlow2 Code Block:

            |get_pwm_duty.png|

        MicroPython Code Block:

            .. code-block:: python

                duty = servos8v2_0.get_pwm_duty(0)
        """
        channel = self._check_channel(channel)
        response = self._send_status_payload(self.CMD_GET_PWM_DUTY, bytes([channel]))
        if response and len(response) >= 1:
            return response[0]
        return None

    def _set_timer_freq(self, timer: int, freq: int) -> bool:
        freq = self._limit(freq, 1, 65535)
        return self._send_status(self.CMD_SET_TIMER_FREQ, bytes([timer]) + struct.pack("<H", freq))

    def set_pwm_freq(self, channel: int, freq: int) -> bool:
        """Set the PWM frequency of a specific channel.

        Channels 0-3 share one frequency, and channels 4-7 share another frequency.
        Setting the frequency of any channel changes the frequency of every channel
        in the same group.

        :param int channel: The channel number (0 to 7).
        :param int freq: PWM frequency in Hz, range 1 to 65535.

        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_pwm_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_pwm_freq(0, 1000)
        """
        return self._set_timer_freq(self._timer_for_channel(channel), freq)

    def get_pwm_freq(self, channel: int) -> int:
        """Get the PWM frequency of a specific channel.

        Channels 0-3 share one frequency, and channels 4-7 share another frequency.
        The returned value is the shared frequency of the channel's group.

        :param int channel: The channel number (0 to 7).
        :return: PWM frequency in Hz.
        :rtype: int

        UiFlow2 Code Block:

            |get_pwm_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                freq = servos8v2_0.get_pwm_freq(0)
        """
        timer = self._timer_for_channel(channel)
        response = self._send_status_payload(self.CMD_GET_TIMER_FREQ, bytes([timer]))
        if response and len(response) >= 2:
            return struct.unpack("<H", response[:2])[0]
        return None

    def _get_u16(self, cmd: int) -> int:
        response = self._send_payload(cmd)
        if response and len(response) >= 2:
            return struct.unpack("<H", response[:2])[0]
        return None

    def get_reference_voltage(self) -> int:
        """Get the reference voltage.

        :return: Reference voltage in mV.
        :rtype: int

        UiFlow2 Code Block:

            |get_reference_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = servos8v2_0.get_reference_voltage()
        """
        return self._get_u16(self.CMD_GET_REFERENCE_VOLTAGE)

    def get_grove_voltage(self) -> int:
        """Get the Grove port voltage.

        :return: Grove port voltage in mV.
        :rtype: int

        UiFlow2 Code Block:

            |get_grove_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = servos8v2_0.get_grove_voltage()
        """
        return self._get_u16(self.CMD_GET_GROVE_VOLTAGE)

    def get_dc_voltage(self) -> int:
        """Get the DC input voltage.

        :return: DC input voltage in mV.
        :rtype: int

        UiFlow2 Code Block:

            |get_dc_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = servos8v2_0.get_dc_voltage()
        """
        return self._get_u16(self.CMD_GET_DC_VOLTAGE)

    def get_current(self) -> int:
        """Get the system current.

        :return: System current in mA.
        :rtype: int

        UiFlow2 Code Block:

            |get_current.png|

        MicroPython Code Block:

            .. code-block:: python

                current = servos8v2_0.get_current()
        """
        return self._get_u16(self.CMD_GET_CURRENT)

    def get_uid(self, uid_type: int = 0) -> tuple:
        """Get the device UID.

        :param int uid_type: UID type. Use 0 for 4-byte UID or 1 for 12-byte UID. Default is 0.
        :return: Tuple of UID bytes. Returns an empty tuple if failed.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_uid.png|

        MicroPython Code Block:

            .. code-block:: python

                uid = servos8v2_0.get_uid(0)
        """
        if uid_type not in (0, 1):
            raise ValueError("uid_type must be 0 or 1")
        response = self._send_status_payload(self.CMD_GET_UID, bytes([uid_type]))
        expected_len = 4 if uid_type == 0 else 12
        if response and len(response) >= expected_len:
            return tuple(response[:expected_len])
        return tuple()

    def get_bootloader_version(self) -> int:
        """Get the bootloader version.

        :return: Bootloader version, or None if failed.
        :rtype: int

        UiFlow2 Code Block:

            |get_bootloader_version.png|

        MicroPython Code Block:

            .. code-block:: python

                version = servos8v2_0.get_bootloader_version()
        """
        response = self._send_payload(self.CMD_GET_BOOTLOADER_VERSION)
        if response and len(response) >= 1:
            return response[0]
        return None

    def get_firmware_version(self) -> int:
        """Get the firmware version.

        :return: Firmware version.
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                version = servos8v2_0.get_firmware_version()
        """
        response = self._send_payload(self.CMD_GET_FIRMWARE_VERSION)
        if response and len(response) >= 1:
            return response[0]
        return None

    def get_device_type(self) -> int:
        """Get the Chain device type.

        :return: Device type. Unit 8Servos2 Chain is 0x000C.
        :rtype: int

        UiFlow2 Code Block:

            |get_device_type.png|

        MicroPython Code Block:

            .. code-block:: python

                device_type = servos8v2_0.get_device_type()
        """
        response = self._send_payload(self.CMD_GET_DEVICE_TYPE)
        if response and len(response) >= 2:
            return struct.unpack("<H", response[:2])[0]
        return None

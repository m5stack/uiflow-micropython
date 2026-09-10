# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import struct
import sys
from .pahub import PAHUBUnit
from .unit_helper import UnitError

if sys.platform != "esp32":
    from typing import Union


SERVOS_8_V2_ADDR = 0x25  # Default I2C address.

REG_MODE = 0x00         # Channel mode registers, IO0-IO7.
REG_PULL = 0x10         # Input pull-up/down configuration registers.
REG_INPUT = 0x20        # Input level registers.
REG_OUTPUT = 0x30       # Output level registers.
REG_ADC = 0x40          # 12-bit ADC value registers, two bytes per channel.
REG_SERVO_ANGLE = 0x50  # Servo angle registers, 0-180 degrees.
REG_RGB_CONFIG = 0x60   # WS2812 LED count and refresh bit registers.
REG_PWM_DUTY = 0x70     # PWM duty registers, 0-100%.
REG_RGB_BUFFER = 0x80   # WS2812 color buffer, B/G/R bytes at a 4-byte stride.
REG_TIMER_FREQ = 0xD0   # TIM2/TIM3 frequency registers.
REG_UID = 0xE0          # 12-byte device UID registers.
REG_SYS = 0xF0          # Voltage/current telemetry block.
REG_FW_VER = 0xFE       # Firmware version register.
REG_I2C_ADDR = 0xFF     # Current I2C address register.


class Servos8V2Unit:
    """Create a Unit 8Servos2 object.

    :param machine.I2C | PAHUBUnit i2c: The I2C bus the Unit 8Servos2 is connected to.
    :param int | list | tuple address: The I2C address of the device, range 0x25 to 0x34.
        Default is 0x25.

    :raises UnitError: If the Unit 8Servos2 is not connected.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C, Pin
            from unit import Servos8V2Unit

            i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
            servos8v2_0 = Servos8V2Unit(i2c0, 0x25)
    """

    MODE_INPUT = 0x00   # GPIO input mode.
    MODE_OUTPUT = 0x01  # GPIO output mode.
    MODE_ADC = 0x02     # ADC input mode.
    MODE_SERVO = 0x03   # Servo angle output mode.
    MODE_RGB = 0x04     # RGB WS2812 data output mode.
    MODE_PWM = 0x05     # PWM duty output mode.

    PULL_NONE = 0  # Disable input pull resistor.
    PULL_UP = 1    # Enable input pull-up.
    PULL_DOWN = 2  # Enable input pull-down.

    def __init__(
        self, i2c: Union[machine.I2C, PAHUBUnit], address: int | list | tuple = SERVOS_8_V2_ADDR
    ):
        self._i2c = i2c
        self._address = address
        self._available()

    def _available(self) -> None:
        if self._address not in self._i2c.scan():
            raise UnitError("8Servos2 unit maybe not connect")

    def _check_channel(self, channel: int) -> int:
        if not 0 <= channel <= 7:
            raise ValueError("channel must be in range 0-7")
        return channel

    def _timer_for_channel(self, channel: int) -> int:
        channel = self._check_channel(channel)
        return 0 if channel < 4 else 1

    def _limit(self, value: int, minimum: int, maximum: int) -> int:
        value = int(value)
        if value < minimum:
            return minimum
        if value > maximum:
            return maximum
        return value

    def _read(self, reg: int, length: int) -> bytearray:
        return self._i2c.readfrom_mem(self._address, reg, length)

    def _write(self, reg: int, data) -> None:
        self._i2c.writeto_mem(self._address, reg, bytearray(data))

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
        return self._read(REG_MODE + channel, 1)[0]

    def set_channel_mode(self, channel: int, mode: int) -> None:
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

        UiFlow2 Code Block:

            |set_channel_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_channel_mode(0, Servos8V2Unit.MODE_SERVO)
        """
        channel = self._check_channel(channel)
        mode = self._limit(mode, self.MODE_INPUT, self.MODE_PWM)
        self._write(REG_MODE + channel, [mode])
        if mode == self.MODE_SERVO:
            self._set_timer_freq(self._timer_for_channel(channel), 50)

    def set_input_pull(self, channel: int, pull: int) -> None:
        """Set the input pull configuration of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param int pull: Pull configuration. Use PULL_NONE, PULL_UP, or PULL_DOWN.

        UiFlow2 Code Block:

            |set_input_pull.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_input_pull(0, Servos8V2Unit.PULL_UP)
        """
        channel = self._check_channel(channel)
        pull = self._limit(pull, self.PULL_NONE, self.PULL_DOWN)
        self._write(REG_PULL + channel, [pull])

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
        return self._read(REG_PULL + channel, 1)[0]

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
        return self._read(REG_INPUT + channel, 1)[0] == 1

    def set_gpio_output_value(self, channel: int, value: bool) -> None:
        """Set the GPIO output value of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param bool value: Output value, False for low level or True for high level.

        UiFlow2 Code Block:

            |set_gpio_output_value.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_gpio_output_value(0, True)
        """
        channel = self._check_channel(channel)
        self._write(REG_OUTPUT + channel, [1 if value else 0])

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
        return self._read(REG_OUTPUT + channel, 1)[0] == 1

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
        return struct.unpack("<H", self._read(REG_ADC + channel * 2, 2))[0]

    def set_servo_angle(self, channel: int, angle: int) -> None:
        """Set the servo angle of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param int angle: Servo angle, range 0 to 180.

        UiFlow2 Code Block:

            |set_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_servo_angle(0, 90)
        """
        channel = self._check_channel(channel)
        self._write(REG_SERVO_ANGLE + channel, [self._limit(angle, 0, 180)])

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
        return self._read(REG_SERVO_ANGLE + channel, 1)[0]

    def _pack_rgb_config(self, count: int, refresh: bool = False) -> int:
        count = self._limit(count, 0, 16)
        return (0x20 if refresh else 0x00) | (count & 0x1F)

    def set_rgb_config(self, channel: int, count: int, refresh: bool = False) -> None:
        """Set the WS2812 LED count and refresh flag of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param int count: WS2812 LED count, range 0 to 16.
        :param bool refresh: Whether to trigger an RGB refresh. Default is False.

        UiFlow2 Code Block:

            |set_rgb_config.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_rgb_config(0, 4, refresh=True)
        """
        channel = self._check_channel(channel)
        self._write(REG_RGB_CONFIG + channel, [self._pack_rgb_config(count, refresh)])

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
        return self._read(REG_RGB_CONFIG + channel, 1)[0]

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
        return self.get_rgb_config(channel) & 0x1F

    def refresh_rgb(self, channel: int) -> None:
        """Trigger WS2812 refresh for a specific channel.

        :param int channel: The channel number (0 to 7).

        UiFlow2 Code Block:

            |refresh_rgb.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.refresh_rgb(0)
        """
        count = self.get_rgb_count(channel)
        self.set_rgb_config(channel, count, refresh=True)

    def _color_to_bgr(self, color: int) -> tuple:
        color = self._limit(color, 0, 0xFFFFFF)
        return (color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF)

    def _bgr_to_color(self, data) -> int:
        b, g, r = data[0], data[1], data[2]
        return (r << 16) | (g << 8) | b

    def _rgb_buffer_reg(self, index: int) -> int:
        if not 0 <= index <= 15:
            raise ValueError("index must be in range 0-15")
        return REG_RGB_BUFFER + index * 4

    def set_rgb_buffer(self, index: int, color: int) -> None:
        """Set one WS2812 color buffer entry.

        :param int index: WS2812 color buffer index, range 0 to 15.
        :param int color: RGB888 color value in ``0xRRGGBB`` format.

        UiFlow2 Code Block:

            |set_rgb_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_rgb_buffer(0, 0xFF0000)
        """
        self._write(self._rgb_buffer_reg(index), self._color_to_bgr(color))

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
        return self._bgr_to_color(self._read(self._rgb_buffer_reg(index), 3))

    def set_pwm_duty(self, channel: int, duty: int) -> None:
        """Set the PWM duty of a specific channel.

        :param int channel: The channel number (0 to 7).
        :param int duty: PWM duty, range 0 to 100.

        UiFlow2 Code Block:

            |set_pwm_duty.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_pwm_duty(0, 50)
        """
        channel = self._check_channel(channel)
        self._write(REG_PWM_DUTY + channel, [self._limit(duty, 0, 100)])

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
        return self._read(REG_PWM_DUTY + channel, 1)[0]

    def _set_timer_freq(self, timer: int, freq: int) -> None:
        freq = self._limit(freq, 1, 65535)
        self._write(REG_TIMER_FREQ + timer * 2, struct.pack("<H", freq))

    def set_pwm_freq(self, channel: int, freq: int) -> None:
        """Set the PWM frequency of a specific channel.

        Channels 0-3 share one frequency, and channels 4-7 share another frequency.
        Setting the frequency of any channel changes the frequency of every channel
        in the same group.

        :param int channel: The channel number (0 to 7).
        :param int freq: PWM frequency in Hz, range 1 to 65535.

        UiFlow2 Code Block:

            |set_pwm_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                servos8v2_0.set_pwm_freq(0, 1000)
        """
        self._set_timer_freq(self._timer_for_channel(channel), freq)

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
        return struct.unpack("<H", self._read(REG_TIMER_FREQ + timer * 2, 2))[0]

    def _get_sys_values(self) -> tuple:
        return struct.unpack("<HHHH", self._read(REG_SYS, 8))

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
        return self._get_sys_values()[0]

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
        return self._get_sys_values()[1]

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
        return self._get_sys_values()[2]

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
        return self._get_sys_values()[3]

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
        return self._read(REG_FW_VER, 1)[0]

    def get_i2c_address(self) -> int:
        """Get the current I2C address.

        :return: Current I2C address.
        :rtype: int

        UiFlow2 Code Block:

            |get_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                address = servos8v2_0.get_i2c_address()
        """
        return self._read(REG_I2C_ADDR, 1)[0]

    def get_uid(self) -> tuple:
        """Get the 12-byte device UID.

        :return: Tuple containing the 12 UID bytes.
        :rtype: tuple

        UiFlow2 Code Block:

            |get_uid.png|

        MicroPython Code Block:

            .. code-block:: python

                uid = servos8v2_0.get_uid()
        """
        return tuple(self._read(REG_UID, 12))

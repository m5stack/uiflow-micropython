# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""M5IOE1 I2C IO-expander driver.

The public GPIO API uses the product labels G1 through G14. Register bit 0
therefore represents G1. Alternate functions are fixed by the M5IOE1 firmware:
ADC inputs are G2/G4/G5/G7, PWM channels 0..3 are G9/G8/G11/G10, and the
NeoPixel output is G14.
"""

try:
    from micropython import const
except ImportError:

    def const(value):
        return value


try:
    import time
except ImportError:
    time = None

try:
    from machine import Pin as _MachinePin
except (ImportError, AttributeError):
    _MachinePin = None

try:
    from machine import PinBase as _PinBase
except (ImportError, AttributeError):
    _PinBase = object


DEFAULT_ADDR = const(0x6F)
I2C_ADDR = DEFAULT_ADDR
GPIO_COUNT = const(14)
PWM_CHANNEL_COUNT = const(4)
ADC_MAX = const(0x0FFF)

REG_UID_L = const(0x00)
REG_REV = const(0x02)
REG_GPIO_MODE_L = const(0x03)
REG_GPIO_MODE_H = const(0x04)
REG_GPIO_OUT_L = const(0x05)
REG_GPIO_OUT_H = const(0x06)
REG_GPIO_IN_L = const(0x07)
REG_GPIO_IN_H = const(0x08)
REG_GPIO_PU_L = const(0x09)
REG_GPIO_PU_H = const(0x0A)
REG_GPIO_PD_L = const(0x0B)
REG_GPIO_PD_H = const(0x0C)
REG_GPIO_IE_L = const(0x0D)
REG_GPIO_IE_H = const(0x0E)
REG_GPIO_IP_L = const(0x0F)
REG_GPIO_IP_H = const(0x10)
REG_GPIO_IS_L = const(0x11)
REG_GPIO_IS_H = const(0x12)
REG_GPIO_DRV_L = const(0x13)
REG_GPIO_DRV_H = const(0x14)
REG_ADC_CTRL = const(0x15)
REG_ADC_DATA_L = const(0x16)
REG_TEMP_CTRL = const(0x18)
REG_TEMP_DATA_L = const(0x19)
REG_PWM1_DUTY_L = const(0x1B)
REG_PWM1_DUTY_H = const(0x1C)
REG_PWM2_DUTY_L = const(0x1D)
REG_PWM2_DUTY_H = const(0x1E)
REG_PWM3_DUTY_L = const(0x1F)
REG_PWM3_DUTY_H = const(0x20)
REG_PWM4_DUTY_L = const(0x21)
REG_PWM4_DUTY_H = const(0x22)
REG_I2C_CFG = const(0x23)
REG_LED_CFG = const(0x24)
REG_PWM_FREQ_L = const(0x25)
REG_PWM_FREQ_H = const(0x26)
REG_REF_VOLTAGE_L = const(0x27)
REG_RESET = const(0x29)
REG_LED_RAM_START = const(0x30)
REG_RTC_RAM_START = const(0x70)
REG_AW8737A_PULSE = const(0x90)

GPIO_MODE_IN = const(0)
GPIO_MODE_OUT = const(1)
GPIO_PULL_NONE = const(0)
GPIO_PULL_UP = const(1)
GPIO_PULL_DOWN = const(2)
GPIO_DRIVE_PUSH_PULL = const(0)
GPIO_DRIVE_OPEN_DRAIN = const(1)

IRQ_FALLING = const(0)
IRQ_RISING = const(1)

ADC_BUSY = const(1 << 7)
ADC_START = const(1 << 6)
TEMP_BUSY = const(1 << 7)
TEMP_START = const(1 << 6)
PWM_ENABLE = const(1 << 15)
PWM_INVERT = const(1 << 14)
PWM_DUTY_MASK = const(0x0FFF)
LED_NUM_MASK = const(0x3F)
LED_REFRESH = const(1 << 6)
I2C_INTERNAL_PULL_DISABLE = const(1 << 6)
I2C_WAKE_RISING = const(1 << 5)
I2C_SPEED_400K = const(1 << 4)
RESET_KEY = const(0x3A)
AW_REFRESH = const(1 << 7)

ADC_PINS = (2, 4, 5, 7)
PWM_PINS = (9, 8, 11, 10)
NEOPIXEL_PIN = const(14)

# Compatibility constants used by the previous private helpers.
IN = const(0)
OUT = const(1)
PULL_UP = const(2)
PULL_DOWN = const(3)
LOW = const(0)
HIGH = const(1)

_PIN_PULL_KEEP = const(-1)

if _MachinePin is None:
    _machine_pin_in = 0
    _machine_pin_out = 1
    _machine_pin_open_drain = 2
    _machine_pin_pull_up = 1
    _machine_pin_pull_down = 2
else:
    _machine_pin_in = _MachinePin.IN
    _machine_pin_out = _MachinePin.OUT
    _machine_pin_open_drain = _MachinePin.OPEN_DRAIN
    _machine_pin_pull_up = _MachinePin.PULL_UP
    _machine_pin_pull_down = _MachinePin.PULL_DOWN


def _ticks_ms():
    if time is None:
        return 0
    if hasattr(time, "ticks_ms"):
        return time.ticks_ms()
    if hasattr(time, "monotonic"):
        return int(time.monotonic() * 1000)
    return int(time.time() * 1000)


def _ticks_diff(new, old):
    if time is not None and hasattr(time, "ticks_diff"):
        return time.ticks_diff(new, old)
    return new - old


def _sleep_ms(milliseconds):
    if time is None:
        return
    if hasattr(time, "sleep_ms"):
        time.sleep_ms(milliseconds)
    else:
        time.sleep(milliseconds / 1000)


def _bool(value, name):
    if isinstance(value, bool):
        return value
    if value in (0, 1):
        return bool(value)
    raise ValueError("%s must be bool" % name)


class M5IOE1:
    """M5IOE1 low-level driver.

    :param i2c: MicroPython I2C-compatible object.
    :param int addr: 7-bit I2C address. Default is 0x6F.
    """

    def __init__(self, i2c, addr=DEFAULT_ADDR):
        addr = int(addr)
        if not 0 <= addr <= 0x7F:
            raise ValueError("addr must be 0..127")
        self.i2c = i2c
        self.addr = addr
        if self.addr not in self.i2c.scan():
            raise Exception("M5IOE1 not found at I2C address 0x%02X" % self.addr)
        self._led_count = 0

    def _check_reg(self, reg):
        reg = int(reg)
        if not 0 <= reg <= 0xFF:
            raise ValueError("reg must be 0..255")
        return reg

    def _check_byte(self, value, name="value"):
        value = int(value)
        if not 0 <= value <= 0xFF:
            raise ValueError("%s must be 0..255" % name)
        return value

    def _check_pin(self, pin):
        pin = int(pin)
        if not 1 <= pin <= GPIO_COUNT:
            raise ValueError("pin must be G1..G14")
        return pin

    def _check_pwm_channel(self, channel):
        channel = int(channel)
        if not 0 <= channel < PWM_CHANNEL_COUNT:
            raise ValueError("channel must be 0..3")
        return channel

    def _read_mem(self, reg, length):
        reg = self._check_reg(reg)
        length = int(length)
        if length < 0 or reg + length > 0x100:
            raise ValueError("invalid read range")
        return self.i2c.readfrom_mem(self.addr, reg, length)

    def _write_mem(self, reg, data):
        reg = self._check_reg(reg)
        data = bytes(data)
        if reg + len(data) > 0x100:
            raise ValueError("invalid write range")
        self.i2c.writeto_mem(self.addr, reg, data)

    def read_reg(self, reg):
        """Read one 8-bit register."""
        return self._read_mem(reg, 1)[0]

    def write_reg(self, reg, value):
        """Write one 8-bit register."""
        self._write_mem(reg, (self._check_byte(value),))

    def read_reg16(self, reg):
        """Read one little-endian 16-bit register pair."""
        data = self._read_mem(reg, 2)
        return data[0] | (data[1] << 8)

    def write_reg16(self, reg, value):
        """Write one little-endian 16-bit register pair atomically."""
        value = int(value)
        if not 0 <= value <= 0xFFFF:
            raise ValueError("value must be 0..65535")
        self._write_mem(reg, (value & 0xFF, value >> 8))

    def update_bits(self, reg, mask, value):
        """Update selected bits in an 8-bit register."""
        mask = self._check_byte(mask, "mask")
        value = self._check_byte(value)
        current = self.read_reg(reg)
        updated = (current & ~mask) | (value & mask)
        if updated != current:
            self.write_reg(reg, updated)
        return updated

    _read_reg8 = read_reg

    def _write_reg8(self, reg, value):
        self.write_reg(reg, value)
        return True

    _read_reg16 = read_reg16

    def _write_reg16(self, reg, value):
        self.write_reg16(reg, value)
        return True

    def _write_bytes(self, reg, data):
        self._write_mem(reg, data)
        return True

    def is_connected(self):
        """Return whether the device responds at the configured address."""
        try:
            self.read_reg(REG_UID_L)
            return True
        except OSError:
            return False

    def get_uid(self):
        """Return the factory 16-bit unique identifier."""
        return self.read_reg16(REG_UID_L)

    def get_firmware_version(self):
        """Return the M5IOE1 firmware revision byte."""
        return self.read_reg(REG_REV)

    def Pin(self, pin, mode=None, pull=_PIN_PULL_KEEP, *, value=None, drive=None):  # noqa: N802
        """Create a Pin-compatible GPIO object."""
        return Pin(self, pin, mode, pull, value=value, drive=drive)

    def ADC(self, pin):  # noqa: N802
        """Create an ADC object for G2, G4, G5, or G7."""
        return ADC(self, pin)

    def PWM(  # noqa: N802
        self, channel, *, freq=None, duty_u16=0, duty_ns=None, invert=False
    ):
        """Create a PWM object for channel 0..3."""
        return PWM(
            self,
            channel,
            freq=freq,
            duty_u16=duty_u16,
            duty_ns=duty_ns,
            invert=invert,
        )

    def NeoPixel(self, pin, count, *, bpp=3, timing=1):  # noqa: N802
        """Create a buffered NeoPixel object on G14."""
        return NeoPixel(self, pin, count, bpp=bpp, timing=timing)

    def _pin_mask(self, pin):
        return 1 << (self._check_pin(pin) - 1)

    def set_pin_mode(self, pin, mode):
        """Set a pin to GPIO input or output mode."""
        mask = self._pin_mask(pin)
        if mode == GPIO_MODE_IN:
            value = 0
        elif mode == GPIO_MODE_OUT:
            value = mask
        else:
            raise ValueError("mode must be GPIO_MODE_IN or GPIO_MODE_OUT")
        current = self.read_reg16(REG_GPIO_MODE_L)
        self.write_reg16(REG_GPIO_MODE_L, (current & ~mask) | value)

    def set_pin_pull(self, pin, pull):
        """Configure no pull, pull-up, or pull-down for a GPIO."""
        mask = self._pin_mask(pin)
        pu = self.read_reg16(REG_GPIO_PU_L) & ~mask
        pd = self.read_reg16(REG_GPIO_PD_L) & ~mask
        if pull == GPIO_PULL_UP:
            pu |= mask
        elif pull == GPIO_PULL_DOWN:
            pd |= mask
        elif pull != GPIO_PULL_NONE:
            raise ValueError("pull must be GPIO_PULL_NONE, GPIO_PULL_UP, or GPIO_PULL_DOWN")
        self.write_reg16(REG_GPIO_PU_L, pu)
        self.write_reg16(REG_GPIO_PD_L, pd)

    def set_pin_drive(self, pin, drive):
        """Set a GPIO to push-pull or open-drain drive."""
        mask = self._pin_mask(pin)
        current = self.read_reg16(REG_GPIO_DRV_L)
        if drive == GPIO_DRIVE_PUSH_PULL:
            current &= ~mask
        elif drive == GPIO_DRIVE_OPEN_DRAIN:
            current |= mask
        else:
            raise ValueError("drive must be push-pull or open-drain")
        self.write_reg16(REG_GPIO_DRV_L, current)

    def set_pin_value(self, pin, value):
        """Set a GPIO output latch to 0 or 1."""
        mask = self._pin_mask(pin)
        current = self.read_reg16(REG_GPIO_OUT_L)
        current = current | mask if _bool(value, "value") else current & ~mask
        self.write_reg16(REG_GPIO_OUT_L, current)

    def read_pin(self, pin):
        """Read a GPIO input and return 0 or 1."""
        mask = self._pin_mask(pin)
        return 1 if self.read_reg16(REG_GPIO_IN_L) & mask else 0

    def enable_pin_irq(self, pin, trigger=IRQ_FALLING):
        """Enable the M5IOE1 interrupt for a GPIO."""
        mask = self._pin_mask(pin)
        polarity = self.read_reg16(REG_GPIO_IP_L)
        if trigger == IRQ_RISING:
            polarity |= mask
        elif trigger == IRQ_FALLING:
            polarity &= ~mask
        else:
            raise ValueError("trigger must be IRQ_FALLING or IRQ_RISING")
        self.write_reg16(REG_GPIO_IP_L, polarity)
        self.write_reg16(REG_GPIO_IE_L, self.read_reg16(REG_GPIO_IE_L) | mask)

    def disable_pin_irq(self, pin):
        """Disable the M5IOE1 interrupt for a GPIO."""
        mask = self._pin_mask(pin)
        self.write_reg16(REG_GPIO_IE_L, self.read_reg16(REG_GPIO_IE_L) & ~mask)

    def get_irq_status(self, *, clear=False):
        """Return the 14-bit GPIO interrupt status bitmap."""
        status = self.read_reg16(REG_GPIO_IS_L) & 0x3FFF
        if clear and status:
            self.clear_irq_status(status)
        return status

    def clear_irq_status(self, mask=0x3FFF):
        """Clear selected write-zero-to-clear GPIO interrupt flags."""
        mask = int(mask)
        if not 0 <= mask <= 0x3FFF:
            raise ValueError("mask must be 0..0x3fff")
        self.write_reg16(REG_GPIO_IS_L, (~mask) & 0x3FFF)

    def _pin_mode(self, pin, mode, pull=None):
        try:
            self._check_pin(pin)
            if pull == PULL_UP:
                gpio_pull = GPIO_PULL_UP
            elif pull == PULL_DOWN:
                gpio_pull = GPIO_PULL_DOWN
            else:
                gpio_pull = GPIO_PULL_NONE
            self.set_pin_pull(pin, gpio_pull)
            self.set_pin_drive(pin, GPIO_DRIVE_PUSH_PULL)
            if mode not in (IN, OUT):
                return False
            self.set_pin_mode(pin, GPIO_MODE_OUT if mode == OUT else GPIO_MODE_IN)
            return True
        except ValueError:
            return False

    def _pin_write(self, pin, value):
        try:
            self.set_pin_value(pin, value)
            return True
        except ValueError:
            return False

    def _pin_read(self, pin):
        try:
            return self.read_pin(pin)
        except ValueError:
            return None

    def _wait_clear(self, reg, mask, timeout_ms):
        timeout_ms = int(timeout_ms)
        if timeout_ms < 1:
            raise ValueError("timeout_ms must be >= 1")
        started = _ticks_ms()
        while self.read_reg(reg) & mask:
            if _ticks_diff(_ticks_ms(), started) >= timeout_ms:
                raise TimeoutError("M5IOE1 conversion timed out")
            _sleep_ms(1)

    def read_adc_raw(self, pin, timeout_ms=100):
        """Read the native 12-bit ADC value from G2, G4, G5, or G7."""
        pin = self._check_pin(pin)
        if pin not in ADC_PINS:
            raise ValueError("ADC pin must be G2, G4, G5, or G7")
        channel = ADC_PINS.index(pin) + 1
        self.write_reg(REG_ADC_CTRL, channel | ADC_START)
        self._wait_clear(REG_ADC_CTRL, ADC_BUSY, timeout_ms)
        return self.read_reg16(REG_ADC_DATA_L) & ADC_MAX

    def read_reference_voltage_mv(self):
        """Return the internal ADC reference voltage in millivolts."""
        return self.read_reg16(REG_REF_VOLTAGE_L)

    def read_adc_mv(self, pin, timeout_ms=100):
        """Read an ADC input in millivolts using the internal reference."""
        raw = self.read_adc_raw(pin, timeout_ms)
        return (raw * self.read_reference_voltage_mv() + ADC_MAX // 2) // ADC_MAX

    def read_temperature_raw(self, timeout_ms=100):
        """Return the native 12-bit internal temperature sensor value."""
        self.write_reg(REG_TEMP_CTRL, TEMP_START)
        self._wait_clear(REG_TEMP_CTRL, TEMP_BUSY, timeout_ms)
        return self.read_reg16(REG_TEMP_DATA_L) & ADC_MAX

    def _pwm_reg(self, channel):
        return REG_PWM1_DUTY_L + self._check_pwm_channel(channel) * 2

    def set_pwm_frequency(self, frequency):
        """Set the shared PWM frequency in hertz (1..65535)."""
        frequency = int(frequency)
        if not 1 <= frequency <= 0xFFFF:
            raise ValueError("frequency must be 1..65535")
        self.write_reg16(REG_PWM_FREQ_L, frequency)

    def get_pwm_frequency(self):
        """Return the shared PWM frequency in hertz."""
        return self.read_reg16(REG_PWM_FREQ_L)

    def _pwm_reg_value(self, channel):
        raw = self.read_reg16(self._pwm_reg(channel))
        return raw & PWM_DUTY_MASK, bool(raw & PWM_INVERT), bool(raw & PWM_ENABLE)

    def _write_pwm_raw(self, channel, duty, invert=False, enabled=True):
        channel = self._check_pwm_channel(channel)
        duty = int(duty)
        if not 0 <= duty <= PWM_DUTY_MASK:
            raise ValueError("duty must be 0..4095")
        self.set_pin_drive(PWM_PINS[channel], GPIO_DRIVE_PUSH_PULL)
        raw = duty
        if _bool(invert, "invert"):
            raw |= PWM_INVERT
        if _bool(enabled, "enabled"):
            raw |= PWM_ENABLE
        self.write_reg16(self._pwm_reg(channel), raw)

    def set_pwm_duty_u12(self, channel, duty, *, invert=False):
        """Set a PWM channel duty on the native 0..4095 scale."""
        self._write_pwm_raw(channel, duty, invert, True)

    def get_pwm_duty_u12(self, channel):
        """Return a PWM channel duty on the native 0..4095 scale."""
        return self._pwm_reg_value(channel)[0]

    def disable_pwm(self, channel):
        """Disable a PWM channel without changing its stored duty."""
        duty, invert, _ = self._pwm_reg_value(channel)
        self._write_pwm_raw(channel, duty, invert, False)

    def _pwm_write(self, channel, duty):
        try:
            duty = max(0, min(1000, int(duty)))
            self._write_pwm_raw(channel, duty * PWM_DUTY_MASK // 1000, False, duty > 0)
            return True
        except ValueError:
            return False

    def _pwm_frequency(self, frequency):
        self.set_pwm_frequency(max(1, min(0xFFFF, int(frequency))))
        return True

    def _color(self, color):
        if isinstance(color, int):
            if not 0 <= color <= 0xFFFFFF:
                raise ValueError("color must be 0..0xffffff")
            return (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF
        if len(color) != 3:
            raise ValueError("color must contain 3 channels")
        return tuple(self._check_byte(value, "color") for value in color)

    def _rgb565(self, color):
        red, green, blue = self._color(color)
        return ((red >> 3) << 11) | ((green >> 2) << 5) | (blue >> 3)

    def set_neopixel_count(self, count):
        """Configure the G14 NeoPixel output for 0..32 LEDs."""
        count = int(count)
        if not 0 <= count <= 32:
            raise ValueError("count must be 0..32")
        if count:
            self.set_pin_drive(NEOPIXEL_PIN, GPIO_DRIVE_PUSH_PULL)
        self.write_reg(REG_LED_CFG, count & LED_NUM_MASK)
        self._led_count = count

    def set_neopixel_color(self, index, color, *, refresh=True):
        """Write one RGB888 color into the active NeoPixel buffer."""
        index = int(index)
        if not 0 <= index < self._led_count:
            raise IndexError("pixel index out of range")
        self.write_reg16(REG_LED_RAM_START + index * 2, self._rgb565(color))
        if refresh:
            self.refresh_neopixels()

    def write_neopixels(self, colors, *, auto_refresh=True):
        """Write 1..32 RGB888 colors to the NeoPixel RAM in one burst."""
        colors = tuple(colors)
        if not 1 <= len(colors) <= 32:
            raise ValueError("colors must contain 1..32 entries")
        data = bytearray(len(colors) * 2)
        for index, color in enumerate(colors):
            rgb565 = self._rgb565(color)
            data[index * 2] = rgb565 & 0xFF
            data[index * 2 + 1] = rgb565 >> 8
        self.set_pin_drive(NEOPIXEL_PIN, GPIO_DRIVE_PUSH_PULL)
        self._write_mem(REG_LED_RAM_START, data)
        self._led_count = len(colors)
        cfg = self._led_count & LED_NUM_MASK
        if auto_refresh:
            cfg |= LED_REFRESH
        self.write_reg(REG_LED_CFG, cfg)

    def refresh_neopixels(self):
        """Refresh the active NeoPixel output from LED RAM."""
        self.write_reg(REG_LED_CFG, (self._led_count & LED_NUM_MASK) | LED_REFRESH)

    def clear_neopixels(self, *, auto_refresh=True):
        """Clear every configured NeoPixel."""
        if self._led_count == 0:
            return
        self._write_mem(REG_LED_RAM_START, bytes(self._led_count * 2))
        cfg = self._led_count & LED_NUM_MASK
        if auto_refresh:
            cfg |= LED_REFRESH
        self.write_reg(REG_LED_CFG, cfg)

    def disable_neopixels(self):
        """Disable the NeoPixel output and forget the active count."""
        self.write_reg(REG_LED_CFG, 0)
        self._led_count = 0

    def _set_leds(self, colors, count=None, auto_refresh=True):
        try:
            colors = list(colors)
            count = len(colors) if count is None else int(count)
            if not 1 <= count <= 32:
                return False
            colors.extend(((0, 0, 0),) * (count - len(colors)))
            self.write_neopixels(colors[:count], auto_refresh=auto_refresh)
            return True
        except (ValueError, TypeError):
            return False

    def set_i2c_frequency(self, frequency):
        """Set the M5IOE1-side I2C frequency to 100000 or 400000 Hz."""
        frequency = int(frequency)
        if frequency == 100000:
            value = 0
        elif frequency == 400000:
            value = I2C_SPEED_400K
        else:
            raise ValueError("frequency must be 100000 or 400000")
        self.update_bits(REG_I2C_CFG, I2C_SPEED_400K, value)

    def get_i2c_frequency(self):
        """Return the configured M5IOE1-side I2C frequency."""
        return 400000 if self.read_reg(REG_I2C_CFG) & I2C_SPEED_400K else 100000

    def set_i2c_sleep_timeout_s(self, timeout_s):
        """Set the I2C idle sleep timeout to 0..15 seconds."""
        timeout_s = int(timeout_s)
        if not 0 <= timeout_s <= 15:
            raise ValueError("timeout_s must be 0..15")
        self.update_bits(REG_I2C_CFG, 0x0F, timeout_s)

    def set_i2c_internal_pulls(self, enabled):
        """Enable or disable the M5IOE1 internal I2C pull resistors."""
        value = 0 if _bool(enabled, "enabled") else I2C_INTERNAL_PULL_DISABLE
        self.update_bits(REG_I2C_CFG, I2C_INTERNAL_PULL_DISABLE, value)

    def set_i2c_wake_trigger(self, trigger):
        """Set I2C wake to falling or rising edge."""
        if trigger == IRQ_FALLING:
            value = 0
        elif trigger == IRQ_RISING:
            value = I2C_WAKE_RISING
        else:
            raise ValueError("trigger must be IRQ_FALLING or IRQ_RISING")
        self.update_bits(REG_I2C_CFG, I2C_WAKE_RISING, value)

    def read_rtc_ram(self, offset=0, length=32):
        """Read bytes from the 32-byte retention RAM."""
        offset = int(offset)
        length = int(length)
        if offset < 0 or length < 0 or offset + length > 32:
            raise ValueError("offset and length must stay within 32 bytes")
        return self._read_mem(REG_RTC_RAM_START + offset, length)

    def write_rtc_ram(self, offset, data):
        """Write bytes to the 32-byte retention RAM."""
        offset = int(offset)
        data = bytes(data)
        if offset < 0 or offset + len(data) > 32:
            raise ValueError("offset and data must stay within 32 bytes")
        self._write_mem(REG_RTC_RAM_START + offset, data)

    def set_aw8737a_pulse(self, pin, pulses, *, refresh=True):
        """Configure and optionally trigger 0..3 AW8737A control pulses."""
        pin = self._check_pin(pin)
        pulses = int(pulses)
        if not 0 <= pulses <= 3:
            raise ValueError("pulses must be 0..3")
        value = (pulses << 5) | (pin - 1)
        if refresh:
            value |= AW_REFRESH
        self.write_reg(REG_AW8737A_PULSE, value)

    def restore_defaults(self):
        """Restore M5IOE1 firmware defaults using the documented reset key."""
        self.write_reg(REG_RESET, RESET_KEY)
        self._led_count = 0
        _sleep_ms(5)


class Pin(_PinBase):
    """MicroPython Pin-compatible wrapper for M5IOE1 G1..G14."""

    def __init__(self, ioe1, pin, mode=None, pull=_PIN_PULL_KEEP, *, value=None, drive=None):
        self.ioe1 = ioe1
        self.pin = ioe1._check_pin(pin)
        self._active = False
        self.init(mode, pull, value=value, drive=drive)

    def init(self, mode=None, pull=_PIN_PULL_KEEP, *, value=None, drive=None):
        """Initialize or reconfigure this GPIO."""
        if value is not None:
            self.ioe1.set_pin_value(self.pin, value)
        if pull != _PIN_PULL_KEEP:
            if pull is None:
                gpio_pull = GPIO_PULL_NONE
            elif pull == self.PULL_UP:
                gpio_pull = GPIO_PULL_UP
            elif pull == self.PULL_DOWN:
                gpio_pull = GPIO_PULL_DOWN
            else:
                raise ValueError("pull must be None, Pin.PULL_UP, or Pin.PULL_DOWN")
            self.ioe1.set_pin_pull(self.pin, gpio_pull)
        if mode is not None:
            if mode == self.IN:
                gpio_mode = GPIO_MODE_IN
                gpio_drive = GPIO_DRIVE_PUSH_PULL if drive is None else drive
            elif mode == self.OUT:
                gpio_mode = GPIO_MODE_OUT
                gpio_drive = GPIO_DRIVE_PUSH_PULL if drive is None else drive
            elif mode == self.OPEN_DRAIN:
                gpio_mode = GPIO_MODE_OUT
                gpio_drive = GPIO_DRIVE_OPEN_DRAIN
            else:
                raise ValueError("mode must be Pin.IN, Pin.OUT, or Pin.OPEN_DRAIN")
            self.ioe1.set_pin_drive(self.pin, gpio_drive)
            self.ioe1.set_pin_mode(self.pin, gpio_mode)
        elif drive is not None:
            self.ioe1.set_pin_drive(self.pin, drive)
        self._active = True

    def deinit(self):
        """Restore the GPIO as a floating input."""
        if not self._active:
            return
        self.ioe1.set_pin_mode(self.pin, GPIO_MODE_IN)
        self.ioe1.set_pin_pull(self.pin, GPIO_PULL_NONE)
        self._active = False

    def value(self, value=None):
        """Read the input or set the output latch."""
        if not self._active:
            raise RuntimeError("Pin is deinitialized")
        if value is None:
            return self.ioe1.read_pin(self.pin)
        self.ioe1.set_pin_value(self.pin, value)

    def on(self):
        """Set the output high."""
        self.value(1)

    def off(self):
        """Set the output low."""
        self.value(0)

    def __call__(self, value=None):
        return self.value(value)


class ADC:
    """MicroPython ADC-compatible wrapper for fixed M5IOE1 ADC pins."""

    def __init__(self, ioe1, pin):
        self.ioe1 = ioe1
        self.pin = ioe1._check_pin(pin)
        if self.pin not in ADC_PINS:
            raise ValueError("ADC pin must be G2, G4, G5, or G7")
        self._active = True
        self.ioe1.set_pin_mode(self.pin, GPIO_MODE_IN)
        self.ioe1.set_pin_pull(self.pin, GPIO_PULL_NONE)

    def deinit(self):
        """Deactivate this ADC wrapper."""
        self._active = False

    def _require_active(self):
        if not self._active:
            raise RuntimeError("ADC is deinitialized")

    def read(self):
        """Return the native 12-bit ADC value."""
        self._require_active()
        return self.ioe1.read_adc_raw(self.pin)

    def read_u16(self):
        """Return the ADC value normalized to 0..65535."""
        return (self.read() * 0xFFFF + ADC_MAX // 2) // ADC_MAX

    def read_uv(self):
        """Return the ADC input voltage in microvolts."""
        self._require_active()
        return self.ioe1.read_adc_mv(self.pin) * 1000


class PWM:
    """MicroPython PWM-compatible wrapper for channels 0..3."""

    def __init__(
        self,
        ioe1,
        channel,
        freq=1000,
        duty=0,
        *,
        duty_u16=None,
        duty_ns=None,
        invert=False,
    ):
        self.ioe1 = ioe1
        self.channel = ioe1._check_pwm_channel(channel)
        self.pin = PWM_PINS[self.channel]
        self._active = True
        if duty_u16 is not None and duty_ns is not None:
            raise ValueError("duty_u16 and duty_ns are mutually exclusive")
        if freq is not None:
            self.freq(freq)
        if duty_u16 is not None:
            self.duty_u16(duty_u16)
        elif duty_ns is not None:
            self.duty_ns(duty_ns)
        else:
            self._write_legacy_duty(duty, invert)

    def _require_active(self):
        if not self._active:
            raise RuntimeError("PWM is deinitialized")

    def _write_legacy_duty(self, duty, invert=False):
        duty = int(duty)
        if not 0 <= duty <= 1000:
            raise ValueError("duty must be 0..1000")
        raw = (duty * PWM_DUTY_MASK + 500) // 1000
        self.ioe1._write_pwm_raw(self.channel, raw, invert, True)

    def deinit(self):
        """Disable PWM and restore its fixed pin as a floating input."""
        if not self._active:
            return
        self.ioe1.disable_pwm(self.channel)
        self.ioe1.set_pin_mode(self.pin, GPIO_MODE_IN)
        self.ioe1.set_pin_pull(self.pin, GPIO_PULL_NONE)
        self._active = False

    def freq(self, value=None):
        """Read or set the shared frequency in hertz."""
        self._require_active()
        if value is None:
            return self.ioe1.get_pwm_frequency()
        self.ioe1.set_pwm_frequency(value)

    def duty(self, value=None):
        """Read or set the legacy duty scale of 0..1000."""
        self._require_active()
        raw, invert, _ = self.ioe1._pwm_reg_value(self.channel)
        if value is None:
            return (raw * 1000 + PWM_DUTY_MASK // 2) // PWM_DUTY_MASK
        self._write_legacy_duty(value, invert)

    def duty_u16(self, value=None):
        """Read or set duty on the standard 0..65535 scale."""
        self._require_active()
        raw, invert, _ = self.ioe1._pwm_reg_value(self.channel)
        if value is None:
            return (raw * 0xFFFF + PWM_DUTY_MASK // 2) // PWM_DUTY_MASK
        value = int(value)
        if not 0 <= value <= 0xFFFF:
            raise ValueError("duty_u16 must be 0..65535")
        raw = (value * PWM_DUTY_MASK + 0x7FFF) // 0xFFFF
        self.ioe1._write_pwm_raw(self.channel, raw, invert, True)

    def duty_ns(self, value=None):
        """Read or set the pulse width in nanoseconds."""
        self._require_active()
        frequency = self.freq()
        if frequency <= 0:
            raise RuntimeError("PWM frequency is zero")
        period = 1000000000 // frequency
        raw, invert, _ = self.ioe1._pwm_reg_value(self.channel)
        if value is None:
            return (raw * period + PWM_DUTY_MASK // 2) // PWM_DUTY_MASK
        value = int(value)
        if not 0 <= value <= period:
            raise ValueError("duty_ns must be 0..%d" % period)
        raw = (value * PWM_DUTY_MASK + period // 2) // period
        self.ioe1._write_pwm_raw(self.channel, raw, invert, True)

    def invert(self, value=None):
        """Read or set output polarity inversion."""
        self._require_active()
        raw, invert, enabled = self.ioe1._pwm_reg_value(self.channel)
        if value is None:
            return invert
        self.ioe1._write_pwm_raw(self.channel, raw, _bool(value, "invert"), enabled)


class NeoPixel:
    """Buffered RGB NeoPixel output fixed to M5IOE1 G14."""

    def __init__(self, ioe1, pin, count, *, bpp=3, timing=1):
        self.ioe1 = ioe1
        self.pin = ioe1._check_pin(pin)
        if self.pin != NEOPIXEL_PIN:
            raise ValueError("NeoPixel output is fixed to G14")
        self.n = int(count)
        if not 1 <= self.n <= 32:
            raise ValueError("count must be 1..32")
        self.bpp = int(bpp)
        if self.bpp != 3:
            raise ValueError("bpp must be 3")
        self.timing = int(timing)
        if self.timing not in (0, 1):
            raise ValueError("timing must be 0 or 1")
        self.buf = bytearray(self.n * self.bpp)
        self._active = True
        self.ioe1.set_neopixel_count(self.n)

    def _require_active(self):
        if not self._active:
            raise RuntimeError("NeoPixel is deinitialized")

    def _index(self, index):
        index = int(index)
        if index < 0:
            index += self.n
        if not 0 <= index < self.n:
            raise IndexError("pixel index out of range")
        return index

    def __len__(self):
        return self.n

    def __getitem__(self, index):
        index = self._index(index)
        offset = index * self.bpp
        return tuple(self.buf[offset : offset + self.bpp])

    def __setitem__(self, index, color):
        index = self._index(index)
        offset = index * self.bpp
        self.buf[offset : offset + self.bpp] = bytes(self.ioe1._color(color))

    def fill(self, color):
        """Fill the local buffer without updating the LEDs."""
        color = bytes(self.ioe1._color(color))
        for offset in range(0, len(self.buf), self.bpp):
            self.buf[offset : offset + self.bpp] = color

    def write(self):
        """Write the local buffer and refresh the LEDs."""
        self._require_active()
        colors = [
            tuple(self.buf[offset : offset + self.bpp])
            for offset in range(0, len(self.buf), self.bpp)
        ]
        self.ioe1.write_neopixels(colors)

    def deinit(self):
        """Clear LEDs, disable G14 NeoPixel output, and deactivate the object."""
        if not self._active:
            return
        self.ioe1.clear_neopixels()
        self.ioe1.disable_neopixels()
        self.ioe1.set_pin_mode(NEOPIXEL_PIN, GPIO_MODE_IN)
        self.ioe1.set_pin_pull(NEOPIXEL_PIN, GPIO_PULL_NONE)
        self._active = False


class RGB(NeoPixel):
    """Compatibility RGB helper using RGB888 integers and immediate refresh."""

    def __init__(self, ioe1, io=NEOPIXEL_PIN, n=12):
        super().__init__(ioe1, io, n)
        self.io = self.pin
        self._colors = [(0, 0, 0)] * self.n

    def set_color(self, index, color, refresh=True):
        """Set one pixel using an RGB888 integer."""
        try:
            index = self._index(index)
        except IndexError:
            return False
        rgb = self.ioe1._color(color)
        self._colors[index] = rgb
        self[index] = rgb
        if refresh:
            self.refresh()
        return True

    def fill_color(self, color, refresh=True):
        """Fill all pixels using an RGB888 integer."""
        rgb = self.ioe1._color(color)
        self._colors = [rgb] * self.n
        self.fill(rgb)
        if refresh:
            self.write()
        return True

    def refresh(self):
        """Write the cached colors and refresh the output."""
        self.write()
        return True

    def clear(self, refresh=True):
        """Set all pixels to black."""
        return self.fill_color(0, refresh)


M5IOE1.GPIO_MODE_IN = GPIO_MODE_IN
M5IOE1.GPIO_MODE_OUT = GPIO_MODE_OUT
M5IOE1.GPIO_PULL_NONE = GPIO_PULL_NONE
M5IOE1.GPIO_PULL_UP = GPIO_PULL_UP
M5IOE1.GPIO_PULL_DOWN = GPIO_PULL_DOWN
M5IOE1.GPIO_DRIVE_PUSH_PULL = GPIO_DRIVE_PUSH_PULL
M5IOE1.GPIO_DRIVE_OPEN_DRAIN = GPIO_DRIVE_OPEN_DRAIN
M5IOE1.IRQ_FALLING = IRQ_FALLING
M5IOE1.IRQ_RISING = IRQ_RISING

Pin.IN = _machine_pin_in
Pin.OUT = _machine_pin_out
Pin.OPEN_DRAIN = _machine_pin_open_drain
Pin.PULL_UP = _machine_pin_pull_up
Pin.PULL_DOWN = _machine_pin_pull_down
Pin.LOW = LOW
Pin.HIGH = HIGH
Pin.IRQ_FALLING = IRQ_FALLING
Pin.IRQ_RISING = IRQ_RISING

M5ioe1 = M5IOE1

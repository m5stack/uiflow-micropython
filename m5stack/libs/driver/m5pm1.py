# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""M5PM1 power-management IC driver.

This module implements the AIFlow MicroPython API documented in
``m5stack/libs/driver/m5pm1.md``.  It keeps register names close to the
M5PM1 datasheet so hardware bring-up logs can be matched with the source.
"""

try:
    from micropython import const
except ImportError:
    # Keep the module importable by CPython for syntax and fake-I2C tests.
    def const(value):
        return value

try:
    from micropython import schedule as _schedule
except (ImportError, AttributeError):
    _schedule = None

try:
    import time
except ImportError:
    # Host-side tests may not provide MicroPython's time module.
    time = None

try:
    from machine import PinBase as _PinBase
except (ImportError, AttributeError):
    _PinBase = object

try:
    from machine import Pin as _MachinePin
except (ImportError, AttributeError):
    _MachinePin = None


DEFAULT_ADDR = const(0x6E)
DEFAULT_I2C_FREQ = const(100000)
GPIO_COUNT = const(5)

REG_DEVICE_ID = const(0x00)        # R: device ID.
REG_DEVICE_MODEL = const(0x01)     # R: device model.
REG_HW_REV = const(0x02)           # R: hardware revision.
REG_SW_REV = const(0x03)           # R: firmware revision.
REG_PWR_SRC = const(0x04)          # R: active power-source bit mask [2:0].
REG_WAKE_SRC = const(0x05)         # R/W0C: wake-source flags [6:0].
REG_PWR_CFG = const(0x06)          # R/W: charge and power-rail enables.
REG_HOLD_CFG = const(0x07)         # R/W: GPIO/LDO/BOOST power-hold bits.
REG_BATT_LVP = const(0x08)         # R/W: battery low-voltage threshold.
REG_I2C_CFG = const(0x09)          # R/W: I2C sleep timeout and speed.
REG_WDT_CNT = const(0x0A)          # R/W: watchdog counter/config.
REG_WDT_KEY = const(0x0B)          # W: watchdog feed key register.
REG_SYS_CMD = const(0x0C)          # W: shutdown/reboot/download command.

REG_GPIO_MODE = const(0x10)        # R/W: GPIO direction bits, 1=output.
REG_GPIO_OUT = const(0x11)         # R/W: GPIO output latch.
REG_GPIO_IN = const(0x12)          # R: GPIO input state.
REG_GPIO_DRV = const(0x13)         # R/W: GPIO drive, 1=open-drain.
REG_GPIO_PUPD0 = const(0x14)       # R/W: GPIO0..3 pull config, 2 bits each.
REG_GPIO_PUPD1 = const(0x15)       # R/W: GPIO4 pull config.
REG_GPIO_FUNC0 = const(0x16)       # R/W: GPIO0..3 function, 2 bits each.
REG_GPIO_FUNC1 = const(0x17)       # R/W: GPIO4 function.
REG_GPIO_WAKE_EN = const(0x18)     # R/W: GPIO wake enable bits.
REG_GPIO_WAKE_CFG = const(0x19)    # R/W: GPIO wake edge config bits.

REG_VREF_L = const(0x20)           # R: VREF voltage, u16 mV.
REG_VBAT_L = const(0x22)           # R: battery voltage, u16 mV.
REG_VIN_L = const(0x24)            # R: VIN/USB input voltage, u16 mV.
REG_5VINOUT_L = const(0x26)        # R: 5VINOUT voltage, u16 mV.
REG_ADC_RES_L = const(0x28)        # R: ADC result, 12-bit value in u16.
REG_ADC_CTRL = const(0x2A)         # R/W: ADC control, bit0 busy/start.

REG_PWM0_L = const(0x30)           # R/W: PWM0 duty/control, u16.
REG_PWM1_L = const(0x32)           # R/W: PWM1 duty/control, u16.
REG_PWM_FREQ_L = const(0x34)       # R/W: shared PWM frequency, u16 Hz.
REG_TIM_CNT_0 = const(0x38)        # R/W: timer counter, 32-bit seconds.
REG_TIM_CFG = const(0x3C)          # R/W: timer action/config.
REG_TIM_KEY = const(0x3D)          # W: timer reload/start key.

REG_IRQ_STATUS1 = const(0x40)      # R/W0C: GPIO IRQ status bits.
REG_IRQ_STATUS2 = const(0x41)      # R/W0C: system IRQ status bits.
REG_IRQ_STATUS3 = const(0x42)      # R/W0C: button IRQ status bits.
REG_IRQ_MASK1 = const(0x43)        # R/W: GPIO IRQ mask bits.
REG_IRQ_MASK2 = const(0x44)        # R/W: system IRQ mask bits.
REG_IRQ_MASK3 = const(0x45)        # R/W: button IRQ mask bits.
REG_BTN_STATUS = const(0x48)       # R: button level and latched flag.
REG_BTN_CFG_1 = const(0x49)        # R/W: click/double/long timing config.
REG_BTN_CFG_2 = const(0x4A)        # R/W: double-click poweroff config.

REG_NEO_CFG = const(0x50)          # R/W: NeoPixel count and refresh bit.
REG_AW8737A_PULSE = const(0x53)    # R/W: AW8737A GPIO/pulse/refresh.
REG_NEO_DATA_START = const(0x60)   # R/W: NeoPixel RGB565 RAM start.
REG_RTC_RAM_START = const(0xA0)    # R/W: RTC retention RAM start.
REG_UID_START = const(0xE0)        # R: 12-byte device UID, single reads safest.

_PWR_CHG_EN = const(1 << 0)        # REG_PWR_CFG: charging enable.
_PWR_DCDC_EN = const(1 << 1)       # REG_PWR_CFG: 3.3V DCDC enable.
_PWR_LDO_EN = const(1 << 2)        # REG_PWR_CFG: 3.3V LDO enable.
_PWR_BOOST_EN = const(1 << 3)      # REG_PWR_CFG: BOOST/5VINOUT enable.
_PWR_LED_CTRL = const(1 << 4)      # REG_PWR_CFG: LED_EN default level.

_HOLD_LDO = const(1 << 5)          # REG_HOLD_CFG: LDO power hold.
_HOLD_BOOST = const(1 << 6)        # REG_HOLD_CFG: BOOST power hold.

_I2C_SLEEP_MASK = const(0x0F)      # REG_I2C_CFG: idle sleep timeout.
_I2C_SPEED_400K = const(1 << 4)    # REG_I2C_CFG: 1=400 kHz, 0=100 kHz.

_SYS_CMD_KEY = const(0xA0)         # REG_SYS_CMD: command key high nibble.
_SYS_CMD_SHUTDOWN = const(0x01)    # REG_SYS_CMD: shutdown command.
_SYS_CMD_REBOOT = const(0x02)      # REG_SYS_CMD: reboot command.
_SYS_CMD_DOWNLOAD = const(0x03)    # REG_SYS_CMD: enter download command.

_WDT_FEED_KEY = const(0xA5)        # REG_WDT_KEY: feed watchdog key.
_TIM_RELOAD_KEY = const(0xA5)      # REG_TIM_KEY: reload timer key.

_NEO_REFRESH = const(1 << 6)       # REG_NEO_CFG: refresh LED output.
_NEO_COUNT_MASK = const(0x3F)      # REG_NEO_CFG: active LED count.

_PWM_EN = const(0x10)              # PWM high byte: output enable bit.
_PWM_POLARITY = const(0x20)        # PWM high byte: inverted polarity bit.
_PWM_DUTY_MASK = const(0x0FFF)     # PWM/ADC low 12-bit value mask.

_AW_REFRESH = const(1 << 7)        # REG_AW8737A_PULSE: trigger pulse.

_FUNC_GPIO = const(0)              # GPIO function select: normal GPIO.
_FUNC_IRQ = const(1)               # GPIO function select: active-low IRQ output.
_FUNC_WAKE = const(2)              # Driver API sentinel; raw mux value 2 is reserved.
_FUNC_OTHER = const(3)             # GPIO function select: alternate function.

_GPIO_MODE_IN = const(0)           # GPIO mode: digital input.
_GPIO_MODE_OUT = const(1)          # GPIO mode: push-pull output.
_GPIO_MODE_OPEN_DRAIN = const(2)   # GPIO mode: open-drain output.

_PULL_NONE = const(0)              # Internal pull state: no pull resistor.
_PULL_UP = const(1)                # Internal pull state: pull-up enabled.
_PULL_DOWN = const(2)              # Internal pull state: pull-down enabled.

_DRIVE_PUSH_PULL = const(0)        # GPIO drive mode: push-pull output.
_DRIVE_OPEN_DRAIN = const(1)       # GPIO drive mode: open-drain output.

_PIN_PULL_KEEP = const(-1)         # Pin init sentinel: keep current pull.

# Pin wrapper values follow the active port's machine.Pin constants. ESP32
# values differ from the compact M5PM1 register enums above.
if _MachinePin is None:
    _machine_pin_in = 1
    _machine_pin_out = 3
    _machine_pin_open_drain = 7
    _machine_pin_pull_up = 2
    _machine_pin_pull_down = 1
else:
    _machine_pin_in = _MachinePin.IN
    _machine_pin_out = _MachinePin.OUT
    _machine_pin_open_drain = _MachinePin.OPEN_DRAIN
    _machine_pin_pull_up = _MachinePin.PULL_UP
    _machine_pin_pull_down = _MachinePin.PULL_DOWN

_ADC_MAX = const(0x0FFF)           # ADC full-scale 12-bit code.
_PWM_DEFAULT_FREQ = const(500)     # Datasheet reset frequency in Hz.
_PWM_U16_MAX = const(0xFFFF)       # MicroPython PWM duty_u16 full scale.
_NEOPIXEL_GPIO = const(0)          # NeoPixel output is fixed to GPIO0.
_PWM_GPIOS = (3, 4)                # PWM0/PWM1 fixed output pins.

_ADC_CHANNELS = (1, 2, 6)          # Valid ADC channels: GPIO1, GPIO2, temperature.

# Each IRQ group uses the same status/mask flow but exposes different valid bits.
_IRQ_KINDS = {
    "gpio": (REG_IRQ_STATUS1, REG_IRQ_MASK1, 0x1F),
    "system": (REG_IRQ_STATUS2, REG_IRQ_MASK2, 0x3F),
    "button": (REG_IRQ_STATUS3, REG_IRQ_MASK3, 0x07),
    0: (REG_IRQ_STATUS1, REG_IRQ_MASK1, 0x1F),
    1: (REG_IRQ_STATUS2, REG_IRQ_MASK2, 0x3F),
    2: (REG_IRQ_STATUS3, REG_IRQ_MASK3, 0x07),
}


class EVENT:
    """M5PM1 event filter flags used by ``add_event_cb()``."""

    GPIO0_CHANGE = const(1 << 0)
    GPIO1_CHANGE = const(1 << 1)
    GPIO2_CHANGE = const(1 << 2)
    GPIO3_CHANGE = const(1 << 3)
    GPIO4_CHANGE = const(1 << 4)

    VIN_INSERT = const(1 << 5)
    VIN_REMOVE = const(1 << 6)
    VINOUT_INSERT = const(1 << 7)
    VINOUT_REMOVE = const(1 << 8)
    BATTERY_INSERT = const(1 << 9)
    BATTERY_REMOVE = const(1 << 10)

    BUTTON_CLICK = const(1 << 11)
    WAKE = const(1 << 12)
    BUTTON_DOUBLE = const(1 << 13)

    ALL = const((1 << 14) - 1)


def _bool(value, name):
    if isinstance(value, bool):
        return value
    if value in (0, 1):
        return bool(value)
    raise ValueError("%s must be bool" % name)


class Event:
    """M5PM1 event delivered to a registered callback.

    Attributes:
        target (M5PM1): Driver instance that produced the event.
        code (int): One ``EVENT`` flag.
        user_data: Value supplied when the callback was registered.
    """

    __slots__ = ("target", "code", "user_data")

    def __init__(self, target, code, user_data):
        self.target = target
        self.code = code
        self.user_data = user_data

    def __repr__(self):
        return "Event(code=0x%04x)" % self.code


class M5PM1:
    """M5PM1 power-management IC driver.

    Args:
        i2c: MicroPython I2C-compatible object. It must provide
            ``readfrom_mem()`` and ``writeto_mem()``; ``writeto()`` is used
            opportunistically by :meth:`wake`.
        addr (int): I2C address. Defaults to ``0x6e``. Range: ``0x00..0x7f``.
        mcu_int_gpio (int): MCU GPIO connected to the M5PM1 interrupt output.
            Defaults to ``-1`` when the interrupt line is not connected.
        pm1_int_gpio (int): M5PM1 GPIO used as the active-low interrupt output.
            Defaults to ``-1`` when the interrupt line is not connected.

    Raises:
        ValueError: If an address or interrupt pin is outside its range.
    """

    PIN_FUNCTION_GPIO = _FUNC_GPIO
    PIN_FUNCTION_IRQ = _FUNC_IRQ
    PIN_FUNCTION_WAKE = _FUNC_WAKE
    PIN_FUNCTION_OTHER = _FUNC_OTHER

    GPIO_MODE_IN = _GPIO_MODE_IN
    GPIO_MODE_OUT = _GPIO_MODE_OUT
    GPIO_MODE_OPEN_DRAIN = _GPIO_MODE_OPEN_DRAIN

    GPIO_PULL_NONE = _PULL_NONE
    GPIO_PULL_UP = _PULL_UP
    GPIO_PULL_DOWN = _PULL_DOWN

    DRIVE_PUSH_PULL = _DRIVE_PUSH_PULL
    DRIVE_OPEN_DRAIN = _DRIVE_OPEN_DRAIN

    POWER_SOURCE_NONE = const(0x00)
    POWER_SOURCE_5VIN = const(0x01)
    POWER_SOURCE_5VINOUT = const(0x02)
    POWER_SOURCE_BATTERY = const(0x04)

    WAKE_SOURCE_TIMER = const(0x01)
    WAKE_SOURCE_VIN = const(0x02)
    WAKE_SOURCE_POWER_BUTTON = const(0x04)
    WAKE_SOURCE_RESET_BUTTON = const(0x08)
    WAKE_SOURCE_COMMAND_RESET = const(0x10)
    WAKE_SOURCE_GPIO = const(0x20)
    WAKE_SOURCE_5V_INOUT = const(0x40)

    BUTTON_TIMING_CLICK = const(0)
    BUTTON_TIMING_DOUBLE = const(1)
    BUTTON_TIMING_LONG = const(2)

    TIMER_ACTION_STOP = const(0)
    TIMER_ACTION_FLAG = const(1)
    TIMER_ACTION_REBOOT = const(2)
    TIMER_ACTION_POWER_ON = const(3)
    TIMER_ACTION_POWER_OFF = const(4)

    IRQ_GROUP_GPIO = const(0)
    IRQ_GROUP_SYSTEM = const(1)
    IRQ_GROUP_BUTTON = const(2)

    WAKE_EDGE_FALLING = const(0)
    WAKE_EDGE_RISING = const(1)

    def __init__(
        self,
        i2c,
        *,
        addr=DEFAULT_ADDR,
        mcu_int_gpio=-1,
        pm1_int_gpio=-1,
    ):
        addr = int(addr)
        if not 0 <= addr <= 0x7f:
            raise ValueError("addr must be 0..127")
        self.i2c = i2c
        self.addr = addr
        self.mcu_int_gpio = int(mcu_int_gpio)
        if self.mcu_int_gpio < -1:
            raise ValueError("mcu_int_gpio must be -1 or >= 0")
        self.pm1_int_gpio = int(pm1_int_gpio)
        if self.pm1_int_gpio < -1 or self.pm1_int_gpio >= GPIO_COUNT:
            raise ValueError("pm1_int_gpio must be -1 or 0..4")
        if (self.mcu_int_gpio < 0) != (self.pm1_int_gpio < 0):
            raise ValueError(
                "mcu_int_gpio and pm1_int_gpio must both be configured or both be -1"
            )
        self._led_count = 0
        self._last_aw8737a = 0
        self._mcu_int_pin = None
        self._event_callbacks = []
        self._next_event_handle = 1
        self._event_irq_initialized = False
        self._saved_pm1_int_gpio = None
        self._saved_event_gpios = {}
        self._saved_irq_masks = None
        self._irq_pending = False
        self._irq_dispatch_cb = self._dispatch_irq
        self.wake()
        if self.mcu_int_gpio >= 0:
            self._init_event_irq()

    def _ensure_mcu_int_pin(self):
        if self.mcu_int_gpio < 0:
            raise RuntimeError("mcu_int_gpio and pm1_int_gpio are not configured")
        if _MachinePin is None:
            raise RuntimeError("machine.Pin is unavailable")
        if self._mcu_int_pin is None:
            try:
                self._mcu_int_pin = _MachinePin(
                    self.mcu_int_gpio,
                    _MachinePin.IN,
                    _MachinePin.PULL_UP,
                )
            except (TypeError, AttributeError):
                self._mcu_int_pin = _MachinePin(self.mcu_int_gpio, _MachinePin.IN)
        return self._mcu_int_pin

    def _queue_irq(self, pin=None):
        if self._irq_pending or not self._event_callbacks:
            return
        self._irq_pending = True
        if _schedule is None:
            # CPython fake-Pin tests have no hard-IRQ context.
            self._dispatch_irq(0)
            return
        try:
            _schedule(self._irq_dispatch_cb, 0)
        except RuntimeError:
            # A full scheduler queue must not leave the driver permanently
            # blocked. The asserted INT line can still be drained manually.
            self._irq_pending = False

    def _dispatch_irq(self, _):
        if not self._event_callbacks:
            self._irq_pending = False
            return
        try:
            gpio, system, button = self._read_irq_snapshot(clear=True)
            if self.pm1_int_gpio >= 0:
                gpio &= ~(1 << self.pm1_int_gpio)
            event_filter = gpio | (system << 5) | (button << 11)
            callbacks = tuple(self._event_callbacks)
            code = 1
            while event_filter:
                if event_filter & 1:
                    for _, callback, callback_filter, user_data in callbacks:
                        if callback_filter & code:
                            callback(Event(self, code, user_data))
                event_filter >>= 1
                code <<= 1
        finally:
            self._irq_pending = False
        if self._event_callbacks and self._mcu_int_pin is not None:
            if self._mcu_int_pin.value() == 0:
                self._queue_irq()

    def _event_filter_to_masks(self, event_filter):
        return (
            event_filter & 0x1f,
            (event_filter >> 5) & 0x3f,
            (event_filter >> 11) & 0x07,
        )

    def _apply_event_filter(self):
        event_filter = 0
        for _, _, callback_filter, _ in self._event_callbacks:
            event_filter |= callback_filter
        if self.pm1_int_gpio >= 0:
            event_filter &= ~(1 << self.pm1_int_gpio)
        gpio, system, button = self._event_filter_to_masks(event_filter)
        self.write_reg(REG_IRQ_MASK1, 0x1f & ~gpio)
        self.write_reg(REG_IRQ_MASK2, 0x3f & ~system)
        self.write_reg(REG_IRQ_MASK3, 0x07 & ~button)

    def _read_pin_function(self, gpio):
        reg = REG_GPIO_FUNC0 if gpio < 4 else REG_GPIO_FUNC1
        shift = gpio * 2 if gpio < 4 else 0
        return (self.read_reg(reg) >> shift) & 0x03

    def _configure_event_gpio(self, gpio):
        if gpio in self._saved_event_gpios:
            return
        bit = 1 << gpio
        self._saved_event_gpios[gpio] = (
            self._read_pin_function(gpio),
            bool(self.read_reg(REG_GPIO_MODE) & bit),
            bool(self.read_reg(REG_GPIO_DRV) & bit),
            bool(self.read_reg(REG_GPIO_WAKE_EN) & bit),
            bool(self.read_reg(REG_GPIO_WAKE_CFG) & bit),
        )
        self.set_pin_function(gpio, self.PIN_FUNCTION_GPIO)
        self.set_pin_mode(gpio, self.GPIO_MODE_IN)

    def _restore_event_gpio(self, gpio):
        saved = self._saved_event_gpios.pop(gpio, None)
        if saved is None:
            return
        function, output, open_drain, wake_enabled, wake_edge = saved
        self.set_pin_function(gpio, function)
        self.set_pin_mode(
            gpio,
            self.GPIO_MODE_OUT if output else self.GPIO_MODE_IN,
        )
        self.set_pin_drive(
            gpio,
            self.DRIVE_OPEN_DRAIN if open_drain else self.DRIVE_PUSH_PULL,
        )
        if wake_enabled:
            bit = 1 << gpio
            self.update_bits(REG_GPIO_WAKE_CFG, bit, bit if wake_edge else 0)
            self.update_bits(REG_GPIO_WAKE_EN, bit, bit)

    def _sync_event_gpios(self):
        gpio_filter = 0
        for _, _, callback_filter, _ in self._event_callbacks:
            gpio_filter |= callback_filter & 0x1f
        if self.pm1_int_gpio >= 0:
            gpio_filter &= ~(1 << self.pm1_int_gpio)
        for gpio in range(GPIO_COUNT):
            if gpio_filter & (1 << gpio):
                self._configure_event_gpio(gpio)
            else:
                self._restore_event_gpio(gpio)

    def _restore_all_event_gpios(self):
        for gpio in tuple(self._saved_event_gpios):
            self._restore_event_gpio(gpio)

    def _init_event_irq(self):
        if self._event_irq_initialized:
            return
        if self.pm1_int_gpio < 0:
            raise RuntimeError("mcu_int_gpio and pm1_int_gpio are not configured")
        pin = self._ensure_mcu_int_pin()
        self._saved_irq_masks = (
            self.read_reg(REG_IRQ_MASK1),
            self.read_reg(REG_IRQ_MASK2),
            self.read_reg(REG_IRQ_MASK3),
        )
        self.disable_irq_events(self.IRQ_GROUP_GPIO, 0x1f)
        self.disable_irq_events(self.IRQ_GROUP_SYSTEM, 0x3f)
        self.disable_irq_events(self.IRQ_GROUP_BUTTON, 0x07)
        self.clear_irq(self.IRQ_GROUP_GPIO)
        self.clear_irq(self.IRQ_GROUP_SYSTEM)
        self.clear_irq(self.IRQ_GROUP_BUTTON)

        if self.pm1_int_gpio < 4:
            func_reg = REG_GPIO_FUNC0
            shift = self.pm1_int_gpio * 2
        else:
            func_reg = REG_GPIO_FUNC1
            shift = 0
        self._saved_pm1_int_gpio = (
            (self.read_reg(func_reg) >> shift) & 0x03,
            (self.read_reg(REG_GPIO_DRV) >> self.pm1_int_gpio) & 0x01,
            bool(self.read_reg(REG_GPIO_WAKE_EN) & (1 << self.pm1_int_gpio)),
            bool(self.read_reg(REG_GPIO_WAKE_CFG) & (1 << self.pm1_int_gpio)),
        )
        self.set_pin_drive(self.pm1_int_gpio, self.DRIVE_OPEN_DRAIN)
        self.set_pin_function(self.pm1_int_gpio, self.PIN_FUNCTION_IRQ)

        pin.irq(trigger=_MachinePin.IRQ_FALLING, handler=self._queue_irq)
        self._event_irq_initialized = True

    def _deinit_event_irq(self):
        self._restore_all_event_gpios()
        if self._mcu_int_pin is not None:
            self._mcu_int_pin.irq(handler=None)
        if self._saved_irq_masks is None:
            self.write_reg(REG_IRQ_MASK1, 0x1f)
            self.write_reg(REG_IRQ_MASK2, 0x3f)
            self.write_reg(REG_IRQ_MASK3, 0x07)
        else:
            self.write_reg(REG_IRQ_MASK1, self._saved_irq_masks[0])
            self.write_reg(REG_IRQ_MASK2, self._saved_irq_masks[1])
            self.write_reg(REG_IRQ_MASK3, self._saved_irq_masks[2])
        if self._event_irq_initialized and self._saved_pm1_int_gpio is not None:
            function, drive, wake_enabled, wake_edge = self._saved_pm1_int_gpio
            self.set_pin_function(self.pm1_int_gpio, function)
            self.set_pin_drive(self.pm1_int_gpio, drive)
            if wake_enabled:
                bit = 1 << self.pm1_int_gpio
                self.update_bits(REG_GPIO_WAKE_CFG, bit, bit if wake_edge else 0)
                self.update_bits(REG_GPIO_WAKE_EN, bit, bit)
        self._saved_pm1_int_gpio = None
        self._saved_irq_masks = None
        self._event_irq_initialized = False
        self._irq_pending = False

    def add_event_cb(self, callback, filter, *, user_data=None):
        """Register a callback for one or more ``EVENT`` flags.

        Args:
            callback (callable): Called as ``callback(event)`` in scheduled
                MicroPython context.
            filter (int): One or more ``EVENT`` flags combined with ``|``.
            user_data: Value exposed as ``event.user_data``.

        Returns:
            int: Registration handle accepted by :meth:`remove_event_cb`.
        """
        if not callable(callback):
            raise TypeError("callback must be callable")
        filter = int(filter)
        if filter == 0 or filter & ~EVENT.ALL:
            raise ValueError("filter must contain EVENT flags")
        self._init_event_irq()
        handle = self._next_event_handle
        self._next_event_handle += 1
        self._event_callbacks.append((handle, callback, filter, user_data))
        self._sync_event_gpios()
        self._apply_event_filter()
        if self._mcu_int_pin.value() == 0:
            self._queue_irq()
        return handle

    def remove_event_cb(self, handle_or_callback):
        """Remove event callbacks selected by handle or callback object.

        Returns:
            int: Number of callback registrations removed.
        """
        if not isinstance(handle_or_callback, int) and not callable(handle_or_callback):
            raise TypeError("handle_or_callback must be int or callable")
        callbacks = []
        removed = 0
        for item in self._event_callbacks:
            handle, callback, _, _ = item
            if handle_or_callback == handle or handle_or_callback is callback:
                removed += 1
            else:
                callbacks.append(item)
        self._event_callbacks = callbacks
        self._apply_event_filter()
        self._sync_event_gpios()
        return removed

    def deinit(self):
        """Release event callbacks and the host IRQ registration.

        This method is idempotent. The caller-owned I2C object is not
        deinitialized, and register polling APIs remain usable. Calling
        :meth:`add_event_cb` again recreates the host Pin registration.
        """
        if self._event_irq_initialized:
            self._deinit_event_irq()
        self._mcu_int_pin = None
        self._event_callbacks = []
        self._irq_pending = False

    def _delay_us(self, us):
        if time is not None and hasattr(time, "sleep_us"):
            time.sleep_us(us)

    def wake(self):
        """Wake M5PM1 and wait for communication to recover.

        Sleeping PM1 firmware may NACK the first transaction, so this method
        intentionally ignores the wake write error and waits briefly.
        """
        if not hasattr(self.i2c, "writeto"):
            return
        try:
            self.i2c.writeto(self.addr, b"")
        except OSError:
            pass
        if time is not None and hasattr(time, "sleep_ms"):
            time.sleep_ms(10)

    def _readfrom_mem(self, reg, n):
        try:
            data = self.i2c.readfrom_mem(self.addr, reg, n)
            self._delay_us(500)
            return data
        except OSError:
            raise OSError("m5pm1 read failed: addr=0x%02x reg=0x%02x" % (self.addr, reg))

    def _writeto_mem(self, reg, data):
        try:
            self.i2c.writeto_mem(self.addr, reg, data)
            self._delay_us(500)
        except OSError:
            raise OSError("m5pm1 write failed: addr=0x%02x reg=0x%02x" % (self.addr, reg))

    def _check_reg(self, reg):
        reg = int(reg)
        if not 0 <= reg <= 0xff:
            raise ValueError("reg must be 0..255")
        return reg

    def _check_byte(self, value, name):
        value = int(value)
        if not 0 <= value <= 0xff:
            raise ValueError("%s must be 0..255" % name)
        return value

    def _check_u16(self, value, name):
        value = int(value)
        if not 0 <= value <= 0xffff:
            raise ValueError("%s must be 0..65535" % name)
        return value

    def _check_gpio(self, gpio):
        gpio = int(gpio)
        if not 0 <= gpio < GPIO_COUNT:
            raise ValueError("gpio must be 0..4")
        return gpio

    def _check_pwm_channel(self, channel):
        channel = int(channel)
        if not 0 <= channel <= 1:
            raise ValueError("channel must be 0..1")
        return channel

    def _check_mask(self, mask, max_mask, name="mask"):
        mask = int(mask)
        if not 0 <= mask <= max_mask:
            raise ValueError("%s must be 0..0x%02x" % (name, max_mask))
        return mask

    def _irq_regs(self, group):
        if isinstance(group, str):
            group = group.lower()
        if group not in _IRQ_KINDS:
            raise ValueError("group must be 'gpio', 'system', 'button', 0, 1, or 2")
        return _IRQ_KINDS[group]

    def _has_wakeup_enabled(self, gpio):
        return bool(self.read_reg(REG_GPIO_WAKE_EN) & (1 << gpio))

    def _check_wakeup_gpio(self, gpio):
        gpio = self._check_gpio(gpio)
        if gpio == 1:
            raise ValueError("gpio 1 does not support wakeup")
        if gpio == 0 and self._has_wakeup_enabled(2):
            raise ValueError("gpio 0 wakeup conflicts with gpio 2")
        if gpio == 2 and self._has_wakeup_enabled(0):
            raise ValueError("gpio 2 wakeup conflicts with gpio 0")
        if gpio == 3 and self._has_wakeup_enabled(4):
            raise ValueError("gpio 3 wakeup conflicts with gpio 4")
        if gpio == 4 and self._has_wakeup_enabled(3):
            raise ValueError("gpio 4 wakeup conflicts with gpio 3")
        return gpio

    def _sleep_ms(self, ms):
        if time is not None and hasattr(time, "sleep_ms"):
            time.sleep_ms(ms)

    def _read_mem(self, reg, length):
        reg = self._check_reg(reg)
        length = int(length)
        if length < 0:
            raise ValueError("length must be >= 0")
        if reg + length > 0x100:
            raise ValueError("reg + length must be <= 256")
        if length == 0:
            return b""
        return bytes(self._readfrom_mem(reg, length))

    def _write_mem(self, reg, data):
        reg = self._check_reg(reg)
        data = bytes(data)
        if reg + len(data) > 0x100:
            raise ValueError("reg + len(data) must be <= 256")
        if data:
            self._writeto_mem(reg, data)

    def read_reg(self, reg):
        """Read one byte from a register.

        Args:
            reg (int): Register address. Range: ``0..255``.

        Returns:
            int: Register value. Range: ``0..255``.

        Raises:
            ValueError: If ``reg`` is outside ``0..255``.
            OSError: If the I2C read fails.
        """
        reg = self._check_reg(reg)
        return self._readfrom_mem(reg, 1)[0]

    def write_reg(self, reg, value):
        """Write one byte to a register.

        Args:
            reg (int): Register address. Range: ``0..255``.
            value (int): Register value. Range: ``0..255``.

        Raises:
            ValueError: If ``reg`` or ``value`` is outside range.
            OSError: If the I2C write fails.
        """
        reg = self._check_reg(reg)
        value = self._check_byte(value, "value")
        self._writeto_mem(reg, bytes((value,)))

    def read_reg16(self, reg):
        """Read a little-endian 16-bit register value.

        Args:
            reg (int): First register address. Range: ``0..255``.

        Returns:
            int: Little-endian value. Range: ``0..65535``.
        """
        reg = self._check_reg(reg)
        if reg == 0xff:
            raise ValueError("reg must be 0..254 for a 16-bit read")
        data = self._readfrom_mem(reg, 2)
        return data[0] | (data[1] << 8)

    def write_reg16(self, reg, value):
        """Write a little-endian 16-bit register value.

        Args:
            reg (int): First register address. Range: ``0..255``.
            value (int): Value to write. Range: ``0..65535``.
        """
        reg = self._check_reg(reg)
        if reg == 0xff:
            raise ValueError("reg must be 0..254 for a 16-bit write")
        value = self._check_u16(value, "value")
        self._writeto_mem(reg, bytes((value & 0xff, value >> 8)))

    def update_bits(self, reg, mask, value):
        """Update selected bits in an 8-bit register.

        Args:
            reg (int): Register address. Range: ``0..255``.
            mask (int): Bit mask to update. Range: ``0..255``.
            value (int): New masked value. Range: ``0..255``.
        """
        reg = self._check_reg(reg)
        mask = self._check_byte(mask, "mask")
        value = self._check_byte(value, "value")
        current = self.read_reg(reg)
        self.write_reg(reg, (current & ~mask) | (value & mask))

    def is_connected(self):
        """Check whether a device responds at the configured I2C address.

        Returns:
            bool: ``True`` if a simple register read succeeds, otherwise
            ``False``.
        """
        try:
            self.read_reg(REG_DEVICE_ID)
            return True
        except OSError:
            return False

    def get_device_info(self):
        """Read the device information block.

        Returns:
            tuple: ``(device_id, device_model, hw_version, firmware_version)``.
            Each item is an ``int`` in ``0..255``.
        """
        data = self._readfrom_mem(REG_DEVICE_ID, 4)
        return (data[0], data[1], data[2], data[3])

    def get_uid(self):
        """Read the 12-byte device unique identifier.

        The UID range is not listed as a supported I2C Burst block, so the
        driver uses single-byte reads for firmware compatibility.

        Returns:
            bytes: Device UID. Length: ``12`` bytes.
        """
        return bytes(self.read_reg(REG_UID_START + offset) for offset in range(12))

    def get_device_id(self):
        """Read the device ID.

        Returns:
            int: Device ID. Range: ``0..255``.
        """
        return self.read_reg(REG_DEVICE_ID)

    def get_device_model(self):
        """Read the device model.

        Returns:
            int: Device model. Range: ``0..255``.
        """
        return self.read_reg(REG_DEVICE_MODEL)

    def get_hardware_version(self):
        """Read the hardware version.

        Returns:
            int: Hardware version. Range: ``0..255``.
        """
        return self.read_reg(REG_HW_REV)

    def get_firmware_version(self):
        """Read the firmware version.

        Returns:
            int: Firmware version. Range: ``0..255``.
        """
        return self.read_reg(REG_SW_REV)

    def Pin(self, gpio, mode=None, pull=_PIN_PULL_KEEP, *, value=None):
        """Create a MicroPython Pin-style object backed by M5PM1 GPIO registers.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
            mode (int | None): ``Pin.IN``, ``Pin.OUT``, or
                ``Pin.OPEN_DRAIN``. ``None`` keeps the current mode.
            pull (int | None): ``None`` disables pulls; ``Pin.PULL_UP`` and
                ``Pin.PULL_DOWN`` enable a pull. Defaults to ``-1`` to keep
                the current pull.
            value (int | bool | None): Optional initial output value.

        Returns:
            Pin: Pin-style GPIO helper.
        """
        return Pin(self, gpio, mode, pull, value=value)

    def ADC(self, channel):
        """Create a MicroPython ADC-style object for GPIO1 or GPIO2.

        Args:
            channel (int): ADC channel and GPIO index. Valid values: ``1``
                or ``2``.

        Returns:
            ADC: ADC-style helper configured for the selected input.
        """
        return ADC(self, channel)

    def PWM(self, channel, *, freq=None, duty_u16=0, duty_ns=None, invert=False):
        """Create a MicroPython PWM-style object for PWM0 or PWM1.

        Args:
            channel (int): PWM channel. Range: ``0..1``. Channels map to
                GPIO3 and GPIO4 respectively.
            freq (int | None): Shared PWM frequency in hertz. Unit: Hz.
                Range: ``1..65535``. Defaults to ``None`` to preserve the
                current frequency, or use 500 Hz if the register is zero.
            duty_u16 (int): Initial duty. Range: ``0..65535``. Defaults to 0.
            duty_ns (int | None): Initial pulse width in nanoseconds. Mutually
                exclusive with a nonzero ``duty_u16`` value.
            invert (bool): Invert output polarity. Defaults to ``False``.

        Returns:
            PWM: PWM-style helper.
        """
        return PWM(
            self,
            channel,
            freq=freq,
            duty_u16=duty_u16,
            duty_ns=duty_ns,
            invert=invert,
        )

    def NeoPixel(self, gpio, count, *, bpp=3, timing=1):
        """Create a buffered MicroPython NeoPixel-style object.

        Args:
            gpio (int): NeoPixel output pin. Only GPIO0 is supported.
            count (int): Active LED count. Range: ``1..32``.
            bpp (int): Bytes per pixel. Only RGB ``3`` is supported.
                Defaults to ``3``.
            timing (int): NeoPixel protocol timing selector. Accepted values
                are ``0`` and ``1``; M5PM1 uses its fixed hardware timing fo
                both values.

        Returns:
            NeoPixel: Buffered NeoPixel-style helper on fixed GPIO0.
        """
        return NeoPixel(self, gpio, count, bpp=bpp, timing=timing)

    def set_pin_function(self, gpio, function):
        """Set a GPIO function mux.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
            function (int): One of ``M5PM1.PIN_FUNCTION_GPIO``,
                ``PIN_FUNCTION_IRQ``, ``PIN_FUNCTION_WAKE``, or
                ``PIN_FUNCTION_OTHER``.
        """
        gpio = self._check_gpio(gpio)
        function = int(function)
        if not 0 <= function <= 3:
            raise ValueError("function must be 0..3")
        if function == _FUNC_WAKE:
            self.enable_pin_wakeup(gpio)
            return
        reg = REG_GPIO_FUNC0 if gpio < 4 else REG_GPIO_FUNC1
        shift = gpio * 2 if gpio < 4 else 0
        self.update_bits(REG_GPIO_WAKE_EN, 1 << gpio, 0)
        current = self.read_reg(reg)
        current_func = (current >> shift) & 0x03
        updated = (current & ~(0x03 << shift)) | (function << shift)
        if updated == current:
            return
        self.write_reg(reg, updated)
        if gpio == _NEOPIXEL_GPIO and (
            current_func == _FUNC_OTHER or function == _FUNC_OTHER
        ):
            # GPIO0 NeoPixel mux changes switch the PMIC clock and reset its
            # I2C peripheral. Wait for firmware recovery before the next API.
            self._sleep_ms(20)
            self.wake()

    def set_pin_mode(self, gpio, mode):
        """Set a GPIO input/output mode.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
            mode (int): ``GPIO_MODE_IN``, ``GPIO_MODE_OUT``, or
                ``GPIO_MODE_OPEN_DRAIN``.
        """
        gpio = self._check_gpio(gpio)
        if mode == _GPIO_MODE_IN:
            self.update_bits(REG_GPIO_MODE, 1 << gpio, 0)
        elif mode == _GPIO_MODE_OUT:
            self.update_bits(REG_GPIO_MODE, 1 << gpio, 1 << gpio)
            self.set_pin_drive(gpio, _DRIVE_PUSH_PULL)
        elif mode == _GPIO_MODE_OPEN_DRAIN:
            self.update_bits(REG_GPIO_MODE, 1 << gpio, 1 << gpio)
            self.set_pin_drive(gpio, _DRIVE_OPEN_DRAIN)
        else:
            raise ValueError(
                "mode must be GPIO_MODE_IN, GPIO_MODE_OUT, or GPIO_MODE_OPEN_DRAIN"
            )

    def set_pin_pull(self, gpio, pull):
        """Set GPIO pull configuration.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
            pull (int): ``GPIO_PULL_NONE``, ``GPIO_PULL_UP``, or
                ``GPIO_PULL_DOWN``.
        """
        gpio = self._check_gpio(gpio)
        pull = int(pull)
        if pull not in (_PULL_NONE, _PULL_UP, _PULL_DOWN):
            raise ValueError(
                "pull must be GPIO_PULL_NONE, GPIO_PULL_UP, or GPIO_PULL_DOWN"
            )
        reg = REG_GPIO_PUPD0 if gpio < 4 else REG_GPIO_PUPD1
        shift = gpio * 2 if gpio < 4 else 0
        self.update_bits(reg, 0x03 << shift, pull << shift)

    def set_pin_drive(self, gpio, drive):
        """Set GPIO output drive type.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
            drive (int): ``DRIVE_PUSH_PULL`` or ``DRIVE_OPEN_DRAIN``.
        """
        gpio = self._check_gpio(gpio)
        drive = int(drive)
        if drive not in (_DRIVE_PUSH_PULL, _DRIVE_OPEN_DRAIN):
            raise ValueError("drive must be DRIVE_PUSH_PULL or DRIVE_OPEN_DRAIN")
        value = (1 << gpio) if drive == _DRIVE_OPEN_DRAIN else 0
        self.update_bits(REG_GPIO_DRV, 1 << gpio, value)

    def set_pin_value(self, gpio, value):
        """Write a GPIO output latch value.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
            value (bool | int): Output value. Accepted values: ``False``,
                ``True``, ``0``, or ``1``.
        """
        gpio = self._check_gpio(gpio)
        value = 1 if _bool(value, "value") else 0
        self.update_bits(REG_GPIO_OUT, 1 << gpio, value << gpio)

    def read_pin(self, gpio):
        """Read a GPIO input value.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.

        Returns:
            int: ``0`` or ``1``.
        """
        gpio = self._check_gpio(gpio)
        return (self.read_reg(REG_GPIO_IN) >> gpio) & 1

    def get_power_source(self):
        """Read the active power-source bit mask.

        Returns:
            int: ORed ``POWER_SOURCE_*`` bits. Multiple sources may be active
                at the same time; ``POWER_SOURCE_NONE`` means no source flag.
        """
        return self.read_reg(REG_PWR_SRC) & 0x07

    def get_power_config(self):
        """Read the power-configuration bit mask.

        Returns:
            int: Bit mask containing charging, DCDC, LDO, BOOST, and LED_EN
            default-level state.
        """
        return self.read_reg(REG_PWR_CFG)

    def is_charging_enabled(self):
        """Return whether battery charging is enabled.

        M5PM1 exposes a charge-enable bit but no independent charge-in-progress
        flag, so this method reports the configured ``CHG_EN`` state.

        Returns:
            bool: ``True`` when ``PWR_CFG.CHG_EN`` is set.
        """
        return bool(self.get_power_config() & _PWR_CHG_EN)

    def is_dcdc_enabled(self):
        """Return whether the DCDC power rail is enabled.

        Returns:
            bool: ``True`` when ``PWR_CFG.DCDC_EN`` is set.
        """
        return bool(self.get_power_config() & _PWR_DCDC_EN)

    def is_ldo_enabled(self):
        """Return whether the LDO power rail is enabled.

        Returns:
            bool: ``True`` when ``PWR_CFG.LDO_EN`` is set.
        """
        return bool(self.get_power_config() & _PWR_LDO_EN)

    def is_boost_enabled(self):
        """Return whether the BOOST / 5VINOUT power rail is enabled.

        Returns:
            bool: ``True`` when ``PWR_CFG.BOOST_EN`` is set.
        """
        return bool(self.get_power_config() & _PWR_BOOST_EN)

    def _set_power_bit(self, mask, enable):
        self.update_bits(REG_PWR_CFG, mask, mask if enable else 0)

    def enable_charging(self):
        """Enable battery charging."""
        self._set_power_bit(_PWR_CHG_EN, True)

    def disable_charging(self):
        """Disable battery charging."""
        self._set_power_bit(_PWR_CHG_EN, False)

    def enable_dcdc(self):
        """Enable the DCDC power rail."""
        self._set_power_bit(_PWR_DCDC_EN, True)

    def disable_dcdc(self):
        """Disable the DCDC power rail.

        Warning:
            Disabling this rail may power off board peripherals depending on
            the hardware design.
        """
        self._set_power_bit(_PWR_DCDC_EN, False)

    def enable_ldo(self):
        """Enable the LDO power rail."""
        self._set_power_bit(_PWR_LDO_EN, True)

    def disable_ldo(self):
        """Disable the LDO power rail."""
        self._set_power_bit(_PWR_LDO_EN, False)

    def enable_boost(self):
        """Enable the BOOST / 5VINOUT power rail."""
        self._set_power_bit(_PWR_BOOST_EN, True)

    def disable_boost(self):
        """Disable the BOOST / 5VINOUT power rail.

        Warning:
            Disabling this rail may remove power from Grove or external 5V
            outputs depending on the board design.
        """
        self._set_power_bit(_PWR_BOOST_EN, False)

    def set_led_enable_level(self, level):
        """Set the LED_EN default output level bit.

        Args:
            level (bool): ``True`` for high level, ``False`` for low level.
        """
        level = _bool(level, "level")
        self.update_bits(REG_PWR_CFG, _PWR_LED_CTRL, _PWR_LED_CTRL if level else 0)

    def set_battery_low_voltage_threshold_mv(self, voltage_mv):
        """Set the battery low-voltage protection threshold.

        Args:
            voltage_mv (int): Threshold in millivolts. Unit: mV.
                Range: ``2000..3991``.

        Raises:
            ValueError: If ``voltage_mv`` is outside ``2000..3991``.
        """
        voltage_mv = int(voltage_mv)
        if not 2000 <= voltage_mv <= 3991:
            raise ValueError("voltage_mv must be 2000..3991")
        self.write_reg(REG_BATT_LVP, ((voltage_mv - 2000) * 100 + 390) // 781)

    def get_battery_low_voltage_threshold_mv(self):
        """Read the configured battery low-voltage threshold.

        Returns:
            int: Threshold in millivolts. Unit: mV. Range: ``2000..3991``.
        """
        return 2000 + (self.read_reg(REG_BATT_LVP) * 781) // 100

    def enable_gpio_power_hold(self, gpio):
        """Enable power-hold behavior for one GPIO output.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
        """
        gpio = self._check_gpio(gpio)
        self.update_bits(REG_HOLD_CFG, 1 << gpio, 1 << gpio)

    def disable_gpio_power_hold(self, gpio):
        """Disable power-hold behavior for one GPIO output.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
        """
        gpio = self._check_gpio(gpio)
        self.update_bits(REG_HOLD_CFG, 1 << gpio, 0)

    def enable_ldo_power_hold(self):
        """Enable LDO power hold."""
        self.update_bits(REG_HOLD_CFG, _HOLD_LDO, _HOLD_LDO)

    def disable_ldo_power_hold(self):
        """Disable LDO power hold."""
        self.update_bits(REG_HOLD_CFG, _HOLD_LDO, 0)

    def enable_boost_power_hold(self):
        """Enable BOOST / 5VINOUT power hold."""
        self.update_bits(REG_HOLD_CFG, _HOLD_BOOST, _HOLD_BOOST)

    def disable_boost_power_hold(self):
        """Disable BOOST / 5VINOUT power hold."""
        self.update_bits(REG_HOLD_CFG, _HOLD_BOOST, 0)

    def read_adc_raw(self, channel):
        """Read a raw ADC conversion value.

        Args:
            channel (int): ADC channel. Valid values: ``1``, ``2``, or ``6``.
                Channel ``6`` is the internal temperature sensor.

        Returns:
            int: Raw 12-bit ADC value. Range: ``0..4095``.

        Raises:
            ValueError: If ``channel`` is invalid.
            OSError: If the conversion times out or I2C access fails.
        """
        channel = int(channel)
        if channel not in _ADC_CHANNELS:
            raise ValueError("channel must be 1, 2, or 6")
        self.write_reg(REG_ADC_CTRL, ((channel & 0x07) << 1) | 0x01)
        for _ in range(50):
            self._sleep_ms(10)
            if not (self.read_reg(REG_ADC_CTRL) & 0x01):
                return self.read_reg16(REG_ADC_RES_L) & _PWM_DUTY_MASK
        raise OSError("m5pm1 adc timeout: channel=%d" % channel)

    def read_adc_mv(self, channel):
        """Read an external ADC channel in millivolts.

        Args:
            channel (int): ADC channel. Valid values: ``1`` or ``2``.

        Returns:
            int: Voltage in millivolts. Unit: mV.
        """
        channel = int(channel)
        if channel not in (1, 2):
            raise ValueError("channel must be 1 or 2")
        return (self.read_adc_raw(channel) * self.read_reference_voltage_mv()) // _PWM_DUTY_MASK

    def read_temperature_raw(self):
        """Read the internal temperature sensor raw code.

        Returns:
            int: Raw 12-bit temperature code. Range: ``0..4095``.
        """
        return self.read_adc_raw(6)

    def read_button(self):
        """Read the current PM1 button state.

        Returns:
            int: ``0`` when released, ``1`` when pressed.
        """
        return self.read_reg(REG_BTN_STATUS) & 1

    def read_button_event(self):
        """Read the sticky button-pressed flag.

        Returns:
            bool: ``True`` if the PM1 button flag is set.

        Note:
            PM1 firmware auto-clears the hardware flag when ``BTN_STATUS`` is
            read.
        """
        return bool(self.read_reg(REG_BTN_STATUS) & 0x80)

    def set_button_timing(self, event, duration_ms):
        """Configure button timing.

        Args:
            event (int): ``BUTTON_TIMING_CLICK``, ``BUTTON_TIMING_DOUBLE``,
                or ``BUTTON_TIMING_LONG``.
            duration_ms (int): Duration in milliseconds. Unit: ms. Valid values are
                ``125``, ``250``, ``500``, ``1000`` for click/double-click and
                ``1000``, ``2000``, ``3000``, ``4000`` for long press.
        """
        event = int(event)
        if event == self.BUTTON_TIMING_CLICK:
            shift = 1
            options = (125, 250, 500, 1000)
        elif event == self.BUTTON_TIMING_LONG:
            shift = 3
            options = (1000, 2000, 3000, 4000)
        elif event == self.BUTTON_TIMING_DOUBLE:
            shift = 5
            options = (125, 250, 500, 1000)
        else:
            raise ValueError(
                "event must be BUTTON_TIMING_CLICK, BUTTON_TIMING_DOUBLE, "
                "or BUTTON_TIMING_LONG"
            )
        duration_ms = int(duration_ms)
        if duration_ms not in options:
            raise ValueError("duration_ms must be one of %s" % (options,))
        value = options.index(duration_ms)
        self.update_bits(REG_BTN_CFG_1, 0x03 << shift, value << shift)

    def _read_voltage_mv(self, reg):
        return self.read_reg16(reg)

    def read_reference_voltage_mv(self):
        """Read the PM1 reference voltage.

        Returns:
            int: Voltage in millivolts. Unit: mV.
        """
        return self._read_voltage_mv(REG_VREF_L)

    def read_battery_voltage_mv(self):
        """Read the battery voltage.

        Returns:
            int: Voltage in millivolts. Unit: mV.
        """
        return self._read_voltage_mv(REG_VBAT_L)

    def read_vin_voltage_mv(self):
        """Read VIN voltage.

        Returns:
            int: Voltage in millivolts. Unit: mV.
        """
        return self._read_voltage_mv(REG_VIN_L)

    def read_5v_inout_voltage_mv(self):
        """Read 5VINOUT voltage.

        Returns:
            int: Voltage in millivolts. Unit: mV.
        """
        return self._read_voltage_mv(REG_5VINOUT_L)

    def get_wake_source(self, *, clear=False):
        """Read wake-source flags.

        Args:
            clear (bool): Clear the returned flags. Defaults to ``False``.

        Returns:
            int: Wake-source bit mask.

        Note:
            PM1 wake-source flags are write-0-to-clear.
        """
        clear = _bool(clear, "clear")
        value = self.read_reg(REG_WAKE_SRC) & 0x7f
        if clear and value:
            self.write_reg(REG_WAKE_SRC, 0x7f & ~value)
        return value

    def clear_wake_source(self, mask=None):
        """Clear wake-source flags.

        Args:
            mask (int | None): Flags to clear. Defaults to ``None`` to clear
                all wake-source flags.

        Note:
            PM1 wake-source flags are write-0-to-clear.
        """
        if mask is None:
            self.write_reg(REG_WAKE_SRC, 0)
            return
        mask = self._check_mask(mask, 0x7f)
        self.write_reg(REG_WAKE_SRC, 0x7f & ~mask)

    def set_pwm_frequency(self, frequency):
        """Set the shared PWM frequency.

        Args:
            frequency (int): PWM frequency in hertz. Unit: Hz.
                Range: ``1..65535``.
        """
        frequency = self._check_u16(frequency, "frequency")
        if frequency == 0:
            raise ValueError("frequency must be 1..65535")
        self.write_reg16(REG_PWM_FREQ_L, frequency)

    def get_pwm_frequency(self):
        """Read the shared PWM frequency.

        Returns:
            int: PWM frequency in hertz. Unit: Hz.
        """
        return self.read_reg16(REG_PWM_FREQ_L)

    def _pwm_reg(self, channel):
        channel = self._check_pwm_channel(channel)
        return REG_PWM0_L if channel == 0 else REG_PWM1_L

    def _read_pwm_raw(self, channel):
        value = self.read_reg16(self._pwm_reg(channel))
        return value & _PWM_DUTY_MASK, bool(value & (_PWM_POLARITY << 8)), bool(value & (_PWM_EN << 8))

    def _write_pwm_raw(self, channel, duty, invert, enabled):
        duty = int(duty)
        if not 0 <= duty <= _PWM_DUTY_MASK:
            raise ValueError("duty must be 0..4095")
        high = (duty >> 8) & 0x0f
        if _bool(invert, "invert"):
            high |= _PWM_POLARITY
        if _bool(enabled, "enabled"):
            high |= _PWM_EN
        self._write_mem(self._pwm_reg(channel), (duty & 0xff, high))

    def set_pwm_duty_percent(self, channel, percent, *, invert=False):
        """Set a PWM channel duty by percent.

        Args:
            channel (int): PWM channel. Range: ``0..1``.
            percent (int): Duty cycle in percent. Unit: percent. Range:
                ``0..100``.
            invert (bool): ``True`` for inverted output. Defaults to
                ``False``.
        """
        percent = int(percent)
        if not 0 <= percent <= 100:
            raise ValueError("percent must be 0..100")
        _, _, enabled = self._read_pwm_raw(channel)
        self._write_pwm_raw(
            channel,
            (percent * _PWM_DUTY_MASK + 50) // 100,
            invert,
            enabled,
        )

    def set_pwm_duty_u12(self, channel, duty_u12, *, invert=False):
        """Set a PWM channel duty by 12-bit code.

        Args:
            channel (int): PWM channel. Range: ``0..1``.
            duty_u12 (int): Duty code. Range: ``0..4095``.
            invert (bool): ``True`` for inverted output. Defaults to
                ``False``.
        """
        duty_u12 = int(duty_u12)
        if not 0 <= duty_u12 <= _PWM_DUTY_MASK:
            raise ValueError("duty_u12 must be 0..4095")
        _, _, enabled = self._read_pwm_raw(channel)
        self._write_pwm_raw(channel, duty_u12, invert, enabled)

    def enable_pwm(self, channel):
        """Enable a PWM output channel.

        Args:
            channel (int): PWM channel. Range: ``0..1``.
        """
        duty, polarity, _ = self._read_pwm_raw(channel)
        self._write_pwm_raw(channel, duty, polarity, True)

    def disable_pwm(self, channel):
        """Disable a PWM output channel.

        Args:
            channel (int): PWM channel. Range: ``0..1``.
        """
        duty, polarity, _ = self._read_pwm_raw(channel)
        self._write_pwm_raw(channel, duty, polarity, False)

    def get_pwm_duty_percent(self, channel):
        """Read a PWM channel duty by percent.

        Args:
            channel (int): PWM channel. Range: ``0..1``.

        Returns:
            int: Duty cycle in percent. Range: ``0..100``.
        """
        duty, _, _ = self._read_pwm_raw(channel)
        return (duty * 100 + (_PWM_DUTY_MASK // 2)) // _PWM_DUTY_MASK

    def get_pwm_duty_u12(self, channel):
        """Read a PWM channel duty by 12-bit code.

        Args:
            channel (int): PWM channel. Range: ``0..1``.

        Returns:
            int: Duty code. Range: ``0..4095``.
        """
        duty, _, _ = self._read_pwm_raw(channel)
        return duty

    def _rgb888_to_rgb565(self, color):
        if isinstance(color, int):
            if not 0 <= color <= 0xffffff:
                raise ValueError("color must be 0..0xffffff")
            r = (color >> 16) & 0xff
            g = (color >> 8) & 0xff
            b = color & 0xff
        else:
            if len(color) != 3:
                raise ValueError("color tuple must have 3 items")
            r, g, b = [self._check_byte(c, "color") for c in color]
        return ((r & 0xf8) << 8) | ((g & 0xfc) << 3) | (b >> 3)

    def set_neopixel_count(self, count):
        """Set the active NeoPixel LED count.

        Args:
            count (int): Active LED count. Range: ``0..32``.
        """
        count = int(count)
        if not 0 <= count <= 32:
            raise ValueError("count must be 0..32")
        self._led_count = count
        self.update_bits(REG_NEO_CFG, _NEO_COUNT_MASK, count)

    def set_neopixel_color(self, index, color):
        """Write one RGB888 color into LED RAM.

        Args:
            index (int): LED index. Range: ``0..31``.
            color (int | tuple): RGB888 color, either ``0xRRGGBB`` or
                ``(r, g, b)`` with each channel in ``0..255``.
        """
        index = int(index)
        if not 0 <= index < 32:
            raise ValueError("index must be 0..31")
        self.write_reg16(REG_NEO_DATA_START + index * 2, self._rgb888_to_rgb565(color))

    def write_neopixels(self, colors, *, auto_refresh=True):
        """Write multiple RGB888 colors into LED RAM.

        Args:
            colors: Iterable of RGB888 colors. Length range: ``0..32``.
            auto_refresh (bool): Refresh LEDs after writing. Defaults to
                ``True``.

        Raises:
            ValueError: If ``auto_refresh`` is not boolean, the color count
                exceeds 32, or a color value is invalid.
        """
        auto_refresh = _bool(auto_refresh, "auto_refresh")
        colors = list(colors)
        if len(colors) > 32:
            raise ValueError("colors length must be <= 32")
        self.set_neopixel_count(len(colors))
        data = bytearray()
        for color in colors:
            rgb565 = self._rgb888_to_rgb565(color)
            data.append(rgb565 & 0xff)
            data.append((rgb565 >> 8) & 0xff)
        if data:
            self._write_mem(REG_NEO_DATA_START, data)
        if auto_refresh:
            self.refresh_neopixels()

    def refresh_neopixels(self):
        """Refresh NeoPixel output from LED RAM.

        M5PM1 rejects I2C traffic while emitting the NeoPixel waveform. The
        worst-case 32-pixel refresh takes about 7 ms, so the driver waits 8 ms
        before returning.
        """
        self.update_bits(REG_NEO_CFG, _NEO_REFRESH, _NEO_REFRESH)
        self._sleep_ms(8)

    def clear_neopixels(self, *, auto_refresh=True):
        """Clear LED RAM to black.

        Args:
            auto_refresh (bool): Refresh LEDs after clearing. Defaults to
                ``True``.

        Raises:
            ValueError: If ``auto_refresh`` is not boolean.
        """
        auto_refresh = _bool(auto_refresh, "auto_refresh")
        count = self._led_count or (self.read_reg(REG_NEO_CFG) & _NEO_COUNT_MASK)
        if count:
            self._write_mem(REG_NEO_DATA_START, bytes(count * 2))
        if auto_refresh:
            self.refresh_neopixels()

    def enable_neopixels(self):
        """Enable NeoPixel output without changing LED RAM."""
        count = self._led_count or (self.read_reg(REG_NEO_CFG) & _NEO_COUNT_MASK) or 1
        self.set_neopixel_count(count)

    def disable_neopixels(self):
        """Disable NeoPixel output without clearing LED RAM."""
        self.write_reg(REG_NEO_CFG, 0)
        self._led_count = 0

    def set_aw8737a_pulse(self, gpio, pulses, *, refresh=True):
        """Configure AW8737A pulse output.

        Args:
            gpio (int): Output GPIO index. Range: ``0..4``.
            pulses (int): Pulse count. Range: ``0..3``.
            refresh (bool): Execute the pulse immediately. Defaults to
                ``True``.
        """
        gpio = self._check_gpio(gpio)
        pulses = int(pulses)
        if not 0 <= pulses <= 3:
            raise ValueError("pulses must be 0..3")
        value = gpio | (pulses << 5)
        self.write_reg(REG_AW8737A_PULSE, value | (_AW_REFRESH if _bool(refresh, "refresh") else 0))
        self._last_aw8737a = value

    def refresh_aw8737a(self):
        """Execute the last configured AW8737A pulse output."""
        value = self.read_reg(REG_AW8737A_PULSE) & 0x7f
        if value == 0 and self._last_aw8737a:
            value = self._last_aw8737a
        self.write_reg(REG_AW8737A_PULSE, value | _AW_REFRESH)

    def set_aw8737a_mode(self, gpio, mode, *, refresh=True):
        """Set AW8737A gain mode.

        Args:
            gpio (int): Output GPIO index. Range: ``0..4``.
            mode (int): Gain mode. Range: ``0..3``. The value maps directly
                to the pulse count.
            refresh (bool): Execute the pulse immediately. Defaults to
                ``True``.
        """
        mode = int(mode)
        if not 0 <= mode <= 3:
            raise ValueError("mode must be 0..3")
        self.set_aw8737a_pulse(gpio, mode, refresh=refresh)

    def get_irq_status(self, group, *, clear=False):
        """Read an IRQ status group.

        Args:
            group (str | int): IRQ group. Valid values: ``"gpio"``,
                ``"system"``, ``"button"``, ``0``, ``1``, or ``2``.
            clear (bool): Clear the returned flags. Defaults to ``False``.

        Returns:
            int: IRQ status bit mask.

        Note:
            PM1 IRQ status registers are write-0-to-clear.
        """
        status_reg, _, valid_mask = self._irq_regs(group)
        clear = _bool(clear, "clear")
        value = self.read_reg(status_reg) & valid_mask
        if clear and value:
            self.write_reg(status_reg, valid_mask & ~value)
        return value

    def _read_irq_snapshot(self, *, clear=False):
        """Read all three IRQ status groups as one coherent snapshot."""
        clear = _bool(clear, "clear")
        data = self._read_mem(REG_IRQ_STATUS1, 3)
        gpio = data[0] & 0x1f
        system = data[1] & 0x3f
        button = data[2] & 0x07
        if clear:
            if gpio:
                self.write_reg(REG_IRQ_STATUS1, 0x1f & ~gpio)
            if system:
                self.write_reg(REG_IRQ_STATUS2, 0x3f & ~system)
            if button:
                self.write_reg(REG_IRQ_STATUS3, 0x07 & ~button)
        return gpio, system, button

    def clear_irq(self, group, mask=None):
        """Clear IRQ status bits.

        Args:
            group (str | int): IRQ group. Valid values are the same as
                :meth:`get_irq_status`.
            mask (int | None): Bits to clear. Defaults to ``None`` to clear
                all bits in the group.

        Note:
            PM1 IRQ status registers are write-0-to-clear.
        """
        status_reg, _, valid_mask = self._irq_regs(group)
        if mask is None:
            self.write_reg(status_reg, 0)
            return
        mask = self._check_mask(mask, valid_mask)
        self.write_reg(status_reg, valid_mask & ~mask)

    def disable_irq_events(self, group, events):
        """Disable selected IRQ events.

        Args:
            group (str | int): IRQ group.
            events (int): Event bits to disable.
        """
        _, mask_reg, valid_mask = self._irq_regs(group)
        events = self._check_mask(events, valid_mask, "events")
        self.update_bits(mask_reg, events, events)

    def enable_irq_events(self, group, events):
        """Enable selected IRQ events.

        Args:
            group (str | int): IRQ group.
            events (int): Event bits to enable.
        """
        _, mask_reg, valid_mask = self._irq_regs(group)
        events = self._check_mask(events, valid_mask, "events")
        self.update_bits(mask_reg, events, 0)

    def enable_pin_wakeup(self, gpio):
        """Enable GPIO wakeup.

        Args:
            gpio (int): GPIO index. Range: ``0..4``. GPIO1 does not support
                wakeup. GPIO0 conflicts with GPIO2, and GPIO3 conflicts with
                GPIO4.

        Raises:
            ValueError: If the GPIO does not support wakeup or conflicts with
                an already enabled wake input.
        """
        gpio = self._check_wakeup_gpio(gpio)
        func_reg = REG_GPIO_FUNC0 if gpio < 4 else REG_GPIO_FUNC1
        shift = gpio * 2 if gpio < 4 else 0
        self.update_bits(func_reg, 0x03 << shift, _FUNC_GPIO << shift)
        self.update_bits(REG_GPIO_MODE, 1 << gpio, 0)
        self.update_bits(REG_GPIO_WAKE_EN, 1 << gpio, 1 << gpio)

    def disable_pin_wakeup(self, gpio):
        """Disable GPIO wakeup.

        Args:
            gpio (int): GPIO index. Range: ``0..4``.
        """
        gpio = self._check_gpio(gpio)
        self.update_bits(REG_GPIO_WAKE_EN, 1 << gpio, 0)

    def set_pin_wakeup_edge(self, gpio, edge):
        """Set GPIO wakeup edge.

        Args:
            gpio (int): GPIO index. Range: ``0..4``. GPIO1 is not supported.
            edge (int): ``0`` for falling edge, ``1`` for rising edge.
        """
        gpio = self._check_gpio(gpio)
        if gpio == 1:
            raise ValueError("gpio 1 does not support wakeup")
        edge = int(edge)
        if edge not in (0, 1):
            raise ValueError("edge must be 0 or 1")
        self.update_bits(REG_GPIO_WAKE_CFG, 1 << gpio, edge << gpio)

    def enable_watchdog(self, timeout_s):
        """Enable the watchdog and set its timeout.

        Args:
            timeout_s (int): Timeout in seconds. Unit: s. Range: ``1..255``.
        """
        timeout_s = self._check_byte(timeout_s, "timeout_s")
        if timeout_s == 0:
            raise ValueError("timeout_s must be 1..255")
        self.write_reg(REG_WDT_CNT, timeout_s)

    def disable_watchdog(self):
        """Disable the watchdog."""
        self.write_reg(REG_WDT_CNT, 0)

    def feed_watchdog(self):
        """Feed the watchdog."""
        self.write_reg(REG_WDT_KEY, _WDT_FEED_KEY)

    def get_watchdog_countdown_s(self):
        """Read the watchdog countdown.

        Returns:
            int: Remaining watchdog count. Unit: s. Range: ``0..255``.
        """
        return self.read_reg(REG_WDT_CNT)

    def set_timer(self, duration_s, action):
        """Set the PM1 timer and timeout action.

        Args:
            duration_s (int): Timer duration in seconds. Unit: s.
                Range: ``0..2147483647``.
            action (int): Timer action. Use ``TIMER_ACTION_*`` constants.
                Range: ``0..4``.
        """
        duration_s = int(duration_s)
        if not 0 <= duration_s <= 0x7fffffff:
            raise ValueError("duration_s must be 0..2147483647")
        action = int(action)
        if not 0 <= action <= self.TIMER_ACTION_POWER_OFF:
            raise ValueError("action must be 0..4")
        self._write_mem(REG_TIM_CNT_0, (
            duration_s & 0xff,
            (duration_s >> 8) & 0xff,
            (duration_s >> 16) & 0xff,
            (duration_s >> 24) & 0x7f,
        ))
        self.write_reg(REG_TIM_CFG, 0x08 | action)
        self.write_reg(REG_TIM_KEY, _TIM_RELOAD_KEY)

    def clear_timer(self):
        """Stop and clear the PM1 timer."""
        self.write_reg(REG_TIM_CFG, 0)
        self.write_reg(REG_TIM_KEY, _TIM_RELOAD_KEY)

    def set_i2c_sleep_timeout_s(self, timeout_s):
        """Set PM1 I2C idle sleep timeout.

        Args:
            timeout_s (int): Idle sleep timeout in seconds. Unit: s.
                Range: ``0..15``.
        """
        timeout_s = int(timeout_s)
        if not 0 <= timeout_s <= 15:
            raise ValueError("timeout_s must be 0..15")
        self.update_bits(REG_I2C_CFG, _I2C_SLEEP_MASK, timeout_s)

    def get_i2c_sleep_timeout_s(self):
        """Read PM1 I2C idle sleep timeout.

        Returns:
            int: Timeout in seconds. Unit: s. Range: ``0..15``.
        """
        return self.read_reg(REG_I2C_CFG) & _I2C_SLEEP_MASK

    def set_i2c_frequency(self, frequency):
        """Set PM1 device-side I2C speed mode.

        Args:
            frequency (int): I2C speed in hertz. Unit: Hz. Valid values:
                ``100000`` or ``400000``.
        """
        if frequency not in (100000, 400000):
            raise ValueError("frequency must be 100000 or 400000")
        self.update_bits(REG_I2C_CFG, _I2C_SPEED_400K, _I2C_SPEED_400K if frequency == 400000 else 0)

    def get_i2c_frequency(self):
        """Read the PM1 device-side I2C speed mode.

        Returns:
            int: I2C frequency in hertz. Unit: Hz. Returns ``100000`` o
                ``400000``.
        """
        return 400000 if self.read_reg(REG_I2C_CFG) & _I2C_SPEED_400K else 100000

    def read_rtc_ram(self, offset=0, length=32):
        """Read RTC retention RAM.

        Args:
            offset (int): Start offset. Range: ``0..31``. Defaults to ``0``.
            length (int): Number of bytes. Range: ``0..32``. Defaults to
                ``32``. ``offset + length`` must be less than or equal to
                ``32``.

        Returns:
            bytes: RTC RAM data.
        """
        offset = int(offset)
        length = int(length)
        if not 0 <= offset <= 31:
            raise ValueError("offset must be 0..31")
        if not 0 <= length <= 32 or offset + length > 32:
            raise ValueError("length must be 0..32 and offset + length <= 32")
        return self._read_mem(REG_RTC_RAM_START + offset, length)

    def write_rtc_ram(self, offset, data):
        """Write RTC retention RAM.

        Args:
            offset (int): Start offset. Range: ``0..31``.
            data: Bytes-like object. ``offset + len(data)`` must be less than
                or equal to ``32``.
        """
        offset = int(offset)
        data = bytes(data)
        if not 0 <= offset <= 31:
            raise ValueError("offset must be 0..31")
        if offset + len(data) > 32:
            raise ValueError("offset + len(data) must be <= 32")
        self._write_mem(REG_RTC_RAM_START + offset, data)

    def restore_defaults(self):
        """Restore writable M5PM1 configuration to documented defaults.

        This resets power, GPIO, wake, ADC, PWM, timer, IRQ, button,
        NeoPixel, and AW8737A configuration. Event callbacks are removed.
        Device identity, UID, and the 32-byte RTC retention RAM are preserved.

        Warning:
            Restoring power rails and GPIO configuration can immediately
            change board power and external signal levels. Existing Pin,
            ADC, PWM, and NeoPixel helper objects must be reinitialized before
            reuse. The PM1 device-side I2C speed returns to 100 kHz; the host
            I2C bus must use the same speed for subsequent access.
        """
        self.deinit()

        self.write_reg(REG_WAKE_SRC, 0x00)

        # System configuration, excluding I2C_CFG which is restored last.
        self._write_mem(REG_PWR_CFG, bytes((0x17, 0x00, 0x40)))
        self.write_reg(REG_WDT_CNT, 0x00)

        # GPIO input, output, drive, pull, function, and wake defaults.
        self._write_mem(REG_GPIO_MODE, bytes((0x00, 0x00)))
        self._write_mem(REG_GPIO_DRV, bytes((0x1F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00)))

        self.write_reg(REG_ADC_CTRL, 0x00)

        # PWM channels disabled at zero duty; shared frequency is 500 Hz.
        self._write_mem(REG_PWM0_L, bytes((0x00, 0x00, 0x00, 0x00, 0xF4, 0x01)))
        self._write_mem(REG_TIM_CNT_0, bytes((0x00, 0x00, 0x00, 0x00, 0x00)))

        # Clear sticky IRQ status and restore unmasked defaults.
        self._write_mem(REG_IRQ_STATUS1, bytes((0x00, 0x00, 0x00, 0x00, 0x00, 0x00)))
        self._write_mem(REG_BTN_CFG_1, bytes((0x2A, 0x00)))

        self.write_reg(REG_NEO_CFG, 0x00)
        self.write_reg(REG_AW8737A_PULSE, 0x00)
        self._write_mem(REG_NEO_DATA_START, bytes(64))

        self._led_count = 0
        self._last_aw8737a = 0

        # Restore 100 kHz and disable I2C idle sleep only after other writes.
        self.write_reg(REG_I2C_CFG, 0x00)

    def _system_command(self, command):
        self._sleep_ms(120)
        self.write_reg(REG_SYS_CMD, _SYS_CMD_KEY | command)

    def power_off(self):
        """Request PM1 shutdown.

        Warning:
            This command may power off the board before Python continues.
        """
        self._system_command(_SYS_CMD_SHUTDOWN)

    def reboot(self):
        """Request PM1 reboot.

        Warning:
            This command may reset the board before Python continues.
        """
        self._system_command(_SYS_CMD_REBOOT)

    def enter_download_mode(self):
        """Request PM1 download mode.

        Warning:
            This command changes boot/recovery behavior and should only be
            called on explicit user request.
        """
        self._system_command(_SYS_CMD_DOWNLOAD)

    def enable_download_lock(self):
        """Enable the PM1 download-mode lock.

        Warning:
            This may make firmware recovery harder until the PM1 loses power.
        """
        self.update_bits(REG_BTN_CFG_1, 0x80, 0x80)

    def disable_download_lock(self):
        """Disable the PM1 download-mode lock."""
        self.update_bits(REG_BTN_CFG_1, 0x80, 0)

    def enable_single_click_reset(self):
        """Enable single-click reset behavior."""
        self.update_bits(REG_BTN_CFG_1, 0x01, 0)

    def disable_single_click_reset(self):
        """Disable single-click reset behavior."""
        self.update_bits(REG_BTN_CFG_1, 0x01, 0x01)

    def enable_double_click_power_off(self):
        """Enable double-click power-off behavior."""
        self.update_bits(REG_BTN_CFG_2, 0x01, 0)

    def disable_double_click_power_off(self):
        """Disable double-click poweroff behavior."""
        self.update_bits(REG_BTN_CFG_2, 0x01, 0x01)


class ADC:
    """M5PM1 ADC object compatible with the common MicroPython ADC API.

    Args:
        pmic (M5PM1): Parent M5PM1 driver instance.
        channel (int): ADC channel and GPIO index. Valid values: ``1`` or
            ``2``.

    The constructor claims the selected pin's alternate function. Call
    :meth:`deinit` to restore it as a floating GPIO input.
    """

    def __init__(self, pmic, channel):
        self.pmic = pmic
        self.channel = int(channel)
        if self.channel not in (1, 2):
            raise ValueError("channel must be 1 or 2")
        self._active = False
        self.init()

    def _require_active(self):
        if not self._active:
            raise RuntimeError("ADC is deinitialized")

    def init(self):
        """Initialize or reinitialize the ADC input.

        This method is idempotent and restores an object after
        :meth:`deinit`.
        """
        self.pmic.set_pin_pull(self.channel, _PULL_NONE)
        self.pmic.set_pin_mode(self.channel, _GPIO_MODE_IN)
        self.pmic.set_pin_function(self.channel, M5PM1.PIN_FUNCTION_OTHER)
        self._active = True

    def deinit(self):
        """Release the ADC function and restore a floating GPIO input."""
        if not self._active:
            return
        self.pmic.set_pin_function(self.channel, M5PM1.PIN_FUNCTION_GPIO)
        self.pmic.set_pin_mode(self.channel, _GPIO_MODE_IN)
        self.pmic.set_pin_pull(self.channel, _PULL_NONE)
        self._active = False

    def read(self):
        """Read the native 12-bit ADC code.

        Returns:
            int: Raw ADC code. Range: ``0..4095``.
        """
        self._require_active()
        return self.pmic.read_adc_raw(self.channel)

    def read_u16(self):
        """Read a full-scale normalized unsigned 16-bit value.

        Returns:
            int: Normalized ADC value. Range: ``0..65535``.
        """
        raw = self.read()
        return (raw * _PWM_U16_MAX + (_ADC_MAX // 2)) // _ADC_MAX

    def read_uv(self):
        """Read the ADC input voltage in microvolts.

        Returns:
            int: Input voltage in microvolts. Unit: uV.
        """
        self._require_active()
        return self.pmic.read_adc_mv(self.channel) * 1000

class PWM:
    """M5PM1 PWM object compatible with the common MicroPython PWM API.

    Args:
        pmic (M5PM1): Parent M5PM1 driver instance.
        channel (int): PWM channel. Range: ``0..1``. Channels map to GPIO3
            and GPIO4 respectively.
        freq (int | None): Shared frequency in hertz. Unit: Hz. Range:
            ``1..65535``. Defaults to ``None`` to preserve the current value.
        duty_u16 (int): Initial duty. Range: ``0..65535``. Defaults to 0.
        duty_ns (int | None): Initial pulse width in nanoseconds. Mutually
            exclusive with a nonzero ``duty_u16`` value.
        invert (bool): Invert output polarity. Defaults to ``False``.

    Both PWM channels share one hardware frequency register. Setting
    :meth:`freq` on either object changes the frequency of both channels.
    """

    def __init__(self, pmic, channel, *, freq=None, duty_u16=0, duty_ns=None, invert=False):
        self.pmic = pmic
        self.channel = pmic._check_pwm_channel(channel)
        self.gpio = _PWM_GPIOS[self.channel]
        self._active = False
        self.init(freq=freq, duty_u16=duty_u16, duty_ns=duty_ns, invert=invert)

    def _require_active(self):
        if not self._active:
            raise RuntimeError("PWM is deinitialized")

    def _period_ns(self):
        frequency = self.pmic.get_pwm_frequency()
        if frequency <= 0:
            raise RuntimeError("PWM frequency is zero")
        return 1000000000 // frequency

    def _duty12_from_u16(self, value):
        value = int(value)
        if not 0 <= value <= _PWM_U16_MAX:
            raise ValueError("duty_u16 must be 0..65535")
        return (value * _PWM_DUTY_MASK + (_PWM_U16_MAX // 2)) // _PWM_U16_MAX

    def _duty12_from_ns(self, value):
        value = int(value)
        period_ns = self._period_ns()
        if not 0 <= value <= period_ns:
            raise ValueError("duty_ns must be 0..%d" % period_ns)
        return (value * _PWM_DUTY_MASK + (period_ns // 2)) // period_ns

    def init(self, *, freq=None, duty_u16=None, duty_ns=None, invert=None):
        """Initialize or reconfigure the PWM output.

        Args:
            freq (int | None): Shared frequency in hertz. Unit: Hz. Range:
                ``1..65535``. ``None`` preserves the current value.
            duty_u16 (int | None): Duty in ``0..65535``. ``None`` preserves
                the current duty.
            duty_ns (int | None): Pulse width in nanoseconds. Mutually
                exclusive with ``duty_u16``.
            invert (bool | None): Output polarity. ``None`` preserves it.
        """
        if duty_u16 is not None and duty_ns is not None:
            if int(duty_u16) != 0:
                raise ValueError("duty_u16 and duty_ns are mutually exclusive")
            duty_u16 = None
        self.pmic.set_pin_drive(self.gpio, _DRIVE_PUSH_PULL)
        self.pmic.set_pin_function(self.gpio, M5PM1.PIN_FUNCTION_OTHER)
        self._active = True

        if freq is not None:
            self.pmic.set_pwm_frequency(freq)
        elif self.pmic.get_pwm_frequency() == 0:
            self.pmic.set_pwm_frequency(_PWM_DEFAULT_FREQ)

        current_duty, current_invert, _ = self.pmic._read_pwm_raw(self.channel)
        polarity = current_invert if invert is None else _bool(invert, "invert")
        if duty_u16 is not None:
            current_duty = self._duty12_from_u16(duty_u16)
        elif duty_ns is not None:
            current_duty = self._duty12_from_ns(duty_ns)
        self.pmic._write_pwm_raw(self.channel, current_duty, polarity, True)

    def deinit(self):
        """Disable PWM and restore its fixed pin as a floating input."""
        if not self._active:
            return
        self.pmic.disable_pwm(self.channel)
        self.pmic.set_pin_function(self.gpio, M5PM1.PIN_FUNCTION_GPIO)
        self.pmic.set_pin_mode(self.gpio, _GPIO_MODE_IN)
        self.pmic.set_pin_pull(self.gpio, _PULL_NONE)
        self._active = False

    def freq(self, value=None):
        """Read or set the shared PWM frequency.

        Args:
            value (int | None): Frequency in hertz. Unit: Hz. Range:
                ``1..65535``. Defaults to ``None`` to read.

        Returns:
            int | None: Current frequency when reading; ``None`` when setting.
        """
        self._require_active()
        if value is None:
            return self.pmic.get_pwm_frequency()
        self.pmic.set_pwm_frequency(value)

    def duty_u16(self, value=None):
        """Read or set duty using the MicroPython unsigned 16-bit scale."""
        self._require_active()
        duty12, polarity, enabled = self.pmic._read_pwm_raw(self.channel)
        if value is None:
            return (duty12 * _PWM_U16_MAX + (_PWM_DUTY_MASK // 2)) // _PWM_DUTY_MASK
        self.pmic._write_pwm_raw(
            self.channel,
            self._duty12_from_u16(value),
            polarity,
            enabled,
        )

    def duty_ns(self, value=None):
        """Read or set PWM pulse width in nanoseconds."""
        self._require_active()
        duty12, polarity, enabled = self.pmic._read_pwm_raw(self.channel)
        period_ns = self._period_ns()
        if value is None:
            return (duty12 * period_ns + (_PWM_DUTY_MASK // 2)) // _PWM_DUTY_MASK
        self.pmic._write_pwm_raw(
            self.channel,
            self._duty12_from_ns(value),
            polarity,
            enabled,
        )

    def invert(self, value=None):
        """Read or set output polarity."""
        self._require_active()
        duty12, polarity, enabled = self.pmic._read_pwm_raw(self.channel)
        if value is None:
            return polarity
        self.pmic._write_pwm_raw(
            self.channel,
            duty12,
            _bool(value, "invert"),
            enabled,
        )


class NeoPixel:
    """Buffered RGB NeoPixel object backed by M5PM1 LED RAM.

    Args:
        pmic (M5PM1): Parent M5PM1 driver instance.
        gpio (int): NeoPixel output pin. Only GPIO0 is supported.
        count (int): Active LED count. Range: ``1..32``.
        bpp (int): Bytes per pixel. Only RGB ``3`` is supported.
        timing (int): NeoPixel protocol timing selector. Accepted values are
            ``0`` and ``1``; M5PM1 uses its fixed hardware timing for both.
    """

    def __init__(self, pmic, gpio, count, *, bpp=3, timing=1):
        self.pmic = pmic
        self.gpio = pmic._check_gpio(gpio)
        if self.gpio != _NEOPIXEL_GPIO:
            raise ValueError("gpio must be 0 for NeoPixel")
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
        self._active = False
        self.init()

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

    def _color(self, color):
        if isinstance(color, int):
            if not 0 <= color <= 0xffffff:
                raise ValueError("color must be 0..0xffffff")
            return ((color >> 16) & 0xff, (color >> 8) & 0xff, color & 0xff)
        if len(color) != 3:
            raise ValueError("color must contain 3 channels")
        return tuple(self.pmic._check_byte(value, "color") for value in color)

    def init(self):
        """Initialize or reinitialize the fixed GPIO0 NeoPixel output."""
        self.pmic.set_pin_drive(_NEOPIXEL_GPIO, _DRIVE_PUSH_PULL)
        self.pmic.set_pin_function(_NEOPIXEL_GPIO, M5PM1.PIN_FUNCTION_OTHER)
        self.pmic.set_neopixel_count(self.n)
        self._active = True

    def deinit(self):
        """Clear LEDs, disable output, and restore GPIO0 as an input."""
        if not self._active:
            return
        self.pmic.clear_neopixels()
        self.pmic.disable_neopixels()
        self.pmic.set_pin_function(_NEOPIXEL_GPIO, M5PM1.PIN_FUNCTION_GPIO)
        self.pmic.set_pin_mode(_NEOPIXEL_GPIO, _GPIO_MODE_IN)
        self.pmic.set_pin_pull(_NEOPIXEL_GPIO, _PULL_NONE)
        self._active = False

    def __len__(self):
        return self.n

    def __getitem__(self, index):
        index = self._index(index)
        offset = index * self.bpp
        return tuple(self.buf[offset : offset + self.bpp])

    def __setitem__(self, index, color):
        index = self._index(index)
        offset = index * self.bpp
        self.buf[offset : offset + self.bpp] = bytes(self._color(color))

    def fill(self, color):
        """Fill the local buffer without writing the LEDs."""
        color = bytes(self._color(color))
        for offset in range(0, len(self.buf), self.bpp):
            self.buf[offset : offset + self.bpp] = color

    def write(self):
        """Convert the RGB buffer to RGB565 and refresh the LED output."""
        self._require_active()
        colors = [
            tuple(self.buf[offset : offset + self.bpp])
            for offset in range(0, len(self.buf), self.bpp)
        ]
        self.pmic.write_neopixels(colors)


class Pin(_PinBase):
    """M5PM1 GPIO object compatible with the MicroPython Pin API.

    Args:
        pmic (M5PM1): Parent M5PM1 driver instance.
        gpio (int): GPIO index. Range: ``0..4``.
        mode (int | None): ``machine.Pin.IN``, ``machine.Pin.OUT``, or
            ``machine.Pin.OPEN_DRAIN``. ``None`` keeps the current mode.
        pull (int | None): ``None`` disables pulls; ``Pin.PULL_UP`` and
            ``Pin.PULL_DOWN`` enable a pull. Defaults to ``-1`` to keep the
            current pull.
        value (int | bool | None): Optional initial output value.
    """

    IN = _machine_pin_in
    OUT = _machine_pin_out
    OPEN_DRAIN = _machine_pin_open_drain

    PULL_UP = _machine_pin_pull_up
    PULL_DOWN = _machine_pin_pull_down

    def __init__(self, pmic, gpio, mode=None, pull=_PIN_PULL_KEEP, *, value=None):
        self.pmic = pmic
        self.gpio = pmic._check_gpio(gpio)
        self._active = False
        self.init(mode, pull, value=value)

    def init(self, mode=None, pull=_PIN_PULL_KEEP, *, value=None):
        """Initialize or reconfigure the GPIO pin.

        Args:
            mode (int | None): ``machine.Pin.IN``, ``machine.Pin.OUT``, or
                ``machine.Pin.OPEN_DRAIN``. ``None`` keeps the current mode.
            pull (int | None): ``None`` disables pulls. Defaults to ``-1``
                to keep the current pull.
            value (int | bool | None): Optional output value.
        """
        if mode is not None:
            if mode == self.IN:
                gpio_mode = _GPIO_MODE_IN
            elif mode == self.OUT:
                gpio_mode = _GPIO_MODE_OUT
            elif mode == self.OPEN_DRAIN:
                gpio_mode = _GPIO_MODE_OPEN_DRAIN
            else:
                raise ValueError("mode must be Pin.IN, Pin.OUT, or Pin.OPEN_DRAIN")
            self.pmic.set_pin_function(self.gpio, M5PM1.PIN_FUNCTION_GPIO)
            self.pmic.set_pin_mode(self.gpio, gpio_mode)
        if pull != _PIN_PULL_KEEP:
            if pull is None:
                gpio_pull = _PULL_NONE
            elif pull == self.PULL_UP:
                gpio_pull = _PULL_UP
            elif pull == self.PULL_DOWN:
                gpio_pull = _PULL_DOWN
            else:
                raise ValueError("pull must be None, Pin.PULL_UP, or Pin.PULL_DOWN")
            self.pmic.set_pin_pull(self.gpio, gpio_pull)
        self._active = True
        if value is not None:
            self.value(value)

    def deinit(self):
        """Restore a floating GPIO input and deactivate this object."""
        if not self._active:
            return
        self.pmic.set_pin_function(self.gpio, M5PM1.PIN_FUNCTION_GPIO)
        self.pmic.set_pin_mode(self.gpio, _GPIO_MODE_IN)
        self.pmic.set_pin_pull(self.gpio, _PULL_NONE)
        self._active = False

    def value(self, value=None):
        """Read or write the GPIO value.

        Args:
            value (int | bool | None): Output value. Defaults to ``None`` to
                read the current input value.

        Returns:
            int | None: ``0`` or ``1`` when reading; ``None`` when writing.
        """
        if not self._active:
            raise RuntimeError("Pin is deinitialized")
        if value is None:
            return self.pmic.read_pin(self.gpio)
        self.pmic.set_pin_value(self.gpio, value)

    def on(self):
        """Set the GPIO output high."""
        self.value(1)

    def off(self):
        """Set the GPIO output low."""
        self.value(0)

    def __call__(self, value=None):
        """Call alias for :meth:`value`."""
        return self.value(value)

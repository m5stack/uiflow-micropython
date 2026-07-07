# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import time

import esp32
import m5utils
from driver.m5ioe1 import M5ioe1, Pin, RGB
from driver.si12t import Si12T, OUTPUT_NONE
from driver.scs_servo import Scscl
from driver.ina226 import INA226
from unit.nfc import NFCUnit


# RGB LED
RGB_IO_PIN = 14
RGB_LED_COUNT = 12
RGB_STRIP_LED_COUNT = 6
RGB_STRIP0_PHYS_START = 0
RGB_STRIP1_PHYS_START = 6

# Servo
SERVO_POWER_PIN = 1
SERVO_ID_X = 1
SERVO_ID_Y = 2
SERVO_MODE_POS = 0
SERVO_MODE_PWM = 1
SERVO_PWM_USER_MAX = 100
SERVO_PWM_HW_MAX = 1023
X_AXIS_ZERO_POS = 450
Y_AXIS_ZERO_POS = 125
MOVE_TIME_MS = 10
SERVO_POWER_ON_DELAY_MS = 1000
SERVO_POWER_OFF_DELAY_MS = 200
SERVO_SPEED_USER_MAX = 100
SERVO_SPEED_HW_MAX = 1500

# NVS key
_SERVO_NVS_NS = "servo"
_SERVO_NVS_ZERO_KEY = {SERVO_ID_X: "zero_pos_1", SERVO_ID_Y: "zero_pos_2"}
_SERVO_RAW_MIN = 0
_SERVO_RAW_MAX = 1000


def angle_to_pos(angle_deg, zero_pos):
    """Convert angle to servo position value

    :param angle_deg: angle value (degrees)
    :type angle_deg: int or float
    :param zero_pos: zero position
    :type zero_pos: int
    :return: servo position value (0-1000)
    :rtype: int
    """
    angle_01deg = int(angle_deg * 10)
    mapped_pos = zero_pos + angle_01deg * 16 // 5 // 10
    mapped_pos = max(0, min(1000, mapped_pos))
    return mapped_pos


def pos_to_angle(pos, zero_pos):
    """Convert servo position value to angle

    :param pos: servo position value (0-1000)
    :type pos: int
    :param zero_pos: zero position
    :type zero_pos: int
    :return: angle value (degrees)
    :rtype: float
    """
    angle_01deg = (pos - zero_pos) * 5 * 10 // 16
    angle_deg = angle_01deg / 10.0
    return angle_deg


class StackChan:
    SERVO_ID_X = 1
    SERVO_ID_Y = 2
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StackChan, cls).__new__(cls)
        return cls._instance

    def __init__(self, i2c=1, uart=1):
        if StackChan._initialized:
            if i2c != self._i2c_num or uart != self._uart_num:
                raise ValueError(
                    "StackChan already initialized with i2c=%s uart=%s"
                    % (self._i2c_num, self._uart_num)
                )
            self.rgb.clear()
            # Re-running examples re-enters here; leave servos in a deterministic off state.
            self.set_servo_power(False)
            return

        self._i2c_num = int(i2c)
        self._uart_num = int(uart)
        self.servo_power_enabled = False
        self.servo_torque_enabled = {SERVO_ID_X: False, SERVO_ID_Y: False}
        self._servo_x_mode = None
        # I2C
        self.i2c = machine.I2C(
            self._i2c_num, scl=machine.Pin(11), sda=machine.Pin(12), freq=100000
        )
        time.sleep_ms(100)
        # print(f"I2C devices found: {[hex(d) for d in self.i2c.scan()]}")
        self.ioe1 = M5ioe1(self.i2c, 0x6F)
        time.sleep_ms(100)
        # rgb led
        self.rgb = RGB(self.ioe1, io=RGB_IO_PIN, n=RGB_LED_COUNT)
        self.rgb.clear(refresh=True)
        # touch
        self.touch = Si12T(self.i2c)
        # servo
        self.servo_power_pin = Pin(self.ioe1, SERVO_POWER_PIN, Pin.OUT)
        self.set_servo_power(False)
        self.uart = machine.UART(self._uart_num, baudrate=1000000, tx=6, rx=7)
        self.servo = Scscl(self.uart, end=1, level=1)
        self._servo_nvs = esp32.NVS(_SERVO_NVS_NS)
        self._servo_zero_runtime = {
            SERVO_ID_X: self._load_servo_zero_from_nvs(SERVO_ID_X),
            SERVO_ID_Y: self._load_servo_zero_from_nvs(SERVO_ID_Y),
        }
        # power monitor
        self.power_monitor = INA226(self.i2c, 0x41, shunt_resistor=0.08)
        self.power_monitor.configure(
            avg=INA226.CFG_AVGMODE_16SAMPLES,
            vbus_conv_time=INA226.CFG_VBUSCT_8244us,
            vshunt_conv_time=INA226.CFG_VSHUNTCT_8244us,
            mode=INA226.CFG_MODE_SANDBVOLT_CONTINUOUS,
        )
        self.power_monitor.calibrate(cal_value=0x0800)
        # NFC
        self.nfc = NFCUnit(self.i2c)

        StackChan._initialized = True

    """
    ========================================================================
     RGB LED control
    ========================================================================
    """

    def set_rgb_color(self, *args):
        n = len(args)
        if n == 1:
            (color,) = args
            return self.rgb.fill_color(color, refresh=True)
        if n == 2:
            strip, color = args
            if strip == 0:
                start, end = RGB_STRIP0_PHYS_START, RGB_STRIP0_PHYS_START + RGB_STRIP_LED_COUNT
            elif strip == 1:
                start, end = RGB_STRIP1_PHYS_START, RGB_STRIP1_PHYS_START + RGB_STRIP_LED_COUNT
            else:
                raise ValueError("strip must be 0 or 1")
            for i in range(start, end):
                if not self.rgb.set_color(i, color, refresh=False):
                    return False
            return self.rgb.refresh()
        if n == 3:
            strip, index, color = args
            if index < 0 or index >= RGB_STRIP_LED_COUNT:
                raise ValueError("index must be 0..%u for each strip" % (RGB_STRIP_LED_COUNT - 1))
            if strip == 0:
                phys = RGB_STRIP0_PHYS_START + index
            elif strip == 1:
                phys = RGB_STRIP1_PHYS_START + (RGB_STRIP_LED_COUNT - 1 - index)
            else:
                raise ValueError("strip must be 0 or 1")
            return self.rgb.set_color(phys, color, refresh=True)

    def get_rgb_color(self, strip, index):
        if index < 0 or index >= RGB_STRIP_LED_COUNT:
            raise ValueError("index must be 0..%u for each strip" % (RGB_STRIP_LED_COUNT - 1))
        if strip == 0:
            phys = RGB_STRIP0_PHYS_START + index
        elif strip == 1:
            phys = RGB_STRIP1_PHYS_START + (RGB_STRIP_LED_COUNT - 1 - index)
        else:
            raise ValueError("strip must be 0 or 1")
        r, g, b = self.rgb._colors[phys]
        return (r, g, b)

    """
    ========================================================================
     Servo control
    ========================================================================
    """

    def _default_zero_for(self, servo_id):
        return X_AXIS_ZERO_POS if servo_id == SERVO_ID_X else Y_AXIS_ZERO_POS

    def _load_servo_zero_from_nvs(self, servo_id):
        default = self._default_zero_for(servo_id)
        key = _SERVO_NVS_ZERO_KEY[servo_id]
        axis = "X" if servo_id == SERVO_ID_X else "Y"
        try:
            v = self._servo_nvs.get_i32(key)
            if _SERVO_RAW_MIN <= v <= _SERVO_RAW_MAX:
                return v
            print(
                "[StackChan] invalid NVS zero %s %s=%d, use default %d" % (axis, key, v, default)
            )
        except OSError as e:
            print("[StackChan] no NVS zero %s (%s), use default %d — %s" % (axis, key, default, e))
        return default

    def _save_servo_zero(self, servo_id):
        if servo_id not in (SERVO_ID_X, SERVO_ID_Y):
            return False
        pos = self.servo.read_pos(servo_id)
        if pos < 0 or not (_SERVO_RAW_MIN <= pos <= _SERVO_RAW_MAX):
            return False
        self._servo_nvs.set_i32(_SERVO_NVS_ZERO_KEY[servo_id], pos)
        self._servo_nvs.commit()
        self._servo_zero_runtime[servo_id] = pos
        return True

    def _reset_servo_zero(self, servo_id):
        if servo_id not in (SERVO_ID_X, SERVO_ID_Y):
            return False
        d = self._default_zero_for(servo_id)
        self._servo_nvs.set_i32(_SERVO_NVS_ZERO_KEY[servo_id], d)
        self._servo_nvs.commit()
        self._servo_zero_runtime[servo_id] = d
        return True

    def set_servo_zero(self, reset=False):
        """Set logical zero in NVS (``zero_pos_1`` / ``zero_pos_2``).

        :param reset: If False (default), use **current** pose as X+Y zero. If True, restore **code** defaults (``X_AXIS_ZERO_POS`` / ``Y_AXIS_ZERO_POS``) to NVS.
        :return: ``True`` if both axes succeeded.
        """
        if reset:
            return self._reset_servo_zero(SERVO_ID_X) and self._reset_servo_zero(SERVO_ID_Y)
        return self._save_servo_zero(SERVO_ID_X) and self._save_servo_zero(SERVO_ID_Y)

    def set_servo_power(self, enable=True, settle_ms=None):
        if enable:
            self.servo_power_pin.on()
            if settle_ms is None:
                settle_ms = SERVO_POWER_ON_DELAY_MS
            time.sleep_ms(max(0, int(settle_ms)))
            if hasattr(self, "uart"):
                while self.uart.any() > 0:
                    self.uart.read(self.uart.any())
        else:
            self.servo_power_pin.off()
            if settle_ms is None:
                settle_ms = SERVO_POWER_OFF_DELAY_MS
            time.sleep_ms(max(0, int(settle_ms)))
            self._servo_x_mode = None
            self.servo_torque_enabled[SERVO_ID_X] = False
            self.servo_torque_enabled[SERVO_ID_Y] = False
        self.servo_power_enabled = enable

    def _servo_retry(self, func, args=(), ok=(1, True), attempts=5, delay_ms=50):
        result = None
        for _ in range(attempts):
            result = func(*args)
            if result in ok:
                return result
            time.sleep_ms(delay_ms)
        return result

    def set_servo_torque(self, servo_id, enable=True):
        result = self._servo_retry(self.servo.enable_torque, (servo_id, 1 if enable else 0))
        if result == 1:
            self.servo_torque_enabled[servo_id] = enable
            return True
        print("[StackChan] servo %s torque(%s) failed: %s" % (servo_id, enable, result))
        return False

    def ensure_servo_x_mode(self, mode):
        if self._servo_x_mode == mode:
            return True
        if self._servo_x_mode is None:
            current = self.servo.read_mode(SERVO_ID_X)
            if current == mode:
                self._servo_x_mode = mode
                return True
            if current == SERVO_MODE_POS:
                self.servo.min_angle[SERVO_ID_X] = _SERVO_RAW_MIN
                self.servo.max_angle[SERVO_ID_X] = _SERVO_RAW_MAX
        result = self._servo_retry(
            self.servo.switch_mode, (SERVO_ID_X, mode), ok=(0,), attempts=5, delay_ms=80
        )
        if result == 0:
            self._servo_x_mode = mode
            return True
        print("[StackChan] servo X switch_mode(%s) failed: %s" % (mode, result))
        return False

    def set_servo_x_pwm(self, pwm_out):
        if not self.ensure_servo_x_mode(SERVO_MODE_PWM):
            return False
        p = max(-100, min(100, int(pwm_out)))
        ap = abs(p)
        mag = int(
            round(
                m5utils.remap(
                    float(ap),
                    0.0,
                    float(100),
                    0.0,
                    float(SERVO_PWM_HW_MAX),
                )
            )
        )
        hw = -mag if p < 0 else mag
        hw = max(-SERVO_PWM_HW_MAX, min(SERVO_PWM_HW_MAX, hw))
        return self._servo_retry(self.servo.write_pwm, (SERVO_ID_X, hw)) == 1

    def set_servo_angle(self, servo_id, angle_deg, time_ms=MOVE_TIME_MS, speed=0):
        if servo_id == SERVO_ID_X:
            if not self.ensure_servo_x_mode(SERVO_MODE_POS):
                return False
        elif servo_id != SERVO_ID_Y:
            raise ValueError("servo_id must be SERVO_ID_X or SERVO_ID_Y")
        zero = self._servo_zero_runtime[servo_id]
        pos = angle_to_pos(angle_deg, zero)
        s = max(0, min(SERVO_SPEED_USER_MAX, int(speed)))
        hw_speed = int(
            round(
                m5utils.remap(
                    float(s),
                    0.0,
                    100.0,
                    0.0,
                    float(SERVO_SPEED_HW_MAX),
                )
            )
        )
        hw_speed = max(0, min(SERVO_SPEED_HW_MAX, hw_speed))
        return self._servo_retry(self.servo.write_pos, (servo_id, pos, time_ms, hw_speed)) == 1

    def get_servo_angle(self, servo_id):
        if servo_id not in (SERVO_ID_X, SERVO_ID_Y):
            return None
        zero = self._servo_zero_runtime[servo_id]
        pos = self.servo.read_pos(servo_id)
        if pos is None or pos < 0:
            return None
        return pos_to_angle(pos, zero)

    def get_servo_voltage(self, servo_id):
        v = self.servo.read_voltage(servo_id)
        if v < 0:
            return None
        return v

    def get_servo_current(self, servo_id):
        c = self.servo.read_current(servo_id)
        if c == -1:
            return None
        return c

    """
    ========================================================================
     Touch sensor
    ========================================================================
    """

    def get_touch(self, index=None):
        tp = self.touch.get_touch_status()
        if tp is None:
            tp = [OUTPUT_NONE, OUTPUT_NONE, OUTPUT_NONE]
        if index is None:
            return [tp[2], tp[1], tp[0]]
        i = int(index)
        if i < 0 or i > 2:
            return OUTPUT_NONE
        return tp[2 - i]

    """
    ========================================================================
     Power monitor
    ========================================================================
    """

    def get_battery_voltage(self):
        """get battery voltage, unit: volts"""
        return self.power_monitor.read_bus_voltage()

    def get_battery_current(self):
        """get battery current, unit: amps"""
        return self.power_monitor.read_current()

    def get_battery_power(self):
        """get battery power, unit: watts"""
        return self.power_monitor.read_power()

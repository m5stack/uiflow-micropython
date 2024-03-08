# MIT License (MIT)
# Copyright (c) 2022 Mike Teachman
# https://opensource.org/licenses/MIT

# Platform-independent MicroPython code for the rotary encoder module

# Documentation:
#   https://github.com/MikeTeachman/micropython-rotary

import micropython
from micropython import const

_DIR_CW = const(0x10)  # Clockwise step
_DIR_CCW = const(0x20)  # Counter-clockwise step

# Rotary Encoder States
_R_START = const(0x0)
_R_CW_1 = const(0x1)
_R_CW_2 = const(0x2)
_R_CW_3 = const(0x3)
_R_CCW_1 = const(0x4)
_R_CCW_2 = const(0x5)
_R_CCW_3 = const(0x6)
_R_ILLEGAL = const(0x7)

_transition_table = [
    # |------------- NEXT STATE -------------|            |CURRENT STATE|
    # CLK/DT    CLK/DT     CLK/DT    CLK/DT
    #   00        01         10        11
    [_R_START, _R_CCW_1, _R_CW_1, _R_START],  # _R_START
    [_R_CW_2, _R_START, _R_CW_1, _R_START],  # _R_CW_1
    [_R_CW_2, _R_CW_3, _R_CW_1, _R_START],  # _R_CW_2
    [_R_CW_2, _R_CW_3, _R_START, _R_START | _DIR_CW],  # _R_CW_3
    [_R_CCW_2, _R_CCW_1, _R_START, _R_START],  # _R_CCW_1
    [_R_CCW_2, _R_CCW_1, _R_CCW_3, _R_START],  # _R_CCW_2
    [_R_CCW_2, _R_START, _R_CCW_3, _R_START | _DIR_CCW],  # _R_CCW_3
    [_R_START, _R_START, _R_START, _R_START],
]  # _R_ILLEGAL

_transition_table_half_step = [
    [_R_CW_3, _R_CW_2, _R_CW_1, _R_START],
    [_R_CW_3 | _DIR_CCW, _R_START, _R_CW_1, _R_START],
    [_R_CW_3 | _DIR_CW, _R_CW_2, _R_START, _R_START],
    [_R_CW_3, _R_CCW_2, _R_CCW_1, _R_START],
    [_R_CW_3, _R_CW_2, _R_CCW_1, _R_START | _DIR_CW],
    [_R_CW_3, _R_CCW_2, _R_CW_3, _R_START | _DIR_CCW],
    [_R_START, _R_START, _R_START, _R_START],
    [_R_START, _R_START, _R_START, _R_START],
]

_STATE_MASK = const(0x07)
_DIR_MASK = const(0x30)


def _wrap(value, incr, lower_bound, upper_bound):
    range = upper_bound - lower_bound + 1
    value = value + incr

    if value < lower_bound:
        value += range * ((lower_bound - value) // range + 1)

    return lower_bound + (value - lower_bound) % range


def _bound(value, incr, lower_bound, upper_bound):
    return min(upper_bound, max(lower_bound, value + incr))


def _trigger(rotary_instance):
    for listener in rotary_instance._listener:
        listener()


class Rotary(object):
    RANGE_UNBOUNDED = const(1)
    RANGE_WRAP = const(2)
    RANGE_BOUNDED = const(3)

    def __init__(self, min_val, max_val, incr, reverse, range_mode, half_step, invert):
        self._min_val = min_val
        self._max_val = max_val
        self._incr = incr
        self._reverse = -1 if reverse else 1
        self._range_mode = range_mode
        self._value = min_val
        self._state = _R_START
        self._half_step = half_step
        self._invert = invert
        self._listener = []

    def set(
        self, value=None, min_val=None, incr=None, max_val=None, reverse=None, range_mode=None
    ):
        # disable DT and CLK pin interrupts
        self._hal_disable_irq()

        if value is not None:
            self._value = value
        if min_val is not None:
            self._min_val = min_val
        if max_val is not None:
            self._max_val = max_val
        if incr is not None:
            self._incr = incr
        if reverse is not None:
            self._reverse = -1 if reverse else 1
        if range_mode is not None:
            self._range_mode = range_mode
        self._state = _R_START

        # enable DT and CLK pin interrupts
        self._hal_enable_irq()

    def value(self):
        return self._value

    def reset(self):
        self._value = 0

    def close(self):
        self._hal_close()

    def add_listener(self, l):
        self._listener.append(l)

    def remove_listener(self, l):
        if l not in self._listener:
            raise ValueError("{} is not an installed listener".format(l))
        self._listener.remove(l)

    def _process_rotary_pins(self, pin):
        old_value = self._value
        clk_dt_pins = (self._hal_get_clk_value() << 1) | self._hal_get_dt_value()

        if self._invert:
            clk_dt_pins = ~clk_dt_pins & 0x03

        # Determine next state
        if self._half_step:
            self._state = _transition_table_half_step[self._state & _STATE_MASK][clk_dt_pins]
        else:
            self._state = _transition_table[self._state & _STATE_MASK][clk_dt_pins]
        direction = self._state & _DIR_MASK

        incr = 0
        if direction == _DIR_CW:
            incr = self._incr
        elif direction == _DIR_CCW:
            incr = -self._incr

        incr *= self._reverse

        if self._range_mode == self.RANGE_WRAP:
            self._value = _wrap(self._value, incr, self._min_val, self._max_val)
        elif self._range_mode == self.RANGE_BOUNDED:
            self._value = _bound(self._value, incr, self._min_val, self._max_val)
        else:
            self._value = self._value + incr

        try:
            if old_value != self._value and len(self._listener) != 0:
                _trigger(self)
        except:
            pass

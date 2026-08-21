# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from hardware import Button
from machine import Pin


def DualButtonUnit(port):  # noqa: N802
    return Button(port[0]), Button(port[1])


class SimpleButton:
    def __init__(self, pin_num, active_low=True):
        self._pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self._active_low = active_low
        self._prev_active = False
        self._was_pressed = False
        self._was_released = False

    def value(self):
        """Raw pin value: 0 or 1."""
        return self._pin.value()

    def is_active(self):
        """True when button is physically pressed (accounts for active_low)."""
        if self._active_low:
            return self._pin.value() == 0
        return self._pin.value() == 1

    def update(self):
        """Call once per loop iteration to enable edge detection."""
        active = self.is_active()
        self._was_pressed = active and not self._prev_active
        self._was_released = not active and self._prev_active
        self._prev_active = active

    def was_pressed(self):
        """True once on the loop tick when button transitions from released to pressed."""
        return self._was_pressed

    def was_released(self):
        """True once on the loop tick when button transitions from pressed to released."""
        return self._was_released


def SimpleDualButtonUnit(port, active_low=True):  # noqa: N802
    return SimpleButton(port[0], active_low), SimpleButton(port[1], active_low)

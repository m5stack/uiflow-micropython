# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import time

from hardware import Button
from machine import Pin


def DualButtonUnit(port):  # noqa: N802
    return Button(port[0]), Button(port[1])


class SimpleButton:
    def __init__(self, pin_num, active_low=True, debounce_ms=50):
        if debounce_ms < 0:
            raise ValueError("debounce_ms must be greater than or equal to 0")

        pull = Pin.PULL_UP if active_low else Pin.PULL_DOWN
        self._pin = Pin(pin_num, Pin.IN, pull)
        self._active_low = active_low
        self._debounce_ms = debounce_ms
        active = self._read_active()
        self._raw_active = active
        self._stable_active = active
        self._changed_at = time.ticks_ms()
        self._was_pressed = False
        self._was_released = False

    def value(self):
        """Raw pin value: 0 or 1."""
        return self._pin.value()

    def is_active(self):
        """True when button is physically pressed (accounts for active_low)."""
        return self._read_active()

    def _read_active(self):
        return self._pin.value() == (0 if self._active_low else 1)

    def update(self):
        """Update debounced press and release edge states."""
        now = time.ticks_ms()
        active = self._read_active()
        self._was_pressed = False
        self._was_released = False

        if active != self._raw_active:
            self._raw_active = active
            self._changed_at = now

        if active == self._stable_active:
            return
        if time.ticks_diff(now, self._changed_at) < self._debounce_ms:
            return

        self._stable_active = active
        self._was_pressed = active
        self._was_released = not active

    def was_pressed(self):
        """True once on the loop tick when button transitions from released to pressed."""
        return self._was_pressed

    def was_released(self):
        """True once on the loop tick when button transitions from pressed to released."""
        return self._was_released


def SimpleDualButtonUnit(port, active_low=True, debounce_ms=50):  # noqa: N802
    return (
        SimpleButton(port[0], active_low, debounce_ms),
        SimpleButton(port[1], active_low, debounce_ms),
    )

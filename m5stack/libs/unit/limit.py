# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import Pin
from hardware import Button

SWITCH = 1
COUNTER = 2


class LIMITUnit(Button):
    """
    note:
        en: LIMIT Unit is a device used to track limit switches or counting signals. It extends the functionality of the Button class and supports both switch and counter modes.

    details:
        link: https://docs.m5stack.com/en/unit/Unit%20Limit
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/Unit%20Limit/img-7da470fe-12b4-4694-bcd7-62077c1cce2e.webp
        category: Unit

    example:
        - ../../../examples/unit/limit/limit_example.py

    m5f2:
        - unit/limit/limit_example.m5f2
    """

    def __init__(self, port, active_low=True, type=SWITCH):
        """
        note:
            en: Initialize a LIMITUnit instance with the given port, active-low configuration, and operational type.

        params:
            port:
                note: The port used for the limit unit, typically the GPIO pin connected to the device.
            active_low:
                note: Determines whether the signal is active-low. Default is True.
            type:
                note: The operation mode of the unit: SWITCH or COUNTER. Default is SWITCH.
        """
        self.count_value = 0
        self.curr_status = 0
        self.prev_status = 0 if active_low else 1
        self.pin = Pin(port[0], Pin.IN, Pin.PULL_UP)
        super().__init__(port[0], active_low=active_low)
        if type != SWITCH:
            self.pin.irq(handler=self._cb_irq, trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING))

    def _cb_irq(self, arg):
        """
        note:
            en: Interrupt handler for the pin. It updates the counter when the pin's value changes.

        params:
            note:
        """
        self.curr_status = self.pin.value()
        if self.curr_status != self.prev_status:
            self.count_value += 1
        self.prev_status = self.curr_status

    def count_reset(self):
        """
        note:
            en: Reset the count value to zero.

        params:
            note:
        """
        self.count_value = 0

from machine import Pin
from hardware import Button

SWITCH = 1
COUNTER = 2


class LIMITUnit(Button):
    def __init__(self, port, active_low=True, type=SWITCH):
        self.count_value = 0
        self.curr_status = 0
        self.prev_status = 0 if active_low else 1
        self.pin = Pin(port[0], Pin.IN, Pin.PULL_UP)
        super().__init__(port[0], active_low=active_low)
        if type != SWITCH:
            self.pin.irq(handler=self._cb_irq, trigger=(Pin.IRQ_FALLING | Pin.IRQ_RISING))

    def _cb_irq(self, arg):
        self.curr_status = self.pin.value()
        if self.curr_status != self.prev_status:
            self.count_value += 1
        self.prev_status = self.curr_status

    def count_reset(self):
        self.count_value = 0

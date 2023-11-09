from machine import Pin

SWITCH = 1
COUNTER = 2


class OPUnit:
    def __init__(self, port, type=SWITCH):
        self.count_value = 0
        self.pin = Pin(port[0], Pin.IN, Pin.PULL_UP)
        if type != SWITCH:
            self.pin.irq(handler=self._cb_irq, trigger=Pin.IRQ_RISING)

    @property
    def get_value(self):
        return self.pin.value()

    def _cb_irq(self, arg):
        self.count_value += 1

    def count_reset(self):
        self.count_value = 0

from pca9685 import Servos
import i2c_bus
import module


class Servo2Module(Servos):
    def __init__(self, address=0x40, min_us=400, max_us=2350, degrees=180):
        self._addr = address
        self.min_us = min_us
        self.max_us = max_us
        self.degrees = degrees
        self.i2c = i2c_bus.get(i2c_bus.PORTA)
        self._available()
        super(Servo2Module, self).__init__(
            self.i2c,
            address=self._addr,
            min_us=self.min_us,
            max_us=self.max_us,
            degrees=self.degrees,
        )

    def _available(self):
        if self.i2c.is_ready(self._addr) or self.i2c.is_ready(self._addr):
            pass
        else:
            raise module.Module("module Servo2 maybe not connect")

    def deinit(self):
        pass


"""
if __name__ == "__main__":

    servo = Servo2()
"""

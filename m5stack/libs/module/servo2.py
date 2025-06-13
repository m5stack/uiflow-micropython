from driver.pca9685 import Servos
from . import mbus


class Servo2Module(Servos):
    def __init__(self, address=0x40, freq=50, min_us=400, max_us=2350, degrees=180):
        self._addr = address
        self.min_us = min_us
        self.max_us = max_us
        self.degrees = degrees
        self.i2c = mbus.i2c1
        if self._addr not in self.i2c.scan():
            raise Exception("Servo2 Module not found at I2C address 0x%02X" % self._addr)

        super(Servo2Module, self).__init__(
            self.i2c,
            freq=freq,
            address=self._addr,
            min_us=self.min_us,
            max_us=self.max_us,
            degrees=self.degrees,
        )

    def deinit(self):
        pass


"""
if __name__ == "__main__":

    servo = Servo2()
"""

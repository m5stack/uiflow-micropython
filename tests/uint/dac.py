# Simple demo of setting the DAC value up and down through its entire range
# of values.
import time
from machine import I2C, Pin
from unit.dac import DAC

# Initialize I2C bus.
i2c = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)

# Initialize MCP4725.
dac = DAC(i2c)

# There are a three ways to set the DAC output, you can use any of these:
dac.set_value(65535)  # Use the value property with a 16-bit number just like

dac.set_raw_value(4095)  # Use the raw_value property to directly read and write
# the 12-bit DAC value.  The range of values is
# 0 (minimum/ground) to 4095 (maximum/Vout).

dac.set_normalized_value(1.0)  # Use the normalized_value property to set the
# output with a floating point value in the range
# 0 to 1.0 where 0 is minimum/ground and 1.0 is
# maximum/Vout.


class Voltage:
    def __init__(self, start, stop, step):
        self._start = start
        self._stop = stop
        self._self = step

    def __iter__(self):
        self._vol = self._start
        return self

    def __next__(self):
        if self._start > self._stop:
            if self._vol > self._stop:
                x = self._vol
                self._vol += self._self
                return x
            else:
                raise StopIteration
        else:
            if self._vol < self._stop:
                x = self._vol
                self._vol += self._self
                return x
            else:
                raise StopIteration


# Main loop will go up and down through the range of DAC values forever.
while True:
    # Go up the 12-bit raw range.
    print("Going up 0-3.3V...")
    voltage = Voltage(0, 4095, 1)
    myiter = iter(voltage)
    for x in myiter:
        dac.set_raw_value(x)
        time.sleep(0.01)

    # Go back down the 12-bit raw range.
    print("Going down 3.3-0V...")
    voltage = Voltage(3.3, 0.0, -0.1)
    myiter = iter(voltage)
    for x in myiter:
        dac.set_voltage(x)
        time.sleep(0.5)

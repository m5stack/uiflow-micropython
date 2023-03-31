from machine import I2C, Pin
from extio2 import EXTIO2
import unittest
import time

class TestEXTIO2(unittest.TestCase):

    def __init__(self):
        i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
        self._extio2_0 = EXTIO2(i2c0)

    def test_fw_version(self):
        result = self._extio2_0.read_fw_version()
        self.assertEqual(result, 1)

    def test_digit_io_low(self):
        self._extio2_0.set_config_mode(0, self._extio2_0.OUT)
        self._extio2_0.set_config_mode(1, self._extio2_0.IN)
        self._extio2_0.write_output_pin(0, 0)
        result = self._extio2_0.read_input_pin(1)
        self.assertEqual(result, 0)

    def test_digit_io_high(self):
        self._extio2_0.set_config_mode(0, self._extio2_0.OUT)
        self._extio2_0.set_config_mode(1, self._extio2_0.IN)
        self._extio2_0.write_output_pin(0, 1)
        result = self._extio2_0.read_input_pin(1)
        self.assertEqual(result, 1)

    def test_analog_input_8b(self):
        self._extio2_0.set_config_mode(0, self._extio2_0.OUT)
        self._extio2_0.write_output_pin(0, 1)
        self._extio2_0.set_config_mode(1, self._extio2_0.ANALOG)
        result = self._extio2_0.read_adc8_pin(1)
        self.assertTrue(result > 250)

    def test_analog_input_12b(self):
        self._extio2_0.set_config_mode(0, self._extio2_0.OUT)
        self._extio2_0.write_output_pin(0, 1)
        self._extio2_0.set_config_mode(1, self._extio2_0.ANALOG)
        result = self._extio2_0.read_adc12_pin(1)
        self.assertTrue(result > 4000)

    def test_servo_angle_ctl(self):
        self._extio2_0.set_config_mode(3, self._extio2_0.SERVO)
        self._extio2_0.write_servo_angle(3, 90)
        result = self._extio2_0.read_servo_angle(3)
        self.assertEqual(result, 90)

    def test_servo_pluse(self):
        self._extio2_0.set_config_mode(4, self._extio2_0.SERVO)
        self._extio2_0.write_servo_pluse(4, 2000)
        result = self._extio2_0.read_servo_pulse(4)
        self.assertEqual(result, 2000)

    def test_rgb_led(self):
        self._extio2_0.set_config_mode(5, self._extio2_0.NEOPIXEL)
        self._extio2_0.write_rgb_led(5, 0xFF0000)
        result = self._extio2_0.read_rgb_led(5)
        self.assertEqual(result, 0xFF0000)

    def test_set_address(self):
        self._extio2_0.set_address(0x12)
        time.sleep(1)
        result = self._extio2_0.get_address()
        time.sleep(1)
        self._extio2_0.set_address(0x45)
        self.assertEqual(result, 0x12)

if __name__ == '__main__':
    unittest.main()


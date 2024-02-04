from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct
from time import sleep_ms
import sys

if sys.platform != "esp32":
    from typing import Union

SERVOS_8_ADDR = 0x25

DIGITAL_IN_MODE = 0x00
DIGITAL_OUT_MODE = 0x01
ADC_IN_MODE = 0x02
SERVO_CTRL_MODE = 0x03
RGB_LED_MODE = 0x04
PWM_DUTY_MODE = 0x05

MODE_REG = 0x00
DIGITAL_OUT_REG = 0x10
DIGITAL_IN_REG = 0x20
ADC_8IN_REG = 0x30
ADC_12IN_REG = 0x40
SERVO_ANGLE_REG = 0x50
SERVO_PULSE_REG = 0x60
RGB_LED_REG = 0x70
PWM_DUTY_REG = 0x90
SERVO_CURRENT_REG = 0xA0
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class SERVOS8Unit:
    def __init__(self, i2c: Union[I2C, PAHUBUnit], addr=SERVOS_8_ADDR):
        """
        slave_addr : 1 to 127
        """
        self.servos8_i2c = i2c
        self.i2c_addr = addr
        if addr >= 1 and addr <= 127:
            self.i2c_addr = addr
        self.available()

    def available(self):
        if not (self.i2c_addr in self.servos8_i2c.scan()):
            raise UnitError("8 Servos unit maybe not connect")

    def get_mode(self, channel):
        """
        get mode.
        channel: 0 to 7
        """
        if channel >= 0 and channel <= 7:
            return self.servos8_i2c.readfrom_mem(self.i2c_addr, MODE_REG + channel, 1)[0]

    def set_mode(self, mode, channel):
        """
        set mode.
        channel: 0 to 7
        mode:   DIGITAL_INPUT_MODE=0
                DIGITAL_OUTPUT_MODE=1
                ADC_INPUT_MODE=2
                SERVO_CTL_MODE=3
                RGB_LED_MODE=4
                PWM_DUTY_MODE=5
        """
        if channel >= 0 and channel <= 7:
            self.servos8_i2c.writeto_mem(self.i2c_addr, MODE_REG + channel, bytearray([mode]))

    def get_digital_input(self, channel):
        """
        get digital input.
        channel: 0 to 7
        """
        if channel >= 0 and channel <= 7:
            if DIGITAL_IN_MODE == self.get_mode(channel):
                return bool(
                    self.servos8_i2c.readfrom_mem(self.i2c_addr, (DIGITAL_IN_REG + channel), 1)[0]
                )

    def set_output_value(self, value, channel):
        """
        set digital output.
        channel: 0 to 7
        value : 0 or 1
        """
        if channel >= 0 and channel <= 7:
            if DIGITAL_OUT_MODE == self.get_mode(channel):
                self.servos8_i2c.writeto_mem(
                    self.i2c_addr, (DIGITAL_OUT_REG + channel), bytearray([value])
                )

    def get_8bit_adc_raw(self, channel):
        """
        get adc 8 bit.
        channel: 0 to 7
        return : 0 to 255
        """
        if channel >= 0 and channel <= 7:
            if ADC_IN_MODE == self.get_mode(channel):
                return self.servos8_i2c.readfrom_mem(self.i2c_addr, (ADC_8IN_REG + channel), 1)[0]

    def get_12bit_adc_raw(self, channel):
        """
        get adc 12 bit.
        channel: 0 to 7
        return : 0 to 4095
        """
        if channel >= 0 and channel <= 7:
            if ADC_IN_MODE == self.get_mode(channel):
                buf = self.servos8_i2c.readfrom_mem(
                    self.i2c_addr, (ADC_12IN_REG + (channel * 2)), 2
                )
                return struct.unpack("<h", buf)[0]

    def set_servo_angle(self, angle, channel):
        """
        set servo angle.
        angle : 0 to 180
        channel: 0 to 7
        """
        if channel >= 0 and channel <= 7:
            if SERVO_CTRL_MODE == self.get_mode(channel):
                self.servos8_i2c.writeto_mem(
                    self.i2c_addr, (SERVO_ANGLE_REG + channel), bytearray([angle])
                )

    def get_servo_angle(self, channel):
        """
        get servo angle.
        channel: 0 to 7
        return : 0 to 180
        """
        if channel >= 0 and channel <= 7:
            if SERVO_CTRL_MODE == self.get_mode(channel):
                return self.servos8_i2c.readfrom_mem(
                    self.i2c_addr, (SERVO_ANGLE_REG + channel), 1
                )[0]

    def set_servo_pulse(self, pulse, channel):
        """
        set servo pulse.
        pulse : 500 to 2500
        channel: 0 to 7
        """
        if channel >= 0 and channel <= 7:
            if SERVO_CTRL_MODE == self.get_mode(channel):
                pulse = struct.pack("<h", pulse)
                self.servos8_i2c.writeto_mem(
                    self.i2c_addr, (SERVO_PULSE_REG + (channel * 2)), pulse
                )

    def get_servo_pulse(self, channel):
        """
        get servo pulse.
        channel: 0 to 7
        return : 500 to 2500
        """
        if channel >= 0 and channel <= 7:
            if SERVO_CTRL_MODE == self.get_mode(channel):
                buf = self.servos8_i2c.readfrom_mem(
                    self.i2c_addr, (SERVO_PULSE_REG + (channel * 2)), 2
                )
                return struct.unpack("<h", buf)[0] // 10

    def set_rgb_led(self, rgb, channel):
        """
        set rgb led.
        rgb: 0x000000 to 0xffffff
        channel: 0 to 7
        """
        r = (rgb >> 16) & 0xFF
        g = (rgb >> 8) & 0xFF
        b = rgb & 0xFF
        if channel >= 0 and channel <= 7:
            if RGB_LED_MODE == self.get_mode(channel):
                self.servos8_i2c.writeto_mem(
                    self.i2c_addr, (RGB_LED_REG + (channel * 3)), bytearray([r, g, b])
                )

    def get_rgb_led(self, channel):
        """
        get rgb led.
        channel: 0 to 7
        return : (0 to 255, 0 to 255, 0 to 255)
        """
        if channel >= 0 and channel <= 7:
            if RGB_LED_MODE == self.get_mode(channel):
                return list(
                    self.servos8_i2c.readfrom_mem(self.i2c_addr, (RGB_LED_REG + (channel * 3)), 3)
                )

    def set_pwm_dutycycle(self, duty, channel):
        """
        set pwm dutycycle.
        duty : 0 to 100
        channel: 0 to 7
        """
        if channel >= 0 and channel <= 7:
            if PWM_DUTY_MODE == self.get_mode(channel):
                duty = max(min(duty, 100), 0)
                self.servos8_i2c.writeto_mem(
                    self.i2c_addr, (PWM_DUTY_REG + channel), bytearray([duty])
                )

    def get_input_current(self):
        """
        get input current.
        """
        buf = self.servos8_i2c.readfrom_mem(self.i2c_addr, SERVO_CURRENT_REG, 4)
        return round(struct.unpack("<f", buf)[0], 3)

    def get_device_spec(self, mode):
        """
        get device firmware version and i2c address.
        mode : 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.servos8_i2c.readfrom_mem(self.i2c_addr, mode, 1)[0]

    def set_i2c_address(self, addr):
        """
        set i2c address.
        addr:  1 to 127
        """
        if addr >= 1 and addr <= 127:
            if addr != self.i2c_addr:
                self.servos8_i2c.writeto_mem(self.i2c_addr, I2C_ADDR_REG, bytearray([addr]))
                self.i2c_addr = addr
                sleep_ms(150)

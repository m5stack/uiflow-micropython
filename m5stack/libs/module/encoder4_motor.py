from .mbus import i2c1
from .module_helper import ModuleError
import struct
import time

DEVADDR = 0x24

MTR_PWM_DUTY = 0x20
MTR_ENCODER = 0x30
MTR_SPEED = 0x40
MTR1_MODE = 0x50
MTR2_MODE = 0x60
MTR3_MODE = 0x70
MTR4_MODE = 0x80
VIN_AMPS_FLT = 0x90
VIN_ADC8 = 0xA0
VIN_ADC12 = 0xB0
VIN_AMPS_INT = 0xC0
ENCODER_AB = 0xD0
FIRM_VER = 0xFE
I2C_ADDR = 0xFF

NORMAL_MODE = 0x00
POSITION_MODE = 0x01
SPEED_MODE = 0x02


class Encoder4MotorModule:
    def __init__(self, address: int = DEVADDR):
        """
        init the i2c address
        address : 1 to 127
        """
        self.mtr_i2c = i2c1
        self.i2c_addr = address
        if address >= 1 and address <= 127:
            self.i2c_addr = address
        self.available()
        self.mode = NORMAL_MODE

    def available(self):
        check = False
        for i in range(3):
            if self.i2c_addr in self.mtr_i2c.scan():
                check = True
                break
            time.sleep(0.2)
        if not check:
            raise ModuleError("4Encoder motor module maybe not connect")

    def set_motor_mode(self, pos, mode):
        """
        pos: [ONE or TWO or THREE or FOUR]
        mode: [NORMAL_MODE or POSITION or SPEED]
        """
        self.mode = mode
        self.mtr_i2c.writeto_mem(self.i2c_addr, MTR1_MODE + (0x10 * pos), bytearray([mode]))

    def set_all_motors_mode(self, mode):
        """
        mode: [NORMAL_MODE or POSITION or SPEED]
        """
        for i in range(0, 3):
            self.set_motor_mode(i, mode)
            time.sleep_ms(150)

    def set_motor_pwm_dutycycle(self, pos, duty):
        """
        pos: [ONE or TWO or THREE or FOUR]
        duty: -127 ~ 127
        """
        duty = min(max(duty, -128), 127)
        duty = struct.pack(">b", duty)
        self.mtr_i2c.writeto_mem(self.i2c_addr, MTR_PWM_DUTY + pos, duty)

    def get_motor_encoder_value(self, pos):
        """
        pos: [ONE or TWO or THREE or FOUR]
        """
        buf = self.mtr_i2c.readfrom_mem(self.i2c_addr, MTR_ENCODER + (0x04 * pos), 4)
        return struct.unpack(">i", buf)[0]

    def set_motor_encoder_value(self, pos, value):
        """
        pos: [ONE or TWO or THREE or FOUR]
        value: signed int 4byte
        """
        value = struct.pack(">i", value)
        self.mtr_i2c.writeto_mem(self.i2c_addr, MTR_ENCODER + (0x04 * pos), value)

    def get_encoder_mode(self):
        """
        return: 0[AB] or 1[BA] mode
        """
        return self.mtr_i2c.readfrom_mem(self.i2c_addr, ENCODER_AB, 1)[0]

    def set_encoder_mode(self, mode):
        """
        mode: [AB or BA]
        """
        self.mtr_i2c.writeto_mem(self.i2c_addr, ENCODER_AB, bytearray([mode]))
        time.sleep_ms(150)

    def get_motor_speed_value(self, pos):
        """
        pos: [ONE or TWO or THREE or FOUR]
        """
        return self.mtr_i2c.readfrom_mem(self.i2c_addr, MTR_SPEED + pos, 1)[0]

    def set_position_encoder_value(self, pos, value):
        """
        pos: [ONE or TWO or THREE or FOUR]
        value: signed int 4byte
        """
        value = struct.pack("<i", value)
        self.mtr_i2c.writeto_mem(self.i2c_addr, MTR1_MODE + (0x10 * pos) + 0x04, value)

    def set_position_max_speed_value(self, pos, value):
        """
        pos: [ONE or TWO or THREE or FOUR]
        value: -127 ~ 127
        """
        value = min(max(value, -128), 127)
        value = struct.pack("<b", value)
        self.mtr_i2c.writeto_mem(self.i2c_addr, MTR1_MODE + (0x10 * pos) + 0x08, value)

    def get_position_PID_value(self, pos):
        """
        pos: [ONE or TWO or THREE or FOUR]
        """
        return list(self.mtr_i2c.readfrom_mem(self.i2c_addr, MTR1_MODE + (0x10 * pos) + 0x01, 3))

    def set_position_PID_value(self, pos, P, I, D):
        """
        pos: [ONE or TWO or THREE or FOUR]
        P: 0 ~ 255
        I: 0 ~ 255
        D: 0 ~ 255
        """
        self.mtr_i2c.writeto_mem(
            self.i2c_addr, MTR1_MODE + (0x10 * pos) + 0x01, bytearray([P, I, D])
        )

    def get_speed_PID_value(self, pos):
        """
        pos: [ONE or TWO or THREE or FOUR]
        """
        return list(self.mtr_i2c.readfrom_mem(self.i2c_addr, MTR1_MODE + (0x10 * pos) + 0x09, 3))

    def set_speed_PID_value(self, pos, P, I, D):
        """
        pos: [ONE or TWO or THREE or FOUR]
        P: 0 ~ 255
        I: 0 ~ 255
        D: 0 ~ 255
        """
        self.mtr_i2c.writeto_mem(
            self.i2c_addr, MTR1_MODE + (0x10 * pos) + 0x09, bytearray([P, I, D])
        )

    def set_speed_point_value(self, pos, point):
        """
        pos: [ONE or TWO or THREE or FOUR]
        point: -127 ~ 127
        """
        point = min(max(point, -128), 127)
        point = struct.pack("<b", point)
        self.mtr_i2c.writeto_mem(self.i2c_addr, MTR1_MODE + (0x10 * pos) + 0x0C, point)

    def get_vin_current_float_value(self):
        """
        get input current value in float
        """
        buf = self.mtr_i2c.readfrom_mem(self.i2c_addr, VIN_AMPS_FLT, 4)
        return round(struct.unpack("<f", buf)[0], 3)

    def get_vin_current_int_value(self):
        """
        get input current value in int
        """
        buf = self.mtr_i2c.readfrom_mem(self.i2c_addr, VIN_AMPS_INT, 4)
        return struct.unpack("<i", buf)[0] * 10

    def get_vin_adc_raw8_value(self):
        """
        get input volt adc 8bit raw value
        """
        return self.mtr_i2c.readfrom_mem(self.i2c_addr, VIN_ADC8, 1)[0]

    def get_vin_adc_raw12_value(self):
        """
        get input volt adc 12bit raw value
        """
        buf = self.mtr_i2c.readfrom_mem(self.i2c_addr, VIN_ADC12, 2)
        return struct.unpack("<h", buf)[0]

    def get_vin_voltage(self):
        """
        get input volt value
        """
        value = self.get_vin_adc_raw12_value()
        return round(value / 4095 * 3.3 / (20 / 120), 2)  # 20k/(20k+100k)

    def get_device_spec(self, info):
        """
        get device firmware version and i2c address
        info: [0xFE or 0xFF]
        """
        return self.mtr_i2c.readfrom_mem(self.i2c_addr, info, 1)[0]

    def set_i2c_address(self, addr):
        """
        set i2c address
        addr: 1~127
        """
        addr = min(max(addr, 1), 127)
        if addr != self.i2c_addr:
            self.mtr_i2c.writeto_mem(self.i2c_addr, I2C_ADDR, bytearray([addr]))
            self.i2c_addr = addr
            time.sleep_ms(150)

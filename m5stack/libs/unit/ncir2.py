from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct
import time


NCIR2_I2C_ADDR = 0x5A

TEMPERATURE_REG = 0x00
EMISSIVITY_REG = 0x10
ALARM_LOW_TEMP_REG = 0x20
ALARM_HIGH_TEMP_REG = 0x22
RGB_LOW_TEMP_REG = 0x30
RGB_HIGH_TEMP_REG = 0x33
LOW_TEMP_FREQ_REG = 0x40
LOW_ALARM_INTER_REG = 0x42
LOW_ALARM_DUTY_REG = 0x44
HIGH_TEMP_FREQ_REG = 0x45
HIGH_ALARM_INTER_REG = 0x47
HIGH_ALARM_DUTY_REG = 0x49
BUZZER_FREQ_REG = 0x50
BUZZER_DUTY_REG = 0x52
BUZZER_CTRL_REG = 0x53
RGB_LED_REG = 0x60
BUTTON_REG = 0x70
SAVE_CONFIG_REG = 0x80
CHIP_TEMP_REG = 0x90
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class NCIR2Unit:
    def __init__(self, i2c: I2C | PAHUBUnit, addr: int = NCIR2_I2C_ADDR) -> None:
        """! init the i2c address
        addr : 1 to 127
        """
        self.ncir_i2c = i2c
        if addr >= 1 and addr <= 127:
            self.unit_addr = addr
        self.available()

    def available(self) -> None:
        if self.unit_addr not in self.ncir_i2c.scan():
            raise UnitError("Ncir2 unit maybe not connect")

    @property
    def get_temperature_value(self) -> float:
        """! get ncir temperature measure."""
        buf = self.read_from_mem(TEMPERATURE_REG, 2)
        return round((struct.unpack("<h", buf)[0]) / 100, 2)

    @property
    def get_emissivity_value(self) -> float:
        """! get ncir emissivity measure."""
        buf = self.read_from_mem(EMISSIVITY_REG, 2)
        return round((struct.unpack("<H", buf)[0]) / 65535, 2)

    def set_emissivity_value(self, emissive) -> None:
        """! set ncir emissivity measure.
        emissive: 0.1 to 1
        """
        if emissive >= 0.1 and emissive <= 1:
            self.ncir_i2c.writeto_mem(
                self.unit_addr, EMISSIVITY_REG, struct.pack("<H", int(round(emissive * 65535)))
            )

    def get_temperature_threshold(self, alarm_reg=ALARM_LOW_TEMP_REG) -> float:
        """! get high or low temp threshold."""
        buf = self.read_from_mem(alarm_reg, 2)
        return round((struct.unpack("<h", buf)[0]) / 100, 2)

    def set_temperature_threshold(self, alarm_reg=ALARM_LOW_TEMP_REG, temp=0) -> None:
        """! set high or low temp threshold.
        temp : C
        """
        temp = round(temp, 2) * 100
        self.ncir_i2c.writeto_mem(self.unit_addr, alarm_reg, struct.pack("<H", int(temp)))

    def get_temp_alarm_led(self, alarm_reg=RGB_LOW_TEMP_REG) -> list:
        """! get high or low temp alarm LED Color."""
        return list(self.read_from_mem(alarm_reg, 3))

    def set_temp_alarm_led(self, alarm_reg=RGB_LOW_TEMP_REG, rgb=0) -> None:
        """! set high or low temp alarm LED Color.
        rgb: 0x00 to 0xffffff
        """
        self.ncir_i2c.writeto_mem(self.unit_addr, alarm_reg, rgb.to_bytes(3, "big"))

    def get_temp_buzzer_freq(self, alarm_reg=LOW_TEMP_FREQ_REG) -> int:
        """! get high or low temp alarm freq."""
        buf = self.read_from_mem(alarm_reg, 2)
        return struct.unpack("<H", buf)[0]

    def set_temp_buzzer_freq(self, alarm_reg=LOW_TEMP_FREQ_REG, freq=20) -> None:
        """! set high or low temp alarm freq.
        freq: 20hz to 20khz
        """
        if freq >= 20 and freq <= 20000:
            self.ncir_i2c.writeto_mem(self.unit_addr, alarm_reg, struct.pack("<H", int(freq)))

    def get_temp_alarm_interval(self, alarm_reg=LOW_ALARM_INTER_REG) -> int:
        """! get high or low temp alarm interval."""
        buf = self.read_from_mem(alarm_reg, 2)
        return struct.unpack("<H", buf)[0]

    def set_temp_alarm_interval(self, alarm_reg=LOW_ALARM_INTER_REG, interval=0) -> None:
        """! set high or low temp alarm interval.
        interval: 1 to 5000 ms
        """
        interval = max(min(interval, 5000), 50)
        self.ncir_i2c.writeto_mem(self.unit_addr, alarm_reg, struct.pack("<H", int(interval)))

    def get_temp_buzzer_duty(self, duty_reg=LOW_ALARM_DUTY_REG) -> int:
        """! get buzzer duty."""
        return self.read_from_mem(duty_reg, 1)[0]

    def set_temp_buzzer_duty(self, duty_reg=LOW_ALARM_DUTY_REG, duty=0) -> None:
        """! set buzzer duty.
        duty : 0 to 255
        """
        self.ncir_i2c.writeto_mem(self.unit_addr, duty_reg, bytearray([duty]))

    @property
    def get_buzzer_freq(self) -> float:
        """! get buzzer frequency."""
        buf = self.read_from_mem(BUZZER_FREQ_REG, 2)
        return struct.unpack("<H", buf)[0]

    def set_buzzer_freq(self, freq=0) -> None:
        """! set buzzer frequency.
        freq : 20 to 20000
        """
        if freq >= 20 and freq <= 20000:
            self.ncir_i2c.writeto_mem(
                self.unit_addr, BUZZER_FREQ_REG, struct.pack("<H", int(freq))
            )

    @property
    def get_buzzer_duty(self) -> int:
        """! get buzzer duty."""
        return self.read_from_mem(BUZZER_DUTY_REG, 1)[0]

    def set_buzzer_duty(self, duty=0) -> None:
        """! set buzzer duty.
        duty : 0 to 255
        """
        self.ncir_i2c.writeto_mem(self.unit_addr, BUZZER_DUTY_REG, bytearray([duty]))

    @property
    def get_buzzer_control(self) -> bool:
        """! get buzzer control."""
        return bool(self.read_from_mem(BUZZER_CTRL_REG, 1)[0])

    def set_buzzer_control(self, ctrl=0) -> None:
        """! set buzzer control.
        ctrl : 0 to 1
        """
        self.ncir_i2c.writeto_mem(self.unit_addr, BUZZER_CTRL_REG, bytearray([ctrl]))

    @property
    def get_rgb_led(self) -> list:
        """! get rgb led."""
        return list(self.read_from_mem(RGB_LED_REG, 3))

    def set_rgb_led(self, rgb=0) -> None:
        """! set rgb led.
        rgb: 0x00 to 0xffffff
        """
        self.ncir_i2c.writeto_mem(self.unit_addr, RGB_LED_REG, rgb.to_bytes(3, "big"))

    @property
    def get_button_status(self) -> bool:
        """! get button status.
        return : 0 to 1
        """
        return not self.read_from_mem(BUTTON_REG, 1)[0]

    @property
    def save_config_setting(self) -> None:
        """! save configure setting."""
        self.ncir_i2c.writeto_mem(self.unit_addr, SAVE_CONFIG_REG, b"\x01")
        time.sleep_ms(200)

    @property
    def get_chip_temperature(self) -> float:
        """! get ncir chip temperature measure."""
        buf = self.read_from_mem(CHIP_TEMP_REG, 2)
        return round((struct.unpack("<h", buf)[0]) / 100, 2)

    def get_device_spec(self, mode) -> int:
        """! get firmware version and i2c address.
        mode : 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.read_from_mem(mode, 1)[0]

    def set_i2c_address(self, addr) -> None:
        """! set i2c address.
        addr :  1 to 127
        """
        if addr >= 1 and addr <= 127:
            if addr != self.unit_addr:
                self.ncir_i2c.writeto_mem(self.unit_addr, I2C_ADDR_REG, bytearray([addr]))
                self.unit_addr = addr
                time.sleep_ms(200)

    def read_from_mem(self, reg, num):
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self.ncir_i2c.writeto(self.unit_addr, buf)
        buf = bytearray(num)
        self.ncir_i2c.readfrom_into(self.unit_addr, buf)
        return buf

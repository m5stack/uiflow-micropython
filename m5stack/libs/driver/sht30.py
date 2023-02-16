import time

__version__ = "0.2.3"
__author__ = "Roberto Sánchez"
__license__ = "Apache License 2.0. https://www.apache.org/licenses/LICENSE-2.0"

# I2C address B 0x44 ADDR (pin 2) connected to GND
DEFAULT_I2C_ADDRESS = 0x44


class SHT30:
    """
    SHT30 sensor driver in pure python based on I2C bus

    References:
    * https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/2_Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Datasheet_digital.pdf  # NOQA
    * https://www.wemos.cc/sites/default/files/2016-11/SHT30-DIS_datasheet.pdf
    * https://github.com/wemos/WEMOS_SHT3x_Arduino_Library
    * https://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/11_Sample_Codes_Software/Humidity_Sensors/Sensirion_Humidity_Sensors_SHT3x_Sample_Code_V2.pdf
    """

    POLYNOMIAL = 0x131  # P(x) = x^8 + x^5 + x^4 + 1 = 100110001

    ALERT_PENDING_MASK = 0x8000  # 15
    HEATER_MASK = 0x2000  # 13
    RH_ALERT_MASK = 0x0800  # 11
    T_ALERT_MASK = 0x0400  # 10
    RESET_MASK = 0x0010  # 4
    CMD_STATUS_MASK = 0x0002  # 1
    WRITE_STATUS_MASK = 0x0001  # 0

    # MSB = 0x2C LSB = 0x06 Repeatability = High, Clock stretching = enabled
    MEASURE_CMD = b"\x2C\x10"
    STATUS_CMD = b"\xF3\x2D"
    RESET_CMD = b"\x30\xA2"
    CLEAR_STATUS_CMD = b"\x30\x41"
    ENABLE_HEATER_CMD = b"\x30\x6D"
    DISABLE_HEATER_CMD = b"\x30\x66"

    def __init__(self, i2c=None, delta_temp=0, delta_hum=0, i2c_address=DEFAULT_I2C_ADDRESS):
        if i2c is None:
            raise ValueError("An I2C object is required.")
        self.i2c = i2c
        self.i2c_addr = i2c_address
        self.set_delta(delta_temp, delta_hum)
        time.sleep_ms(50)

    def is_present(self):
        """
        Return true if the sensor is correctly conneced, False otherwise
        """
        return self.i2c_addr in self.i2c.scan()

    def set_delta(self, delta_temp=0, delta_hum=0):
        """
        Apply a delta value on the future measurements of temperature and/or humidity
        The units are Celsius for temperature and percent for humidity (can be negative values)
        """
        self.delta_temp = delta_temp
        self.delta_hum = delta_hum

    def _check_crc(self, data):
        # calculates 8-Bit checksum with given polynomial
        crc = 0xFF

        for b in data[:-1]:
            crc ^= b
            for _ in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ SHT30.POLYNOMIAL
                else:
                    crc <<= 1
        crc_to_check = data[-1]
        return crc_to_check == crc

    def send_cmd(self, cmd_request, response_size=6, read_delay_ms=100):
        """
        Send a command to the sensor and read (optionally) the response
        The responsed data is validated by CRC
        """
        try:
            self.i2c.writeto(self.i2c_addr, cmd_request)
            if not response_size:
                return
            time.sleep_ms(read_delay_ms)
            data = self.i2c.readfrom(self.i2c_addr, response_size)

            for i in range(response_size // 3):
                if not self._check_crc(data[i * 3 : (i + 1) * 3]):  # pos 2 and 5 are CRC
                    raise SHT30Error(SHT30Error.CRC_ERROR)
            if data == bytearray(response_size):
                raise SHT30Error(SHT30Error.DATA_ERROR)
            return data
        except OSError:
            raise SHT30Error(SHT30Error.BUS_ERROR)
        except Exception as ex:
            raise ex

    def clear_status(self):
        """
        Clear the status register
        """
        return self.send_cmd(SHT30.CLEAR_STATUS_CMD, None)

    def reset(self):
        """
        Send a soft-reset to the sensor
        """
        return self.send_cmd(SHT30.RESET_CMD, None)

    def status(self, raw=False):
        """
        Get the sensor status register.
        It returns a int value or the bytearray(3) if raw==True
        """
        data = self.send_cmd(SHT30.STATUS_CMD, 3, read_delay_ms=20)

        if raw:
            return data

        status_register = data[0] << 8 | data[1]
        return status_register

    def measure(self, raw=False):
        """
        If raw==True returns a bytearrya(6) with sensor direct measurement otherwise
        It gets the temperature (T) and humidity (RH) measurement and return them.

        The units are Celsius and percent
        """
        data = self.send_cmd(SHT30.MEASURE_CMD, 6)

        if raw:
            return data

        t_celsius = (((data[0] << 8 | data[1]) * 175) / 0xFFFF) - 45 + self.delta_temp
        rh = (((data[3] << 8 | data[4]) * 100.0) / 0xFFFF) + self.delta_hum
        return t_celsius, rh

    def measure_int(self, raw=False):
        """
        Get the temperature (T) and humidity (RH) measurement using integers.
        If raw==True returns a bytearrya(6) with sensor direct measurement otherwise
        It returns a tuple with 4 values: T integer, T decimal, H integer, H decimal
        For instance to return T=24.0512 and RH= 34.662 This method will return
        (24, 5, 34, 66) Only 2 decimal digits are returned, .05 becomes 5
        Delta values are not applied in this method
        The units are Celsius and percent.
        """
        data = self.send_cmd(SHT30.MEASURE_CMD, 6)
        if raw:
            return data
        aux = (data[0] << 8 | data[1]) * 175
        t_int = (aux // 0xFFFF) - 45
        t_dec = (aux % 0xFFFF * 100) // 0xFFFF
        aux = (data[3] << 8 | data[4]) * 100
        h_int = aux // 0xFFFF
        h_dec = (aux % 0xFFFF * 100) // 0xFFFF
        return t_int, t_dec, h_int, h_dec


class SHT30Error(Exception):
    """
    Custom exception for errors on sensor management
    """

    BUS_ERROR = 0x01
    DATA_ERROR = 0x02
    CRC_ERROR = 0x03

    def __init__(self, error_code=None):
        self.error_code = error_code
        super().__init__(self.get_message())

    def get_message(self):
        if self.error_code == SHT30Error.BUS_ERROR:
            return "Bus error"
        elif self.error_code == SHT30Error.DATA_ERROR:
            return "Data error"
        elif self.error_code == SHT30Error.CRC_ERROR:
            return "CRC error"
        else:
            return "Unknown error"

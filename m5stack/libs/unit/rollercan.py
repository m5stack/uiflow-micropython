# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C, UART
from typing import Literal
from pahub import PAHUBUnit
from micropython import const
from unit_helper import UnitError
import struct
import time

#! I2C REGISTER MAP
_ROLLERCAN_I2C_ADDR = const(0x64)
_ROLLERCAN_CAN_ADDR = const(0xA8)

#! 485 VIA I2C CONTROL READ & WRITE !#
_READ_I2C_SLAVE_REG_ADDR = 0x60
_WRITE_I2C_SLAVE_REG_ADDR = 0x61
_READ_I2C_SLAVE_ADDR = 0x62
_WRITE_I2C_SLAVE_ADDR = 0x63

_COMMON_REG = {
    #! "COMMAND": (I2C-REGISTER, CAN-CMD-ID, CAN-DATA-FIELD, CAN-INDEX-ID, CAN-READ-LENGTH, CAN-DATA-AREA)
    #! MOTOR CONFIGURATION REGISTER !#                                     这里的LENGTH是指可读写单个参数列表中的字节数
    "MOTOR_OUTPUT": (0x00, 0x12, None, 0x7004, 1),
    "MOTOR_MODE": (0x01, 0x12, None, 0x7005, 1),
    "MOTOR_ORP": (0x0A, 0x0C, None, None),  # 0x0C:ENABLE,0x0D:DISABLE
    "RELEASE_STALL_PROTECT": (0x0B, 0x12, None, 0x7003, 1),
    "MOTOR_STATUS": (0x0C, None, None, None, 22),
    "MOTOR_ERROR_CODE": (0x0D, None, None, None),
    "BTN_SWITCH_MODE_ENABLE": (0x0E, None, None, None),
    "MOTOR_STALL_PROTRCT": (0x0F, None, None, None),
    "MOTOR_ID": (0x10, 0x00, 16, None, 8),  # REA CMD ID为0x00,WRITE CMD ID为0x07
    "CAN_BSP": (0x11, 0x0B, 16, None),
    "RGB_BRIGHT": (0x12, 0x12, None, 0x7052, 1),
    #! SPEED CONTROL REGISTER !#
    "SPEED_SETTING": (0x40, 0x12, None, 0x700A, 4),
    "SPEED_MAX_CURRENT": (0x50, 0x12, None, 0x7018, 4),
    "SPEED_READBACK": (0x60, 0x12, None, 0x7030, 4),
    "SPEED_PID": (0x70, 0x12, None, 0x7020, 4),  # 特例SPEED ,P,I,D被分为0x7020~0x7022三个写入地址
    #! POSITION CONTROL REGISTER !#
    "POSITION_SETTING": (0x80, 0x12, None, 0x7016, 4),
    "POSITION_MAX_CURRENT": (0x20, 0x12, None, 0x7017, 4),
    "POSITION_READBACK": (0x90, 0x12, None, 0x7031, 4),
    "POSITION_PID": (
        0xA0,
        0x12,
        None,
        0x7023,
        4,
    ),  # POSITION ,P,I,D被分为0x7023~0x7025三个写入地址
    #! CURRENT CONTROL REGISTER !#
    "MAX_CURRENT": (0xB0, 0x12, None, 0x7006, 4),
    "CURRENT_READBACK": (0xC0, 0x12, None, 0x7032, 4),
    #! SYSTEM REGISTER !#
    #! "COMMAND": (I2C-REGISTER, CAN-CMD-ID, CAN-INDEX-ID, CAN-READ-WRITE-POSISTION)
    "SYSTEM_RGB": (0x30, 0x12, None, 0x7051, 4),
    "SYSTEM_RGB_MODE": (0x33, 0x12, None, 0x7050, 1),
    "SYSTEM_VIN": (0x34, 0x12, None, 0x7034, 4),
    "SYSTEM_TEMP": (0x38, 0x12, None, 0x7035, 4),
    "SYSTEM_ENCODER": (0x3C, 0x12, None, 0x7033, 4),
    "SYSTEM_FLASH_WRITE": (0xF0, 0x12, None, 0x7002, 1),
    "SYSTEM_FIRMWARE": (0xFE, None, None),
    "SYSTEM_I2C_ADDRESS": (0xFF, None, None),
}


class RollerBase:
    #! Initialize the roller485Base.
    def __init__(self) -> None:
        pass

    def read(self, register, length) -> bytes:
        raise NotImplementedError("Subclasses should implement this method!")

    def write(self, register, data: bytes):
        raise NotImplementedError("Subclasses should implement this method!")

    def readfrom_mem(self, addr: int, mem_addr: int, nbytes: int) -> bytes:  # 0x60
        raise NotImplementedError("Subclasses should implement this method!")

    def readfrom_mem_into(self, addr: int, mem_addr: int, buf: bytearray) -> None:  # 0x60
        raise NotImplementedError("Subclasses should implement this method!")

    def writeto_mem(self, addr: int, mem_addr: int, buf: list) -> Literal[True]:  # 0x61
        raise NotImplementedError("Subclasses should implement this method!")

    def readfrom(self, addr: int, nbytes: int):  # 0x62
        raise NotImplementedError("Subclasses should implement this method!")

    def readfrom_into(self, addr: int, buf: bytearray) -> None:  # 0x62
        raise NotImplementedError("Subclasses should implement this method!")

    def writeto(self, addr: int, buf: bytes | bytearray, stop: bool = True):
        raise NotImplementedError("Subclasses should implement this method!")

    def scan(self) -> list:
        raise NotImplementedError("Subclasses should implement this method!")

    def deinit(self) -> None:
        raise NotImplementedError("Subclasses should implement this method!")

    def create_frame(self, cmd_id, option, data, is_read=False):
        raise NotImplementedError("Subclasses should implement this method!")

    #! MOTOR CONFIGURATION API !#
    def set_motor_output_state(self, ctrl: int = 0) -> None:
        """! Set the motor output state.

        @param ctrl: Control value for the motor output.
        """
        self.write("MOTOR_OUTPUT", bytes([ctrl]))

    def get_motor_output_state(self) -> bool:
        """! Get the motor output status.

        @return: True if the motor output is active, False otherwise.
        """
        return self.read("MOTOR_OUTPUT", 1)[0] != 0

    def set_motor_mode(self, mode: int) -> None:
        """! Set the motor mode.

        @param mode: The mode to set for the motor.
        """
        self.write("MOTOR_MODE", bytes([mode]))

    def get_motor_mode(self) -> int:
        """! Get the motor mode.

        @return: The current motor mode.
        """
        return self.read("MOTOR_MODE", 1)[0]

    def set_motor_over_range_protect_state(self, state: int = 1) -> None:
        """! Set the motor over range protection state.

        @param state: Protection state value (1 to enable, 0 to disable).
        """
        self.write("MOTOR_ORP", bytes([state]))

    def get_motor_over_range_protect_state(self) -> bool:
        """! Get the motor over range protection status.

        @return: True if protection is enabled, False otherwise.
        """
        return self.read("MOTOR_ORP", 1)[0] != 0

    def remove_motor_jam_protect(self) -> None:
        """! Set the motor jam release protection."""
        self.write("RELEASE_STALL_PROTECT", bytes([0x01]))

    def get_motor_status(self) -> int:
        """! Get the motor status.

        @return: The current status of the motor.
        """
        return self.read("MOTOR_STATUS", 1)[0]

    def get_motor_error_code(self) -> int:
        """! Get the motor error code.

        @return: The current error code of the motor.
        """
        return self.read("MOTOR_ERROR_CODE", 1)[0]

    def set_button_change_mode(self, state: int = 1) -> None:
        """! Set the button change mode.

        @param state: Change mode state value (1 to enable, 0 to disable).
        """
        self.write("BTN_SWITCH_MODE_ENABLE", bytes([state]))

    def get_button_change_mode(self) -> int:
        """! Get the button change mode.

        @return: The current button change mode value.
        """
        return self.read("BTN_SWITCH_MODE_ENABLE", 1)[0]

    def set_motor_jam_protect_state(self, state: int = 1) -> None:
        """! Set the motor jam protection enable/disable.

        @param state: Protection state value (1 to enable, 0 to disable).
        """
        self.write("MOTOR_STALL_PROTRCT", bytes([state]))

    def get_motor_jam_protect_state(self) -> bool:
        """! Get the motor jam protection status.

        @return: True if jam protection is enabled, False otherwise.
        """
        return self.read("MOTOR_STALL_PROTRCT", 1)[0] != 0

    def set_motor_id(self, id: int = 0) -> None:
        """! Set the motor ID.

        @param id: The ID to assign to the motor.
        """
        self.write("MOTOR_ID", bytes([id]))

    def get_motor_id(self) -> int:
        """! Get the motor ID.

        @return: The current motor ID.
        """
        return self.read("MOTOR_ID", 1)[0]

    def set_485_baudrate(self, bps: int = 0) -> None:
        """! Set the 485 baudrate.

        @param bps: Baud rate value.
        """
        self.write("CAN_BSP", bytes([bps]))

    def get_485_baudrate(self) -> int:
        """! Get the 485 baudrate.

        @return: The current 485 baudrate.
        """
        return self.read("CAN_BSP", 1)[0]

    def set_rgb_brightness(self, bright: int = 0) -> None:
        """! Set RGB brightness.

        @param bright: Brightness value.
        """
        self.write("RGB_BRIGHT", bytes([bright]))

    def get_rgb_brightness(self) -> int:
        """! Get RGB brightness.

        @return: The current RGB brightness value.
        """
        return self.read("RGB_BRIGHT", 1)[0]

    def set_motor_speed(self, speed: int) -> None:
        """! Set the motor speed and max current setting.

        @param speed: The speed value to set.
        """
        speed *= 100
        self.write("SPEED_SETTING", struct.pack("<i", speed))

    def get_motor_speed(self) -> int:
        """! Get the motor speed and max current setting.

        @return: The current motor speed.
        """
        buf = self.read("SPEED_SETTING", 4)
        return int(struct.unpack("<i", buf)[0] / 100)

    def set_speed_max_current(self, current: int) -> None:
        """! Set the motor speed and max current setting.

        @param current: The max current value to set.
        """
        current *= 100
        self.write("SPEED_MAX_CURRENT", struct.pack("<i", current))

    def get_speed_max_current(self) -> int:
        """! Get the motor speed and max current setting.

        @return: The current max current setting.
        """
        buf = self.read("SPEED_MAX_CURRENT", 4)
        print(buf)
        return int(struct.unpack("<i", buf)[0] / 100)

    def get_motor_speed_readback(self) -> float:
        """! Get the motor speed readback.

        @return: The readback value of the motor speed.
        """
        buf = self.read("SPEED_READBACK", 4)
        return int(struct.unpack("<i", buf)[0] / 100)

    def set_motor_speed_pid(self, p: float, i: float, d: float) -> None:
        """! Set the motor speed PID.

        @param p: Proportional gain.
        @param i: Integral gain.
        @param d: Derivative gain.
        """
        p *= 100000
        i *= 10000000
        d *= 100000
        self.write("SPEED_PID", struct.pack("<iii", int(p), int(i), int(d)))

    def get_motor_speed_pid(self) -> tuple:
        """! Get the motor speed PID.

        @return: A tuple containing the PID values.
        """
        buf = self.read("SPEED_PID", 12)
        return tuple(a / b for a, b in zip(struct.unpack("<iii", buf), (100000, 10000000, 100000)))

    def set_motor_position(self, position: int) -> None:
        """! Set the motor position and max current setting.

        @param position: The position value to set.
        """
        position *= 100
        self.write("POSITION_SETTING", struct.pack("<i", position))

    def get_motor_position(self) -> int:
        """! Get the motor position and max current setting.

        @return: The current motor position.
        """
        buf = self.read("POSITION_SETTING", 4)
        return int(struct.unpack("<i", buf)[0] / 100)

    def set_position_max_current(self, current: int) -> None:
        """! Set the motor position and max current setting.

        @param current: The max current value to set.
        """
        current *= 100
        self.write("POSITION_MAX_CURRENT", struct.pack("<i", current))

    def get_position_max_current(self) -> int:
        """! Get the motor position and max current setting.

        @return: The current max current setting.
        """
        buf = self.read("POSITION_MAX_CURRENT", 4)
        return int(struct.unpack("<i", buf)[0] / 100)

    def get_motor_position_readback(self) -> float:
        """! Get the motor position readback.

        @return: The readback value of the motor position.
        """
        buf = self.read("POSITION_READBACK", 4)
        return struct.unpack("<i", buf)[0] / 100

    def get_motor_position_pid(self) -> tuple:
        """! Get the motor position PID.

        @return: A tuple containing the PID values for position.
        """
        buf = self.read("POSITION_PID", 12)
        return struct.unpack("<iii", buf)

    def set_motor_position_pid(self, p: float, i: float, d: float) -> None:
        """! Set the motor position PID.

        @param p: Proportional gain.
        @param i: Integral gain.
        @param d: Derivative gain.
        """
        p *= 100000
        i *= 10000000
        d *= 100000
        buf = struct.pack("<iii", int(p), int(i), int(d))
        print(f"buf:{buf}")
        self.write("POSITION_PID", buf)

    def set_motor_max_current(self, current: int) -> None:
        """! Set the motor max current.

        @param current: The maximum current for the motor, multiplied by 100 before sending.
        """
        current *= 100
        self.write("MAX_CURRENT", struct.pack("<i", current))

    def get_motor_max_current(self) -> int:
        """! Get the motor max current.

        @return: The motor max current, divided by 100 after reading.
        """
        buf = self.read("MAX_CURRENT", 4)
        return int(struct.unpack("<i", buf)[0] / 100)

    def get_motor_current_readback(self) -> float:
        """! Get the motor current readback.

        @return: The motor current readback value, divided by 100 after reading.
        """
        buf = self.read("CURRENT_READBACK", 4)
        return struct.unpack("<i", buf)[0] / 100

    def set_rgb_color(self, rgb: int = 0) -> None:
        """! Set the system RGB color.

        @param rgb: The RGB color value, where the format is 0xRRGGBB.
        """
        r = (rgb >> 16) & 0xFF
        g = (rgb >> 8) & 0xFF
        b = rgb & 0xFF
        self.write("SYSTEM_RGB", bytes([b, g, r]))

    def get_rgb_color(self) -> tuple:
        """! Get the system RGB color.

        @return: The RGB color as a tuple (R, G, B).
        """
        buf = self.read("SYSTEM_RGB", 3)
        return tuple(reversed(struct.unpack("BBB", buf)))

    def set_rgb_mode(self, mode: int) -> None:
        """! Set the system RGB mode.

        @param mode: The RGB mode value.
        """
        self.write("SYSTEM_RGB_MODE", bytes([mode]))

    def get_rgb_mode(self) -> int:
        """! Get the system RGB mode.

        @return: The current RGB mode value.
        """
        return self.read("SYSTEM_RGB_MODE", 1)[0]

    def get_vin_voltage(self) -> int:
        """! Get the system VIN voltage.

        @return: The system VIN voltage value, multiplied by 10 after reading.
        """
        buf = self.read("SYSTEM_VIN", 4)
        return struct.unpack("<i", buf)[0] * 10

    def get_temperature_value(self) -> int:
        """! Get the system temperature.

        @return: The current system temperature value.
        """
        buf = self.read("SYSTEM_TEMP", 4)
        return struct.unpack("<i", buf)[0]

    def set_encoder_value(self, count: int) -> None:
        """! Set the system encoder value.

        @param count: The encoder count value.
        """
        self.write("SYSTEM_ENCODER", struct.pack("<i", count))

    def get_encoder_value(self) -> int:
        """! Get the system encoder value.

        @return: The current encoder value.
        """
        buf = self.read("SYSTEM_ENCODER", 4)
        return struct.unpack("<i", buf)[0]

    def save_param_to_flash(self) -> None:
        """! Save the motor data to flash."""
        time.sleep_ms(10)
        self.write("SYSTEM_FLASH_WRITE", b"\x01")
        time.sleep_ms(200)

    def get_firmware_version(self) -> int:
        """! Get the device firmware version.

        @return: The current firmware version.
        """
        return self.read("SYSTEM_FIRMWARE", 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """! Set the I2C address.

        @param addr: The new I2C address. Must be between 0x08 and 0x77.
        """
        if 0x08 <= addr <= 0x77:
            time.sleep_ms(10)
            if addr != self._i2c_addr:
                self.write("SYSTEM_I2C_ADDRESS", struct.pack("B", addr))
                self._i2c_addr = addr
            time.sleep_ms(200)

    def get_i2c_address(self) -> int:
        """! Get the current I2C address.

        @return: The current I2C address.
        """
        return self.read("SYSTEM_I2C_ADDRESS", 1)[0]


class RollerI2C(RollerBase):
    def __init__(
        self, i2c: I2C | PAHUBUnit, address: int = _ROLLERCAN_I2C_ADDR, mode=None
    ) -> None:
        """! Initialize the RollerI2C object.

        @param i2c: I2C bus instance or PAHUBUnit instance.
        @param address: I2C address of the device. Defaults to _ROLLERCAN_I2C_ADDR.
        """
        self._i2c_bus = i2c
        self._i2c_addr = address
        super().__init__()

    def read(self, register, length) -> bytes:
        """! Read data from a specified register on the I2C device.

        @param register: The name of the register to read from.
        @param length: The number of bytes to read.
        @return: The data read from the device as a bytes object.
        """
        return self._i2c_bus.readfrom_mem(self._i2c_addr, _COMMON_REG[register][0], length)

    def write(self, register, bytes) -> None:
        """! Write data to a specified register on the I2C device.

        @param register: The name of the register to write to.
        @param bytes: The data to write to the register as a bytes object.
        """
        self._i2c_bus.writeto_mem(self._i2c_addr, _COMMON_REG[register][0], bytes)


class RollerCAN(RollerBase):
    def __init__(self, bus, address=_ROLLERCAN_CAN_ADDR, mode=None) -> None:
        """! Initialize the RollerCAN object.

        @param bus: The CAN bus instance.
        @param address: The motor's CAN address. Defaults to _ROLLERCAN_CAN_ADDR.
        """
        self._can_bus = bus
        self._can_addr = address  # motor id == address
        super().__init__()
        self._obuffer = bytearray(15)  # Output buffer for sending commands.
        self._ibuffer = bytearray(17)  # Input buffer for receiving responses.
        self.setting_buf = [0] * 8  # Buffer for storing settings.
        self.rgb_buf = [0] * 8  # Buffer for storing RGB data.

    def create_frame(self, register, option, data, is_read=False):
        if len(data) < 4:
            data = data[:4] + b"\x00" * (4 - len(data))
        identifier = (
            0x00000000
            | ((_COMMON_REG[register][1] if not is_read else _COMMON_REG[register][1] - 1) << 24)
            | (option << 16)
            | self._can_addr
        )
        can_data = (
            bytes(
                [_COMMON_REG[register][3] & 0xFF, (_COMMON_REG[register][3] >> 8) & 0xFF, 0x0, 0x0]
            )
            + data
        )
        return identifier, can_data

    def read(self, register, length):
        identifier, can_data = self.create_frame(register, 0, bytes(0), is_read=True)
        self._can_bus.send(can_data, id=identifier, timeout=0, rtr=False, extframe=True)
        return self.read_response()

    def write(self, register, bytes):
        try:
            identifier, can_data = self.create_frame(register, 0, bytes)
            self._can_bus.send(can_data, id=identifier, timeout=0, rtr=False, extframe=True)
            self._can_bus.recv(0, timeout=100)  # 清除写入后的返回数据，调整超时为 100ms
            buf = self.read(register, bytes)
            # if (can_data[4:8], _COMMON_REG[register][3]) == buf:
            return (can_data[4:8]) == buf
        except Exception as e:
            print(f"Error in write: {e}")
            return False

    def read_response(self):
        receive_data = self._can_bus.recv(0, timeout=200)
        cmd_id = (receive_data[0] >> 24) & 0x1F  # 24~28 bit
        master_can_id = (receive_data[0] >> 8) & 0xFFFF  # 8~23 bit
        motor_can_id = (receive_data[0] >> 0) & 0xFF  # 0~7 bit
        index = (receive_data[4][1] << 8) | receive_data[4][0]
        data = receive_data[4][4:8]
        print(f"Identifier: 0x{receive_data[0]:04x}")
        print(f"CMD ID: 0x{cmd_id:02x}")
        print(f"MASTER CAN ID: 0x{master_can_id:02x}")
        print(f"Motor ID: 0x{motor_can_id:01x}")
        print(f"Rec Data: 0x{receive_data[4].hex()}")
        print(f"Index: 0x{index:04x}")
        print(f"Data: 0x{data.hex()}")
        # return data, index
        return data


class RollerCANUnit:
    """! A factory class to create Roller instances based on communication mode."""

    _I2C_MODE = 0  # I2C mode identifier
    _CAN_MODE = 1  # CAN mode identifier
    _CAN_TO_I2C_MODE = 2  # CAN to I2C mode identifier

    def __new__(cls, *args, **kwargs) -> RollerBase:
        """! Create a new instance of Roller based on the specified communication mode.

        @param args: Positional arguments to be passed to the Roller class constructors.
        @param kwargs: Keyword arguments, including the 'mode' key to specify the communication mode.

        @return: An instance of RollerBase or one of its subclasses.
        """
        if kwargs["mode"] == cls._I2C_MODE:
            cls.instance = RollerI2C(args[0], **kwargs)
        elif kwargs["mode"] == cls._CAN_MODE:
            cls.instance = RollerCAN(args[0], **kwargs)
        # elif kwargs["mode"] == cls._CAN_TO_I2C_MODE:
        #     cls.instance = RollerCANToI2CBus(args[0], **kwargs)
        else:
            raise ValueError("Invalid mode specified")
        return cls.instance

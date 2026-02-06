# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C, UART
from micropython import const
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import struct
import time
import sys

if sys.platform != "esp32":
    from typing import Literal

#! I2C REGISTER MAP
_ROLLERCAN_I2C_ADDR = const(0x64)
_ROLLERCAN_CAN_ADDR = const(0xA8)

_COMMON_REG = {
    #! "COMMAND": (I2C-REGISTER, CAN-CMD-ID, CAN-DATA-FIELD, CAN-INDEX-ID)
    #! MOTOR CONFIGURATION REGISTER !#
    "READ_I2C_SLAVE": (None, 0x15, None, None),
    "WRITE_I2C_SLAVE": (None, 0x16, None, None),
    "MOTOR_OUTPUT": (0x00, 0x12, None, 0x7004),
    "MOTOR_MODE": (0x01, 0x12, None, 0x7005),
    "MOTOR_ORP": (0x0A, None, None, None),  # 0x0C: ENABLE, 0x0D: DISABLE
    "RELEASE_STALL_PROTECT": (0x0B, 0x12, None, 0x7003),
    "MOTOR_STATUS": (0x0C, None, None, None),
    "MOTOR_ERROR_CODE": (0x0D, None, None, None),
    "BTN_SWITCH_MODE_ENABLE": (0x0E, None, None, None),
    "MOTOR_STALL_PROTRCT": (0x0F, 0x0C, None, None),
    "MOTOR_STALL_PROTRCT_REMOVE": (0x0F, 0x0D, None, None),
    "MOTOR_ID": (0x10, 0x00, None, None),  # REA CMD ID 为 0x00
    "SET_MOTOR_ID": (0x10, 0x07, None, None),  # WRITE CMD ID 为 0x07
    "CAN_BSP": (0x11, 0x0B, None, None),
    "RGB_BRIGHT": (0x12, 0x12, None, 0x7052),
    #! SPEED CONTROL REGISTER !#
    "SPEED_SETTING": (0x40, 0x12, None, 0x700A),
    "SPEED_MAX_CURRENT": (0x50, 0x12, None, 0x7018),
    "SPEED_READBACK": (0x60, 0x12, None, 0x7030),
    "SPEED_PID": (0x70, 0x12, None, 0x7020),
    "SPEED_PID_I": (None, 0x12, None, 0x7021),
    "SPEED_PID_D": (None, 0x12, None, 0x7022),
    #! POSITION CONTROL REGISTER !#
    "POSITION_SETTING": (0x80, 0x12, None, 0x7016),
    "POSITION_MAX_CURRENT": (0x20, 0x12, None, 0x7017),
    "POSITION_READBACK": (0x90, 0x12, None, 0x7031),
    "POSITION_PID": (0xA0, 0x12, None, 0x7023),
    "POSITION_PID_I": (None, 0x12, None, 0x7024),
    "POSITION_PID_D": (None, 0x12, None, 0x7025),
    #! CURRENT CONTROL REGISTER !#
    "MAX_CURRENT": (0xB0, 0x12, None, 0x7006),
    "CURRENT_READBACK": (0xC0, 0x12, None, 0x7032),
    #! SYSTEM REGISTER !#
    "SYSTEM_RGB": (0x30, 0x12, None, 0x7051),
    "SYSTEM_RGB_MODE": (0x33, 0x12, None, 0x7050),
    "SYSTEM_VIN": (0x34, 0x12, None, 0x7034),
    "SYSTEM_TEMP": (0x38, 0x12, None, 0x7035),
    "SYSTEM_ENCODER": (0x3C, 0x12, None, 0x7033),
    "SYSTEM_FLASH_WRITE": (0xF0, 0x12, None, 0x7002),
    "SYSTEM_FIRMWARE": (0xFE, None, None, None),
    "SYSTEM_I2C_ADDRESS": (0xFF, None, None, None),
}


class RollerBase:
    #! Initialize the roller485Base.
    def __init__(self) -> None:
        pass

    def read(self, register, length) -> bytes:
        raise NotImplementedError("Subclasses should implement this method!")

    def i2c_read(self, register, length):
        raise NotImplementedError("Subclasses should implement this method!")

    def i2c_write(self, register, data, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method!")

    def write(self, register, data: bytes):
        raise NotImplementedError("Subclasses should implement this method!")

    def readfrom_mem(
        self, addr: int, mem_addr: int, nbytes: int, *args, **kwargs
    ) -> bytes:  # 0x60
        raise NotImplementedError("Subclasses should implement this method!")

    def readfrom_mem_into(
        self, addr: int, mem_addr: int, buf: bytearray, *args, **kwargs
    ) -> None:  # 0x60
        raise NotImplementedError("Subclasses should implement this method!")

    def writeto_mem(
        self, addr: int, mem_addr: int, buf: list, *args, **kwargs
    ) -> Literal[True]:  # 0x61
        raise NotImplementedError("Subclasses should implement this method!")

    def readfrom(self, addr: int, nbytes: int, *args, **kwargs):  # 0x62
        raise NotImplementedError("Subclasses should implement this method!")

    def readfrom_into(self, addr: int, buf: bytearray, *args, **kwargs) -> None:  # 0x62
        raise NotImplementedError("Subclasses should implement this method!")

    def writeto(self, addr: int, buf: bytes | bytearray, *args, **kwargs):
        raise NotImplementedError("Subclasses should implement this method!")

    def scan(self, *args, **kwargs) -> list:
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
        if self._mode == RollerCANUnit.I2C_MODE:
            return self.read("MOTOR_ERROR_CODE", 1)[0]
        else:
            return self.error_code

    def set_button_change_mode(self, state: int = 1) -> None:
        """! Set the button change mode.

        @param state: Change mode state value (1 to enable, 0 to disable).
        """
        self.write("BTN_SWITCH_MODE_ENABLE", bytes([state]))

    def get_button_change_mode(self) -> int:
        """! Get Button switching mode status.

        @return: The current button change mode value.
        """
        return self.read("BTN_SWITCH_MODE_ENABLE", 1)[0]

    def set_motor_jam_protect_state(self, state: int = 1) -> None:
        """! Set the motor jam protection enable/disable.

        @param state: Protection state value (1 to enable, 0 to disable).
        """
        self.write(
            "MOTOR_STALL_PROTRCT" if state else "MOTOR_STALL_PROTRCT_REMOVE", bytes([state])
        )

    def get_motor_jam_protect_state(self) -> bool:
        """! Get the motor jam protection status.

        @return: True if jam protection is enabled, False otherwise.
        """
        return self.read("MOTOR_STALL_PROTRCT", 1)[0] != 0

    def set_motor_id(self, id: int = 0) -> None:
        """! Set the motor ID.

        @param id: The ID to assign to the motor.
        """
        self.write(
            "SET_MOTOR_ID" if self._mode != RollerCANUnit.I2C_MODE else "MOTOR_ID", bytes([id])
        )

    def get_motor_id(self) -> int:
        """! Get the motor ID.

        @return: The current motor ID.
        """
        return self.read("MOTOR_ID", 1)[0]

    def set_can_baudrate(self, bps: int = 0) -> None:
        """! Set the can baudrate.

        @param bps: Baud rate value.
        """
        self.write("CAN_BSP", bytes([bps]))

    def get_can_baudrate(self) -> int:
        """! Get the can baudrate.

        @return: The current can baudrate.
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
        if self._mode != RollerCANUnit.I2C_MODE:
            self.write("SPEED_PID", struct.pack("<i", int(p)))
            self.write("SPEED_PID_I", struct.pack("<i", int(i)))
            self.write("SPEED_PID_D", struct.pack("<i", int(d)))
        else:
            self.write("SPEED_PID", struct.pack("<iii", int(p), int(i), int(d)))

    def get_motor_speed_pid(self) -> tuple:
        """! Get the motor speed PID.

        @return: A tuple containing the PID values.
        """
        if self._mode != RollerCANUnit.I2C_MODE:
            buf = bytearray()
            buf.extend(self.read("SPEED_PID", 4))
            buf.extend(self.read("SPEED_PID_I", 4))
            buf.extend(self.read("SPEED_PID_D", 4))
            print(f"buf:{buf}")
        else:
            buf = self.read("SPEED_PID", 12)
        return struct.unpack("<iii", buf)

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
        if self._mode != RollerCANUnit.I2C_MODE:
            buf = bytearray()
            buf.extend(self.read("POSITION_PID", 4))
            buf.extend(self.read("POSITION_PID_I", 4))
            buf.extend(self.read("POSITION_PID_D", 4))
            print(f"buf:{buf}")
        else:
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
        if self._mode != RollerCANUnit.I2C_MODE:
            self.write("POSITION_PID", struct.pack("<i", int(p)))
            self.write("POSITION_PID_I", struct.pack("<i", int(i)))
            self.write("POSITION_PID_D", struct.pack("<i", int(d)))
        else:
            self.write("POSITION_PID", struct.pack("<iii", int(p), int(i), int(d)))

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
        self._mode = mode
        if self._i2c_addr not in self._i2c_bus.scan():
            raise Exception("RollerCAN unit not found in Grove")
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
        @param mode: Optional mode for setting specific operational mode.
        """
        self._can_bus = bus
        self._can_addr = address  # motor id == address
        self._mode = RollerCANUnit.CAN_MODE
        super().__init__()
        self._obuffer = bytearray(15)  # Output buffer for sending commands.
        self._ibuffer = bytearray(17)  # Input buffer for receiving responses.
        self.setting_buf = [0] * 8  # Buffer for storing settings.
        self.rgb_buf = [0] * 8  # Buffer for storing RGB data.

    def create_frame(self, register, option, data, is_read=False):
        """! Create a CAN frame for sending commands.

        @param register: The register for command identification.
        @param option: Command option to specify the data.
        @param data: Data payload for the frame.
        @param is_read: Whether this frame is for a read command.
        @return: A tuple containing the CAN identifier and data payload.
        """
        if len(data) < 4:
            data = data[:4] + b"\x00" * (4 - len(data))
        cmd_id = _COMMON_REG[register][1]
        if is_read:
            if cmd_id == 0x12:
                cmd_id -= 1
            elif cmd_id in range(0x0C, 0x0D + 1):
                cmd_id = 0x02
        else:
            if cmd_id == 0x07 or cmd_id == 0x0B:
                option = data[0]
        index_id = _COMMON_REG[register][3] or 0
        identifier = 0x00000000 | (cmd_id << 24) | (option << 16) | self._can_addr
        if cmd_id == 0x15:
            can_data = data + bytes([0, 0, 0, 0])
        elif cmd_id == 0x16:
            can_data = data[:8] + b"\x00" * (8 - len(data))
        else:
            can_data = bytes([index_id & 0xFF, (index_id >> 8) & 0xFF, 0x0, 0x0]) + data
        return identifier, can_data

    def read(self, register, length):
        """! Send a read command to a specific register.

        @param register: The register address to read from.
        @param length: Length of data to read.
        @return: Data received from the register.
        """
        cmd_id = _COMMON_REG[register][1]
        if cmd_id in {0x12, 0x00, 0x15}:
            if cmd_id == 0x12:
                self._can_bus.recv(0, timeout=1)  # 清除写入后的返回数据，调整超时为 100ms
            identifier, can_data = self.create_frame(register, 0, bytes(0), is_read=True)
            self._can_bus.send(can_data, id=identifier, timeout=0, rtr=False, extframe=True)
        return self.read_response()

    def i2c_read(self, register, length):
        """! Read data from an I2C slave via CAN.

        @param register: The I2C register address to read from.
        @param length: Number of bytes to read.
        @return: A tuple containing success status and read data.
        """
        identifier, can_data = self.create_frame("READ_I2C_SLAVE", 0, bytes([register, length]))
        self._can_bus.send(can_data, id=identifier, timeout=0, rtr=False, extframe=True)
        return self.read_response()

    def i2c_write(self, register, data, *args, **kwargs):
        """! Write data to an I2C slave via CAN.

        @param register: The I2C register address to write to.
        @param data: The data to write.
        @param stop: Whether to end the transaction with a stop condition.
        @return: Success status of the write operation.
        """
        stop = args[0] if args else True
        identifier, can_data = self.create_frame(
            "WRITE_I2C_SLAVE", register | 0x80 if stop else register, bytes([len(data)]) + data
        )
        self._can_bus.send(can_data, id=identifier, timeout=0, rtr=False, extframe=True)
        return self.read_response()

    def write(self, register, data):
        """! Write data to a specific register.

        @param register: The register address to write to.
        @param data: Data payload to send to the register.
        @return: Boolean indicating whether the write operation was successful.
        """
        try:
            print(data)
            identifier, can_data = self.create_frame(register, 0, data)
            self._can_bus.send(can_data, id=identifier, timeout=0, rtr=False, extframe=True)
            buf = self.read(register, data)
            if _COMMON_REG[register][1] == 0x12:
                if (can_data[4:8], _COMMON_REG[register][3]) == buf:
                    return (can_data[4:8]) == buf
            elif _COMMON_REG[register][1] == 0x0B:
                return data == buf
            else:
                return True
        except Exception as e:
            print(f"Error in write: {e}")
            return False

    def read_response(self):
        """! Read the response data from the CAN bus.

        @return: Processed response data depending on command type.
        """
        receive_data = self._can_bus.recv(0, timeout=200)
        cmd_id = (receive_data[0] >> 24) & 0x1F  # 24~28 bit
        if cmd_id == 0x02:
            print("Feedback data")
            error_info = (receive_data[0] >> 16) & 0x07
            over_range = (receive_data[0] >> 18) & 0x01
            jam_motor = (receive_data[0] >> 17) & 0x01
            over_voltage = (receive_data[0] >> 16) & 0x01
            print(
                f"Error Info: {error_info}, Over Range: {over_range}, Jam Motor: {jam_motor}, Over Voltage: {over_voltage}"
            )
            self.error_code = error_info
        elif cmd_id == 0x0B:
            print("CAN BPS")
            can_bps = (receive_data[0] >> 16) & 0xFF  # 16~23bit
            print(f"CAN BPS:{can_bps}")
        elif cmd_id == 0x15:
            print("I2C Read")
            is_read_success = (receive_data[0] >> 16) & 0x01
            print(f"Read Success: {is_read_success}")
            print(f"Raw Data: 0x{receive_data[4]}")
            print(f"Rec Data: 0x{receive_data[4].hex()}")
            return is_read_success, receive_data[4]
        elif cmd_id == 0x16:
            print("I2C Write")
            is_write_success = (receive_data[0] >> 16) & 0x01
            print(f"Write Success: {is_write_success}")
            return is_write_success

        master_can_id = (receive_data[0] >> 8) & 0xFF  # 8~15 bit
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
        if cmd_id == 0x11:
            return data
        elif cmd_id == 0x00:
            return bytes([master_can_id])
        elif cmd_id == 0x0B:
            return bytes([can_bps])


class RollerCANToI2CBus(RollerCAN):
    def __init__(self, bus, address=_ROLLERCAN_I2C_ADDR, mode=None) -> None:
        """! Initialize RollerCANToI2CBus object with CAN bus and address.

        @param bus: The CAN bus instance.
        @param address: The I2C device address, default is _ROLLERCAN_I2C_ADDR.
        @param mode: Optional mode for setting specific operational mode.
        """
        self._can_bus = bus
        self._can_addr = address  # motor id == address
        self._mode = RollerCANUnit.CAN_TO_I2C_MODE
        self.error_code = 0
        super().__init__(bus, address=address)

    def readfrom_mem(self, addr: int, mem_addr: int, nbytes: int, *args, **kwargs) -> bytes:
        """! Read data from an I2C memory register.

        @param addr: I2C device address.
        @param mem_addr: Memory register address.
        @param nbytes: Number of bytes to read.
        @return: Data read from the specified memory address.
        """
        self.writeto(addr, bytes([mem_addr]), stop=True)
        buf = self.readfrom(addr, nbytes)
        print(f"buf: {buf}")
        return buf

    def readfrom_mem_into(self, addr: int, mem_addr: int, buf: bytearray, *args, **kwargs) -> None:
        """! Read data from an I2C memory register and store it in the provided buffer.

        @param addr: I2C device address.
        @param mem_addr: Memory register address.
        @param buf: Buffer to store the data.
        """
        data = self.readfrom_mem(addr, mem_addr, len(buf))
        buf[: len(data)] = data

    def writeto_mem(
        self, addr: int, mem_addr: int, buf: bytearray, *args, **kwargs
    ) -> Literal[True]:
        """! Write data to an I2C memory register.

        @param addr: I2C device address.
        @param mem_addr: Memory register address.
        @param buf: Data to write.
        @return: True if the write operation was successful.
        """
        print(f"addr: {addr:#04x}, mem_addr: {mem_addr:#04x}, buf: {[hex(b) for b in buf]}")
        return self.writeto(addr, bytes([mem_addr]) + buf, True)

    def readfrom(self, addr: int, nbytes: int, *args, **kwargs) -> bytes:
        """! Read data from an I2C device.

        @param addr: I2C device address.
        @param nbytes: Number of bytes to read.
        @return: Data read from the specified I2C address.
        @raises Exception: If reading fails for any chunk.
        """
        chunk_size = 8
        blocks = (nbytes + chunk_size - 1) // chunk_size
        result = bytearray()
        for block in range(blocks):
            to_read = min(chunk_size, nbytes - block * chunk_size)
            success, output = self.i2c_read(addr, to_read)
            print(f"success: {success}, output: {output}")
            if success:
                result += output[:to_read]
                print(f"result: {result}\n\n")
            else:
                raise Exception(f"Read I2C Slave failed: register {addr:#04x}, nbytes {nbytes}")
        return bytes(result)

    def readfrom_into(self, addr: int, buf: bytearray, *args, **kwargs) -> None:
        """! Read data from an I2C device and store it in the provided buffer.

        @param addr: I2C device address.
        @param buf: Buffer to store the data.
        """
        data = self.readfrom(addr, len(buf))
        buf[: len(data)] = data

    def writeto(self, addr: int, buf: bytes | bytearray, *args, **kwargs) -> Literal[True]:
        """! Write data to an I2C device in chunks.

        @param addr: I2C device address.
        @param buf: Data to write.
        @param stop: Whether to end the transaction with a stop condition.
        @return: True if the write operation was successful.
        """
        total_len = len(buf)
        chunk_size = 7
        stop = args[0] if args else True
        print(f"addr: {addr:#04x}, buf: {[hex(b) for b in buf]}, stop: {stop}")

        for i in range(0, total_len, chunk_size):
            chunk = buf[i : i + chunk_size]
            stop_bit = stop if (i + chunk_size >= total_len) else False
            print(f"chunk: {[hex(b) for b in chunk]}")
            success = self.i2c_write(addr, chunk, stop_bit)
            print(f"success: {success}\n\n")
            if not success:
                print(f"Write to I2C Slave failed for chunk {chunk}")
                # raise Exception(f"Write to I2C Slave failed for chunk {chunk}")
        return True

    def scan(self, *args, **kwargs) -> list:
        """! Scan for I2C devices on the bus.

        @return: List of addresses of detected I2C devices.
        """
        found_devices = []
        for address in range(0x08, 0x77 + 1):
            try:
                if self.i2c_write(address, bytes([0x01]), False):
                    found_devices.append(address)
                    print(f"Found device at address {address:#04x}")
            except OSError:
                pass
        return found_devices


class RollerCANUnit:
    """! A factory class to create Roller instances based on communication mode."""

    I2C_MODE = 0  # I2C mode identifier
    CAN_MODE = 1  # CAN mode identifier
    CAN_TO_I2C_MODE = 2  # CAN to I2C mode identifier

    def __new__(cls, *args, **kwargs) -> RollerBase:
        """! Create a new instance of Roller based on the specified communication mode.

        @param args: Positional arguments to be passed to the Roller class constructors.
        @param kwargs: Keyword arguments, including the 'mode' key to specify the communication mode.

        @return: An instance of RollerBase or one of its subclasses.
        """
        if kwargs["mode"] == cls.I2C_MODE:
            cls.instance = RollerI2C(args[0], **kwargs)
        elif kwargs["mode"] == cls.CAN_MODE:
            cls.instance = RollerCAN(args[0], **kwargs)
        elif kwargs["mode"] == cls.CAN_TO_I2C_MODE:
            cls.instance = RollerCANToI2CBus(args[0], **kwargs)
        else:
            raise ValueError("Invalid mode specified")
        return cls.instance

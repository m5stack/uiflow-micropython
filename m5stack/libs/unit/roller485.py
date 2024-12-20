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
_ROLLER485_I2C_ADDR = const(0x64)
_ROLLER485_RS485_ADDR = const(0x00)

#! 485 VIA I2C CONTROL READ & WRITE !#
_READ_I2C_SLAVE_REG_ADDR = 0x60
_WRITE_I2C_SLAVE_REG_ADDR = 0x61
_READ_I2C_SLAVE_ADDR = 0x62
_WRITE_I2C_SLAVE_ADDR = 0x63

_COMMON_REG = {
    #! "COMMAND": (I2C-REGISTER, RS485-WRITE-REGISTER, RS485-WRITE-POSISTION, RS485-READ-REGISTER, RS485-READ-POSISTION, RS485-REGISTER-CONTINUOUS)
    #! MOTOR CONFIGURATION REGISTER !#
    "MOTOR_OUTPUT": (0x00, 0x00, 2, None, None, 0),
    "MOTOR_MODE": (0x01, 0x01, 2, 0x40, 14, 0),
    "MOTOR_ORP": (0x0A, 0x0E, 2, None, None, 0),
    "STALL_PROTECT": (0x0B, 0x06, 6, None, None, 0),
    "MOTOR_STATUS": (0x0C, None, None, 0x40, 15, 0),
    "MOTOR_ERROR": (0x0D, None, None, 0x40, 16, 0),
    "BTN_SWITCH_MODE": (0x0E, 0x09, 2, 0x43, 16, 0),
    "MOTOR_JAM": (0x0F, 0x0D, 2, None, None, 0),
    "MOTOR_ID": (0x10, 0x0C, 2, 0x43, 14, 0),
    "BPS_RS485": (0x11, 0x0B, 2, 0x43, 15, 0),
    "RGB_BRIGHT": (0x12, 0x0A, 6, 0x41, 15, 2),
    #! SPEED CONTROL REGISTER !#
    "SPEED_SETTING": (0x40, 0x20, 2, None, None, 1),
    "SPEED_MAX_CURRENT": (0x50, 0x20, 6, None, None, 1),
    "SPEED_READBACK": (0x60, None, None, 0x40, 2, 0),
    "SPEED_PID": (0x70, 0x21, 2, 0x42, 2, 0),
    #! POSITION CONTROL REGISTER !#
    "POSITION_SETTING": (0x80, 0x22, 2, None, None, 1),
    "POSITION_MAX_CURRENT": (0x20, 0x22, 6, None, None, 1),
    "POSITION_READBACK": (0x90, None, None, 0x40, 6, 0),
    "POSITION_PID": (0xA0, 0x23, 2, 0x43, 2, 0),
    #! CURRENT CONTROL REGISTER !#
    "MAX_CURRENT": (0xB0, 0x24, 2, None, None, 0),
    "CURRENT_READBACK": (0xC0, None, None, 0x40, 10, 0),
    #! SYSTEM REGISTER !#
    "SYSTEM_RGB": (0x30, 0x0A, 2, 0x42, 14, 2),
    "SYSTEM_RGB_MODE": (0x33, 0x0A, 5, 0x41, 14, 2),
    "SYSTEM_VIN": (0x34, None, None, 0x41, 2, 0),
    "SYSTEM_TEMP": (0x38, None, None, 0x41, 6, 0),
    "SYSTEM_ENCODER": (0x3C, 0x08, 2, 0x41, 10, 0),
    "SYSTEM_FLASH_WRITE": (0xF0, 0x07, 2, None, None, 0),
    "SYSTEM_FIRMWARE": (0xFE, None, None, None, None, 0),
    "SYSTEM_ADDRESS": (0xFF, None, None, None, None, 0),
}


class RollerBase:
    #! Initialize the roller485Base.
    def __init__(self) -> None:
        pass

    def read(self, register, length) -> bytes:
        raise NotImplementedError("Subclasses should implement this method!")

    def write(self, register, data: bytes) -> None:
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
        self.write("STALL_PROTECT", bytes([0x01]))

    def get_motor_status(self) -> int:
        """! Get the motor status.

        @return: The current status of the motor.
        """
        return self.read("MOTOR_STATUS", 1)[0]

    def get_motor_error_code(self) -> int:
        """! Get the motor error code.

        @return: The current error code of the motor.
        """
        return self.read("MOTOR_ERROR", 1)[0]

    def set_button_change_mode(self, state: int = 1) -> None:
        """! Set the button change mode.

        @param state: Change mode state value (1 to enable, 0 to disable).
        """
        self.write("BTN_SWITCH_MODE", bytes([state]))

    def get_button_change_mode(self) -> int:
        """! Get the button change mode.

        @return: The current button change mode value.
        """
        return self.read("BTN_SWITCH_MODE", 1)[0]

    def set_motor_jam_protect_state(self, state: int = 1) -> None:
        """! Set the motor jam protection enable/disable.

        @param state: Protection state value (1 to enable, 0 to disable).
        """
        self.write("MOTOR_JAM", bytes([state]))

    def get_motor_jam_protect_state(self) -> bool:
        """! Get the motor jam protection status.

        @return: True if jam protection is enabled, False otherwise.
        """
        return self.read("MOTOR_JAM", 1)[0] != 0

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
        self.write("BPS_RS485", bytes([bps]))

    def get_485_baudrate(self) -> int:
        """! Get the 485 baudrate.

        @return: The current 485 baudrate.
        """
        return self.read("BPS_RS485", 1)[0]

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
                self.write("SYSTEM_ADDRESS", struct.pack("B", addr))
                self._i2c_addr = addr
            time.sleep_ms(200)

    def get_i2c_address(self) -> int:
        """! Get the current I2C address.

        @return: The current I2C address.
        """
        return self.read("SYSTEM_ADDRESS", 1)[0]


class RollerI2C(RollerBase):
    def __init__(
        self, i2c: I2C | PAHUBUnit, address: int = _ROLLER485_I2C_ADDR, mode=None
    ) -> None:
        """! Initialize the RollerI2C object.

        @param i2c: I2C bus instance or PAHUBUnit instance.
        @param address: I2C address of the device. Defaults to _ROLLER485_I2C_ADDR.
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


class Roller485(RollerBase):
    def __init__(self, bus, address=_ROLLER485_RS485_ADDR, mode=None) -> None:
        """! Initialize the Roller485 object.

        @param bus: The RS485 bus instance.
        @param address: The motor's RS485 address. Defaults to _ROLLER485_RS485_ADDR.
        """
        self._rs485_bus = bus
        self._rs485_addr = address  # motor id == address
        super().__init__()
        self._obuffer = bytearray(15)  # Output buffer for sending commands.
        self._ibuffer = bytearray(17)  # Input buffer for receiving responses.
        self.setting_buf = [0] * 8  # Buffer for storing settings.
        self.rgb_buf = [0] * 8  # Buffer for storing RGB data.

    def read(self, register, length):
        """! Read data from a specified register via RS485.

        @param register: The name of the register to read from.
        @param length: The number of bytes to read.
        @return: The data read from the device.
        """
        self.send_command(_COMMON_REG[register][3], self._rs485_addr, 0, buf_len=4)
        success, output = self.read_response(_COMMON_REG[register][3], self._rs485_addr)
        if success:
            return output[_COMMON_REG[register][4] : (_COMMON_REG[register][4] + length)]

    def create_frame(self, cmd, motor_id, *datas) -> None:
        """! Create a command frame with the given command and motor ID.

        @param cmd: The command byte.
        @param motor_id: The ID of the motor.
        @param datas: Additional data bytes to include in the frame.
        """
        struct.pack_into(">B", self._obuffer, 0, cmd)
        struct.pack_into(">B", self._obuffer, 1, motor_id)
        for i, data in enumerate(datas):
            struct.pack_into(">B", self._obuffer, 2 + i, data)

    def write(self, register, bytes) -> bool:
        """! Write data to a specified register via RS485.

        @param register: The name of the register to write to.
        @param bytes: The data to write to the register as a bytes object.
        @return: The response after writing the data.
        """
        if _COMMON_REG[register][5]:
            data_buf = [0] * len(bytes) * 2
            if _COMMON_REG[register][5] == 1:
                self.setting_buf[
                    (_COMMON_REG[register][2] - 2) : (_COMMON_REG[register][2] - 2 + len(bytes))
                ] = [int(b) for b in bytes]
                data_buf = self.setting_buf
            else:
                self.rgb_buf[
                    (_COMMON_REG[register][2] - 2) : (_COMMON_REG[register][2] - 2 + len(bytes))
                ] = [int(b) for b in bytes]
                data_buf = self.rgb_buf
        else:
            data_buf = [0] * len(bytes)

        data_buf[(_COMMON_REG[register][2] - 2) : (_COMMON_REG[register][2] - 2 + len(bytes))] = [
            int(b) for b in bytes
        ]
        self.send_command(_COMMON_REG[register][1], self._rs485_addr, data_buf, buf_len=15)
        return self.read_response(_COMMON_REG[register][1], self._rs485_addr)[0]

    def send_command(self, cmd, id, data, buf_len=15) -> None:
        """! Send a command via RS485.

        @param cmd: The command byte.
        @param id: The motor ID.
        @param data: The data to send along with the command.
        @param buf_len: The length of the buffer.
        """
        cmd_buf = [0] * buf_len
        cmd_buf[0] = cmd
        cmd_buf[1] = id
        if isinstance(data, int):
            data = [data]
        cmd_buf[2 : (2 + len(data))] = data
        cmd_buf[-1] = self._crc8(cmd_buf[:-1])
        self._rs485_bus.write(bytes(cmd_buf))

    def read_response(self, cmd, id):
        """! Read the response from the RS485 bus.

        @param cmd: The command byte.
        @param id: The motor ID.
        @return: A tuple (success, response). Success is True if the response is valid, and response is the data read.
        """
        # 根据 cmd 确定响应包的长度
        cmd += 0x10  # Write cmd+10 = response cmd
        if cmd in [
            0x10,
            0x11,
            0x16,
            0x17,
            0x18,
            0x19,
            0x1A,
            0x1B,
            0x1C,
            0x1D,
            0x1E,
        ] or cmd in range(0x30, 0x35):
            expected_length = 15 + 2
        elif cmd in range(0x50, 0x54):  # cmd 0x50~0x53
            expected_length = 18 + 2
        elif cmd in [0x70, 0x72]:  # cmd 0x70 和 0x72
            expected_length = 25 + 2
        elif cmd in [0x71, 0x73]:  # cmd 0x71 和 0x73
            expected_length = 4 + 2
        else:
            print(f"Unsupported cmd: {cmd:#04x}")
            return (False, 0)  # 返回失败状态

        time_out = time.ticks_ms() + 500
        resp_buf = bytearray()  # 用于存储拼接的响应数据
        while time_out > time.ticks_ms():
            if self._rs485_bus.any():
                new_data = self._rs485_bus.read()
                resp_buf.extend(new_data)  # 将新读到的数据拼接到 resp_buf
                # print(f"Response RAW: {[hex(byte) for byte in resp_buf]}")
                if len(resp_buf) < expected_length:  # 检查当前已接收到的长度是否满足预期
                    # print(f"Partial response received, current length: {len(resp_buf)}")
                    continue
                if len(resp_buf) != expected_length:  # 如果数据多于预期，打印并继续处理
                    print(
                        f"Unexpected response length: {len(resp_buf)}, expected: {expected_length}"
                    )
                    resp_buf[:] = b""  # 清除当前数据，重新接收
                    continue
                if resp_buf[0:2] == b"\xaa\x55":  # 检查包头
                    if resp_buf[2:4] == bytes([(cmd), id]):
                        if self._crc8(resp_buf[2:-1]) == resp_buf[-1]:
                            # print(f"Response: {[hex(byte) for byte in resp_buf]}")
                            return (True, resp_buf[2:-1])
            time.sleep_ms(100)
        return (False, 0)

    def _crc8(self, buffer) -> int:
        """! Calculate CRC8 checksum.

        @param buffer: The data buffer to compute the checksum for.
        @return: The computed CRC8 value.
        """
        crc = 0x00
        for byte in buffer:
            crc ^= byte
            for _ in range(8):
                if crc & 0x01:
                    crc = (crc >> 1) ^ 0x8C
                else:
                    crc = crc >> 1
        return crc & 0xFF  # return the bottom 8 bits


class Roller485ToI2CBus(Roller485):
    def __init__(self, bus, address=_ROLLER485_RS485_ADDR, mode=None) -> None:
        """! Initialize the Roller485ToI2CBus object.

        @param bus: The RS485 bus instance.
        @param address: The motor's RS485 address. Defaults to _ROLLER485_RS485_ADDR.
        """
        self._rs485_bus = bus
        self._rs485_addr = address  # Motor ID == address
        super().__init__(bus, address=address)

    def readfrom_mem(self, addr: int, mem_addr: int, nbytes: int) -> bytes:  # 0x60
        """Read data from the I2C memory register."""
        chunk_size = 16  # 设置一次最多读取16字节
        byte_len = 2 if mem_addr > 0xFF else 1  # 根据寄存器地址长度确定字节数
        result = bytearray()
        blocks = (nbytes + chunk_size - 1) // chunk_size  # 计算需要的块数

        for block in range(blocks):
            to_read = min(chunk_size, nbytes - block * chunk_size)  # 本次读取的字节数
            if byte_len == 1:
                data = [addr, 0, mem_addr + block * chunk_size, 0, to_read]
            else:
                data = [
                    addr,
                    1,
                    mem_addr + block * chunk_size,
                    (mem_addr + block * chunk_size) >> 8,
                    to_read,
                ]
            self.send_command(_READ_I2C_SLAVE_REG_ADDR, self._rs485_addr, data, buf_len=8)
            success, output = self.read_response(_READ_I2C_SLAVE_REG_ADDR, self._rs485_addr)
            if success and output[2]:
                result += output[8 : 8 + to_read]
            else:
                raise Exception(
                    f"Read I2C Slave Memory Register failed: register {mem_addr:#04x}, nbytes {nbytes}"
                )
        return bytes(result)

    def readfrom_mem_into(self, addr: int, mem_addr: int, buf: bytearray) -> None:
        """! Read data from the I2C memory register and store it in the provided buffer.

        @param addr: I2C device address.
        @param mem_addr: Memory register address.
        @param buf: Buffer to store the data.
        """
        data = self.readfrom_mem(addr, mem_addr, len(buf))
        buf[: len(data)] = data

    def writeto_mem(self, addr: int, mem_addr: int, buf) -> Literal[True]:  # 0x61
        """Write data to the I2C memory register in chunks."""
        # print(f"addr: {addr:#04x}, mem_addr: {mem_addr:#04x}, buf: {buf}")
        byte_len = 2 if mem_addr > 0xFF else 1
        total_len = len(buf)
        chunk_size = 16
        for i in range(0, total_len, chunk_size):
            chunk = buf[i : i + chunk_size]
            data_len = len(chunk)
            if byte_len == 1:
                data = [addr, 0, mem_addr + i, 0, data_len, 0]
            else:
                data = [addr, 1, mem_addr + i, (mem_addr + i) >> 8, data_len, 0]
            data += chunk
            self.send_command(_WRITE_I2C_SLAVE_REG_ADDR, self._rs485_addr, data, buf_len=25)
            success, output = self.read_response(_WRITE_I2C_SLAVE_REG_ADDR, self._rs485_addr)
            if not (success and output[2]):
                raise Exception(
                    f"Write to I2C Memory Register failed: register {mem_addr:#04x}, chunk {chunk}"
                )
        return True

    def readfrom(self, addr: int, nbytes: int) -> bytes:
        """Read data from the I2C slave."""
        chunk_size = 16
        blocks = (nbytes + chunk_size - 1) // chunk_size  # 计算需要多少块
        result = bytearray()
        for block in range(blocks):
            to_read: int = min(chunk_size, nbytes - block * chunk_size)
            self.send_command(_READ_I2C_SLAVE_ADDR, self._rs485_addr, [addr, to_read], buf_len=5)
            success, output = self.read_response(_READ_I2C_SLAVE_ADDR, self._rs485_addr)
            if success and output[2]:
                result += output[8 : 8 + to_read]
            else:
                raise Exception(f"Read I2C Slave failed: register {addr:#04x}, nbytes {nbytes}")
        return bytes(result)

    def readfrom_into(self, addr: int, buf: bytearray) -> None:  # 0x62
        """! Read data from the I2C device and store it in the provided buffer.

        @param addr: I2C device address.
        @param buf: Buffer to store the data.
        """
        data = self.readfrom(addr, len(buf))
        buf[: len(data)] = data

    def writeto(self, addr: int, buf: bytes | bytearray, stop: bool = True) -> Literal[True]:
        """Write data to the I2C slave in chunks."""
        total_len = len(buf)
        chunk_size = 16

        for i in range(0, total_len, chunk_size):
            chunk = buf[i : i + chunk_size]
            data_len = len(chunk)
            stop_bit = stop if i + chunk_size >= total_len else False
            data = [addr, data_len, stop_bit, 0, 0, 0] + list(chunk)
            self.send_command(_WRITE_I2C_SLAVE_ADDR, self._rs485_addr, data, buf_len=25)
            success, output = self.read_response(_WRITE_I2C_SLAVE_ADDR, self._rs485_addr)
            if not (success and output[2]):
                raise Exception(f"Write to I2C Slave failed for chunk {chunk}")
        return True

    def _writeto(self, addr: int, buf: bytes | bytearray, stop: bool = True):
        data_len = len(buf)
        data = [addr, data_len, stop, 0, 0, 0] + list(buf)
        self.send_command(_WRITE_I2C_SLAVE_ADDR, self._rs485_addr, data, buf_len=25)
        success, output = self.read_response(_WRITE_I2C_SLAVE_ADDR, self._rs485_addr)
        if success and output[2]:
            return True

    def scan(self) -> list:
        """! Scan for I2C devices on the bus.

        @return: A list of addresses of the found I2C devices.
        """
        found_devices = []
        for address in range(0x08, 0x77 + 1):
            try:
                if self._writeto(address, bytes(0x01), stop=False):
                    found_devices.append(address)
                    # print(f"Found device at address {address:#04x}")
            except OSError:
                pass
        return found_devices


class Roller485Unit:
    """! A factory class to create Roller instances based on communication mode."""

    I2C_MODE = 0  # I2C mode identifier
    RS485_MODE = 1  # RS485 mode identifier
    RS485_TO_I2C_MODE = 2  # RS485 to I2C mode identifier

    def __new__(cls, *args, **kwargs) -> RollerBase:
        """! Create a new instance of Roller based on the specified communication mode.

        @param args: Positional arguments to be passed to the Roller class constructors.
        @param kwargs: Keyword arguments, including the 'mode' key to specify the communication mode.

        @return: An instance of RollerBase or one of its subclasses.
        """
        if kwargs["mode"] == cls.I2C_MODE:
            cls.instance = RollerI2C(args[0], **kwargs)
        elif kwargs["mode"] == cls.RS485_MODE:
            cls.instance = Roller485(args[0], **kwargs)
        elif kwargs["mode"] == cls.RS485_TO_I2C_MODE:
            cls.instance = Roller485ToI2CBus(args[0], **kwargs)
        else:
            raise ValueError("Invalid mode specified")
        return cls.instance

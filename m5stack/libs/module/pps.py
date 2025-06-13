# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Import necessary libraries
from . import mbus
from .module_helper import ModuleError
import struct


class PPSModule:
    """! Programmable Power Supply (PPS), supports output up to 30V 5A.

    @en The Programmable Power Supply (PPS), capable of providing an output up to 30V and 5A. It allows for precise control over the output voltage and current, with features to read back the actual output values and the module's status.
    @cn 可编程电源供应器（PPS），能够提供最高30V和5A的输出。它允许对输出电压和电流进行精确控制，并具有读回实际输出值和模块状态的功能。

    @attr OUT_DISABLED PPS output is disabled.
    @attr OUT_CV_MODE PPS output is in constant voltage mode.
    @attr OUT_CC_MODE PPS output is in constant current mode.
    @color #0FE6D7
    @link https://docs.m5stack.com/en/module/pps
    @image https://static-cdn.m5stack.com/resource/docs/products/module/pps/pps_01.webp

    @init
        from module import PPS
                pps = PPS(addr=0x35)

    @test
                pps.set_output_voltage(5.5)
                pps.set_output_current(1)
                pps.set_output(True)
                pps.read_psu_running_mode()
                pps.read_output_current()
                pps.read_output_voltage()
                pps.read_input_voltage()
                pps.read_data_update_flag()
                pps.read_mcu_temperature()
                pps.read_module_id()
                pps.read_uid()

    """

    OUT_DISABLED = 0
    OUT_CV_MODE = 1
    OUT_CC_MODE = 2

    def __init__(self, address=0x35):
        """! Initialize the PPS.

        @param port I2C port to use.
        @param addr I2C address of the device.
        """

        self.i2c = mbus.i2c1
        self.addr = address

        # Check if the devices are connected and accessible
        self._available()

    def _available(self):
        """! Check if PPS is available on the I2C bus.

        Raises:
            Exception: If the PPS device is not found.
        """
        if self.addr not in self.i2c.scan():
            raise ModuleError("PPS Module not found.")

    def set_output(self, enable: bool):
        """Enable or disable the PPS module output.

        @en Set the output mode of %1 to %2.
        @cn 设置%1的输出模式%2。

        @param enable True to enable, False to disable.
        """
        data = 0x01 if enable else 0x00
        self.i2c.writeto_mem(self.addr, 0x04, struct.pack("B", data))

    def enable_output(self):
        """Enable the PPS module output.

        @en Enable the output of %1.
        @cn 启用%1的输出。
        """
        self.set_output(True)

    def disable_output(self):
        """Disable the PPS module output.

        @en Disable the output of %1.
        @cn 禁用%1的输出。
        """
        self.set_output(False)

    def set_output_voltage(self, voltage: float):
        """Set the output voltage of the PPS.

        @en Set the output voltage of %1 to %2 V.
        @cn 将%1的输出电压设置为%2 V。

        @param voltage: float, Desired output voltage in volts, range 0 to 30.0.
        """
        if not 0.0 <= voltage <= 30.0:
            raise ValueError("Voltage must be between 0.0 and 30.0 volts")

        # Pack the floating point voltage value into 4 bytes
        data = struct.pack("<f", voltage)

        # Write the 4-byte data to the PPS device starting at address 0x18
        self.i2c.writeto_mem(self.addr, 0x18, data)

    def set_output_current(self, current: float):
        """Set the output current of the PPS.

        @en Set the output current of %1 to %2 A.
        @cn 将%1的输出电流设置为%2 A。

        @param current Desired output current, from 0.0A to 5.0A.
        """
        if not 0.0 <= current <= 5.0:
            raise ValueError("Current must be between 0.0 and 5.0A")
        # 将浮点数电流值打包成4字节数据
        data = struct.pack("<f", current)
        self.i2c.writeto_mem(self.addr, 0x1C, data)

    def read_psu_running_mode(self) -> int:
        """Read the PSU running mode.

        @en Read the PSU running mode of %1.
        @cn 读取%1的PSU运行模式。

        Returns:
            int: The current running mode of the PSU. One of OUT_DISABLED, OUT_CV_MODE, or OUT_CC_MODE.
        """
        mode = self.i2c.readfrom_mem(self.addr, 0x05, 1)
        return struct.unpack("B", mode)[0]

    def read_output_current(self) -> float:
        """Read the output current.

        @en Read the output current of %1.
        @cn 读取%1的输出电流。

        Returns:
            float: The current output current in Amperes.
        """
        current = self.i2c.readfrom_mem(self.addr, 0x0C, 4)
        return struct.unpack("<f", current)[0]

    def read_output_voltage(self) -> float:
        """Read the output voltage.

        @en Read the output voltage of %1.
        @cn 读取%1的输出电压。

        Returns:
            float: The current output voltage in Volts.
        """
        voltage = self.i2c.readfrom_mem(self.addr, 0x08, 4)
        return struct.unpack("<f", voltage)[0]

    def read_input_voltage(self) -> float:
        """Read the input voltage.

        @en Read the input voltage of %1.
        @cn 读取%1的输入电压。

        Returns:
            float: The current input voltage in Volts.
        """
        voltage = self.i2c.readfrom_mem(self.addr, 0x14, 4)
        return struct.unpack("<f", voltage)[0]

    def read_data_update_flag(self) -> int:
        """Read the data update flag. When the PSU data is updated, this value will increase by 1.

        @en Read the data update flag of %1.
        @cn 读取%1的数据更新标志。

        Returns:
            int: The data update flag value.
        """
        flag = self.i2c.readfrom_mem(self.addr, 0x07, 1)
        return struct.unpack("B", flag)[0]

    def read_mcu_temperature(self) -> float:
        """Read the MCU temperature.

        @en Read the MCU temperature of %1.
        @cn 读取%1的MCU温度。

        Returns:
            float: The current MCU temperature in degrees Celsius.
        """
        temperature = self.i2c.readfrom_mem(self.addr, 0x10, 4)
        return struct.unpack("<f", temperature)[0]

    def read_module_id(self) -> int:
        """Read the module ID.

        @en Read the module ID of %1.
        @cn 读取%1的模块ID。

        Returns:
            int: The module ID as an unsigned 16-bit integer.
        """
        module_id = self.i2c.readfrom_mem(self.addr, 0x00, 2)
        return struct.unpack("<H", module_id)[0]

    def read_uid(self) -> bytearray:
        """!
        @en Read the unique identifier (UID) of %1.
        @cn 读取%1的唯一标识符（UID）。

        Returns:
            bytearray: The UID as a bytearray.
        """
        uid_data = self.i2c.readfrom_mem(self.addr, 0x52, 12)
        return bytearray(uid_data)

    def get_i2c_address(self) -> int:
        """Get the current I2C address of the device.

        @en Get the current I2C address of %1.
        @cn 获取%1的当前I2C地址。

        Returns:
            int: The current I2C address.
        """
        address = self.i2c.readfrom_mem(self.addr, 0x5F, 1)
        return struct.unpack("B", address)[0]

    def set_i2c_address(self, new_address: int):
        """Set a new I2C address for the device.

        @en Set a new I2C address for %1.
        @cn 为%1设置新的I2C地址。

        @param new_address: The new I2C address to set.
        """
        self.i2c.writeto_mem(self.addr, 0x5F, struct.pack("B", new_address))

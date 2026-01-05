# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .chain import ChainBus
from .key import KeyChain
import struct


class BusChainUnit(KeyChain):
    """Bus Chain Unit class for interacting with Bus devices over Chain bus.

    :param ChainBus bus: The Chain bus instance.
    :param int device_id: The device ID of the Bus device on the Chain bus.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from chain import ChainBus
            from chain import BusChainUnit

            chainbus_0 = ChainBus(2, 32, 33, verbose=True)
            bus_chain_unit_0 = BusChainUnit(chainbus_0, 1)
    """

    # Device commands
    CMD_BUS_WORK_STATUS = 0x70

    # GPIO commands
    CMD_BUS_GPIO_OUTPUT = 0x30  # 设置为 GPIO 输出模式
    CMD_BUS_GPIO_OUTPUT_LEVEL = 0x31  # 设置 GPIO 输出电平
    CMD_BUS_GPIO_INPUT = 0x40  # 设置为 GPIO 输入模式
    CMD_BUS_GPIO_INPUT_LEVEL = 0x41  # 获取 GPIO 输入电平

    # GPIO external interrupt commands
    CMD_BUS_GPIO_EXIT = 0x50  # 设置为 GPIO 外部中断模式
    CMD_BUS_GPIO_EXIT_NOTIFY = 0xE0  # 外部中断事件通知

    # I2C commands
    CMD_BUS_I2C_INIT = 0x10  # 设置为 I2C 模式
    CMD_BUS_I2C_READ = 0x11  # I2C 读
    CMD_BUS_I2C_WRITE = 0x12  # I2C 写
    CMD_BUS_I2C_READ_MEM = 0x13  # I2C 指定地址读
    CMD_BUS_I2C_WRITE_MEM = 0x14  # I2C 指定地址写
    CMD_BUS_I2C_SCAN = 0x15  # I2C 设备扫描

    # ADC commands
    CMD_BUS_ADC_CONFIG = 0x60  # 设置为 ADC 模式
    CMD_BUS_ADC_READ = 0x61  # ADC 读

    # GPIO mode constants
    GPIO_MODE_PUSHPULL = 0  # 推挽输出模式
    GPIO_MODE_OPENDRAIN = 1  # 开漏输出模式
    # GPIO pull-up/down constants
    GPIO_PULL_UP = 0  # 上拉
    GPIO_PULL_DOWN = 1  # 下拉
    GPIO_PULL_NONE = 2  # 无上拉/下拉
    # GPIO interrupt trigger mode constants
    GPIO_INTR_RISING = 0  # 上升沿触发
    GPIO_INTR_FALLING = 1  # 下降沿触发
    GPIO_INTR_ANYEDGE = 2  # 双边沿触发

    # I2C speed constants
    I2C_SPEED_100K = 0  # 100 KHz
    I2C_SPEED_400K = 1  # 400 KHz

    # Work mode constants
    WORK_MODE_UNCONFIGURED = 0  # 未配置
    WORK_MODE_GPIO_OUTPUT = 1  # GPIO 输出
    WORK_MODE_GPIO_INPUT = 2  # GPIO 输入
    WORK_MODE_EXIT = 3  # 外部中断
    WORK_MODE_ADC = 4  # ADC
    WORK_MODE_I2C = 5  # I2C

    def __init__(self, bus: ChainBus, device_id: int):
        super().__init__(bus, device_id)

    # ============================================================================
    # 设备功能
    # ============================================================================
    def get_work_mode(self, gpio: int) -> int | None:
        """Get the Unit ChainBus work mode.

        Returns the work mode of the specified GPIO pin.

        Work mode values:
            - :attr:`BusChainUnit.WORK_MODE_UNCONFIGURED`
            - :attr:`BusChainUnit.WORK_MODE_GPIO_OUTPUT`
            - :attr:`BusChainUnit.WORK_MODE_GPIO_INPUT`
            - :attr:`BusChainUnit.WORK_MODE_EXIT`
            - :attr:`BusChainUnit.WORK_MODE_ADC`
            - :attr:`BusChainUnit.WORK_MODE_I2C`

        :param int gpio: GPIO number (1 or 2).
        :return: Work mode value, or None if failed.
        :rtype: int | None

        UiFlow2 Code Block:

            |get_work_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = unit_chain_bus.get_work_mode(1)
                if mode == BusChainUnit.WORK_MODE_GPIO_OUTPUT:
                    print("GPIO1 is configured as output")
        """
        if gpio not in (1, 2):
            return None

        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_WORK_STATUS, bytes())
        if state:
            if len(response) >= 2:
                if gpio == 1:
                    return response[0]
                else:  # gpio == 2
                    return response[1]
        return None

    # ============================================================================
    # GPIO mode
    # ============================================================================
    def set_gpio_output(self, gpio: int, mode: int, pull: int = 2) -> bool:
        """Set pin as output.

        :param int gpio: GPIO number (1 or 2).
        :param int mode: Output mode. Use :attr:`BusChainUnit.GPIO_MODE_PUSHPULL` (0) or :attr:`BusChainUnit.GPIO_MODE_OPENDRAIN` (1).
        :param int pull: Pull-up/down configuration. Use :attr:`BusChainUnit.GPIO_PULL_UP` (0), :attr:`BusChainUnit.GPIO_PULL_DOWN` (1), or :attr:`BusChainUnit.GPIO_PULL_NONE` (2). Default is :attr:`BusChainUnit.GPIO_PULL_NONE` (2).
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_gpio_output.png|

        MicroPython Code Block:

            .. code-block:: python

                success = unit_chain_bus.set_gpio_output(1, BusChainUnit.GPIO_MODE_PUSHPULL, BusChainUnit.GPIO_PULL_UP)
        """
        if gpio not in (1, 2):
            return False
        if mode not in (0, 1):
            return False
        if pull not in (0, 1, 2):
            return False

        payload = struct.pack("<BBB", gpio & 0xFF, mode & 0xFF, pull & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_GPIO_OUTPUT, payload)
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def set_gpio_output_value(self, gpio: int, value: int) -> bool:
        """Set GPIO output value.

        :param int gpio: GPIO number (1 or 2).
        :param int value: Output value. 0 for low level, 1 for high level.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_gpio_output_value.png|

        MicroPython Code Block:

            .. code-block:: python

                success = unit_chain_bus.set_gpio_output_value(1, 1)  # Set GPIO1 to high level
        """
        if gpio not in (1, 2):
            return False
        if value not in (0, 1):
            return False

        payload = struct.pack("<BB", gpio & 0xFF, value & 0xFF)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_BUS_GPIO_OUTPUT_LEVEL, payload
        )
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def set_gpio_input(self, gpio: int, pull: int) -> bool:
        """Set GPIO input mode configuration.

        :param int gpio: GPIO number (1 or 2).
        :param int pull: Pull-up/down configuration. Use :attr:`BusChainUnit.GPIO_PULL_UP` (0), :attr:`BusChainUnit.GPIO_PULL_DOWN` (1), or :attr:`BusChainUnit.GPIO_PULL_NONE` (2).
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_gpio_input.png|

        MicroPython Code Block:

            .. code-block:: python

                success = unit_chain_bus.set_gpio_input(1, BusChainUnit.GPIO_PULL_UP)
        """
        if gpio not in (1, 2):
            return False
        if pull not in (0, 1, 2):
            return False

        payload = struct.pack("<BB", gpio & 0xFF, pull & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_GPIO_INPUT, payload)
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def get_gpio_input_value(self, gpio: int) -> int | None:
        """Get GPIO input value.

        :param int gpio: GPIO number (1 or 2).
        :return: GPIO value. 0 for low level, 1 for high level. Returns None if failed.
        :rtype: int | None

        UiFlow2 Code Block:

            |get_gpio_input_value.png|

        MicroPython Code Block:

            .. code-block:: python

                value = unit_chain_bus.get_gpio_input_value(1)
                if value == 1:
                    print("GPIO1 is high")
        """
        if gpio not in (1, 2):
            return None

        payload = struct.pack("<B", gpio & 0xFF)
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_BUS_GPIO_INPUT_LEVEL, payload
        )
        if state:
            if len(response) >= 2:
                if response[0] == 1:
                    return response[1]
        return None

    def set_gpio_exit(self, gpio: int, pull: int, trigger_mode: int) -> bool:
        """Set pin as external interrupt input mode.

        :param int gpio: GPIO number (1 or 2).
        :param int pull: Pull-up/down configuration. Use :attr:`BusChainUnit.GPIO_PULL_UP` (0), :attr:`BusChainUnit.GPIO_PULL_DOWN` (1), or :attr:`BusChainUnit.GPIO_PULL_NONE` (2).
        :param int trigger_mode: Trigger mode. Use :attr:`BusChainUnit.GPIO_INTR_RISING` (0), :attr:`BusChainUnit.GPIO_INTR_FALLING` (1), or :attr:`BusChainUnit.GPIO_INTR_ANYEDGE` (2).
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_gpio_exit.png|

        MicroPython Code Block:

            .. code-block:: python

                success = unit_chain_bus.set_gpio_exit(1, BusChainUnit.GPIO_PULL_UP, BusChainUnit.GPIO_INTR_RISING)
        """
        if gpio not in (1, 2):
            return False
        if pull not in (0, 1, 2):
            return False
        if trigger_mode not in (0, 1, 2):
            return False

        payload = struct.pack("<BBB", gpio & 0xFF, pull & 0xFF, trigger_mode & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_GPIO_EXIT, payload)
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def set_gpio_exit_callback(self, gpio_num: int, trigger_mode: int, callback) -> None:
        """Set GPIO external interrupt callback.

        :param int gpio_num: GPIO number (1 or 2).
        :param int trigger_mode: Trigger mode. Use :attr:`BusChainUnit.GPIO_INTR_RISING` (0) for rising edge or :attr:`BusChainUnit.GPIO_INTR_FALLING` (1) for falling edge.
        :param callback: Callback function.

        UiFlow2 Code Block:

            |set_gpio_exit_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def gpio_exit_callback(args):
                    print("GPIO external interrupt")

                unit_chain_bus.set_gpio_exit_callback(1, BusChainUnit.GPIO_INTR_RISING, gpio_exit_callback)
        """
        if trigger_mode not in (0, 1, 2):
            return
        if gpio_num not in (1, 2):
            return
        payload = struct.pack("<BB", trigger_mode & 0xFF, gpio_num & 0xFF)
        self.bus.register_event(self, self.CMD_BUS_GPIO_EXIT_NOTIFY, payload, callback)

    # ============================================================================
    # ADC mode
    # ============================================================================
    def set_adc(self, channel: int) -> bool:
        """Set ADC channel.

        :param int channel: ADC channel number (1 or 2), corresponding to GPIO1 or GPIO2.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_adc.png|

        MicroPython Code Block:

            .. code-block:: python

                success = unit_chain_bus.set_adc(1)
        """
        if channel not in (1, 2):
            return False

        payload = struct.pack("<B", channel & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_ADC_CONFIG, payload)
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    def get_adc_input(self, channel: int) -> int | None:
        """Read ADC value.

        :param int channel: ADC channel number (1 or 2).
        :return: ADC value (0-4095), or None if failed.
        :rtype: int | None

        UiFlow2 Code Block:

            |get_adc_input.png|

        MicroPython Code Block:

            .. code-block:: python

                value = unit_chain_bus.get_adc_input(1)
        """
        if channel not in (1, 2):
            return None

        payload = struct.pack("<B", channel & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_ADC_READ, payload)
        if state:
            if len(response) >= 3:
                if response[0] == 1:  # Success
                    # ADC value is little-endian (low byte first)
                    return response[1] | (response[2] << 8)
        return None

    # ============================================================================
    # I2C mode
    # ============================================================================
    def set_i2c(self, speed: int = 0) -> bool:
        """Set I2C mode.

        :param int speed: I2C speed. Use :attr:`BusChainUnit.I2C_SPEED_100K` (0) or :attr:`BusChainUnit.I2C_SPEED_400K` (1). Default: 0.
        :return: True if the operation was successful, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |set_i2c.png|

        MicroPython Code Block:

            .. code-block:: python

                success = unit_chain_bus.set_i2c(BusChainUnit.I2C_SPEED_400K)
        """
        if speed not in (0, 1):
            speed = 0

        payload = struct.pack("<B", speed & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_I2C_INIT, payload)
        if state:
            if len(response) >= 1:
                return response[0] == 1
        return False

    # ============================================================================
    # I2C operations
    # ============================================================================
    def readfrom(self, addr: int, nbytes: int, stop: bool = True) -> bytes:
        """Read data from an I2C device.

        :param int addr: I2C device address (7-bit).
        :param int nbytes: Number of bytes to read (max 64).
        :param bool stop: Generate stop condition (ignored, kept for compatibility).
        :return: Read data as bytes.
        :rtype: bytes

        UiFlow2 Code Block:

            |readfrom.png|

        MicroPython Code Block:

            .. code-block:: python

                data = unit_chain_bus.readfrom(0x48, 4)
        """
        if nbytes <= 0 or nbytes > 64:
            return b""

        payload = struct.pack("<BB", addr & 0xFF, nbytes & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_I2C_READ, payload)
        if state:
            if len(response) >= 1:
                if response[0] == 1:  # Success
                    data_len = len(response) - 1
                    if data_len > nbytes:
                        data_len = nbytes
                    return bytes(response[1 : 1 + data_len])
        return b""

    def readfrom_into(self, addr: int, buf: bytearray, stop: bool = True) -> None:
        """Read data from an I2C device into a buffer.

        :param int addr: I2C device address (7-bit).
        :param bytearray buf: Buffer to read into.
        :param bool stop: Generate stop condition (ignored, kept for compatibility).

        UiFlow2 Code Block:

            |readfrom_into.png|

        MicroPython Code Block:

            .. code-block:: python

                buf = bytearray(4)
                unit_chain_bus.readfrom_into(0x48, buf)
        """
        data = self.readfrom(addr, len(buf))
        if data:
            buf[: len(data)] = data

    def writeto(self, addr: int, buf: bytes | bytearray, stop: bool = True) -> int:
        """Write data to an I2C device.

        :param int addr: I2C device address (7-bit).
        :param bytes|bytearray buf: Data to write.
        :param bool stop: Generate stop condition (ignored, kept for compatibility).
        :return: Number of bytes written.
        :rtype: int

        UiFlow2 Code Block:

            |writeto.png|

        MicroPython Code Block:

            .. code-block:: python

                n = unit_chain_bus.writeto(0x48, b"\x01\x02\x03")
        """
        if isinstance(buf, bytearray):
            buf = bytes(buf)
        if not buf or len(buf) == 0:
            return 0

        payload = struct.pack("<BB", addr & 0xFF, len(buf) & 0xFF) + buf
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_I2C_WRITE, payload)
        if state:
            if len(response) >= 1:
                if response[0] == 1:
                    return len(buf)
        return 0

    def readfrom_mem(self, addr: int, memaddr: int, nbytes: int, addrsize: int = 8) -> bytes:
        """Read data from an I2C device memory (register).

        :param int addr: I2C device address (7-bit).
        :param int memaddr: Memory/register address.
        :param int nbytes: Number of bytes to read.
        :param int addrsize: Register address size in bits (8 or 16). Default: 8.
        :return: Read data as bytes.
        :rtype: bytes

        UiFlow2 Code Block:

            |readfrom_mem.png|

        MicroPython Code Block:

            .. code-block:: python

                data = unit_chain_bus.readfrom_mem(0x48, 0x00, 4)
        """
        if addrsize not in (8, 16):
            return b""
        if nbytes <= 0:
            return b""

        reg_addr_size = 1 if addrsize == 8 else 2
        payload = struct.pack(
            "<BBBB", addr & 0xFF, reg_addr_size & 0xFF, memaddr & 0xFF, (memaddr >> 8) & 0xFF
        )
        payload += struct.pack("<B", nbytes & 0xFF)
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_I2C_READ_MEM, payload)
        if state:
            if len(response) >= 1:
                if response[0] == 1:  # Success
                    data_len = len(response) - 1
                    if data_len > nbytes:
                        data_len = nbytes
                    return bytes(response[1 : 1 + data_len])
        return b""

    def readfrom_mem_into(
        self, addr: int, memaddr: int, buf: bytearray, addrsize: int = 8
    ) -> None:
        """Read data from an I2C device memory (register) into a buffer.

        :param int addr: I2C device address (7-bit).
        :param int memaddr: Memory/register address.
        :param bytearray buf: Buffer to read into.
        :param int addrsize: Register address size in bits (8 or 16). Default: 8.

        UiFlow2 Code Block:

            |readfrom_mem_into.png|

        MicroPython Code Block:

            .. code-block:: python

                buf = bytearray(4)
                unit_chain_bus.readfrom_mem_into(0x48, 0x00, buf)
        """
        data = self.readfrom_mem(addr, memaddr, len(buf), addrsize)
        if data:
            buf[: len(data)] = data

    def writeto_mem(
        self, addr: int, memaddr: int, buf: bytes | bytearray, addrsize: int = 8
    ) -> None:
        """Write data to an I2C device memory (register).

        :param int addr: I2C device address (7-bit).
        :param int memaddr: Memory/register address.
        :param bytes|bytearray buf: Data to write.
        :param int addrsize: Register address size in bits (8 or 16). Default: 8.

        UiFlow2 Code Block:

            |writeto_mem.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_chain_bus.writeto_mem(0x48, 0x00, b"\x01\x02")
        """
        if isinstance(buf, bytearray):
            buf = bytes(buf)
        if addrsize not in (8, 16):
            return
        if not buf or len(buf) == 0:
            return

        reg_addr_size = 1 if addrsize == 8 else 2
        payload = struct.pack(
            "<BBBB", addr & 0xFF, reg_addr_size & 0xFF, memaddr & 0xFF, (memaddr >> 8) & 0xFF
        )
        payload += struct.pack("<B", len(buf) & 0xFF) + buf
        state, response = self.bus.chainll.send(
            self.device_id, self.CMD_BUS_I2C_WRITE_MEM, payload
        )
        if state:
            if len(response) >= 1:
                if response[0] == 1:  # Success
                    return
        return

    def scan(self) -> list:
        """Scan for I2C devices.

        :return: List of I2C device addresses found, or empty list if failed.
        :rtype: list

        UiFlow2 Code Block:

            |scan.png|

        MicroPython Code Block:

            .. code-block:: python

                devices = unit_chain_bus.scan()
                for addr in devices:
                    print("Found device at 0x{:02X}".format(addr))
        """
        max_devices = 32
        state, response = self.bus.chainll.send(self.device_id, self.CMD_BUS_I2C_SCAN, bytes())
        if state:
            if len(response) >= 2:
                if response[0] == 1:  # Success
                    dev_num = response[1]
                    if dev_num > max_devices:
                        dev_num = max_devices
                    if len(response) >= 2 + dev_num:
                        return list(response[2 : 2 + dev_num])
        return []

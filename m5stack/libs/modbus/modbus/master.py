# SPDX-FileCopyrightText: Copyright (c) 2021 Tobias Eydam
# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT

# ToDo:
# - async
# - error messages
# - documentation
# - modbus master (rtu) -> factory for slaves

from .frame import ModbusFrame, ModbusRTUFrame, ModbusTCPFrame
import socket
import time
import math
import struct
import sys
import asyncio

if sys.implementation.name == "micropython":
    import machine
    import micropython


class ModbusMaster:
    def __init__(self, ms_type: str = "tcp"):
        """
        Basic Modbus Master class

        :param str ms_type: Modbus type (tcp or rtu)
        """
        self.ms_type = ms_type

    def _send(self, frame: ModbusFrame, timeout: int = 2000) -> ModbusFrame:
        """
        MUST BE OVERRIDDEN

        Args:
            frame (ModbusFrame): the frame to send

        Returns:
            ModbusFrame: response
        """
        raise NotImplementedError

    async def _send_async(self, frame: ModbusFrame, timeout: int = 2000) -> ModbusFrame:
        """MUST BE OVERRIDDEN (async)

        Args:
            frame (ModbusFrame): the frame to send

        Returns:
            ModbusFrame: response
        """
        raise NotImplementedError

    def read_coils(self, address: int, register: int, quantity: int, timeout: int = 2000) -> list:
        """Read a number (quantity) of coils

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of coils

        Returns:
            list: response
        """
        data = self._read_registers(address, register, quantity, 1, timeout=timeout)
        if data is None:
            return []
        res = [False for _ in range(quantity)]
        for i in range(quantity):
            if data[i // 8] & 0x01 << (i % 8) > 0:
                res[i] = True
        return res

    async def read_coils_async(
        self, address: int, register: int, quantity: int, timeout: int = 2000
    ) -> list:
        """Read a number (quantity) of coils (async)

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of coils

        Returns:
            list: response
        """
        data = await self._read_registers_async(address, register, quantity, 1, timeout=timeout)
        if data is None:
            return []
        res = [False for _ in range(quantity)]
        for i in range(quantity):
            if data[i // 8] & 0x01 << (i % 8) > 0:
                res[i] = True
        return res

    def read_discrete_inputs(
        self, address: int, register: int, quantity: int, timeout: int = 2000
    ) -> list:
        """Read a number (quantity) of digital inputs

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of inputs

        Returns:
            list: response
        """
        data = self._read_registers(address, register, quantity, 2, timeout=timeout)
        if data is None:
            return []
        res = [False for _ in range(quantity)]
        for i in range(quantity):
            if data[i // 8] & 0x01 << (i % 8) > 0:
                res[i] = True
        return res

    async def read_discrete_inputs_async(
        self, address: int, register: int, quantity: int, timeout: int = 2000
    ) -> list:
        """Read a number (quantity) of digital inputs (async)

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of inputs

        Returns:
            list: response
        """
        data = await self._read_registers_async(address, register, quantity, 2, timeout=timeout)
        if data is None:
            return []
        res = [False for _ in range(quantity)]
        for i in range(quantity):
            if data[i // 8] & 0x01 << (i % 8) > 0:
                res[i] = True
        return res

    def read_holding_registers(
        self, address: int, register: int, quantity: int, timeout: int = 2000
    ) -> list:
        """Read a number (quantity) of holding registers

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of holding registers

        Returns:
            list: response
        """
        data = self._read_registers(address, register, quantity, 3, timeout=timeout)
        if data is None:
            return []
        res = []
        # TODO: quantity * 2 == len(data)
        for i in range(0, len(data), 2):
            res.append(int.from_bytes(data[i : i + 2], "big"))
        return res

    async def read_holding_registers_async(
        self, address: int, register: int, quantity: int, timeout: int = 2000
    ) -> list:
        """Read a number (quantity) of holding registers (async)

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of holding registers

        Returns:
            list: response
        """
        data = await self._read_registers_async(address, register, quantity, 3, timeout=timeout)
        if data is None:
            return []
        res = []
        # TODO: quantity * 2 == len(data)
        for i in range(0, len(data), 2):
            res.append(int.from_bytes(data[i : i + 2], "big"))
        return res

    def read_input_registers(
        self, address: int, register: int, quantity: int, timeout: int = 2000
    ) -> list:
        """Read a number (quantity) of input registers

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of input registers

        Returns:
            list: response
        """
        data = self._read_registers(address, register, quantity, 4, timeout=timeout)
        if data is None:
            return []
        res = []
        for i in range(0, len(data), 2):
            res.append(int.from_bytes(data[i : i + 2], "big"))
        return res

    async def read_input_registers_async(
        self, address: int, register: int, quantity: int, timeout: int = 2000
    ) -> list:
        """Read a number (quantity) of input registers (async)

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of input registers

        Returns:
            list: response
        """
        data = await self._read_registers_async(address, register, quantity, 4, timeout=timeout)
        if data is None:
            return []
        res = []
        for i in range(0, len(data), 2):
            res.append(int.from_bytes(data[i : i + 2], "big"))
        return res

    def _read_registers(
        self, address: int, register: int, quantity: int, code: int, timeout: int = 2000
    ) -> bytearray:
        """private helper function

        Args:
            register (int): start register
            quantity (int): number of registers
            code (int): function code

        Returns:
            bytearray: response
        """
        if self.ms_type == "tcp":
            f = ModbusTCPFrame(
                transaction_id=self.ti,
                func_code=code,
                register=register,
                fr_type="request",
                length=quantity,
            )
            state, resp = self._send(f.get_frame(), timeout=timeout)
            if state is False:
                return None
            resp_frame = ModbusTCPFrame.parse_frame(resp)
            self.ti += 1
        elif self.ms_type == "rtu":
            f = ModbusRTUFrame(
                device_addr=address,
                func_code=code,
                register=register,
                fr_type="request",
                length=quantity,
            )
            state, resp = self._send(f.get_frame(), timeout=timeout)
            if state is False:
                return None
            resp_frame = ModbusRTUFrame.parse_frame(resp, fr_type="response")

        return resp_frame.data

    async def _read_registers_async(
        self, address: int, register: int, quantity: int, code: int, timeout: int = 2000
    ) -> bytearray:
        """private helper function (asnc)

        Args:
            address (int): slave address
            register (int): start register
            quantity (int): number of registers
            code (int): function code

        Returns:
            bytearray: response
        """
        if self.ms_type == "tcp":
            f = ModbusTCPFrame(
                transaction_id=self.ti,
                func_code=code,
                register=register,
                fr_type="request",
                length=quantity,
            )
            state, resp = await self._send_async(f.get_frame(), timeout=timeout)
            if state is False:
                return None
            resp_frame = ModbusTCPFrame.parse_frame(resp)
            self.ti += 1
        elif self.ms_type == "rtu":
            f = ModbusRTUFrame(
                device_addr=address,
                func_code=code,
                register=register,
                fr_type="request",
                length=quantity,
            )
            state, resp = await self._send_async(f.get_frame(), timeout=timeout)
            if state is False:
                return None
            resp_frame = ModbusRTUFrame.parse_frame(resp, fr_type="response")

        return resp_frame.data

    def write_single_coil(
        self, address: int, register: int, value: bool or int or str, timeout: int = 2000
    ) -> bool:
        """Write a coil

        Args:
            address (int): slave address
            register (int): register of the coil
            value (bool or int or str): True/1/"on"/"ON"/"On" or False/0/"off"/"OFF"/"Off"

        Raises:
            ValueError: if value is not valid
            ValueError: if coil can't be written

        Returns:
            bool: The value of the coil
        """
        if value in [True, 1, "on", "ON", "On"]:
            data = bytearray([0xFF, 0x00])
        elif value in [False, 0, "off", "OFF", "Off"]:
            data = bytearray([0x00, 0x00])
        else:
            raise ValueError("cannot write coil value {}".format(value))
        resp = self._write_registers(address, register, 1, data, 5, timeout=timeout)
        if resp is None:
            return False
        return resp == bytearray([0xFF, 0x00])

    async def write_single_coil_async(
        self, address: int, register: int, value: bool or int or str, timeout: int = 2000
    ) -> bool:
        """Write a coil (async)

        Args:
            register (int): register of the coil
            value (bool or int or str): True/1/"on"/"ON"/"On" or False/0/"off"/"OFF"/"Off"

        Raises:
            ValueError: if value is not valid
            ValueError: if coil can't be written

        Returns:
            bool: The value of the coil
        """
        if value in [True, 1, "on", "ON", "On"]:
            data = bytearray([0xFF, 0x00])
        elif value in [False, 0, "off", "OFF", "Off"]:
            data = bytearray([0x00, 0x00])
        else:
            raise ValueError("cannot write coil value {}".format(value))
        res = await self._write_registers_async(address, register, 1, data, 5, timeout=timeout)
        return res == bytearray([0xFF, 0x00])

    def write_single_register(
        self, address: int, register: int, value: int, timeout: int = 2000
    ) -> int:
        """Write a holding register

        Args:
            address (int): slave address
            register (int): register of the holding register
            value (int): value

        Raises:
            ValueError: if register can't be written

        Returns:
            int: the written value
        """
        resp = self._write_registers(
            address, register, 1, value.to_bytes(2, "big"), 6, timeout=timeout
        )
        if resp is None:
            return -1
        return int.from_bytes(resp, "big")

    async def write_single_register_async(
        self, address: int, register: int, value: int, timeout: int = 2000
    ) -> int:
        """Write a holding register (async)

        Args:
            register (int): register of the holding register
            value (int): value

        Raises:
            ValueError: if register can't be written

        Returns:
            int: the written value
        """
        data = await self._write_registers_async(
            address, register, 1, value.to_bytes(2, "big"), 6, timeout=timeout
        )
        if data is None:
            return -1
        return int.from_bytes(data, "big")

    def write_multiple_coils(
        self, address: int, register: int, value: list, timeout: int = 2000
    ) -> int:
        """Write multiple coils

        Args:
            address (int): slave address
            register (int): start register of the coils
            value (list): value

        Raises:
            ValueError: if coils can't be written

        Returns:
            list: the value of the coils
        """
        new_value = bytearray(math.ceil(len(value) / 8))
        for i in range(len(value)):
            if value[i] is True or value[i] == 0x01:
                new_value[i // 8] |= 0x01 << (i % 8)
        resp = self._write_registers(address, register, len(value), new_value, 15, timeout=timeout)
        if resp is None:
            return -1
        return resp

    async def write_multiple_coils_async(
        self, address: int, register: int, value: list, timeout: int = 2000
    ) -> list:
        """Write multiple coils (async)

        Args:
            address (int): slave address
            register (int): start register of the coils
            value (list): value

        Raises:
            ValueError: if coils can't be written

        Returns:
            int: the value of the coils
        """
        new_value = bytearray(math.ceil(len(value) / 8))
        for i in range(len(value)):
            if value[i] is True or value[i] == 0x01:
                new_value[i // 8] |= 0x01 << (i % 8)
        return await self._write_registers_async(
            address, register, len(value), new_value, 15, timeout=timeout
        )

    def write_multiple_registers(
        self, address: int, register: int, value: list, timeout: int = 2000
    ) -> list:
        """Write multiple registers

        Args:
            address (int): slave address
            register (int): start register
            value (list): value

        Raises:
            ValueError: if registers can't be written

        Returns:
            list: the written value
        """
        new_value = bytearray(len(value) * 2)
        for i in range(len(value)):
            struct.pack_into(">H", new_value, i * 2, value[i])
        resp = self._write_registers(address, register, len(value), new_value, 16, timeout=timeout)
        if resp is None:
            return -1
        return resp

    async def write_multiple_registers_async(
        self, address: int, register: int, value: list, timeout: int = 2000
    ) -> list:
        """Write multiple registers (async)

        Args:
            address (int): slave address
            register (int): start register
            value (list): value

        Raises:
            ValueError: if registers can't be written

        Returns:
            list: the written value
        """
        new_value = bytearray(len(value) * 2)
        for i in range(len(value)):
            struct.pack_into(">H", new_value, i * 2, value[i])

        return await self._write_registers_async(
            address, register, len(value), new_value, 16, timeout=timeout
        )

    def _write_registers(
        self,
        address: int,
        register: int,
        quantity: int,
        value: bytearray,
        code: int,
        timeout: int = 2000,
    ) -> bytearray or int:
        """Helper function

        Args:
            address (int): slave address
            register (int): register
            quantity (int): quantity
            value (bytearray): value
            code (int): function code

        Raises:
            ValueError: if value can't be written

        Returns:
            bytearray or int: data or quantity (depending on function code)
        """
        f = None
        if self.ms_type == "tcp":
            if code in [0x05, 0x06]:
                f = ModbusTCPFrame(
                    transaction_id=self.ti,
                    unit_id=address,
                    func_code=code,
                    register=register,
                    fr_type="request",
                    data=value,
                )
            if code in [0x0F, 0x10]:
                f = ModbusTCPFrame(
                    transaction_id=self.ti,
                    unit_id=address,
                    func_code=code,
                    register=register,
                    fr_type="request",
                    data=value,
                    length=quantity,
                )
            self.ti += 1
        elif self.ms_type == "rtu":
            if code in [0x05, 0x06]:
                f = ModbusRTUFrame(
                    device_addr=address,
                    func_code=code,
                    register=register,
                    fr_type="request",
                    data=value,
                )
            if code in [0x0F, 0x10]:
                f = ModbusRTUFrame(
                    device_addr=address,
                    func_code=code,
                    register=register,
                    fr_type="request",
                    data=value,
                    length=quantity,
                )

        state, resp = self._send(f.get_frame(), timeout=timeout)
        if state is False:
            return None

        if self.ms_type == "tcp":
            resp_frame = ModbusTCPFrame.parse_frame(resp)
        elif self.ms_type == "rtu":
            resp_frame = ModbusRTUFrame.parse_frame(resp)

        if resp_frame is None:
            return None

        if resp_frame.func_code in [0x05, 0x06]:
            return resp_frame.data
        if resp_frame.func_code in [0x0F, 0x10]:
            return resp_frame.length
        if resp_frame.func_code in [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x8F, 0x90]:
            txt = {
                1: "ILLEGAL_FUNCTION",
                2: "ILLEGAL_DATA_ADDRESS",
                3: "ILLEGAL_DATA_VALUE",
                4: "SLAVE_DEVICE_FAILURE",
                5: "ACKNOWLEDGE",
                6: "SLAVE_DEVICE_BUSY",
                7: "NEGATIVE_ACKNOWLEDGE",
                8: "MEMORY_PARITY_ERROR",
                10: "GATEWAY_PATH_UNAVAILABLE",
                11: "GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND",
            }[resp_frame.error_code]
            self._verbose and print(
                "Received Error Frame (Function Code: {:02x}, Exception Code: {:02x}, {})".format(
                    resp_frame.func_code, resp_frame.error_code, txt
                )
            )
            if self.exception_cb and sys.implementation.name == "micropython":
                micropython.schedule(
                    self.exception_cb, (self, resp_frame.func_code, resp_frame.error_code)
                )

    async def _write_registers_async(
        self,
        address: int,
        register: int,
        quantity: int,
        value: bytearray,
        code: int,
        timeout: int = 2000,
    ) -> bytearray or int:
        """Helper function (async)

        Args:
            register (int): register
            quantity (int): quantity
            value (bytearray): value
            code (int): function code

        Raises:
            ValueError: if value can't be written

        Returns:
            bytearray or int: data or quantity (depending on function code)
        """
        f = None
        if self.ms_type == "tcp":
            if code in [0x05, 0x06]:
                f = ModbusTCPFrame(
                    transaction_id=self.ti,
                    unit_id=address,
                    func_code=code,
                    register=register,
                    fr_type="request",
                    data=value,
                )
            if code in [0x0F, 0x10]:
                f = ModbusTCPFrame(
                    transaction_id=self.ti,
                    unit_id=address,
                    func_code=code,
                    register=register,
                    fr_type="request",
                    data=value,
                    length=quantity,
                )
            self.ti += 1
        elif self.ms_type == "rtu":
            if code in [0x05, 0x06]:
                f = ModbusRTUFrame(
                    device_addr=address,
                    func_code=code,
                    register=register,
                    fr_type="request",
                    data=value,
                )
            if code in [0x0F, 0x10]:
                f = ModbusRTUFrame(
                    device_addr=address,
                    func_code=code,
                    register=register,
                    fr_type="request",
                    data=value,
                    length=quantity,
                )

        state, resp = await self._send_async(f.get_frame(), timeout=timeout)
        if state is False:
            return None

        if self.ms_type == "tcp":
            resp_frame = ModbusTCPFrame.parse_frame(resp)
        elif self.ms_type == "rtu":
            resp_frame = ModbusRTUFrame.parse_frame(resp)

        if resp_frame.func_code in [0x05, 0x06]:
            return resp_frame.data
        if resp_frame.func_code in [0x0F, 0x10]:
            return resp_frame.length
        if resp_frame.func_code in [0x81, 0x82, 0x83, 0x84, 0x85, 0x86, 0x8F, 0x90]:
            txt = {
                1: "ILLEGAL_FUNCTION",
                2: "ILLEGAL_DATA_ADDRESS",
                3: "ILLEGAL_DATA_VALUE",
                4: "SLAVE_DEVICE_FAILURE",
                5: "ACKNOWLEDGE",
                6: "SLAVE_DEVICE_BUSY",
                7: "NEGATIVE_ACKNOWLEDGE",
                8: "MEMORY_PARITY_ERROR",
                10: "GATEWAY_PATH_UNAVAILABLE",
                11: "GATEWAY_TARGET_DEVICE_FAILED_TO_RESPOND",
            }[resp_frame.error_code]
            self._verbose and print(
                "Received Error Frame (Function Code: {:02x}, Exception Code: {:02x}, {})".format(
                    resp_frame.func_code, resp_frame.error_code, txt
                )
            )
            if self.exception_cb and sys.implementation.name == "micropython":
                self.exception_cb(resp_frame.func_code, resp_frame.error_code)


class ModbusTCPClient(ModbusMaster):
    def __init__(self, host: str, port: int = 502, verbose=False, *args, **kwargs):
        """Init a modbus tcp client

        Args:
            host (str): IP or Hostname
            port (int): Port Defaults to 502
        """

        self.host = host
        self.port = port
        self.connected = False
        self.ti = 1
        self._verbose = verbose
        self.exception_cb = None
        super(ModbusTCPClient, self).__init__(ms_type="tcp")

    def _send(self, frame: bytearray, timeout: int = 2000) -> bytearray:
        """Send a frame an return the resonse

        Args:
            frame (bytearray): data to send

        Returns:
            bytearray: response
        """
        # self.sock.settimeout(timeout / 1000)
        self.sock.send(frame)
        resp = self.sock.recv(256)
        state = self._exit_read(resp)
        return (state, resp)

    def _exit_read(self, response: bytearray) -> bool:
        response_len = len(response)
        if response_len >= 2 and response[1] >= 0x80:
            if response_len < 0x05:
                return False
        elif response_len >= 3 and (0x01 <= response[1] <= 0x04):
            expected_len = (
                1 + 1 + 1 + response[2] + 2
            )  # address + function code + byte count + data + crc
            if response_len < expected_len:
                return False
        elif response_len < 0x08:
            return False

        return True

    async def _send_async(self, frame: bytearray, timeout: int = 2000) -> bytearray:
        """Send a frame an return the resonse (async)

        Args:
            frame (bytearray): data to send

        Returns:
            bytearray: response
        """
        loop = asyncio.get_event_loop()
        self.sock.send(frame)
        resp = await loop.sock_recv(self.sock, 256)
        state = self._exit_read(resp)
        return (state, resp)

    def connect(self):
        """Connect socket"""
        if not self.connected:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.connected = True

    def disconnect(self):
        """Disconnect socket"""
        if self.connected:
            self.sock.close()
            self.connected = False


class _CModbusRTUMaster(ModbusMaster):
    def __init__(
        self,
        uart_no: int = 1,
        baudrate: int = 9600,
        bits: int = 8,
        stop: int = 1,
        parity: int = None,
        tx_pin: int = 14,
        rx_pin: int = 13,
        en_pin: int = 15,
        uart=None,
        device_addr: int = 1,
        verbose: bool = False,
        *args,
        **kwargs,
    ):
        """Init a modbus RTU master. Pins or UART-Modul can be passed. If a second slave

        Args:
            uart_no (int, optional): [description]. Defaults to 1.
            baudrate (int, optional): [description]. Defaults to 9600.
            bits (int, optional): [description]. Defaults to 8.
            stop (int, optional): [description]. Defaults to 1.
            parity (int, optional): [description]. Defaults to None.
            tx_pin (int, optional): [description]. Defaults to 14.
            rx_pin (int, optional): [description]. Defaults to 13.
            en_pin (int, optional): [description]. Defaults to 15.
            uart (uart, optional): [description]. Defaults to None.
            device_addr (int, optional): [description]. Defaults to 1.
        """
        self._verbose = verbose
        super(_CModbusRTUMaster, self).__init__(ms_type="rtu", *args, **kwargs)
        self.uart = uart
        self._t1char = (
            1000000 * (self.uart.bytesize + self.uart.stopbits + 2)
        ) // self.uart.baudrate
        if self.uart.baudrate <= 19200:
            self._inter_frame_delay = (self._t1char * 3500) // 1000
        else:
            self._t1char = 500
            self._inter_frame_delay = 1750
        self._verbose and print("[MODBUS] character time: {}us".format(self._t1char))
        self._verbose and print("[MODBUS] inter frame delay: {}us".format(self._inter_frame_delay))

    def _exit_read(self, response: bytearray) -> bool:
        response_len = len(response)
        if response_len >= 2 and response[1] >= 0x80:
            if response_len < 0x05:
                return False
        elif response_len >= 3 and (0x01 <= response[1] <= 0x04):
            expected_len = (
                1 + 1 + 1 + response[2] + 2
            )  # address + function code + byte count + data + crc
            if response_len < expected_len:
                return False
        elif response_len < 0x08:
            return False

        return True

    def _send(self, frame: bytearray, timeout: int = 2000) -> bytearray:
        """Send a frame an return the resonse

        Args:
            frame (bytearray): data to send

        Returns:
            bytearray: response
        """
        self._verbose and print("[MODBUS] M->S: " + " ".join("{:02x}".format(x) for x in frame))
        self.uart.write(frame)
        self.uart.flush()
        time.sleep(self._inter_frame_delay / 1000 / 1000)

        response = bytearray()
        state = False
        startpos = -1
        timeout = time.time_ns() + timeout * 1000 * 1000  # 500ms
        while True:
            if self.uart.inWaiting() > 0:
                data = self.uart.read(1)
                if startpos == -1:
                    startpos = data.find(frame[0:1])
                    response.extend(data)
                    continue
                response.extend(data)
                if self._exit_read(response):
                    state = True
                    break
            if time.time_ns() > timeout:
                break
        return (state, response)

    async def _send_async(self, frame: bytearray, timeout: int = 2000) -> bytearray:
        """Send a frame an return the resonse (async)

        Args:
            frame (bytearray): data to send

        Returns:
            bytearray: response
        """
        # TODO: implement async
        self._verbose and print("[MODBUS] M->S: " + " ".join("{:02x}".format(x) for x in frame))
        self.uart.write(frame)
        self.uart.flush()
        await asyncio.sleep(self._inter_frame_delay / 1000 / 1000)

        response = bytearray()
        state = False
        startpos = -1
        timeout = time.time_ns() + timeout * 1000 * 1000  # 500ms
        while True:
            if self.uart.inWaiting() > 0:
                data = self.uart.read(1)
                if startpos == -1:
                    startpos = data.find(frame[0:1])
                    response.extend(data)
                    continue
                response.extend(data)
                if self._exit_read(response):
                    state = True
                    break
            await asyncio.sleep(0.05)
            if time.time_ns() > timeout:
                break
        return (state, response)


class _MModbusRTUMaster(ModbusMaster):
    def __init__(
        self,
        uart_no: int = 1,
        baudrate: int = 9600,
        bits: int = 8,
        stop: int = 1,
        parity: int = None,
        tx_pin: int = 14,
        rx_pin: int = 13,
        en_pin: int = -1,
        uart=None,
        device_addr: int = 1,
        verbose: bool = False,
    ):
        """Init a modbus RTU master. Pins or UART-Modul can be passed. If a second slave

        Args:
            uart_no (int, optional): [description]. Defaults to 1.
            baudrate (int, optional): [description]. Defaults to 9600.
            bits (int, optional): [description]. Defaults to 8.
            stop (int, optional): [description]. Defaults to 1.
            parity (int, optional): [description]. Defaults to None.
            tx_pin (int, optional): [description]. Defaults to 14.
            rx_pin (int, optional): [description]. Defaults to 13.
            en_pin (int, optional): [description]. Defaults to 15.
            uart (uart, optional): [description]. Defaults to None.
            device_addr (int, optional): [description]. Defaults to 1.
        """
        self._verbose = verbose
        super(_MModbusRTUMaster, self).__init__(ms_type="rtu")
        self.baudrate = baudrate
        self._en_pin = None
        if en_pin != -1:
            self.en_pin = machine.Pin(en_pin, machine.Pin.OUT)
        if uart is None:
            self.uart = machine.UART(
                uart_no,
                baudrate=baudrate,
                bits=bits,
                parity=parity,
                stop=stop,
                tx=tx_pin,
                rx=rx_pin,
                timeout=30,
                timeout_char=30,
                rxbuf=1024,
            )
        else:
            self.uart = uart

        self._calculate_character_times()
        self._verbose and print("[MODBUS] character time: {}us".format(self._t1char))
        self._verbose and print("[MODBUS] inter frame delay: {}us".format(self._inter_frame_delay))

    def _calculate_character_times(self):
        """UART(1, baudrate=115201, bits=8, parity=None, stop=1, tx=13, rx=14, rts=-1, cts=-1, txbuf=256, rxbuf=256, timeout=0, timeout_char=0)"""
        import re

        uart_string = str(self.uart)
        match = re.search(r"baudrate=(\d+).*?bits=(\d+).*?stop=(\d+)", uart_string)
        if match:
            baudrate = int(match.group(1))
            bits = int(match.group(2))
            stop = int(match.group(3))
            if baudrate <= 19200:
                self._t1char = (1000000 * (bits + stop + 2)) // baudrate
                self._inter_frame_delay = (self._t1char * 3500) // 1000
            else:
                self._t1char = 500
                self._inter_frame_delay = 1750
        else:
            self._t1char = 500
            self._inter_frame_delay = 1750

    def _exit_read(self, response: bytearray) -> bool:
        response_len = len(response)
        if response_len >= 2 and response[1] >= 0x80:
            if response_len < 0x05:
                return False
        elif response_len >= 3 and (0x01 <= response[1] <= 0x04):
            expected_len = (
                1 + 1 + 1 + response[2] + 2
            )  # address + function code + byte count + data + crc
            if response_len < expected_len:
                return False
        elif response_len < 0x08:
            return False

        return True

    def _send(self, frame: bytearray, timeout: int = 2000) -> bytearray:
        """Send a frame an return the resonse

        Args:
            frame (bytearray): data to send

        Returns:
            bytearray: response
        """
        self._verbose and print("[MODBUS] M->S: " + " ".join("{:02x}".format(x) for x in frame))
        self.uart.write(frame)
        self.uart.flush()
        time.sleep(self._inter_frame_delay / 1000 / 1000)

        response = bytearray()
        state = False
        startpos = -1
        timeout = time.ticks_ms() + timeout
        while True:
            if self.uart.any() > 0:
                data = self.uart.read(1)
                if startpos == -1:
                    startpos = data.find(frame[0:1])
                    response.extend(data)
                    continue
                response.extend(data)
                if self._exit_read(response):
                    state = True
                    break

            if time.ticks_ms() > timeout:
                break
        return (state, response)

    async def _send_async(self, frame: bytearray, timeout: int = 2000) -> bytearray:
        """Send a frame an return the resonse (async)

        Args:
            frame (bytearray): data to send

        Returns:
            bytearray: response
        """
        self._verbose and print("[MODBUS] M->S: " + " ".join("{:02x}".format(x) for x in frame))
        self.uart.write(frame)
        self.uart.flush()
        await asyncio.sleep(self._inter_frame_delay / 1000 / 1000)

        response = bytearray()
        state = False
        startpos = -1
        timeout = time.ticks_ms() + timeout
        while True:
            if self.uart.any() > 0:
                data = self.uart.read(1)
                if startpos == -1:
                    startpos = data.find(frame[0:1])
                    response.extend(data)
                    continue
                response.extend(data)
                if self._exit_read(response):
                    state = True
                    break
            await asyncio.sleep(0.05)
            if time.ticks_ms() > timeout:
                break
        return (state, response)


class ModbusRTUMaster:
    def __new__(cls, *args, **kwargs):
        if sys.implementation.name == "cpython":
            return _CModbusRTUMaster(*args, **kwargs)
        elif sys.implementation.name == "micropython":
            return _MModbusRTUMaster(*args, **kwargs)

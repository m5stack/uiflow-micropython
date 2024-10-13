# SPDX-FileCopyrightText: Copyright (c) 2021 Tobias Eydam
# SPDX-FileCopyrightText: Copyright (c) 2024 lbuque, written for M5Stack
#
# SPDX-License-Identifier: MIT

# ToDo:
# - async
# - error messages
# - documentation

from .frame import ModbusRTUFrame, ModbusTCPFrame
import socket
import math
import asyncio
import sys
import struct
import time


class ModbusSlave:
    _available_register_types = (
        "coils",
        "discrete_inputs",
        "holding_registers",
        "input_registers",
    )

    def __init__(self, sl_type="tcp", context=None, device_address=1):
        self.sl_type = sl_type
        self.context = context
        self.forward_message = None
        self.stopped = False
        self._device_address = device_address
        if context is None:
            self.context = {
                "discrete_inputs": [],
                "coils": [],
                "input_registers": [],
                "holding_registers": [],
            }
        self.cb = {
            0x02: None,  # Read Discrete Inputs
            0x01: None,  # Read Coils
            0x05: None,  # Write Single Coil
            0x0F: None,  # Write Multiple Coils
            0x04: None,  # Read Input Registers
            0x03: None,  # Read Holding Registers
            0x06: None,  # Write Single Register
            0x10: None,  # Write Multiple Registers
            0x17: None,  # Read/Write Multiple Registers
            0x16: None,  # Mask Write Register
            0x14: None,  # Read File Record
            0x15: None,  # Write File Record
            0x2B: None,  # Read Device Identification
        }

    def _add_register_in_context(self, reg_type, register, value):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        added = False
        for reg in self.context[reg_type]:
            if reg["register"] <= register < reg["register"] + len(self.context[reg_type]["val"]):
                # if register exists in the context
                idx = register - reg["register"]
                reg["val"][idx] = value
                added = True
            elif reg["register"] + 1 == register:
                # if register is at the end of the context
                reg["val"].append(value)
                added = True

        if not added:
            # if register is not in the context
            self.context[reg_type].append({"register": register, "val": [value]})

        # sort the registers in the context
        regs = self.context[reg_type]
        for i in range(len(regs)):
            for j in range(len(regs)):
                if regs[i]["register"] < regs[j]["register"]:
                    regs[i], regs[j] = regs[j], regs[i]

        # Merge registers with consecutive addresses
        for i in range(len(regs) - 1, -1, -1):
            if regs[i]["register"] == regs[i - 1]["register"] + len(regs[i - 1]["val"]):
                regs[i - 1]["val"].extend(regs[i]["val"])
                regs.pop(i)

    def _remove_register_from_context(self, reg_type, register):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        new_regs = []
        regs = self.context[reg_type]
        for i in range(len(regs) - 1, -1, -1):
            quantity = len(regs[i]["val"])
            if regs[i]["register"] <= register < regs[i]["register"] + quantity:
                idx = register - regs[i]["register"]
                if quantity == 1:
                    del regs[i]
                elif idx == 0:
                    regs[i]["register"] += 1
                    regs[i]["val"].pop(0)
                elif idx == quantity - 1:
                    regs[i]["val"].pop(-1)
                elif 0 < idx < quantity - 1:
                    new_regs.append(
                        {"register": regs[i]["register"], "val": regs[i]["val"][0:idx]}
                    )
                    new_regs.append(
                        {
                            "register": regs[i]["register"] + idx + 1,
                            "val": regs[i]["val"][idx + 1 :],
                        }
                    )
                    del regs[i]

        regs.extend(new_regs)
        # sort the registers in the context
        for i in range(len(regs)):
            for j in range(len(regs)):
                if regs[i]["register"] < regs[j]["register"]:
                    regs[i], regs[j] = regs[j], regs[i]

    def add_coil(self, register, value):
        """Add a coil to the modbus register dictionary.

        Args:

        """
        self._add_register_in_context("coils", register, value)

    def add_discrete_input(self, register, value):
        """Add a discrete input to the modbus register dictionary.

        Args:

        """
        self._add_register_in_context("discrete_inputs", register, value)

    def add_holding_register(self, register, value):
        """Add a holding register to the modbus register dictionary.

        Args:

        """
        self._add_register_in_context("holding_registers", register, value)

    def add_input_register(self, register, value):
        """Add an input register to the modbus register dictionary.

        Args:

        """
        self._add_register_in_context("input_registers", register, value)

    def remove_coil(self, register):
        """Remove a coil from the modbus register dictionary.

        Args:

        """
        self._remove_register_from_context("coils", register)

    def remove_discrete_input(self, register):
        """Remove a discrete input from the modbus register dictionary.

        Args:

        """
        self._remove_register_from_context("discrete_inputs", register)

    def remove_holding_register(self, register):
        """Remove a holding register from the modbus register dictionary.

        Args:

        """
        self._remove_register_from_context("holding_registers", register)

    def remove_input_register(self, register):
        """Remove an input register from the modbus register dictionary.

        Args:

        """
        self._remove_register_from_context("input_registers", register)

    def _get_reg_data(self, reg_type, register):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        for reg in self.context[reg_type]:
            if reg["register"] <= register < reg["register"] + len(reg["val"]):
                idx = register - reg["register"]
                return reg["val"][idx]

        raise KeyError("Register {} not found in context".format(register))

    def _set_reg_data(self, reg_type, register, value):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        for reg in self.context[reg_type]:
            if reg["register"] <= register < reg["register"] + len(reg["val"]):
                idx = register - reg["register"]
                reg["val"][idx] = value
                return

        raise KeyError("Register {} not found in context".format(register))

    def _set_reg_datablock(self, reg_type, register, block):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        for reg in self.context[reg_type]:
            if reg["register"] <= register < reg["register"] + len(reg["val"]):
                idx = register - reg["register"]
                for new_value in block:
                    reg["val"][idx] = new_value
                    idx += 1
                return

        raise KeyError("Register {} not found in context".format(register))

    def get_coil(self, register):
        """Get the coil value.

        Args:

        """
        return self._get_reg_data("coils", register)

    def get_discrete_input(self, register):
        """Get the discrete input value.

        Args:

        """
        return self._get_reg_data("discrete_inputs", register)

    def get_holding_register(self, register):
        """Get the holding register value.

        Args:

        """
        return self._get_reg_data("holding_registers", register)

    def get_input_register(self, register):
        """Get the input register value.

        Args:

        """
        return self._get_reg_data("input_registers", register)

    def set_coil(self, register, value):
        """Set the coil value.

        Args:

        """
        self._set_reg_data("coils", register, value)

    def set_multi_coils(self, register, value):
        """Set the coil value.

        Args:

        """
        self._set_reg_datablock("coils", register, value)

    def set_discrete_input(self, register, value):
        """Set the discrete input value.

        Args:

        """
        self._set_reg_data("discrete_inputs", register, value)

    def set_holding_register(self, register, value):
        """Set the holding register value.

        Args:

        """
        self._set_reg_data("holding_registers", register, value)

    def set_multi_holding_register(self, register, value):
        """Set the holding register value.

        Args:

        """
        self._set_reg_datablock("holding_registers", register, value)

    def set_input_register(self, register, value):
        """Set the input register value.

        Args:

        """
        self._set_reg_data("input_registers", register, value)

    def stop(self):
        self.stopped = True

    def handle_message(self, frame):  # noqa: C901
        # TODO: Refactor this method
        if self.context is None:
            if self.forward_message is not None:
                return self.forward_message(frame)
            return

        db = {
            1: "coils",
            2: "discrete_inputs",
            3: "holding_registers",
            4: "input_registers",
            5: "coils",
            6: "holding_registers",
            15: "coils",
            16: "holding_registers",
        }[frame.func_code]

        if db not in self.context:
            # No: Function code supported
            if self.sl_type == "tcp":
                return ModbusTCPFrame(
                    transaction_id=frame.transaction_id,
                    unit_id=frame.unit_id,
                    func_code=0x80 + frame.func_code,
                    fr_type="response",
                    error_code=0x01,
                )
            if self.sl_type == "rtu":
                return ModbusRTUFrame(
                    device_addr=frame.device_addr,
                    func_code=0x80 + frame.func_code,
                    fr_type="response",
                    error_code=0x01,
                )

        if frame.func_code in [1, 2, 3, 4]:
            if not (0x0001 <= frame.length <= 0x07D0):
                # No: 0x0001 <= quantity of registers <= 0x007D
                if self.sl_type == "tcp":
                    return ModbusTCPFrame(
                        transaction_id=frame.transaction_id,
                        unit_id=frame.unit_id,
                        func_code=0x80 + frame.func_code,
                        fr_type="response",
                        error_code=0x03,
                    )
                if self.sl_type == "rtu":
                    return ModbusRTUFrame(
                        device_addr=frame.device_addr,
                        func_code=0x80 + frame.func_code,
                        fr_type="response",
                        error_code=0x03,
                    )
            if self._check_register(frame.register, frame.length, self.context[db]):
                data = self._get_data(frame.register, frame.length, self.context[db])
                res = None
                if frame.func_code in [1, 2]:
                    res = bytearray([0x00] * math.ceil(frame.length / 8))
                    for i in range(frame.length):
                        if data[i] is True or data[i] == 0x01:
                            res[i // 8] |= 0x01 << (i % 8)
                else:
                    res = bytearray(frame.length * 2)
                    for i in range(frame.length):
                        struct.pack_into(">H", res, i * 2, data[i])
                if self.sl_type == "tcp":
                    return ModbusTCPFrame(
                        transaction_id=frame.transaction_id,
                        unit_id=frame.unit_id,
                        func_code=frame.func_code,
                        fr_type="response",
                        data=res,
                    )
                if self.sl_type == "rtu":
                    return ModbusRTUFrame(
                        device_addr=frame.device_addr,
                        func_code=frame.func_code,
                        fr_type="response",
                        data=res,
                    )
            else:
                # No: Starting Address == OK AND Starting Address + Quantity of Outputs == OK
                if self.sl_type == "tcp":
                    return ModbusTCPFrame(
                        transaction_id=frame.transaction_id,
                        unit_id=frame.unit_id,
                        func_code=0x80 + frame.func_code,
                        fr_type="response",
                        error_code=0x02,
                    )
                if self.sl_type == "rtu":
                    return ModbusRTUFrame(
                        device_addr=frame.device_addr,
                        func_code=0x80 + frame.func_code,
                        fr_type="response",
                        error_code=0x02,
                    )

        if frame.func_code in [5, 6, 15, 16]:
            if frame.func_code == 5:
                length = 1
                data = frame.data
                if data[0] not in [0x00, 0xFF] and data[0] != 0x00:
                    # No: Output Value == 0x0000 OR 0xFF00
                    if self.sl_type == "tcp":
                        return ModbusTCPFrame(
                            transaction_id=frame.transaction_id,
                            unit_id=frame.unit_id,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x03,
                        )
                    if self.sl_type == "rtu":
                        return ModbusRTUFrame(
                            device_addr=frame.device_addr,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x03,
                        )
                if self._check_register(frame.register, length, self.context[db]):
                    self.set_coil(frame.register, True if data[0] else False)
                else:
                    # No: Output Address == OK
                    if self.sl_type == "tcp":
                        return ModbusTCPFrame(
                            transaction_id=frame.transaction_id,
                            unit_id=frame.unit_id,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x02,
                        )
                    if self.sl_type == "rtu":
                        return ModbusRTUFrame(
                            device_addr=frame.device_addr,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x02,
                        )
            if frame.func_code == 6:
                length = 1
                data = frame.data
                if self._check_register(frame.register, length, self.context[db]):
                    self.set_holding_register(frame.register, struct.unpack(">H", data)[0])
                else:
                    # No: Register Address == OK
                    if self.sl_type == "tcp":
                        return ModbusTCPFrame(
                            transaction_id=frame.transaction_id,
                            unit_id=frame.unit_id,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x02,
                        )
                    if self.sl_type == "rtu":
                        return ModbusRTUFrame(
                            device_addr=frame.device_addr,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x02,
                        )
            if frame.func_code == 15:
                length = frame.length
                data = [False for _ in range(frame.length)]
                for i in range(frame.length):
                    if frame.data[i // 8] & 0x01 << (i % 8) > 0:
                        data[i] = True
                if not (0x0001 <= length <= 0x07B0):
                    # 0x0001 ≤ Quantity of Outputs ≤ 0x07B0 AND Byte Count = N*
                    if self.sl_type == "tcp":
                        return ModbusTCPFrame(
                            transaction_id=frame.transaction_id,
                            unit_id=frame.unit_id,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x03,
                        )
                    if self.sl_type == "rtu":
                        return ModbusRTUFrame(
                            device_addr=frame.device_addr,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x03,
                        )
                if self._check_register(frame.register, length, self.context[db]):
                    self.set_multi_coils(frame.register, data)
                else:
                    # No: Starting Address == OK AND Starting Address + Quantity of Outputs == OK
                    if self.sl_type == "tcp":
                        return ModbusTCPFrame(
                            transaction_id=frame.transaction_id,
                            unit_id=frame.unit_id,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x02,
                        )
                    if self.sl_type == "rtu":
                        return ModbusRTUFrame(
                            device_addr=frame.device_addr,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x02,
                        )
            if frame.func_code == 16:
                length = frame.length
                data = frame.data
                if not (0x0001 <= length <= 0x007B and len(data) == length * 2):
                    # 0x0001 ≤ Quantity of Outputs ≤ 0x07B0 AND Byte Count = N*
                    if self.sl_type == "tcp":
                        return ModbusTCPFrame(
                            transaction_id=frame.transaction_id,
                            unit_id=frame.unit_id,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x03,
                        )
                    if self.sl_type == "rtu":
                        return ModbusRTUFrame(
                            device_addr=frame.device_addr,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x03,
                        )
                if self._check_register(frame.register, length, self.context[db]):
                    self.set_multi_holding_register(
                        frame.register, struct.unpack(">" + "H" * frame.length, data)
                    )
                else:
                    # No: Starting Address == OK AND Starting Address + Quantity of Outputs == OK
                    if self.sl_type == "tcp":
                        return ModbusTCPFrame(
                            transaction_id=frame.transaction_id,
                            unit_id=frame.unit_id,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x02,
                        )
                    if self.sl_type == "rtu":
                        return ModbusRTUFrame(
                            device_addr=frame.device_addr,
                            func_code=0x80 + frame.func_code,
                            fr_type="response",
                            error_code=0x02,
                        )

            if frame.func_code in [5, 6]:
                if self.sl_type == "tcp":
                    return ModbusTCPFrame(
                        transaction_id=frame.transaction_id,
                        unit_id=frame.unit_id,
                        register=frame.register,
                        func_code=frame.func_code,
                        fr_type="response",
                        data=data,
                    )
                if self.sl_type == "rtu":
                    return ModbusRTUFrame(
                        device_addr=frame.device_addr,
                        register=frame.register,
                        func_code=frame.func_code,
                        fr_type="response",
                        data=data,
                    )

            if frame.func_code in [15, 16]:
                if self.sl_type == "tcp":
                    return ModbusTCPFrame(
                        transaction_id=frame.transaction_id,
                        unit_id=frame.unit_id,
                        register=frame.register,
                        func_code=frame.func_code,
                        fr_type="response",
                        length=frame.length,
                    )
                if self.sl_type == "rtu":
                    return ModbusRTUFrame(
                        device_addr=frame.device_addr,
                        register=frame.register,
                        func_code=frame.func_code,
                        fr_type="response",
                        length=frame.length,
                    )

    def _check_register(self, register, length, regs):
        for reg in regs:
            quantity = len(reg["val"])
            if reg["register"] <= register < reg["register"] + quantity:
                if reg["register"] + quantity >= register + length:
                    return True
        return False

    def _get_data(self, register, length, regs):
        for reg in regs:
            if reg["register"] <= register < reg["register"] + len(reg["val"]):
                return reg["val"][
                    (register - reg["register"]) : (register - reg["register"] + length)
                ]

    def _set_data(self, register, length, data_Block, data):
        offset = register - data_Block["startAddr"]
        for i in range(length * 2):
            data_Block["registers"][2 * offset + i] = data[i]


class _CModbusRTUSlave(ModbusSlave):
    def __init__(self, uart, verbose=True, *args, **kwargs):
        self._verbose = verbose
        self.uart = uart
        super(_CModbusRTUSlave, self).__init__(sl_type="rtu", *args, **kwargs)

    async def run_async(self):
        self._verbose and print("starting async rtu slave")
        while not self.stopped:
            self.tick()
            await asyncio.sleep(0.1)

    def tick(self):
        if not self.stopped and self.uart.inWaiting():
            rsp = self.uart.read_all()
            frame = ModbusRTUFrame.parse_frame(rsp)
            resp = self.handle_message(frame).get_frame()
            self.uart.write(resp)
            cb = self.cb[frame.func_code]
            if cb is not None:
                db = {
                    1: "coils",
                    2: "discrete_inputs",
                    3: "holding_registers",
                    4: "input_registers",
                    5: "coils",
                    6: "holding_registers",
                    15: "coils",
                    16: "holding_registers",
                }[frame.func_code]
                if frame.func_code in [1, 2, 3, 4]:
                    data = self._get_data(frame.register, frame.length, self.context[db])
                    cb(frame.register, frame.length, data)
                if frame.func_code in [5, 6, 15, 16]:
                    cb(frame.register, frame.length, data)


class _MModbusRTUSlave(ModbusSlave):
    def __init__(self, uart, verbose=True, *args, **kwargs):
        self._verbose = verbose
        self.uart = uart
        super(_MModbusRTUSlave, self).__init__(
            sl_type="rtu",
            context=kwargs.get("context", None),
            device_address=kwargs.get("device_address", 1),
        )

    async def run_async(self):
        self._verbose and print("starting async rtu slave")
        while not self.stopped:
            self.tick()
            await asyncio.sleep(0.1)

    def run(self):
        self._verbose and print("starting rtu slave")
        while not self.stopped:
            self.tick()
            time.sleep(0.1)

    def tick(self):
        if not self.stopped and self.uart.any():
            rsp = self.uart.readline()
            frame = ModbusRTUFrame.parse_frame(rsp)
            resp = self.handle_message(frame).get_frame()
            self.uart.write(resp)
            cb = self.cb[frame.func_code]
            if cb is not None:
                db = {
                    1: "coils",
                    2: "discrete_inputs",
                    3: "holding_registers",
                    4: "input_registers",
                    5: "coils",
                    6: "holding_registers",
                    15: "coils",
                    16: "holding_registers",
                }[frame.func_code]
                if frame.func_code in [1, 2, 3, 4]:
                    data = self._get_data(frame.register, frame.length, self.context[db])
                    cb(frame.register, frame.length, data)
                if frame.func_code in [5, 6, 15, 16]:
                    cb(frame.register, frame.length, data)


class ModbusRTUSlave:
    def __new__(cls, *args, **kwargs):
        if sys.implementation.name == "cpython":
            return _CModbusRTUSlave(*args, **kwargs)
        elif sys.implementation.name == "micropython":
            return _MModbusRTUSlave(*args, **kwargs)


class ModbusTCPServer(ModbusSlave):
    def __init__(self, host, port, verbose=True, *args, **kwargs):
        self.host = host
        self.port = port
        self._verbose = verbose
        super(ModbusTCPServer, self).__init__(
            sl_type="tcp",
            context=kwargs.get("context", None),
            device_address=kwargs.get("device_address", 1),
        )

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)

    def run(self):
        while not self.stopped:
            conn, addr = self.sock.accept()
            self._verbose and print("new connection from {}".format(addr))
            while True:
                frame = conn.recv(256)
                if len(frame) > 0:
                    try:
                        res = self.handle_message(ModbusTCPFrame.parse_frame(frame)).get_frame()
                        self._verbose and print(res)
                        conn.send(res)
                    except:
                        break
                else:
                    break
            conn.close()
        self.sock.close()

    async def run_async(self):
        self._verbose and print("starting async tcp server on port {}".format(self.port))
        loop = asyncio.get_event_loop()
        self.sock.setblocking(False)
        while not self.stopped:
            conn, addr = await loop.sock_accept(self.sock)
            self._verbose and print("new connection from {}".format(addr))
            while True:
                frame = await loop.sock_recv(conn, 256)
                if len(frame) > 0:
                    req = ModbusTCPFrame.parse_frame(frame)
                    self._verbose and print("received Frame        {}".format(req))
                    res = self.handle_message(req)
                    self._verbose and print("responding with Frame {}".format(res))
                    conn.send(res.get_frame())
                else:
                    self._verbose and print("shutting down async server")
                    break
            conn.close()
        self.sock.close()

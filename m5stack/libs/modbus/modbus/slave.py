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
import select

if sys.implementation.name == "micropython":
    import micropython


class ModbusSlave:
    READ_COILS_EVENT = 0x01
    READ_DISCRETE_INPUTS_EVENT = 0x02
    READ_HOLDING_REGISTERS_EVENT = 0x03
    READ_INPUT_REGISTERS_EVENT = 0x04
    WRITE_SINGLE_COIL_EVENT = 0x05
    WRITE_SINGLE_REGISTER_EVENT = 0x06
    WRITE_MULTIPLE_COILS_EVENT = 0x0F
    WRITE_MULTIPLE_REGISTERS_EVENT = 0x10

    _available_register_types = (
        "coils",
        "discrete_inputs",
        "holding_registers",
        "input_registers",
    )

    _FUNCTION_MAP = {
        1: "coils",
        2: "discrete_inputs",
        3: "holding_registers",
        4: "input_registers",
        5: "coils",
        6: "holding_registers",
        15: "coils",
        16: "holding_registers",
    }

    def __init__(self, sl_type="tcp", context=None, ignore_unit_id=False, device_address=1):
        self.sl_type = sl_type
        self.context = context
        self.ignore_unit_id = ignore_unit_id
        self._device_address = device_address
        self.forward_message = None
        self.stopped = False
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

    def set_callback(self, event, callback):
        self.cb[event] = callback

    def _add_register_in_context(self, reg_type, register, value):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        added = False
        for reg in self.context[reg_type]:
            if reg["register"] <= register < reg["register"] + len(reg["value"]):
                # if register exists in the context
                idx = register - reg["register"]
                reg["value"][idx] = value
                added = True
            elif reg["register"] + 1 == register:
                # if register is at the end of the context
                reg["value"].append(value)
                added = True

        if not added:
            # if register is not in the context
            self.context[reg_type].append({"register": register, "value": [value]})

        # sort the registers in the context
        regs = self.context[reg_type]
        for i in range(len(regs)):
            for j in range(len(regs)):
                if regs[i]["register"] < regs[j]["register"]:
                    regs[i], regs[j] = regs[j], regs[i]

        # Merge registers with consecutive addresses
        for i in range(len(regs) - 1, -1, -1):
            if regs[i]["register"] == regs[i - 1]["register"] + len(regs[i - 1]["value"]):
                regs[i - 1]["value"].extend(regs[i]["value"])
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
            quantity = len(regs[i]["value"])
            if regs[i]["register"] <= register < regs[i]["register"] + quantity:
                idx = register - regs[i]["register"]
                if quantity == 1:
                    del regs[i]
                elif idx == 0:
                    regs[i]["register"] += 1
                    regs[i]["value"].pop(0)
                elif idx == quantity - 1:
                    regs[i]["value"].pop(-1)
                elif 0 < idx < quantity - 1:
                    new_regs.append(
                        {"register": regs[i]["register"], "value": regs[i]["value"][0:idx]}
                    )
                    new_regs.append(
                        {
                            "register": regs[i]["register"] + idx + 1,
                            "value": regs[i]["value"][idx + 1 :],
                        }
                    )
                    del regs[i]

        regs.extend(new_regs)
        # sort the registers in the context
        for i in range(len(regs)):
            for j in range(len(regs)):
                if regs[i]["register"] < regs[j]["register"]:
                    regs[i], regs[j] = regs[j], regs[i]

    def add_coil(self, register: int, value: bool) -> None:
        """Add a coil to the modbus register dictionary.

        Args:
            register (int): address of the coils. The address is 0x0000 to 0xFFFF.
            value (bool): Value to add. The value is True or False.

        """
        self._add_register_in_context("coils", register, value)

    def add_discrete_input(self, register: int, value: bool) -> None:
        """Add a discrete input to the modbus register dictionary.

        Args:
            register (int): address of the discrete inputs. The address is 0x0000 to 0xFFFF.
            value (bool): Value to add. The value is True or False.

        """
        self._add_register_in_context("discrete_inputs", register, value)

    def add_holding_register(self, register: int, value: int) -> None:
        """Add a holding register to the modbus register dictionary.

        Args:
            register (int): address of the holding registers. The address is 0x0000 to 0xFFFF.
            value (int): Value to add. The value is 0x0000 to 0xFFFF.

        """
        self._add_register_in_context("holding_registers", register, value)

    def add_input_register(self, register: int, value: int) -> None:
        """Add an input register to the modbus register dictionary.

        Args:
            register (int): address of the input registers. The address is 0x0000 to 0xFFFF.
            value (int): Value to add. The value is 0x0000 to 0xFFFF.

        """
        self._add_register_in_context("input_registers", register, value)

    def remove_coil(self, register: int) -> None:
        """Remove a coil from the modbus register dictionary.

        Args:
            register (int): address of the coils. The address is 0x0000 to 0xFFFF.

        """
        self._remove_register_from_context("coils", register)

    def remove_discrete_input(self, register: int) -> None:
        """Remove a discrete input from the modbus register dictionary.

        Args:
            register (int): address of the discrete inputs. The address is 0x0000 to 0xFFFF.

        """
        self._remove_register_from_context("discrete_inputs", register)

    def remove_holding_register(self, register: int) -> None:
        """Remove a holding register from the modbus register dictionary.

        Args:
            register (int): address of the holding registers. The address is 0x0000 to 0xFFFF.

        """
        self._remove_register_from_context("holding_registers", register)

    def remove_input_register(self, register) -> None:
        """Remove an input register from the modbus register dictionary.

        Args:
            register (int): address of the input registers. The address is 0x0000 to 0xFFFF.

        """
        self._remove_register_from_context("input_registers", register)

    def _get_reg_data(self, reg_type: str, register: int):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        for reg in self.context[reg_type]:
            if reg["register"] <= register < reg["register"] + len(reg["value"]):
                idx = register - reg["register"]
                return reg["value"][idx]

        raise KeyError("Register {} not found in context".format(register))

    def _set_reg_data(self, reg_type, register, value):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        for reg in self.context[reg_type]:
            if reg["register"] <= register < reg["register"] + len(reg["value"]):
                idx = register - reg["register"]
                reg["value"][idx] = value
                return

        raise KeyError("Register {} not found in context".format(register))

    def _set_reg_datablock(self, reg_type: str, register: int, block: list):
        if reg_type not in self._available_register_types:
            raise KeyError(
                "{} is Invalid register type of {}".format(
                    reg_type, self._available_register_types
                )
            )

        for reg in self.context[reg_type]:
            if reg["register"] <= register < reg["register"] + len(reg["value"]):
                idx = register - reg["register"]
                for i in range(idx, idx + len(block)):
                    reg["value"][i] = block[i - idx]
                # for new_value in block:
                #     reg["value"][idx] = new_value
                #     idx += 1
                return

        raise KeyError("Register {} not found in context".format(register))

    def get_coil(self, register: int) -> bool:
        """Get the coil value.

        Args:
            register (int): address of the coils. The address is 0x0000 to 0xFFFF.

        Returns:
            bool: Value of the coil. The value is True or False.
        """
        return self._get_reg_data("coils", register)

    def get_discrete_input(self, register: int) -> bool:
        """Get the discrete input value.

        Args:
            register (int): address of the discrete inputs. The address is 0x0000 to 0xFFFF.

        Returns:
            bool: Value of the discrete input. The value is True or False.
        """
        return self._get_reg_data("discrete_inputs", register)

    def get_holding_register(self, register: int) -> int:
        """Get the holding register value.

        Args:
            register (int): address of the holding registers. The address is 0x0000 to 0xFFFF.

        Returns:
            int: Value of the holding register. The value is 0x0000 to 0xFFFF
        """
        return self._get_reg_data("holding_registers", register)

    def get_input_register(self, register: int) -> int:
        """Get the input register value.

        Args:
            register (int): address of the input registers. The address is 0x0000 to 0xFFFF.

        Returns:
            int: Value of the input register. The value is 0x0000 to 0xFFFF
        """
        return self._get_reg_data("input_registers", register)

    def set_coil(self, register: int, value: bool) -> None:
        """Set the coil value.

        Args:
            register (int): address of the coils. The address is 0x0000 to 0xFFFF.
            value (bool): Value to add. The value is True or False.
        """
        self._set_reg_data("coils", register, value)

    def set_multi_coils(self, register: int, value: list) -> None:
        """Set the coil value.

        Args:
            register (int): Start address of the coils. The address is 0x0000 to 0xFFFF.
            value (bool): Values to write. The item of the list is True or False.
        """
        self._set_reg_datablock("coils", register, value)

    def set_discrete_input(self, register: int, value: bool) -> None:
        """Set the discrete input value.

        Args:
            register (int): address of the discrete inputs. The address is 0x0000 to 0xFFFF.
            value (bool): Value to add. The value is True or False.
        """
        self._set_reg_data("discrete_inputs", register, value)

    def set_multi_discrete_input(self, register: int, value: list) -> None:
        """Set the discrete input value.

        Args:
            register (int): Start address of the discrete inputs. The address is 0x0000 to 0xFFFF.
            Values to write. The item of the list is True or False.
        """
        self._set_reg_datablock("discrete_inputs", register, value)

    def set_holding_register(self, register: int, value: int) -> None:
        """Set the holding register value.

        Args:
            register (int): address of the holding registers. The address is 0x0000 to 0xFFFF.
            value (int): Value to add. The value is 0x0000 to 0xFFFF.
        """
        self._set_reg_data("holding_registers", register, value)

    def set_multi_holding_register(self, register: int, value: list) -> None:
        """Set the holding register value.

        Args:
            register (int): Start address of the holding registers. The address is 0x0000 to 0xFFFF.
            value (int): Values to write. The item of the list is 0x0000 to 0xFFFF.
        """
        self._set_reg_datablock("holding_registers", register, value)

    def set_input_register(self, register: int, value: int) -> None:
        """Set the input register value.

        Args:
            register (int): address of the input registers. The address is 0x0000 to 0xFFFF.
            value (int): Value to add. The value is 0x0000 to 0xFFFF.
        """
        self._set_reg_data("input_registers", register, value)

    def set_multi_input_register(self, register: int, value: list) -> None:
        """Set the discrete input value.

        Args:
            register (int): Start address of the input registers. The address is 0x0000 to 0xFFFF.
            Values to write. The item of the list is 0x0000 to 0xFFFF.
        """
        self._set_reg_datablock("input_registers", register, value)

    def stop(self) -> None:
        self.stopped = True

    def handle_message(self, frame):  # noqa: C901
        # TODO: Refactor this method
        if self.context is None:
            if self.forward_message is not None:
                return self.forward_message(frame)
            return

        db = self._FUNCTION_MAP[frame.func_code]

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
            quantity = len(reg["value"])
            if reg["register"] <= register < reg["register"] + quantity:
                if reg["register"] + quantity >= register + length:
                    return True
        return False

    def _get_data(self, register, length, regs):
        for reg in regs:
            if reg["register"] <= register < reg["register"] + len(reg["value"]):
                return reg["value"][
                    (register - reg["register"]) : (register - reg["register"] + length)
                ]

    def _set_data(self, register, length, data_Block, data):
        offset = register - data_Block["startAddr"]
        for i in range(length * 2):
            data_Block["registers"][2 * offset + i] = data[i]


class _CModbusRTUSlave(ModbusSlave):
    def __init__(self, uart, verbose=False, *args, **kwargs):
        self._verbose = verbose
        self.uart = uart
        super(_CModbusRTUSlave, self).__init__(sl_type="rtu", *args, **kwargs)

    def start(self):
        self.stopped = False
        if self.uart.inWaiting():
            self.uart.read_all()

    async def run_async(self):
        self._verbose and print("starting async rtu slave")
        while not self.stopped:
            self.tick()
            await asyncio.sleep(0.1)

    def tick(self):
        if not self.stopped and self.uart.inWaiting():
            rsp = self.uart.read_all()
            frame = ModbusRTUFrame.parse_frame(rsp, verbose=self._verbose)
            if frame is None or (
                self.ignore_unit_id is not True and frame.device_addr != self._device_address
            ):
                return
            resp = self.handle_message(frame).get_frame()
            self.uart.write(resp)
            cb = self.cb[frame.func_code]
            if cb is not None:
                db = self._FUNCTION_MAP[frame.func_code]
                data = self._get_data(frame.register, frame.length, self.context[db])
                if frame.func_code in [1, 2, 3, 4, 15, 16]:
                    cb(self, frame.register, data)
                if frame.func_code in [5, 6]:
                    cb(self, frame.register, data[0])


class _MModbusRTUSlave(ModbusSlave):
    def __init__(self, uart, verbose=False, *args, **kwargs):
        self._verbose = verbose
        self.uart = uart
        super(_MModbusRTUSlave, self).__init__(
            sl_type="rtu",
            context=kwargs.get("context", None),
            ignore_unit_id=kwargs.get("ignore_unit_id", False),
            device_address=kwargs.get("device_address", 1),
        )
        self.rsp = b""

    async def run_async(self):
        self._verbose and print("starting async rtu slave")
        while not self.stopped:
            self.tick()
            await asyncio.sleep(0.1)

    def start(self):
        self.stopped = False
        if self.uart.any() > 0:
            self.uart.read()

    def run(self):
        self._verbose and print("starting rtu slave")
        while not self.stopped:
            self.tick()
            time.sleep(0.1)

    def tick(self):
        if not self.stopped and self.uart.any():
            rsp = self.rsp + self.uart.read()
            frame = ModbusRTUFrame.parse_frame(rsp, verbose=self._verbose)
            if frame is None or (
                self.ignore_unit_id is not True and frame.device_addr != self._device_address
            ):
                if frame is None:
                    self.rsp = rsp  # Save response for next tick
                return
            self.rsp = b""  # Reset response
            resp = self.handle_message(frame).get_frame()
            self.uart.write(resp)
            cb = self.cb[frame.func_code]
            if cb is not None:
                db = self._FUNCTION_MAP[frame.func_code]
                if frame.func_code in [1, 2, 3, 4, 15, 16]:
                    data = self._get_data(frame.register, frame.length, self.context[db])
                    micropython.schedule(cb, (self, frame.register, data))
                if frame.func_code in [5, 6]:
                    data = self._get_data(frame.register, 1, self.context[db])
                    micropython.schedule(cb, (self, frame.register, data[0]))


class ModbusRTUSlave:
    def __new__(cls, *args, **kwargs):
        if sys.implementation.name == "cpython":
            return _CModbusRTUSlave(*args, **kwargs)
        elif sys.implementation.name == "micropython":
            return _MModbusRTUSlave(*args, **kwargs)


class _CModbusTCPServer(ModbusSlave):
    def __init__(self, host, port, verbose=False, *args, **kwargs):
        self.host = host
        self.port = port
        self._verbose = verbose
        super(_CModbusTCPServer, self).__init__(
            sl_type="tcp",
            context=kwargs.get("context", None),
            ignore_unit_id=kwargs.get("ignore_unit_id", False),
            device_address=kwargs.get("device_address", 1),
        )

    def start(self):
        self.poll = select.poll()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.poll.register(self.sock, select.POLLIN)
        self.clients = {}

    def run(self):
        while not self.stopped:
            conn, addr = self.sock.accept()
            self._verbose and print("new connection from {}".format(addr))
            while True:
                frame = conn.recv(256)
                if len(frame) > 0:
                    try:
                        frame = ModbusTCPFrame.parse_frame(frame, verbose=self._verbose)
                        if frame is None or (
                            self.ignore_unit_id is not True
                            and frame.device_addr != self._device_address
                        ):
                            return
                        res = self.handle_message(frame).get_frame()
                        self._verbose and print(res)
                        conn.send(res)
                    except:
                        break
                else:
                    break
            conn.close()
        self.sock.close()

    def tick(self):
        if not self.stopped:
            fds = self.poll.poll(10)
            for fd, event in fds:
                # fd == file no(int)
                # print(fd, event)
                if event & select.POLLIN:
                    if fd == self.sock.fileno():
                        conn, addr = self.sock.accept()
                        conn.setblocking(False)
                        self.poll.register(conn.fileno(), select.POLLIN)
                        self.clients[conn.fileno()] = conn
                        self._verbose and print(conn, "accept", addr)
                    else:
                        client = self.clients[fd]
                        frame = client.recv(256)
                        if len(frame) > 0:
                            frame = ModbusTCPFrame.parse_frame(frame, verbose=self._verbose)
                            if frame is None or (
                                self.ignore_unit_id is not True
                                and frame.unit_id != self._device_address
                            ):
                                self._verbose and print("unit id not match")
                                return
                            res = self.handle_message(frame).get_frame()
                            self._verbose and print(res)
                            client.send(res)
                            cb = self.cb[frame.func_code]
                            if cb is not None:
                                db = self._FUNCTION_MAP[frame.func_code]
                                if frame.func_code in [1, 2, 3, 4, 15, 16]:
                                    data = self._get_data(
                                        frame.register, frame.length, self.context[db]
                                    )
                                    micropython.schedule(cb, (self, frame.register, data))
                                if frame.func_code in [5, 6]:
                                    data = self._get_data(frame.register, 1, self.context[db])
                                    micropython.schedule(cb, (self, frame.register, data[0]))
                        else:
                            self._verbose and print(fd, "closed")
                            self.poll.unregister(fd)

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
                    req = ModbusTCPFrame.parse_frame(frame, verbose=self._verbose)
                    if req is None or (req.device_addr != self._device_address):
                        continue
                    self._verbose and print("received Frame        {}".format(req))
                    res = self.handle_message(req)
                    self._verbose and print("responding with Frame {}".format(res))
                    conn.send(res.get_frame())
                    cb = self.cb[frame.func_code]
                    if cb is not None:
                        db = self._FUNCTION_MAP[frame.func_code]
                        if frame.func_code in [1, 2, 3, 4, 15, 16]:
                            data = self._get_data(frame.register, frame.length, self.context[db])
                            micropython.schedule(cb, (self, frame.register, data))
                        if frame.func_code in [5, 6]:
                            data = self._get_data(frame.register, 1, self.context[db])
                            micropython.schedule(cb, (self, frame.register, data[0]))
                else:
                    self._verbose and print("shutting down async server")
                    break
            conn.close()
        self.sock.close()


class _MModbusTCPServer(ModbusSlave):
    def __init__(self, host, port, verbose=False, *args, **kwargs):
        self.host = host
        self.port = port
        self._verbose = verbose
        super(_MModbusTCPServer, self).__init__(
            sl_type="tcp",
            context=kwargs.get("context", None),
            ignore_unit_id=kwargs.get("ignore_unit_id", False),
            device_address=kwargs.get("device_address", 1),
        )

    def start(self):
        import select

        self.poll = select.poll()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.poll.register(self.sock, select.POLLIN)

    def run(self):
        while not self.stopped:
            conn, addr = self.sock.accept()
            self._verbose and print("new connection from {}".format(addr))
            while True:
                frame = conn.recv(256)
                if len(frame) > 0:
                    try:
                        frame = ModbusTCPFrame.parse_frame(frame, verbose=self._verbose)
                        if frame is None or (
                            self.ignore_unit_id is not True
                            and frame.unit_id != self._device_address
                        ):
                            return
                        res = self.handle_message(frame).get_frame()
                        self._verbose and print(res)
                        conn.send(res)
                    except:
                        break
                else:
                    break
            conn.close()
        self.sock.close()

    def tick(self):
        import select

        if not self.stopped:
            fds = self.poll.poll(10)
            for fd, event in fds:
                print(fd, event)
                if fd == self.sock:
                    conn, addr = self.sock.accept()
                    self.poll.register(conn, select.POLLIN)
                    self._verbose and print(conn, "accept", addr)
                else:
                    frame = fd.recv(256)
                    if len(frame) > 0:
                        frame = ModbusTCPFrame.parse_frame(frame, verbose=self._verbose)
                        if frame is None or (
                            self.ignore_unit_id is not True
                            and frame.unit_id != self._device_address
                        ):
                            return
                        res = self.handle_message(frame).get_frame()
                        self._verbose and print(res)
                        fd.send(res)
                        cb = self.cb[frame.func_code]
                        if cb is not None:
                            db = self._FUNCTION_MAP[frame.func_code]
                            if frame.func_code in [1, 2, 3, 4, 15, 16]:
                                data = self._get_data(
                                    frame.register, frame.length, self.context[db]
                                )
                                micropython.schedule(cb, (self, frame.register, data))
                            if frame.func_code in [5, 6]:
                                data = self._get_data(frame.register, 1, self.context[db])
                                micropython.schedule(cb, (self, frame.register, data[0]))
                    else:
                        self._verbose and print(fd, "closed")
                        self.poll.unregister(fd)

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
                    req = ModbusTCPFrame.parse_frame(frame, verbose=self._verbose)
                    if req is None or req.device_addr != self._device_address:
                        continue
                    self._verbose and print("received Frame        {}".format(req))
                    res = self.handle_message(req)
                    self._verbose and print("responding with Frame {}".format(res))
                    conn.send(res.get_frame())
                    cb = self.cb[frame.func_code]
                    if cb is not None:
                        db = self._FUNCTION_MAP[frame.func_code]
                        if frame.func_code in [1, 2, 3, 4, 15, 16]:
                            data = self._get_data(frame.register, frame.length, self.context[db])
                            micropython.schedule(cb, (self, frame.register, data))
                        if frame.func_code in [5, 6]:
                            data = self._get_data(frame.register, 1, self.context[db])
                            micropython.schedule(cb, (self, frame.register, data[0]))
                else:
                    self._verbose and print("shutting down async server")
                    break
            conn.close()
        self.sock.close()


class ModbusTCPServer:
    def __new__(cls, *args, **kwargs):
        if sys.implementation.name == "cpython":
            return _CModbusTCPServer(*args, **kwargs)
        elif sys.implementation.name == "micropython":
            return _MModbusTCPServer(*args, **kwargs)

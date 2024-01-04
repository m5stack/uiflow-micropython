# Source: https://github.com/pycom/pycom-modbus/tree/master/uModbus (2018-07-16)
# This file has been modified and differ from its source version.
from . import uFunctions as functions
from . import uConst as Const
from machine import UART
from machine import Pin
import struct
import time
import machine


class uSerial:
    def __init__(
        self,
        uart_id,
        tx,
        rx,
        baudrate=9600,
        data_bits=8,
        stop_bits=1,
        parity=None,
        ctrl_pin=None,
        debug=False,
    ):
        self._mdbus_uart = UART(
            uart_id,
            tx=tx,
            rx=rx,
            baudrate=baudrate,
            bits=data_bits,
            parity=parity,
            stop=stop_bits,
            timeout_char=10,
        )
        if ctrl_pin is not None:
            self._ctrlPin = Pin(ctrl_pin, mode=Pin.OUT)
        else:
            self._ctrlPin = None
        self.char_time_ms = (1000 * (data_bits + stop_bits + 2)) // baudrate
        self._modbus_debug = debug

    def _calculate_crc16(self, data):
        crc = 0xFFFF

        for char in data:
            crc = (crc >> 8) ^ Const.CRC16_TABLE[((crc) ^ char) & 0xFF]
        return struct.pack("<H", crc)

    def _bytes_to_bool(self, byte_list):
        bool_list = []
        for index, byte in enumerate(byte_list):
            bool_list.extend([bool(byte & (1 << n)) for n in range(8)])
        return bool_list

    def _to_short(self, byte_array, signed=True):
        response_quantity = int(len(byte_array) / 2)
        fmt = ">" + (("h" if signed else "H") * response_quantity)

        return struct.unpack(fmt, byte_array)

    def _exit_read(self, response):
        if response[1] >= Const.ERROR_BIAS:
            if len(response) < Const.ERROR_RESP_LEN:
                return False
        elif Const.READ_COILS <= response[1] <= Const.READ_INPUT_REGISTER:
            expected_len = Const.RESPONSE_HDR_LENGTH + 1 + response[2] + Const.CRC_LENGTH
            if len(response) < expected_len:
                return False
        elif len(response) < Const.FIXED_RESP_LEN:
            return False
        return True

    def _mdbus_uart_read(self, timeout=2000):
        response = bytearray()
        loop_max = int(timeout / 50)
        for x in range(1, loop_max):
            if self._mdbus_uart.any():
                response.extend(self._mdbus_uart.read())
                # variable length function codes may require multiple reads
                if self._exit_read(response):
                    break
            time.sleep(0.05)
        return response

    def _send_receive(self, modbus_pdu, slave_addr, count, timeout=2000):
        serial_pdu = bytearray()
        serial_pdu.append(slave_addr)
        serial_pdu.extend(modbus_pdu)

        crc = self._calculate_crc16(serial_pdu)
        serial_pdu.extend(crc)

        # flush the Rx FIFO
        read_data = self._mdbus_uart.read()
        if read_data is not None:
            self.print_debug("ModBus", "R <= {}".format(self.BytesToHexStr(read_data)))
        if self._ctrlPin:
            self._ctrlPin(1)

        self.print_debug("ModBus", "T => {}".format(self.BytesToHexStr(serial_pdu)))
        self._mdbus_uart.write(serial_pdu)
        if self._ctrlPin:
            while not self._mdbus_uart.wait_tx_done(2):
                machine.idle()
            time.sleep_ms(1 + self.char_time_ms)
            self._ctrlPin(0)
        return self._validate_resp_hdr(
            self._mdbus_uart_read(timeout), slave_addr, modbus_pdu[0], count
        )

    def _validate_resp_hdr(self, response, slave_addr, function_code, count):
        if len(response):
            self.print_debug("ModBus", "R <= {}".format(self.BytesToHexStr(response)))

            resp_crc = response[-Const.CRC_LENGTH :]
            expected_crc = self._calculate_crc16(response[0 : len(response) - Const.CRC_LENGTH])
            if (resp_crc[0] != expected_crc[0]) or (resp_crc[1] != expected_crc[1]):
                raise OSError("invalid response CRC")

            if response[0] != slave_addr:
                raise ValueError("wrong slave address")

            if response[1] == (function_code + Const.ERROR_BIAS):
                raise ValueError("slave returned exception code: {:d}".format(response[2]))

            hdr_length = (Const.RESPONSE_HDR_LENGTH + 1) if count else Const.RESPONSE_HDR_LENGTH
            return response[hdr_length : len(response) - Const.CRC_LENGTH]

    def read_coils(self, slave_addr, starting_addr, coil_qty, timeout=2000):
        modbus_pdu = functions.read_coils(starting_addr, coil_qty)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True, timeout)
        if resp_data != None:
            status_pdu = self._bytes_to_bool(resp_data)
            return status_pdu

    def read_discrete_inputs(self, slave_addr, starting_addr, input_qty, timeout=2000):
        modbus_pdu = functions.read_discrete_inputs(starting_addr, input_qty)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True, timeout)
        if resp_data != None:
            status_pdu = self._bytes_to_bool(resp_data)
            return status_pdu

    def read_holding_registers(
        self, slave_addr, starting_addr, register_qty, signed=True, timeout=2000
    ):
        modbus_pdu = functions.read_holding_registers(starting_addr, register_qty)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True, timeout)
        if resp_data != None:
            register_value = self._to_short(resp_data, signed)
            return list(register_value)

    def read_input_registers(
        self, slave_addr, starting_address, register_quantity, signed=True, timeout=2000
    ):
        modbus_pdu = functions.read_input_registers(starting_address, register_quantity)

        resp_data = self._send_receive(modbus_pdu, slave_addr, True, timeout)
        if resp_data != None:
            register_value = self._to_short(resp_data, signed)
            return list(register_value)

    def write_single_coil(self, slave_addr, output_address, output_value, timeout=2000):
        modbus_pdu = functions.write_single_coil(output_address, output_value)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False, timeout)
        if resp_data != None:
            operation_status = functions.validate_resp_data(
                resp_data,
                Const.WRITE_SINGLE_COIL,
                output_address,
                value=output_value,
                signed=False,
            )
            return operation_status

    def write_single_register(
        self, slave_addr, register_address, register_value, signed=True, timeout=2000
    ):
        modbus_pdu = functions.write_single_register(register_address, register_value, signed)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False, timeout)
        if resp_data != None:
            operation_status = functions.validate_resp_data(
                resp_data,
                Const.WRITE_SINGLE_REGISTER,
                register_address,
                value=register_value,
                signed=signed,
            )
            return operation_status

    def write_multiple_coils(self, slave_addr, starting_address, output_values, timeout=2000):
        modbus_pdu = functions.write_multiple_coils(starting_address, output_values)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False, timeout)
        if resp_data != None:
            operation_status = functions.validate_resp_data(
                resp_data,
                Const.WRITE_MULTIPLE_COILS,
                starting_address,
                quantity=len(output_values),
            )
            return operation_status

    def write_multiple_registers(
        self, slave_addr, starting_address, register_values, signed=True, timeout=2000
    ):
        modbus_pdu = functions.write_multiple_registers(starting_address, register_values, signed)

        resp_data = self._send_receive(modbus_pdu, slave_addr, False, timeout)
        if resp_data != None:
            operation_status = functions.validate_resp_data(
                resp_data,
                Const.WRITE_MULTIPLE_REGISTERS,
                starting_address,
                quantity=len(register_values),
            )
            return operation_status

    def BytesToHexStr(self, bins):
        return "".join(["%02X" % x for x in bins]).strip()

    def print_debug(self, tag, msg):
        if self._modbus_debug:
            print("[ \033[32m{}\033[0m ] {}".format(tag, msg))

    def close(self):
        if self._mdbus_uart is None:
            return
        try:
            self._mdbus_uart.deinit()
        except Exception:
            pass

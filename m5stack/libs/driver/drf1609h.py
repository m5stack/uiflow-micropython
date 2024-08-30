# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import time


class DeviceParameter:
    device_type = 0x02
    pan_id = 0x1620
    channel = 20
    transfer_mode = 0x01
    custom_address = 0x6677
    baud_rate = 0x06
    data_bits = 0x01
    stop_bits = 0x01
    parity = 0x01
    ant_type = 0x00
    mac = None
    short_address = 0xFFFE
    encryption_enable = 0xA1
    password = b"\x00\x00\x00\x00"

    def deepcopy(self):
        n = DeviceParameter()
        n.device_type = self.device_type
        n.pan_id = self.pan_id
        n.channel = self.channel
        n.transfer_mode = self.transfer_mode
        n.custom_address = self.custom_address
        n.baud_rate = self.baud_rate
        n.data_bits = self.data_bits
        n.stop_bits = self.stop_bits
        n.parity = self.parity
        n.ant_type = self.ant_type
        n.mac = self.mac
        n.short_address = self.short_address
        n.encryption_enable = self.encryption_enable
        n.password = self.password
        return n


class DeviceParameterList:
    def __init__(self) -> None:
        self.nodes = []

    def __len__(self):
        return len(self.nodes)

    def __getitem__(self, key):
        return self.nodes[key]

    def __setitem__(self, key, value):
        self.nodes[key] = value

    def append(self, node):
        self.nodes.append(node)

    def pop(self, index=-1):
        self.nodes.pop(index=index)

    def update(self, new_node):
        for index, node in enumerate(self.nodes):
            if node.custom_address == new_node.custom_address:
                del self.nodes[index]
        self.nodes.append(new_node)

    def index(self, short_address):
        for node in self.nodes:
            if node.custom_address == short_address:
                return node
        return None


class DRF1609H:
    def __init__(self, uart, verbose=False) -> None:
        self._uart = uart
        self._verbose = verbose

        self._buffer7 = bytearray(7)
        self._buffer22 = bytearray(22)
        self._buffer33 = bytearray(33)
        self._buffer39 = bytearray(39)
        self._buffer96 = bytearray(96)
        self.manufacturer = None
        self.firmware_version = None
        self.parameter = DeviceParameter()
        self.router = DeviceParameter()
        self.node_list = DeviceParameterList()
        if self.connect_command() is False:
            raise Exception("DRF1609H Connection failed")
        self.read_module_param_command()
        self.restart_command()

    def unpack_p2p_data(self, rxdata):
        self._verbose and print("Recv buffer: %s" % (" ".join(f"{byte:02x}" for byte in rxdata)))
        (rxdata_len,) = struct.unpack_from("!B", rxdata, 1)
        (dest_address,) = struct.unpack_from("!H", rxdata, 2)
        (data,) = struct.unpack_from("!%ds" % (rxdata_len), rxdata, 4)
        (src_address,) = struct.unpack_from("!H", rxdata, 4 + rxdata_len)
        return (dest_address, data, src_address)

    def receive(self):
        _buffer = b""
        if self._uart.any():
            _buffer += self._uart.read(1)
            if _buffer[0] == 0xED:
                _buffer += self._uart.read(1)
                total = 1 + 1 + 2 + _buffer[1] + 2
                while len(_buffer) < total:
                    _buffer += self._uart.read()
                return self.unpack_p2p_data(_buffer)
            else:
                _buffer += self._uart.read()
                return (0xFFFF, _buffer, -1)
        return None

    def p2p_transmission(self, address, data):
        struct.pack_into("!B", self._buffer96, 0, 0xED)
        struct.pack_into("!B", self._buffer96, 1, len(data))
        struct.pack_into("!H", self._buffer96, 2, address)
        struct.pack_into("!%ds" % (len(data)), self._buffer96, 4, data)
        self._uart.write(memoryview(self._buffer96)[: 4 + len(data)])

    def broadcast(self, data):
        self.p2p_transmission(0xFFFF, data)

    def connect_command(self):
        rxdata, err_code, status = self.command(0xFC, data=b"\x04\x44\x54\x4b\x52\x46")
        if status is False or err_code != 0x0A:
            return False
        (self.manufacturer, self.firmware_version) = struct.unpack_from("!3sH", rxdata, 1)
        self.manufacturer = self.manufacturer.decode()
        self.firmware_version = round(self.firmware_version / 10, 1)
        return True

    def restart_command(self):
        _, err_code, status = self.command(0xFC, data=b"\x06\x44\x54\x4b\xaa\xbb")
        if status and err_code == 0x0A:
            time.sleep(3)
            return True
        return False

    def _unpack_module_param(self, rxdata):
        offset = 1
        (self.parameter.device_type,) = struct.unpack_from("!B", rxdata, offset + 0)
        (self.parameter.pan_id,) = struct.unpack_from("!H", rxdata, offset + 1)
        (self.parameter.channel,) = struct.unpack_from("!B", rxdata, offset + 3)
        (self.parameter.transfer_mode,) = struct.unpack_from("!B", rxdata, offset + 4)
        (self.parameter.custom_address,) = struct.unpack_from("!H", rxdata, offset + 5)
        (self.parameter.baud_rate,) = struct.unpack_from("!B", rxdata, offset + 9)
        (self.parameter.data_bits,) = struct.unpack_from("!B", rxdata, offset + 10)
        (self.parameter.stop_bits,) = struct.unpack_from("!B", rxdata, offset + 11)
        (self.parameter.parity,) = struct.unpack_from("!B", rxdata, offset + 12)
        (self.parameter.ant_type,) = struct.unpack_from("!B", rxdata, offset + 15)
        (self.parameter.mac,) = struct.unpack_from("!8s", rxdata, offset + 16)

        (self.router.device_type,) = struct.unpack_from("!B", rxdata, offset + 24)
        (self.router.pan_id,) = struct.unpack_from("!H", rxdata, offset + 25)
        (self.router.channel,) = struct.unpack_from("!B", rxdata, offset + 27)
        (self.router.transfer_mode,) = struct.unpack_from("!B", rxdata, offset + 28)
        (self.router.custom_address,) = struct.unpack_from("!B", rxdata, offset + 29)
        (self.router.baud_rate,) = struct.unpack_from("!B", rxdata, offset + 33)
        (self.router.data_bits,) = struct.unpack_from("!B", rxdata, offset + 34)
        (self.router.stop_bits,) = struct.unpack_from("!B", rxdata, offset + 35)
        (self.router.parity,) = struct.unpack_from("!B", rxdata, offset + 36)
        (self.router.ant_type,) = struct.unpack_from("!B", rxdata, offset + 39)
        (self.router.short_address,) = struct.unpack_from("!H", rxdata, offset + 40)
        if self.firmware_version >= 7.2:
            (self.router.encryption_enable,) = struct.unpack_from("!B", rxdata, offset + 43)
            (self.router.password,) = struct.unpack_from("!4s", rxdata, offset + 44)

    def _pack_module_param(self, txdata):
        struct.pack_into("!B", txdata, 0, 0x07)
        offset = 1
        struct.pack_into("!B", txdata, offset + 0, self.parameter.device_type)
        struct.pack_into("!H", txdata, offset + 1, self.parameter.pan_id)
        struct.pack_into("!B", txdata, offset + 3, self.parameter.channel)
        struct.pack_into("!B", txdata, offset + 4, self.parameter.transfer_mode)
        struct.pack_into("!H", txdata, offset + 5, self.parameter.custom_address)
        struct.pack_into("!H", txdata, offset + 7, 0xAABB)
        struct.pack_into("!B", txdata, offset + 9, self.parameter.baud_rate)
        struct.pack_into("!B", txdata, offset + 10, self.parameter.data_bits)
        struct.pack_into("!B", txdata, offset + 11, self.parameter.stop_bits)
        struct.pack_into("!B", txdata, offset + 12, self.parameter.parity)
        struct.pack_into("!H", txdata, offset + 13, 0x05A6)
        struct.pack_into("!B", txdata, offset + 15, self.parameter.ant_type)

        struct.pack_into("!B", txdata, offset + 16, self.router.device_type)
        struct.pack_into("!H", txdata, offset + 17, self.router.pan_id)
        struct.pack_into("!B", txdata, offset + 19, self.router.channel)
        struct.pack_into("!B", txdata, offset + 20, self.router.transfer_mode)
        struct.pack_into("!H", txdata, offset + 21, self.router.custom_address)
        struct.pack_into("!H", txdata, offset + 23, 0xCCDD)
        struct.pack_into("!B", txdata, offset + 25, self.router.baud_rate)
        struct.pack_into("!B", txdata, offset + 26, self.router.data_bits)
        struct.pack_into("!B", txdata, offset + 27, self.router.stop_bits)
        struct.pack_into("!B", txdata, offset + 28, self.router.parity)
        struct.pack_into("!H", txdata, offset + 29, 0x05A6)
        struct.pack_into("!B", txdata, offset + 31, self.router.ant_type)
        if self.firmware_version >= 7.2:
            struct.pack_into("!B", txdata, offset + 32, 0x01)
            struct.pack_into("!B", txdata, offset + 33, self.router.encryption_enable)
            struct.pack_into("!4s", txdata, offset + 34, self.router.password)

    def read_module_param_command(self):
        if self.firmware_version in (7.0, 7.1):
            rxdata, err_code, status = self.command(0xFC, data=b"\x05\x44\x54\x4b\x52\x46")
            if err_code == 0x0A and status:
                self._unpack_module_param(rxdata)
                return True
        elif self.firmware_version >= 7.2:
            rxdata, err_code, status = self.command(0xFC, data=b"\x0e\x44\x54\x4b\x52\x46")
            if err_code == 0x0A and status:
                self._unpack_module_param(rxdata)
                return True
        return False

    def write_module_param_command(self):
        txdata = self._buffer39 if self.firmware_version >= 7.2 else self._buffer33
        self._pack_module_param(txdata)
        _, err_code, status = self.command(0xFC, data=txdata)
        return False if ((status is False) or (err_code != 0x0A)) else True

    def query_enddevice_position_command(self):
        if self.firmware_version >= 7.2:
            self.command(0xFC, data=b"\x0b\x44\x54\x4b\x52\x46")
            # TODO

    def query_node_signal_strength(self):
        total_hops = -1
        last_router_adrress = 0x0000
        strength = -1
        if self.firmware_version >= 7.2:
            rxdata, err_code, status = self.command(0xFC, data=b"\x0c\x44\x54\x4b\x52\x46")
            if err_code == 0x0A and status:
                (total_hops, last_router_adrress, strength) = struct.unpack_from("!BHB", rxdata, 0)
        return (total_hops, last_router_adrress, strength)

    def _unpack_node_param(self, rxdata):
        offset = 1
        node_parameter = DeviceParameter()
        (node_parameter.device_type,) = struct.unpack_from("!B", rxdata, offset + 0)
        (node_parameter.pan_id,) = struct.unpack_from("!H", rxdata, offset + 1)
        (node_parameter.channel,) = struct.unpack_from("!B", rxdata, offset + 3)
        (node_parameter.transfer_mode,) = struct.unpack_from("!B", rxdata, offset + 4)
        (node_parameter.custom_address,) = struct.unpack_from("!H", rxdata, offset + 5)
        (node_parameter.baud_rate,) = struct.unpack_from("!B", rxdata, offset + 9)
        (node_parameter.data_bits,) = struct.unpack_from("!B", rxdata, offset + 10)
        (node_parameter.stop_bits,) = struct.unpack_from("!B", rxdata, offset + 11)
        (node_parameter.parity,) = struct.unpack_from("!B", rxdata, offset + 12)
        (node_parameter.ant_type,) = struct.unpack_from("!B", rxdata, offset + 15)
        (node_parameter.mac,) = struct.unpack_from("!8s", rxdata, offset + 16)
        (node_parameter.encryption_enable,) = struct.unpack_from("!B", rxdata, offset + 24)
        (node_parameter.password,) = struct.unpack_from("!4s", rxdata, offset + 25)
        self.node_list.update(node_parameter)

    def read_node_param_command(self, short_address):
        if self.firmware_version >= 8.4:
            txdata = bytearray(6)
            struct.pack_into("!4s", txdata, 0, b"\x10\x44\x54\x4b")
            struct.pack_into("!H", txdata, 4, short_address)
            rxdata, err_code, status = self.command(0xFC, data=txdata)
            if err_code == 0x0A and status:
                self._unpack_node_param(rxdata)

    def _pack_node_param(self, txdata, short_address, node_parameter: DeviceParameter):
        struct.pack_into("!4s", txdata, 0, b"\x11\x44\x54\x4b")
        struct.pack_into("!H", txdata, 5, short_address)
        offset = 6
        struct.pack_into("!B", txdata, offset + 0, node_parameter.device_type)
        struct.pack_into("!H", txdata, offset + 1, node_parameter.pan_id)
        struct.pack_into("!B", txdata, offset + 3, node_parameter.channel)
        struct.pack_into("!B", txdata, offset + 4, node_parameter.transfer_mode)
        struct.pack_into("!H", txdata, offset + 5, node_parameter.custom_address)
        struct.pack_into("!H", txdata, offset + 7, 0xAABB)
        struct.pack_into("!B", txdata, offset + 9, node_parameter.baud_rate)
        struct.pack_into("!B", txdata, offset + 10, node_parameter.data_bits)
        struct.pack_into("!B", txdata, offset + 11, node_parameter.stop_bits)
        struct.pack_into("!B", txdata, offset + 12, node_parameter.parity)
        struct.pack_into("!H", txdata, offset + 13, 0x05A6)
        struct.pack_into("!B", txdata, offset + 15, node_parameter.ant_type)

    def write_node_param_command(self, short_address):
        if self.firmware_version >= 8.4:
            node = self.node_list.index(short_address)
            if node is None:
                node = DeviceParameter()
                node.short_address = short_address
            else:
                node = node.deepcopy()
            self._pack_node_param(self._buffer22, short_address, node)
            _, err_code, status = self.command(0xFC, data=self._buffer22)
            if status is True and err_code == 0x0A:
                self.node_list.update(node)
                return True
            return False
        else:
            return False

    def restart_node_command(self, short_address):
        if self.firmware_version >= 8.4:
            struct.pack_into("!4sHB", self._buffer7, 0, b"\x15\x44\x54\x4b", short_address, 0xA9)
            _, err_code, status = self.command(0xFC, data=self._buffer22)
            return False if ((status is False) or (err_code != 0x0A)) else True
        else:
            return False

    def join_network_command(self):
        if self.firmware_version >= 8.4:
            _, err_code, status = self.command(0xFC, data=b"\x19\x44\x54\x4b\xac")
            return False if ((status is False) or (err_code != 0x0A)) else True
        else:
            return False

    def command(self, cmd, data=b"", timeout=5000):
        self._send(cmd, data)
        return self._receive(timeout=timeout)

    def _send(self, cmd, data=b""):
        checksum = self._checksum(cmd, len(data), data)
        frame = struct.pack(
            "!BB%dsB" % len(data),
            cmd,
            len(data),
            data,
            checksum,
        )
        self._verbose and print("Frame to send: %s" % (" ".join(f"{byte:02x}" for byte in frame)))
        self._uart.write(frame)

    def _receive(self, timeout=3000):
        _buffer = b""
        startpos = -1
        count = timeout
        l = -1
        while count > 0:
            if self._uart.any() == 0:
                time.sleep(0.01)
                count -= 10
                continue
            _buffer += self._uart.read(1)

            if startpos == -1:
                startpos = _buffer.find(b"\xfa")
                continue
            if l == -1 and startpos != -1 and (len(_buffer) - startpos) > 1:
                l = _buffer[startpos + 1] + 4
            if l != -1 and l == (len(_buffer) - startpos):
                break

        if startpos != -1 and l != -1:
            self._verbose and print(
                "Recv buffer: %s" % (" ".join(f"{byte:02x}" for byte in _buffer))
            )
            frame = _buffer[startpos : startpos + l]
            cmd, length, err_code = struct.unpack_from("!BBB", frame, 0)
            rxdata, checksum = struct.unpack_from("!%dsB" % (length), frame, 3)
            if self._checksum(cmd, err_code, length, rxdata) != checksum:
                self._verbose and print(
                    "Invalid checksum: %s, data: 0x%s"
                    % (checksum, " ".join(f"{byte:02x}" for byte in frame))
                )
                return (b"", -1, False)
            return (rxdata, err_code, True if cmd == 0xFA else False)
        else:
            self._verbose and print("Malformed packet received, ignore it")
            return (b"", -1, False)

    def _checksum(self, *args):
        chcksum = 0
        for arg in args:
            if isinstance(arg, int):
                chcksum += arg
                continue
            for x in arg:
                chcksum += x
        return chcksum & 0xFF

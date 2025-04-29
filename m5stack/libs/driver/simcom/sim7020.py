# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import socket
import machine
import micropython
from driver.umodem import modem as umodem
from driver.umodem.parser import Parser
from driver.simcom.common import utils
from driver.simcom.toolkit import requests2
from driver.simcom.toolkit import umqtt


class SIMComError(Exception):
    D_GENERIC = 0
    D_TCPIP_ERR_INFO = 1  # 11.5
    D_TCPIP_ERR = 2  # 11.6
    D_DNS_ERROR_CODE = 3

    _err_desc = {
        D_GENERIC: {
            2: "AT command timeout({})",
        },
        D_DNS_ERROR_CODE: {
            10: "DNS GENERAL ERROR({})",
        },
        D_TCPIP_ERR_INFO: {
            0: "Connection time out({})",
            1: "Bind port failed({})",
            2: "Port overflow({})",
            3: "Create socket failed({})",
            4: "Network is already opened({})",
            5: "Network is already closed({})",
            6: "No clients connected({})",
            7: "No active client({})",
            8: "Network not opened({})",
            9: "Client index overflow({})",
            10: "Connection is already created({})",
            11: "Connection is not created({})",
            12: "Invalid parameter({})",
            13: "Operation not supported({})",
            14: "DNS query failed({})",
            15: "TCP busy({})",
            16: "Netclose failed for socket opened({})",
            17: "Sending time out({})",
            18: "Sending failure for network error({})",
            19: "Open failure for network error({})",
            20: "Server is already listening({})",
            21: "No data({})",
            22: "Port overflow({})",
        },
        D_TCPIP_ERR: {
            0: "Operation succeeded({})",
            1: "Network failure({})",
            2: "Network not opened({})",
            3: "Wrong parameter({})",
            4: "Operation not supported({})",
            5: "Failed to create socket({})",
            6: "Failed to bind socket({})",
            7: "TCP server is already listening({})",
            8: "Busy({})",
            9: "Sockets opened({})",
            10: "Timeout({})",
            11: "DNS parse failed for AT+CIPOPEN({})",
            12: "Unknown error({})",
        },
    }

    def __init__(self, *args):
        if len(args) == 1:
            super().__init__(args[0])
            return
        elif len(args) == 3:
            domain, errno, cmd = args
            msg = self._err_desc[domain].get(errno, "Unknown error({})")
            super().__init__(msg.format(repr(cmd)))


# TCP/UDP socket
class _socket:
    AF_INET = socket.AF_INET
    AF_INET6 = socket.AF_INET6

    SOCK_STREAM = socket.SOCK_STREAM
    SOCK_DGRAM = socket.SOCK_DGRAM
    SOCK_RAW = socket.SOCK_RAW

    IPPROTO_IP = socket.IPPROTO_IP
    IPPROTO_TCP = socket.IPPROTO_TCP
    IPPROTO_UDP = socket.IPPROTO_UDP

    _proto_type = {
        IPPROTO_TCP: "TCP",
        IPPROTO_UDP: "UDP",
    }

    _STATE_OPEN = 0
    _STATE_CLOSE = 1

    def __init__(self, modem: "SIM7020", af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP):
        self._modem = modem
        self._domain = af
        self._type = type
        self._proto = proto
        self._fd = self._modem.apply_fd()
        self._address = None
        if self._fd == -1:
            raise SIMComError("No available socket")

        self._state = self._STATE_CLOSE
        self._ringio = micropython.RingIO(1500)
        self._timeout = 2000
        self.blocking = False

    def __del__(self):
        self.close()

    def close(self) -> None:
        if self._fd == -1:
            return
        cmd = umodem.Command(
            "+CIPCLOSE",
            umodem.Command.CMD_WRITE,
            self._fd,
            rsp1="CLOSE OK",
            timeout=10000,
        )

        self._modem.execute(cmd)
        self._modem.release_fd(self._fd)
        self._fd = -1
        self._state = self._STATE_CLOSE
        if hasattr(self, "_local_port"):
            self._modem.release_port(self._local_port)

    def bind(self, address):
        pass

    def listen(self, backlog):
        pass

    def accept(self):
        pass

    def connect(self, address: tuple[str, int]):
        if self._fd == -1:
            raise SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return

        self._address = address
        # _fd is connect num
        cmd = umodem.Command(
            "+CIPSTART",
            umodem.Command.CMD_WRITE,
            self._fd,
            str(self._proto_type.get(self._proto, "")),
            str(address[0]),
            str(address[1]),
            rsp1="CONNECT OK",
            timeout=160000,
        )
        resp = self._modem.execute(cmd)
        if resp.status_code == resp.ERR_NONE:
            self._state = self._STATE_OPEN
            return True
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cmd)
        elif resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("{},".format(self._fd).encode())
            err = parser.parseutil(b"\r\n")
            raise SIMComError(err.decode())

    def send(self, data: bytes | str | bytearray) -> int:
        # data type check
        data = utils.converter(data, bytes)
        # print(f"tcp data: {data}")
        total_length = len(data)
        total_sent = 0

        max_segment_size = 1460

        while total_sent < total_length:
            segment_size = min(max_segment_size, total_length - total_sent)
            segment_data = data[total_sent : total_sent + segment_size]

            cmd = umodem.Command(
                "+CIPSEND",
                umodem.Command.CMD_WRITE,
                self._fd,
                segment_size,
                rsp1=">",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.execute(cmd, line_end="")
            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("+CME ERROR ".encode())
                err = parser.parseutil(b"\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, err, cmd.cmd)
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            self._modem.uart.write(segment_data)

            cmd = umodem.Command(
                "+CIPSEND",
                umodem.Command.CMD_EXECUTION,
                rsp1="SEND OK",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.response_at_command2(cmd)

            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("{},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
                raise SIMComError(err.decode())
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            total_sent += segment_size
            # print(f"Sent segment: {segment_size} bytes, Total: {total_sent}/{total_length}")

        return total_length

    def sendall(self, data: bytes | str | bytearray) -> None:
        self.send(data)

    def sendto(self, data: bytes | str | bytearray, address) -> int:
        if self._state == self._STATE_CLOSE:
            self._local_port = self._modem.apply_port()
            cipopen = umodem.Command(
                "+CIPSTART",
                umodem.Command.CMD_WRITE,
                self._fd,
                str(self._proto_type.get(self.IPPROTO_UDP, "")),
                str(address[0]),
                str(address[1]),
                rsp1="CONNECT OK",
                timeout=self._modem._default_timeout,
            )
            resp: umodem.Response = self._modem.execute(cipopen)
            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("{},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
                raise SIMComError(err.decode())
                raise SIMComError(err.decode())
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cipopen.cmd)
            self._state = self._STATE_OPEN

        # data type check
        data = utils.converter(data, bytes)
        total_length = len(data)
        total_sent = 0

        max_segment_size = 1460

        while total_sent < total_length:
            segment_size = min(max_segment_size, total_length - total_sent)
            segment_data = data[total_sent : total_sent + segment_size]

            cmd = umodem.Command(
                "+CIPSEND",
                umodem.Command.CMD_WRITE,
                self._fd,
                segment_size,
                rsp1=">",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.execute(cmd, line_end="")
            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("+CME ERROR ".encode())
                err = parser.parseutil(b"\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, err, cmd.cmd)
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            self._modem.uart.write(segment_data)

            cmd = umodem.Command(
                "+CIPSEND",
                umodem.Command.CMD_EXECUTION,
                rsp1="SEND OK",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.response_at_command2(cmd)

            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("{},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
                raise SIMComError(err.decode())
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            total_sent += segment_size
            # print(f"Sent segment: {segment_size} bytes, Total: {total_sent}/{total_length}")

        return total_length

    def _recv(self) -> None:
        ciprxget = umodem.Command(
            "+CIPRXGET",
            umodem.Command.CMD_WRITE,
            4,
            self._fd,
            timeout=self._modem._default_timeout,
        )
        resp = self._modem.execute(ciprxget)
        if resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("+CME ERROR ".encode())
            err = parser.parseutil(b"\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR, err, ciprxget.cmd)
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, resp.status_code, ciprxget.cmd)

        parser = Parser(resp.content)
        parser.skipuntil("+CIPRXGET: 4,{},".format(self._fd).encode())
        to_recv = parser.parseint(b"\r\n")
        # print(f"to_recv: {to_recv}")
        if to_recv == 0:
            return

        to_recv = (1500 - self._ringio.any()) if to_recv > (1500 - self._ringio.any()) else to_recv

        ciprxget = umodem.Command(
            "+CIPRXGET",
            umodem.Command.CMD_WRITE,
            2,
            self._fd,
            to_recv,
            timeout=self._modem._default_timeout,
        )
        resp = self._modem.execute(ciprxget)
        if resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("+CME ERROR ".encode())
            errno = parser.parseutil(b"\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR_INFO, errno, ciprxget.cmd)
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, resp.status_code, ciprxget.cmd)

        # prase data
        parser = Parser(resp.content)
        parser.skipuntil("+CIPRXGET: 2,{},".format(self._fd).encode())
        read_len = parser.parseint()
        parser.skipuntil("+CIPRXGET: 2,{},{},".format(self._fd, read_len).encode())
        rest_len = parser.parseint(b"\r\n")
        fstr = utils.converter(
            "+CIPRXGET: 2,{},{},{}\r\n".format(self._fd, read_len, rest_len), type(resp.content)
        )
        # print(f"fstr: {fstr}")
        start = resp.content.find(fstr) + len(fstr)

        self._ringio.write(resp.content[start : start + read_len])

    def recv(self, bufsize) -> bytes | None:
        return self.recvfrom(bufsize)

    def readall(self) -> bytes:
        out = bytearray(self._ringio.any())
        self._ringio.readinto(out)
        last_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), last_time) < self._timeout:
            self._recv()
            buf = self._ringio.read()
            out.extend(buf)

        return bytes(out)

    def recvfrom(self, bufsize: int) -> bytes | None:
        if bufsize == -1:
            return self.readall()

        if self._ringio.any() > bufsize:
            return self._ringio.read(bufsize)

        read_len = self._ringio.any()
        out = bytearray(read_len)
        self._ringio.readinto(out)
        last_time = time.ticks_ms()
        while read_len < bufsize and time.ticks_diff(time.ticks_ms(), last_time) < self._timeout:
            self._recv()
            buf = self._ringio.read(bufsize - read_len)
            out.extend(buf)
            read_len += len(buf)

        # https://docs.python.org/3.4/library/io.html#io.RawIOBase.read
        # "If the object is in non-blocking mode and no bytes are available,
        # None is returned."
        # This is actually very weird, as naive truth check will treat
        # this as EOF.
        if self.blocking is False and read_len == 0:
            return None

        return bytes(out)

    def setsockopt(self, level, optname, value):
        print("setsockopt is not implemented")

    def settimeout(self, timeout):
        self._timeout = 2000 if timeout is None else timeout

    def setblocking(self, flag):
        self.blocking = flag

    def makefile(self, mode):
        return self

    def fileno(self):
        return self._fd

    def read(self, *args) -> bytes | None:
        return self.recvfrom(args[0] if len(args) > 0 else -1)

    def readinto(self, *args) -> int:
        buf = args[0]
        nbytes = len(buf)
        if len(args) > 1:
            nbytes = args[1] if args[1] < nbytes else nbytes

        if self._ringio.any() < nbytes:
            self._recv()

        return self._ringio.readinto(buf, nbytes)

    def readline(self) -> bytes:
        last_time = time.ticks_ms()
        while (
            self._ringio.any() == 0 and time.ticks_diff(time.ticks_ms(), last_time) < self._timeout
        ):
            self._recv()
        return self._ringio.readline()

    def write(self, *args) -> int:
        data = args[0]
        l = len(data)
        max_len = len(data)
        off = 0
        if len(args) == 2:
            max_len = args[1]
        if len(args) == 3:
            off = args[1]
            max_len = args[2]
        if off > l:
            off = l
        l = l - off
        max_len = l if l < max_len else max_len
        # print(f"data[off : off + max_len]: {data[off : off + max_len]}")
        return self.send(data[off : off + max_len])


class _sockets(_socket):
    AF_INET = socket.AF_INET
    AF_INET6 = socket.AF_INET6

    SOCK_STREAM = socket.SOCK_STREAM
    SOCK_DGRAM = socket.SOCK_DGRAM
    SOCK_RAW = socket.SOCK_RAW

    IPPROTO_IP = socket.IPPROTO_IP
    IPPROTO_TCP = socket.IPPROTO_TCP
    IPPROTO_UDP = socket.IPPROTO_UDP

    _proto_type = {
        IPPROTO_TCP: "TCP",
        IPPROTO_UDP: "UDP",
    }

    _STATE_OPEN = 0
    _STATE_CLOSE = 1

    def __init__(self, modem: "SIM7020", af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP):
        self._modem = modem
        self._domain = af
        self._type = type
        self._proto = proto
        self._fd = self._modem.apply_session_id()
        self._address = None
        if self._fd == -1:
            raise SIMComError("No available session")

        self._state = self._STATE_CLOSE
        self._ringio = micropython.RingIO(1500)
        self._timeout = 2000
        self.blocking = False

    def __del__(self):
        self.close()

    def close(self) -> None:
        if self._fd == -1:
            return
        # _fd is connect num
        cmd = umodem.Command(
            "+CTLSCLOSE",
            umodem.Command.CMD_WRITE,
            self._fd,
            timeout=self._modem._default_timeout,
        )
        self._modem.execute(cmd)

        self._modem.release_session_id(self._fd)
        self._fd = -1
        self._state = self._STATE_CLOSE
        if hasattr(self, "_local_port"):
            self._modem.release_port(self._local_port)

    def bind(self, address):
        pass

    def listen(self, backlog):
        pass

    def accept(self):
        pass

    def tls_config(self, address):
        if self._fd == -1:
            raise SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return
        # Set the first SSL context to be used in the SSL connection
        cmd = umodem.Command(
            "+CTLSCFG",
            umodem.Command.CMD_WRITE,
            self._fd,  # tid
            1,
            str(address[0]),
            2,
            address[1],
            3,
            0,  # only support TCP
            4,
            0,
            5,
            2,
            timeout=self._modem._default_timeout,
        )
        self._modem.execute(cmd)
        # TODO: check error

    def connect(self, address):
        if self._fd == -1:
            raise SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return

        self._address = address
        cipstart = umodem.Command(
            "+CTLSCONN",
            umodem.Command.CMD_WRITE,
            self._fd,
            1,
            rsp1="CTLSCONN:",
            timeout=60000,
        )
        resp = self._modem.execute(cipstart)

        if resp.status_code == resp.ERR_NONE:
            self._state = self._STATE_OPEN
            self._connect_time = time.ticks_ms()
            return True
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cipstart.cmd)
        elif resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("+CTLSCONN: {},".format(self._fd).encode())
            err = parser.parseutil(b"\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR, err, cipstart.cmd)

    def send(self, data: bytes | str | bytearray) -> int:
        # data type check
        data = utils.converter(data, bytes)
        # print(f"raw data: {repr(data)}")
        data = data.decode("utf-8").replace("\r\n", "\\r\\n")
        # print(f"after raw data: {repr(data)}")
        total_length = len(data)
        total_sent = 0
        # print(f"data: {data}")

        max_segment_size = 1024

        while total_sent < total_length:
            segment_size = min(max_segment_size, total_length - total_sent)
            segment_data = data[total_sent : total_sent + segment_size]
            # print(f"segment_data: {segment_data}")
            # print(f"raw segment_data: {repr(segment_data)}")
            # print(f"segment_size: {segment_size}")
            cmd = umodem.Command(
                "+CTLSSEND",
                umodem.Command.CMD_WRITE,
                self._fd,
                segment_size,
                str(segment_data),
                rsp1="CTLSSEND:",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.execute(cmd)
            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("+CTLSSEND: {},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, err, cmd.cmd)
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            total_sent += segment_size
            # print(f"Sent segment: {segment_size} bytes, Total: {total_sent}/{total_length}")

        return total_length

    def sendall(self, data: bytes | str | bytearray) -> None:
        self.send(data)

    def _recv(self) -> None:
        cmd = umodem.Command(
            "+CTLSRECV",
            umodem.Command.CMD_WRITE,
            self._fd,
            512,  # max length to receive
            801,  # encoder method
            rsp1="CTLSRECV:",
            timeout=self._modem._default_timeout,
        )
        resp = self._modem.execute(cmd)
        if resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("+CTLSRECV: {},".format(self._fd).encode())
            errno = parser.parseutil(b"\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR_INFO, errno, cmd.cmd)
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

        # print(f"resp.content: {resp.content}")
        parser = Parser(resp.content)
        parser.skipuntil("+CTLSRECV: {},".format(self._fd).encode())
        recv_len = parser.parseint(b"\r\n")
        # print(f"recv_len: {recv_len}")
        if recv_len is not None and recv_len > 0:
            fstr = utils.converter(
                "+CTLSRECV: {},{},{}".format(self._fd, recv_len, '"'), type(resp.content)
            )
            start = resp.content.find(fstr) + len(fstr)
            data = resp.content[start : start + recv_len]
            # print(f"data: {data}")
            self._ringio.write(data)

    def recv(self, bufsize) -> bytes:
        return self.recvfrom(bufsize)

    def readall(self) -> bytes:
        out = bytearray(self._ringio.any())
        self._ringio.readinto(out)
        last_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), last_time) < self._timeout:
            self._recv()
            buf = self._ringio.read()
            out.extend(buf)

        return bytes(out)

    def recvfrom(self, bufsize) -> bytes:
        if bufsize == -1:
            return self.readall()

        if self._ringio.any() > bufsize:
            return self._ringio.read(bufsize)

        read_len = self._ringio.any()
        out = bytearray(read_len)
        self._ringio.readinto(out)
        last_time = time.ticks_ms()
        while read_len < bufsize and time.ticks_diff(time.ticks_ms(), last_time) < self._timeout:
            self._recv()
            buf = self._ringio.read(bufsize - read_len)
            out.extend(buf)
            read_len += len(buf)

        # https://docs.python.org/3.4/library/io.html#io.RawIOBase.read
        # "If the object is in non-blocking mode and no bytes are available,
        # None is returned."
        # This is actually very weird, as naive truth check will treat
        # this as EOF.
        if self.blocking is False and read_len == 0:
            return None

        return bytes(out)

    def setsockopt(self, level, optname, value):
        print("setsockopt is not implemented")
        return None

    def settimeout(self, timeout):
        print("settimeout is not implemented")
        return None

    def setblocking(self, flag):
        self.blocking = flag
        return None

    def makefile(self, mode):
        return self

    def fileno(self):
        return self._fd

    def read(self, *args) -> bytes:
        return self.recvfrom(args[0] if len(args) > 0 else -1)

    def readinto(self, *args) -> int:
        buf = args[0]
        nbytes = len(buf)
        if len(args) > 1:
            nbytes = args[1] if args[1] < nbytes else nbytes

        if self._ringio.any() < nbytes:
            self._recv()

        return self._ringio.readinto(buf, nbytes)

    def readline(self) -> bytes:
        last_time = time.ticks_ms()
        while (
            self._ringio.any() == 0 and time.ticks_diff(time.ticks_ms(), last_time) < self._timeout
        ):
            self._recv()
        return self._ringio.readline()

    def write(self, data) -> int:
        return self.send(data)


class SIM7020(umodem.UModem):
    # tcp/udp socket fd list
    _fds = [-1 for _ in range(6)]

    _session_id = [-1 for _ in range(6)]

    # tcp/udp socket port list
    _used_port = []

    def __init__(
        self, uart=None, pwrkey_pin=None, reset_pin=None, power_pin=None, verbose=False
    ) -> None:
        # Pin initialization
        pwrkey_obj = machine.Pin(pwrkey_pin, machine.Pin.OUT) if pwrkey_pin else None
        reset_obj = machine.Pin(reset_pin, machine.Pin.OUT) if reset_pin else None
        power_obj = machine.Pin(power_pin, machine.Pin.OUT) if power_pin else None

        # Status setup
        pwrkey_obj and pwrkey_obj(0)
        reset_obj and reset_obj(1)
        power_obj and power_obj(1)
        super().__init__(uart, verbose=verbose)

        # pdp
        self._cid = 1

        self._default_timeout = 3000
        self._is_active = True
        self._mqtt_client = None
        self.reset()
        self.active(True)
        self.connect()

    """fd/port management"""

    def apply_fd(self) -> int:
        for i in range(6):
            if self._fds[i] == -1:
                self._fds[i] = i
                return i
        return -1

    def release_fd(self, fd: int) -> None:
        self._fds[fd] = -1

    def apply_session_id(self) -> int:
        for i in range(6):
            if self._session_id[i] == -1:
                self._session_id[i] = i + 1
                return i + 1
        return -1

    def release_session_id(self, session_id: int) -> None:
        self._session_id[session_id] = -1

    def _low_power_mode(self):
        """enter low power mode"""
        cmd = umodem.Command("+CFUN", umodem.Command.CMD_WRITE, 0, timeout=10000)
        resp = self.execute(cmd)
        if resp.status_code == resp.ERR_NONE:
            self._is_active = False

    def active(self, is_active=True) -> bool:
        """activate or deactivate the modem"""
        if self._is_active == is_active:
            return self._is_active

        if is_active:
            cmd = umodem.Command(
                "+CFUN", umodem.Command.CMD_WRITE, 1, timeout=self._default_timeout
            )
            resp = self.execute(cmd)
            self.connect()
            if resp.status_code == resp.ERR_NONE:
                self._is_active = True
            time.sleep_ms(1000)
        else:
            self.reset()
            self._low_power_mode()
        return self._is_active

    def connect(self, apn=None):
        if apn is None:
            # auto activate PDP context
            # Check SIM card status
            cmd = umodem.Command("+CPIN", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            time.sleep_ms(100)
            # Check RF signal
            cmd = umodem.Command(
                "+CSQ", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout
            )
            self.execute(cmd)
            # Enable getting data from network manually.
            cmd = umodem.Command(
                "+CIPRXGET", umodem.Command.CMD_WRITE, 1, timeout=self._default_timeout
            )
            self.execute(cmd)
            # Check PS service
            cmd = umodem.Command("+CGREG", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            # Check PS service. 1 indicates PS has attached.
            cmd = umodem.Command("+CGATT", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            # PDN automatically active success,
            cmd = umodem.Command("+CGACT", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            # Query Network information, operator and network mode 9, NB-IOT network
            cmd = umodem.Command("+COPS", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            # Start Up Multi-IP Connection
            cmd = umodem.Command(
                "+CIPMUX", umodem.Command.CMD_WRITE, 1, timeout=self._default_timeout
            )
            # When module is in multi-IP state, before this command is executed, it is necessary to process "AT+CSTT, AT+CIICR, AT+CIFSR".
            self.execute(cmd)
            # Start Task and Set APN,USER NAME,PASSWORD
            cmd = umodem.Command(
                "+CSTT", umodem.Command.CMD_WRITE, "CMNBIOT", timeout=self._default_timeout
            )
            self.execute(cmd)

        else:
            # manually activate PDP context
            # Disable RF
            cmd = umodem.Command(
                "+CFUN", umodem.Command.CMD_WRITE, 0, timeout=self._default_timeout
            )
            self.execute(cmd)
            # set the APN manually
            cmd = umodem.Command(
                "*MCGDEFCONT", umodem.Command.CMD_WRITE, "IP", apn, timeout=self._default_timeout
            )
            self.execute(cmd)
            # Enable RF
            cmd = umodem.Command(
                "+CFUN", umodem.Command.CMD_WRITE, 1, timeout=self._default_timeout
            )
            self.execute(cmd)
            # Inquiry PS service
            cmd = umodem.Command("+CGATT", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)

        # Attached PS domain and got IP address and APN automatically from network
        cmd = umodem.Command(
            "+CGCONTRDP",
            umodem.Command.CMD_EXECUTION,
            rsp1="+CGCONTRDP:",
            timeout=10000,
        )
        self.execute(cmd)
        # Bring Up Wireless Connection
        cmd = umodem.Command("+CIICR", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        self.execute(cmd)
        # Get Local IP Address
        cmd = umodem.Command(
            "+CIFSR",
            umodem.Command.CMD_EXECUTION,
            rsp1="",
            rsp2='"',
            timeout=self._default_timeout,
        )
        self.execute(cmd)

    def disconnect(self):
        # 断开PDP连接，但是RF还是开启的
        raise NotImplementedError

    def isconnected(self) -> bool:
        parameters = self._get_pdp_context_dynamic_parameters()
        return parameters[3] != "0.0.0.0" and parameters[3] != ""

    def reset(self):
        cmd = umodem.Command(
            "+CRESET", umodem.Command.CMD_EXECUTION, rsp1="", rsp2="", timeout=500
        )
        self.execute(cmd)
        time.sleep(3.5)

    PIN_ERROR = -1  # PIN is not correct
    PIN_READY = 0  # MT is not pending for any password
    SIM_PIN = 1  # MT is waiting SIM PIN to be given
    SIM_PUK = 2  # MT is waiting for SIM PUK to be given
    PH_SIM_PIN = 3  # ME is waiting for phone to SIM card (antitheft)
    PH_SIM_PUK = 4  # ME is waiting for SIM PUK (antitheft)
    SIM_PIN2 = 5  # PIN2, e.g. for editing the FDN book possible only if preceding Command was acknowledged with +CME ERROR:17
    SIM_PUK2 = 6  # Possible only if preceding Command was acknowledged with error +CME ERROR: 18.
    PH_SIM_PIN = 7  # ME is waiting for phone to SIM card (antitheft)
    PH_NET_PIN = 8  # Network personalization password is required.
    PH_NETSUB_PIN = 9  # Network subset is required.
    PH_SP_PIN = 10  # Service provider personalization password is required.
    PH_CORP_PIN = 11  # Corporate personalization password is required.

    _cpin_code = {
        "READY": PIN_READY,
        "SIM PIN": SIM_PIN,
        "SIM PUK": SIM_PUK,
        "PH_SIM PIN": PH_SIM_PIN,
        "PH_SIM PUK": PH_SIM_PUK,
        "SIM PIN2": SIM_PIN2,
        "SIM PUK2": SIM_PUK2,
        "PH-SIM PIN": PH_SIM_PIN,
        "PH-NET PIN": PH_NET_PIN,
        "PH-NETSUB PIN": PH_NETSUB_PIN,
        "PH-SP PIN": PH_SP_PIN,
        "PH-CORP PIN": PH_CORP_PIN,
    }

    def _convert_rssi(self, rssi) -> int:
        """return dbm"""
        if rssi == 0:
            return -110
        elif rssi == 1:
            return -109
        elif rssi == 2:
            return -107
        elif rssi >= 3 and rssi <= 30:
            return -105 + (rssi - 3) * 2
        elif rssi == 31:
            return -48
        return -115

    def status(self, param=None) -> bool | int | str | tuple | None:
        if param is None or param == "status":
            parameters = self._get_pdp_context_dynamic_parameters()
            return parameters[3] != "0.0.0.0" and parameters[3] != ""
        elif param == "rssi":
            cmd = umodem.Command(
                "+CSQ", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout
            )
            resp = self.execute(cmd)
            if resp.status_code == umodem.Response.ERR_NONE:
                parser = Parser(resp.content)
                parser.skipuntil(b"+CSQ: ")
                rssi = parser.parseint()
                return self._convert_rssi(rssi)
        elif param == "pin":
            cmd = umodem.Command("+CPIN", umodem.Command.CMD_READ, timeout=self._default_timeout)
            resp = self.execute(cmd)
            if resp.status_code == umodem.Response.ERR_NONE:
                parser = Parser(resp.content)
                parser.skipuntil(b"+CPIN: ")
                code = parser.parseutil(b"\r\n").replace(b'"', b"")
                return self._cpin_code.get(code, self.PIN_ERROR)
            return self.PIN_ERROR
        elif param == "station":
            station, _ = self._get_network_state()
            return station
        elif param == "neighbor":
            _, neighbor = self._get_network_state()
            return neighbor

    def ifconfig(self, addr=None, mask=None, gateway=None, dns=None):
        params = self._get_pdp_context_dynamic_parameters()
        return (params[3], params[4], params[5], params[6])

    MODE_NB_IOT = 9

    def config(self, *args, **kwargs):
        if len(kwargs) != 0:
            for key, value in kwargs.items():
                if key == "band":
                    self.set_band(value)
            return

        if len(args) != 1:
            raise TypeError("can query only one param")

        param = args[0]
        if param == "apn":
            return self._get_pdp_context_dynamic_parameters()[2]
        elif param == "mode":
            # sim7020 support NB-IOT only
            return self.MODE_NB_IOT
        elif param == "band":
            return self.get_band()
        elif param == "ccid":
            return self.get_ccid_number()
        elif param == "imei":
            return self.get_imei_number()
        elif param == "imsi":
            return self.get_imsi_number()
        elif param == "mfr":
            return self.get_manufacturer()
        elif param == "model":
            return self.get_model_id()
        elif param == "version":
            return self.get_model_software_version()

    def _get_pdp_context_dynamic_parameters(self) -> tuple:
        """PDP Context Read Dynamic Parameters"""
        cmd = umodem.Command(
            "+CGCONTRDP",
            umodem.Command.CMD_WRITE,
            rsp1="+CGCONTRDP",
            timeout=self._default_timeout,
        )
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"+CGCONTRDP: ")
            cid = parser.parseint()  # cid
            bearer_id = parser.parseint()  # bearer_id
            apn = parser.parseutil(b",").strip(b'"')  # apn
            locl_ip = parser.parseutil(b",").strip(b'"')  # local_ip and subnet_mask
            if locl_ip.count(b".") == 7:
                # ipv4
                parts = locl_ip.split(b".")
                locl_ip = b".".join(parts[:4])
                subnet_mask = b".".join(parts[4:])
            elif locl_ip.count(b".") == 31:
                # ipv6
                parts = locl_ip.split(b".")
                locl_ip = b".".join(parts[:16])
                subnet_mask = b".".join(parts[16:])
            else:
                locl_ip = b"0.0.0.0"
                subnet_mask = b"0.0.0.0"
            gateway = parser.parseutil(b",").strip(b'"')  # gateway
            gateway = gateway if gateway != b"" else b"0.0.0.0"
            dns1 = parser.parseutil(b",").strip(b'"')
            dns1 = dns1 if dns1 != b"" else b"0.0.0.0"
            dns2 = parser.parseutil(b",").strip(b'"')
            dns2 = dns2 if dns2 != b"" else b"0.0.0.0"
            return (
                cid,
                bearer_id,
                apn.decode(),
                locl_ip.decode(),
                subnet_mask.decode(),
                gateway.decode(),
                dns1.decode(),
                dns2.decode(),
            )
        else:
            return (-9999, -9999, "", "0.0.0.0", "0.0.0.0", "0.0.0.0", "0.0.0.0", "0.0.0.0")

    def _get_network_state(self):
        cmd = umodem.Command("+CENG", umodem.Command.CMD_READ, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            num = resp.content.count("+CENG: ")
            if num == 0:
                return ((), ())
            parser = Parser(resp.content)
            parser.skipuntil(b"+CENG: ")
            station = []
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseutil(",").strip(b'"'))
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseutil(",").strip(b'"'))
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint(chr=b"\r"))
            neighbors = []
            for _ in range(num - 1):
                parser.skipuntil(b"+CENG: ")
                neighbor = []
                neighbor.append(parser.parseint())
                neighbor.append(parser.parseint())
                neighbor.append(parser.parseint())
                neighbor.append(parser.parseint(chr=b"\r"))
                neighbors.append(tuple(neighbor))
            return (tuple(station), tuple(neighbors))
        return ((), ())

    def apply_port(self) -> int:
        for i in range(1024, 65535):
            if i not in self._used_port:
                self._used_port.append(i)
                return i
        return -1

    def release_port(self, port: int) -> None:
        self._used_port.remove(port)

    def getaddrinfo(self, host: str, port, af=0, type=0, proto=0, flags=0):
        """
        The resulting list of 5-tuples has the following structure:
            (family, type, proto, canonname, sockaddr)
        """
        res = []

        cmd = umodem.Command(
            "+CDNSGIP={}".format(host.strip('"')),
            umodem.Command.CMD_EXECUTION,
            rsp1="+CDNSGIP:",
            timeout=10000,
        )

        resp = self.execute(cmd)
        self._verbose and print(resp.content)
        self._verbose and print(resp.status_code)

        ip = "0.0.0.0"
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil('+CDNSGIP: 1,"{}","'.format(host).encode())
            ip = parser.parseutil(b'"\r\n').decode()
        elif resp.status_code == umodem.Response.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, resp.status_code, cmd.cmd)
        elif resp.status_code == umodem.Response.ERR_GENERIC:
            raise SIMComError(SIMComError.D_DNS_ERROR_CODE, 10, cmd.cmd)

        res.append(
            (
                socket.AF_INET,
                socket.SOCK_STREAM,
                socket.IPPROTO_TCP,
                host,
                (utils.converter(ip, str), port),
            )
        )
        return res

    def socket(self, af=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP):
        return _socket(self, af, type, proto)

    def wrap_socket(
        self,
        sock: _socket,
        # server_side=False,
        # key=None,
        # cert=None,
        # cert_reqs=None,
        # cadata=None,
        server_hostname=None,
        # do_handshake=True,
    ):
        # print(f"key: {key}")
        # print(f"cert: {cert}")
        # print(f"raw cert: {repr(cert)}")
        # cert = cert.replace("\r\n", "\\r\\n")
        # print(f"after replace cert: {cert}")
        # print(f"cert_reqs: {cert_reqs}")
        # print(f"cadata: {cadata}")
        # print(f"server_hostname: {server_hostname}")
        # print(f"do_handshake: {do_handshake}")
        sock.close()
        s = _sockets(self, sock._domain, sock._type, sock._proto)
        s.tls_config(sock._address)
        # if cert is not None:
        #     cmd = umodem.Command(
        #         "+CTLSCFG",
        #         umodem.Command.CMD_WRITE,
        #         1,
        #         6,
        #         timeout=self._default_timeout,
        #     )
        #     self.execute(cmd)
        # if cert is not None:
        #     cert_len = len(cert)
        #     chunk_size = 450
        #     for i in range(0, cert_len, chunk_size):
        #         chunk = cert[i : i + chunk_size]
        #         last_chunk = i + chunk_size >= cert_len
        #         is_last_flag = 0 if last_chunk else 1

        #         cmd = umodem.Command(
        #             "+CTLSCERT",
        #             umodem.Command.CMD_WRITE,
        #             1,
        #             6,
        #             cert_len,
        #             is_last_flag,
        #             chunk,
        #             timeout=self._default_timeout,
        #         )
        #         self.execute(cmd)
        s.connect(sock._address)
        return s

    """request method"""

    def request(
        self,
        method,
        url,
        data=None,
        json=None,
        headers={},
        stream=None,
        auth=None,
        timeout=None,
        parse_headers=True,
    ):
        return requests2._request(
            self, method, url, data, json, headers, stream, auth, timeout, parse_headers
        )

    def head(self, url, **kw):
        return self.request("HEAD", url, **kw)

    def get(self, url, **kw):
        return self.request("GET", url, **kw)

    def post(self, url, **kw):
        return self.request("POST", url, **kw)

    def put(self, url, **kw):
        return self.request("PUT", url, **kw)

    def patch(self, url, **kw):
        return self.request("PATCH", url, **kw)

    def delete(self, url, **kw):
        return self.request("DELETE", url, **kw)

    """mqtt method"""

    def MQTTClient(  # noqa: N802
        self,
        client_id,
        server,
        port=0,
        user=None,
        password=None,
        keepalive=0,
        ssl=False,
        ssl_params={},
    ):
        return umqtt.MQTTClient(
            self,
            client_id,
            server,
            port=port,
            user=user,
            password=password,
            keepalive=keepalive,
            ssl=ssl,
            ssl_params=ssl_params,
        )

    def set_band(self, band: tuple) -> bool:
        cmd = umodem.Command(
            "+CBAND", umodem.Command.CMD_WRITE, *band, timeout=self._default_timeout
        )
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def get_band(self) -> tuple:
        cmd = umodem.Command("+CBAND", umodem.Command.CMD_READ, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"+CBAND: ")
            parts = parser.parseutil(b"\r\n").split(b",")
            return tuple([int(part) for part in parts])
        return ()

    def get_manufacturer(self) -> str:
        cmd = umodem.Command("+CGMI", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"\n")
            return parser.parseutil(b"\r\n").decode()
        return ""

    def get_model_id(self) -> str:
        cmd = umodem.Command("+CGMM", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"\n")
            return parser.parseutil(b"\r\n").decode()
        return ""

    def get_model_software_version(self) -> str:
        cmd = umodem.Command("+CGMR", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"\n")
            return parser.parseutil(b"\r\n").decode()
        return ""

    def get_imei_number(self) -> str:
        """Request TA Serial Number Identification(IMEI)"""
        cmd = umodem.Command("+CGSN", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        self._verbose and print(f"resp.content: {resp.content}")
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"\n")
            return parser.parseutil(b"\r\n").decode("utf-8")
        return ""

    def get_ccid_number(self) -> str:
        """Show ICCID"""
        cmd = umodem.Command("+CCID", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"\n")
            return parser.parseutil(b"\r\n").decode()
        return ""

    def get_imsi_number(self) -> str:
        cmd = umodem.Command("+CIMI", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"\n")
            return parser.parseutil(b"\r\n").decode()
        return ""

    ###################################################################################

    def set_pdp_context(self, active: bool) -> bool:
        """PDP Context Activate or Deactivate"""
        cmd = umodem.Command(
            "+CGACT", umodem.Command.CMD_WRITE, int(active), 1, timeout=self._default_timeout
        )
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def get_pdp_context_status(self) -> bool:
        """PDP Context Activate or Deactivate"""
        cmd = umodem.Command("+CGACT", umodem.Command.CMD_READ, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"+CGACT: ")
            parser.parseint(b",")
            return bool(parser.parseint(b"\r\n"))
        return False

    def set_pdp_context_apn(self, apn="cmnbiot") -> bool:
        """Set Default PSD Connection Settings"""
        cmd = umodem.Command(
            "*MCGDEFCONT", umodem.Command.CMD_WRITE, "IP", apn, timeout=self._default_timeout
        )
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def get_pdp_context_dynamic_parameters(self, param=1):
        resp = self._get_pdp_context_dynamic_parameters()
        if param == 1:
            return resp[3]
        elif param == 2:
            return resp[2]
        else:
            return ""

    # MQTT Test Server:mqtt.m5stack.com, Port:1883.
    def mqtt_server_connect(
        self, server: str, port: int, client_id: str, username: str, passwd: str, keepalive: int
    ):
        self._mqtt_client = self.MQTTClient(
            client_id,
            server,
            port,
            user=username,
            password=passwd,
            keepalive=keepalive,
        )
        self._mqtt_client.connect()

        return self._mqtt_client.isconnected()

    def mqtt_server_disconnect(self):
        if self._mqtt_client is not None:
            self._mqtt_client.disconnect()
            self._mqtt_client = None
        else:
            raise SIMComError("MQTT client is not create")

    def mqtt_subscribe_topic(self, topic, cb, qos=0) -> bool:
        if self._mqtt_client is not None:
            self._mqtt_client.subscribe(topic, qos)
            self._mqtt_client.set_callback(cb)
            return True
        else:
            raise SIMComError("MQTT client is not create")

    def mqtt_unsubscribe_topic(self, topic):
        if self._mqtt_client is not None:
            self._mqtt_client.unsubscribe(topic)
            return True
        else:
            raise SIMComError("MQTT client is not create")

    def mqtt_publish_topic(self, topic, payload, qos=0, retained=False, duplicate=None):
        if self._mqtt_client is not None:
            self._mqtt_client.publish(topic, msg=payload, retain=retained, qos=qos)
        else:
            raise SIMComError("MQTT client is not create")

    def mqtt_server_is_connect(self):
        # Check mqtt server connection.
        if self._mqtt_client is not None:
            return self._mqtt_client.isconnected()
        else:
            raise SIMComError("MQTT client is not create")

    def mqtt_polling_loop(self):
        if self._mqtt_client is not None:
            self._mqtt_client.check_msg()
        else:
            raise SIMComError("MQTT client is not create")

    # Create & Request Http(s)
    HTTPCLIENT_GET = 0
    HTTPCLIENT_POST = 1
    HTTPCLIENT_PUT = 2
    HTTPCLIENT_DELETE = 3
    HTTPCLIENT_PATCH = 4
    HTTPCLIENT_HEAD = 5

    def http_request(
        self, method=HTTPCLIENT_GET, url="http://api.m5stack.com/v1", headers={}, data=None
    ):
        self.data_content = ""
        self.response_code = 0
        method_map = {
            self.HTTPCLIENT_GET: "GET",
            self.HTTPCLIENT_POST: "POST",
            self.HTTPCLIENT_PUT: "PUT",
            self.HTTPCLIENT_DELETE: "DELETE",
            self.HTTPCLIENT_PATCH: "PATCH",
            self.HTTPCLIENT_HEAD: "HEAD",
        }

        if isinstance(method, int):
            str_method = method_map.get(method, "GET")
            if isinstance(data, dict):
                import ujson

                data = ujson.dumps(data).encode()

                if "Content-Type" not in headers:
                    headers["Content-Type"] = "application/json"

            elif isinstance(data, str):
                data = data.encode()
            response = self.request(str_method, url, data=data, headers=headers)
            self.data_content = response.reason
            self.response_code = response.status_code

    def write_read(self, cmd: str, rsp1="OK", rsp2="ERROR", line_end="\r\n", timeout: int = 10000):
        cmdstr = "AT+" + "{}\r\n".format(cmd)
        self._verbose and print("TE -> TA:", repr(cmdstr))
        self.uart.write(cmdstr.encode("utf-8"))
        output = bytearray()
        ticks = time.ticks_ms()

        rsp1_bytes = rsp1.encode("utf-8")
        rsp2_bytes = rsp2.encode("utf-8")
        line_end_bytes = line_end.encode("utf-8")

        find_keyword = False

        while time.ticks_diff(time.ticks_ms(), ticks) < timeout:
            if self.uart.any() == 0:
                time.sleep_ms(10)
                continue

            line = self.uart.read(self.uart.any())
            self._verbose and print("TE <- TA:", repr(line))
            output.extend(line)

            # Do we have an error?
            if output.rfind(rsp2_bytes) != -1:
                if output.endswith(line_end_bytes):
                    print("Get AT command error response:", repr(output))
                    find_keyword = True

            # If we had a pre-end, do we have the expected end?
            if output.rfind(rsp1_bytes) != -1:
                if output.endswith(line_end_bytes):
                    find_keyword = True

            if find_keyword:
                break

        return output.decode("utf-8")

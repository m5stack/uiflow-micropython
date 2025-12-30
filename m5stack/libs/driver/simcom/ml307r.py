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

    def __init__(self, modem: "ML307R", af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP):
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

    def connect(self, address: tuple[str, int]):
        if self._fd == -1:
            raise SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return

        self._address = address
        # _fd is connect num
        cmd = umodem.Command(
            "+MIPOPEN",
            umodem.Command.CMD_WRITE,
            self._fd,
            str(self._proto_type.get(self._proto, "")),
            str(address[0]),
            address[1],
            60,
            2 if self._proto == self.IPPROTO_TCP else 3,
            rsp1="+MIPOPEN: {},{}".format(self._fd, 0),
            timeout=60000,
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

    def __del__(self):
        self.close()

    def close(self) -> None:
        if self._fd == -1:
            return
        cmd = umodem.Command(
            "+MIPCLOSE",
            umodem.Command.CMD_WRITE,
            self._fd,
            rsp1="+MIPCLOSE: {}".format(self._fd),
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
                "+MIPSEND",
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
                "+MIPSEND:",
                umodem.Command.CMD_EXEC,
                rsp1="+MIPSEND: {},{}".format(self._fd, segment_size),
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
            print(f"Sent segment: {segment_size} bytes, Total: {total_sent}/{total_length}")

        return total_length

    def sendall(self, data: bytes | str | bytearray) -> None:
        self.send(data)

    def sendto(self, data: bytes | str | bytearray, address) -> int:
        if self._state == self._STATE_CLOSE:
            self._local_port = self._modem.apply_port()
            self._fd = self._modem.apply_fd()
            if self._fd == -1:
                raise SIMComError("No available socket")
            print(f"_proto: {self._proto_type.get(self._proto, '')}, address: {address}")
            cipopen = umodem.Command(
                "+MIPOPEN",
                umodem.Command.CMD_WRITE,
                self._fd,
                str(self._proto_type.get(self._proto, "")),
                str(address[0]),
                address[1],
                60,
                2 if self._proto == self.IPPROTO_TCP else 3,
                rsp1="+MIPOPEN: {},{}".format(self._fd, 0),
                timeout=60000,
            )
            resp: umodem.Response = self._modem.execute(cipopen)
            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("{},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
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
                "+MIPSEND",
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
                "+MIPSEND",
                umodem.Command.CMD_EXEC,
                rsp1="+MIPSEND: {},{}".format(self._fd, segment_size),
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
            print(f"Sent segment: {segment_size} bytes, Total: {total_sent}/{total_length}")

        return total_length

    def _recv(self) -> None:
        ciprxget = umodem.Command(
            "+MIPRD",
            umodem.Command.CMD_WRITE,
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
        parser.skipuntil("+MIPRD: {},".format(self._fd).encode())
        to_recv = parser.parseint(b"\r\n")
        if to_recv == 0:
            return

        to_recv = (4095 - self._ringio.any()) if to_recv > (4095 - self._ringio.any()) else to_recv

        ciprxget = umodem.Command(
            "+MIPRD",
            umodem.Command.CMD_WRITE,
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
        parser.skipuntil("+MIPRD: {},".format(self._fd).encode())
        rest_len = parser.parseint()
        read_len = parser.parseint()
        fstr = utils.converter(
            "+MIPRD: {},{},{},".format(self._fd, rest_len, read_len), type(resp.content)
        )
        start = resp.content.find(fstr) + len(fstr)

        self._ringio.write(resp.content[start : start + read_len])

    def test_recv(self):
        out = bytearray(self._ringio.any())
        self._recv()
        buf = self._ringio.read()
        out.extend(buf)
        return bytes(out)

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


class ML307R(umodem.UModem):
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
        if not self.check_sim_ready():
            raise SIMComError("SIM card not ready")
        self.active(True)

        # self.connect()

    def _low_power_mode(self):
        """enter low power mode"""
        cmd = umodem.Command("+CFUN", umodem.Command.CMD_WRITE, 0, timeout=10000)
        resp = self.execute(cmd)
        if resp.status_code == resp.ERR_NONE:
            self._is_active = False

    def reset(self):
        cmd = umodem.Command("+CFUN", umodem.Command.CMD_WRITE, 0, rsp1="", rsp2="", timeout=500)
        self.execute(cmd)
        time.sleep(0.5)
        cmd = umodem.Command("+CFUN", umodem.Command.CMD_WRITE, 1, rsp1="", rsp2="", timeout=500)
        self.execute(cmd)
        time.sleep(3.5)

    def check_sim_ready(self) -> bool:
        cmd = umodem.Command("+CPIN", umodem.Command.CMD_READ, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"CPIN: ")
            return parser.parseutil(b"\r\n") == "READY"
        return False

    def active(self, is_active=True) -> bool:
        """activate or deactivate the modem"""
        # if self._is_active == is_active:
        #     return self._is_active

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

    def check_network_ready(self) -> bool:
        cmd = umodem.Command("+CEREG", umodem.Command.CMD_READ, timeout=10000)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"CEREG: ")
            parser.skipuntil(b",")
            return parser.parseutil(b",") == "1"
        return False

    def connect(self, apn=None):
        if apn is None:
            # auto activate PDP context
            # Check network status
            while True:
                _tick_time = time.ticks_ms()
                if self.check_network_ready():
                    break
                if time.ticks_diff(time.ticks_ms(), _tick_time) > 60000:
                    raise SIMComError("Network registration timeout")

            # Check dialing status
            cmd = umodem.Command(
                "+MIPCALL", umodem.Command.CMD_READ, timeout=self._default_timeout
            )
            self.execute(cmd)
            time.sleep_ms(100)
        else:
            # manually activate PDP context
            cmd = umodem.Command(
                "+CGDCONT",
                umodem.Command.CMD_WRITE,
                1,
                "IPV4V6",
                apn,
                timeout=self._default_timeout,
            )
            self.execute(cmd)
            # Activate PDP to establish an application layer dial-up connection.
            cmd = umodem.Command(
                "+MIPCALL",
                umodem.Command.CMD_WRITE,
                1,
                1,
                rsp1="+MIPCALL:",
                timeout=self._default_timeout,
            )
            self.execute(cmd)

    def disconnect(self):
        cmd = umodem.Command(
            "+MIPCALL",
            umodem.Command.CMD_WRITE,
            0,
            rsp1="+MIPCALL:",
            timeout=self._default_timeout,
        )
        self.execute(cmd)

    def isconnected(self) -> bool:
        parameters = self._get_pdp_context_dynamic_parameters()
        return parameters[3] != "0.0.0.0" and parameters[3] != ""

    def get_pdp_context_dynamic_parameters(self, param=1):
        resp = self._get_pdp_context_dynamic_parameters()
        if param == 1:
            return resp[3]
        elif param == 2:
            return resp[2]
        else:
            return ""

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
            if locl_ip.count(b".") == 3:
                # ipv4
                parts = locl_ip.split(b".")
                locl_ip = b".".join(parts[:4])
            elif locl_ip.count(b".") == 31:
                # ipv6
                parts = locl_ip.split(b".")
                locl_ip = b".".join(parts[:16])
            else:
                locl_ip = b"0.0.0.0"
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
                gateway.decode(),
                dns1.decode(),
                dns2.decode(),
            )
        else:
            return (-9999, -9999, "", "0.0.0.0", "0.0.0.0", "0.0.0.0", "0.0.0.0")

    def getaddrinfo(self, host: str, port, af=0, type=0, proto=0, flags=0):
        """
        The resulting list of 5-tuples has the following structure:
            (family, type, proto, canonname, sockaddr)
        """
        res = []

        cmd = umodem.Command(
            "+MDNSGIP={}".format(host.strip('"')),
            umodem.Command.CMD_EXEC,
            rsp1="+MDNSGIP:",
            timeout=10000,
        )

        resp = self.execute(cmd)
        self._verbose and print(resp.content)
        self._verbose and print(resp.status_code)

        ip = "0.0.0.0"
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil('+MDNSGIP: "{}","'.format(host).encode())
            ip = parser.parseutil(b'"').decode()
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

    def get_imei_number(self) -> str:
        """Request TA Serial Number Identification(IMEI)"""
        cmd = umodem.Command("+GSN", umodem.Command.CMD_EXEC, 1, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"GSN: ")
            return parser.parseutil(b"\r\n").decode("utf-8")
        return ""

    def get_model_identification(self) -> str:
        cmd = umodem.Command("+CGMM", umodem.Command.CMD_EXEC, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"\r\n")
            return parser.parseutil(b"\r\n").decode("utf-8")
        return ""

    def get_pdp_context_status(self) -> bool:
        cmd = umodem.Command("+CGACT", umodem.Command.CMD_READ, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"+CGACT: ")
            parser.parseint(b",")
            return bool(parser.parseint(b"\r\n"))
        return False

    def socket(self, af=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP):
        return _socket(self, af, type, proto)

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

    def apply_port(self) -> int:
        for i in range(1024, 65535):
            if i not in self._used_port:
                self._used_port.append(i)
                return i
        return -1

    def release_port(self, port: int) -> None:
        self._used_port.remove(port)

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

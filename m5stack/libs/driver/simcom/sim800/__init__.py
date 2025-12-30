# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import umodem
import re
import socket
import micropython
import umodem.parser
from .. import utils
import time
import machine


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

    def __init__(self, modem, af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP):
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

    def accept(self):
        raise NotImplementedError

    def bind(self, address):
        raise NotImplementedError

    def close(self):
        if self._fd == -1:
            return

        cmd = umodem.Command(
            "+CIPCLOSE", umodem.Command.CMD_WRITE, self._fd, timeout=self._modem._default_timeout
        )
        self._modem.execute_at_command2(cmd)
        self._modem.release_fd(self._fd)
        self._fd = -1
        self._state = self._STATE_CLOSE
        if hasattr(self, "_local_port"):
            self._modem.release_port(self._local_port)

    def connect(self, address):
        if self._fd == -1:
            raise SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return

        self._address = address
        cmd = umodem.Command(
            "+CIPSTART",
            umodem.Command.CMD_WRITE,
            self._fd,
            self._proto_type.get(self._proto, ""),
            address[0],
            address[1],
            rsp1="CONNECT OK",
            timeout=self._modem._default_timeout,
        )

        output, error = self._modem.execute_at_command2(cmd)
        if error == self._modem.ERR_NONE:
            self._state = self._STATE_OPEN
            return True
        elif error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, cmd())
        elif error == self._modem.ERR_GENERIC:
            err = utils.extract_int(output, "+CIPOPEN: {},".format(self._fd), "\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR, err, cmd())

    def fileno(self) -> int:
        return self._fd

    def listen(self, backlog):
        raise NotImplementedError

    def makefile(self, mode):
        return self

    def read(self, size=-1) -> bytes:
        return self.recvfrom(size)

    def readinto(self, buf, nbytes=-1) -> int:
        nbytes = min(nbytes, len(buf)) if nbytes != -1 else len(buf)

        if self._ringio.any() < nbytes:
            self._recv()

        return self._ringio.readinto(buf, nbytes)

    def readline(self) -> str:
        l = ""
        while 1:
            c = self._ringio.read(1)
            l += c
            if c == "\\n" or c == "":
                return l

    def recv(self, bufsize) -> bytes:
        return self.recvfrom(bufsize)

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

    def send(self, buf) -> int:
        # data type check
        data = utils.converter(buf, bytes)

        # send cmd
        to_send = len(data)
        cipsend = umodem.Command(
            "AT+CIPSEND={},{}".format(self._fd, to_send),
            ">",
            "ERROR",
            self._modem._default_timeout,
        )
        output, error = self._modem.execute_at_command2(cipsend, line_end="")
        if error == self._modem.ERR_GENERIC:
            err = utils.extract_int(output, "+CIPSEND: ", "\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR, err, cipsend.cmd)
        elif error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, cipsend.cmd)

        sented = 0
        while sented < to_send:
            self._modem.uart.write(data[sented:to_send])
            cipsend = umodem.Command(
                "AT+CIPSEND={},{}".format(self._fd, to_send),
                "+CIPSEND:",
                "ERROR",
                self._modem._default_timeout,
            )
            output, error = self._modem.response_at_command2(cipsend)
            if error == self._modem.ERR_GENERIC:
                err = utils.extract_int(output, "+CIPERROR: ", "\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, err, cipsend.cmd)
            elif error == self._modem.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, error, cipsend.cmd)
            elif error == self._modem.ERR_NONE:
                cnf = utils.extract_text(
                    output, "+CIPSEND: {},{},".format(self._fd, to_send), "\r\n"
                )
                sented = int(cnf) if cnf else 0
        return to_send

    def sendall(self, buf):
        self.send(buf)

    def sendto(self, buf, address):
        if self._state == self._STATE_CLOSE:
            self._local_port = self._modem.apply_port()
            cipopen = umodem.Command(
                "AT+CIPOPEN={},{},,,{}".format(
                    self._fd,
                    "".join(['"', self._proto_type.get(self._proto, ""), '"']),
                    self._local_port,
                ),
                "OK",
                "ERROR",
                self._modem._default_timeout,
            )
            output, error = self._modem.execute_at_command2(cipopen)
            if error == self._modem.ERR_GENERIC:
                errno = utils.extract_int(output, "+CIPOPEN: ", "\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, errno, cipopen.cmd)
            elif error == self._modem.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, error, cipopen.cmd)
            self._state = self._STATE_OPEN

        # data type check
        data = utils.converter(buf, bytes)

        # send cmd
        to_send = len(data)
        cipsend = umodem.Command(
            "AT+CIPSEND={},{},{},{}".format(
                self._fd, to_send, "".join(['"', address[0], '"']), address[1]
            ),
            ">",
            "ERROR",
            self._modem._default_timeout,
        )
        output, error = self._modem.execute_at_command2(cipsend, line_end="")
        if error == self._modem.ERR_GENERIC:
            errno = utils.extract_int(output, "+CIPSEND: ", "\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR, errno, cipsend.cmd)
        elif error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, cipsend.cmd)

        sented = 0
        while sented < to_send:
            self._modem.uart.write(data[sented:to_send])
            cipsend = umodem.Command(
                "AT+CIPSEND={},{}".format(self._fd, to_send),
                "+CIPSEND:",
                "ERROR",
                self._modem._default_timeout,
            )
            output, error = self._modem.response_at_command2(cipsend)
            if error == self._modem.ERR_GENERIC:
                errno = utils.extract_int(output, "+CIPERROR: ", "\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, errno, cipsend.cmd)
            elif error == self._modem.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, error, cipsend.cmd)
            else:
                cnf = utils.extract_text(
                    output, "+CIPSEND: {},{},".format(self._fd, to_send), "\r\n"
                )
                sented = int(cnf) if cnf else 0
        return to_send

    def setblocking(self, flag):
        self.blocking = flag

    def setsockopt(self, level, optname, value):
        raise NotImplementedError

    def settimeout(self, timeout):
        raise NotImplementedError

    def write(self, buf):
        return self.send(buf)


class SIM800(umodem.UModem):
    def __init__(self, uart=None, pwrkey_pin=None, reset_pin=None, power_pin=None, verbose=False):
        # Pin initialization
        pwrkey_obj = machine.Pin(pwrkey_pin, machine.Pin.OUT) if pwrkey_pin else None
        reset_obj = machine.Pin(reset_pin, machine.Pin.OUT) if reset_pin else None
        power_obj = machine.Pin(power_pin, machine.Pin.OUT) if power_pin else None

        # Status setup
        pwrkey_obj and pwrkey_obj(0)
        reset_obj and reset_obj(1)
        power_obj and power_obj(1)
        super().__init__(uart, verbose=verbose)

        self._default_timeout = 2000
        self._is_active = True
        self._low_power_mode()

    def _low_power_mode(self):
        """enter low power mode"""
        cmd = umodem.Command("+CFUN", umodem.Command.CMD_WRITE, 0, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == resp.ERR_NONE:
            self._is_active = False

    def active(self, is_active) -> bool:
        """activate or deactivate the modem"""
        if self._is_active == is_active:
            return self._is_active

        if is_active:
            cmd = umodem.Command(
                "+CFUN", umodem.Command.CMD_WRITE, 1, timeout=self._default_timeout
            )
            resp = self.execute(cmd)
            if resp.status_code == resp.ERR_NONE:
                self._is_active = True
        else:
            self._low_power_mode()
        return self._is_active

    def connect(self, apn=None):
        if apn is None:
            # auto activate PDP context
            # Check SIM card status
            cmd = umodem.Command("+CFIN?", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            # Check RF signal
            cmd = umodem.Command("+CSQ", umodem.Command.CMD_EXEC, timeout=self._default_timeout)
            self.execute(cmd)
            # Check PS service. 1 indicates PS has attached.
            cmd = umodem.Command("+CGATT", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            # PDN active success
            cmd = umodem.Command("+CGACT", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            # Query Network information, operator and network mode 9, NB-IOT network
            cmd = umodem.Command("+COPS", umodem.Command.CMD_READ, timeout=self._default_timeout)
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

        # Attached PS domain and got IP address automatically
        cmd = umodem.Command("+CGCONTRDP", umodem.Command.CMD_EXEC, timeout=self._default_timeout)
        self.execute(cmd)

    def disconnect(self):
        raise NotImplementedError

    def isconnected(self) -> bool:
        raise NotImplementedError

    def status(self) -> int:
        raise NotImplementedError

    def ifconfig(self, addr=None, mask=None, gateway=None, dns=None):
        raise NotImplementedError

    def config(self, param: str):
        pass

    def getaddrinfo(self, host, port, af=0, type=0, proto=0, flags=0):
        pass

    def socket(self, af=0, type=0, proto=0):
        pass

    def get_imei_number(self) -> str:
        # Request TA Serial Number Identification(IMEI)
        cmd = umodem.Command("+CGSN", umodem.Command.CMD_EXEC, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == resp.ERR_NONE:
            parser = umodem.parser.Parser(resp.content)
            parser.skipuntil("\n")
            return parser.parseutil("\r\n")
        return ""

    def get_ccid_number(self) -> str:
        # Show ICCID
        cmd = umodem.Command("+ICCID", umodem.Command.CMD_EXEC, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == resp.ERR_NONE:
            parser = umodem.parser.Parser(resp.content)
            parser.skipuntil("\n")
            return parser.parseutil("\r\n")
        return ""

    def get_pdp_context_dynamic_parameters(self, cid: int = 1) -> tuple:
        # PDP Context Read Dynamic Parameters
        cmd = umodem.Command(
            "+CGCONTRDP", umodem.Command.CMD_WRITE, cid, timeout=self._default_timeout
        )
        resp = self.execute(cmd)
        if resp.status_code == resp.ERR_NONE:
            return False
        parser = umodem.parser.Parser(resp.content)
        parser.skipuntil("+CGCONTRDP: ")
        cid = parser.parseint()
        bearer_id = parser.parseint()
        apn = parser.parseutil(",").strip('"')
        locl_ip = parser.parseutil(",").strip('"')
        parts = locl_ip.split(".")
        locl_ip = ".".join(parts[:4])
        subnet_mask = parser.parseutil(",").strip('"')
        gateway = parser.parseutil(",").strip('"')
        dns1 = parser.parseutil(",")
        dns2 = parser.parseutil("\r\n")
        return cid, bearer_id, apn, locl_ip, subnet_mask, gateway, dns1, dns2

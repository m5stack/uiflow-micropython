# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .common import Modem
from .common import ATCommand
from . import utils
from .toolkit import requests2
import re
import socket
import micropython
import time


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
        self._timeout = 5000

    def __del__(self):
        self.close()

    def close(self) -> None:
        if self._fd == -1:
            return
        close = ATCommand(
            "AT+CIPCLOSE={}".format(self._fd), "OK\r\n", "ERROR\r\n", self._modem._default_timeout
        )
        self._modem.execute_at_command2(close)
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

    def connect(self, address):
        if self._fd == -1:
            raise SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return

        self._address = address
        cipstart = ATCommand(
            "AT+CIPOPEN={},{},{},{}".format(
                self._fd,
                "".join(['"', self._proto_type.get(self._proto, ""), '"']),
                "".join(['"', address[0], '"']),
                address[1],
            ),
            "+CIPOPEN",
            "ERROR\r\n",
            120000,  # Maximum Response Time
        )
        output, error = self._modem.execute_at_command2(cipstart)
        if error == self._modem.ERR_NONE:
            self._state = self._STATE_OPEN
            return True
        elif error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, cipstart.cmd)
        elif error == self._modem.ERR_GENERIC:
            err = utils.extract_int(output, "\+CIPOPEN: {},".format(self._fd), "\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR, err, cipstart.cmd)

    def send(self, data: bytes | str | bytearray) -> int:
        # data type check
        if isinstance(data, str):
            data = data.encode("utf-8")
        if isinstance(data, bytearray):
            data = bytes(data)

        # send cmd
        to_send = len(data)
        cipsend = ATCommand(
            "AT+CIPSEND={},{}".format(self._fd, to_send),
            ">",
            "ERROR\r\n",
            self._modem._default_timeout,
        )
        output, error = self._modem.execute_at_command2(cipsend, line_end="")
        if error == self._modem.ERR_GENERIC:
            err = utils.extract_int(output, "\+CIPSEND: ", "\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR, err, cipsend.cmd)
        elif error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, cipsend.cmd)

        sented = 0
        while sented < to_send:
            self._modem.uart.write(data[sented:to_send])
            cipsend = ATCommand(
                "AT+CIPSEND={},{}".format(self._fd, to_send),
                "+CIPSEND:",
                "ERROR\r\n",
                self._modem._default_timeout,
            )
            output, error = self._modem.response_at_command2(cipsend)
            if error == self._modem.ERR_GENERIC:
                err = utils.extract_int(output, "\+CIPERROR: ", "\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, err, cipsend.cmd)
            elif error == self._modem.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, error, cipsend.cmd)
            elif error == self._modem.ERR_NONE:
                cnf = utils.extract_text(
                    output, "\+CIPSEND: {},{},".format(self._fd, to_send), "\r\n"
                )
                sented = int(cnf) if cnf else 0
        return to_send

    def sendall(self, data: bytes | str | bytearray) -> None:
        self.send(data)

    def sendto(self, data: bytes | str | bytearray, address) -> int:
        if self._state == self._STATE_CLOSE:
            self._local_port = self._modem.apply_port()
            cipopen = ATCommand(
                "AT+CIPOPEN={},{},,,{}".format(
                    self._fd,
                    "".join(['"', self._proto_type.get(self._proto, ""), '"']),
                    self._local_port,
                ),
                "OK\r\n",
                "ERROR\r\n",
                self._modem._default_timeout,
            )
            output, error = self._modem.execute_at_command2(cipopen)
            if error == self._modem.ERR_GENERIC:
                errno = utils.extract_int(output, "\+CIPOPEN: ", "\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, errno, cipopen.cmd)
            elif error == self._modem.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, error, cipopen.cmd)
            self._state = self._STATE_OPEN

        # data type check
        if isinstance(data, str):
            data = data.encode("utf-8")
        if isinstance(data, bytearray):
            data = bytes(data)

        # send cmd
        to_send = len(data)
        cipsend = ATCommand(
            "AT+CIPSEND={},{},{},{}".format(
                self._fd, to_send, "".join(['"', address[0], '"']), address[1]
            ),
            ">",
            "ERROR\r\n",
            self._modem._default_timeout,
        )
        output, error = self._modem.execute_at_command2(cipsend, line_end="")
        if error == self._modem.ERR_GENERIC:
            errno = utils.extract_int(output, "\+CIPSEND: ", "\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR, errno, cipsend.cmd)
        elif error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, cipsend.cmd)

        sented = 0
        while sented < to_send:
            self._modem.uart.write(data[sented:to_send])
            cipsend = ATCommand(
                "AT+CIPSEND={},{}".format(self._fd, to_send),
                "+CIPSEND:",
                "ERROR\r\n",
                self._modem._default_timeout,
            )
            output, error = self._modem.response_at_command2(cipsend)
            if error == self._modem.ERR_GENERIC:
                errno = utils.extract_int(output, "\+CIPERROR: ", "\r\n")
                raise SIMComError(SIMComError.D_TCPIP_ERR, errno, cipsend.cmd)
            elif error == self._modem.ERR_TIMEOUT:
                raise SIMComError(SIMComError.D_GENERIC, error, cipsend.cmd)
            else:
                cnf = utils.extract_text(
                    output, "\+CIPSEND: {},{},".format(self._fd, to_send), "\r\n"
                )
                sented = int(cnf) if cnf else 0
        return to_send

    def _recv(self) -> None:
        ciprxget = ATCommand(
            "AT+CIPRXGET=4,{}".format(self._fd),
            "OK\r\n",
            "ERROR\r\n",
            self._modem._default_timeout,
        )
        output, error = self._modem.execute_at_command2(ciprxget)
        if error == self._modem.ERR_GENERIC:
            errno = utils.extract_int(output, "\+IP ERROR: ", "\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR_INFO, errno, ciprxget.cmd)
        elif error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, ciprxget.cmd)

        to_recv = int(utils.extract_text(output, "\+CIPRXGET: 4,{},".format(self._fd), "\r\n"))
        if to_recv == 0:
            return

        to_recv = (1500 - self._ringio.any()) if to_recv > (1500 - self._ringio.any()) else to_recv

        ciprxget = ATCommand(
            "AT+CIPRXGET=2,{},{}".format(self._fd, to_recv),
            "OK\r\n",
            "ERROR\r\n",
            self._modem._default_timeout,
        )
        output, error = self._modem.execute_at_command2(ciprxget)
        if error == self._modem.ERR_GENERIC:
            errno = utils.extract_int(output, "\+IP ERROR: ", "\r\n")
            raise SIMComError(SIMComError.D_TCPIP_ERR_INFO, errno, ciprxget.cmd)
        elif error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, ciprxget.cmd)

        # prase data
        read_len = utils.extract_text(output, "\+CIPRXGET: 2,{},".format(self._fd), ",")
        read_len = int(read_len) if read_len else 0
        rest_len = utils.extract_text(
            output, "\+CIPRXGET: 2,{},{},".format(self._fd, read_len), "\r\n"
        )
        rest_len = int(rest_len) if rest_len else 0
        fstr = "+CIPRXGET: 2,{},{},{}\r\n".format(self._fd, read_len, rest_len)
        start = output.find(fstr) + len(fstr)

        self._ringio.write(output[start : start + read_len].encode("utf-8"))

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

        return bytes(out)

    def setsockopt(self, level, optname, value):
        raise NotImplementedError

    def settimeout(self, timeout):
        if timeout is None:
            self._timeout = 500

        cipccfg = ATCommand("AT+CIPCCFG?", "OK\r\n", "ERROR\r\n", self._modem._default_timeout)
        output, error = self._modem.execute_at_command2(cipccfg)
        if error == self._modem.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, cipccfg.cmd)

        params = utils.extract_number(output)

        cipccfg = ATCommand(
            "AT+CIPCCFG={},{},{},{},{},{},{}".format(
                params[0], params[1], params[2], params[3], params[4], params[5], self._timeout
            ),
            "OK\r\n",
            "ERROR\r\n",
            self._modem._default_timeout,
        )

    def setblocking(self):
        raise NotImplementedError

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


class SIM7600(Modem):
    # tcp/udp socket fd list
    _fds = [-1 for _ in range(10)]

    # tcp/udp socket port list
    _used_port = []

    def __init__(
        self,
        uart=None,
        pwrkey_pin=None,
        reset_pin=None,
        power_pin=None,
        tx_pin=None,
        rx_pin=None,
        verbose=False,
    ):
        super().__init__(uart, pwrkey_pin, reset_pin, power_pin, tx_pin, rx_pin, verbose)
        self._default_timeout = 5000

        # disable echo
        self.execute_at_command2(ATCommand("ATE0", "OK\r\n", "ERROR\r\n", self._default_timeout))

        # buffer access mode
        self.execute_at_command2(
            ATCommand("AT+CIPRXGET=1", "OK\r\n", "ERROR\r\n", self._default_timeout)
        )
        # No transparent transmission mode
        self.execute_at_command2(
            ATCommand("AT+CIPMODE=0", "OK\r\n", "ERROR\r\n", self._default_timeout)
        )
        # open network
        self.execute_at_command2(
            ATCommand("AT+NETOPEN", "OK\r\n", "ERROR\r\n", self._default_timeout)
        )

    """fd/port management"""

    def apply_fd(self) -> int:
        for i in range(10):
            if self._fds[i] == -1:
                self._fds[i] = i
                return i
        return -1

    def release_fd(self, fd: int) -> None:
        self._fds[fd] = -1

    def apply_port(self) -> int:
        for i in range(1024, 65535):
            if i not in self._used_port:
                self._used_port.append(i)
                return i
        return -1

    def release_port(self, port: int) -> None:
        self._used_port.remove(port)

    """socket method"""

    def getaddrinfo(self, host, port, af=0, type=0, proto=0, flags=0):
        """
        The resulting list of 5-tuples has the following structure:
            (family, type, proto, canonname, sockaddr)
        """
        res = []

        at = ATCommand('AT+CDNSGIP="{}"'.format(host), "OK\r\n", "ERROR\r\n", 10000)
        output, error = self.execute_at_command2(at)

        ip = "0.0.0.0"
        if error == self.ERR_NONE:
            ip = utils.extract_text(output, '"{}","'.format(host), '"')
        elif error == self.ERR_TIMEOUT:
            raise SIMComError(SIMComError.D_GENERIC, error, at.cmd)
        elif error == self.ERR_GENERIC:
            raise SIMComError(SIMComError.D_DNS_ERROR_CODE, 10, at.cmd)

        res.append((socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, host, (ip, port)))
        return res

    def socket(self, af=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP):
        return _socket(self, af, type, proto)

    # def wrap_socket(
    #     self,
    #     sock,
    #     server_side=False,
    #     key=None,
    #     cert=None,
    #     cert_reqs=CERT_NONE,
    #     cadata=None,
    #     server_hostname=None,
    #     do_handshake=True,
    # ):
    #     sock.close()
    #     s = _sockets(self, sock._domain, sock._type, sock._proto)
    #     s.connect(sock._address)
    #     return s

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

    """common method"""

    def check_modem_is_ready(self) -> bool:
        # Check if modem is ready for AT command
        at = ATCommand("AT", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(at, True)
        return not error

    def set_command_echo_mode(self, state=1) -> bool:
        # Set echo mode off or on
        at = ATCommand("ATE{}".format(state), "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(at)
        return not error

    def check_sim_is_connected(self) -> bool:
        # Check the SIM card is connected or not?
        at = ATCommand("AT+CPIN?", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(at)
        if error:
            return False
        return True if output.find("READY") != -1 else False

    REG_NO_RESULT = -1
    REG_UNREGISTERED = 0
    REG_SEARCHING = 2
    REG_DENIED = 3
    REG_OK_HOME = 1
    REG_OK_ROAMING = 5
    REG_UNKNOWN = 4

    def get_network_registration_status(self) -> int:
        # Get the registration status with the network
        creg = ATCommand("AT+CGREG?", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(creg)
        if error:
            return self.REG_NO_RESULT
        n = utils.extract_int(output, "+CGREG: ", ",")
        stat = utils.extract_int(output, "+CGREG: {}".format(n), "\r\n" if n == 0 else ",")
        return stat

    def get_signal_strength(self) -> int:
        # Get the signal strength
        csq = ATCommand("AT+CSQ", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(csq)
        if error:
            return 99

        rssi = utils.extract_int(output, "+CSQ: ", ",")
        return rssi

    def get_gprs_registration_status(self):
        # Get the registration status with the gprs network
        return self.get_network_registration_status()

    def get_model_identification(self) -> str:
        # Query the model identification information
        cgmm = ATCommand("AT+CGMM", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(cgmm)
        if error:
            return ""
        return utils.extract_text(output, "\r\n", "\r\n")

    def get_gprs_network_status(self) -> bool:
        # Get attach or detach from the GPRS network
        cgatt = ATCommand("AT+CGATT?", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(cgatt)
        if error:
            return False
        state = utils.extract_int(output, "+CGATT: ", "\r\n")
        return True if state == 1 else False

    def set_gprs_network_state(self, enable=1) -> bool:
        # Set attach or detach from the GPRS network
        cgatt = ATCommand("AT+CGATT={0}".format(enable), "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(cgatt)
        if error:
            return False
        state = utils.extract_int(output, "+CGATT: ", "\r\n")
        return True if state == enable else False

    def set_pdp_context(self, apn=""):
        # Set Define PDP Context
        cgdcont = ATCommand(
            'AT+CGDCONT=1,"IP","{}"'.format(apn), "OK", "ERROR", self._default_timeout
        )
        output, error = self.execute_at_command2(cgdcont)
        return not error

    def get_show_pdp_address(self, cid) -> str:
        # Get Show PDP address.
        # cid: 1 - 24
        cgpaddr = ATCommand("AT+CGPADDR={}".format(cid), "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(cgpaddr)
        if error:
            return "0.0.0.0"
        address = utils.extract_text(output, '+CGPADDR: {},"'.format(cid), '"')
        return address

    def get_selected_operator(self) -> int:
        # Get selected operator.
        cops = ATCommand("AT+COPS?", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(cops)
        if error:
            return 0
        return utils.extract_int(output, "+COPS: ", ",")

    def get_imei_number(self):
        # Request TA Serial Number Identification(IMEI)
        cgsn = ATCommand("AT+CGSN=1", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(cgsn)
        if error:
            return ""
        return utils.extract_text(output, "\r\n", "\r\n")

    def get_ccid_number(self) -> str:
        # Show ICCID
        iccid = ATCommand("AT+ICCID", "OK", "ERROR", self._default_timeout)
        output, error = self.execute_at_command2(iccid)
        if error:
            return ""
        return utils.extract_text(output, "+ICCID: ", "\r\n")

    PDP_PARAM_IP = 1
    PDP_PARAM_APN = 2

    def get_pdp_context_dynamic_parameters(self, param=1) -> str:
        # PDP Context Read Dynamic Parameters
        if param == self.PDP_PARAM_IP:
            return self.get_show_pdp_address(1)
        elif param == self.PDP_PARAM_APN:
            cgdcont = ATCommand("AT+CGDCONT?", "OK", "ERROR", self._default_timeout)
            output, error = self.execute_at_command2(cgdcont)
            if error:
                return ""
            return utils.extract_text(output, '+CGDCONT: 1,"IP","', '"')

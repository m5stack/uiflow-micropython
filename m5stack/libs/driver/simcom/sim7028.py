# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import sim7020
from driver.umodem import modem as umodem
from driver.umodem.parser import Parser
from . import utils
import time
import socket
import micropython
import binascii


# TCP/UDP socket
class _socket(sim7020._socket):
    def close(self) -> None:
        if self._fd == -1:
            return
        cmd = umodem.Command(
            "+CIPCLOSE",
            umodem.Command.CMD_WRITE,
            self._fd,
            timeout=10000,
        )

        self._modem.execute(cmd)
        self._modem.release_fd(self._fd)
        self._fd = -1
        self._state = self._STATE_CLOSE
        if hasattr(self, "_local_port"):
            self._modem.release_port(self._local_port)

    def connect(self, address: tuple[str, int]):
        if self._fd == -1:
            raise sim7020.SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return

        self._address = address
        # _fd is connect num
        cmd = umodem.Command(
            "+CIPOPEN",
            umodem.Command.CMD_WRITE,
            self._fd,
            self._proto_type.get(self._proto, ""),
            address[0],
            address[1],
            rsp1="+CIPOPEN:",
            timeout=160000,
        )
        resp = self._modem.execute(cmd)
        if resp.status_code == resp.ERR_NONE:
            self._state = self._STATE_OPEN
            return True
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise sim7020.SIMComError(sim7020.SIMComError.D_GENERIC, resp.status_code, cmd)
        elif resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("{},".format(self._fd).encode())
            err = parser.parseutil(b"\r\n")
            raise sim7020.SIMComError(err.decode())

    def send(self, data: bytes | str | bytearray) -> int:
        # data type check
        data = utils.converter(data, bytes)
        # print(f"tcp data: {data}")
        total_length = len(data)
        total_sent = 0

        max_segment_size = 1500

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
                parser.skipuntil(b"+CIPERROR: ")
                err = parser.parseutil(b"\r\n")
                raise sim7020.SIMComError(sim7020.SIMComError.D_TCPIP_ERR, err, cmd.cmd)
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise sim7020.SIMComError(sim7020.SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            self._modem.uart.write(segment_data)

            cmd = umodem.Command(
                "+CIPSEND",
                umodem.Command.CMD_EXEC,
                rsp1="+CIPSEND",
                rsp2="+CIPERROR",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.response_at_command2(cmd)

            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("{},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
                raise sim7020.SIMComError(err.decode())
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise sim7020.SIMComError(sim7020.SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            total_sent += segment_size
            # print(f"Sent segment: {segment_size} bytes, Total: {total_sent}/{total_length}")

        return total_length

    def sendall(self, data: bytes | str | bytearray) -> None:
        self.send(data)

    def sendto(self, data: bytes | str | bytearray, address) -> int:
        if self._state == self._STATE_CLOSE:
            self._local_port = self._modem.apply_port()
            cipopen = umodem.Command(
                "+CIPSEND",
                umodem.Command.CMD_WRITE,
                self._fd,
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
                raise sim7020.SIMComError(err.decode())
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise sim7020.SIMComError(
                    sim7020.SIMComError.D_GENERIC, resp.status_code, cipopen.cmd
                )
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
                parser.skipuntil(b"+CIPERROR: ")
                err = parser.parseutil(b"\r\n")
                raise sim7020.SIMComError(sim7020.SIMComError.D_TCPIP_ERR, err, cmd.cmd)
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise sim7020.SIMComError(sim7020.SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            self._modem.uart.write(segment_data)

            cmd = umodem.Command(
                "+CIPSEND",
                umodem.Command.CMD_EXEC,
                rsp1="+CIPSEND",
                rsp2="+CIPERROR",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.response_at_command2(cmd)

            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("{},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
                raise sim7020.SIMComError(err.decode())
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise sim7020.SIMComError(sim7020.SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

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
            parser.skipuntil(b"+IP ERROR:")
            err = parser.parseutil(b"\r\n")
            raise sim7020.SIMComError(sim7020.SIMComError.D_TCPIP_ERR, err, ciprxget.cmd)
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise sim7020.SIMComError(
                sim7020.SIMComError.D_GENERIC, resp.status_code, ciprxget.cmd
            )

        parser = Parser(resp.content)
        parser.skipuntil("+CIPRXGET: 4,{},".format(self._fd).encode())
        to_recv = parser.parseint(b"\r\n")
        # print(f"to_recv: {to_recv}")
        if to_recv == 0:
            return

        to_recv = (1500 - self._ringio.any()) if to_recv > (1500 - self._ringio.any()) else to_recv

        # using hex format to receive data
        ciprxget = umodem.Command(
            "+CIPRXGET",
            umodem.Command.CMD_WRITE,
            3,
            self._fd,
            to_recv,
            timeout=self._modem._default_timeout,
        )
        resp = self._modem.execute(ciprxget)
        if resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("+CME ERROR ".encode())
            errno = parser.parseutil(b"\r\n")
            raise sim7020.SIMComError(sim7020.SIMComError.D_TCPIP_ERR_INFO, errno, ciprxget.cmd)
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise sim7020.SIMComError(
                sim7020.SIMComError.D_GENERIC, resp.status_code, ciprxget.cmd
            )

        # prase data
        parser = Parser(resp.content)
        parser.skipuntil("+CIPRXGET: 3,{},".format(self._fd).encode())
        read_len = parser.parseint()
        parser.skipuntil("+CIPRXGET: 3,{},{},".format(self._fd, read_len).encode())
        rest_len = parser.parseint(b"\r\n")
        fstr = utils.converter(
            "+CIPRXGET: 3,{},{},{}\r\n\r\n".format(self._fd, read_len, rest_len),
            type(resp.content),
        )
        start = resp.content.find(fstr) + len(fstr)

        self._ringio.write(binascii.unhexlify(resp.content[start : start + read_len * 2]))

    def setsockopt(self, level, optname, value):
        print("setsockopt is not implemented")


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

    def __init__(self, modem: "SIM7028", af=AF_INET, type=SOCK_STREAM, proto=IPPROTO_TCP):
        self._modem = modem
        self._domain = af
        self._type = type
        self._proto = proto
        self._fd = self._modem.apply_session_id()
        self._address = None
        if self._fd == -1:
            raise sim7020.SIMComError("No available session")

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
            "+CCHCLOSE",
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
            raise sim7020.SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return
        # Set the first SSL context to be used in the SSL connection
        cmd = umodem.Command(
            "+CSSLCFG",
            umodem.Command.CMD_WRITE,
            "authmode",
            self._fd,  # tid
            0,  # no authentication.
            timeout=self._modem._default_timeout,
        )
        resp = self._modem.execute(cmd)
        return resp.status_code == resp.ERR_NONE

    def connect(self, address):
        if self._fd == -1:
            raise sim7020.SIMComError("socket closed")

        if self._state == self._STATE_OPEN:
            return

        self._address = address
        cipstart = umodem.Command(
            "+CCHOPEN",
            umodem.Command.CMD_WRITE,
            self._fd,
            address[0],
            address[1],
            2,  # SSL/TLS client.
            rsp1="+CCHOPEN:",
            timeout=60000,
        )
        resp = self._modem.execute(cipstart)

        if resp.status_code == resp.ERR_NONE:
            self._state = self._STATE_OPEN
            self._connect_time = time.ticks_ms()
            return True
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise sim7020.SIMComError(
                sim7020.SIMComError.D_GENERIC, resp.status_code, cipstart.cmd
            )
        elif resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("+CCHOPEN: {},".format(self._fd).encode())
            err = parser.parseutil(b"\r\n")
            raise sim7020.SIMComError(sim7020.SIMComError.D_TCPIP_ERR, err, cipstart.cmd)

    def send(self, data: bytes | str | bytearray) -> int:
        # data type check
        data = utils.converter(data, bytes)
        # print(f"raw data: {repr(data)}")
        # data = data.decode("utf-8").replace("\r\n", "\\r\\n")
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
                "+CCHSEND",
                umodem.Command.CMD_WRITE,
                self._fd,
                segment_size,
                rsp1=">",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.execute(cmd, line_end="")
            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("+CCHSEND: {},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
                raise sim7020.SIMComError(sim7020.SIMComError.D_TCPIP_ERR, err, cmd.cmd)
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise sim7020.SIMComError(sim7020.SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            self._modem.uart.write(segment_data)
            self._modem._log("TE -> TA:", repr(segment_data))

            cmd = umodem.Command(
                "+CCHSEND",
                umodem.Command.CMD_EXEC,
                rsp1="+CCHSEND",
                timeout=self._modem._default_timeout,
            )
            resp = self._modem.response_at_command2(cmd)

            if resp.status_code == resp.ERR_GENERIC:
                parser = Parser(resp.content)
                parser.skipuntil("{},".format(self._fd).encode())
                err = parser.parseutil(b"\r\n")
                raise sim7020.SIMComError(err.decode())
            elif resp.status_code == resp.ERR_TIMEOUT:
                raise sim7020.SIMComError(sim7020.SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

            total_sent += segment_size
            # print(f"Sent segment: {segment_size} bytes, Total: {total_sent}/{total_length}")

        return total_length

    def sendall(self, data: bytes | str | bytearray) -> None:
        self.send(data)

    def _recv(self) -> None:
        cmd = umodem.Command(
            "+CCHRECV",
            umodem.Command.CMD_WRITE,
            self._fd,
            512,  # max length to receive
            rsp1="CCHRECV:",
            timeout=self._modem._default_timeout,
        )
        resp = self._modem.execute(cmd)
        if resp.status_code == resp.ERR_GENERIC:
            parser = Parser(resp.content)
            parser.skipuntil("+CCHRECV: {},".format(self._fd).encode())
            errno = parser.parseutil(b"\r\n")
            raise sim7020.SIMComError(sim7020.SIMComError.D_TCPIP_ERR_INFO, errno, cmd.cmd)
        elif resp.status_code == resp.ERR_TIMEOUT:
            raise sim7020.SIMComError(sim7020.SIMComError.D_GENERIC, resp.status_code, cmd.cmd)

        # print(f"resp.content: {resp.content}")
        parser = Parser(resp.content)
        find_data = 0
        while True:
            if parser.skipuntil("+CCHRECV: DATA,{},".format(self._fd).encode()) != find_data:
                recv_len = parser.parseint(b"\r\n")

                if recv_len is not None and recv_len > 0:
                    fstr = utils.converter(
                        "+CCHRECV: DATA,{},{}".format(self._fd, recv_len), type(resp.content)
                    )
                    start = resp.content.find(fstr) + len(fstr)
                    data = resp.content[start : start + recv_len]
                    # print(f"data: {data}")
                    self._ringio.write(data)
            else:
                break

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


class SIM7028(sim7020.SIM7020):
    # tcp/udp socket fd list

    SOCKET_COUNT = 2
    SSL_COUNT = 2

    _fds = [-1 for _ in range(SOCKET_COUNT)]

    _session_id = [-1 for _ in range(SSL_COUNT)]

    def __init__(
        self, uart=None, pwrkey_pin=None, reset_pin=None, power_pin=None, verbose=False
    ) -> None:
        super().__init__(
            uart=uart,
            pwrkey_pin=pwrkey_pin,
            reset_pin=reset_pin,
            power_pin=power_pin,
            verbose=verbose,
        )
        self._socket_initialized = False
        self._ssl_initialized = False

    def connect(self, apn=None):
        # reference SIM7028 Series_TCPIP_Application Note_V1.03.pdf
        if apn is None:
            apn = "CMNET"

        # Check SIM card status
        while self.status("pin") != self.PIN_READY:
            time.sleep(0.1)
            if self._verbose:
                print("Waiting for SIM card ready...")

        # Check RF signal
        while self.status("rssi") < -109:
            time.sleep(0.1)
            if self._verbose:
                print("Waiting for signal...")

        # Network Registration
        while True:
            cmd = umodem.Command("+CREG", umodem.Command.CMD_READ, timeout=self._default_timeout)
            resp = self.execute(cmd)
            if resp.status_code == umodem.Response.ERR_NONE:
                break
            time.sleep(0.1)
            if self._verbose:
                print("Waiting for network registration...")

        # EPS Network Registration Status
        while True:
            cmd = umodem.Command("+CEREG", umodem.Command.CMD_READ, timeout=self._default_timeout)
            resp = self.execute(cmd)
            if resp.status_code == umodem.Response.ERR_NONE:
                break
            time.sleep(0.1)
            if self._verbose:
                print("Waiting for EPS network registration...")

        # Inquiring UE system information
        while True:
            # Activate PDP context
            cmd = umodem.Command("+CPSI", umodem.Command.CMD_READ, timeout=self._default_timeout)
            resp = self.execute(cmd)
            if resp.status_code == umodem.Response.ERR_NONE:
                break
            time.sleep(0.1)
            if self._verbose:
                print("Waiting for UE system information...")

    def reset(self):
        pass

    def socket(self, af=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP):
        if self._socket_initialized is False:
            # Open TCP/IP stack
            cmd = umodem.Command(
                "+NETOPEN", umodem.Command.CMD_EXEC, timeout=self._default_timeout
            )
            resp = self.execute(cmd)
            if (
                resp.status_code != umodem.Response.ERR_NONE
                and resp.content.find(b"Network is already opened") == -1
            ):
                raise sim7020.SIMComError("Failed to open network")

            # buffer access mode
            cmd = umodem.Command(
                "+CIPRXGET", umodem.Command.CMD_WRITE, 1, timeout=self._default_timeout
            )
            resp = self.execute(cmd)
            if resp.status_code != umodem.Response.ERR_NONE:
                raise sim7020.SIMComError("Failed to set buffer access mode")

            self._socket_initialized = True

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
        sock.close()

        if self.config("version") == "2110B07SIM7028":
            raise sim7020.SIMComError("SIM7028 does not support SSL/TLS")

        if self._ssl_initialized is False:
            # Initialize TLS/SSL stack
            cmd = umodem.Command(
                "+CCHSTART", umodem.Command.CMD_EXEC, timeout=self._default_timeout
            )
            self.execute(cmd)
            self._ssl_initialized = True

        s = _sockets(self, sock._domain, sock._type, sock._proto)
        s.tls_config(sock._address)
        s.connect(sock._address)
        return s

    def get_ccid_number(self) -> str:
        """Show CICCID"""
        cmd = umodem.Command("+CICCID", umodem.Command.CMD_EXEC, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"+CICCID: ")
            return parser.parseutil(b"\r\n").decode()
        return ""

    def set_band(self, band: tuple) -> bool:
        lte_mode = sum(1 << (i - 1) for i in band)
        cmd = umodem.Command(
            "+CNBP",
            umodem.Command.CMD_WRITE,
            "0x{:016X}".format(lte_mode),
            timeout=self._default_timeout,
        )
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def get_band(self) -> tuple:
        cmd = umodem.Command("+CNBP", umodem.Command.CMD_READ, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"+CNBP: ")
            lte_mode = parser.parseint(chr=b"\r\n")
            return tuple([i + 1 for i in range(64) if (lte_mode >> i) & 1])
        return ()

    def _get_pdp_context_dynamic_parameters(self) -> tuple:
        """PDP Context Read Dynamic Parameters"""
        cmd = umodem.Command(
            "+CGCONTRDP",
            umodem.Command.CMD_WRITE,
            0,
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
        cmd = umodem.Command("+QCBCINFO", umodem.Command.CMD_EXEC, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = Parser(resp.content)
            parser.skipuntil(b"+QCBCINFOSC: ")
            station = []
            sc_earfcn = parser.parseint()  # sc_earfcn
            sc_pci = parser.parseint()  # sc_pci
            sc_rsrp = parser.parseint()  # sc_rsrp
            sc_rsrq = parser.parseint()  # sc_rsrq
            parser.parsestr()  # mcc
            parser.parsestr()  # mnc
            sc_cellid = parser.parsestr()  # sc_cellid
            sc_tac = parser.parsestr(b"\r\n")  # sc_tac

            station.append(sc_earfcn)  # sc_earfcn
            station.append(-1)  # sc_earfcn_offset
            station.append(sc_pci)  # sc_pci
            station.append(sc_cellid)  # sc_cellid
            station.append(sc_rsrp)  # sc_rsrp
            station.append(sc_rsrq)  # sc_rsrq
            station.append(-1)  # sc_rssi
            station.append(-1)  # sc_snr
            station.append(-1)  # sc_band
            station.append(sc_tac)  # sc_tac
            station.append(-1)  # sc_ecl
            station.append(-1)  # sc_tx_pwr
            station.append(-1)  # sc_re_rsrp

            # neighbor cell info
            parser.skipuntil(b"+QCBCINFONC: ")
            neighbor = []
            neighbor.append(parser.parseint())  # nc_earfcn
            neighbor.append(parser.parseint())  # nc_pci
            neighbor.append(parser.parseint())  # nc_rsrp
            neighbor.append(parser.parseint(b"\r\n"))  # nc_rsrq
            return (tuple(station), (tuple(neighbor),))
        return ((), ())

    def _convert_rssi(self, rssi) -> int:
        """return dbm"""
        if rssi == 0:
            return -113
        elif rssi == 1:
            return -111
        elif rssi >= 2 and rssi <= 30:
            return -109 + (rssi - 2) * 2
        elif rssi == 31:
            return -51
        return -113

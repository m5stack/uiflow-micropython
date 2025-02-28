# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import umodem
import machine
import socket
from .toolkit import requests2
from .toolkit import umqtt


class SIM7020(umodem.UModem):
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
        self._low_power_mode()

    def _low_power_mode(self):
        """enter low power mode"""
        cmd = umodem.Command("+CFUN", umodem.Command.CMD_WRITE, 0, timeout=10000)
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
            cmd = umodem.Command("+CPIN", umodem.Command.CMD_READ, timeout=self._default_timeout)
            self.execute(cmd)
            # Check RF signal
            cmd = umodem.Command(
                "+CSQ", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout
            )
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
        cmd = umodem.Command(
            "+CGCONTRDP", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout
        )
        self.execute(cmd)

    def disconnect(self):
        # 断开PDP连接，但是RF还是开启的
        raise NotImplementedError

    def isconnected(self) -> bool:
        parameters = self._get_pdp_context_dynamic_parameters()
        return parameters[3] != "0.0.0.0" and parameters[3] != ""

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
                parser = umodem.Parser(resp.content)
                parser.skipuntil("+CSQ: ")
                rssi = parser.parseint()
                return self._convert_rssi(rssi)
        elif param == "pin":
            cmd = umodem.Command("+CPIN", umodem.Command.CMD_READ, timeout=self._default_timeout)
            resp = self.execute(cmd)
            if resp.status_code == umodem.Response.ERR_NONE:
                parser = umodem.Parser(resp.content)
                parser.skipuntil("+CPIN: ")
                code = parser.parseutil("\r\n").replace('"', "")
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
            "+CGCONTRDP", umodem.Command.CMD_WRITE, self._cid, timeout=self._default_timeout
        )
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = umodem.Parser(resp.content)
            parser.skipuntil("+CGCONTRDP: ")
            cid = parser.parseint()  # cid
            bearer_id = parser.parseint()  # bearer_id
            apn = parser.parseutil(",").strip('"')  # apn
            locl_ip = parser.parseutil(",").strip('"')  # local_ip and subnet_mask
            if locl_ip.count(".") == 7:
                # ipv4
                parts = locl_ip.split(".")
                locl_ip = ".".join(parts[:4])
                subnet_mask = ".".join(parts[4:])
            elif locl_ip.count(".") == 31:
                # ipv6
                parts = locl_ip.split(".")
                locl_ip = ".".join(parts[:16])
                subnet_mask = ".".join(parts[16:])
            else:
                locl_ip = "0.0.0.0"
                subnet_mask = "0.0.0.0"
            gateway = parser.parseutil(",").strip('"')  # gateway
            gateway = gateway if gateway != "" else "0.0.0.0"
            dns1 = parser.parseutil(",").strip('"')
            dns1 = dns1 if dns1 != "" else "0.0.0.0"
            dns2 = parser.parseutil(",").strip('"')
            dns2 = dns2 if dns2 != "" else "0.0.0.0"
            return (cid, bearer_id, apn, locl_ip, subnet_mask, gateway, dns1, dns2)
        else:
            return (-9999, -9999, "", "0.0.0.0", "0.0.0.0", "0.0.0.0", "0.0.0.0", "0.0.0.0")

    def _get_network_state(self):
        cmd = umodem.Command("+CENG", umodem.Command.CMD_READ, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            num = resp.content.count("+CENG: ")
            if num == 0:
                return ((), ())
            parser = umodem.Parser(resp.content)
            parser.skipuntil("+CENG: ")
            station = []
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseutil(",").strip('"'))
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseutil(",").strip('"'))
            station.append(parser.parseint())
            station.append(parser.parseint())
            station.append(parser.parseint(chr="\r"))
            neighbors = []
            for _ in range(num - 1):
                parser.skipuntil("+CENG: ")
                neighbor = []
                neighbor.append(parser.parseint())
                neighbor.append(parser.parseint())
                neighbor.append(parser.parseint())
                neighbor.append(parser.parseint(chr="\r"))
                neighbors.append(tuple(neighbor))
            return (tuple(station), tuple(neighbors))
        return ((), ())

    def getaddrinfo(self, host, port, af=0, type=0, proto=0, flags=0):
        """
        The resulting list of 5-tuples has the following structure:
            (family, type, proto, canonname, sockaddr)
        """

    def socket(self, af=socket.AF_INET, type=socket.SOCK_STREAM, proto=socket.IPPROTO_TCP):
        """see sim7600"""
        raise NotImplementedError

    def wrap_socket(
        self,
        sock,
        # server_side=False,
        # key=None,
        # cert=None,
        # cert_reqs=CERT_NONE,
        # cadata=None,
        server_hostname=None,
        # do_handshake=True,
    ):
        """see sim7600"""
        raise NotImplementedError

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
            parser = umodem.Parser(resp.content)
            parser.skipuntil("+CBAND: ")
            parts = parser.parseutil("\r\n").split(",")
            return tuple([int(part) for part in parts])
        return ()

    def get_manufacturer(self) -> str:
        cmd = umodem.Command("+CGMI", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = umodem.Parser(resp.content)
            parser.skipuntil("\n")
            return parser.parseutil("\r\n")
        return ""

    def get_model_id(self) -> str:
        cmd = umodem.Command("+CGMM", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = umodem.Parser(resp.content)
            parser.skipuntil("\n")
            return parser.parseutil("\r\n")
        return ""

    def get_model_software_version(self) -> str:
        cmd = umodem.Command("+CGMR", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = umodem.Parser(resp.content)
            parser.skipuntil("\n")
            return parser.parseutil("\r\n")
        return ""

    def get_imei_number(self) -> str:
        """Request TA Serial Number Identification(IMEI)"""
        cmd = umodem.Command("+CGSN", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = umodem.Parser(resp.content)
            parser.skipuntil("\n")
            return parser.parseutil("\r\n")
        return ""

    def get_ccid_number(self) -> str:
        """Show ICCID"""
        cmd = umodem.Command("+CCID", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = umodem.Parser(resp.content)
            parser.skipuntil("\n")
            return parser.parseutil("\r\n")
        return ""

    def get_imsi_number(self) -> str:
        cmd = umodem.Command("+CIMI", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout)
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = umodem.Parser(resp.content)
            parser.skipuntil("\n")
            return parser.parseutil("\r\n")
        return ""

    """
    TODO: 下面的方法是pandian写的，需要测试，并且这些方法已经在 nb-iot unit使用了，需要做向前兼容
    """

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
            parser = umodem.Parser(resp.content)
            parser.skipuntil("+CGACT: ")
            parser.parseint()
            return bool(parser.parseint())
        return False

    def set_pdp_context_apn(self, apn="cmnbiot") -> bool:
        """Set Default PSD Connection Settings"""
        cmd = umodem.Command(
            "*MCGDEFCONT", umodem.Command.CMD_WRITE, "IP", apn, timeout=self._default_timeout
        )
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def get_pdp_context_dynamic_parameters(self, param=1):
        """PDP Context Read Dynamic Parameters"""
        cmd = umodem.Command(
            "+CGCONTRDP", umodem.Command.CMD_EXECUTION, timeout=self._default_timeout
        )
        resp = self.execute(cmd)
        if resp.status_code == umodem.Response.ERR_NONE:
            parser = umodem.Parser(resp.content)
            parser.parseint()  # cid
            parser.parseint()  # bearer_id
            apn = parser.parseutil(",").strip('"')  # apn
            locl_ip = parser.parseutil(",").strip('"')  # local_ip and subnet_mask
            parts = locl_ip.split(".")
            locl_ip = ".".join(parts[:4])  # local_ip. FIXME: support ipv6
            if param == 1:
                return locl_ip
            elif param == 2:
                return apn
        else:
            return ""

    # MQTT Test Server:mqtt.m5stack.com, Port:1883.
    def mqtt_server_connect(self, server, port, client_id, username, passwd, keepalive):
        cmd = umodem.Command(
            "+CMQNEW",
            umodem.Command.CMD_WRITE,
            server,
            port,
            12000,
            1024,
            timeout=self._default_timeout,
        )
        self._mqtt_id = 0
        # mqtt callback function keyword is set
        self.downlink_keyword.append("+CMQPUB:")
        self.callback_keyword.append("MQTT_CB")
        self.downlink_callback["MQTT_CB"] = self.mqtt_subscribe_cb

        self.mqtt_subscribe_cb_list = {}

        resp = self.execute(cmd)
        if resp.status_code != umodem.Response.ERR_NONE:
            return False
        self._mqtt_id = int(resp.content[-1])

        cmd = umodem.Command(
            "+CMQCON",
            umodem.Command.CMD_WRITE,
            self._mqtt_id,
            3,
            client_id,
            keepalive,
            1,
            0,
            username,
            passwd,
            timeout=self._default_timeout,
        )
        resp = self.execute(cmd)
        if resp.status_code != umodem.Response.ERR_NONE:
            return False

        result = self.mqtt_server_is_connect()
        return bool(result)

    def mqtt_server_disconnect(self):
        cmd = umodem.Command(
            "+CMQDISCON", umodem.Command.CMD_WRITE, self._mqtt_id, timeout=self._default_timeout
        )
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def mqtt_subscribe_topic(self, topic, cb, qos=0):
        # Subscribe topic(support wildcards).
        cmd = umodem.Command(
            "+CMQSUB",
            umodem.Command.CMD_WRITE,
            self._mqtt_id,
            topic,
            qos,
            timeout=self._default_timeout,
        )
        resp = self.execute(cmd)
        if resp.status_code != umodem.Response.ERR_NONE:
            return False
        if topic not in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list[topic] = cb
        return True

    def mqtt_unsubscribe_topic(self, topic):
        # Unsubscribe topic.
        cmd = umodem.Command(
            "+CMQUNSUB",
            umodem.Command.CMD_WRITE,
            self._mqtt_id,
            topic,
            timeout=self._default_timeout,
        )
        resp = self.execute(cmd)
        if resp.status_code != umodem.Response.ERR_NONE:
            return False
        if topic in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list.pop(topic)
        return True

    def mqtt_publish_topic(self, topic, payload, qos=0, retained=None, duplicate=None):
        # Publish message with topic.
        if retained is None and duplicate is None:
            cmd = umodem.Command(
                "+CMQPUB",
                umodem.Command.CMD_WRITE,
                self._mqtt_id,
                topic,
                qos,
                len(payload),
                payload,
                timeout=self._default_timeout,
            )
        else:
            cmd = umodem.Command(
                "+CMQPUB",
                umodem.Command.CMD_WRITE,
                self._mqtt_id,
                topic,
                qos,
                retained,
                duplicate,
                len(payload),
                payload,
                timeout=self._default_timeout,
            )

        resp = self.execute(cmd)
        if resp.status_code != umodem.Response.ERR_NONE:
            return False

    def mqtt_server_is_connect(self):
        # Check mqtt server connection.
        cmd = umodem.Command("+CMQCON?", umodem.Command.CMD_READ, timeout=self._default_timeout)
        resp = self.execute(cmd)
        return (
            False
            if resp.status_code != umodem.Response.ERR_NONE
            else int(resp.content.split(",")[1])
        )

    def mqtt_polling_loop(self):
        pass

    def mqtt_subscribe_cb(self, buffer):
        # main callback function
        topic = buffer.split('"')[1]
        payload = buffer.split('"')[3]
        if topic in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list[topic](topic, payload)

    # Create & Request Http(s)
    HTTPCLIENT_GET = 0
    HTTPCLIENT_POST = 1
    HTTPCLIENT_PUT = 2
    HTTPCLIENT_DELETE = 3

    def http_request(
        self, method=HTTPCLIENT_GET, url="http://api.m5stack.com/v1", headers={}, data=None
    ):
        # Create HTTP host instance
        proto, dummy, host, path = url.split("/", 3)
        find_url = url.find("/", 10)
        host = url[: find_url + 1]
        self.http_client_id = None
        self.response_code = 0
        self.data_content = ""

        cmd = umodem.Command(
            'AT+CHTTPCREATE="{0}"'.format(host), umodem.Command.CMD_EXECUTION, timeout=10
        )
        resp = self.execute(cmd)
        if resp.status_code != umodem.Response.ERR_NONE:
            return False
        self.http_client_id = int(resp.content[-1])

        output = self.http_server_connect()
        if output is False:
            return False

        temp_header = ""
        for head in headers.items():
            if head[0] == "Content-Type":
                contenttype = head[1]
            else:
                temp_header += self.make_header(head[0], head[1])

        if method == self.HTTPCLIENT_GET:
            cmd = umodem.Command(
                "+CHTTPSEND",
                umodem.Command.CMD_WRITE,
                self.http_client_id,
                self.HTTPCLIENT_GET,
                ("/" + path),
                timeout=10,
            )

        elif method == self.HTTPCLIENT_POST:
            temp_header = self.asciistr_to_hexstr(temp_header) if temp_header != "" else 0
            cmd = umodem.Command(
                "+CHTTPSEND",
                umodem.Command.CMD_WRITE,
                self.http_client_id,
                self.HTTPCLIENT_POST,
                ("/" + path),
                temp_header,
                contenttype,
                self.asciistr_to_hexstr(data),
                timeout=10,
            )

        resp = self.execute(cmd)
        if resp.status_code != umodem.Response.ERR_NONE:
            return False

        self.response_code = int(resp.content.split(",")[1])
        if self.response_code != 200:
            print('Response code: "{0}"'.format(self.response_code))
            return False

        if resp.content.find("+CHTTPNMIC:") != -1:  # noqa: N806
            self.data_content = self.hexstr_to_asciistr(resp.content.split(",")[-1])

        output = self.http_server_disconnect()
        if output is False:
            return False

        output = self.http_server_destroy()
        if output is False:
            return False

    def http_server_connect(self):
        # Http server is connect
        cmd = umodem.Command("+CHTTPCON", umodem.Command.CMD_WRITE, self.http_client_id, timeout=3)
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def http_server_is_connect(self):
        # Is check http server connect
        cmd = umodem.Command("+CHTTPCON?", umodem.Command.CMD_READ, timeout=3)
        resp = self.execute(cmd)
        output = resp.content.split("+CHTTPCON")
        output[self.http_client_id + 1].split(",")[1]
        return (
            False
            if resp.status_code != umodem.Response.ERR_NONE
            else int(output[self.http_client_id + 1].split(",")[1])
        )

    def http_server_disconnect(self):
        # http server disconnected
        cmd = umodem.Command(
            "+CHTTPDISCON", umodem.Command.CMD_WRITE, self.http_client_id, timeout=10
        )
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def http_server_destroy(self):
        # http server destroy
        cmd = umodem.Command(
            "+CHTTPDESTROY", umodem.Command.CMD_WRITE, self.http_client_id, timeout=10
        )
        resp = self.execute(cmd)
        return resp.status_code == umodem.Response.ERR_NONE

    def make_header(self, key, value):
        return str(key) + ":" + str(value) + "\n"

    def asciistr_to_hexstr(self, byte):
        return "".join(["%02X" % x for x in byte.encode()]).strip()

    def hexstr_to_asciistr(self, hex):
        return bytes.fromhex(hex).decode()

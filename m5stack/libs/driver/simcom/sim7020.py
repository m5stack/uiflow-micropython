# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.simcom.common import Modem
from collections import namedtuple


AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class SIM7020(Modem):
    def __init__(
        self,
        uart=None,
        MODEM_PWKEY_PIN=None,
        MODEM_RST_PIN=None,
        MODEM_POWER_ON_PIN=None,
        MODEM_TX_PIN=None,
        MODEM_RX_PIN=None,
    ) -> None:
        super().__init__(
            uart, MODEM_PWKEY_PIN, MODEM_RST_PIN, MODEM_POWER_ON_PIN, MODEM_TX_PIN, MODEM_RX_PIN
        )

    def get_imei_number(self):
        # Request TA Serial Number Identification(IMEI)
        CGSN = AT_CMD("AT+CGSN", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CGSN)
        return False if error else output

    def get_ccid_number(self):
        # Show ICCID
        CCID = AT_CMD("AT+CCID", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CCID)
        return False if error else output

    def set_pdp_context(self, active=1):
        # PDP Context Activate or Deactivate
        CGACT = AT_CMD("AT+CGACT={0},1".format(active), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CGACT)
        return False if error else output

    def get_pdp_context_status(self):
        # PDP Context Activate or Deactivate
        CGACT = AT_CMD("AT+CGACT?", "+CGACT:", 3)  # noqa: N806
        output, error = self.execute_at_command(CGACT)
        return False if error else int(output[-1])

    def set_pdp_context_apn(self, apn="cmnbiot"):
        # Set Default PSD Connection Settings
        MCGDEFCONT = AT_CMD('AT*MCGDEFCONT="IP","{}"'.format(apn), "OK", 12)  # noqa: N806
        output, error = self.execute_at_command(MCGDEFCONT)
        return not error

    def get_pdp_context_dynamic_parameters(self, param=1):
        # PDP Context Read Dynamic Parameters
        CGCONTRDP = AT_CMD("AT+CGCONTRDP", "+CGCONTRDP:", 5)  # noqa: N806
        output, error = self.execute_at_command(CGCONTRDP)
        if error:
            return False
        return (
            output.split(",")[-1].replace('"', "").rsplit(".", 4)[0]
            if param == 1
            else output.split(",")[-2].replace('"', "")
        )

    # MQTT Test Server:mqtt.m5stack.com, Port:1883.
    def mqtt_server_connect(self, server, port, client_id, username, passwd, keepalive):
        CMQNEW = AT_CMD(  # noqa: N806
            'AT+CMQNEW="{0}","{1}",{2},{3}'.format(server, port, 12000, 1024),  # noqa: N806
            "+CMQNEW",  # noqa: N806
            3,
        )
        self._mqtt_id = 0
        # mqtt callback function keyword is set
        self.downlink_keyword.append("+CMQPUB:")
        self.callback_keyword.append("MQTT_CB")
        self.downlink_callback["MQTT_CB"] = self.mqtt_subscribe_cb

        self.mqtt_subscribe_cb_list = {}

        output, error = self.execute_at_command(CMQNEW)
        if error:
            return False
        self._mqtt_id = int(output[-1])

        CMQCON = AT_CMD(  # noqa: N806
            'AT+CMQCON={0},{1},"{2}",{3},{4},{5},"{6}","{7}"'.format(  # noqa: N806
                self._mqtt_id, 3, client_id, keepalive, 1, 0, username, passwd
            ),
            "OK",  # noqa: N806
            3,
        )
        _, error = self.execute_at_command(CMQCON)
        if error:
            return False

        result = self.mqtt_server_is_connect()
        return bool(result)

    def mqtt_server_disconnect(self):
        SMDISC = AT_CMD("AT+CMQDISCON={0}".format(self._mqtt_id), "OK", 3)  # noqa: N806
        _, error = self.execute_at_command(SMDISC)
        return not error

    def mqtt_subscribe_topic(self, topic, cb, qos=0):
        # Subscribe topic(support wildcards).
        CMQSUB = AT_CMD('AT+CMQSUB={0},"{1}",{2}'.format(self._mqtt_id, topic, qos), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CMQSUB)
        if error:
            return False
        if topic not in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list[topic] = cb
        return True

    def mqtt_unsubscribe_topic(self, topic):
        # Unsubscribe topic.
        CMQUNSUB = AT_CMD('AT+CMQUNSUB={0},"{1}"'.format(self._mqtt_id, topic), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CMQUNSUB)
        if error:
            return False
        if topic in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list.pop(topic)
        return True

    def mqtt_publish_topic(self, topic, payload, qos=0, retained=None, duplicate=None):
        # Publish message with topic.
        if retained is None and duplicate is None:
            CMQPUB = AT_CMD(  # noqa: N806
                'AT+CMQPUB={0},"{1}",{2},0,0,{3},"{4}"'.format(  # noqa: N806
                    self._mqtt_id, topic, qos, len(payload), payload
                ),
                "OK",  # noqa: N806
                3,
            )
        else:
            CMQPUB = AT_CMD(  # noqa: N806
                'AT+CMQPUB={0},"{1}",{2},{3},{4},{5},"{6}"'.format(  # noqa: N806
                    self._mqtt_id, topic, qos, retained, duplicate, len(payload), payload
                ),
                "OK",  # noqa: N806
                3,
            )

        _, error = self.execute_at_command(CMQPUB)
        if error:
            return False

    def mqtt_server_is_connect(self):
        # Check mqtt server connection.
        CMQCON = AT_CMD("AT+CMQCON?", "+CMQCON:", 3)  # noqa: N806
        output, error = self.execute_at_command(CMQCON)
        return False if error else int(output.split(",")[1])

    def mqtt_polling_loop(self):
        DUMMY = AT_CMD("", "", 0)  # noqa: N806
        self.response_at_command(DUMMY)

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

        CHTTPCREATE = AT_CMD('AT+CHTTPCREATE="{0}"'.format(host), "+CHTTPCREATE:", 10)  # noqa: N806
        output, error = self.execute_at_command(CHTTPCREATE)
        if error:
            return False
        self.http_client_id = int(output[-1])

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
            CHTTPSEND = AT_CMD(  # noqa: N806
                'AT+CHTTPSEND={0},{1},"{2}"'.format(  # noqa: N806
                    self.http_client_id, self.HTTPCLIENT_GET, ("/" + path)
                ),
                "+CHTTPNMIC:",  # noqa: N806
                15,
            )

        elif method == self.HTTPCLIENT_POST:
            temp_header = self.asciistr_to_hexstr(temp_header) if temp_header != "" else 0
            CHTTPSEND = AT_CMD(  # noqa: N806
                'AT+CHTTPSEND={0},{1},"{2}",{3},"{4}",{5}'.format(  # noqa: N806
                    self.http_client_id,
                    self.HTTPCLIENT_POST,
                    ("/" + path),
                    temp_header,
                    contenttype,
                    self.asciistr_to_hexstr(data),
                ),
                "+CHTTPNMIC:",  # noqa: N806
                15,
            )

        output, error = self.execute_at_command(CHTTPSEND)
        if error:
            return False

        self.response_code = int(output.split(",")[1])
        if self.response_code != 200:
            print('Response code: "{0}"'.format(self.response_code))
            return False

        if output.find("+CHTTPNMIC:") != -1:  # noqa: N806
            self.data_content = self.hexstr_to_asciistr(output.split(",")[-1])

        output = self.http_server_disconnect()
        if output is False:
            return False

        output = self.http_server_destroy()
        if output is False:
            return False

    def http_server_connect(self):
        # Http server is connect
        CHTTPCON = AT_CMD("AT+CHTTPCON={0}".format(self.http_client_id), "OK", 20)  # noqa: N806
        _, error = self.execute_at_command(CHTTPCON)
        return not error

    def http_server_is_connect(self):
        # Is check http server connect
        CHTTPCON = AT_CMD("AT+CHTTPCON?", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CHTTPCON)
        output = output.split("+CHTTPCON")  # noqa: N806
        output[self.http_client_id + 1].split(",")[1]
        return False if error else int(output[self.http_client_id + 1].split(",")[1])

    def http_server_disconnect(self):
        # http server disconnected
        CHTTPDISCON = AT_CMD("AT+CHTTPDISCON={0}".format(self.http_client_id), "OK", 10)  # noqa: N806
        _, error = self.execute_at_command(CHTTPDISCON)
        return not error

    def http_server_destroy(self):
        # http server destroy
        CHTTPDESTROY = AT_CMD("AT+CHTTPDESTROY={0}".format(self.http_client_id), "OK", 10)  # noqa: N806
        _, error = self.execute_at_command(CHTTPDESTROY)
        return not error

    def make_header(self, key, value):
        return str(key) + ":" + str(value) + "\n"

    def asciistr_to_hexstr(self, byte):
        return "".join(["%02X" % x for x in byte.encode()]).strip()

    def hexstr_to_asciistr(self, hex):
        return bytes.fromhex(hex).decode()

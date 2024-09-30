# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


from driver.simcom.common import Modem
from collections import namedtuple
import re


AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class SIM7028(Modem):
    def __init__(
        self,
        uart=None,
        modem_pwkey_pin=None,
        modem_rst_pin=None,
        modem_power_on_pin=None,
        modem_tx_pin=None,
        modem_rx_pin=None,
    ) -> None:
        super().__init__(
            uart, modem_pwkey_pin, modem_rst_pin, modem_power_on_pin, modem_tx_pin, modem_rx_pin
        )

    def get_imei_number(self) -> str | bool:
        # Request TA Serial Number Identification(IMEI)
        CGSN = AT_CMD("AT+CGSN=1", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CGSN)
        return False if error else output

    def get_ccid_number(self) -> str | bool:
        # Show ICCID
        CICCID = AT_CMD("AT+CICCID", "+CICCID:", 3)  # noqa: N806
        output, error = self.execute_at_command(CICCID)
        return False if error else output.split(" ")[1]

    def get_pdp_context_dynamic_parameters(self, param=1) -> str | bool:
        # PDP Context Read Dynamic Parameters
        CGCONTRDP = AT_CMD("AT+CGCONTRDP", "+CGCONTRDP:", 5)  # noqa: N806
        output, error = self.execute_at_command(CGCONTRDP)
        if error:
            return False
        return (
            output.split(",")[4].replace('"', "")
            if param == 1
            else output.split(",")[2].replace('"', "")
        )

    # MQTT Test Server:mqtt.m5stack.com, Port:1883.
    def mqtt_server_configure(self, server, port, client_id, username, passwd, keepalive) -> bool:
        #! Connect to MQTT broker.
        self.mqtt_username = username
        self.mqtt_passwd = passwd
        self.mqtt_keepalive = keepalive
        self.mqtt_host_port = "tcp://" + server + ":" + str(port)
        self.clean_session = self.mqttclient_index = None
        self.mqtt_connect_status = False

        # mqtt callback function keyword is set
        self.downlink_keyword.append("+CMQTTRXTOPIC:")
        self.downlink_keyword.append("+CMQTTRXPAYLOAD:")
        self.downlink_keyword.append("+CMQTTCONNLOST:")
        self.callback_keyword.append("MQTT_CB")
        self.downlink_callback["MQTT_CB"] = self.mqtt_subscribe_cb
        self.mqtt_subscribe_cb_list = {}
        self.topic = self.message = None

        CMQTTSTART = AT_CMD("AT+CMQTTSTART", "+CMQTTSTART: 0", 12)  # noqa: N806
        output, error = self.execute_at_command(CMQTTSTART)
        if error or output[-1] != "0":
            return False

        CMQTTACCQ = AT_CMD('AT+CMQTTACCQ=0,"{0}"'.format(client_id), "OK", 5)  # noqa: N806
        _, error = self.execute_at_command(CMQTTACCQ)
        if error:
            return False

        return self.mqtt_server_connect(0)

    def mqtt_server_connect(self, clean_session=0) -> bool:
        self.clean_session = clean_session
        CMQTTCONNECT = AT_CMD(  # noqa: N806
            (
                'AT+CMQTTCONNECT=0,"{0}",{1},{2},"{3}","{4}"'.format(
                    self.mqtt_host_port,
                    self.mqtt_keepalive,
                    clean_session,
                    self.mqtt_username,
                    self.mqtt_passwd,
                )
                if len(self.mqtt_username) and len(self.mqtt_passwd)
                else 'AT+CMQTTCONNECT=0,"{0}",{1},{2}'.format(
                    self.mqtt_host_port, self.mqtt_keepalive, clean_session
                )
            ),
            "+CMQTTCONNECT:",
            30,
        )
        output, error = self.execute_at_command(CMQTTCONNECT)
        if error or output[-1] != "0":
            return False
        self.mqttclient_index = int(output[15])
        self.mqtt_connect_status = True
        return True

    def mqtt_server_disconnect(self) -> None | bool:
        CMQTTDISC = AT_CMD("AT+CMQTTDISC={0},120".format(self.mqttclient_index), "+CMQTTDISC:", 5)  # noqa: N806
        _, error = self.execute_at_command(CMQTTDISC)
        if error:
            return False
        CMQTTREL = AT_CMD("AT+CMQTTREL={0}".format(self.mqttclient_index), "OK", 5)  # noqa: N806
        _, error = self.execute_at_command(CMQTTREL)
        if error:
            return False
        CMQTTSTOP = AT_CMD("AT+CMQTTSTOP", "+CMQTTSTOP:", 5)  # noqa: N806
        _, error = self.execute_at_command(CMQTTSTOP)
        if error:
            return False

    def mqtt_subscribe_topic(self, topic, cb, qos=0) -> bool:
        # Subscribe topic(support wildcards).
        CMQTTSUB = AT_CMD(  # noqa: N806
            "AT+CMQTTSUB={0},{1},{2}".format(self.mqttclient_index, len(topic), qos), ">", 10
        )
        output, error = self.execute_at_command(CMQTTSUB)
        if error:
            return False
        TOPIC = AT_CMD("{0}".format(topic), "+CMQTTSUB:", 10)  # noqa: N806
        output, error = self.execute_at_command(TOPIC)
        if error or output[-1] != "0":
            return False
        if topic not in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list[topic] = cb
        return True

    def mqtt_unsubscribe_topic(self, topic) -> bool:
        # Unsubscribe topic.
        CMQTTUNSUB = AT_CMD(  # noqa: N806
            "AT+CMQTTUNSUB={0},{1}".format(self.mqttclient_index, len(topic)), ">", 10
        )
        output, error = self.execute_at_command(CMQTTUNSUB)
        if error:
            return False
        TOPIC = AT_CMD("{0}".format(topic), "+CMQTTUNSUB:", 10)  # noqa: N806
        output, error = self.execute_at_command(TOPIC)
        if error or output[-1] != "0":
            return False
        if topic in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list.pop(topic)
        return True

    def mqtt_publish_topic(self, topic, payload, qos=0) -> None | bool:
        # Publish message with topic.
        CMQTTTOPIC = AT_CMD(  # noqa: N806
            "AT+CMQTTTOPIC={0},{1}".format(self.mqttclient_index, len(topic)), ">", 10
        )
        _, error = self.execute_at_command(CMQTTTOPIC)
        if error:
            return False
        TOPIC = AT_CMD("{0}".format(topic), "OK", 10)  # noqa: N806
        _, error = self.execute_at_command(TOPIC)
        if error:
            return False

        CMQTTPAYLOAD = AT_CMD(  # noqa: N806
            "AT+CMQTTPAYLOAD={0},{1}".format(self.mqttclient_index, len(payload)), ">", 10
        )
        _, error = self.execute_at_command(CMQTTPAYLOAD)
        if error:
            return False
        TOPIC = AT_CMD("{0}".format(payload), "OK", 10)  # noqa: N806
        _, error = self.execute_at_command(TOPIC)
        if error:
            return False

        CMQTTPUB = AT_CMD(  # noqa: N806
            "AT+CMQTTPUB={0},{1},120".format(self.mqttclient_index, qos), "+CMQTTPUB:", 10
        )
        output, error = self.execute_at_command(CMQTTPUB)
        if error or output[-1] != "0":
            return False

    def mqtt_server_is_connect(self) -> bool:
        # Check mqtt server connection.
        CMQTTCONNECT = AT_CMD("AT+CMQTTCONNECT?", "+CMQTTCONNECT:", 5)  # noqa: N806
        output, error = self.execute_at_command(CMQTTCONNECT)
        if error:
            return False
        self.mqttclient_index = int(output[-1])
        return True if (output.split(",")[1].replace('"', "") == self.mqtt_host_port) else False

    def mqtt_polling_loop(self) -> None:
        DUMMY = AT_CMD("", "", 0)  # noqa: N806
        self.response_at_command(DUMMY)
        if self.mqtt_connect_status is not True:
            self.mqtt_server_connect(self.clean_session)

    def mqtt_subscribe_cb(self, buffer) -> None:
        # main callback function
        if "+CMQTTCONNLOST:" in buffer:
            self.mqtt_connect_status = False
        if "+CMQTTRXTOPIC:" in buffer:
            self.topic = self.message = None
            self.topic = buffer.split(",")[-1][:-2]
        if "+CMQTTRXPAYLOAD:" in buffer:
            self.message = buffer.split(",")[-1][:-1]
        if self.topic in self.mqtt_subscribe_cb_list.keys():
            if self.message:
                self.mqtt_subscribe_cb_list[self.topic](self.topic, self.message)
                self.topic = self.message = None

    # Create & Request Http(s)
    HTTPCLIENT_GET = 0
    HTTPCLIENT_POST = 1

    def http_request(
        self, method=HTTPCLIENT_GET, url="http://api.m5stack.com/v1", headers={}, data=None
    ) -> str | bool:
        # Create HTTP host instance
        self.response_code = 0
        self.data_content = ""

        self.set_pdp_context("cmnbiot")

        for i in range(3):
            HTTPINIT = AT_CMD("AT+HTTPINIT", "OK", 15)  # noqa: N806
            output, error = self.execute_at_command(HTTPINIT)
            if not error:
                break
            self.http_terminate()

        HTTPPARA = AT_CMD('AT+HTTPPARA="URL","{0}"'.format(url), "OK", 10)  # noqa: N806
        output, error = self.execute_at_command(HTTPPARA)
        if error:
            return False

        if method == self.HTTPCLIENT_POST:
            for head in headers.items():
                if head[0] == "Content-Type":
                    contenttype = head[1]

            HTTPPARA = AT_CMD('AT+HTTPPARA="CONTENT","{0}"'.format(contenttype), "OK", 5)  # noqa: N806
            output, error = self.execute_at_command(HTTPPARA)
            if error:
                return False
            HTTPPARA = AT_CMD("AT+HTTPDATA={0},3000".format(len(data)), "DOWNLOAD", 5)  # noqa: N806
            output, error = self.execute_at_command(HTTPPARA)
            if error:
                return False
            DATA = AT_CMD("{0}".format(data), "OK", 10)  # noqa: N806
            _, error = self.execute_at_command(DATA)
            if error:
                return False

        HTTPACTION = AT_CMD("AT+HTTPACTION={0}".format(method), "+HTTPACTION:", 25)  # noqa: N806
        output, error = self.execute_at_command(HTTPACTION)
        if error:
            return False

        self.response_code = int(output.split(",")[1])
        if self.response_code != 200:
            print('Response code: "{0}"'.format(self.response_code))
            return False

        HTTPREAD = AT_CMD("AT+HTTPREAD=0,500", "+HTTPREAD:", 25)  # noqa: N806
        output, error = self.execute_at_command(HTTPREAD)
        if error:
            return False
        match = re.search(r"\+HTTPREAD: (\d+)", output)
        if match:
            data_len = match.group(1)
        else:
            return False
        # data_len = ''.join(filter(str.isdigit, output.split(' ')[1]))
        data_index = len(output.split(" ")[0]) + len(data_len) + 1
        self.data_content = output[data_index : (data_index + int(data_len))]

    def http_terminate(self) -> bool:
        # http service terminate
        HTTPTERM = AT_CMD("AT+HTTPTERM", "OK", 15)  # noqa: N806
        _, error = self.execute_at_command(HTTPTERM)
        return not error

    def make_header(self, key, value) -> str:
        return str(key) + ":" + str(value) + "\n"

    def asciistr_to_hexstr(self, byte) -> bool:
        return "".join(["%02X" % x for x in byte.encode()]).strip()

    def hexstr_to_asciistr(self, hex) -> str:
        return bytes.fromhex(hex).decode()

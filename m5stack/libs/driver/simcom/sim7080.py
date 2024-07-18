# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.simcom.common import Modem
from collections import namedtuple


AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class SIM7080(Modem):
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

    def get_mode_selection(self):
        # get Preferred Selection between CAT-M and NB-IoT
        CMNB = AT_CMD("AT+CMNB?", "+CMNB:", 3)  # noqa: N806
        output, error = self.execute_at_command(CMNB)
        return False if error else int(output[-1])

    def get_imei_number(self):
        # Request TA Serial Number Identification(IMEI)
        GSN = AT_CMD("AT+GSN", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(GSN)
        return False if error else output

    def get_ccid_number(self):
        # Show ICCID
        CCID = AT_CMD("AT+CCID", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CCID)
        return False if error else output

    def set_mode_selection(self, mode=3):
        # get Preferred Selection between CAT-M and NB-IoT
        CMNB = AT_CMD("AT+CMNB={0}".format(mode), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CMNB)
        return not error

    def get_network_activated(self, pdp_id):
        # Get APP Network Active or Not
        CNACT = AT_CMD("AT+CNACT?", "+CNACT:", 3)  # noqa: N806
        output, error = self.execute_at_command(CNACT)
        return False if error else int(output.split("+CNACT: ")[pdp_id + 1][2])

    def set_network_active(self, pdp_id, action):
        # Set APP Network Active
        CNACT = AT_CMD("AT+CNACT={0},{1}".format(pdp_id, action), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CNACT)
        return not error

    def get_network_ip(self, pdp_id):
        # get APP Network IP Address
        CNACT = AT_CMD("AT+CNACT?", "+CNACT:", 3)  # noqa: N806
        output, error = self.execute_at_command(CNACT)
        return False if error else output.split("+CNACT: ")[pdp_id + 1][5:-1]

    # MQTT Test Server:mqtt.m5stack.com, Port:1883.
    def mqtt_server_connect(self, server, port, client_id, username, passwd, keepalive):
        SMCONF_URL = AT_CMD('AT+SMCONF="URL","{0}",{1}'.format(server, port), "OK", 3)  # noqa: N806
        SMCONF_KEEPTIME = AT_CMD('AT+SMCONF="KEEPTIME",{0}'.format(keepalive), "OK", 3)  # noqa: N806
        SMCONF_CLEANSS = AT_CMD('AT+SMCONF="CLEANSS",1', "OK", 3)  # noqa: N806
        SMCONF_CLIENTID = AT_CMD('AT+SMCONF="CLIENTID","{0}"'.format(client_id), "OK", 3)  # noqa: N806
        SMCONF_USERNAME = AT_CMD('AT+SMCONF="USERNAME","{0}"'.format(username), "OK", 3)  # noqa: N806
        SMCONF_PASSWORD = AT_CMD('AT+SMCONF="PASSWORD","{0}"'.format(passwd), "OK", 3)  # noqa: N806
        SMCONN = AT_CMD("AT+SMCONN", "OK", 10)  # noqa: N806

        # mqtt callback function keyword is set
        self.downlink_keyword.append("+SMSUB:")
        self.callback_keyword.append("MQTT_CB")
        self.downlink_callback["MQTT_CB"] = self.mqtt_subscribe_cb

        self.mqtt_subscribe_cb_list = {}

        for pdp_id in range(0, 4):
            if self.get_network_activated(pdp_id):
                break
            else:
                error = self.set_network_active(pdp_id, 1)
                if error is False:
                    return False
                break

        _, error = self.execute_at_command(SMCONF_URL)
        if error:
            return False

        _, error = self.execute_at_command(SMCONF_KEEPTIME)
        if error:
            return False

        _, error = self.execute_at_command(SMCONF_CLEANSS)
        if error:
            return False

        _, error = self.execute_at_command(SMCONF_CLIENTID)
        if error:
            return False

        _, error = self.execute_at_command(SMCONF_USERNAME)
        if error:
            return False

        _, error = self.execute_at_command(SMCONF_PASSWORD)
        if error:
            return False

        _, error = self.execute_at_command(SMCONN)
        if error:
            return False

        result = self.mqtt_server_is_connect()
        return bool(result)

    def mqtt_server_disconnect(self):
        SMDISC = AT_CMD("AT+SMDISC", "OK", 3)  # noqa: N806
        _, error = self.execute_at_command(SMDISC)
        return not error

    def mqtt_subscribe_topic(self, topic, cb, qos=0):
        # Subscribe topic(support wildcards).
        SMSUB = AT_CMD('AT+SMSUB="{0}",{1}'.format(topic, qos), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(SMSUB)
        if error:
            return False
        if topic not in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list[topic] = cb
        return True

    def mqtt_unsubscribe_topic(self, topic):
        # Unsubscribe topic.
        SMUNSUB = AT_CMD('AT+SMUNSUB="{0}"'.format(topic), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(SMUNSUB)
        if error:
            return False
        if topic in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list.pop(topic)
        return True

    def mqtt_publish_topic(self, topic, payload, qos=0, retained=None):
        # Publish message with topic.
        if retained is None:
            SMPUB = AT_CMD('AT+SMPUB="{0}",{1},{2},0'.format(topic, len(payload), qos), ">", 3)  # noqa: N806
        else:
            SMPUB = AT_CMD(  # noqa: N806
                'AT+SMPUB="{0}",{1},{2},{3}'.format(topic, len(payload), qos, retained),
                ">",
                3,
            )

        output, error = self.execute_at_command(SMPUB)
        if error:
            return False

        PAYLOAD = AT_CMD("{0}".format(payload), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(PAYLOAD)
        return not error

    def mqtt_server_is_connect(self):
        # Check mqtt server connection.
        SMSTATE = AT_CMD("AT+SMSTATE?", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(SMSTATE)
        return False if error else int(output[-1])

    def mqtt_polling_loop(self):
        # self.polling_callback()
        DUMMY = AT_CMD("", "", 0)  # noqa: N806
        self.response_at_command(DUMMY)

    def mqtt_subscribe_cb(self, buffer):
        # main callback function
        topic = buffer.split('"')[1]
        payload = buffer.split('"')[3]
        if topic in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list[topic](topic, payload)

    # Create & Request Http(s)
    HTTPCLIENT_GET = 1
    HTTPCLIENT_PUT = 2
    HTTPCLIENT_POST = 3

    def http_request(
        self, method=HTTPCLIENT_GET, url="http://api.m5stack.com/v1", headers={}, data=None
    ):
        # Create HTTP host instance
        proto, dummy, host, path = url.split("/", 3)
        find_url = url.find("/", 10)
        host = url[:find_url]
        CSSLCFG_IGNORE = AT_CMD('AT+CSSLCFG="ignorertctime",1,1', "OK", 3)  # noqa: N806
        CSSLCFG_SSL = AT_CMD('AT+CSSLCFG="sslversion",1,3', "OK", 3)  # noqa: N806
        SHSSL = AT_CMD('AT+SHSSL=1,""', "OK", 3)  # noqa: N806
        SHCONF_URL = AT_CMD('AT+SHCONF="URL","{0}"'.format(host), "OK", 3)  # noqa: N806
        SHCONF_BODYLEN = AT_CMD('AT+SHCONF="BODYLEN",1024', "OK", 3)  # noqa: N806
        SHCONF_HEADERLEN = AT_CMD('AT+SHCONF="HEADERLEN",350', "OK", 3)  # noqa: N806

        self.response_code = 0
        self.data_content = ""

        for pdp_id in range(0, 4):
            if self.get_network_activated(pdp_id):
                break
            else:
                error = self.set_network_active(pdp_id, 1)
                if error is False:
                    return False
                break

        if proto == "https:":
            _, error = self.execute_at_command(CSSLCFG_IGNORE)
            if error:
                return False

            _, error = self.execute_at_command(CSSLCFG_SSL)
            if error:
                return False

            _, error = self.execute_at_command(SHSSL)
            if error:
                return False

        _, error = self.execute_at_command(SHCONF_URL)
        if error:
            return False

        _, error = self.execute_at_command(SHCONF_BODYLEN)
        if error:
            return False

        _, error = self.execute_at_command(SHCONF_HEADERLEN)
        if error:
            return False

        self.http_server_connect()

        if self.is_http_server_connect() == 0:
            return False

        for head in headers.items():
            SHAHEAD = AT_CMD('AT+SHAHEAD="{0}","{1}"'.format(head[0], head[1]), "OK", 3)  # noqa: N806
            _, error = self.execute_at_command(SHAHEAD)
            if error:
                return False

        if method == self.HTTPCLIENT_POST:
            if data is not None:
                SHBOD = AT_CMD("AT+SHBOD={0},10000".format(len(data)), ">", 15)  # noqa: N806
                _, error = self.execute_at_command(SHBOD)
                if error:
                    return False
                DATA = AT_CMD("{0}".format(data), "OK", 3)  # noqa: N806
                _, error = self.execute_at_command(DATA)
                if error:
                    return False

        SHREQ = AT_CMD('AT+SHREQ="{0}",{1}'.format(path, method), "+SHREQ:", 25)  # noqa: N806
        output, error = self.execute_at_command(SHREQ)
        if error:
            return False

        self.response_code = int(output.split(",")[1])
        if self.response_code != 200:
            print('Response code: "{0}"'.format(self.response_code))
            self.http_server_disconnect()
            return False

        length = output.split(",")[2]
        SHREAD = AT_CMD("AT+SHREAD=0,{0}".format(int(length)), "+SHREAD:", 10)  # noqa: N806
        output, error = self.execute_at_command(SHREAD)
        if error:
            return False
        find_out_str = "+SHREAD: {}".format(length)
        find_index = output.find(find_out_str)
        if find_index != -1:
            self.data_content = output[(len(find_out_str) + find_index) :]

        error = self.http_server_disconnect()
        return error

    def http_server_connect(self):
        # Http server is connect
        SHCONN = AT_CMD("AT+SHCONN", "OK", 25)  # noqa: N806
        _, error = self.execute_at_command(SHCONN)
        return not error

    def is_http_server_connect(self):
        # Is check http server connect
        SHSTATE = AT_CMD("AT+SHSTATE?", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(SHSTATE)
        return False if error else int(output[-1])

    def http_server_disconnect(self):
        # http server disconnected
        SHDISC = AT_CMD("AT+SHDISC", "OK", 10)  # noqa: N806
        _, error = self.execute_at_command(SHDISC)
        return not error

    # GNSS
    DD = 1
    DDM = 2
    DMS = 3

    def get_check_gnss_power(self):
        # Check Power Gnss.
        CGNSPWR = AT_CMD("AT+CGNSPWR?", "+CGNSPWR", 5)  # noqa: N806
        output, error = self.execute_at_command(CGNSPWR)
        return False if error else int(output[-1])

    def set_gnss_power_ctrl(self, state):
        # Power Gnss Control State.
        self.time_offset = 8.0
        self.time = "10:00:00"
        self.date = "2000/01/01"
        self.fix_status = "0"
        self.latitude = "0.000000"
        self.longitude = "0.000000"
        self.altitude = "0.0"
        self.satellite_num = "0"
        self.speed = "0.0"
        self.course = "0.0"
        CGNSPWR = AT_CMD("AT+CGNSPWR={0}".format(state), "OK", 5)  # noqa: N806
        _, error = self.execute_at_command(CGNSPWR)
        if error:
            return False

    def set_gnss_work_mode(self, mode):
        # Gnss Work Mode.
        glonass, beidou, galilean, qzss = (
            mode >> 0 & 0x01,
            mode >> 1 & 0x01,
            mode >> 2 & 0x01,
            mode >> 3 & 0x01,
        )
        CGNSMOD = AT_CMD(  # noqa: N806
            "AT+CGNSMOD=1,{0},{1},{2},{3}".format(glonass, beidou, galilean, qzss),
            "OK",
            5,
        )
        _, error = self.execute_at_command(CGNSMOD)
        if error:
            return False

    def gnss_nmea_output_polling(self):
        # Gnss nmea out parameters.
        CGNSINF = AT_CMD("AT+CGNSINF", "+CGNSINF:", 5)  # noqa: N806
        output, error = self.execute_at_command(CGNSINF)
        if error:
            return False
        if output[10] == "1":
            gnss = output.split(",")
            if gnss[1] == "1":
                utc = gnss[2]
                self.date = utc[0:4] + "/" + utc[4:6] + "/" + utc[6:8]
                gnss_hour = int(utc[8:10]) + int(self.time_offset)
                gnss_min = int(utc[10:12]) + int(
                    round((self.time_offset - int(self.time_offset)), 2) * 100
                )

                if gnss_min > 59:
                    gnss_min = gnss_min - 60
                    gnss_hour += 1
                if gnss_min < 0:
                    gnss_min = gnss_min + 60
                    gnss_hour -= 1

                if gnss_hour > 23:
                    gnss_hour = gnss_hour - 24
                if gnss_hour < 0:
                    gnss_hour = gnss_hour + 24
                self.time = (
                    "{:0>2d}".format(gnss_hour)
                    + ":"
                    + "{:0>2d}".format(gnss_min)
                    + ":"
                    + utc[12:14]
                )
                self.latitude = gnss[3]
                self.longitude = gnss[4]
                self.altitude = gnss[5]
                self.satellite_num = gnss[14]
                self.fix_status = gnss[1]
                self.speed = gnss[6]
                self.course = gnss[7]
            else:
                self.fix_status = "0"

    def get_gnss_position(self, unit=0, format=DD):
        dd = 0
        if unit == 0 and self.fix_status == "1":
            if self.latitude != "0N":
                dd = self.latitude
                mag = "N" if float(dd) > 0 else "S"
            else:
                return "0N"
        elif unit == 1 and self.fix_status == "1":
            if self.longitude != "0E":
                dd = self.longitude
                mag = "E" if float(dd) > 0 else "W"
            else:
                return "0E"
        if dd != 0:
            if format == self.DD:
                return dd + mag
            elif format == self.DDM:
                d = int(float(dd))
                m = (float(dd) - d) * 60
                ddm = "{0}.{1}{2}".format(d, m, mag)
                return ddm
            elif format == self.DMS:
                d = int(float(dd))
                m = int((float(dd) - d) * 60)
                s = (float(dd) - d - m / 60) * 3600
                dms = "{0}.{1}.{2}{3}".format(d, m, s, mag)
                return dms

    def set_time_zone(self, hour, min):
        self.time_offset = float("{0}.{1}".format(hour, min))

    def set_gnss_start(self, start="COLD"):
        # GNSS Cold, Warm, Hot Start
        CGNS = AT_CMD("AT+CGNS{0}".format(start), "OK", 5)  # noqa: N806
        output, error = self.execute_at_command(CGNS)
        return not error

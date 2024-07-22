# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


from machine import UART
from collections import namedtuple
from .unit_helper import UnitError
import time
import sys

if sys.platform != "esp32":
    from typing import Literal

AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class MQTTUnit:
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None) -> None:
        self.uart = UART(
            id, tx=port[1], rx=port[0], baudrate=9600, bits=8, parity=None, stop=1, rxbuf=1024
        )
        self.downlink_keyword = ["+MQRECV:", "+NETUNCONNECT", "+MQUNCONNECT", "+MQCONNECT"]
        self._debug = False
        self.mqtt_subscribe_cb_list = {}
        self.network_status = False
        self.mqtt_server_status = False
        while not self.check_modem_is_ready(1):
            time.sleep(0.5)

    def check_modem_is_ready(self, delay=5) -> str:
        # check modem is ready
        AT = AT_CMD("AT", "AT", delay)  # noqa: N806
        output, error = self.execute_at_command(AT)
        return not error

    def get_firmware_version(self) -> str:
        # current firmware version number
        VERSION = AT_CMD("AT+VERSION?", "+VERSION=OK:", 5)  # noqa: N806
        output, error = self.execute_at_command(VERSION)
        return False if error else output

    def get_baudrate(self) -> int:
        # baud rate of the serial port
        BAUD = AT_CMD("AT+BAUD?", "+BAUD=OK:", 5)  # noqa: N806
        output, error = self.execute_at_command(BAUD)
        return False if error else int(output)

    def get_mqtt_status(self) -> int:
        # MQTT connection status
        MQSTATUS = AT_CMD("AT+MQSTATUS?", "+MQSTATUS=OK:", 5)  # noqa: N806
        output, error = self.execute_at_command(MQSTATUS)
        return False if error else int(output)

    def get_network_status(self) -> int:
        # network status 1 or 0
        NETIP = AT_CMD("AT+NETIP?", "+NETIP=OK:", 5)  # noqa: N806
        output, error = self.execute_at_command(NETIP)
        if error:
            return False
        return 0 if output.find("0.0.0.0") != -1 else 1

    def get_network_parameters(self, param=0) -> str:
        # current IP address, subnet mask, gateway, DNS server address
        NETIP = AT_CMD("AT+NETIP?", "+NETIP=OK:", 5)  # noqa: N806
        output, error = self.execute_at_command(NETIP)
        return False if error else output.replace('"', "").split(",")[param]

    def get_mac_address(self) -> str:
        # current MAC address
        NETMAC = AT_CMD("AT+NETMAC?", "+NETMAC=OK:", 5)  # noqa: N806
        output, error = self.execute_at_command(NETMAC)
        return False if error else output.replace('"', "")

    def get_static_ip(self, param=0) -> str:
        # static IP address, subnet mask, gateway
        NETSTATICIP = AT_CMD("AT+NETSTATICIP?", "+NETSTATICIP=OK:", 5)  # noqa: N806
        output, error = self.execute_at_command(NETSTATICIP)
        return False if error else output.replace('"', "").split(",")[param]

    def get_dhcp_status(self) -> int:
        # DHCP enable/disable
        NETDHCPEN = AT_CMD("AT+NETDHCPEN?", "+NETDHCPEN=OK:", 5)  # noqa: N806
        output, error = self.execute_at_command(NETDHCPEN)
        return False if error else int(output)

    def set_baudrate(self, baudrate) -> None:
        # baud rate of the serial port
        BAUD = AT_CMD("AT+BAUD={0}".format(baudrate), "+BAUD=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(BAUD)
        return False if error else self.uart.init(baudrate)

    def set_dhcp_state(self, state=1) -> None:
        # DHCP enable/disable
        NETDHCPEN = AT_CMD("AT+NETDHCPEN={0}".format(state), "+NETDHCPEN=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(NETDHCPEN)
        return not error

    def set_static_ip(self, ip, subnet, gateway) -> None:
        #  network address: ip, subnet, gateway
        NETSTATICIP = AT_CMD(  # noqa: N806
            'AT+NETSTATICIP="{0}","{1}","{2}"'.format(ip, subnet, gateway), "+NETSTATICIP=OK", 5
        )
        output, error = self.execute_at_command(NETSTATICIP)
        return not error

    def set_mqtt_service_start(self) -> None:
        # MQTT Start Command
        MQSTART = AT_CMD("AT+MQSTART", "+MQSTART=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(MQSTART)
        return not error

    def set_mqtt_service_stop(self) -> None:
        # MQTT Stop Command
        MQSTOP = AT_CMD("AT+MQSTOP", "+MQSTOP=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(MQSTOP)
        return not error

    def set_mqtt_server_config(self, host, port, clientId, user, pwd, keepalive):
        # Configure the MQTT Command
        MQCLIENTID = AT_CMD('AT+MQCLIENTID="{}"'.format(clientId), "+MQCLIENTID=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(MQCLIENTID)
        if error:
            return False

        MQSERVER = AT_CMD('AT+MQSERVER="{0}",{1}'.format(host, port), "+MQSERVER=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(MQSERVER)
        if error:
            return False

        MQUSERPWD = AT_CMD('AT+MQUSERPWD="{0}","{1}"'.format(user, pwd), "+MQUSERPWD=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(MQUSERPWD)
        if error:
            return False

        MQKEEP = AT_CMD("AT+MQKEEP={}".format(keepalive), "+MQKEEP=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(MQKEEP)
        return not error

    def set_mqtt_subscribe(self, number, topic, quality, cb):
        # subscribe the MQTT Command
        MQSUBSCRIBE = AT_CMD(  # noqa: N806
            'AT+MQSUBSCRIBE={0},1,"{1}",{2}'.format(number, topic, quality), "+MQSUBSCRIBE=OK", 5
        )
        output, error = self.execute_at_command(MQSUBSCRIBE)
        if error:
            return False

        if topic not in self.mqtt_subscribe_cb_list.keys():
            self.mqtt_subscribe_cb_list[topic] = cb
        return True

    def set_mqtt_publish(self, topic, message, quality):
        # publish the MQTT command
        MQPUBLISH = AT_CMD(  # noqa: N806
            'AT+MQPUBLISH="{0}","{1}",{2}'.format(topic, message, quality), "+MQPUBLISH=OK", 5
        )
        output, error = self.execute_at_command(MQPUBLISH)
        return not error

    def save_current_config(self):
        # save the configure parameter and reset Command
        SAVE = AT_CMD("AT+SAVE", "+SAVE=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(SAVE)
        if error:
            return False

        RESET = AT_CMD("AT+RESET", "+RESET=OK", 5)  # noqa: N806
        output, error = self.execute_at_command(RESET)
        if error:
            return False
        self.mqtt_server_status = False
        while not self.mqtt_server_status:
            self.mqtt_polling_loop()
            time.sleep(0.5)

    #! Create this mpy API like software -> mqtt mpy API
    def set_client(self, client_id, server, port, username, password, keepalive):
        self.set_mqtt_server_config(server, port, client_id, username, password, keepalive)
        self.mqtt_serial_id = 1

    def set_connect(self):
        self.save_current_config()
        self.set_mqtt_service_start()

    def set_disconnect(self):
        self.set_mqtt_service_stop()

    def set_publish(self, topic, message, quality):
        self.set_mqtt_publish(topic, message, quality)

    def set_subscribe(self, topic, cb, quality):
        if self.mqtt_serial_id <= 4:
            self.set_mqtt_subscribe(self.mqtt_serial_id, topic, quality, cb)
            self.mqtt_serial_id += 1
        # else:
        #     assert False, "A server can only subscribe to four topics at a time"

    def check_msg(self):
        self.mqtt_polling_loop()

    def mqtt_polling_loop(self):
        DUMMY = AT_CMD("", "", 0)  # noqa: N806
        self.response_at_command(DUMMY)

    def mqtt_subscribe_cb(self, buffer):
        # internal callback funciton.
        if "+MQRECV:" in buffer:
            topic = buffer.split('"')[1]
            payload = buffer.split('"')[3]
            if topic in self.mqtt_subscribe_cb_list.keys():
                self.mqtt_subscribe_cb_list[topic]((topic, payload))
        elif "+NETUNCONNECT" in buffer:
            self.network_status = False
        elif "+MQUNCONNECT" in buffer:
            self.mqtt_server_status = False
        elif "+MQCONNECT" in buffer:
            self.network_status = True
            self.mqtt_server_status = True

    # ----------------------
    # Execute AT commands
    # ----------------------
    def execute_at_command(self, command: AT_CMD, clean_output=True):
        # Clear the uart buffer
        DUMMY = AT_CMD("", "", 0)  # noqa: N806
        self.response_at_command(DUMMY)

        # Execute the AT command
        command_string_for_at = "{}\r\n".format(command.command)
        if self._debug:
            print('write AT command: "{}"'.format(command.command))
        self.uart.write(command_string_for_at)
        return self.response_at_command(command, clean_output)

    def response_at_command(self, command: AT_CMD, clean_output=True):
        # Support vars
        find_keyword = False
        output = ""
        error = False
        empty_reads = 0
        in_cmd = False
        if command.command != "":
            in_cmd = True

        while True:
            line = self.uart.readline()
            if not line:
                if not in_cmd:
                    break
                time.sleep(1)
                empty_reads += 1
                if empty_reads > command.timeout:
                    print(
                        'Timeout for command "{}", timeout={}'.format(
                            command.command, command.timeout
                        )
                    )
                    error = True
                    break
            else:
                if self._debug:
                    print('response AT command: "{}"'.format(line))
                # Convert line to string
                try:
                    line_str = line.decode("utf-8")
                except:
                    line_str = ""

                for kw in self.downlink_keyword:
                    if kw in line_str:
                        self.mqtt_subscribe_cb(line_str)
                        line_str = ""
                        break

                # Do we have an error?
                if "ERROR:" in line_str:
                    # raise GenericATError('Got generic AT error')
                    print('Got generic AT error for command "{}"'.format(command.command))
                    error = True
                    break

                # If we had a pre-end, do we have the expected end?
                if line_str == "{}\r\n".format(command.response) or line_str.startswith(
                    "{}".format(command.response)
                ):
                    find_keyword = True

                # Save this line unless in particular conditions
                output += line_str

                if find_keyword and self.uart.any() == 0:
                    break

        # ..and remove the last \r\n added by the AT protocol
        if output.endswith("\r\n"):
            output = output[:-2]

        # Also, clean output if needed
        if clean_output:
            output = output.replace("{}".format(command.response), "")
            # output = output.replace("OK", "")
            output = output.replace("\r\n", "")

        # Return
        return (output, error)

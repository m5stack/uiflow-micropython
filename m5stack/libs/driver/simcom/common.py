# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
# References: https://github.com/pythings/Drivers/tree/master
#
# SPDX-License-Identifier: MIT


import time
import json
from collections import namedtuple

AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class Response(object):
    def __init__(self, status_code, content):
        self.status_code = int(status_code)
        self.content = content


class Modem(object):
    def __init__(
        self,
        uart=None,
        MODEM_PWKEY_PIN=None,
        MODEM_RST_PIN=None,
        MODEM_POWER_ON_PIN=None,
        MODEM_TX_PIN=None,
        MODEM_RX_PIN=None,
    ):
        # Uart
        self.uart = uart
        self.modem_debug = False
        self.downlink_callback = {}
        self.downlink_keyword = []
        self.callback_keyword = []

        if not self.uart:
            from machine import UART, Pin

            # Pin initialization
            MODEM_PWKEY_PIN_OBJ = Pin(MODEM_PWKEY_PIN, Pin.OUT) if MODEM_PWKEY_PIN else None  # noqa: N806
            MODEM_RST_PIN_OBJ = Pin(MODEM_RST_PIN, Pin.OUT) if MODEM_RST_PIN else None  # noqa: N806
            MODEM_POWER_ON_PIN_OBJ = (  # noqa: N806
                Pin(MODEM_POWER_ON_PIN, Pin.OUT) if MODEM_POWER_ON_PIN else None
            )

            # Status setup
            if MODEM_PWKEY_PIN_OBJ:
                MODEM_PWKEY_PIN_OBJ.value(0)
            if MODEM_RST_PIN_OBJ:
                MODEM_RST_PIN_OBJ.value(1)
            if MODEM_POWER_ON_PIN_OBJ:
                MODEM_POWER_ON_PIN_OBJ.value(1)

            # Setup UART
            self.uart = UART(1, 115200, timeout=1000, rx=MODEM_TX_PIN, tx=MODEM_RX_PIN)

    def check_modem_is_ready(self):
        # Check if modem is ready for AT command
        AT = AT_CMD("AT", "OK", 10)  # noqa: N806
        output, error = self.execute_at_command(AT, True)
        return not error

    def set_command_echo_mode(self, state=1):
        # Set echo mode off or on
        ATE = AT_CMD("ATE{}".format(state), "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(ATE)
        return not error

    def check_sim_is_connected(self):
        # Check the SIM card is connected or not?
        CPIN = AT_CMD("AT+CPIN?", "+CPIN: READY", 10)  # noqa: N806
        output, error = self.execute_at_command(CPIN)
        return not error

    def get_network_registration_status(self):
        # Get the registration status with the network
        CREG = AT_CMD("AT+CREG?", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CREG)
        if error:
            return False
        return int(output[-3:].split(",")[1])

    def get_signal_strength(self):
        # Get the signal strength
        CSQ = AT_CMD("AT+CSQ", "+CSQ:", 3)  # noqa: N806
        output, error = self.execute_at_command(CSQ)
        if error:
            return False
        return int(output[-5:].split(",")[0])

    def get_gprs_registration_status(self):
        # Get the registration status with the gprs network
        CGREG = AT_CMD("AT+CGREG?", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CGREG)
        if error:
            return False
        return int(output[-3:].split(",")[1])

    def get_model_identification(self):
        # Query the model identification information
        CGMM = AT_CMD("AT+CGMM", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CGMM)
        if error:
            return False
        return output

    def get_gprs_network_status(self):
        # Get attach or detach from the GPRS network
        CGATT = AT_CMD("AT+CGATT?", "OK", 3)  # noqa: N806
        output, error = self.execute_at_command(CGATT)
        if error:
            return False
        return int(output[-1:])

    def set_gprs_network_state(self, enable=1):
        # Set attach or detach from the GPRS network
        CGATT = AT_CMD("AT+CGATT={0}".format(enable), "OK", 75)  # noqa: N806
        output, error = self.execute_at_command(CGATT)
        return not error

    def set_pdp_context(self, apn="CMNET"):
        # Set Define PDP Context
        CGDCONT = AT_CMD('AT+CGDCONT=1,"IP","{}"'.format(apn), "OK", 12)  # noqa: N806
        output, error = self.execute_at_command(CGDCONT)
        return not error

    def get_show_pdp_address(self, cid):
        # Get Show PDP address.
        CGPADDR = AT_CMD("AT+CGPADDR={}".format(cid), "OK", 12)  # noqa: N806
        output, error = self.execute_at_command(CGPADDR)
        if error:
            return False
        return (output.split(",")[1]).replace('"', "")

    def get_selected_operator(self):
        # Get selected operator.
        COPS = AT_CMD("AT+COPS?", "OK", 12)  # noqa: N806
        output, error = self.execute_at_command(COPS)
        if error:
            return False
        if output.find('"') != -1:
            return output.split('"')[1]
        else:
            return ""

    # ----------------------
    # Execute AT commands
    # ----------------------
    def execute_at_command(self, command: AT_CMD, repeat=False, clean_output=True):
        # Clear the uart buffer
        DUMMY = AT_CMD("", "", 0)  # noqa: N806
        self.response_at_command(DUMMY)

        # Execute the AT command
        command_string_for_at = "{}\r\n".format(command.command)
        if self.modem_debug:
            print('write AT command: "{}"'.format(command.command))
        self.uart.write(command_string_for_at)
        return self.response_at_command(command, repeat, clean_output)

    def response_at_command(self, command: AT_CMD, repeat=False, clean_output=True):
        # Support vars
        processed_lines = 0
        pre_end = True
        output = ""
        error = False
        empty_reads = 0
        in_cmd = False
        if command.command != "":
            command_string_for_at = "{}\r\n".format(command.command)
            in_cmd = True

        while True:
            line = self.uart.readline()
            if not line:
                if not in_cmd:
                    break
                time.sleep(1)
                if repeat:
                    self.uart.write(command_string_for_at)
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
                if self.modem_debug:
                    print('response AT command: "{}"'.format(line))
                # Convert line to string
                try:
                    line_str = line.decode("utf-8")
                except:
                    line_str = ""

                for kw in self.downlink_keyword:
                    if kw in line_str:
                        for cb_kw in self.callback_keyword:
                            self.downlink_callback[cb_kw](line_str)
                        break

                # Do we have an error?
                if line_str == "ERROR\r\n":
                    # raise GenericATError('Got generic AT error')
                    print('Got generic AT error for command "{}"'.format(command.command))
                    error = True
                    break

                # If we had a pre-end, do we have the expected end?
                if line_str == "{}\r\n".format(command.response):
                    break
                if pre_end and line_str.startswith("{}".format(command.response)):
                    output += line_str
                    break

                # Do we have a pre-end?
                if line_str == "\r\n" or line_str == "{}\r\r\n".format(command.command):
                    pre_end = True
                else:
                    pre_end = False

                # Keep track of processed lines and stop if exceeded
                processed_lines += 1

                # Save this line unless in particular conditions
                output += line_str

        # Remove the command string from the output
        output = output.replace(command.command + "\r\r\n", "")

        # ..and remove the last \r\n added by the AT protocol
        if output.endswith("\r\n"):
            output = output[:-2]

        # Also, clean output if needed
        if clean_output:
            output = output.replace("OK", "")
            output = output.replace("\r\n", "")
            output = output.replace("\r", "")
            output = output.replace("\n", "")
            if output.startswith("\n"):
                output = output[1:]
            if output.endswith("\n"):
                output = output[:-1]

        # Return
        return (output, error)

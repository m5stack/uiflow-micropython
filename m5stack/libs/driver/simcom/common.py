# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
# References: https://github.com/pythings/Drivers/tree/master
#
# SPDX-License-Identifier: MIT

import sys
import time
from . import utils
from collections import namedtuple

AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])
ATCommand = namedtuple("ATCommand", ["cmd", "rsp1", "rsp2", "timeout"])


class Response(object):
    def __init__(self, status_code, content):
        self.status_code = int(status_code)
        self.content = content


class Modem(object):
    ERR_NONE = 0
    ERR_GENERIC = 1
    ERR_TIMEOUT = 2

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
        # Uart
        self.uart = uart
        self._verbose = verbose
        self.downlink_callback = {}
        self.downlink_keyword = []
        self.callback_keyword = []

        if not self.uart:
            import machine

            # Pin initialization
            pwrkey_obj = machine.Pin(pwrkey_pin, machine.Pin.OUT) if pwrkey_pin else None
            reset_obj = machine.Pin(reset_pin, machine.Pin.OUT) if reset_pin else None
            power_obj = machine.Pin(power_pin, machine.Pin.OUT) if power_pin else None

            # Status setup
            if pwrkey_obj:
                pwrkey_obj(0)
            if reset_obj:
                reset_obj(1)
            if power_obj:
                power_obj(1)

            # Setup UART
            self.uart = machine.UART(1, 115200, timeout=1000, rx=tx_pin, tx=rx_pin, rxbuf=1024)

    def check_modem_is_ready(self):
        # Check if modem is ready for AT command
        at = AT_CMD("AT", "OK", 10)
        output, error = self.execute_at_command(at, True)
        return not error

    def set_command_echo_mode(self, state=1):
        # Set echo mode off or on
        ate = AT_CMD("ATE{}".format(state), "OK", 3)
        output, error = self.execute_at_command(ate)
        return not error

    def check_sim_is_connected(self):
        # Check the SIM card is connected or not?
        cpin = AT_CMD("AT+CPIN?", "+CPIN: READY", 10)
        output, error = self.execute_at_command(cpin)
        return not error

    def get_network_registration_status(self):
        # Get the registration status with the network
        creg = AT_CMD("AT+CREG?", "+CREG:", 3)
        output, error = self.execute_at_command(creg)
        return False if error else int(output[-1])

    def get_signal_strength(self):
        # Get the signal strength
        csq = AT_CMD("AT+CSQ", "+CSQ:", 3)
        output, error = self.execute_at_command(csq)
        return (
            False
            if error
            else int(utils.extract_text(output + "\n", "+CSQ: ", "\n").split(",")[0])
        )

    def get_gprs_registration_status(self):
        # Get the registration status with the gprs network
        cgreg = AT_CMD("AT+CGREG?", "+CGREG:", 3)
        output, error = self.execute_at_command(cgreg)
        return False if error else int(output[-1])

    def get_model_identification(self):
        # Query the model identification information
        cgmm = AT_CMD("AT+CGMM", "SIM", 3)
        output, error = self.execute_at_command(cgmm)
        return False if error else output

    def get_gprs_network_status(self):
        # Get attach or detach from the GPRS network
        cgatt = AT_CMD("AT+CGATT?", "+CGATT:", 3)
        output, error = self.execute_at_command(cgatt)
        return False if error else int(output[-1]) == 1

    def set_gprs_network_state(self, enable=1):
        # Set attach or detach from the GPRS network
        cgatt = AT_CMD("AT+CGATT={0}".format(enable), "OK", 75)
        output, error = self.execute_at_command(cgatt)
        return not error

    def set_pdp_context(self, apn="CMNET"):
        # Set Define PDP Context
        cgdcont = AT_CMD('AT+CGDCONT=1,"IP","{}"'.format(apn), "OK", 12)
        output, error = self.execute_at_command(cgdcont)
        return not error

    def get_show_pdp_address(self, cid):
        # Get Show PDP address.
        cgpaddr = AT_CMD("AT+CGPADDR={}".format(cid), "+CGPADDR:", 12)
        output, error = self.execute_at_command(cgpaddr)
        return False if error else (output.split(",")[1]).replace('"', "")

    def get_selected_operator(self):
        # Get selected operator.
        cops = AT_CMD("AT+COPS?", "+COPS", 12)
        output, error = self.execute_at_command(cops)
        if error:
            return False
        return output.split('"')[1] if output.find('"') != -1 else ""

    def get_keyword_index_in_list(self, list_item, keyword):
        if isinstance(list_item, list):
            list_item = [list_item]
        for index, kw in enumerate(list_item):
            if keyword in kw:
                return (list_item, index, False)
        return (list_item, 0, True)

    # ----------------------
    # Execute AT commands
    # ----------------------
    def execute_at_command(self, command: AT_CMD, repeat=False, clean_output=True):
        # Clear the uart buffer
        dummy = AT_CMD("", "", 0)
        self.response_at_command(dummy)

        # Execute the AT command
        cmdstr = "{}\r\n".format(command.command)
        self._verbose and print("write AT command: {}".format(repr(cmdstr)))
        self.uart.write(cmdstr)
        return self.response_at_command(command, repeat, clean_output)

    def response_at_command(self, command: AT_CMD, repeat=False, clean_output=True):
        # Support vars
        processed_lines = 0
        pre_end = True
        find_keyword = False
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
                self._verbose and print('response AT command: "{}"'.format(line))
                # Convert line to string
                try:
                    line_str = line.decode("utf-8")
                except:
                    line_str = ""

                for kw in self.downlink_keyword:
                    if kw in line_str:
                        for cb_kw in self.callback_keyword:
                            self.downlink_callback[cb_kw](line_str)
                        line_str = ""
                        break

                # Do we have an error?
                if line_str == "ERROR\r\n":
                    # raise GenericATError('Got generic AT error')
                    print('Got generic AT error for command "{}"'.format(command.command))
                    error = True
                    break

                # If we had a pre-end, do we have the expected end?
                if line_str == "{}\r\n".format(command.response):
                    find_keyword = True
                if pre_end and line_str.startswith("{}".format(command.response)):
                    find_keyword = True

                # Do we have a pre-end?
                if line_str == "\r\n" or line_str == "{}\r\r\n".format(command.command):
                    pre_end = True
                else:
                    pre_end = False

                # Keep track of processed lines and stop if exceeded
                processed_lines += 1

                # Save this line unless in particular conditions
                output += line_str

                if find_keyword and self.uart.any() == 0:
                    break

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
            if output.startswith("\n"):
                output = output[1:]
            if output.endswith("\n"):
                output = output[:-1]

        # Return
        return (output, error)

    def execute_at_command2(
        self, cmd: ATCommand, repeat=False, clean_output=True, line_end="\r\n"
    ):
        # clear the uart buffer
        self.uart.write(b"\r\n")

        # execute the AT command
        cmdstr = "{}\r\n".format(cmd.cmd)
        self._verbose and print("TE -> TA:", repr(cmdstr))
        self.uart.write(cmdstr.encode("utf-8"))

        # wait for response
        return self.response_at_command2(cmd, repeat, clean_output, line_end)

    # @utils.measure_time
    def response_at_command2(
        self, command: ATCommand, repeat=False, clean_output=True, line_end="\r\n"
    ):
        # Support vars
        find_keyword = False
        output = bytearray()
        error = self.ERR_NONE
        rsp1 = command.rsp1.encode("utf-8")
        rsp2 = command.rsp2.encode("utf-8")
        line_end = line_end.encode("utf-8")

        ticks = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), ticks) < command.timeout:
            if self.uart.any() == 0:
                time.sleep_ms(10)
                continue

            line = self.uart.read(self.uart.any())
            self._verbose and print("TE <- TA:", repr(line))
            output.extend(line)

            # Do we have an error?
            if output.rfind(rsp2) != -1:
                if output.endswith(line_end):
                    print("Get AT command error response:", repr(output))
                    error = self.ERR_GENERIC
                    find_keyword = True

            # If we had a pre-end, do we have the expected end?
            if output.rfind(rsp1) != -1:
                if output.endswith(line_end):
                    find_keyword = True

            if find_keyword:
                break

        if time.ticks_diff(time.ticks_ms(), ticks) > command.timeout:
            print("Timeout for command:", repr(command.cmd))
            error = self.ERR_TIMEOUT

        # Also, clean output if needed
        # if clean_output:
        #     output = output.replace("OK", "")
        #     output = output.replace("\r\n", "")
        #     output = output.replace("\r", "")
        #     if output.startswith("\n"):
        #         output = output[1:]
        #     if output.endswith("\n"):
        #         output = output[:-1]

        # Return
        return (output, error)

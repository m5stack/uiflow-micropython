# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import network
import machine
import sys
import time
from collections import namedtuple

ATCommand = namedtuple("ATCommand", ["cmd", "rsp1", "rsp2", "timeout"])

if sys.platform != "esp32":
    from typing import Literal


class LTEModule:
    ERR_NONE = 0
    ERR_GENERIC = 1
    ERR_TIMEOUT = 2

    def __init__(self, id: Literal[0, 1, 2], tx: int, rx: int, verbose: bool = False):
        self._uart = machine.UART(
            id,
            baudrate=115200,
            bits=8,
            parity=None,
            stop=1,
            tx=tx,
            rx=rx,
            txbuf=256,
            rxbuf=256,
            timeout=0,
            timeout_char=0,
            invert=0,
            flow=0,
        )
        self._verbose = verbose
        self._ppp = network.PPP(self._uart)

    def execute_at_command2(
        self, cmd: ATCommand, repeat=False, clean_output=True, line_end="\r\n"
    ):
        # clear the uart buffer
        self._uart.write(b"\r\n")

        # execute the AT command
        cmdstr = "{}\r\n".format(cmd.cmd)
        self._uart.write(cmdstr)
        self._verbose and print("TE -> TA:", repr(cmdstr))

        # wait for response
        return self.response_at_command2(cmd, repeat, clean_output, line_end)

    # @utils.measure_time
    def response_at_command2(
        self, command: ATCommand, repeat=False, clean_output=True, line_end="\r\n"
    ):
        find_keyword = False
        output = bytearray()
        error = self.ERR_NONE
        rsp1 = command.rsp1.encode("utf-8")
        rsp2 = command.rsp2.encode("utf-8")
        line_end = line_end.encode("utf-8")

        ticks = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), ticks) < command.timeout:
            if self._uart.any() == 0:
                time.sleep_ms(10)
                continue

            line = self._uart.read(self._uart.any())
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

        return (output, error)

    def chat(self, script: tuple):
        output = bytearray()

        for command, value in script:
            self._verbose and print("chat cmd: {}, value: {}".format(repr(command), repr(value)))

            if command == "ABORT":
                rsp = self._uart.read(len(value))
                if rsp:
                    output.extend(rsp)
                    self._verbose and print("chat response:", repr(rsp))
                    if output.find(value.encode("utf-8")) != -1:
                        break
                continue

            if command == "SAY":
                print(value)
                continue

            if r"\d" in value:
                while True:
                    time.sleep(1)
                    rsp = self._uart.readline()
                    self._verbose and print("chat response:", repr(rsp))
                    if rsp and rsp.find(b"CONNECT") != -1:
                        break
                continue

            while True:
                cmd = ATCommand(value, command, "ERROR", 0 if command == "" else 5000)
                rsp, error = self.execute_at_command2(cmd)
                if command == "":
                    break
                if command != "" and error is self.ERR_NONE:
                    self._verbose and print("chat response:", repr(rsp))
                    rsp = rsp.decode("utf-8")
                    if rsp.find(command) != -1:
                        break

    def chat2(self, pdp_type: str, apn: str):
        self.chat(
            (
                ("ABORT", "BUSY"),
                ("ABORT", "NO ANSWER"),
                ("ABORT", "NO CARRIER"),
                ("ABORT", "NO DIALTONE"),
                ("ABORT", "\nRINGING\r\n\r\nRINGING\r"),
                ("SAY", "modem init: press <ctrl>-C to disconnect\n"),
                ("", "+++ATH"),
                ("SAY", "Before Connecting\n"),
                ("OK", 'AT+CGDCONT=1,"{}","{}"'.format(pdp_type, apn)),
                ("SAY", "\n + defining PDP context\n"),
                ("", "ATD*99#"),
                ("SAY", "Number Dialled\n"),
                ("SAY", "\n + attaching"),
                ("SAY", "\n + requesting data connection"),
                ("CONNECT", r"\d\c"),
                ("SAY", "\n + connected"),
            )
        )

    def __getattr__(self, attr):
        return getattr(self._ppp, attr)

    def deinit(self):
        actived = self._ppp.active()
        self._ppp.active(False)
        self.chat(
            (
                ("DISCONNECTED" if actived else "", "+++ATH" if actived else ""),
                # ("OK", "AT")
            )
        )
        # FIXME: For unknown reasons, if this command is used, UART cannot receive data.
        self._uart.write(b"AT\r\n")
        time.sleep(0.5)
        self._uart.read()
        self._ppp.deinit()

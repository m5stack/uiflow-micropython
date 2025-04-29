# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
from machine import UART


def _measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.ticks_ms()
        result = func(*args, **kwargs)
        end_time = time.ticks_ms()
        execution_time = end_time - start_time  # noqa: F841
        # print(f"total time consumed to execute {func}: {execution_time}ms")
        return result

    return wrapper


class Response:
    ERR_NONE = 0
    ERR_GENERIC = 1
    ERR_TIMEOUT = 2

    def __init__(self, status_code, content):
        self.status_code = int(status_code)
        self.content = content


class Command:
    CMD_TEST = "=?"
    CMD_READ = "?"
    CMD_WRITE = "="
    CMD_EXECUTION = ""

    def __init__(self, cmd, type, *args, rsp1="OK", rsp2="ERROR", timeout=2000) -> None:
        self.cmd = cmd
        self.cmd_type = type
        self.args = []
        for arg in args:
            if isinstance(arg, str):
                self.args.append(f'"{arg}"')
            elif isinstance(arg, int):
                self.args.append(str(arg))

        self.rsp1 = rsp1
        self.rsp2 = rsp2

        self.timeout = timeout

    def __call__(self) -> str:
        t = ["AT", self.cmd, self.cmd_type]
        for arg in self.args:
            t.append(arg)
            t.append(",")
        self.args and t.pop()
        t.append("\r\n")
        return "".join(t)


class UModem:
    def __init__(self, uart: UART, verbose=False):
        self.uart = uart
        self._verbose = verbose

    def execute(self, command: Command, repeat: bool = False, line_end: str = "\r\n") -> Response:
        # clear the uart buffer
        if self.uart.any():
            self.uart.read(self.uart.any())

        # execute the AT command
        self._verbose and print("TE -> TA:", repr(command()))
        self.uart.write(command())

        # wait for response
        return self.response_at_command2(command, repeat, line_end=line_end)

    @_measure_time
    def response_at_command2(
        self, command: Command, repeat: bool = False, clean_output: bool = True, line_end="\r\n"
    ) -> Response:
        # Support vars
        find_keyword = False
        output = bytearray()
        error = Response.ERR_NONE
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
                    error = Response.ERR_GENERIC
                    find_keyword = True

            # If we had a pre-end, do we have the expected end?
            if output.rfind(rsp1) != -1:
                if output.endswith(line_end):
                    find_keyword = True

            if find_keyword:
                break

        if time.ticks_diff(time.ticks_ms(), ticks) > command.timeout:
            print("Timeout for command:", repr(command.cmd))
            error = Response.ERR_TIMEOUT

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
        return Response(error, output)

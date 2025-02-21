# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import UART
from micropython import schedule
import sys

if sys.platform != "esp32":
    from typing import Literal


class ASRUnit:
    """
    note:
        en: ASRUnit is a hardware module designed for voice command recognition. It communicates via UART and supports command parsing, handling, and custom command registration. The module provides functions for receiving, sending messages, and managing commands.

    details:
        link: https://docs.m5stack.com/en/unit/asr
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/asr/asr_01.webp
        category: Unit

    example:
        - ../../../examples/unit/asr/asr_cores3_example.py

    m5f2:
        - unit/asr/asr_cores3_example.m5f2
    """

    DEBUG = True
    myprint = print if DEBUG else lambda *_, **__: None

    _COMMAND_LIST = {
        0x01: ["up", None],
        0x02: ["down", None],
        0x03: ["left", None],
        0x04: ["turn left", None],
        0x05: ["right", None],
        0x06: ["turn right", None],
        0x07: ["forward", None],
        0x08: ["front", None],
        0x09: ["backward", None],
        0x0A: ["back", None],
        0x10: ["open", None],
        0x11: ["close", None],
        0x12: ["start", None],
        0x13: ["stop", None],
        0x14: ["turn on", None],
        0x15: ["turn off", None],
        0x16: ["play", None],
        0x17: ["pause", None],
        0x18: ["turn on the lights", None],
        0x19: ["turn off the lights", None],
        0x1A: ["previous", None],
        0x1B: ["next", None],
        0x20: ["zero", None],
        0x21: ["one", None],
        0x22: ["two", None],
        0x23: ["three", None],
        0x24: ["four", None],
        0x25: ["five", None],
        0x26: ["six", None],
        0x27: ["seven", None],
        0x28: ["eight", None],
        0x29: ["nine", None],
        0x30: ["ok", None],
        0x31: ["hi, A S R", None],
        0x32: ["hello", None],
        0x40: ["increase volume", None],
        0x41: ["decrease volume", None],
        0x42: ["maximum volume", None],
        0x43: ["medium volume", None],
        0x44: ["minimum volume", None],
        0x45: ["check firmware version", None],
        0xFE: ["Announce", None],
        0xFF: ["Hi,M Five", None],
    }

    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None):
        """
        note:
            en: Initialize the ASRUnit object with UART configuration and set up the command handler.

        params:
            id:
                note: The UART port ID for communication, default is 1.
            port:
                note: A list or tuple containing the TX and RX pins for UART communication.
        """
        self.uart = UART(id, tx=port[1], rx=port[0])
        self.uart.init(115200, bits=8, parity=None, stop=1)
        self.uart.irq(handler=self._handler, trigger=UART.IRQ_RXIDLE)
        self.raw_message = ""
        self.command_num = 0
        self.is_recieved = False

    def _handler(self, uart) -> None:
        """
        note:
            en: UART interrupt handler to process incoming data and parse the command number.

        params:
            uart:
                note: The UART object receiving the data.
        """
        data = uart.readline()
        if data is not None and len(data) >= 5:  # 至少包含帧头、命令、帧尾
            self.myprint(("Received data: ", data))

            # 校验帧头和帧尾
            if data[0] == 0xAA and data[1] == 0x55 and data[-2] == 0x55 and data[-1] == 0xAA:
                self.is_recieved = True
                self.raw_message = " ".join(f"0x{byte:02X}" for byte in data)
                self.myprint(("Parsed message:", self.raw_message.split()))

                self.command_num = data[2]
                self.check_tick_callback()
            else:
                self.myprint("Invalid frame received: header/footer mismatch")
                uart.read()

    def get_received_status(self) -> bool:
        """
        note:
            en: Get the status of the received message.

        params:
            note:

        returns:
            note: True if a message is received, False otherwise.
        """
        status = self.is_recieved
        self.is_recieved = False
        return status

    def send_message(
        self,
        command_num: int,
    ) -> None:
        """
        note:
            en: Send a message with a specified command number via UART.

        params:
            command_num:
                note: The command number to send in the message.
        """
        message: list[int] = [0xAA, 0x55, command_num, 0x55, 0xAA]
        buf = bytes(message)
        self.myprint(buf)
        self.uart.write(buf)

    def get_current_raw_message(self) -> str:
        """
        note:
            en: Get the raw message received in hexadecimal format.

        params:
            note:

        returns:
            note: The raw message as a string in hexadecimal format.
        """
        return self.raw_message

    def get_current_command_word(self) -> str:
        """
        note:
            en: Get the command word corresponding to the current command number.

        params:
            note:

        returns:
            note: The command word as a string.
        """
        return self._COMMAND_LIST.get(self.command_num, ["Unknown command word", None])[0]

    def get_current_command_num(self) -> str:
        """
        note:
            en: Get the current command number.

        params:
            note:

        returns:
            note: The command number.
        """
        return "0x{:X}".format(self.command_num)

    def get_command_handler(self) -> bool:
        """
        note:
            en: Check if the current command has an associated handler.

        params:
            note:

        returns:
            note: True if a handler exists for the current command, False otherwise.
        """
        return self._COMMAND_LIST.get(self.command_num, ["", None])[1] is not None

    def add_command_word(
        self,
        command_num: int,
        command_word: str,
        event_handler=None,
    ) -> None:
        """
        note:
            en: Add a new command word and its handler to the command list.

        params:
            command_num:
                note: The command number (must be between 0 and 255).
            command_word:
                note: The command word to associate with the command number.
            event_handler:
                note: An optional event handler function to be called for the command.
        """
        if not (0 <= command_num <= 255):
            raise ValueError("Command number must be between 0 and 255")
        self._COMMAND_LIST[command_num] = [command_word, event_handler]

    def remove_command_word(self, command_word: str) -> None:
        """
        note:
            en: Remove a command word from the command list by its word.

        params:
            command_word:
                note: The command word to remove.
        """
        command_num = self.search_command_num(command_word)
        if command_num != -1:
            self._COMMAND_LIST.pop(command_num)
        else:
            raise ValueError("Command word not found")

    def search_command_num(self, command_word: str) -> int:
        """
        note:
            en: Search for the command number associated with a command word.

        params:
            command_word:
                note: The command word to search for.

        returns:
            note: The command number if found, otherwise -1.
        """
        for key, value in self._COMMAND_LIST.items():
            if value[0] == command_word:
                return key
        return -1

    def search_command_word(self, command_num: int) -> str:
        """
        note:
            en: Search for the command word associated with a command number.

        params:
            command_num:
                note: The command number to search for.

        returns:
            note: The command word if found, otherwise "Unknown command word".
        """
        return self._COMMAND_LIST.get(command_num, ["Unknown command word", None])[0]

    def get_command_list(self) -> dict:
        """
        note:
            en: Get the list of all commands and their associated handlers.

        params:
            note:

        returns:
            note: A dictionary of command numbers and their corresponding command words and handlers.
        """
        return self._COMMAND_LIST

    def check_tick_callback(self):
        """
        note:
            en: Check if a handler is defined for the current command and schedule its execution.

        params:
            note:
        """
        handler = self._COMMAND_LIST.get(self.command_num, ["", None])[1]
        self.myprint(("handler: ", handler))
        if handler is not None:
            schedule(handler, self)

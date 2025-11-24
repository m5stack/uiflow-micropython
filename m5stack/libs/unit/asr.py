# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import UART
from micropython import schedule
import sys

if sys.platform != "esp32":
    from typing import Literal


class ASRUnit:
    """Voice recognition hardware module.

    :param int id: UART port ID for communication. Default is 1.
    :param list|tuple port: Tuple containing TX and RX pin numbers.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import ASRUnit

            # Initialize with UART1, TX on pin 2, RX on pin 1
            asr = ASRUnit(id=1, port=(1, 2))
    """

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
        0x50: ["PA2 high level", None],
        0x51: ["PA2 low level", None],
        0x52: ["PA3 high level", None],
        0x53: ["PA3 low level", None],
        0x54: ["PA4 high level", None],
        0x55: ["PA4 low level", None],
        0x56: ["PA5 high level", None],
        0x57: ["PA5 low level", None],
        0x58: ["PC4 high level", None],
        0x59: ["PC4 low level", None],
        0x5A: ["inversion level", None],
        0xFE: ["Announce", None],
        0xFF: ["Hi,M Five", None],
    }

    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None, verbose: bool = False):
        self.uart = UART(id, tx=port[1], rx=port[0])
        self.uart.init(115200, bits=8, parity=None, stop=1)
        self.uart.irq(handler=self._handler, trigger=UART.IRQ_RXIDLE)
        self.raw_message = ""
        self.command_num = 0
        self.is_recieved = False
        self.verbose = verbose

    def _debug_print(self, *args, **kwargs):
        """Print debug information if verbose mode is enabled."""
        if self.verbose:
            print(*args, **kwargs)

    def _handler(self, uart) -> None:
        if uart.any() < 5:
            return

        data = uart.read()
        if data is None or len(data) < 5:
            return

        self._debug_print(("Received data: ", data))

        # 检查5字节格式: AA 55 CMD 55 AA
        if (
            len(data) >= 5
            and data[0] == 0xAA
            and data[1] == 0x55
            and data[3] == 0x55
            and data[4] == 0xAA
        ):
            self.is_recieved = True
            self.command_num = data[2]
            self.msg = 0  # 5字节格式没有msg字段
            self.raw_message = " ".join(f"0x{byte:02X}" for byte in data[:5])
            self._debug_print(("Parsed 5-byte message:", self.raw_message))
            self.check_tick_callback()

        # 检查6字节格式: AA 55 CMD MSG 55 AA
        elif (
            len(data) >= 6
            and data[0] == 0xAA
            and data[1] == 0x55
            and data[4] == 0x55
            and data[5] == 0xAA
        ):
            self.is_recieved = True
            self.command_num = data[2]
            self.msg = data[3]  # 6字节格式包含msg字段
            self.raw_message = " ".join(f"0x{byte:02X}" for byte in data[:6])
            self._debug_print(("Parsed 6-byte message:", self.raw_message))
            self.check_tick_callback()

        else:
            self._debug_print("Invalid frame received: header/footer mismatch")
            uart.read()

    def get_received_status(self) -> bool:
        """Get message reception status.

        :returns: True if a message is received, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |get_received_status.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.get_received_status()
        """
        status = self.is_recieved
        self.is_recieved = False
        return status

    def send_message(
        self,
        command_num: int,
    ) -> None:
        """Send command via UART.

        :param int command_num: Command number to send (0-255)

        UiFlow2 Code Block:

            |send_message.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.send_message(0x30)
        """
        message: list[int] = [0xAA, 0x55, command_num, 0x55, 0xAA]
        buf = bytes(message)
        self._debug_print(buf)
        self.uart.write(buf)

    def get_current_raw_message(self) -> str:
        """Get the raw message received in hexadecimal format.

        :returns: The raw message as a string in hexadecimal format.
        :rtype: str

        UiFlow2 Code Block:

            |get_current_raw_message.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.get_current_raw_message()
        """
        return self.raw_message

    def get_current_command_word(self) -> str:
        """Get the command word corresponding to the current command number.

        :returns: The command word as a string.
        :rtype: str

        UiFlow2 Code Block:

            |get_current_command_word.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.get_current_command_word()
        """
        return self._COMMAND_LIST.get(self.command_num, ["Unknown command word", None])[0]

    def get_current_command_num(self) -> str:
        """Get the current command number.

        :returns: The current command number as a string.
        :rtype: str

        UiFlow2 Code Block:

            |get_current_command_num.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.get_current_command_num()
        """
        return "0x{:X}".format(self.command_num)

    def get_command_handler(self) -> bool:
        """Check if the current command has an associated handler.

        :returns: True if the command has an associated handler, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |get_command_handler.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.get_command_handler()
        """
        return self._COMMAND_LIST.get(self.command_num, ["", None])[1] is not None

    def add_command_word(
        self,
        command_num: int,
        command_word: str,
        event_handler=None,
    ) -> None:
        """Register custom command and handler.

        :param int command_num: Command number (0-255)
        :param str command_word: Voice command text
        :param callable event_handler: Handler function

        UiFlow2 Code Block:

            |add_command_word.png|

        MicroPython Code Block:

            .. code-block:: python

                def custom_handler(unit):
                    print("Custom command detected!")

                asr.add_command_word(0x50, "custom command", custom_handler)
        """
        if not (0 <= command_num <= 255):
            raise ValueError("Command number must be between 0 and 255")
        self._COMMAND_LIST[command_num] = [command_word, event_handler]

    def remove_command_word(self, command_word: str) -> None:
        """Remove a command word from the command list by its word.

        :param str command_word: Command word to remove

        UiFlow2 Code Block:

            |remove_command_word.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.remove_command_word("custom command")
        """
        command_num = self.search_command_num(command_word)
        if command_num != -1:
            self._COMMAND_LIST.pop(command_num)
        else:
            raise ValueError("Command word not found")

    def search_command_num(self, command_word: str) -> int:
        """Search for the command number associated with a command word.

        :param str command_word: Command word to search for
        :returns: The command number if found, otherwise -1
        :rtype: int

        UiFlow2 Code Block:

            |search_command_num.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.search_command_num("custom command")
        """
        for key, value in self._COMMAND_LIST.items():
            if value[0] == command_word:
                return key
        return -1

    def search_command_word(self, command_num: int) -> str:
        """Search for the command word associated with a command number.

        :param int command_num: Command number to search for
        :returns: The command word if found, otherwise "Unknown command word"
        :rtype: str

        UiFlow2 Code Block:

            |search_command_word.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.search_command_word(0x50)
        """
        return self._COMMAND_LIST.get(command_num, ["Unknown command word", None])[0]

    def get_command_list(self) -> dict:
        """Get the list of all commands and their associated handlers.

        :returns: A dictionary of command numbers and their corresponding command words and handlers.
        :rtype: dict

        UiFlow2 Code Block:

            |get_command_list.png|

        MicroPython Code Block:

            .. code-block:: python

                asr.get_command_list()
        """
        return self._COMMAND_LIST

    def check_tick_callback(self):
        """Check if a handler is defined for the current command and schedule its execution.

        :returns: The handler if defined, otherwise None
        :rtype: None

        MicroPython Code Block:

            .. code-block:: python

                asr.check_tick_callback()
        """
        handler = self._COMMAND_LIST.get(self.command_num, ["", None])[1]
        self._debug_print(("handler: ", handler))
        if handler is not None:
            schedule(handler, self)

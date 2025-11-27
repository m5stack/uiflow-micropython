# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from driver.simcom.ml307r import ML307R
from driver.simcom.common import Modem
from collections import namedtuple
from .unit_helper import UnitError
import sys

if sys.platform != "esp32":
    from typing import Literal

AT_CMD = namedtuple("AT_CMD", ["command", "response", "timeout"])


class Cat1Unit(ML307R, Modem):
    def __init__(
        self,
        uart_or_id: machine.UART | int,
        port: list | tuple = None,
        verbose: bool = False,
    ) -> None:
        if isinstance(uart_or_id, machine.UART):
            self.uart = uart_or_id
        elif isinstance(uart_or_id, int) and port is not None:
            self.uart = machine.UART(
                uart_or_id,
                tx=port[1],
                rx=port[0],
                baudrate=115200,
                bits=8,
                parity=None,
                stop=1,
                rxbuf=1024,
            )
        else:
            raise ValueError("Invalid arguments: must provide either UART or (id + port)")

        Modem.__init__(self, uart=self.uart, verbose=verbose)

        if not self.check_modem_is_ready():
            raise UnitError("NBIOT unit not found in Grove")
        self.set_command_echo_mode(0)

        ML307R.__init__(self, uart=self.uart, verbose=verbose)


# from unit import Cat1Unit
# cat1 = Cat1Unit(2, port=(33, 32), verbose=True)
# cat1.mqtt_server_connect("broker-cn.emqx.io", 1883, "mqttx_ad4bc4fa", "", "", 120)
# socket = cat1.socket()
# socket.connect(("8.135.10.183", 33864))
# socket.sendto(b"Hello, World!", ("8.135.10.183", 33864))
# socket.send(b"Hello, World!")
# socket.close()
# cat1.getaddrinfo("www.m5stack.com", 80)
# cat1.http_request(
#     1,
#     "http://httpbin.org/post",
#     {"Content-Type": "application/json", "Custom-Header": "MyHeaderValue"},
#     {"message": "Hello from M5Stack! ", "status": "active"},
# )
# cat1.mqtt_publish_topic("Subscription", "asdfas", 0)

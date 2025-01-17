# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine


class RS485Unit:
    def __new__(cls, id, **kwargs):
        port = kwargs.pop("port", None)
        if port is not None:
            tx = port[1]
            rx = port[0]
            kwargs["tx"] = tx
            kwargs["rx"] = rx
        instance = super().__new__(cls)
        instance.uart = machine.UART(id, **kwargs)
        instance.tx = tx
        instance.rx = rx
        return instance

    def __getattr__(self, name):
        return getattr(self.uart, name)

    def __setattr__(self, name, value):
        if name in ["tx", "rx", "uart"]:
            super().__setattr__(name, value)
        else:
            setattr(self.uart, name, value)

    def init(
        self,
        tx_pin=None,
        rx_pin=None,
        baudrate=9600,
        data_bits=None,
        stop_bits=None,
        parity=None,
        **kwargs,
    ):
        tx = tx_pin if tx_pin is not None else self.tx
        rx = rx_pin if rx_pin is not None else self.rx
        if data_bits is None and stop_bits is None:
            data_bits, stop_bits = 8, 1

        kwargs.pop("ctrl_pin", None)
        init_kwargs = {
            "baudrate": baudrate,
            "bits": data_bits,
            "parity": parity,
            "stop": stop_bits,
            "tx": tx,
            "rx": rx,
        }
        init_kwargs.update(kwargs)
        self.uart.init(**init_kwargs)


# uart1 = RS485(1, baudrate=115200, bits=8, parity=None, stop=1, tx=0, rx=35)

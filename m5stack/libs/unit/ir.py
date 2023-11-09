from driver.ir.nec import NEC, NEC_8
from machine import Pin


class IRUnit:
    # def __new__(cls, port, proto):
    #     if proto.upper() == "NEC":
    #         return NEC(Pin(port[1], Pin.IN))

    def __init__(self, port) -> None:
        self._port = port
        self._transmitter = NEC(Pin(self._port[1], Pin.OUT, value=0))
        self._receiver = None

    def tx(self, cmd, data):
        self._transmitter.transmit(cmd, data)

    def rx_cb(self, cb):
        if self._receiver is None:
            self._receiver = NEC_8(Pin(self._port[0], Pin.IN), cb)
        else:
            self._receiver.close()

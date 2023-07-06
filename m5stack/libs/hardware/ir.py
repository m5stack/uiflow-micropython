from driver.ir.nec import NEC, NEC_8
import M5
from machine import Pin

_pin_map = {
    M5.BOARD.M5AtomS3: (None, 4),
    M5.BOARD.M5AtomS3Lite: (None, 4),
    M5.BOARD.M5AtomS3U: (None, 12),
}


class IR:
    def __init__(self) -> None:
        self._port = _pin_map.get(M5.getBoard())
        self._transmitter = NEC(Pin(self._port[1], Pin.OUT, value=0))
        self._receiver = None

    def tx(self, cmd, data):
        self._transmitter.transmit(cmd, data)

    def rx_cb(self, cb):
        if self._port[0] is None:
            return

        if self._receiver is None:
            self._receiver = NEC_8(Pin(self._port[0], Pin.IN), cb)
        else:
            self._receiver.close()

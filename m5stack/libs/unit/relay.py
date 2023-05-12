from machine import Pin


class Relay:
    def __init__(self, port: tuple) -> None:
        self._pin = Pin(port[1])
        self._pin.init(mode=self._pin.OUT)

    def on(self):
        self._pin(1)

    def off(self):
        self._pin(0)

from machine import Pin


class Relay:
    def __init__(self, port: tuple) -> None:
        self._pin = Pin(port[1])
        self._pin.init(mode=self._pin.OUT)

    def on(self) -> None:
        self._pin(1)

    def off(self) -> None:
        self._pin(0)

    def value(self, x: bool) -> None:
        self._pin(int(x))

    def set_status(self, x: bool) -> None:
        self._pin(int(x))

    def get_status(self) -> bool:
        return bool(self._pin())

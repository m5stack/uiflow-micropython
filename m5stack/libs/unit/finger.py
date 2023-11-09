from driver.fpc1020a.fpc1020a import FPC1020A
from machine import UART


class FingerUnit(FPC1020A):
    def __init__(self, port):
        uart1 = UART(1)
        uart1.init(19200, tx=port[1], rx=port[0])
        super().__init__(uart1)

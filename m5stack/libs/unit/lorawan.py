from driver.asr650x import LoRaWAN_470
import machine


class LoRaWANUnit(LoRaWAN_470):
    def __init__(self, port):
        super(LoRaWAN, self).__init__(tx=port[1], rx=port[0])
        self.tx = port[1]
        self.rx = port[0]

    def uart_port_id(self, id_num):
        """
        set core device uart id
        id_num: 1-2
        """
        self.__uart = machine.UART(id_num, tx=self.tx, rx=self.rx)
        self.__uart.init(115200, bits=0, parity=None, stop=1)

    def deinit(self):
        pass

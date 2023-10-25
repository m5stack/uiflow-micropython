from driver.modbus.master.uSerial import uSerial


class RS485(uSerial):
    def __init__(self, port, debug=False):
        self._port = port
        self._debug = debug

    def init(
        self,
        uart,
        tx_pin=17,
        rx_pin=18,
        baudrate=9600,
        data_bits=8,
        stop_bits=1,
        parity=None,
        ctrl_pin=None,
    ):
        if tx_pin != None and rx_pin != None:
            self._port = (rx_pin, tx_pin)
        if data_bits == None and stop_bits == None:
            data_bits = 8
            stop_bits = 1
        super().__init__(
            uart,
            tx=self._port[1],
            rx=self._port[0],
            baudrate=baudrate,
            data_bits=data_bits,
            parity=parity,
            stop_bits=stop_bits,
            ctrl_pin=ctrl_pin,
            debug=self._debug,
        )

    def write(self, payload):
        self._mdbus_uart.write(payload)

    def read(self, byte=None):
        if byte is not None:
            return self._mdbus_uart.read(byte)
        else:
            return self._mdbus_uart.read()

    def readline(self):
        return self._mdbus_uart.readline()

    def any(self):
        return self._mdbus_uart.any()

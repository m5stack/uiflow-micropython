from machine import Pin, ADC


class AngleUnit:
    def __init__(self, port):
        self._adc = ADC(Pin(port[0]), atten=ADC.ATTN_11DB)

    def get_voltage(self) -> float:
        return self._adc.read_uv() / 1000 / 1000

    def get_value(self) -> int:
        return self._adc.read_u16()

try:
    from machine import Pin, ADC
except ImportError:
    pass

class Angle:

    def __init__(self, io):
        self._adc = ADC(Pin(io), atten=ADC.ATTN_11DB)

    def get_voltage(self) -> float:
        return self._adc.read_uv() / 1000 / 1000

    def get_value(self) -> int:
        return self._adc.read_u16()

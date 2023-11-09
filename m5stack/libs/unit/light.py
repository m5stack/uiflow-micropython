from machine import Pin, ADC


class LightUnit:
    def __init__(self, port: tuple) -> None:
        self._ain = ADC(Pin(port[0]), atten=ADC.ATTN_11DB)
        self._din = Pin(port[1], mode=Pin.IN)

    def get_digital_value(self):
        return self._din()

    def get_analog_value(self):
        return self._ain.read_u16()

    def get_ohm(self):
        light_v = self._ain.read_uv() / 1000 / 1000
        return int(light_v * 10000 / (3.3 - light_v))

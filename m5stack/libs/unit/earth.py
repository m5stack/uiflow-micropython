try:
    from machine import Pin, ADC
except ImportError:
    pass

class Earth:
    def __init__(self, aim, dim) -> None:
        self._aim = ADC(Pin(aim), atten=ADC.ATTN_11DB)
        self._dim = Pin(dim, mode=Pin.IN)
        self._min = 2900
        self._max = 1630

    def set_calibrate(self, min_val, max_val) -> None:
        '''
        - ``min_val`` is the voltage value at which the probe just touches the water surface.
        - ``max_val`` is the voltage value at which the probe is fully immersed.
        '''
        self._min = min_val
        self._max = max_val

    def humidity(self) -> float:
        '''warn!
        Humidity is not distributed linearly from 0% to 100%.
        '''
        val = self.get_voltage_mv()
        if self._min > self._max:
            if val > self._min:
                return 0.0
            elif val < self._max:
                return 1.0
        else:
            if val < self._min:
                return 0.0
            elif val > self._max:
                return 1.0
        return abs(val - self._min) / abs(self._max - self._min)

    def get_analog_value(self):
        return self._aim.read_u16()

    def get_voltage_mv(self) -> int:
        return int(self._aim.read_uv() / 1000)

    def get_digital_value(self):
        return self._dim()

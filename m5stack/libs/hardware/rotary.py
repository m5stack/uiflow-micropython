from driver.rotary.rotary_irq_esp import RotaryIRQ


class Rotary(RotaryIRQ):
    def __init__(self, min_val=0, max_val=10) -> None:
        # M5Dial’s unique features
        super().__init__(
            pin_num_clk=41,
            pin_num_dt=40,
            min_val=min_val,
            max_val=max_val,
            reverse=False,
            range_mode=RotaryIRQ.RANGE_UNBOUNDED,
        )
        self._last_value = self.value()

    def get_rotary_status(self):
        val = self.value()
        if val != self._last_value:
            return True
        return False

    def get_rotary_value(self):
        self._last_value = self.value()
        return self.value()

    def reset_rotary_vlaue(self):
        self._last_value = 0
        super().reset()

    def set_rotary_vlaue(self, val):
        self._last_value = val
        super().set(val)

    def get_rotary_increments(self):
        tmp = self._last_value
        return self.get_rotary_value() - tmp

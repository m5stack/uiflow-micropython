from driver.button import Button as ButtonBase
from machine import Pin


class CB_TYPE:
    WAS_CLICKED = 0
    WAS_DOUBLECLICKED = 1
    WAS_HOLD = 2
    WAS_PRESSED = 3
    WAS_RELEASED = 4


class Button(ButtonBase):
    WAS_CLICKED = 0
    WAS_DOUBLECLICKED = 1
    WAS_HOLD = 2
    WAS_PRESSED = 3
    WAS_RELEASED = 4

    def __init__(self, pin_num, active_low=True, pullup_active=True) -> None:
        super().__init__(Pin(pin_num), active_low, pullup_active)
        self.CB_TYPE = CB_TYPE()

    def isHolding(self):
        return self.last_state == self.current_state and self.last_state == self.HOLD

    def isPressed(self):
        return self.last_state == self.current_state and self.last_state == self.PRESSED

    def isReleased(self):
        return self.last_state == self.current_state and self.last_state == self.RELEASED

    def isClicked(self):
        return self.last_state == self.current_state and self.last_state == self.CLICKED

    def wasHold(self):
        return self.last_state == self.HOLD

    def wasPressed(self):
        return self.last_state == self.PRESSED

    def wasReleased(self):
        return self.last_state == self.RELEASED

    def wasClicked(self):
        return self.last_state == self.CLICKED

    def wasSingleClicked(self):
        return self.last_state == self.CLICKED

    def wasDoubleClicked(self):
        return self.last_state == self.DOUBLE_CLICKED

    def setCallback(self, type=None, cb=None):
        if type == 0:
            self.attach_click_event(cb, parameter=self.WAS_CLICKED)
        elif type == 1:
            self.attach_double_click(cb, parameter=self.WAS_DOUBLECLICKED)
        elif type == 2:
            self.attach_during_long_press(cb, parameter=self.WAS_HOLD)
        elif type == 3:
            self.attach_long_press_start(cb, parameter=self.WAS_PRESSED)
        elif type == 4:
            self.attach_long_press_stop(cb, parameter=self.WAS_RELEASED)

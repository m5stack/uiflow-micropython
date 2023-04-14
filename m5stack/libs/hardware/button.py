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
        return super().last_state == super().current_state and super().last_state == super().HOLD

    def isPressed(self):
        return super().last_state == super().current_state and super().last_state == super().PRESSED

    def isReleased(self):
        return super().last_state == super().current_state and super().last_state == super().RELEASED

    def wasHold(self):
        return super().last_state == super().HOLD

    def wasPressed(self):
        return super().last_state == super().PRESSED

    def wasReleased(self):
        return super().last_state == super().RELEASED

    def wasClicked(self):
        return super().last_state == super().CLICKED

    def wasSingleClicked(self):
        return super().last_state == super().CLICKED

    def wasDoubleClicked(self):
        return super().last_state == super().DOUBLE_CLICKED

    def setCallback(self, type=None, cb=None):
        if type == 0:
            super().attach_click_event(cb, parameter=self.WAS_CLICKED)
        elif type == 1:
            super().attach_double_click(cb, parameter=self.WAS_DOUBLECLICKED)
        elif type == 2:
            super().attach_during_long_press(cb, parameter=self.WAS_HOLD)
        elif type == 3:
            super().attach_long_press_start(cb, parameter=self.WAS_PRESSED)
        elif type == 4:
            super().attach_long_press_stop(cb, parameter=self.WAS_RELEASED)

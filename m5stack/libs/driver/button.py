from micropython import const, schedule
import time

OCS_INIT = const(0)
OCS_DOWN = const(1)
OCS_UP = const(2)
OCS_COUNT = const(3)
OCS_PRESS = const(6)
OCS_PRESSEND = const(7)
UNKNOWN = const(99)

VERBOSE = False


class Button:

    NO_ACTIVE = 0
    HOLD = 1
    PRESSED = 2
    RELEASED = 3
    CLICKED = 4
    DOUBLE_CLICKED = 5

    def __init__(self, pin, activeLow=True, pullupActive=True) -> None:
        self._pin = pin
        if pullupActive:
            self._pin.init(mode=self._pin.IN, pull=self._pin.PULL_UP)
        else:
            self._pin.init(mode=self._pin.IN)
        # self._pin.irq(
        #     self._irq,
        #     trigger=self._pin.IRQ_FALLING | self._pin.IRQ_RISING
        # )
        self._debounce_ticks = 50
        self._click_ticks = 400
        self._press_ticks = 800
        self._buttonPressed = 0 if activeLow else 1
        self._start_time = 0
        self._state = OCS_INIT
        self._last_state = OCS_INIT
        self._n_clicks = 0
        self._max_clicks = 0
        self.current_state = self.NO_ACTIVE
        self.last_state = self.NO_ACTIVE

        self._click_handler = None
        self._click_param = None

        self._double_click_handler = None
        self._double_click_param = None

        self._multi_click_handler = None
        self._multi_click_param = None

        self._long_press_start_handler = None
        self._long_press_start_param = None

        self._long_press_stop_handler = None
        self._long_press_stop_param = None

        self._during_long_press_handler = None
        self._during_long_press_param = None

    def set_debounce_ticks(self, ticks):
        self._debounce_ticks = ticks

    def set_click_ticks(self, ticks):
        self._click_ticks = ticks

    def set_press_ticks(self, ticks):
        self._press_ticks = ticks

    def attach_click_event(self, handler, parameter=None):
        self._click_handler = handler
        self._click_param = parameter

    def attach_double_click(self, handler, parameter=None):
        self._double_click_handler = handler
        self._double_click_param = parameter

    def attach_multi_click(self, handler, parameter=None):
        self._multi_click_handler = handler
        self._multi_click_param = parameter

    def attach_long_press_start(self, handler, parameter=None):
        self._long_press_start_handler = handler
        self._long_press_start_param = parameter

    def attach_long_press_stop(self, handler, parameter=None):
        self._long_press_stop_handler = handler
        self._long_press_stop_param = parameter

    def attach_during_long_press(self, handler, parameter=None):
        self._during_long_press_handler = handler
        self._during_long_press_param = parameter

    def _irq(self, pin):
        schedule(self.tick, pin)

    def tick(self, pin):
        level = self._pin() == self._buttonPressed
        now = time.ticks_ms()
        wait_time = now - self._start_time

        if self._state == OCS_INIT:
            if level:
                VERBOSE and print("OCS_INIT")
                self._new_state(OCS_DOWN)
                self._start_time = now
                self._n_clicks = 0
        elif self._state == OCS_DOWN:
            VERBOSE and print("OCS_DOWN")
            if (not level) and (wait_time < self._debounce_ticks):
                VERBOSE and print("released1")
                self._new_state(self._last_state)
            elif not level:
                VERBOSE and print("released2")
                self._new_state(OCS_UP)
                self._start_time = now
            elif level and wait_time > self._press_ticks:
                if self._long_press_start_handler is not None:
                    if self._long_press_start_param is None:
                        self._long_press_start_handler()
                    else:
                        self._long_press_start_handler(self._long_press_start_param)
                self._new_state(OCS_PRESS)
                self._update_state(self.PRESSED)
        elif self._state == OCS_UP:
            VERBOSE and print("OCS_UP")
            if level and wait_time < self._debounce_ticks:
                self._new_state(self._last_state)
                self._update_state(self.last_state)
            elif wait_time >= self._debounce_ticks:
                self._n_clicks += 1
                self._new_state(OCS_COUNT)
        elif self._state == OCS_COUNT:
            VERBOSE and print("OCS_COUNT")
            if level:
                self._new_state(OCS_DOWN)
                self._update_state(self.PRESSED)
                self._start_time = now
            elif wait_time > self._click_ticks or self._n_clicks == self._max_clicks:
                if self._n_clicks == 1:
                    self._update_state(self.CLICKED)
                    VERBOSE and print("click")
                    if self._click_handler is not None:
                        if self._click_param is None:
                            self._click_handler()
                        else:
                            self._click_handler(self._click_param)
                elif self._n_clicks == 2:
                    self._update_state(self.DOUBLE_CLICKED)
                    if self._double_click_handler is not None:
                        if self._double_click_param is None:
                            self._double_click_handler()
                        else:
                            self._double_click_handler(self._double_click_param)
                else:
                    if self._multi_click_handler is not None:
                        if self._multi_click_param is None:
                            self._multi_click_handler()
                        else:
                            self._multi_click_handler(self._multi_click_param)
                self.reset()
        elif self._state == OCS_PRESS:
            VERBOSE and print("OCS_PRESS")
            if not level:
                self._new_state(OCS_PRESSEND)
                self._update_state(self.RELEASED)
                self._start_time = now
            else:
                self._update_state(self.HOLD)
                if self._during_long_press_handler is not None:
                    if self._during_long_press_param is None:
                        self._during_long_press_handler()
                    else:
                        self._during_long_press_handler(self._during_long_press_param)
        elif self._state == OCS_PRESSEND:
            VERBOSE and print("OCS_PRESSEND")
            if level and wait_time < self._debounce_ticks:
                self._new_state(self._last_state)
                self._update_state(self.last_state)
            elif wait_time >= self._debounce_ticks:
                self._update_state(self.RELEASED)
                if self._long_press_stop_handler is not None:
                    if self._long_press_stop_param is None:
                        self._long_press_stop_handler()
                    else:
                        self._long_press_stop_handler(self._long_press_stop_param)
                self.reset()
        else:
            self._new_state(OCS_INIT)

    def _new_state(self, next_state):
        self._last_state = self._state
        self._state = next_state

    def reset(self):
        self._state = OCS_INIT
        self._last_state = OCS_INIT
        self._n_clicks = 0
        self._start_time = 0

    def _update_state(self, state):
        self.last_state = self.current_state
        self.current_state = state

from hardware import *
import time

def click_event():
    print("click")

def double_click_event():
    print("double_click")

def pressed_event():
    print("pressed")

def released_event():
    print("released")

def hold_event():
    print("hold")

b = Button(1, pullup_active=False)
b.attach_click_event(click_event)
b.attach_double_click(double_click_event)
b.attach_long_press_start(pressed_event)
b.attach_long_press_stop(released_event)
b.attach_during_long_press(hold_event)

while True:
    b.tick(None)
    time.sleep_ms(10)

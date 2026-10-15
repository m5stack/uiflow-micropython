# Stamp Timer Power 2

StampTimerPower2 provides power management, GPIO, ADC, PWM, NeoPixel, button events, IRQ, wakeup, watchdog, timers and RTC RAM through I2C.

Support the following products:

    Stamp Timer Power 2

## MicroPython Example

#### GPIO input

G4 is a pull-up input. Connect G4 to GND for Low (0), or release it for High (1).

```python
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from stamp import StampTimerPower2
import time

label_title = None
label_description = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
i2c0 = None
stp2 = None

last_time = None
level = None

def setup():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        i2c0, \
        stp2, \
        last_time, \
        level

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "GPIO Input", 108, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "G4: GND = Low / release = High",
        12,
        38,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    label_caption1 = Widgets.Label(
        "Input Pin", 12, 78, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "G4 Logic Level", 12, 134, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    stp2.set_pin_mode(4, StampTimerPower2.GPIO_MODE_IN)
    stp2.set_pin_function(4, StampTimerPower2.PIN_FUNCTION_GPIO)
    stp2.set_pin_pull(4, StampTimerPower2.GPIO_PULL_UP)
    last_time = time.ticks_ms()

def loop():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        i2c0, \
        stp2, \
        last_time, \
        level
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        level = stp2.read_pin(4)
        label_value1.setText(str("G4 / Pull-Up"))
        if level:
            label_value2.setText(str("High (1)"))
        else:
            label_value2.setText(str("Low (0)"))
        print((str("G4 input: ") + str(level)))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### GPIO output

G3 is the output. Button A sets Low, B toggles the level, and C sets High. The display shows the commanded level and pin readback.

```python
import os, sys, io
import M5
from M5 import *
from stamp import StampTimerPower2
from hardware import Pin
from hardware import I2C
import time

label_title = None
label_description = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
label_key_a = None
label_action_a = None
label_key_b = None
label_action_b = None
label_key_c = None
label_action_c = None
i2c0 = None
stp2 = None

level = None
last_time = None
actual = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual
    level = 0
    stp2.set_pin_value(3, level)

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual
    level = 1 - level
    stp2.set_pin_value(3, level)

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual
    level = 1
    stp2.set_pin_value(3, level)

def setup():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "GPIO Output", 99, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "G3 -> meter or resistor + LED",
        12,
        38,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    label_caption1 = Widgets.Label(
        "G3 Output Command", 12, 78, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "G3 Pin Readback", 12, 134, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "Low", 50, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "Toggle", 140, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "High", 235, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    level = 0
    stp2.set_pin_mode(3, StampTimerPower2.GPIO_MODE_IN)
    stp2.set_pin_function(3, StampTimerPower2.PIN_FUNCTION_GPIO)
    stp2.set_pin_pull(3, StampTimerPower2.GPIO_PULL_NONE)
    stp2.set_pin_value(3, 0)
    stp2.set_pin_mode(3, StampTimerPower2.GPIO_MODE_OUT)
    last_time = time.ticks_ms()

def loop():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        level, \
        last_time, \
        actual
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        actual = stp2.read_pin(3)
        if level:
            label_value1.setText(str("High (1)"))
        else:
            label_value1.setText(str("Low (0)"))
        if actual:
            label_value2.setText(str("High (1)"))
        else:
            label_value2.setText(str("Low (0)"))
        print((str((str((str("G3 command: ") + str(level))) + str(" readback: "))) + str(actual)))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### GPIO interrupt

Connect STP2 G0 to Basic G26 for IRQ. Connect G4 to GND and release it to generate input changes. Button A clears the count, B pauses IRQ handling, and C resumes it. The display shows the count and G4 level.

```python
import os, sys, io
import M5
from M5 import *
from stamp import StampTimerPower2
from driver.m5pm1 import EVENT
from hardware import Pin
from hardware import I2C
import time

label_title = None
label_description = None
label_note = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
label_key_a = None
label_action_a = None
label_key_b = None
label_action_b = None
label_key_c = None
label_action_c = None
i2c0 = None
stp2 = None

count = None
event_handle = None
event_data = None
running = None
removed = None
last_time = None
level = None

# Describe this function...
def start_irq():
    global \
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level, \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2
    stp2 = StampTimerPower2(i2c0, pm1_int_gpio=0, mcu_int_gpio=26)
    event_handle = stp2.add_event_cb(stp2_gpio4_change_event, EVENT.GPIO4_CHANGE)
    stp2.wake()
    stp2.set_pin_pull(4, StampTimerPower2.GPIO_PULL_UP)
    running = 1
    label_note.setText(str("G4: connect to GND / release"))

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    count = 0

def stp2_gpio4_change_event(event):
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    event_data = event.user_data
    count = count + 1

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    if running:
        removed = stp2.remove_event_cb(event_handle)
        stp2.deinit()
        event_handle = None
        running = 0
        label_note.setText(str("PAUSED"))

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    if running == 0:
        start_irq()

def setup():
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "GPIO Interrupt", 91, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "IRQ: STP2 G0 -> Basic G26", 12, 38, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_note = Widgets.Label(
        "G4: connect to GND / release", 12, 54, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_caption1 = Widgets.Label(
        "G4 Change Count", 12, 78, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "G4 Level", 12, 134, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "Clear", 46, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "Pause", 135, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "Resume", 222, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    count = 0
    running = 0
    start_irq()

def loop():
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        count, \
        event_handle, \
        event_data, \
        running, \
        removed, \
        last_time, \
        level
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        label_value1.setText(str(count))
        level = stp2.read_pin(4)
        if level:
            label_value2.setText(str("HIGH (1)"))
        else:
            label_value2.setText(str("LOW (0)"))
        print((str("G4 IRQ count: ") + str(count)))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### ADC input

Read raw ADC values from G1 and G2. Each value is in the range 0 to 4095.

```python
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from stamp import StampTimerPower2
import time

label_title = None
label_description = None
label_note = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
i2c0 = None
stp2 = None

last_time = None
value1 = None
adc1 = None
value2 = None
adc2 = None

def setup():
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        i2c0, \
        stp2, \
        last_time, \
        value1, \
        adc1, \
        value2, \
        adc2

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "ADC Input", 111, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "G1 / G2 analog input", 12, 38, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_note = Widgets.Label(
        "Input: 0..Vref; never connect 5V",
        12,
        54,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    label_caption1 = Widgets.Label(
        "ADC1 / G1  (Raw)", 12, 78, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "ADC2 / G2  (Raw)", 12, 134, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    adc1 = stp2.ADC(1)
    adc2 = stp2.ADC(2)
    last_time = time.ticks_ms()

def loop():
    global \
        label_title, \
        label_description, \
        label_note, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        i2c0, \
        stp2, \
        last_time, \
        value1, \
        adc1, \
        value2, \
        adc2
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        value1 = stp2.read_adc_raw(1)
        value2 = stp2.read_adc_raw(2)
        label_value1.setText(str(str(value1)))
        label_value2.setText(str(str(value2)))
        print((str((str((str("ADC G1: ") + str(value1))) + str(" G2: "))) + str(value2)))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### PWM output

PWM0 uses G3 at 1 kHz. Button A decreases duty by 10 percentage points, B sets duty to zero, and C increases duty by 10 percentage points. Duty is limited to 0 to 100 percent.

```python
import os, sys, io
import M5
from M5 import *
from stamp import StampTimerPower2
from hardware import Pin
from hardware import I2C
import time

label_title = None
label_description = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
label_key_a = None
label_action_a = None
label_key_b = None
label_action_b = None
label_key_c = None
label_action_c = None
i2c0 = None
stp2 = None

import math

pwm = None
duty = None
FREQUENCY_HZ = None
last_time = None

# Describe this function...
def apply_duty():
    global \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time, \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2
    pwm = stp2.PWM(
        0, freq=FREQUENCY_HZ, duty_u16=math.floor((duty * 65535) / 100), duty_ns=None, invert=False
    )

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time
    if duty > 0:
        duty = duty + -10
    apply_duty()

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time
    duty = 0
    apply_duty()

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time
    if duty < 100:
        duty = duty + 10
    apply_duty()

def setup():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "PWM Output", 98, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "PWM0 / G3 -> oscilloscope or LED",
        12,
        38,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    label_caption1 = Widgets.Label(
        "PWM0 / G3 Duty", 12, 78, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "Shared Frequency", 12, 134, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "Duty -10", 36, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 152, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "Zero", 139, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 245, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "Duty +10", 216, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    FREQUENCY_HZ = 1000
    duty = 0
    apply_duty()
    last_time = time.ticks_ms()

def loop():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        pwm, \
        duty, \
        FREQUENCY_HZ, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        label_value1.setText(str((str(duty) + str("%"))))
        label_value2.setText(str((str((stp2.get_pwm_frequency())) + str(" Hz"))))
        print((str("PWM0 duty: ") + str(duty)))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### NeoPixel control

Connect the LED data input to G0 and share GND. Button A cycles through red, green, blue and white; B decreases brightness by 10 percentage points and C increases it by 10. The example controls one LED, starting with red at 20 percent brightness.

```python
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from stamp import StampTimerPower2
import time

label_title = None
label_description = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
label_key_a = None
label_action_a = None
label_key_b = None
label_action_b = None
label_key_c = None
label_action_c = None
i2c0 = None
stp2 = None

import math

intensity = None
color_index = None
brightness = None
color_name = None
led_index = None
last_time = None
red = None
LED_COUNT = None
green = None
blue = None

# Describe this function...
def update_leds():
    global \
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        led_index, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        blue, \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2
    intensity = math.floor((255 * brightness) / 100)
    if color_index == 0:
        color_name = "Red"
        red = intensity
        green = 0
        blue = 0
    else:
        if color_index == 1:
            color_name = "Green"
            red = 0
            green = intensity
            blue = 0
        else:
            if color_index == 2:
                color_name = "Blue"
                red = 0
                green = 0
                blue = intensity
            else:
                color_name = "White"
                red = intensity
                green = intensity
                blue = intensity
    for led_index in range(LED_COUNT):
        stp2.set_neopixel_color(led_index, (red << 16) | (green << 8) | blue)

    stp2.refresh_neopixels()

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue
    color_index = (color_index + 1) % 4
    update_leds()

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue
    if brightness > 0:
        brightness = brightness + -10
    update_leds()

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue
    if brightness < 100:
        brightness = brightness + 10
    update_leds()

def setup():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Neopixel Output", 83, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "LED DIN -> G0; shared GND", 12, 38, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_caption1 = Widgets.Label(
        "LED Color", 12, 78, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label("--", 12, 96, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_caption2 = Widgets.Label(
        "Brightness", 12, 134, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 12, 152, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "Color", 50, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "Dim -10%", 125, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "Up +10%", 222, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    LED_COUNT = 1
    color_index = 0
    brightness = 20
    stp2.set_pin_drive(0, StampTimerPower2.DRIVE_PUSH_PULL)
    stp2.set_pin_function(0, StampTimerPower2.PIN_FUNCTION_OTHER)
    stp2.set_neopixel_count(LED_COUNT)
    update_leds()
    last_time = time.ticks_ms()

def loop():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        intensity, \
        color_index, \
        brightness, \
        color_name, \
        last_time, \
        red, \
        LED_COUNT, \
        green, \
        led_index, \
        blue
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        label_value1.setText(str(color_name))
        label_value2.setText(str((str(brightness) + str("%"))))
        print(
            (str((str((str("LED: ") + str(color_name))) + str(" brightness: "))) + str(brightness))
        )

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Power control

Button A toggles LDO and button B toggles DCDC. The display and serial output show the enable states read from the module every 100 ms.

```python
import os, sys, io
import M5
from M5 import *
from stamp import StampTimerPower2
from hardware import Pin
from hardware import I2C
import time

label_title = None
label_description = None
label_caption1 = None
label_value1 = None
label_caption2 = None
label_value2 = None
label_key_a = None
label_action_a = None
label_key_b = None
label_action_b = None
label_key_c = None
label_action_c = None
i2c0 = None
stp2 = None

last_time = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        last_time
    if stp2.is_ldo_enabled():
        stp2.disable_ldo()
    else:
        stp2.enable_ldo()

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        last_time
    if stp2.is_dcdc_enabled():
        stp2.disable_dcdc()
    else:
        stp2.enable_dcdc()

def setup():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Power Control", 94, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_description = Widgets.Label(
        "STP2 LDO / DCDC Toggle", 12, 38, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_caption1 = Widgets.Label(
        "LDO Output", 12, 90, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value1 = Widgets.Label(
        "--", 140, 86, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_caption2 = Widgets.Label(
        "DCDC Output", 12, 140, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_value2 = Widgets.Label(
        "--", 140, 136, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_key_a = Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_a = Widgets.Label(
        "LDO", 50, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_b = Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_b = Widgets.Label(
        "DCDC", 140, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14
    )
    label_key_c = Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    label_action_c = Widgets.Label(
        "--", 248, 215, 1.0, 0x475569, 0x000000, Widgets.FONTS.Montserrat14
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c0)
    stp2.wake()
    label_key_a.setColor(0x38BDF8, 0x000000)
    label_action_a.setColor(0xE2E8F0, 0x000000)
    label_key_b.setColor(0x38BDF8, 0x000000)
    label_action_b.setColor(0xE2E8F0, 0x000000)
    label_key_c.setColor(0x475569, 0x000000)
    label_action_c.setColor(0x475569, 0x000000)
    last_time = time.ticks_ms()

def loop():
    global \
        label_title, \
        label_description, \
        label_caption1, \
        label_value1, \
        label_caption2, \
        label_value2, \
        label_key_a, \
        label_action_a, \
        label_key_b, \
        label_action_b, \
        label_key_c, \
        label_action_c, \
        i2c0, \
        stp2, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        if stp2.is_ldo_enabled():
            label_value1.setText(str("On"))
        else:
            label_value1.setText(str("Off"))
        if stp2.is_dcdc_enabled():
            label_value2.setText(str("On"))
        else:
            label_value2.setText(str("Off"))
        print(
            (
                str((str((str("LDO: ") + str((stp2.is_ldo_enabled())))) + str(" DCDC: ")))
                + str((stp2.is_dcdc_enabled()))
            )
        )

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Timed power-on

Button A toggles LDO output retention during shutdown (Off by default). Button B cycles the power-on delay through 5, 10 and 15 seconds (5 seconds by default). Button C (Shutdown) applies the setting, arms the power-on timer and immediately shuts down STP2. Buttons are locked until the countdown finishes.

Keep Basic independently powered so it can display the countdown while STP2 is shut down.

The Python example reads the wake source after the countdown and displays whether a timer wake was detected.

```python
import time
import M5
from M5 import BtnA, BtnB, BtnC, Widgets
from hardware import I2C, Pin
from stamp import StampTimerPower2

stp2 = None
label_hold = None
label_on = None
label_status = None
ldo_hold = False
on_delay_s = 5
phase = 0
phase_start = 0
last_refresh = 0

def btna_was_clicked_event(state):
    global ldo_hold
    if phase == 0:
        ldo_hold = not ldo_hold
        label_hold.setText("On" if ldo_hold else "Off")

def btnb_was_clicked_event(state):
    global on_delay_s
    if phase == 0:
        on_delay_s = on_delay_s % 15 + 5
        label_on.setText(str(on_delay_s) + " s")

def btnc_was_clicked_event(state):
    global phase, phase_start
    if phase != 0:
        return
    if ldo_hold:
        stp2.enable_ldo_power_hold()
    else:
        stp2.disable_ldo_power_hold()
    stp2.clear_wake_source(StampTimerPower2.WAKE_SOURCE_TIMER)
    # Arm the power-on timer before shutting down STP2.
    stp2.set_timer(on_delay_s, StampTimerPower2.TIMER_ACTION_POWER_ON)
    stp2.power_off()
    phase_start = time.ticks_ms()
    phase = 1
    label_status.setText("Power on in " + str(on_delay_s) + " s")
    print("Shutdown requested; LDO hold:", ldo_hold, "; power on after", on_delay_s, "s")

def setup():
    global stp2, label_hold, label_on, label_status, last_refresh
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    Widgets.Label("Power-on Timer", 80, 5, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat18)
    Widgets.Label(
        "Keep LDO output during shutdown",
        12,
        38,
        1.0,
        0x94A3B8,
        0x000000,
        Widgets.FONTS.Montserrat14,
    )
    Widgets.Label("LDO keep on", 12, 80, 1.0, 0xFBBF24, 0x000000, Widgets.FONTS.Montserrat14)
    label_hold = Widgets.Label("Off", 190, 76, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    Widgets.Label("Power on after", 12, 125, 1.0, 0x4ADE80, 0x000000, Widgets.FONTS.Montserrat14)
    label_on = Widgets.Label("5 s", 190, 121, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24)
    label_status = Widgets.Label(
        "Ready", 12, 164, 1.0, 0x94A3B8, 0x000000, Widgets.FONTS.Montserrat14
    )
    Widgets.Label("A", 60, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("LDO keep", 30, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("B", 155, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("On +5 s", 125, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("C", 248, 195, 1.0, 0x38BDF8, 0x000000, Widgets.FONTS.Montserrat14)
    Widgets.Label("Shutdown", 217, 215, 1.0, 0xE2E8F0, 0x000000, Widgets.FONTS.Montserrat14)
    i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    stp2 = StampTimerPower2(i2c)
    stp2.wake()
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)
    last_refresh = time.ticks_ms()

def loop():
    global phase, phase_start, last_refresh
    M5.update()
    now = time.ticks_ms()
    if time.ticks_diff(now, last_refresh) < 100:
        return
    last_refresh = now
    if phase == 1:
        # Keep I2C idle while STP2 is off; BASIC stays independently powered.
        elapsed = time.ticks_diff(now, phase_start)
        remaining = max(0, on_delay_s * 1000 - elapsed)
        label_status.setText("Power on in " + str((remaining + 999) // 1000) + " s")
        if elapsed >= on_delay_s * 1000 + 500:
            stp2.wake()
            source = stp2.get_wake_source()
            if source & StampTimerPower2.WAKE_SOURCE_TIMER:
                label_status.setText("Timer wake confirmed")
            else:
                label_status.setText("Timer wake not detected")
            print("Wake source:", source)
            phase = 0

if __name__ == "__main__":
    setup()
    while True:
        loop()
```

## **API**

#### StampTimerPower2

### Constructors

### `class StampTimerPower2(i2c, *, pm1_int_gpio=-1, mcu_int_gpio=-1)`

    Create the module at fixed I2C address `0x6E`. The application owns the I2C object. Supply both IRQ GPIOs or leave both at `-1`.

    - Parameter `i2c`: Caller-owned I2C bus.
    - Type of `i2c`: I2C
    - Parameter `Module IRQ output GPIO, 0~4; -1 disables IRQ. Default` (`pm1_int_gpio:`): -1. Keyword-only parameter.
    - Type of `pm1_int_gpio`: int
    - Parameter `Basic IRQ input GPIO; use 26 for this wiring, or -1 without IRQ. Default` (`mcu_int_gpio:`): -1. Keyword-only parameter.
    - Type of `mcu_int_gpio`: int

```python
import M5
from hardware import I2C, Pin
from stamp import StampTimerPower2

M5.begin()
i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
stp2 = StampTimerPower2(i2c)
# For INT callbacks only: connect STP2 G0 to Basic G26.
# stp2 = StampTimerPower2(i2c, pm1_int_gpio=0, mcu_int_gpio=26)
```
### Constants

    - - Constant
      - Value
      - Meaning
    - - `StampTimerPower2.PIN_FUNCTION_GPIO`
      - 0
      - Normal GPIO function.
    - - `StampTimerPower2.PIN_FUNCTION_IRQ`
      - 1
      - Active-low IRQ output function.
    - - `StampTimerPower2.PIN_FUNCTION_WAKE`
      - 2
      - Power-off wake input function.
    - - `StampTimerPower2.PIN_FUNCTION_OTHER`
      - 3
      - ADC, PWM, NeoPixel, or another alternate function.
    - - `StampTimerPower2.GPIO_MODE_IN`
      - 0
      - Digital input mode.
    - - `StampTimerPower2.GPIO_MODE_OUT`
      - 1
      - Push-pull output mode.
    - - `StampTimerPower2.GPIO_MODE_OPEN_DRAIN`
      - 2
      - Open-drain output mode.
    - - `StampTimerPower2.GPIO_PULL_NONE`
      - 0
      - No internal pull resistor.
    - - `StampTimerPower2.GPIO_PULL_UP`
      - 1
      - Internal pull-up enabled.
    - - `StampTimerPower2.GPIO_PULL_DOWN`
      - 2
      - Internal pull-down enabled.
    - - `StampTimerPower2.DRIVE_PUSH_PULL`
      - 0
      - Push-pull drive.
    - - `StampTimerPower2.DRIVE_OPEN_DRAIN`
      - 1
      - Open-drain drive.
    - - `StampTimerPower2.POWER_SOURCE_NONE`
      - 0
      - No power-source flag is active.
    - - `StampTimerPower2.POWER_SOURCE_5VIN`
      - 1
      - 5VIN / USB input is active.
    - - `StampTimerPower2.POWER_SOURCE_5VINOUT`
      - 2
      - The bidirectional 5VINOUT input is active.
    - - `StampTimerPower2.POWER_SOURCE_BATTERY`
      - 4
      - Battery input is active.
    - - `StampTimerPower2.WAKE_SOURCE_TIMER`
      - 1
      - Timer wake.
    - - `StampTimerPower2.WAKE_SOURCE_VIN`
      - 2
      - 5VIN insertion wake.
    - - `StampTimerPower2.WAKE_SOURCE_POWER_BUTTON`
      - 4
      - Power-button wake.
    - - `StampTimerPower2.WAKE_SOURCE_RESET_BUTTON`
      - 8
      - Reset-button wake.
    - - `StampTimerPower2.WAKE_SOURCE_COMMAND_RESET`
      - 16
      - Command-reset wake.
    - - `StampTimerPower2.WAKE_SOURCE_GPIO`
      - 32
      - GPIO input wake.
    - - `StampTimerPower2.WAKE_SOURCE_5V_INOUT`
      - 64
      - 5VINOUT event wake.
    - - `StampTimerPower2.BUTTON_TIMING_CLICK`
      - 0
      - Single-click timing selector.
    - - `StampTimerPower2.BUTTON_TIMING_DOUBLE`
      - 1
      - Double-click timing selector.
    - - `StampTimerPower2.BUTTON_TIMING_LONG`
      - 2
      - Long-press timing selector.
    - - `StampTimerPower2.TIMER_ACTION_STOP`
      - 0
      - Stop when the timer expires.
    - - `StampTimerPower2.TIMER_ACTION_FLAG`
      - 1
      - Generate an event flag when the timer expires.
    - - `StampTimerPower2.TIMER_ACTION_REBOOT`
      - 2
      - Reboot when the timer expires.
    - - `StampTimerPower2.TIMER_ACTION_POWER_ON`
      - 3
      - Power on when the timer expires.
    - - `StampTimerPower2.TIMER_ACTION_POWER_OFF`
      - 4
      - Power off when the timer expires.
    - - `StampTimerPower2.IRQ_GROUP_GPIO`
      - 0
      - irq group gpio
    - - `StampTimerPower2.IRQ_GROUP_SYSTEM`
      - 1
      - irq group system
    - - `StampTimerPower2.IRQ_GROUP_BUTTON`
      - 2
      - irq group button
    - - `StampTimerPower2.WAKE_EDGE_FALLING`
      - 0
      - wake edge falling
    - - `StampTimerPower2.WAKE_EDGE_RISING`
      - 1
      - wake edge rising

Combine EVENT flags with bitwise OR for add_event_cb(). The namespace refers to the existing driver constants without copying values.

    - - Constant
      - Value
      - Meaning
    - - `StampTimerPower2.EVENT.GPIO0_CHANGE`
      - 0x1
      - gpio0 change
    - - `StampTimerPower2.EVENT.GPIO1_CHANGE`
      - 0x2
      - gpio1 change
    - - `StampTimerPower2.EVENT.GPIO2_CHANGE`
      - 0x4
      - gpio2 change
    - - `StampTimerPower2.EVENT.GPIO3_CHANGE`
      - 0x8
      - gpio3 change
    - - `StampTimerPower2.EVENT.GPIO4_CHANGE`
      - 0x10
      - gpio4 change
    - - `StampTimerPower2.EVENT.VIN_INSERT`
      - 0x20
      - vin insert
    - - `StampTimerPower2.EVENT.VIN_REMOVE`
      - 0x40
      - vin remove
    - - `StampTimerPower2.EVENT.VINOUT_INSERT`
      - 0x80
      - vinout insert
    - - `StampTimerPower2.EVENT.VINOUT_REMOVE`
      - 0x100
      - vinout remove
    - - `StampTimerPower2.EVENT.BATTERY_INSERT`
      - 0x200
      - battery insert
    - - `StampTimerPower2.EVENT.BATTERY_REMOVE`
      - 0x400
      - battery remove
    - - `StampTimerPower2.EVENT.BUTTON_CLICK`
      - 0x800
      - button click
    - - `StampTimerPower2.EVENT.WAKE`
      - 0x1000
      - wake
    - - `StampTimerPower2.EVENT.BUTTON_DOUBLE`
      - 0x2000
      - button double
    - - `StampTimerPower2.EVENT.ALL`
      - 0x3fff
      - all

### Methods

Methods below are called on the StampTimerPower2 instance. Register transactions may raise OSError; failed communication is reported as False by is_connected(). Setters and action methods return None unless a return value is listed. Inputs are converted and validated by the current implementation; validation errors may be ValueError or TypeError.

### `add_event_cb(callback, filter, *, user_data=None)`

    Register an event listener. The IRQ output and MCU falling-edge input are initialized by the StampTimerPower2 constructor. The driver combines all filters, configures IRQ masks, and automatically switches GPIO event inputs to GPIO input mode without changing their pull settings. The original GPIO configuration is restored after its last listener is removed.

    - Parameter `callback`: Callback receiving one `Event` object.
    - Type of `callback`: callable
    - Parameter `filter`: One or more ORed `StampTimerPower2.EVENT.*` flags.
    - Type of `filter`: int
    - Parameter `Application data exposed as `event.user_data`. Default` (`user_data:`): `None`. Keyword-only parameter.
    - Type of `user_data`: object

    - Returns: Registration handle accepted by `remove_event_cb()`.
    - Return type: int

    Callbacks run in scheduled MicroPython context. Each triggered bit produces one Event with target, code and user_data. code contains one EVENT flag. Calling without an IRQ pair raises RuntimeError; remove callbacks by their returned handle.

```python
# Requires an stp2 instance configured for INT callbacks.
def on_event(event):
    print(event.code)

handle = stp2.add_event_cb(on_event, StampTimerPower2.EVENT.GPIO4_CHANGE)
# Keep the Basic main loop running; when finished:
# stp2.remove_event_cb(handle)
# stp2.deinit()
```
### `remove_event_cb(handle_or_callback)`

    Remove one listener by handle or all registrations using the same callback object.

    - Parameter `handle_or_callback`: Registration handle or callback object.
    - Type of `handle_or_callback`: int / callable

    - Returns: Number of registrations removed.
    - Return type: int

```python
# handle was returned by add_event_cb().
removed = stp2.remove_event_cb(handle)
```
### `deinit()`

    Release the host IRQ registration owned by this driver.

    This operation is idempotent. Ordinary register access remains available, and add_event_cb() can recreate the IRQ registration when the pins were configured.

    - Returns: No return value.
    - Return type: None

```python
stp2.deinit()
```
### `wake()`

    Wake StampTimerPower2 and wait for communication to recover. The driver sends an empty I2C transaction and ignores a NACK from the first wake attempt.

    - Returns: No return value.
    - Return type: None

```python
stp2.wake()
```
### `is_connected()`

    Check whether a device responds at the configured I2C address.

    - Returns: `True` when the device responds, otherwise `False`.
    - Return type: bool

```python
value = stp2.is_connected()
print(value)
```
### `get_device_info()`

    Read the device information block.

    - Returns: `(device_id, device_model, hardware_version, firmware_version)`.
    - Return type: tuple

```python
value = stp2.get_device_info()
print(value)
```
### `get_uid()`

    Read the 12-byte device unique identifier.

    - Returns: The 12-byte device UID.
    - Return type: bytes

```python
value = stp2.get_uid()
print(value)
```
### `get_device_id()`

    Read the device ID.

    - Returns: Device ID in the range `0~255`.
    - Return type: int

```python
value = stp2.get_device_id()
print(value)
```
### `get_device_model()`

    Read the device model.

    - Returns: Device model in the range `0~255`.
    - Return type: int

```python
value = stp2.get_device_model()
print(value)
```
### `get_hardware_version()`

    Read the hardware version.

    - Returns: Hardware version in the range `0~255`.
    - Return type: int

```python
value = stp2.get_hardware_version()
print(value)
```
### `get_firmware_version()`

    Read the firmware version.

    - Returns: Firmware version in the range `0~255`.
    - Return type: int

```python
value = stp2.get_firmware_version()
print(value)
```
### `Pin(gpio, mode=None, pull=-1, *, value=None)`

    Create a MicroPython Pin-style object backed by StampTimerPower2 GPIO registers.

    - Parameter `gpio`: StampTimerPower2 GPIO number in the range `0~4`.
    - Type of `gpio`: int
    - Parameter ``Pin.IN`, `Pin.OUT`, or `Pin.OPEN_DRAIN`; `None` preserves the current mode. Default` (`mode:`): `None`.
    - Type of `mode`: int / None
    - Parameter ``Pin.PULL_UP`, `Pin.PULL_DOWN`, or `None`; `-1` preserves the current setting. Default` (`pull:`): `-1`.
    - Type of `pull`: int / None
    - Parameter `Initial output level; `None` leaves the output latch unchanged. Default` (`value:`): `None`. Keyword-only parameter.
    - Type of `value`: int / bool / None

    - Returns: Configured StampTimerPower2 GPIO object.
    - Return type: Pin

```python
from hardware import Pin
pin = stp2.Pin(4)
# Use the returned object, then release it.
pin.deinit()
```
### `ADC(channel)`

    Create a MicroPython ADC-style object for GPIO1 or GPIO2.

    - Parameter `channel`: ADC channel; only `1` (GPIO1) or `2` (GPIO2) is supported.
    - Type of `channel`: int

    - Returns: A new ADC object for the selected input.
    - Return type: ADC

```python
adc = stp2.ADC(1)
# Use the returned object, then release it.
adc.deinit()
```
### `PWM(channel, *, freq=None, duty_u16=0, duty_ns=None, invert=False)`

    Create a MicroPython PWM-style object for PWM0 or PWM1.

    - Parameter `channel`: PWM channel; only `0` (GPIO3) or `1` (GPIO4) is supported.
    - Type of `channel`: int
    - Parameter `Shared frequency in the range `1~65535` Hz; `None` preserves it, falling back to 500 Hz when the frequency register is zero. Default` (`freq:`): `None`. Keyword-only parameter.
    - Type of `freq`: int / None
    - Parameter `Initial duty in the range `0~65535`. Default` (`duty_u16:`): `0`. Keyword-only parameter.
    - Type of `duty_u16`: int
    - Parameter `Initial high pulse width in nanoseconds; mutually exclusive with nonzero `duty_u16`. Default` (`duty_ns:`): `None`. Keyword-only parameter.
    - Type of `duty_ns`: int / None
    - Parameter ``True` selects inverted output polarity. Default` (`invert:`): `False`. Keyword-only parameter.
    - Type of `invert`: bool

    - Returns: Configured StampTimerPower2 PWM object.
    - Return type: PWM

```python
pwm = stp2.PWM(0)
# Use the returned object, then release it.
pwm.deinit()
```
### `NeoPixel(gpio, count, *, bpp=3, timing=1)`

    Create a buffered MicroPython NeoPixel-style object.

    - Parameter `gpio`: NeoPixel output pin; only StampTimerPower2 GPIO0 is supported.
    - Type of `gpio`: int
    - Parameter `count`: Number of buffered LEDs in the range `1~32`.
    - Type of `count`: int
    - Parameter `Bytes per pixel; only RGB value `3` is supported. Default` (`bpp:`): `3`. Keyword-only parameter.
    - Type of `bpp`: int
    - Parameter `NeoPixel protocol timing selector, `0` or `1`; StampTimerPower2 uses fixed hardware timing for both. Default` (`timing:`): `1`. Keyword-only parameter.
    - Type of `timing`: int

    - Returns: A new buffered NeoPixel object.
    - Return type: NeoPixel

```python
pixels = stp2.NeoPixel(0, 1)
# Use the returned object, then release it.
pixels.deinit()
```
### `set_pin_function(gpio, function)`

    Set a GPIO function mux.

    - Parameter `gpio`: GPIO index in the range `0~4`.
    - Type of `gpio`: int
    - Parameter `function`: GPIO function selected with a `PIN_FUNCTION_*` constant.
    - Type of `function`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pin_function(4, StampTimerPower2.PIN_FUNCTION_GPIO)
```
### `set_pin_mode(gpio, mode)`

    Set a GPIO input/output mode.

    - Parameter `gpio`: GPIO index in the range `0~4`.
    - Type of `gpio`: int
    - Parameter `mode`: `GPIO_MODE_IN`, `GPIO_MODE_OUT`, or `GPIO_MODE_OPEN_DRAIN`.
    - Type of `mode`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pin_mode(4, StampTimerPower2.GPIO_MODE_IN)
```
### `set_pin_pull(gpio, pull)`

    Set GPIO pull configuration.

    - Parameter `gpio`: GPIO index in the range `0~4`.
    - Type of `gpio`: int
    - Parameter `pull`: `GPIO_PULL_NONE`, `GPIO_PULL_UP`, or `GPIO_PULL_DOWN`.
    - Type of `pull`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pin_pull(4, StampTimerPower2.GPIO_PULL_UP)
```
### `set_pin_drive(gpio, drive)`

    Set GPIO output drive type.

    - Parameter `gpio`: GPIO index in the range `0~4`.
    - Type of `gpio`: int
    - Parameter `drive`: `DRIVE_PUSH_PULL` or `DRIVE_OPEN_DRAIN`.
    - Type of `drive`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pin_drive(4, StampTimerPower2.DRIVE_PUSH_PULL)
```
### `set_pin_value(gpio, value)`

    Write a GPIO output latch value.

    - Parameter `gpio`: GPIO index in the range `0~4`.
    - Type of `gpio`: int
    - Parameter `Output level` (`value:`): `0`, `1`, `False`, or `True`.
    - Type of `value`: int / bool

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pin_value(4, 1)
```
### `read_pin(gpio)`

    Read a GPIO input value.

    - Parameter `gpio`: GPIO index in the range `0~4`.
    - Type of `gpio`: int

    - Returns: Current input level, `0` or `1`.
    - Return type: int

```python
value = stp2.read_pin(4)
print(value)
```
### `get_power_source()`

    Read the active power-source bit mask.

    - Returns: ORed `POWER_SOURCE_*` flags.
    - Return type: int

```python
value = stp2.get_power_source()
print(value)
```
### `get_power_config()`

    Read the power-configuration bit mask.

    - Returns: Raw power-configuration bit mask in the range `0~255`.
    - Return type: int

```python
value = stp2.get_power_config()
print(value)
```
### `is_charging_enabled()`

    Return whether battery charging is enabled.

    - Returns: `True` when the charging-enable bit is set.
    - Return type: bool

```python
value = stp2.is_charging_enabled()
print(value)
```
### `is_dcdc_enabled()`

    Return whether the DCDC power rail is enabled.

    - Returns: `True` when the DCDC rail is enabled.
    - Return type: bool

```python
value = stp2.is_dcdc_enabled()
print(value)
```
### `is_ldo_enabled()`

    Return whether the LDO power rail is enabled.

    - Returns: `True` when the LDO rail is enabled.
    - Return type: bool

```python
value = stp2.is_ldo_enabled()
print(value)
```
### `is_boost_enabled()`

    Return whether the BOOST / 5VINOUT power rail is enabled.

    - Returns: `True` when the BOOST / 5VINOUT rail is enabled.
    - Return type: bool

```python
value = stp2.is_boost_enabled()
print(value)
```
### `enable_charging()`

    Enable battery charging.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_charging()
```
### `disable_charging()`

    Disable battery charging.

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_charging()
```
### `enable_dcdc()`

    Enable the DCDC power rail.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_dcdc()
```
### `disable_dcdc()`

    Disable the DCDC power rail.

    - Returns: No return value.
    - Return type: None

```python
# Manual power test only; affects the external STP2.
stp2.disable_dcdc()
```
### `enable_ldo()`

    Enable the LDO power rail.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_ldo()
```
### `disable_ldo()`

    Disable the LDO power rail.

    - Returns: No return value.
    - Return type: None

```python
# Manual power test only; affects the external STP2.
stp2.disable_ldo()
```
### `enable_boost()`

    Enable the BOOST / 5VINOUT power rail.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_boost()
```
### `disable_boost()`

    Disable the BOOST / 5VINOUT power rail.

    - Returns: No return value.
    - Return type: None

```python
# Manual power test only; affects the external STP2.
stp2.disable_boost()
```
### `set_led_enable_level(level)`

    Set the LED_EN default output level bit.

    - Parameter `Default LED_EN output level` (`level:`): `0`/`False` for low, `1`/`True` for high.
    - Type of `level`: int / bool

    - Returns: No return value.
    - Return type: None

```python
stp2.set_led_enable_level(True)
```
### `set_battery_low_voltage_threshold_mv(voltage_mv)`

    Set the battery low-voltage protection threshold.

    - Parameter `voltage_mv`: Low-voltage threshold in millivolts; one of `3000`, `3100`, `3200`, or `3300`.
    - Type of `voltage_mv`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_battery_low_voltage_threshold_mv(3000)
```
### `get_battery_low_voltage_threshold_mv()`

    Read the configured battery low-voltage threshold.

    - Returns: Configured threshold in millivolts: `3000`, `3100`, `3200`, or `3300`.
    - Return type: int

```python
value = stp2.get_battery_low_voltage_threshold_mv()
print(value)
```
### `enable_gpio_power_hold(gpio)`

    Enable power-hold behavior for one GPIO output.

    - Parameter `gpio`: GPIO output index in the range `0~4`.
    - Type of `gpio`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_gpio_power_hold(4)
```
### `disable_gpio_power_hold(gpio)`

    Disable power-hold behavior for one GPIO output.

    - Parameter `gpio`: GPIO output index in the range `0~4`.
    - Type of `gpio`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_gpio_power_hold(4)
```
### `enable_ldo_power_hold()`

    Enable LDO power hold.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_ldo_power_hold()
```
### `disable_ldo_power_hold()`

    Disable LDO power hold.

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_ldo_power_hold()
```
### `enable_boost_power_hold()`

    Enable BOOST / 5VINOUT power hold.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_boost_power_hold()
```
### `disable_boost_power_hold()`

    Disable BOOST / 5VINOUT power hold.

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_boost_power_hold()
```
### `read_adc_raw(channel)`

    Read a raw ADC conversion value.

    - Parameter `channel`: ADC channel; use `1`, `2`, or internal temperature channel `6`.
    - Type of `channel`: int

    - Returns: Native 12-bit ADC code in the range `0~4095`.
    - Return type: int

```python
value = stp2.read_adc_raw(1)
print(value)
```
### `read_adc_mv(channel)`

    Read an external ADC channel in millivolts.

    - Parameter `channel`: External ADC channel; only `1` (GPIO1) or `2` (GPIO2) is supported.
    - Type of `channel`: int

    - Returns: External ADC input voltage in millivolts.
    - Return type: int

```python
value = stp2.read_adc_mv(1)
print(value)
```
### `read_temperature_raw()`

    Read the internal temperature sensor raw code.

    - Returns: Internal temperature-channel code in the range `0~4095`.
    - Return type: int

```python
value = stp2.read_temperature_raw()
print(value)
```
### `read_button()`

    Read the current PM1 button state.

    - Returns: Current button level: `0` when released or `1` when pressed.
    - Return type: int

```python
value = stp2.read_button()
print(value)
```
### `read_button_event()`

    Read the sticky button-pressed flag.

    - Returns: `True` when the sticky pressed flag was set; reading clears the hardware flag.
    - Return type: bool

```python
value = stp2.read_button_event()
print(value)
```
### `set_button_timing(event, duration_ms)`

    Configure button timing.

    - Parameter `event`: `BUTTON_TIMING_CLICK`, `BUTTON_TIMING_DOUBLE`, or `BUTTON_TIMING_LONG`.
    - Type of `event`: int
    - Parameter `Button timing in milliseconds` (`duration_ms:`): click/double-click accepts 125, 250, 500 or 1000; long press accepts 1000, 2000, 3000 or 4000.
    - Type of `duration_ms`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_button_timing(StampTimerPower2.BUTTON_TIMING_CLICK, 250)
```
### `read_reference_voltage_mv()`

    Read the PM1 reference voltage.

    - Returns: Current reference voltage in millivolts.
    - Return type: int

```python
value = stp2.read_reference_voltage_mv()
print(value)
```
### `read_battery_voltage_mv()`

    Read the battery voltage.

    - Returns: Battery voltage in millivolts.
    - Return type: int

```python
value = stp2.read_battery_voltage_mv()
print(value)
```
### `read_vin_voltage_mv()`

    Read the voltage at the external module 5VIN input.

    - Returns: 5VIN voltage in millivolts.
    - Return type: int

```python
value = stp2.read_vin_voltage_mv()
print(value)
```
### `read_5v_inout_voltage_mv()`

    Read the voltage at the external module 5VINOUT port.

    - Returns: 5VINOUT voltage in millivolts.
    - Return type: int

```python
value = stp2.read_5v_inout_voltage_mv()
print(value)
```
### `get_wake_source(*, clear=False)`

    Read wake-source flags.

    - Parameter `Clear the wake-source flags returned by this read. Default` (`clear:`): `False`. Keyword-only parameter.
    - Type of `clear`: bool

    - Returns: Wake-source bit mask.
    - Return type: int

```python
value = stp2.get_wake_source()
print(value)
```
### `clear_wake_source(mask=None)`

    Clear wake-source flags.

    - Parameter `Wake-source bits to clear; `None` clears every valid wake-source bit. Default` (`mask:`): `None`.
    - Type of `mask`: int / None

    - Returns: No return value.
    - Return type: None

```python
stp2.clear_wake_source()
```
### `set_pwm_frequency(frequency)`

    Set the shared PWM frequency.

    - Parameter `frequency`: Shared PWM frequency in the range `1~65535` Hz.
    - Type of `frequency`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pwm_frequency(1000)
```
### `get_pwm_frequency()`

    Read the shared PWM frequency.

    - Returns: Shared PWM frequency in hertz.
    - Return type: int

```python
value = stp2.get_pwm_frequency()
print(value)
```
### `set_pwm_duty_percent(channel, percent, *, invert=False)`

    Set a PWM channel duty by percent.

    - Parameter `channel`: PWM channel; only `0` (GPIO3) or `1` (GPIO4) is supported.
    - Type of `channel`: int
    - Parameter `Duty cycle in percent. Range` (`percent:`): `0~100`.
    - Type of `percent`: int
    - Parameter ``True` selects inverted output polarity. Default` (`invert:`): `False`. Keyword-only parameter.
    - Type of `invert`: bool

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pwm_duty_percent(0, 50)
```
### `set_pwm_duty_u12(channel, duty_u12, *, invert=False)`

    Set a PWM channel duty by 12-bit code.

    - Parameter `channel`: PWM channel; only `0` (GPIO3) or `1` (GPIO4) is supported.
    - Type of `channel`: int
    - Parameter `Unsigned 12-bit duty code. Range` (`duty_u12:`): `0~4095`.
    - Type of `duty_u12`: int
    - Parameter ``True` selects inverted output polarity. Default` (`invert:`): `False`. Keyword-only parameter.
    - Type of `invert`: bool

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pwm_duty_u12(0, 2048)
```
### `enable_pwm(channel)`

    Enable a PWM output channel.

    - Parameter `channel`: PWM channel; only `0` (GPIO3) or `1` (GPIO4) is supported.
    - Type of `channel`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_pwm(0)
```
### `disable_pwm(channel)`

    Disable a PWM output channel.

    - Parameter `channel`: PWM channel; only `0` (GPIO3) or `1` (GPIO4) is supported.
    - Type of `channel`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_pwm(0)
```
### `get_pwm_duty_percent(channel)`

    Read a PWM channel duty by percent.

    - Parameter `channel`: PWM channel; only `0` (GPIO3) or `1` (GPIO4) is supported.
    - Type of `channel`: int

    - Returns: Duty percentage in the range `0~100`.
    - Return type: int

```python
value = stp2.get_pwm_duty_percent(0)
print(value)
```
### `get_pwm_duty_u12(channel)`

    Read a PWM channel duty by 12-bit code.

    - Parameter `channel`: PWM channel; only `0` (GPIO3) or `1` (GPIO4) is supported.
    - Type of `channel`: int

    - Returns: 12-bit duty value in the range `0~4095`.
    - Return type: int

```python
value = stp2.get_pwm_duty_u12(0)
print(value)
```
### `set_neopixel_count(count)`

    Set the active NeoPixel LED count.

    - Parameter `count`: Active LED count in the range `0~32`; `0` disables output.
    - Type of `count`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_neopixel_count(1)
```
### `set_neopixel_color(index, color)`

    Write one RGB888 color into LED RAM.

    - Parameter `index`: LED RAM index in the range `0~31`.
    - Type of `index`: int
    - Parameter `color`: `0xRRGGBB` or `(r, g, b)` with each component in `0~255`.
    - Type of `color`: int / tuple

    - Returns: No return value.
    - Return type: None

```python
stp2.set_neopixel_color(0, (32, 0, 0))
```
### `write_neopixels(colors, *, auto_refresh=True)`

    Write multiple RGB888 colors into LED RAM.

    - Parameter `colors`: Up to 32 RGB colors in integer or tuple form.
    - Type of `colors`: iterable
    - Parameter `Refresh the LED output after writing. Default` (`auto_refresh:`): `True`. Keyword-only parameter.
    - Type of `auto_refresh`: bool

    - Returns: No return value.
    - Return type: None

```python
stp2.write_neopixels([(32, 0, 0)])
```
### `refresh_neopixels()`

    Refresh NeoPixel output from LED RAM.

    - Returns: No return value.
    - Return type: None

```python
stp2.refresh_neopixels()
```
### `clear_neopixels(*, auto_refresh=True)`

    Clear LED RAM to black.

    - Parameter `Refresh the LED output after clearing. Default` (`auto_refresh:`): `True`. Keyword-only parameter.
    - Type of `auto_refresh`: bool

    - Returns: No return value.
    - Return type: None

```python
stp2.clear_neopixels()
```
### `enable_neopixels()`

    Enable NeoPixel output without changing LED RAM. After disable_neopixels(), the remembered count is cleared; enabling starts with one LED. Call set_neopixel_count() to select another count.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_neopixels()
```
### `disable_neopixels()`

    Disable NeoPixel output without clearing LED RAM.

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_neopixels()
```
### `set_aw8737a_pulse(gpio, pulses, *, refresh=True)`

    Configure AW8737A pulse output.

    - Parameter `gpio`: AW8737A mode-control GPIO in the range `0~4`.
    - Type of `gpio`: int
    - Parameter `pulses`: Pulse count in the range `0~255`.
    - Type of `pulses`: int
    - Parameter `Execute the configured pulse output immediately. Default` (`refresh:`): `True`. Keyword-only parameter.
    - Type of `refresh`: bool

    - Returns: No return value.
    - Return type: None

```python
stp2.set_aw8737a_pulse(4, 1)
```
### `refresh_aw8737a()`

    Execute the last configured AW8737A pulse output.

    - Returns: No return value.
    - Return type: None

```python
stp2.refresh_aw8737a()
```
### `set_aw8737a_mode(gpio, mode, *, refresh=True)`

    Set AW8737A gain mode.

    - Parameter `gpio`: AW8737A mode-control GPIO in the range `0~4`.
    - Type of `gpio`: int
    - Parameter `mode`: Gain mode in the range `0~3`, mapped directly to the pulse count.
    - Type of `mode`: int
    - Parameter `Execute the configured pulse output immediately. Default` (`refresh:`): `True`. Keyword-only parameter.
    - Type of `refresh`: bool

    - Returns: No return value.
    - Return type: None

```python
stp2.set_aw8737a_mode(4, 1)
```
### `get_irq_status(group, *, clear=False)`

    Read an IRQ status group.

    - Parameter `group`: IRQ group constant or corresponding string.
    - Type of `group`: int / str
    - Parameter `Clear the flags returned by this read. Default` (`clear:`): `False`. Keyword-only parameter.
    - Type of `clear`: bool

    - Returns: Status bit mask for the selected IRQ group.
    - Return type: int

```python
value = stp2.get_irq_status(StampTimerPower2.IRQ_GROUP_GPIO)
print(value)
```
### `clear_irq(group, mask=None)`

    Clear IRQ status bits.

    - Parameter `group`: IRQ group constant or corresponding string.
    - Type of `group`: int / str
    - Parameter `Group-local status bits to clear; `None` clears every valid bit in the group. Default` (`mask:`): `None`.
    - Type of `mask`: int / None

    - Returns: No return value.
    - Return type: None

```python
stp2.clear_irq(StampTimerPower2.IRQ_GROUP_GPIO)
```
### `disable_irq_events(group, events)`

    Mask IRQ bits.

    - Parameter `group`: IRQ group constant or corresponding string.
    - Type of `group`: int / str
    - Parameter `events`: Group-local event bit mask to disable.
    - Type of `events`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_irq_events(StampTimerPower2.IRQ_GROUP_GPIO, 0x10)
```
### `enable_irq_events(group, events)`

    Unmask IRQ bits.

    - Parameter `group`: IRQ group constant or corresponding string.
    - Type of `group`: int / str
    - Parameter `events`: Group-local event bit mask to enable.
    - Type of `events`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_irq_events(StampTimerPower2.IRQ_GROUP_GPIO, 0x10)
```
### `enable_pin_wakeup(gpio)`

    Enable GPIO wakeup.

    - Parameter `gpio`: Wake GPIO in the range `0~4`; GPIO1 does not support wakeup.
    - Type of `gpio`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_pin_wakeup(4)
```
### `disable_pin_wakeup(gpio)`

    Disable GPIO wakeup.

    - Parameter `gpio`: GPIO index in the range `0~4`.
    - Type of `gpio`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_pin_wakeup(4)
```
### `set_pin_wakeup_edge(gpio, edge)`

    Set GPIO wakeup edge.

    - Parameter `gpio`: Wake GPIO in the range `0~4`; GPIO1 does not support wakeup.
    - Type of `gpio`: int
    - Parameter `edge`: `WAKE_EDGE_FALLING` or `WAKE_EDGE_RISING`.
    - Type of `edge`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_pin_wakeup_edge(4, StampTimerPower2.WAKE_EDGE_FALLING)
```
### `enable_watchdog(timeout_s)`

    Set watchdog timeout.

    - Parameter `timeout_s`: Watchdog timeout in the range `1~255` seconds.
    - Type of `timeout_s`: int

    - Returns: No return value.
    - Return type: None

```python
# Manual power test only; affects the external STP2.
stp2.enable_watchdog(10)
```
### `disable_watchdog()`

    Disable the watchdog.

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_watchdog()
```
### `feed_watchdog()`

    Feed the watchdog.

    - Returns: No return value.
    - Return type: None

```python
stp2.feed_watchdog()
```
### `get_watchdog_countdown_s()`

    Read the watchdog countdown.

    - Returns: Remaining watchdog time in seconds.
    - Return type: int

```python
value = stp2.get_watchdog_countdown_s()
print(value)
```
### `set_timer(duration_s, action)`

    Set the PM1 timer and timeout action.

    - Parameter `duration_s`: Timer duration in seconds, range `0~2147483647`.
    - Type of `duration_s`: int
    - Parameter `action`: Timer action selected with a `TIMER_ACTION_*` constant.
    - Type of `action`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_timer(5, StampTimerPower2.TIMER_ACTION_FLAG)
```
### `clear_timer()`

    Stop and clear the PM1 timer.

    - Returns: No return value.
    - Return type: None

```python
stp2.clear_timer()
```
### `set_i2c_sleep_timeout_s(timeout_s)`

    Set PM1 I2C idle sleep timeout.

    - Parameter `timeout_s`: Idle sleep timeout in seconds, range `0~15`.
    - Type of `timeout_s`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_i2c_sleep_timeout_s(10)
```
### `get_i2c_sleep_timeout_s()`

    Read PM1 I2C idle sleep timeout.

    - Returns: Idle-sleep timeout in the range `0~15` seconds.
    - Return type: int

```python
value = stp2.get_i2c_sleep_timeout_s()
print(value)
```
### `set_i2c_frequency(frequency)`

    Set PM1 device-side I2C speed mode.

    - Parameter `frequency`: I2C frequency; only `100000` or `400000` Hz is supported.
    - Type of `frequency`: int

    - Returns: No return value.
    - Return type: None

```python
stp2.set_i2c_frequency(100000)
```
### `get_i2c_frequency()`

    Read the PM1 device-side I2C speed mode.

    - Returns: I2C frequency, either `100000` or `400000` Hz.
    - Return type: int

```python
value = stp2.get_i2c_frequency()
print(value)
```
### `read_rtc_ram(offset=0, length=32)`

    Read a region of the 32-byte RTC retention RAM. Retention depends on the module power conditions; this is not flash storage.

    - Parameter `Byte offset in the range 0~31; offset + length must not exceed 32. Default` (`offset:`): `0`.
    - Type of `offset`: int
    - Parameter `Number of bytes to read; `offset + length` must not exceed `32`. Default` (`length:`): `32`.
    - Type of `length`: int

    - Returns: Requested RTC RAM byte sequence.
    - Return type: bytes

```python
value = stp2.read_rtc_ram()
print(value)
```
### `write_rtc_ram(offset, data)`

    Write a region of the 32-byte RTC retention RAM. Retention depends on the module power conditions.

    - Parameter `offset`: Byte offset in the range 0~31; offset + len(data) must not exceed 32.
    - Type of `offset`: int
    - Parameter `data`: Bytes to write; `offset + len(data)` must not exceed `32`.
    - Type of `data`: buffer / iterable

    - Returns: No return value.
    - Return type: None

```python
original = stp2.read_rtc_ram(24, 2)
try:
    stp2.write_rtc_ram(24, bytes([0x55, 0xAA]))
finally:
    stp2.write_rtc_ram(24, original)
```
### `restore_defaults()`

    Restore writable StampTimerPower2 configuration to the documented defaults, including power, GPIO, wake, ADC, PWM, timer, IRQ, button, NeoPixel, and AW8737A settings, and clear sticky wake and IRQ status. Event callbacks are removed. Device information, UID, and the 32-byte RTC RAM are preserved, and the chip is not rebooted.

    The StampTimerPower2 I2C speed returns to 100 kHz. Configure the host I2C bus for the same speed before subsequent access. Existing `Pin`, `ADC`, `PWM`, and `NeoPixel` objects must be reinitialized before reuse.

    **Exceptions**

    `OSError` is raised on I2C failure; configuration may then be only partially restored.

    - Returns: No return value.
    - Return type: None

```python
# Manual power test only; affects the external STP2.
stp2.restore_defaults()
```
### `power_off()`

    Send a power-off command to the external StampTimerPower2. Basic remains powered by its own USB or battery supply.

    - Returns: No return value.
    - Return type: None

```python
# Manual power test only; affects the external STP2.
stp2.power_off()
```
### `reboot()`

    Reboot the external StampTimerPower2. Basic continues running; wait for the module to recover before further I2C access.

    - Returns: No return value.
    - Return type: None

```python
# Manual power test only; affects the external STP2.
stp2.reboot()
```
### `enter_download_mode()`

    Request PM1 download mode.

    - Returns: No return value.
    - Return type: None

```python
# Manual power test only; affects the external STP2.
stp2.enter_download_mode()
```
### `enable_download_lock()`

    Enable the PM1 download-mode lock.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_download_lock()
```
### `disable_download_lock()`

    Disable the PM1 download-mode lock.

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_download_lock()
```
### `enable_single_click_reset()`

    Enable single-click reset behavior.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_single_click_reset()
```
### `disable_single_click_reset()`

    Disable single-click reset behavior.

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_single_click_reset()
```
### `enable_double_click_power_off()`

    Enable double-click poweroff behavior.

    - Returns: No return value.
    - Return type: None

```python
stp2.enable_double_click_power_off()
```
### `disable_double_click_power_off()`

    Disable double-click poweroff behavior.

    - Returns: No return value.
    - Return type: None

```python
stp2.disable_double_click_power_off()
```
#### Pin object methods

Create this helper through `stp2.Pin()`. The following methods belong to the returned object, not the StampTimerPower2 instance.

### `init(mode=None, pull=-1, *, value=None)`

    Initialize or reconfigure the GPIO pin.

    - Parameter ``Pin.IN`, `Pin.OUT`, or `Pin.OPEN_DRAIN`; `None` preserves the current mode. Default` (`mode:`): `None`.
    - Type of `mode`: int / None
    - Parameter ``Pin.PULL_UP`, `Pin.PULL_DOWN`, or `None`; `-1` preserves the current setting. Default` (`pull:`): `-1`.
    - Type of `pull`: int / None
    - Parameter `Initial output level; `None` leaves the output latch unchanged. Default` (`value:`): `None`. Keyword-only parameter.
    - Type of `value`: int / bool / None

    - Returns: No return value.
    - Return type: None

```python
from hardware import Pin
pin = stp2.Pin(4, Pin.IN, pull=Pin.PULL_UP)
try:
    pin.init()
finally:
    pin.deinit()
```
### `deinit()`

    Restore a floating GPIO input and deactivate this object.

    - Returns: No return value.
    - Return type: None

```python
from hardware import Pin
pin = stp2.Pin(4, Pin.IN, pull=Pin.PULL_UP)
try:
    pin.deinit()
finally:
    pin.deinit()
```
### `value(value=None)`

    Read or write the GPIO value.

    - Parameter `Output level; `None` reads, while `0`, `1`, `False`, or `True` writes. Default` (`value:`): `None`.
    - Type of `value`: int / bool / None

    - Returns: `0` or `1` when reading; `None` when writing.
    - Return type: int / None

```python
from hardware import Pin
pin = stp2.Pin(4, Pin.IN, pull=Pin.PULL_UP)
try:
    value = pin.value()
    print(value)
finally:
    pin.deinit()
```
### `on()`

    Set the GPIO output high.

    - Returns: No return value.
    - Return type: None

```python
from hardware import Pin
pin = stp2.Pin(3, Pin.OUT, value=0)
try:
    pin.on()
finally:
    pin.deinit()
```
### `off()`

    Set the GPIO output low.

    - Returns: No return value.
    - Return type: None

```python
from hardware import Pin
pin = stp2.Pin(3, Pin.OUT, value=0)
try:
    pin.off()
finally:
    pin.deinit()
```
`pin()` reads the level and `pin(value)` writes it, as aliases for value(). Use `hardware.Pin.IN`, `OUT`, `OPEN_DRAIN`, `PULL_UP` and `PULL_DOWN` for the helper arguments.

#### ADC object methods

Create this helper through `stp2.ADC()`. The following methods belong to the returned object, not the StampTimerPower2 instance.

### `init()`

    Initialize or reinitialize the ADC input.

    - Returns: No return value.
    - Return type: None

```python
adc = stp2.ADC(1)
try:
    adc.init()
finally:
    adc.deinit()
```
### `deinit()`

    Release the ADC function and restore a floating GPIO input.

    - Returns: No return value.
    - Return type: None

```python
adc = stp2.ADC(1)
try:
    adc.deinit()
finally:
    adc.deinit()
```
### `read()`

    Read the native 12-bit ADC code.

    - Returns: Native 12-bit ADC code in the range `0~4095`.
    - Return type: int

```python
adc = stp2.ADC(1)
try:
    value = adc.read()
    print(value)
finally:
    adc.deinit()
```
### `read_u16()`

    Read a full-scale normalized unsigned 16-bit value.

    - Returns: Full-scale normalized value in the range `0~65535`.
    - Return type: int

```python
adc = stp2.ADC(1)
try:
    value = adc.read_u16()
    print(value)
finally:
    adc.deinit()
```
### `read_uv()`

    Read the ADC input voltage in microvolts.

    - Returns: ADC input voltage in microvolts.
    - Return type: int

```python
adc = stp2.ADC(1)
try:
    value = adc.read_uv()
    print(value)
finally:
    adc.deinit()
```
#### PWM object methods

Create this helper through `stp2.PWM()`. The following methods belong to the returned object, not the StampTimerPower2 instance.

### `init(*, freq=None, duty_u16=None, duty_ns=None, invert=None)`

    Initialize or reconfigure the PWM output.

    - Parameter `Shared frequency in the range `1~65535` Hz; `None` preserves it, falling back to 500 Hz when the frequency register is zero. Default` (`freq:`): `None`. Keyword-only parameter.
    - Type of `freq`: int / None
    - Parameter `Duty in the range `0~65535`; `None` preserves it. Default` (`duty_u16:`): `None`. Keyword-only parameter.
    - Type of `duty_u16`: int / None
    - Parameter `High pulse width in nanoseconds; mutually exclusive with `duty_u16`. Default` (`duty_ns:`): `None`. Keyword-only parameter.
    - Type of `duty_ns`: int / None
    - Parameter `Output polarity; `None` preserves it. Default` (`invert:`): `None`. Keyword-only parameter.
    - Type of `invert`: bool / None

    - Returns: No return value.
    - Return type: None

```python
pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
try:
    pwm.init()
finally:
    pwm.deinit()
```
### `deinit()`

    Disable PWM and restore its fixed pin as a floating input.

    - Returns: No return value.
    - Return type: None

```python
pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
try:
    pwm.deinit()
finally:
    pwm.deinit()
```
### `freq(value=None)`

    Read or set the shared PWM frequency.

    - Parameter `Shared frequency in the range `1~65535` Hz; `None` reads it. Default` (`value:`): `None`.
    - Type of `value`: int / None

    - Returns: Frequency in hertz when reading; `None` when setting.
    - Return type: int / None

```python
pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
try:
    value = pwm.freq()
    print(value)
finally:
    pwm.deinit()
```
### `duty_u16(value=None)`

    Read or set duty using the MicroPython unsigned 16-bit scale.

    - Parameter `Duty in the range `0~65535`; `None` reads it. Default` (`value:`): `None`.
    - Type of `value`: int / None

    - Returns: Duty in the range `0~65535` when reading; `None` when setting.
    - Return type: int / None

```python
pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
try:
    value = pwm.duty_u16()
    print(value)
finally:
    pwm.deinit()
```
### `duty_ns(value=None)`

    Read or set PWM pulse width in nanoseconds.

    - Parameter `High pulse width in nanoseconds; `None` reads it. The value cannot exceed the current PWM period. Default` (`value:`): `None`.
    - Type of `value`: int / None

    - Returns: High pulse width in nanoseconds when reading; `None` when setting.
    - Return type: int / None

```python
pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
try:
    value = pwm.duty_ns()
    print(value)
finally:
    pwm.deinit()
```
### `invert(value=None)`

    Read or set output invert.

    - Parameter ``True` selects inverted polarity, `False` selects normal polarity, and `None` reads it. Default` (`value:`): `None`.
    - Type of `value`: bool / None

    - Returns: Invert state when reading; `None` when setting.
    - Return type: bool / None

```python
pwm = stp2.PWM(0, freq=1000, duty_u16=32768)
try:
    value = pwm.invert()
    print(value)
finally:
    pwm.deinit()
```
Use duty_u16() or duty_ns(); this implementation does not provide duty(). Frequency is shared between both channels.

#### NeoPixel object methods

Create this helper through `stp2.NeoPixel()`. The following methods belong to the returned object, not the StampTimerPower2 instance.

### `init()`

    Initialize or reinitialize the fixed GPIO0 NeoPixel output.

    - Returns: No return value.
    - Return type: None

```python
pixels = stp2.NeoPixel(0, 1)
try:
    pixels.init()
finally:
    pixels.deinit()
```
### `deinit()`

    Clear LEDs, disable output, and restore GPIO0 as an input.

    - Returns: No return value.
    - Return type: None

```python
pixels = stp2.NeoPixel(0, 1)
try:
    pixels.deinit()
finally:
    pixels.deinit()
```
### `fill(color)`

    Fill the local buffer without writing the LEDs.

    - Parameter `color`: `0xRRGGBB` or `(r, g, b)` with each component in `0~255`.
    - Type of `color`: int / tuple

    - Returns: No return value.
    - Return type: None

```python
pixels = stp2.NeoPixel(0, 1)
try:
    pixels.fill((32, 0, 0))
    pixels.write()
finally:
    pixels.deinit()
```
### `write()`

    Convert the RGB buffer to RGB565 and refresh the LED output.

    - Returns: No return value.
    - Return type: None

```python
pixels = stp2.NeoPixel(0, 1)
try:
    pixels.fill((32, 0, 0))
    pixels.write()
finally:
    pixels.deinit()
```
`len(pixels)` returns the LED count. `pixels[index]` reads or writes an RGB tuple in the local buffer; call write() to display changes. Indices range from 0 to count-1, and RGB components from 0 to 255.

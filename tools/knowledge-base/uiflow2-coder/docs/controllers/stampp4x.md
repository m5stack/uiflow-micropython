# StampP4X

Support the following products:

    StampP4X

## MicroPython Example

#### ADC Input

This example reads the 16-bit ADC value from GPIO23 every 200 ms and prints the result to the serial console.

```python
import os, sys, io
import M5
from M5 import *
from hardware import ADC
from hardware import Pin
import time

adc23 = None

last_time = None

def setup():
    global adc23, last_time

    M5.begin()
    adc23 = ADC(Pin(23), atten=ADC.ATTN_11DB)
    last_time = time.ticks_ms()

def loop():
    global adc23, last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        print((str("ADC(pin23): ") + str((adc23.read_u16()))))

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

#### GPIO Output

This example toggles GPIO15 high and low once per second and prints the current output state to the serial console.

```python
import os, sys, io
import M5
from M5 import *
from hardware import Pin
import time

pin15 = None

last_time = None
enable = None

def setup():
    global pin15, last_time, enable

    M5.begin()
    pin15 = Pin(15, mode=Pin.OUT)
    last_time = time.ticks_ms()

def loop():
    global pin15, last_time, enable
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        enable = not enable
        if enable:
            print("set pin15 high")
            pin15.on()
        else:
            print("set pin15 low")
            pin15.off()

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

#### PWM Output

This example outputs a 20 kHz PWM signal on GPIO15. The duty value repeatedly ramps between 0 and 1023 and is printed to the serial console.

```python
import os, sys, io
import M5
from M5 import *
from hardware import PWM
from hardware import Pin
import time

pwm15 = None

duty = None
last_time = None
dir2 = None

def setup():
    global pwm15, duty, last_time, dir2

    M5.begin()
    pwm15 = PWM(Pin(15), freq=20000, duty=512)
    duty = 0
    dir2 = True
    last_time = time.ticks_ms()

def loop():
    global pwm15, duty, last_time, dir2
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 10:
        last_time = time.ticks_ms()
        duty = (duty if isinstance(duty, (int, float)) else 0) + 1
        if duty >= 1023:
            duty = 0
            dir2 = not dir2
        if dir2:
            pwm15.duty(duty)
            print((str("duty: ") + str(duty)))
        else:
            pwm15.duty((1023 - duty))
            print((str("duty: ") + str((1023 - duty))))

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

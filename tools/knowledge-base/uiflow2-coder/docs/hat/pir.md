# PIR Hat

Support the following products:

    PIR

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hat import PIRHat

label0 = None
hat_pir_0 = None

def hat_pir_0_active_event(pir):
    global label0, hat_pir_0
    label0.setText(str(hat_pir_0.get_status()))

def setup():
    global label0, hat_pir_0

    M5.begin()
    label0 = Widgets.Label("label0", 9, 15, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    hat_pir_0 = PIRHat((26, 0))
    hat_pir_0.set_callback(hat_pir_0_active_event, hat_pir_0.IRQ_ACTIVE)
    hat_pir_0.enable_irq()

def loop():
    global label0, hat_pir_0
    M5.update()

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

## class PIRHat

## Constructors

### `class PIRHat(port)`

    Create a PIRHat object.

    The parameters are:
        - `port` GPIO pin.

## Methods

### `PIRHat.get_status()`

    Get detection status.

### `PIRHat.enable_irq()`

   Enable Human detection function.

### `PIRHat.disable_irq()`

    Disable Human detection function.

### `PIRHat.set_callback()`

    Polling method, placed in the loop function, constantly check.

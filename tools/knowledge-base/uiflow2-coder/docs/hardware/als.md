# ALS

ALS is used to read the built-in ambient light sensor inside the host device.

The following are the details of the host's support for ALS:

                        ALS   |
     CoreS3           S     |
     CoreS3 SE                |

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *

title0 = None
label0 = None

def setup():
    global title0, label0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("CoreS3 Als", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Als:", 2, 104, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

def loop():
    global title0, label0
    M5.update()
    label0.setText(str((str("Als:") + str((M5.Als.getLightSensorData())))))

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

## class ALS

> Important: Methods of the ALS Class heavily rely on `M5.begin()`  and `M5.update()` .
>
> All calls to methods of ALS objects should be placed after `M5.begin()` , and `M5.update()`  should be called in the main loop.
## Methods

### `ALS.getLightSensorData() -> int`

    Read the ambient light sensor value built into the host device.

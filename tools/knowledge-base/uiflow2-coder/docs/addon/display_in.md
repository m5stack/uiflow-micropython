# addon DisplayIn

`DisplayIn` captures HDMI input from the Display In Add-on (U220) connected
to Unit PoE-P4 and saves a frame as a JPEG file. It initializes the LT6911
HDMI receiver when created and releases the capture resources with
`DisplayIn.deinit`.

The current capture format is `1280x720`. Connect an HDMI source before
calling `DisplayIn.capture`.

Support the following products:

    display_in

## MicroPython Example

#### HDMI input

This example captures one frame from the HDMI input and saves it as a JPEG file
in the device flash file system.

```python
import os, sys, io
import M5
from M5 import *
from addon import DisplayIn
import time

addon_display_in_0 = None

def setup():
    global addon_display_in_0

    M5.begin()
    addon_display_in_0 = DisplayIn()
    time.sleep(1)
    print(
        (
            str("saved /flash/lt6911_capture.jpg, ")
            + str(
                (str((addon_display_in_0.capture("/flash/capture.jpg", 75, 1000))) + str("bytes"))
            )
        )
    )

def loop():
    global addon_display_in_0
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

## **API**

#### DisplayIn

## `DisplayIn`
Capture HDMI input from the Display In Add-on (U220) as JPEG images.

`DisplayIn` initializes the LT6911 HDMI receiver. Call `capture`
to save one captured frame, then call `deinit` when capture is no
longer needed.

```python
from addon import DisplayIn

display_in = DisplayIn()
size = display_in.capture("/flash/capture.jpg", quality=75)
display_in.deinit()
```

### `capture`
Capture one HDMI frame and save it as a JPEG file.

- Parameter `path` (`str`): Destination JPEG file path.
- Parameter `quality` (`int`): JPEG quality from `1` to `100`. Default is `75`.
- Parameter `timeout_ms` (`int`): Maximum frame wait time in milliseconds. Default is `1000`.
- Returns: Number of bytes written to `path`.
- Return type: int

```python
size = display_in.capture("/flash/capture.jpg", quality=75)
```

### `deinit`
Release the Display In Add-on (U220) HDMI input resources.

```python
display_in.deinit()
```

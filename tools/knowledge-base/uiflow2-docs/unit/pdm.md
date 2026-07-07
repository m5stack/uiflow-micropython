<!-- .. _unit.PDMUnit: -->

# PDM Unit

<!-- .. sku: U089 -->

<!-- .. include:: ../refs/unit.pdm.ref -->

This is the driver library of PDM Unit, which is provides a set of methods to control the PDM microphone. Through the
I2S interface, the module can record audio data and save it as WAV files.

Support the following products:

    |PDM|

## UiFlow2 Example

#### record voice and play voice

Open the |pdm_cores3_example.m5f2| project in UiFlow2.

This example records voice and plays voice.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### record voice and play voice

This example records voice and plays voice.

MicroPython Code Block:

```python
import os, sys, io
import M5
from M5 import *
from unit import PDMUnit
import time

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
pdm_0 = None

rec_data = None

def setup():
    global title0, label0, label1, label2, label3, pdm_0, rec_data

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("PDMUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Is Start:", 20, 54, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Is Done:", 20, 119, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 131, 52, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 133, 121, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pdm_0 = PDMUnit((1, 2), i2s_port=2, sample_rate=44100)
    Speaker.begin()
    Speaker.setVolumePercentage(1)
    Speaker.end()
    pdm_0.begin()
    label2.setText(str("waiting..."))
    time.sleep(2)
    rec_data = bytearray(44100 * 15)
    pdm_0.record(rec_data, 44100, False)
    time.sleep_ms(150)
    while pdm_0.isRecording():
        label2.setText(str("recording..."))
        time.sleep_ms(100)
    pdm_0.end()
    label2.setText(str("ending..."))
    Speaker.begin()
    label3.setText(str("playing..."))
    Speaker.playRaw(rec_data, 44100)
    while Speaker.isPlaying():
        time.sleep_ms(150)
    label3.setText(str("done"))

def loop():
    global title0, label0, label1, label2, label3, pdm_0, rec_data
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

Example output:

    None

## **API**

#### PDMUnit

## PDMUnit
PDM Unit class.

:param list | tuple port: Connect to the PDM Unit.
:param int i2s_port: I2S port number(0 or 1, 2 is automatic select of available ports).
:param int sample_rate: Sample rate.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import PDMUnit

        pdm_0 = PDMUnit((1, 2), i2s_port=0, sample_rate=44100)

### `deinit`

    PDMUnit class inherits Mic class, See :ref:`hardware.Mic <hardware.Mic>` for more details.

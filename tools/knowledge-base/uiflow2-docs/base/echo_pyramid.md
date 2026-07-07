<!-- .. py:currentmodule:: base.echo_pyramid -->

# Atomic Echo Pyramid Base

<!-- .. sku: A167 -->

<!-- .. include:: ../refs/base.echo_pyramid.ref -->

The following products are supported:

    |Atomic Echo Pyramid Base|

Below is the detailed support for Atomic Echo Pyramid Base on the host:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### |Controller       | Atomic Echo Pyramid Base  |

###### | Atom Echo       | |O|                       |

###### | Atom Lite       | |S|                       |

###### | Atom Matrix     | |S|                       |

###### | AtomS3          | |S|                       |

###### | AtomS3 Lite     | |S|                       |

###### | AtomS3R         | |S|                       |

###### | AtomS3R-CAM     | |S|                       |

###### | AtomS3R-Ext     | |S|                       |

<!-- .. |S| unicode:: U+2705 -->
<!-- .. |O| unicode:: U+2B55 -->

The ``AtomicEchoPyramidBase`` class controls the Echo Pyramid base for Atom Series, providing audio playback/recording, touch input, and dual RGB LED strips.

<!-- .. note:: -->

    Power must be supplied to both the EchoPyramid base and the Atom controller.

## UiFlow2 Example

#### LED Strip Effects

Open the |atoms3r_echopyramid_led_strip_example.m5f2| project in UiFlow2.

This example demonstrates breathing and flowing effects on both RGB strips.

UiFlow2 Code Block:

Example output:

    None

#### Touch Control

Open the |atoms3r_echopyramid_touch_example.m5f2| project in UiFlow2.

This example uses the capacitive touch pads to light different LED segments.

UiFlow2 Code Block:

Example output:

    None

#### Audio Record And Playback

Open the |atoms3r_echopyramid_audio_example.m5f2| project in UiFlow2.

This example records a short WAV clip and then plays it back.

UiFlow2 Code Block:

Example output:

    None

#### Audio Beep

Open the |atoms3r_echopyramid_audio_beep_example.m5f2| project in UiFlow2.

This example plays a random beep tone on each touch.

UiFlow2 Code Block:

Example output:

    None

#### USB Voltage

Open the |atoms3r_echopyramid_usb_voltage_example.m5f2| project in UiFlow2.

This example reads USB input voltage (mV) from the base and displays it.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### LED Strip Effects

This example demonstrates breathing and flowing effects on both RGB strips.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from base import AtomicEchoPyramidBase
import time

label_title = None
label_mode = None
label_tip1 = None
label_tipe = None
i2c1 = None
base_echopyramid = None

mode = None
MODE_BRATH = None
MODE_FLOW = None
index = None
brightness = None
i = None
direction = None

# Describe this function...
def init(mode):
    global \
        MODE_BRATH, \
        MODE_FLOW, \
        index, \
        brightness, \
        i, \
        direction, \
        label_title, \
        label_mode, \
        label_tip1, \
        label_tipe, \
        i2c1, \
        base_echopyramid
    if mode == MODE_BRATH:
        print("mode: brathe")
        label_mode.setText(str("braeth"))
        label_mode.setCursor(x=32, y=40)
        for i in range(14):
            base_echopyramid.set_rgb_color(1, i, 0x33CCFF)
            base_echopyramid.set_rgb_color(2, i, 0x33CCFF)

        brightness = 0
        direction = True
    elif mode == MODE_FLOW:
        print("mode: flow")
        label_mode.setText(str("flow"))
        label_mode.setCursor(x=46, y=40)
        for i in range(14):
            base_echopyramid.set_rgb_color(1, i, 0x000000)
            base_echopyramid.set_rgb_color(2, i, 0x000000)

        base_echopyramid.set_rgb_brightness(1, 30, False)
        base_echopyramid.set_rgb_brightness(2, 30, False)

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_tip1, \
        label_tipe, \
        i2c1, \
        base_echopyramid, \
        mode, \
        MODE_BRATH, \
        MODE_FLOW, \
        index, \
        brightness, \
        direction, \
        i
    mode = (mode if isinstance(mode, (int, float)) else 0) + 1
    mode = mode % 2
    init(mode)

def setup():
    global \
        label_title, \
        label_mode, \
        label_tip1, \
        label_tipe, \
        i2c1, \
        base_echopyramid, \
        mode, \
        MODE_BRATH, \
        MODE_FLOW, \
        index, \
        brightness, \
        direction, \
        i

    M5.begin()
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "EchoPyramid", 1, 1, 1.0, 0x11CFE8, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_mode = Widgets.Label("breath", 32, 36, 1.0, 0xD41194, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip1 = Widgets.Label(
        "press display", 18, 88, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu12
    )
    label_tipe = Widgets.Label(
        "change mode", 16, 106, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu12
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)

    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echopyramid = AtomicEchoPyramidBase(
        i2c1, i2s_port=1, dev_addr=0x1A, sample_rate=16000, i2s_sck=6, i2s_ws=8, i2s_di=5, i2s_do=7
    )
    index = 0
    MODE_BRATH = 0
    MODE_FLOW = 1
    mode = MODE_BRATH
    brightness = 0
    init(mode)

def loop():
    global \
        label_title, \
        label_mode, \
        label_tip1, \
        label_tipe, \
        i2c1, \
        base_echopyramid, \
        mode, \
        MODE_BRATH, \
        MODE_FLOW, \
        index, \
        brightness, \
        direction, \
        i
    M5.update()
    if mode == MODE_BRATH:
        base_echopyramid.set_rgb_brightness(1, brightness, False)
        base_echopyramid.set_rgb_brightness(2, brightness, False)
        if direction:
            brightness = (brightness if isinstance(brightness, (int, float)) else 0) + 1
            if brightness > 50:
                direction = False
        else:
            brightness = (brightness if isinstance(brightness, (int, float)) else 0) + -1
            if brightness < 0:
                direction = True
        print((str("brightness: ") + str(brightness)))
        time.sleep_ms(50)
    elif mode == MODE_FLOW:
        if index > 0:
            base_echopyramid.set_rgb_color(1, index - 1, 0x000000)
            base_echopyramid.set_rgb_color(2, index - 1, 0x000000)
        if index == 14:
            index = 0
        base_echopyramid.set_rgb_color(1, index, 0x3333FF)
        base_echopyramid.set_rgb_color(2, index, 0x3333FF)
        index = (index if isinstance(index, (int, float)) else 0) + 1
        print((str("index： ") + str(index)))
        time.sleep_ms(50)

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

#### Touch Control

This example uses the capacitive touch pads to light different LED segments.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from base import AtomicEchoPyramidBase
import time

label0 = None
label1 = None
label2 = None
i2c1 = None
base_echopyramid = None
tp = None
tp_index = None
last_tp_time = None
strip_enable = None
time_diff = None
i = None

def setup():
    global \
        label0, \
        label1, \
        label2, \
        i2c1, \
        base_echopyramid, \
        tp, \
        last_tp_time, \
        strip_enable, \
        time_diff, \
        tp_index, \
        i

    M5.begin()
    Widgets.fillScreen(0x000000)
    label0 = Widgets.Label("EchoPyramid", 1, 2, 1.0, 0x12C7DE, 0x000000, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Touch", 36, 47, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Control", 29, 75, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echopyramid = AtomicEchoPyramidBase(
        i2c1, i2s_port=1, dev_addr=0x1A, sample_rate=16000, i2s_sck=6, i2s_ws=8, i2s_di=5, i2s_do=7
    )
    base_echopyramid.set_rgb_color(1, 2, 56789)
    last_tp_time = [0, 0, 0, 0]
    strip_enable = [False, False, False, False]

def loop():
    global \
        label0, \
        label1, \
        label2, \
        i2c1, \
        base_echopyramid, \
        tp, \
        last_tp_time, \
        strip_enable, \
        time_diff, \
        tp_index, \
        i
    M5.update()
    tp = base_echopyramid.get_touch()
    print((str("TP: ") + str(tp)))
    for tp_index in range(1, 5):
        if tp[int(tp_index - 1)]:
            if tp_index == 1:
                for i in range(7):
                    base_echopyramid.set_rgb_color(1, 7 + i, 0x00CCCC)

            elif tp_index == 2:
                for i in range(7):
                    base_echopyramid.set_rgb_color(1, i, 0x00CCCC)

            elif tp_index == 3:
                for i in range(7):
                    base_echopyramid.set_rgb_color(2, i, 0x00CCCC)

            elif tp_index == 4:
                for i in range(7):
                    base_echopyramid.set_rgb_color(2, 7 + i, 0x00CCCC)

            last_tp_time[int(tp_index - 1)] = time.ticks_ms()
            strip_enable[int(tp_index - 1)] = True
        else:
            time_diff = time.ticks_diff((time.ticks_ms()), (last_tp_time[int(tp_index - 1)]))
            if time_diff > 500 and strip_enable[int(tp_index - 1)]:
                strip_enable[int(tp_index - 1)] = False
                if tp_index == 1:
                    for i in range(7):
                        base_echopyramid.set_rgb_color(1, 7 + i, 0x000000)

                elif tp_index == 2:
                    for i in range(7):
                        base_echopyramid.set_rgb_color(1, i, 0x000000)

                elif tp_index == 3:
                    for i in range(7):
                        base_echopyramid.set_rgb_color(2, i, 0x000000)

                elif tp_index == 4:
                    for i in range(7):
                        base_echopyramid.set_rgb_color(2, 7 + i, 0x000000)

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

#### Audio Record And Playback

This example records a short WAV clip and then plays it back.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from base import AtomicEchoPyramidBase
import time

label_title = None
label_state = None
label_tip1 = None
label_tip2 = None
i2c1 = None
base_echopyramid = None
record = None
playing = None
record_file_path = None
record_time_ms = None
play_start_time = None
RECORD_DURATION = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_state, \
        label_tip1, \
        label_tip2, \
        i2c1, \
        base_echopyramid, \
        record, \
        playing, \
        RECORD_DURATION, \
        record_file_path, \
        record_time_ms, \
        play_start_time
    if not playing:
        record = True

def setup():
    global \
        label_title, \
        label_state, \
        label_tip1, \
        label_tip2, \
        i2c1, \
        base_echopyramid, \
        record, \
        playing, \
        RECORD_DURATION, \
        record_file_path, \
        record_time_ms, \
        play_start_time

    M5.begin()
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("Audio", 36, 0, 1.0, 0x2293CB, 0x000000, Widgets.FONTS.DejaVu18)
    label_state = Widgets.Label("Idle", 46, 28, 1.0, 0xDED413, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip1 = Widgets.Label(
        "press display", 1, 83, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_tip2 = Widgets.Label(
        "start record", 8, 103, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)

    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echopyramid = AtomicEchoPyramidBase(
        i2c1, i2s_port=1, dev_addr=0x1A, sample_rate=16000, i2s_sck=6, i2s_ws=8, i2s_di=5, i2s_do=7
    )
    RECORD_DURATION = 0
    record_file_path = "test.wav"
    record_time_ms = 5000
    base_echopyramid.set_volume(60)

def loop():
    global \
        label_title, \
        label_state, \
        label_tip1, \
        label_tip2, \
        i2c1, \
        base_echopyramid, \
        record, \
        playing, \
        RECORD_DURATION, \
        record_file_path, \
        record_time_ms, \
        play_start_time
    M5.update()
    if record:
        record = False
        print("start record")
        label_tip1.setVisible(False)
        label_tip2.setVisible(False)
        label_state.setText(str("Recording..."))
        label_state.setCursor(x=6, y=28)
        label_state.setColor(0xFF0000, 0x000000)
        base_echopyramid.record_wav_file(
            "/flash/res/audio/test.wav",
            rate=16000,
            bits=16,
            channel=AtomicEchoPyramidBase.STEREO,
            duration=record_time_ms,
        )
        print("start play")
        label_state.setText(str("Playing..."))
        label_state.setCursor(x=21, y=28)
        label_state.setColor(0x33CC00, 0x000000)
        base_echopyramid.play_wav_file("/flash/res/audio/" + str(record_file_path))
        playing = True
        play_start_time = time.ticks_ms()
    if playing:
        if (time.ticks_diff((time.ticks_ms()), play_start_time)) > record_time_ms:
            playing = False
            print("play finished")
            label_state.setText(str("Idle"))
            label_state.setCursor(x=46, y=28)
            label_state.setColor(0xFFFF00, 0x000000)
            label_tip1.setVisible(True)
            label_tip2.setVisible(True)

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

#### Audio Beep

This example plays a random beep tone on each touch.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from base import AtomicEchoPyramidBase
import random

label_title = None
label_tip1 = None
label_freq = None
label_tip2 = None
i2c1 = None
base_echopyramid = None
beep = None
freq = None

def btna_was_eclicked_event(state):
    global label_title, label_tip1, label_freq, label_tip2, i2c1, base_echopyramid, beep, freq
    beep = True

def setup():
    global label_title, label_tip1, label_freq, label_tip2, i2c1, base_echopyramid, beep, freq

    M5.begin()
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Audio Play", 13, 2, 1.0, 0x0EE9EE, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_tip1 = Widgets.Label(
        "press display", 1, 83, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_freq = Widgets.Label(
        "Freq: -- Hz", 15, 41, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_tip2 = Widgets.Label("beep", 39, 103, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_eclicked_event)

    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echopyramid = AtomicEchoPyramidBase(
        i2c1, i2s_port=1, dev_addr=0x1A, sample_rate=16000, i2s_sck=6, i2s_ws=8, i2s_di=5, i2s_do=7
    )
    base_echopyramid.set_volume(50)

def loop():
    global label_title, label_tip1, label_freq, label_tip2, i2c1, base_echopyramid, beep, freq
    M5.update()
    if beep:
        beep = False
        freq = random.randint(500, 3500)
        if freq >= 1000:
            label_freq.setCursor(x=0, y=41)
            label_freq.setText(str((str("Freq:") + str((str(freq) + str("Hz"))))))
        else:
            label_freq.setCursor(x=9, y=41)
            label_freq.setText(str((str("Freq:") + str((str(freq) + str("Hz"))))))
        base_echopyramid.tone(freq, 200)

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

#### USB Voltage

This example reads USB input voltage (mV) from the base and displays it.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time
import M5
from M5 import *
from base import AtomicEchoPyramidBase
from hardware import Pin
from hardware import I2C

label_title = None
label_voltage = None
label_unit = None
label_value = None
i2c1 = None
base_echopyramid = None
last_time = None
voltage = None

def setup():
    global \
        label_title, \
        label_voltage, \
        label_unit, \
        label_value, \
        i2c1, \
        base_echopyramid, \
        last_time, \
        voltage

    M5.begin()
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "EchoPyramid", 1, 1, 1.0, 0x12C4E6, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_voltage = Widgets.Label(
        "USB Volatge", 5, 31, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_unit = Widgets.Label("mV", 47, 105, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_value = Widgets.Label("5000", 31, 66, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24)

    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echopyramid = AtomicEchoPyramidBase(
        i2c1, i2s_port=1, dev_addr=0x1A, sample_rate=16000, i2s_sck=6, i2s_ws=8, i2s_di=5, i2s_do=7
    )

def loop():
    global \
        label_title, \
        label_voltage, \
        label_unit, \
        label_value, \
        i2c1, \
        base_echopyramid, \
        last_time, \
        voltage
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        voltage = base_echopyramid.get_input_voltage()
        if voltage >= 5000:
            label_value.setColor(0x33CC00, 0x000000)
        else:
            label_value.setColor(0xFF0000, 0x000000)
        label_value.setText(str(voltage))

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

## API

#### AtomicEchoPyramidBase

## AtomicEchoPyramidBase
Echo Pyramid base for AtomS3R + Echo Pyramid.

:param i2c: I2C bus.
:param int dev_addr: STM32 I2C address. Default 0x1A.
:param int es8311_addr: ES8311 I2C address. Default 0x18.
:param int i2s_port: I2S port number. Default 1.
:param int sample_rate: Sample rate. Default 24000.
:param int i2s_sck: I2S BCLK pin. Default 6.
:param int i2s_ws: I2S WS pin. Default 8.
:param int i2s_di: I2S DIN (mic) pin. Default 5.
:param int i2s_do: I2S DOUT (spk) pin. Default 7.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from hardware import I2C, Pin
        from base import AtomicEchoPyramidBase

        i2c = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
        echo_pyramid = AtomicEchoPyramidBase(i2c, dev_addr=0x1A, i2s_sck=6, i2s_ws=8, i2s_di=5, i2s_do=7)
        echo_pyramid.speaker.tone(2000, 500)

### `get_touch`
Get touch status.

:return: (tp1, tp2, tp3, tp4), True=pressed False=released.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        tp1, tp2, tp3, tp4 = echo_pyramid.get_touch()

### `set_rgb_brightness`
Set RGB strip brightness.

:param int strip: Strip index (1 or 2).
:param int brightness: Brightness 0~100.
:param bool save: Save to flash.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.set_rgb_brightness(1, 50, False)

### `get_rgb_brightness`
Get RGB strip brightness.

:param int strip: Strip index (1 or 2).
:return: Brightness 0~100, or 0 on error/invalid strip.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        brightness = echo_pyramid.get_rgb_brightness(1)

### `set_rgb_color`
Set single RGB LED color.

:param int strip: Strip index (1 or 2).
:param int index: LED index 0~13.
:param int color: 24-bit color (R << 16 | G << 8 | B).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.set_rgb_color(1, 0, 0x33CCFF)

### `get_rgb_color`
Get single RGB LED color.

:param int strip: Strip index (1 or 2).
:param int index: LED index 0~13.
:return: 24-bit color (R << 16 | G << 8 | B), or 0 on error.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        color = echo_pyramid.get_rgb_color(1, 0)

### `set_addr`
Set STM32 I2C address. Takes effect after a short delay.

:param int new_addr: New address 0x08~0x77.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.set_addr(0x1B)

### `get_addr`
Get current STM32 I2C address.

:return: I2C address, or 0 on error.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        addr = echo_pyramid.get_addr()

### `get_firmware_version`
Get STM32 firmware version.

:return: Version number, or 0 on error.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        ver = echo_pyramid.get_firmware_version()

### `get_input_voltage`
Get input voltage (from STM32 ADC).

:return: Voltage in mV, or 0 on error.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mv = echo_pyramid.get_input_voltage()

### `set_mute`
Mute or unmute speaker (AW87559).

:param bool mute: True to mute, False to unmute.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.set_mute(True)

### `change_sample_rate`
Change audio sample rate. Affects playback and recording.

:param int sample_rate: Sample rate in Hz (e.g. 16000, 24000).

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.change_sample_rate(24000)

### `play_wav_file`
Play a WAV file from storage.

:param str file: WAV file path.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.play_wav_file("/flash/res/audio/test.wav")

### `tone`
Play a beep tone.

:param int freq: Frequency in Hz.
:param int duration: Duration in milliseconds.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.tone(1000, 200)

### `play_wav`
Play WAV data from buffer.

:param bytes buf: WAV data.
:param int duration: Duration in ms, or -1 for full buffer.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.play_wav(wav_bytes, duration=1000)

### `play_raw`
Play raw PCM data.

:param bytes buf: Raw PCM data.
:param int rate: Sample rate in Hz.
:param int bits: Bit depth (e.g. 16).
:param int channel: Number of channels (1 or 2).
:param int duration: Duration in ms, or -1 for full buffer.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.play_raw(pcm_bytes, rate=16000, bits=16, channel=2)

### `pause`
Pause playback.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.pause()

### `resume`
Resume playback.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.resume()

### `stop`
Stop playback.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.stop()

### `get_volume`
Get speaker volume.

:return: Current volume value.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        volume = echo_pyramid.get_volume()

### `set_volume`
Set speaker volume.

:param int volume: Volume value.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.set_volume(60)

### `record_wav_file`
Record audio to a WAV file.

:param str path: Output file path.
:param int rate: Sample rate in Hz.
:param int bits: Bit depth.
:param int channel: Channel mode. Use ``MONO`` or ``STEREO``.
:param int duration: Duration in milliseconds.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.record_wav_file("/flash/res/audio/test.wav", rate=16000, bits=16, channel=echo_pyramid.STEREO, duration=3000)

### `record`
Record audio to PCM buffer.

:param int rate: Sample rate in Hz.
:param int bits: Bit depth.
:param int channel: Number of channels.
:param int duration: Duration in milliseconds.
:return: Record result (implementation-dependent).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        buf = echo_pyramid.record(rate=16000, bits=16, channel=2, duration=3000)

### `pcm_buffer`
PCM buffer from the microphone (read-only). Available after recording.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        data = echo_pyramid.pcm_buffer

### `deinit`
Deinitialize speaker and microphone, and mute output.

MicroPython Code Block:

    .. code-block:: python

        echo_pyramid.deinit()

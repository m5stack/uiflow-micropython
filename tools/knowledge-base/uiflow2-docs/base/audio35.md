# Atomic Audio-3.5 Base

<!-- .. sku: A166 -->

<!-- .. include:: ../refs/base.audio35.ref -->

The following products are supported:

    |Atomic Audio-3.5 Base|

Below is the detailed support for Atomic Audio-3.5 Base on the host:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### |Controller       | Atomic Audio-3.5 Base  |

###### | Atom Echo       | |O|                    |

###### | Atom Lite       | |S|                    |

###### | Atom Matrix     | |S|                    |

###### | AtomS3          | |S|                    |

###### | AtomS3 Lite     | |S|                    |

###### | AtomS3R         | |S|                    |

###### | AtomS3R-CAM     | |S|                    |

###### | AtomS3R-Ext     | |S|                    |

<!-- .. |S| unicode:: U+2705 -->
<!-- .. |O| unicode:: U+2B55 -->

<!-- .. note:: -->
    Atomic Audio-3.5 Base uses the same Audio CODEC and pin connections as Atomic Echo Base. For detailed usage instructions, please refer to the `Atomic Echo Base <echo.html>`_ documentation.

## UiFlow2 Example

#### Record and play WAV file

Open the |atoms3r_aduio_record_play_example.m5f2| project in UiFlow2.

This example initializes Atomic Audio-3.5 Base, records stereo audio to ``/flash/res/audio/test.wav`` for 5 seconds after pressing BtnA, and then plays the recorded WAV file.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Record and play WAV file

This example initializes Atomic Audio-3.5 Base, records stereo audio to ``/flash/res/audio/test.wav`` for 5 seconds after pressing BtnA, and then plays the recorded WAV file.

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
from base import AtomicAudio35Base
import time

label_title = None
label_status = None
label_tip2 = None
label_tip1 = None
label_remaining = None
i2c0 = None
base_audio35 = None
record = None
playing = None
reaming = None
RECORD_TIME_MS = None
play_start_time = None

def btna_was_click_event(state):
    global label_title, label_status, label_tip2, label_tip1, label_remaining, i2c0, base_audio35, record, playing, reaming, RECORD_TIME_MS, play_start_time
    record = True

def setup():
    global label_title, label_status, label_tip2, label_tip1, label_remaining, i2c0, base_audio35, record, playing, reaming, RECORD_TIME_MS, play_start_time

    M5.begin()
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label("Audio", 36, 4, 1.0, 0x18c3df, 0x000000, Widgets.FONTS.DejaVu18)
    label_status = Widgets.Label("--", 57, 30, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip2 = Widgets.Label("start record", 8, 104, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
    label_tip1 = Widgets.Label("press screen", 5, 82, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu18)
    label_remaining = Widgets.Label("-", 59, 54, 1.0, 0xffffff, 0x000000, Widgets.FONTS.DejaVu24)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_click_event)

    i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=400000)
    base_audio35 = AtomicAudio35Base(i2c0, 0x18, 1, 16000, 8, 6, 7, 5)
    base_audio35.set_volume(60)
    base_audio35.tone(888, 100)
    record = False
    RECORD_TIME_MS = 5000
    label_status.setVisible(False)
    label_remaining.setVisible(False)

def loop():
    global label_title, label_status, label_tip2, label_tip1, label_remaining, i2c0, base_audio35, record, playing, reaming, RECORD_TIME_MS, play_start_time
    M5.update()
    if record:
        record = False
        time.sleep_ms(200)
        label_status.setVisible(True)
        label_tip1.setVisible(False)
        label_tip2.setVisible(False)
        label_status.setText(str('Recording...'))
        label_status.setColor(0xcc0000, 0x000000)
        label_status.setCursor(x=3, y=45)
        base_audio35.record_wav_file('/flash/res/audio/test.wav', rate=16000, bits=16, channel=AtomicAudio35Base.STEREO, duration=RECORD_TIME_MS)
        label_status.setText(str('Playing...'))
        label_status.setColor(0x009900, 0x000000)
        label_status.setCursor(x=16, y=27)
        play_start_time = time.ticks_ms()
        playing = True
        label_remaining.setCursor(x=52, y=70)
        label_remaining.setVisible(True)
        base_audio35.play_wav_file('/flash/res/audio/test.wav')
    if playing:
        reaming = RECORD_TIME_MS - (time.ticks_diff((time.ticks_ms()), play_start_time))
        label_remaining.setText(str(int(reaming / 1000)))
        if (time.ticks_diff((time.ticks_ms()), play_start_time)) >= RECORD_TIME_MS:
            playing = False
            label_remaining.setVisible(False)
            label_status.setVisible(False)
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

## **API**

#### class AtomicAudio35Base

## AtomicAudio35Base
<!-- Failed to find class AtomicAudio35Base in /tmp/mr462_split/m5stack/libs/base/audio35.py -->

``AtomicAudio35Base`` is an alias for ``AtomicEchoBase``. Please refer to the `AtomicEchoBase <echo.html#base.echo.AtomicEchoBase>`_ class for detailed documentation.

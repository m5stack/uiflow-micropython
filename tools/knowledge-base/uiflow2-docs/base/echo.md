# Atomic Echo Base

<!-- .. sku: A149 -->

<!-- .. include:: ../refs/base.echo.ref -->

The following products are supported:

    |Atomic Echo Base|

Below is the detailed support for Atomic Echo Base on the host:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### |Controller       | Atomic Echo Base  |

###### | Atom Echo       | |O|               |

###### | Atom Lite       | |S|               |

###### | Atom Matrix     | |S|               |

###### | AtomS3          | |S|               |

###### | AtomS3 Lite     | |S|               |

###### | AtomS3R         | |S|               |

###### | AtomS3R-CAM     | |S|               |

###### | AtomS3R-Ext     | |S|               |

<!-- .. |S| unicode:: U+2705 -->
<!-- .. |O| unicode:: U+2B55 -->

## UiFlow2 Example

#### Play WAV file

Open the |atoms3_play_wav_example.m5f2| project in UiFlow2.

<!-- .. only:: builder_html -->

    :download:`66.wav <../../../examples/module/audio/66.wav>`

This example reads an audio file from the file system and plays it.

UiFlow2 Code Block:

Example output:

    None

#### Playback Controls

Open the |atoms3_playback_controls_example.m5f2| project in UiFlow2.

<!-- .. only:: builder_html -->

    :download:`66.wav <../../../examples/module/audio/66.wav>`

This example demonstrates how to control playback using the AtomicEchoBase class.

Play the audio for 1 second, pause for 1 second, and then resume playing.

UiFlow2 Code Block:

Example output:

    None

#### Record Audio

Open the |atoms3_record_audio_example.m5f2| project in UiFlow2.

This example records audio from the microphone and saves it to a PCM buffer, then plays it out through the speaker.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Play WAV file

This example reads an audio file from the file system and plays it.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from base import AtomicEchoBase
import time

i2c1 = None
base_echo = None

def setup():
    global i2c1, base_echo

    M5.begin()
    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echo = AtomicEchoBase(i2c1, 0x18, 1, 16000, 8, 6, 7, 5)
    base_echo.play_wav_file("/flash/res/audio/66.wav")
    time.sleep(1)
    base_echo.pause()
    time.sleep(1)
    base_echo.resume()

def loop():
    global i2c1, base_echo
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

#### Playback Controls

This example demonstrates how to control playback using the AtomicEchoBase class.

Play the audio for 1 second, pause for 1 second, and then resume playing.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from base import AtomicEchoBase
import time

i2c1 = None
base_echo = None

def setup():
    global i2c1, base_echo

    M5.begin()
    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echo = AtomicEchoBase(i2c1, 0x18, 1, 16000, 8, 6, 7, 5)
    base_echo.play_wav_file("/flash/res/audio/66.wav")
    time.sleep(1)
    base_echo.pause()
    time.sleep(1)
    base_echo.resume()

def loop():
    global i2c1, base_echo
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

#### Record Audio

This example records audio from the microphone and saves it to a PCM buffer, then plays it out through the speaker.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from base import AtomicEchoBase

i2c1 = None
base_echo = None

def setup():
    global i2c1, base_echo

    M5.begin()
    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echo = AtomicEchoBase(i2c1, 0x18, 1, 16000, 8, 6, 7, 5)
    base_echo.record(rate=16000, bits=16, channel=AtomicEchoBase.STEREO, duration=500)
    base_echo.play_raw(
        base_echo.pcm_buffer, rate=16000, bits=16, channel=AtomicEchoBase.STEREO, duration=-1
    )

def loop():
    global i2c1, base_echo
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

#### AtomicEchoBase

## AtomicEchoBase
Create an AtomicEchoBase object.

:param I2C i2c: I2C object
:param int address: The I2C address of the ES8311. Default is 0x18.
:param int i2s_port: The I2S port number. Default is 1.
:param int sample_rate: The sample rate of the audio. Default is 16000.
:param int i2s_sck: The I2S SCK pin. Default is -1.
:param int i2s_ws: The I2S WS pin. Default is -1.
:param int i2s_di: The I2S DI pin. Default is -1.
:param int i2s_do: The I2S DO pin. Default is -1.

UIFLOW2:

Micropython::

    from hardware import I2C
    from hardware import Pin
    from base import AtomicEchoBase

    # atom echo
    i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
    base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

    # atom lite
    i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
    base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

    # atom matrix
    i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
    base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

    # atoms3 / atoms3 lite
    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=8, i2s_ws=6, i2s_di=7, i2s_do=5)

    # atoms3r / atoms3r-cam / atoms3-ext
    i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
    base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=8, i2s_ws=6, i2s_di=7, i2s_do=5)

    base_echo.speaker.tone(2000, 1000)
    base_echo.speaker.playWavFile('res/audio/66.wav')

### `pi4ioe_init`

### `set_mute`

### `change_sample_rate`

### `play_wav_file`
Play a WAV file.

:param str file: The path of the WAV file to play.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.play_wav_file("/flash/res/audio/test.wav")

### `tone`
Play simple tone sound.

:param int freq: Frequency of the tone in Hz.
:param int duration: Duration of the tone in milliseconds.
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.tone(2000, 50)

### `play_wav`
Play a WAV buffer.

:param bytes buf: The WAV buffer to play.
:param int duration: Duration of the WAV buffer in milliseconds. when duration is -1, it will play until stopped. (default is -1).
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.play_wav(wav_buffer, duration=1000)

### `play_raw`
Play a pcm buffer.

:param bytes buf: The PCM buffer to play.
:param int rate: Sample rate (default is 16000).
:param int bits: Bit depth (default is 16).
:param int channel: Number of channels (default is 2).
:param int duration: Duration of the PCM buffer in milliseconds. when duration is -1, it will play until stopped. (default is -1).
:return: None

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.play_raw(pcm_buffer, rate=16000, bits=16, channel=2, duration=1000)

### `pause`
Pause the playback.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio.tone(2000, 100)
        time.sleep(0.05)
        base_echo.pause()
        time.sleep(0.05)
        base_echo.resume()

### `resume`
Resume the playback.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio.tone(2000, 100)
        time.sleep(0.05)
        base_echo.pause()
        time.sleep(0.05)
        base_echo.resume()

### `stop`
Stop the playback.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio.tone(2000, 100)
        time.sleep(0.05)
        base_echo.stop()

### `get_volume`
Get the speaker volume level.

:return: The volume level (0-100).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.get_volume()

### `set_volume`
Set the speaker volume level.

:param int volume: The volume level (0-100).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.set_volume(50)

### `record_wav_file`
Record audio to a WAV file.

:param str path: The path to save the WAV file.
:param int rate: Sample rate (default is 16000).
:param int bits: Bit depth (default is 16).
:param int channel: Number of channels (default is 2).
:param int duration: Duration of the recording in milliseconds (default is 3000).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.record_wav_file("/flash/res/audio/test.wav", rate=16000, bits=16, channel=2, duration=3000)

### `record`
Record audio to a PCM buffer.

:param int rate: Sample rate (default is 16000).
:param int bits: Bit depth (default is 16).
:param int channel: Number of channels (default is 2).
:param int duration: Duration of the recording in milliseconds (default is 3000).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.record(rate=16000, bits=16, channel=2, duration=3000)

### `pcm_buffer`
Get the PCM buffer.

:return: The PCM buffer.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_echo.pcm_buffer

### `deinit`

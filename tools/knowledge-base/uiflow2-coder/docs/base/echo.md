# Atomic Echo Base

The following products are supported:

    Atomic Echo Base

Below is the detailed support for Atomic Echo Base on the host:

    Controller        Atomic Echo Base  |
     Atom Echo        O               |
     Atom Lite        S               |
     Atom Matrix      S               |
     AtomS3           S               |
     AtomS3 Lite      S               |
     AtomS3R          S               |
     AtomS3R-CAM      S               |
     AtomS3R-Ext      S               |

## MicroPython Example

#### Play WAV file

This example reads an audio file from the file system and plays it.

```python
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

#### Playback Controls

This example demonstrates how to control playback using the AtomicEchoBase class.

Play the audio for 1 second, pause for 1 second, and then resume playing.

```python
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

#### Record Audio

This example records audio from the microphone and saves it to a PCM buffer, then plays it out through the speaker.

```python
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

#### AtomicEchoBase

## `AtomicEchoBase`
Create an AtomicEchoBase object.

- Parameter `i2c` (`I2C`): I2C object
- Parameter `address` (`int`): The I2C address of the ES8311. Default is 0x18.
- Parameter `i2s_port` (`int`): The I2S port number. Default is 1.
- Parameter `sample_rate` (`int`): The sample rate of the audio. Default is 16000.
- Parameter `i2s_sck` (`int`): The I2S SCK pin. Default is -1.
- Parameter `i2s_ws` (`int`): The I2S WS pin. Default is -1.
- Parameter `i2s_di` (`int`): The I2S DI pin. Default is -1.
- Parameter `i2s_do` (`int`): The I2S DO pin. Default is -1.

```python
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
```

### `pi4ioe_init`

### `set_mute`

### `change_sample_rate`

### `play_wav_file`
Play a WAV file.

- Parameter `file` (`str`): The path of the WAV file to play.
- Returns: None

```python
base_echo.play_wav_file("/flash/res/audio/test.wav")
```

### `tone`
Play simple tone sound.

- Parameter `freq` (`int`): Frequency of the tone in Hz.
- Parameter `duration` (`int`): Duration of the tone in milliseconds.
- Returns: None

```python
base_echo.tone(2000, 50)
```

### `play_wav`
Play a WAV buffer.

- Parameter `buf` (`bytes`): The WAV buffer to play.
- Parameter `duration` (`int`): Duration of the WAV buffer in milliseconds. when duration is -1, it will play until stopped. (default is -1).
- Returns: None

```python
base_echo.play_wav(wav_buffer, duration=1000)
```

### `play_raw`
Play a pcm buffer.

- Parameter `buf` (`bytes`): The PCM buffer to play.
- Parameter `rate` (`int`): Sample rate (default is 16000).
- Parameter `bits` (`int`): Bit depth (default is 16).
- Parameter `channel` (`int`): Number of channels (default is 2).
- Parameter `duration` (`int`): Duration of the PCM buffer in milliseconds. when duration is -1, it will play until stopped. (default is -1).
- Returns: None

```python
base_echo.play_raw(pcm_buffer, rate=16000, bits=16, channel=2, duration=1000)
```

### `pause`
Pause the playback.

```python
audio.tone(2000, 100)
time.sleep(0.05)
base_echo.pause()
time.sleep(0.05)
base_echo.resume()
```

### `resume`
Resume the playback.

```python
audio.tone(2000, 100)
time.sleep(0.05)
base_echo.pause()
time.sleep(0.05)
base_echo.resume()
```

### `stop`
Stop the playback.

```python
audio.tone(2000, 100)
time.sleep(0.05)
base_echo.stop()
```

### `get_volume`
Get the speaker volume level.

- Returns: The volume level (0-100).

```python
base_echo.get_volume()
```

### `set_volume`
Set the speaker volume level.

- Parameter `volume` (`int`): The volume level (0-100).

```python
base_echo.set_volume(50)
```

### `record_wav_file`
Record audio to a WAV file.

- Parameter `path` (`str`): The path to save the WAV file.
- Parameter `rate` (`int`): Sample rate (default is 16000).
- Parameter `bits` (`int`): Bit depth (default is 16).
- Parameter `channel` (`int`): Number of channels (default is 2).
- Parameter `duration` (`int`): Duration of the recording in milliseconds (default is 3000).

```python
base_echo.record_wav_file("/flash/res/audio/test.wav", rate=16000, bits=16, channel=2, duration=3000)
```

### `record`
Record audio to a PCM buffer.

- Parameter `rate` (`int`): Sample rate (default is 16000).
- Parameter `bits` (`int`): Bit depth (default is 16).
- Parameter `channel` (`int`): Number of channels (default is 2).
- Parameter `duration` (`int`): Duration of the recording in milliseconds (default is 3000).

```python
base_echo.record(rate=16000, bits=16, channel=2, duration=3000)
```

### `pcm_buffer`
Get the PCM buffer.

- Returns: The PCM buffer.

```python
base_echo.pcm_buffer
```

### `deinit`

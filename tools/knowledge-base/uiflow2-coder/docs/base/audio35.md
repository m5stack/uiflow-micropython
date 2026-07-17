# Atomic Audio-3.5 Base

The following products are supported:

    Atomic Audio-3.5 Base

Below is the detailed support for Atomic Audio-3.5 Base on the host:

    Controller        Atomic Audio-3.5 Base  |
     Atom Echo        O                    |
     Atom Lite        S                    |
     Atom Matrix      S                    |
     AtomS3           S                    |
     AtomS3 Lite      S                    |
     AtomS3R          S                    |
     AtomS3R-CAM      S                    |
     AtomS3R-Ext      S                    |

> Note: Atomic Audio-3.5 Base uses the same Audio CODEC and pin connections as Atomic Echo Base. For detailed usage instructions, please refer to the `Atomic Echo Base <echo.html>`_ documentation.
## MicroPython Example

#### Record and play WAV file

This example initializes Atomic Audio-3.5 Base, records stereo audio to `/flash/res/audio/test.wav` for 5 seconds after pressing BtnA, and then plays the recorded WAV file.

```python
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

## **API**

#### class AtomicAudio35Base

## `AtomicAudio35Base`
`AtomicAudio35Base` is an alias of `AtomicEchoBase` in `m5stack/libs/base/echo.py`.

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

`AtomicAudio35Base` is an alias for `AtomicEchoBase`. Please refer to the `AtomicEchoBase <echo.html#base.echo.AtomicEchoBase>`_ class for detailed documentation.

# Audio Module

The AudioModule class implements playback and recording functions and supports resampling.

It is used to play audio files and streams, record audio from the microphone, and convert between different sample rates.

Support the following products:

    Audio Module

## MicroPython Example

#### Play WAV file

This example reads an audio file from the file system and plays it.

```python
import os, sys, io
import M5
from M5 import *
from module import AudioModule
import time

audio_0 = None

def setup():
    global audio_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    audio_0 = AudioModule(
        0,
        16000,
        i2s_sck=7,
        i2s_ws=6,
        i2s_di=14,
        i2s_do=13,
        i2s_mclk=0,
        work_mode=AudioModule.MODE_HEADPHONE,
        offset=False,
        mux=AudioModule.MUX_NATIONAL,
    )
    audio_0.play_wav_file("/flash/res/audio/66.wav")
    time.sleep(1)
    audio_0.pause()
    time.sleep(1)
    audio_0.resume()

def loop():
    global audio_0
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            audio_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Playback Controls

This example demonstrates how to control playback using the AudioModule class.

Play the audio for 1 second, pause for 1 second, and then resume playing.

```python
import os, sys, io
import M5
from M5 import *
from module import AudioModule
import time

audio_0 = None

def setup():
    global audio_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    audio_0 = AudioModule(
        0,
        16000,
        i2s_sck=7,
        i2s_ws=6,
        i2s_di=14,
        i2s_do=13,
        i2s_mclk=0,
        work_mode=AudioModule.MODE_HEADPHONE,
        offset=False,
        mux=AudioModule.MUX_NATIONAL,
    )
    audio_0.play_wav_file("/flash/res/audio/66.wav")
    time.sleep(1)
    audio_0.pause()
    time.sleep(1)
    audio_0.resume()

def loop():
    global audio_0
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            audio_0.deinit()
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
from module import AudioModule

audio_0 = None

def setup():
    global audio_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    audio_0 = AudioModule(
        0,
        16000,
        i2s_sck=7,
        i2s_ws=6,
        i2s_di=14,
        i2s_do=13,
        i2s_mclk=0,
        work_mode=AudioModule.MODE_HEADPHONE,
        offset=False,
        mux=AudioModule.MUX_NATIONAL,
    )
    audio_0.record(rate=16000, bits=16, channel=AudioModule.STEREO, duration=3000)
    audio_0.play_raw(
        audio_0.pcm_buffer, rate=16000, bits=16, channel=AudioModule.STEREO, duration=-1
    )

def loop():
    global audio_0
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            audio_0.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

#### Class AudioModule

## `AudioModule`
Initialize the audio module.

- Parameter `i2s_port`: I2S port number.
- Parameter `sample_rate`: Sample rate (default is 16000).
- Parameter `i2s_sck`: I2S clock pin.
- Parameter `i2s_ws`: I2S word select pin.
- Parameter `i2s_di`: I2S data input pin.
- Parameter `i2s_do`: I2S data output pin.
- Parameter `i2s_mclk`: I2S master clock pin.
- Parameter `Work mode (0` (`work_mode:`): headphone, 1: line in).
- Parameter `offset`: Generally speaking, when using line in, offset is False; if the input is connected to an ADC microphone, offset is True. (Only valid in line in mode).
- Parameter `mux`: Select the TRRS plug to be used. (default is MUX_NATIONAL).

```python
from module import AudioModule

audio_0 = AudioModule(0, 16000, i2s_sck=7, i2s_ws=6, i2s_di=14, i2s_do=13, i2s_mclk=0, work_mode=AudioModule.MODE_HEADPHONE, offset=False, mux=AudioModule.MUX_NATIONAL)
```

### `play_wav_file`
Play a WAV file.

- Parameter `file` (`str`): The path of the WAV file to play.
- Returns: None

```python
audio_0.play_wav_file("/flash/res/audio/test.wav")
```

### `tone`
Play simple tone sound.

- Parameter `freq` (`int`): Frequency of the tone in Hz.
- Parameter `duration` (`int`): Duration of the tone in milliseconds.
- Returns: None

```python
audio_0.tone(2000, 50)
```

### `play_wav`
Play a WAV buffer.

- Parameter `buf` (`bytes`): The WAV buffer to play.
- Parameter `duration` (`int`): Duration of the WAV buffer in milliseconds. when duration is -1, it will play until stopped. (default is -1).
- Returns: None

```python
audio_0.play_wav(wav_buffer, duration=1000)
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
audio_0.play_raw(pcm_buffer, rate=16000, bits=16, channel=2, duration=1000)
```

### `pause`
Pause the playback.

```python
audio.tone(2000, 100)
time.sleep(0.05)
audio_0.pause()
time.sleep(0.05)
audio_0.resume()
```

### `resume`
Resume the playback.

```python
audio.tone(2000, 100)
time.sleep(0.05)
audio_0.pause()
time.sleep(0.05)
audio_0.resume()
```

### `stop`
Stop the playback.

```python
audio.tone(2000, 100)
time.sleep(0.05)
audio_0.stop()
```

### `get_volume`
Get the speaker volume level.

- Returns: The volume level (0-100).

```python
audio_0.get_volume()
```

### `set_volume`
Set the speaker volume level.

- Parameter `volume` (`int`): The volume level (0-100).

```python
audio_0.set_volume(50)
```

### `record_wav_file`
Record audio to a WAV file.

- Parameter `path` (`str`): The path to save the WAV file.
- Parameter `rate` (`int`): Sample rate (default is 16000).
- Parameter `bits` (`int`): Bit depth (default is 16).
- Parameter `channel` (`int`): Number of channels (default is 2).
- Parameter `duration` (`int`): Duration of the recording in milliseconds (default is 3000).

```python
audio_0.record_wav_file("/flash/res/audio/test.wav", rate=16000, bits=16, channel=2, duration=3000)
```

### `record`
Record audio to a PCM buffer.

- Parameter `rate` (`int`): Sample rate (default is 16000).
- Parameter `bits` (`int`): Bit depth (default is 16).
- Parameter `channel` (`int`): Number of channels (default is 2).
- Parameter `duration` (`int`): Duration of the recording in milliseconds (default is 3000).

```python
audio_0.record(rate=16000, bits=16, channel=2, duration=3000)
```

### `pcm_buffer`
Get the PCM buffer.

- Returns: The PCM buffer.

```python
audio_0.pcm_buffer
```

### `set_color`
Set the RGB LED color.

- Parameter `num` (`int`): The LED number (0-2).
- Parameter `color` (`int`): The color value (0xRRGGBB).

```python
audio_0.set_color(0, 0xFF0000)
```

### `fill_color`
Fill all RGB LEDs with the same color.

- Parameter `color` (`int`): The color value (0xRRGGBB).

```python
audio_0.fill_color(0xFF0000)
```

### `set_brightness`
Set the RGB LED brightness.

- Parameter `br` (`int`): The brightness level (0-100).

```python
audio_0.set_brightness(50)
```

### `deinit`

# AudioPlayer Unit

This is the driver library of AudioPlayer Unit, which is used to play audio files.

Support the following products:

    AudioPlayer

## MicroPython Example

#### play audio

This example plays the audio file on the AudioPlayer Unit.

```python
import os, sys, io
import M5
from M5 import *
from unit import AudioPlayerUnit
import time

title0 = None
label0 = None
label1 = None
label2 = None
audioplayer_0 = None

play_state = None

def btn_b_was_pressed_event(state):
    global title0, label0, label1, label2, audioplayer_0, play_state
    if play_state:
        audioplayer_0.pause_audio()
    else:
        audioplayer_0.play_audio()

def setup():
    global title0, label0, label1, label2, audioplayer_0, play_state

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "AudioPlayerUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(">||", 145, 214, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 71, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 1, 123, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_PRESSED, cb=btn_b_was_pressed_event)

    audioplayer_0 = AudioPlayerUnit(2, port=(33, 32))
    audioplayer_0.set_play_mode(0)
    play_state = 0

def loop():
    global title0, label0, label1, label2, audioplayer_0, play_state
    M5.update()
    play_state = audioplayer_0.check_play_status()
    if play_state:
        label1.setText(str("Play Status: Playing"))
    else:
        label1.setText(str("Play Status: Paused"))
    label2.setText(str((str("Audio Num: ") + str((audioplayer_0.get_current_audio_number())))))
    time.sleep_ms(100)

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

#### AudioPlayerUnit

## `AudioPlayerUnit`
Create an AudioPlayerUnit object.

- Parameter `id` (`int`): The UART ID of the device. Default is 2.
- Parameter `port`: The UART port of the device.
- Type of `port`: list | tuple
- Parameter `verbose` (`bool`): The verbose mode of the device. Default is False.

```python
from unit import AudioPlayerUnit

audio_player_0 = AudioPlayerUnit(2, port=(33, 32))
```

### `check_play_status`
Check the play status of the audio player.

- Returns: The play status of the audio player.
- Return type: bool

```python
audio_player_0.check_play_status()
```

### `play_audio`
Play the audio.

- Returns: The play status of the audio player.
- Return type: int

```python
audio_player_0.play_audio()
```

### `pause_audio`
Pause the audio.

- Returns: The play status of the audio player.
- Return type: bool

```python
audio_player_0.pause_audio()
```

### `stop_audio`
Stop the audio.

- Returns: The play status of the audio player.
- Return type: int

```python
audio_player_0.stop_audio()
```

### `next_audio`
Play the next audio.

- Returns: Current play audio index.
- Return type: int

```python
audio_player_0.next_audio()
```

### `previous_audio`
Play the previous audio.

- Returns: Current play audio index.
- Return type: int

```python
audio_player_0.previous_audio()
```

### `play_audio_by_index`
Play audio by index number.

- Parameter `index` (`int`): The index of the audio to play.
- Returns: Current play audio index.
- Return type: int

```python
audio_player_0.play_audio_by_index(1)
```

### `play_audio_by_name`
Play audio by file name.

- Parameter `name` (`str`): The name of the audio file to play.
- Returns: Current play audio index.
- Return type: int

```python
audio_player_0.play_audio_by_name("music.mp3")
```

### `get_current_online_device_type`
Get the current online device type.

- Returns: Device type code
- Return type: int

    Device type:
        - 1: USB
        - 2: SD
        - 3: UDISK or SD
        - 4: Flash
        - 5: Flash or UDISK
        - 6: Flash or SD

```python
audio_player_0.get_current_online_device_type()
```

### `get_current_play_device_type`
Get the current play device type.

- Returns: Device type code (0: USB, 1: SD, 2: SPI FLASH).
- Return type: int

```python
audio_player_0.get_current_play_device_type()
```

### `get_total_audio_number`
Get the total number of audio files available.

- Returns: The total number of audio files.
- Return type: int

```python
audio_player_0.get_total_audio_number()
```

### `get_current_audio_number`
Get the current audio file number.

- Returns: The current audio file number.
- Return type: int

```python
audio_player_0.get_current_audio_number()
```

### `play_current_audio_at_time`
Play the current audio from a specific time position.

- Parameter `time_min` (`int`): The minute position to start playing from.
- Parameter `time_sec` (`int`): The second position to start playing from.

```python
audio_player_0.play_current_audio_at_time(1, 30)
```

### `play_audio_at_time`
Play a specific audio file from a specific time position.

- Parameter `audio_index` (`int`): The index of the audio file to play.
- Parameter `time_min` (`int`): The minute position to start playing from.
- Parameter `time_sec` (`int`): The second position to start playing from.

```python
audio_player_0.play_audio_at_time(1, 0, 30)
```

### `next_directory`
Navigate to the next directory.

```python
audio_player_0.next_directory()
```

### `previous_directory`
Navigate to the previous directory.

```python
audio_player_0.previous_directory()
```

### `end_audio`
End playing the current audio.

```python
audio_player_0.end_audio()
```

### `get_file_name`
Get the name of the current audio file.

- Returns: The name of the current audio file as a list of bytes.
- Return type: list

```python
audio_player_0.get_file_name()
```

### `select_audio_num`
Select an audio file by number without playing it.

- Parameter `audio_num` (`int`): The number of the audio file to select.
- Returns: The current selected audio file number.
- Return type: int

```python
audio_player_0.select_audio_num(1)
```

### `get_file_count`
Get the total number of files in the current directory.

- Returns: The total number of files.
- Return type: int

```python
audio_player_0.get_file_count()
```

### `get_total_play_time`
Get the total play time of the current audio file.

- Returns: A tuple containing (hour, minute, second) of the total play time.
- Return type: tuple

```python
audio_player_0.get_total_play_time()
```

### `decrease_volume`
Decrease the volume of the audio player.

```python
audio_player_0.decrease_volume()
```

### `increase_volume`
Increase the volume of the audio player.

```python
audio_player_0.increase_volume()
```

### `get_volume`
Get the current volume level of the audio player.

- Returns: The current volume level.
- Return type: int

```python
audio_player_0.get_volume()
```

### `set_volume`
Set the volume level of the audio player.

- Parameter `volume` (`int`): The volume level to set (0-30).

```python
audio_player_0.set_volume(15)
```

### `repeat_at_time`
Set repeat playback between two time positions.

- Parameter `start_min` (`int`): The start minute position.
- Parameter `start_sec` (`int`): The start second position.
- Parameter `end_min` (`int`): The end minute position.
- Parameter `end_sec` (`int`): The end second position.

```python
audio_player_0.repeat_at_time(0, 30, 1, 30)
```

### `end_repeat`
End the repeat playback mode.

```python
audio_player_0.end_repeat()
```

### `get_play_mode`
Get the current play mode.

- Returns: The current play mode.
- Return type: int

```python
audio_player_0.get_play_mode()
```

### `set_play_mode`
Set the play mode.

- Parameter `mode` (`int`): The play mode to set.

```python
audio_player_0.set_play_mode(1)
```

### `start_combine_play`
Start combined play mode.

- Parameter `mode` (`int`): The combined play mode.
- Parameter `data` (`list[int]`): The data for combined play.

```python
audio_player_0.start_combine_play(1, [1, 2, 3])
```

### `end_combine_play`
End the combined play mode.

```python
audio_player_0.end_combine_play()
```

### `into_sleep_mode`
Put the audio player into sleep mode.

- Returns: True if the command was sent successfully.
- Return type: bool

```python
audio_player_0.into_sleep_mode()
```

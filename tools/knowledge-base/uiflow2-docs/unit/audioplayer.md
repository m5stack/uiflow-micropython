# AudioPlayer Unit

<!-- .. sku:U197 -->

<!-- .. include:: ../refs/unit.audioplayer.ref -->

This is the driver library of AudioPlayer Unit, which is used to play audio files.

Support the following products:

    |AudioPlayer|

## UiFlow2 Example

#### play audio

Open the |audioplayer_core2_example.m5f2| project in UiFlow2.

This example plays the audio file on the AudioPlayer Unit.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### play audio

This example plays the audio file on the AudioPlayer Unit.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

Example output:

    None

## **API**

#### AudioPlayerUnit

## AudioPlayerUnit
Create an AudioPlayerUnit object.

:param int id: The UART ID of the device. Default is 2.
:param port: The UART port of the device.
:type port: list | tuple
:param bool verbose: The verbose mode of the device. Default is False.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import AudioPlayerUnit

        audio_player_0 = AudioPlayerUnit(2, port=(33, 32))

### `check_play_status`
Check the play status of the audio player.

:returns: The play status of the audio player.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.check_play_status()

### `play_audio`
Play the audio.

:returns: The play status of the audio player.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.play_audio()

### `pause_audio`
Pause the audio.

:returns: The play status of the audio player.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.pause_audio()

### `stop_audio`
Stop the audio.

:returns: The play status of the audio player.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.stop_audio()

### `next_audio`
Play the next audio.

:returns: Current play audio index.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.next_audio()

### `previous_audio`
Play the previous audio.

:returns: Current play audio index.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.previous_audio()

### `play_audio_by_index`
Play audio by index number.

:param int index: The index of the audio to play.
:returns: Current play audio index.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.play_audio_by_index(1)

### `play_audio_by_name`
Play audio by file name.

:param str name: The name of the audio file to play.
:returns: Current play audio index.
:rtype: int

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.play_audio_by_name("music.mp3")

### `get_current_online_device_type`
Get the current online device type.

:returns: Device type code
:rtype: int

    Device type:
        - 1: USB
        - 2: SD
        - 3: UDISK or SD
        - 4: Flash
        - 5: Flash or UDISK
        - 6: Flash or SD

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_current_online_device_type()

### `get_current_play_device_type`
Get the current play device type.

:returns: Device type code (0: USB, 1: SD, 2: SPI FLASH).
:rtype: int

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_current_play_device_type()

### `get_total_audio_number`
Get the total number of audio files available.

:returns: The total number of audio files.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_total_audio_number()

### `get_current_audio_number`
Get the current audio file number.

:returns: The current audio file number.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_current_audio_number()

### `play_current_audio_at_time`
Play the current audio from a specific time position.

:param int time_min: The minute position to start playing from.
:param int time_sec: The second position to start playing from.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.play_current_audio_at_time(1, 30)

### `play_audio_at_time`
Play a specific audio file from a specific time position.

:param int audio_index: The index of the audio file to play.
:param int time_min: The minute position to start playing from.
:param int time_sec: The second position to start playing from.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.play_audio_at_time(1, 0, 30)

### `next_directory`
Navigate to the next directory.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.next_directory()

### `previous_directory`
Navigate to the previous directory.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.previous_directory()

### `end_audio`
End playing the current audio.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.end_audio()

### `get_file_name`
Get the name of the current audio file.

:returns: The name of the current audio file as a list of bytes.
:rtype: list

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_file_name()

### `select_audio_num`
Select an audio file by number without playing it.

:param int audio_num: The number of the audio file to select.
:returns: The current selected audio file number.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.select_audio_num(1)

### `get_file_count`
Get the total number of files in the current directory.

:returns: The total number of files.
:rtype: int

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_file_count()

### `get_total_play_time`
Get the total play time of the current audio file.

:returns: A tuple containing (hour, minute, second) of the total play time.
:rtype: tuple

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_total_play_time()

### `decrease_volume`
Decrease the volume of the audio player.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.decrease_volume()

### `increase_volume`
Increase the volume of the audio player.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.increase_volume()

### `get_volume`
Get the current volume level of the audio player.

:returns: The current volume level.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_volume()

### `set_volume`
Set the volume level of the audio player.

:param int volume: The volume level to set (0-30).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.set_volume(15)

### `repeat_at_time`
Set repeat playback between two time positions.

:param int start_min: The start minute position.
:param int start_sec: The start second position.
:param int end_min: The end minute position.
:param int end_sec: The end second position.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.repeat_at_time(0, 30, 1, 30)

### `end_repeat`
End the repeat playback mode.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.end_repeat()

### `get_play_mode`
Get the current play mode.

:returns: The current play mode.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.get_play_mode()

### `set_play_mode`
Set the play mode.

:param int mode: The play mode to set.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.set_play_mode(1)

### `start_combine_play`
Start combined play mode.

:param int mode: The combined play mode.
:param list[int] data: The data for combined play.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.start_combine_play(1, [1, 2, 3])

### `end_combine_play`
End the combined play mode.

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.end_combine_play()

### `into_sleep_mode`
Put the audio player into sleep mode.

:returns: True if the command was sent successfully.
:rtype: bool

MicroPython Code Block:

    .. code-block:: python

        audio_player_0.into_sleep_mode()

# Synth Unit

Support the following products:

SynthUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import SynthUnit
import time

synth_0 = None

def setup():
    global synth_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    synth_0 = SynthUnit(1, port=(1, 2))
    synth_0.set_channel_volume(0, 64)
    synth_0.set_instrument(0, 0, 112)

def loop():
    global synth_0
    M5.update()
    synth_0.set_note_on(0, 0, 61)
    synth_0.set_note_on(0, 36, 127)
    time.sleep_ms(300)
    synth_0.set_note_on(0, 48, 124)
    synth_0.set_note_on(0, 60, 124)

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

## class SynthUnit

## Constructors

### `class SynthUnit(id, port)`

    Initializes the MIDI unit with a specified UART ID and port pins.
        The UART interface is used to transmit MIDI messages.

    - Parameter `id` (`Literal[0,1,2]`): UART device ID.
    - Parameter `port` (`List[int]|Tuple[int,int]`): UART TX and RX pins.

## Methods

### `SynthUnit.set_note_on(channel, pitch, velocity)`

    Sends a MIDI Note On message to the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `pitch`: Note pitch (0-127).
    - Parameter `velocity`: Note velocity (0-127).

### `SynthUnit.set_note_off(channel, pitch)`

    Sends a MIDI Note Off message to the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `pitch`: Note pitch (0-127).

### `SynthUnit.set_instrument(bank, channel, value)`

    Changes the program (instrument) on the specified channel.

    - Parameter `bank`: Bank selector (MSB) for the program change.
    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `value`: Program number (0-127).

### `SynthUnit.set_drums_instrument(drum_pitch, velocity)`

    Sets a drum instrument and plays a note on MIDI channel 10.

    - Parameter `drum_pitch`: Drum pitch number.
    - Parameter `velocity`: Note velocity (0-127).

### `SynthUnit.set_pitch_bend(channel, value)`

    Sends a MIDI Pitch Bend message to the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `value`: Pitch bend value (0-16383).

### `SynthUnit.set_pitch_bend_range(channel, value)`

    Sets the pitch bend range on the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `value`: Pitch bend range in semitones.

### `SynthUnit.midi_reset()`

    Sends a MIDI System Exclusive Reset command.

### `SynthUnit.set_channel_volume(channel, level)`

    Sets the channel volume for the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `level`: Volume level (0-100).

### `SynthUnit.set_all_notes_off(channel)`

    Sends a MIDI Control Change message to turn off all notes on the specified channel.

    - Parameter `channel`: MIDI channel (0-15).

### `SynthUnit.set_master_volume(level)`

    Sets the master volume using a standard System Exclusive message.

    - Parameter `level`: Volume level (0-100).

### `SynthUnit.set_reverb(channel, program, level, delayfeedback)`

    Configures reverb effect on the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `program`: Reverb program number (0-7).
    - Parameter `level`: Reverb level (0-127).
    - Parameter `delayfeedback`: Delay feedback amount (0-127).

### `SynthUnit.set_chorus(channel, program, level, feedback, chorusdelay)`

    Configures chorus effect on the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `program`: Chorus program number (0-7).
    - Parameter `level`: Chorus level (0-127).
    - Parameter `feedback`: Chorus feedback amount (0-127).
    - Parameter `chorusdelay`: Chorus delay amount (0-127).

### `SynthUnit.set_pan(channel, value)`

    Sets the pan position for the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `value`: Pan position (0-127).

### `SynthUnit.set_equalizer(channel, lowband, medlowband, medhighband, highband, lowfreq, medlowfreq, medhighfreq, highfreq)`

    Sets the equalizer levels and frequencies for the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `lowband`: Low band level (-12dB to +12dB).
    - Parameter `medlowband`: Mid-low band level (-12dB to +12dB).
    - Parameter `medhighband`: Mid-high band level (-12dB to +12dB).
    - Parameter `highband`: High band level (-12dB to +12dB).
    - Parameter `lowfreq`: Low band frequency (Hz).
    - Parameter `medlowfreq`: Mid-low band frequency (Hz).
    - Parameter `medhighfreq`: Mid-high band frequency (Hz).
    - Parameter `highfreq`: High band frequency (Hz).

### `SynthUnit.set_tuning(channel, fine, coarse)`

    Sets the tuning for the specified channel.

    - Parameter `channel`: MIDI channel (0-15).
    - Parameter `fine`: Fine tuning value (cents).
    - Parameter `coarse`: Coarse tuning value (semitones).

### `SynthUnit.set_vibrate(channel, rate, depth, delay)`

    Sets the vibrato effect parameters on the specified channel.

    - Parameter `channel`: The MIDI channel to apply the vibrato effect to (0-15).
    - Parameter `rate`: The vibrato rate (0-127).
    - Parameter `depth`: The vibrato depth (0-127).
    - Parameter `delay`: The vibrato delay (0-127).

### `SynthUnit.set_tvf(channel, cutoff, resonance)`

    Sets the parameters for a TVF (Tone-Voltage Filter) on the specified channel.

    - Parameter `channel`: The MIDI channel to apply the filter to (0-15).
    - Parameter `cutoff`: The filter cutoff frequency (0-127).
    - Parameter `resonance`: The filter resonance (0-127).

### `SynthUnit.set_envelope(channel, attack, decay, release)`

    Sets the ADSR (Attack, Decay, Sustain, Release) envelope parameters on the specified channel.

    - Parameter `channel`: The MIDI channel to apply the envelope to (0-15).
    - Parameter `attack`: The attack time (0-127).
    - Parameter `decay`: The decay time (0-127).
    - Parameter `release`: The release time (0-127).

### `SynthUnit.set_scale_tuning(channel, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12)`

    Sets scale tuning for the specified channel.

    - Parameter `channel`: The MIDI channel to apply the scale tuning to (0-15).
    - Parameter `v1~v12`: Tuning values for each note in the scale (0-127).

### `SynthUnit.set_mod_wheel(channel, pitch, tvtcutoff, amplitude, rate, pitchdepth, tvfdepth, tvadepth)`

    Sets modulation wheel parameters that affect various effects on the specified channel.

    - Parameter `channel`: The MIDI channel to apply the modulation to (0-15).
    - Parameter `pitch`: Pitch modulation depth.
    - Parameter `tvtcutoff`: Cutoff frequency modulation depth.
    - Parameter `amplitude`: Amplitude modulation depth.
    - Parameter `rate`: Modulation rate.
    - Parameter `pitchdepth`: Depth of pitch modulation.
    - Parameter `tvfdepth`: Depth of TVF modulation.
    - Parameter `tvadepth`: Depth of TVA (Tone-Voltage Amplifier) modulation.

### `SynthUnit.set_all_drums()`

    Sends a System Exclusive message to set all drums on channel 10 to default values.

### `SynthUnit.cmd_write(cmd)`

    Writes a MIDI command to the UART interface.

    - Parameter `cmd`: List of MIDI command bytes.

### `SynthUnit.map(x, in_min, in_max, out_min, out_max)`

    Maps a value from one range to another.

    - Parameter `x`: Value to map.
    - Parameter `in_min`: Minimum value of the input range.
    - Parameter `in_max`: Maximum value of the input range.
    - Parameter `out_min`: Minimum value of the output range.
    - Parameter `out_max`: Maximum value of the output range.

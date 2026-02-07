Synth Unit
==========

.. include:: ../refs/unit.synth.ref

Support the following products:

|SynthUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/synth/synth_cores3_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |synth_cores3_example.m5f2|


class SynthUnit
---------------

Constructors
------------

.. class:: SynthUnit(id, port)

    Initializes the MIDI unit with a specified UART ID and port pins.
        The UART interface is used to transmit MIDI messages.

    :param Literal[0,1,2] id: UART device ID.
    :param List[int]|Tuple[int,int] port: UART TX and RX pins.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: SynthUnit.set_note_on(channel, pitch, velocity)

    Sends a MIDI Note On message to the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  pitch: Note pitch (0-127).
    :param  velocity: Note velocity (0-127).

    UIFLOW2:

        |set_note_on2.png|

        |set_note_on.png|


.. method:: SynthUnit.set_note_off(channel, pitch)

    Sends a MIDI Note Off message to the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  pitch: Note pitch (0-127).

    UIFLOW2:

        |set_note_off.png|

.. method:: SynthUnit.set_instrument(bank, channel, value)

    Changes the program (instrument) on the specified channel.

    :param  bank: Bank selector (MSB) for the program change.
    :param  channel: MIDI channel (0-15).
    :param  value: Program number (0-127).

    UIFLOW2:

        |set_instrument.png|

.. method:: SynthUnit.set_drums_instrument(drum_pitch, velocity)

    Sets a drum instrument and plays a note on MIDI channel 10.

    :param  drum_pitch: Drum pitch number.
    :param  velocity: Note velocity (0-127).

    UIFLOW2:

        |set_drums_instrument.png|

.. method:: SynthUnit.set_pitch_bend(channel, value)

    Sends a MIDI Pitch Bend message to the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  value: Pitch bend value (0-16383).

    UIFLOW2:

        |set_pitch_bend.png|

.. method:: SynthUnit.set_pitch_bend_range(channel, value)

    Sets the pitch bend range on the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  value: Pitch bend range in semitones.

    UIFLOW2:

        |set_pitch_bend_range.png|

.. method:: SynthUnit.midi_reset()

    Sends a MIDI System Exclusive Reset command.


    UIFLOW2:

        |midi_reset.png|

.. method:: SynthUnit.set_channel_volume(channel, level)

    Sets the channel volume for the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  level: Volume level (0-100).

    UIFLOW2:

        |set_channel_volume.png|

.. method:: SynthUnit.set_all_notes_off(channel)

    Sends a MIDI Control Change message to turn off all notes on the specified channel.

    :param  channel: MIDI channel (0-15).

    UIFLOW2:

        |set_all_notes_off.png|

.. method:: SynthUnit.set_master_volume(level)

    Sets the master volume using a standard System Exclusive message.

    :param  level: Volume level (0-100).

    UIFLOW2:

        |set_master_volume.png|

.. method:: SynthUnit.set_reverb(channel, program, level, delayfeedback)

    Configures reverb effect on the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  program: Reverb program number (0-7).
    :param  level: Reverb level (0-127).
    :param  delayfeedback: Delay feedback amount (0-127).

    UIFLOW2:

        |set_reverb.png|

.. method:: SynthUnit.set_chorus(channel, program, level, feedback, chorusdelay)

    Configures chorus effect on the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  program: Chorus program number (0-7).
    :param  level: Chorus level (0-127).
    :param  feedback: Chorus feedback amount (0-127).
    :param  chorusdelay: Chorus delay amount (0-127).

    UIFLOW2:

        |set_chorus.png|

.. method:: SynthUnit.set_pan(channel, value)

    Sets the pan position for the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  value: Pan position (0-127).

    UIFLOW2:

        |set_pan.png|

.. method:: SynthUnit.set_equalizer(channel, lowband, medlowband, medhighband, highband, lowfreq, medlowfreq, medhighfreq, highfreq)

    Sets the equalizer levels and frequencies for the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  lowband: Low band level (-12dB to +12dB).
    :param  medlowband: Mid-low band level (-12dB to +12dB).
    :param  medhighband: Mid-high band level (-12dB to +12dB).
    :param  highband: High band level (-12dB to +12dB).
    :param  lowfreq: Low band frequency (Hz).
    :param  medlowfreq: Mid-low band frequency (Hz).
    :param  medhighfreq: Mid-high band frequency (Hz).
    :param  highfreq: High band frequency (Hz).

    UIFLOW2:

        |set_equalizer.png|

.. method:: SynthUnit.set_tuning(channel, fine, coarse)

    Sets the tuning for the specified channel.

    :param  channel: MIDI channel (0-15).
    :param  fine: Fine tuning value (cents).
    :param  coarse: Coarse tuning value (semitones).

    UIFLOW2:

        |set_tuning.png|

.. method:: SynthUnit.set_vibrate(channel, rate, depth, delay)

    Sets the vibrato effect parameters on the specified channel.

    :param  channel: The MIDI channel to apply the vibrato effect to (0-15).
    :param  rate: The vibrato rate (0-127).
    :param  depth: The vibrato depth (0-127).
    :param  delay: The vibrato delay (0-127).

    UIFLOW2:

        |set_vibrate.png|

.. method:: SynthUnit.set_tvf(channel, cutoff, resonance)

    Sets the parameters for a TVF (Tone-Voltage Filter) on the specified channel.

    :param  channel: The MIDI channel to apply the filter to (0-15).
    :param  cutoff: The filter cutoff frequency (0-127).
    :param  resonance: The filter resonance (0-127).

    UIFLOW2:

        |set_tvf.png|

.. method:: SynthUnit.set_envelope(channel, attack, decay, release)

    Sets the ADSR (Attack, Decay, Sustain, Release) envelope parameters on the specified channel.

    :param  channel: The MIDI channel to apply the envelope to (0-15).
    :param  attack: The attack time (0-127).
    :param  decay: The decay time (0-127).
    :param  release: The release time (0-127).

    UIFLOW2:

        |set_envelope.png|

.. method:: SynthUnit.set_scale_tuning(channel, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12)

    Sets scale tuning for the specified channel.

    :param  channel: The MIDI channel to apply the scale tuning to (0-15).
    :param  v1~v12: Tuning values for each note in the scale (0-127).

    UIFLOW2:

        |set_scale_tuning.png|

.. method:: SynthUnit.set_mod_wheel(channel, pitch, tvtcutoff, amplitude, rate, pitchdepth, tvfdepth, tvadepth)

    Sets modulation wheel parameters that affect various effects on the specified channel.

    :param  channel: The MIDI channel to apply the modulation to (0-15).
    :param  pitch: Pitch modulation depth.
    :param  tvtcutoff: Cutoff frequency modulation depth.
    :param  amplitude: Amplitude modulation depth.
    :param  rate: Modulation rate.
    :param  pitchdepth: Depth of pitch modulation.
    :param  tvfdepth: Depth of TVF modulation.
    :param  tvadepth: Depth of TVA (Tone-Voltage Amplifier) modulation.

    UIFLOW2:

        |set_mod_wheel.png|

.. method:: SynthUnit.set_all_drums()

    Sends a System Exclusive message to set all drums on channel 10 to default values.


    UIFLOW2:

        |set_all_drums.png|

.. method:: SynthUnit.cmd_write(cmd)

    Writes a MIDI command to the UART interface.

    :param  cmd: List of MIDI command bytes.

.. method:: SynthUnit.map(x, in_min, in_max, out_min, out_max)

    Maps a value from one range to another.

    :param  x: Value to map.
    :param  in_min: Minimum value of the input range.
    :param  in_max: Maximum value of the input range.
    :param  out_min: Minimum value of the output range.
    :param  out_max: Maximum value of the output range.






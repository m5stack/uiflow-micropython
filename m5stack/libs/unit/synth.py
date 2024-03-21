# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
Refer to https://github.com/fluxly/Fluxamasynth.
"""

from machine import UART, Pin
import sys

if sys.platform != "esp32":
    from typing import Literal

MIDI_CMD_NOTE_OFF = 0x80  # Note Off
MIDI_CMD_NOTE_ON = 0x90  # Note On
MIDI_CMD_POLYPHONIC_AFTERTOUCH = 0xA0  # Polyphonic Aftertouch (or Key Pressure)
MIDI_CMD_CONTROL_CHANGE = 0xB0  # Control Change (or Channel Mode Message)
MIDI_CMD_PROGRAM_CHANGE = 0xC0  # Program Change
MIDI_CMD_CHANNEL_AFTERTOUCH = 0xD0  # Channel Aftertouch (or Channel Pressure)
MIDI_CMD_PITCH_BEND = 0xE0  # Pitch Bend
MIDI_CMD_SYSTEM_EXCLUSIVE = 0xF0  # System Exclusive (SysEx) Start
MIDI_CMD_TIME_CODE = 0xF1  # MIDI Time Code Quarter Frame
MIDI_CMD_SONG_POSITION = 0xF2  # Song Position Pointer
MIDI_CMD_SONG_SELECT = 0xF3  # Song Select
MIDI_CMD_TUNE_REQUEST = 0xF6  # Tune Request
MIDI_CMD_END_OF_SYSEX = 0xF7  # End of SysEx
MIDI_CMD_TIMING_CLOCK = 0xF8  # Timing Clock (used in System Real-Time Messages)
MIDI_CMD_START = 0xFA  # Start (used in System Real-Time Messages)
MIDI_CMD_CONTINUE = 0xFB  # Continue (used in System Real-Time Messages)
MIDI_CMD_STOP = 0xFC  # Stop (used in System Real-Time Messages)
MIDI_CMD_ACTIVE_SENSING = 0xFE  # Active Sensing (used in System Real-Time Messages)
MIDI_CMD_SYSTEM_RESET = 0xFF  # System Reset

DRUM_SET = {
    "Closed Hi Hat [EXC1]": [27, 49],
    "Pedal Hi-Hat [EXC1]": [28, 49],
    "Open Hi Hat [EXC1]": [29, 49],
    "Ride Cymbal": [30, 49],
    "Kick drum2": [35, 1],
    "Jazz BD 2": [35, 41],
    "Kick drum": [35, 128],
    "Kick drum1": [36, 1],
    "Jazz BD 1": [36, 41],
    # "Kick drum"             :[36, 128],
    "Side Stick": [37, 1],
    "Rim Shot": [37, 128],
    "Snare Drum 1": [38, 1],
    "Gated Snare": [38, 17],
    "Brush Tap": [38, 41],
    "Snare Drum 2": [38, 49],
    "Snare Drum": [38, 128],
    "Hand Clap": [39, 1],
    "Brush Slap": [39, 41],
    "Castanets": [39, 49],
    "Hand Clap": [39, 128],  # noqa: F601
    "Snare Drum 2": [40, 1],  # noqa: F601
    "Brush Swirl": [40, 41],
    "Snare Drum 2": [40, 49],  # noqa: F601
    "Elec Snare Drum": [40, 128],
    "Low Floor Tom": [41, 1],
    "Timpani F": [41, 49],
    "Acoustic Low Tom": [41, 128],
    "Closed Hi Hat [EXC1]": [42, 1],  # noqa: F601
    "Timpani F#": [42, 49],
    "Closed Hi-Hat [Exc1]": [42, 128],
    "High Floor Tom": [43, 49],
    "Timpani G": [43, 49],
    "Acoustic Low Tom": [43, 128],  # noqa: F601
    "Pedal Hi-Hat [EXC1]": [44, 1],  # noqa: F601
    "Timpani G#": [44, 49],
    "Open Hi-Hat 2": [44, 128],
    "Low Tom": [45, 1],
    "Timpani A": [45, 49],
    "Acoustic Middle Tom": [45, 128],
    "Open Hi-Hat [EXC1]": [46, 1],
    "Timpani A#": [46, 49],
    "Open Hi-Hat 1 [Exc1]": [46, 128],
    "Low-Mid Tom": [47, 1],
    "Timpani B": [47, 49],
    "Acoustic Middle Tom": [47, 128],  # noqa: F601
    "Hi Mid Tom": [48, 1],
    "Timpani c": [48, 49],
    "Acoustic High Tom": [48, 128],
    "Crash Cymbal 1": [49, 1],
    "Timpani c#": [49, 49],
    "Crash Cymbal": [49, 128],
    "High Tom": [50, 1],
    "Timpani d": [50, 49],
    "Acoustic High Tom": [50, 128],  # noqa: F601
    "Ride Cymbal 1": [51, 1],
    "Timpani d#": [51, 49],
    "Ride Cymbal": [51, 128],  # noqa: F601
    "Chinese Cymbal": [52, 1],
    "Timpani e": [52, 49],
    "Ride Bell": [53, 1],
    "Timpani f": [53, 49],
    "Tambourine": [54, 1],
    # "Tambourine"            :[54, 128],
    "Splash Cymbal": [55, 1],
    "Cowbell": [56, 1],
    # "Cowbell"               :[56, 128],
    "Crash Cymbal 2": [57, 1],
    "Vibraslap": [58, 1],
    "Ride Cymbal 2": [59, 1],
    "Hi Bongo": [60, 1],
    "Low Bongo": [61, 1],
    "Mute Hi Conga": [62, 1],
    "Open Hi Conga": [63, 1],
    "Low Conga": [64, 1],
    "High Timbale": [65, 1],
    "Low Timbale": [66, 1],
    "High Agogo": [67, 1],
    "Low Agogo": [68, 1],
    "Cabasa": [69, 1],
    "Maracas": [70, 1],
    "Short Whistle[EXC2]": [71, 1],
    "Long Whistle[EXC2]": [72, 1],
    "Short Guiro [EXC3]": [73, 1],
    "Vibra Slap": [73, 128],
    "Long Guiro [EXC3]": [74, 1],
    "Claves": [75, 1],
    # "Claves"                :[75, 128],
    "Hi Wood Block": [76, 1],
    "Low Wood Block": [77, 1],
    "Mute Cuica [EXC4]": [78, 1],
    "Open Cuica [EXC4]": [79, 1],
    "Mute Triangle [EXC5]": [80, 1],
    "Open Triangle[EXC5]": [81, 1],
    "Applauses": [82, 128],
    # "Applauses"             :[88, 49],
    "Helicopter": [94, 127],
    "Gun Shot": [96, 127],
    "Birds": [102, 127],
    "SeaShore": [106, 127],
}


class SYNTHUnit:
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None, port_id=1):
        # TODO: 2.0.6 移除 port_id 参数
        id = port_id
        Pin(port[0], Pin.IN, Pin.PULL_UP)
        self._uart = UART(id, tx=port[1], rx=port[0])
        self._uart.init(31250, bits=8, parity=None, stop=1)

    def set_note_on(self, channel, pitch, velocity):
        cmd = [MIDI_CMD_NOTE_ON | (channel & 0x0F), pitch, velocity]
        self.cmd_write(cmd)

    def set_note_off(self, channel, pitch):
        cmd = [MIDI_CMD_NOTE_OFF | (channel & 0x0F), pitch, 0x00]
        self.cmd_write(cmd)

    def set_instrument(self, bank, channel, value):
        cmd = [MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F), 0x00, bank]
        self.cmd_write(cmd)
        cmd = [MIDI_CMD_PROGRAM_CHANGE | (channel & 0x0F), value]
        self.cmd_write(cmd)

    def set_drums_instrument(self, drum_pitch, velocity):
        self.set_instrument(0, 9, DRUM_SET[drum_pitch][1])
        self.set_note_on(9, DRUM_SET[drum_pitch][0], velocity)

    def set_pitch_bend(self, channel, value):
        value = self.map(value, 0, 1023, 0, 0x3FFF)
        cmd = [MIDI_CMD_PITCH_BEND | (channel & 0x0F), (value & 0xEF), ((value >> 7) & 0xFF)]
        self.cmd_write(cmd)

    def set_pitch_bend_range(self, channel, value):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F),
            0x65,
            0x00,
            0x64,
            0x00,
            0x06,
            (value & 0x7F),
        ]
        self.cmd_write(cmd)

    def midi_reset(self):
        self.cmd_write([MIDI_CMD_SYSTEM_RESET])

    def set_channel_volume(self, channel, level):
        cmd = [MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F), 0x07, level]
        self.cmd_write(cmd)

    def set_all_notes_off(self, channel):
        cmd = [MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F), 0x7B, 0x00]
        self.cmd_write(cmd)

    def set_master_volume(self, level):
        cmd = [
            MIDI_CMD_SYSTEM_EXCLUSIVE,
            0x7F,
            0x7F,
            0x04,
            0x01,
            0x00,
            (level & 0x7F),
            MIDI_CMD_END_OF_SYSEX,
        ]
        self.cmd_write(cmd)

    def set_reverb(self, channel, program, level, delayfeedback):
        cmd = [MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F), 0x50, (program & 0x07)]
        self.cmd_write(cmd)
        cmd = [MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F), 0x5B, (level & 0x7F)]
        self.cmd_write(cmd)
        if delayfeedback > 0:
            cmd = [
                MIDI_CMD_SYSTEM_EXCLUSIVE,
                0x41,
                0x00,
                0x42,
                0x12,
                0x40,
                0x01,
                0x35,
                (delayfeedback & 0x7F),
                0x00,
                MIDI_CMD_END_OF_SYSEX,
            ]
            self.cmd_write(cmd)

    def set_chorus(self, channel, program, level, feedback, chorusdelay):
        cmd = [MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F), 0x51, (program & 0x07)]
        self.cmd_write(cmd)
        cmd = [MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F), 0x5D, (level & 0x7F)]
        self.cmd_write(cmd)
        if feedback > 0:
            cmd = [
                MIDI_CMD_SYSTEM_EXCLUSIVE,
                0x41,
                0x00,
                0x42,
                0x12,
                0x40,
                0x01,
                0x3B,
                (feedback & 0x7F),
                0x00,
                MIDI_CMD_END_OF_SYSEX,
            ]
            self.cmd_write(cmd)
        if chorusdelay > 0:
            cmd = [
                MIDI_CMD_SYSTEM_EXCLUSIVE,
                0x41,
                0x00,
                0x42,
                0x12,
                0x40,
                0x01,
                0x3C,
                (feedback & 0x7F),
                0x00,
                MIDI_CMD_END_OF_SYSEX,
            ]
            self.cmd_write(cmd)

    def set_pan(self, channel, value):
        cmd = [MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F), 0x0A, value]
        self.cmd_write(cmd)

    def set_equalizer(
        self,
        channel,
        lowband,
        medlowband,
        medhighband,
        highband,
        lowfreq,
        medlowfreq,
        medhighfreq,
        highfreq,
    ):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F),
            0x63,
            0x37,
            0x62,
            0x00,
            0x06,
            (lowband & 0x7F),
        ]
        self.cmd_write(cmd)
        cmd[4] = 0x01
        cmd[6] = medlowband & 0x7F
        self.cmd_write(cmd)
        cmd[4] = 0x02
        cmd[6] = medhighband & 0x7F
        self.cmd_write(cmd)
        cmd[4] = 0x03
        cmd[6] = highband & 0x7F
        self.cmd_write(cmd)
        cmd[4] = 0x08
        cmd[6] = lowfreq & 0x7F
        self.cmd_write(cmd)
        cmd[4] = 0x09
        cmd[6] = medlowfreq & 0x7F
        self.cmd_write(cmd)
        cmd[4] = 0x0A
        cmd[6] = medhighfreq & 0x7F
        self.cmd_write(cmd)
        cmd[4] = 0x0B
        cmd[6] = highfreq & 0x7F
        self.cmd_write(cmd)

    def set_tuning(self, channel, fine, coarse):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F),
            0x65,
            0x00,
            0x64,
            0x01,
            0x06,
            (fine & 0x7F),
        ]
        self.cmd_write(cmd)
        cmd[4] = 0x02
        cmd[6] = coarse & 0x7F
        self.cmd_write(cmd)

    def set_vibrate(self, channel, rate, depth, delay):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F),
            0x63,
            0x01,
            0x62,
            0x08,
            0x06,
            (rate & 0x7F),
        ]
        self.cmd_write(cmd)
        cmd[4] = 0x09
        cmd[6] = depth & 0x7F
        self.cmd_write(cmd)
        cmd[4] = 0x0A
        cmd[6] = delay & 0x7F
        self.cmd_write(cmd)

    def set_tvf(self, channel, cutoff, resonance):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F),
            0x63,
            0x01,
            0x62,
            0x20,
            0x06,
            (cutoff & 0x7F),
        ]
        self.cmd_write(cmd)
        cmd[4] = 0x21
        cmd[6] = resonance & 0x7F
        self.cmd_write(cmd)

    def set_envelope(self, channel, attack, decay, release):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE | (channel & 0x0F),
            0x63,
            0x01,
            0x62,
            0x63,
            0x06,
            (attack & 0x7F),
        ]
        self.cmd_write(cmd)
        cmd[4] = 0x64
        cmd[6] = decay & 0x7F
        self.cmd_write(cmd)
        cmd[4] = 0x66
        cmd[6] = release & 0x7F
        self.cmd_write(cmd)

    def set_scale_tuning(self, channel, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE,
            0x41,
            0x00,
            0x42,
            0x12,
            0x40,
            0x10 | (channel & 0x0F),
            0x40,
            v1,
            v2,
            v3,
            v4,
            v5,
            v6,
            v7,
            v8,
            v9,
            v10,
            v11,
            v12,
            MIDI_CMD_END_OF_SYSEX,
        ]
        self.cmd_write(cmd)

    def set_mod_wheel(
        self, channel, pitch, tvtcutoff, amplitude, rate, pitchdepth, tvfdepth, tvadepth
    ):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE,
            0x41,
            0x00,
            0x42,
            0x12,
            0x40,
            0x20 | (channel & 0x0F),
            0x00,
            pitch,
            0x00,
            MIDI_CMD_END_OF_SYSEX,
        ]
        self.cmd_write(cmd)
        cmd[8] = 0x01
        cmd[9] = tvtcutoff
        self.cmd_write(cmd)
        cmd[8] = 0x02
        cmd[9] = amplitude
        self.cmd_write(cmd)
        cmd[8] = 0x03
        cmd[9] = rate
        self.cmd_write(cmd)
        cmd[8] = 0x04
        cmd[9] = pitchdepth
        self.cmd_write(cmd)
        cmd[8] = 0x05
        cmd[9] = tvfdepth
        self.cmd_write(cmd)
        cmd[8] = 0x06
        cmd[9] = tvadepth
        self.cmd_write(cmd)

    def set_all_drums(self):
        cmd = [
            MIDI_CMD_CONTROL_CHANGE,
            0x41,
            0x00,
            0x42,
            0x12,
            0x40,
            0x10,
            0x15,
            0x01,
            0x00,
            MIDI_CMD_END_OF_SYSEX,
        ]
        self.cmd_write(cmd)
        for i in range(1, 15):
            cmd[6] = i
            self.cmd_write(cmd)

    def cmd_write(self, cmd):
        self._uart.write(bytes(cmd))

    def map(self, x, in_min, in_max, out_min, out_max):
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


class SynthUnit(SYNTHUnit):
    def __init__(self, id: Literal[0, 1, 2], port: list | tuple):
        super().__init__(port, id)

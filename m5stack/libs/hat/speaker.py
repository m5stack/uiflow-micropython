# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5
import machine


class SpeakerHat:
    _instance = None
    _en_pin = {
        M5.BOARD.M5StickC: 0,
        M5.BOARD.M5StickCPlus: 0,
        M5.BOARD.M5StickCPlus2: 0,
        M5.BOARD.M5StackCoreInk: 25,
    }

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            return cls._instance

        spk = M5.createSpeaker()
        pin_en = machine.Pin(cls._en_pin.get(M5.getBoard()), machine.Pin.OUT)
        pin_en(1)
        spk.config(pin_data_out=26, use_dac=True, buzzer=False, magnification=32)
        spk.begin()
        spk.setVolume(80)
        cls._instance = spk
        return cls._instance

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5


class Speaker2Hat:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            return cls._instance

        _pin_map = {
            # i2s id, i2s bck, i2s dataout, i2s ws
            M5.BOARD.M5StickC: (2, 26, 25, 0),
            M5.BOARD.M5StickCPlus: (2, 26, 25, 0),
            M5.BOARD.M5StickCPlus2: (2, 26, 25, 0),
            M5.BOARD.ArduinoNessoN1: (0, 7, 2, 6),
        }
        if M5.getBoard() in _pin_map:
            (i2s_id, i2s_bck, i2s_dataout, i2s_ws) = _pin_map.get(M5.getBoard())
            spk = M5.createSpeaker()
            spk.config(
                pin_data_out=i2s_dataout,
                pin_bck=i2s_bck,
                pin_ws=i2s_ws,
                # sample_rate=48000,
                # stereo=True,
                magnification=16,
                # dma_buf_len=256,
                # dma_buf_count=8,
                # task_priority=2,
                # task_pinned_core=255,
                i2s_port=i2s_id,
            )
            M5.Speaker.end()
            M5.Mic.end()
            spk.begin()
            spk.setVolume(50)
            cls._instance = spk
            return cls._instance
        else:
            raise NotImplementedError("Speaker2 Hat is not supported on this board")

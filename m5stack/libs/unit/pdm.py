# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5


class PDMUnit:
    """PDM Unit class.

    :param list | tuple port: Connect to the PDM Unit.
    :param int i2s_port: I2S port number.
    :param int sample_rate: Sample rate.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import PDMUnit

            pdm_0 = PDMUnit((1, 2), i2s_port=0, sample_rate=44100)
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        port: list | tuple = (1, 2),
        i2s_port: int = 0,
        sample_rate: int = 44100,
    ) -> None:
        if self._initialized:
            return

        self._mic = M5.createMic()
        self._mic.config(
            dma_buf_count=3,
            dma_buf_len=256,
            over_sampling=2,
            noise_filter_level=0,
            sample_rate=sample_rate,
            pin_data_in=port[1],
            pin_ws=port[0],
            pin_bck=-1,
            pin_mck=-1,
            use_adc=False,
            stereo=False,
            magnification=2,
            task_priority=2,
            task_pinned_core=255,
            i2s_port=i2s_port,
        )
        self._initialized = True

    def __getattr__(self, name):
        return getattr(self._mic, name)

    def deinit(self):
        self._mic.deinit()

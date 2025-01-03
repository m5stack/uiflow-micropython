# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import driver.es8311 as es8311
import M5


class ATOMEchoBase:
    _instance = None

    PI4IOE_REG_CTRL = 0x00
    PI4IOE_REG_IO_PP = 0x07
    PI4IOE_REG_IO_DIR = 0x03
    PI4IOE_REG_IO_OUT = 0x05
    PI4IOE_REG_IO_PULLUP = 0x0D

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(
        self,
        i2c,
        address: int = 0x18,
        i2s_port: int = 1,
        sample_rate: int = 44100,
        i2s_sck: int = -1,
        i2s_ws: int = -1,
        i2s_di: int = -1,
        i2s_do: int = -1,
    ) -> None:
        if self._initialized:
            return
        self._i2c = i2c
        self._es8311 = es8311.ES8311(i2c, address)
        es_clk = es8311.es8311_clock_config_t()
        es_clk.mclk_inverted = False
        es_clk.sclk_inverted = False
        es_clk.mclk_from_mclk_pin = False  # MCLK taken from SCK pin
        es_clk.mclk_frequency = 0  # Not used
        es_clk.sample_frequency = sample_rate
        self._es8311.init(
            es_clk, es8311.ES8311.ES8311_RESOLUTION_32, es8311.ES8311.ES8311_RESOLUTION_32
        )
        self._es8311.voice_volume_set(100)
        self._es8311.microphone_config(False)

        self.speaker = M5.createSpeaker()
        self.speaker.config(
            pin_data_out=i2s_do,
            pin_bck=i2s_sck,
            pin_ws=i2s_ws,
            sample_rate=sample_rate,
            stereo=True,
            buzzer=False,
            use_dac=False,
            dac_zero_level=False,
            magnification=1,
            dma_buf_len=256,
            dma_buf_count=8,
            task_priority=2,
            task_pinned_core=255,
            i2s_port=i2s_port,
        )

        self.microphone = M5.createMic()
        self.microphone.config(
            pin_data_in=i2s_di,
            pin_bck=i2s_sck,
            pin_mck=-1,
            pin_ws=i2s_ws,
            sample_rate=sample_rate,
            stereo=True,
            over_sampling=1,
            magnification=1,
            noise_filter_level=0,
            use_adc=False,
            dma_buf_len=240,
            dma_buf_count=6,
            task_priority=2,
            task_pinned_core=255,
            i2s_port=i2s_port,
        )
        self.pi4ioe_init()
        self._initialized = True

    def pi4ioe_init(self):
        self._i2c.readfrom_mem(0x43, self.PI4IOE_REG_CTRL, 1)

        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_PP, b"\x00")
        self._i2c.readfrom_mem(0x43, self.PI4IOE_REG_IO_PP, 1)

        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_PULLUP, b"\xff")
        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_DIR, b"\x6e")
        self._i2c.readfrom_mem(0x43, self.PI4IOE_REG_IO_DIR, 1)

        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_OUT, b"\xff")
        self._i2c.readfrom_mem(0x43, self.PI4IOE_REG_IO_OUT, 1)

    def set_mute(self, mute):
        if mute:
            self._i2c.writeto_mem(0x43, 0x05, b"\x00")
        else:
            self._i2c.writeto_mem(0x43, 0x05, b"\xff")

    def deinit(self):
        self.speaker.deinit()
        self.microphone.deinit()

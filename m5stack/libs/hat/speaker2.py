import M5


class Speaker2Hat:
    def __new__(cls):
        spk = M5.createSpeaker()
        spk.config(
            pin_data_out=25,
            pin_bck=26,
            pin_ws=0,
            sample_rate=48000,
            stereo=False,
            buzzer=False,
            use_dac=False,
            dac_zero_level=0,
            magnification=16,
            dma_buf_len=256,
            dma_buf_count=8,
            task_priority=2,
            task_pinned_core=255,
            i2s_port=1,
        )
        M5.Speaker.end()
        M5.Mic.end()
        spk.begin()
        spk.setVolume(50)
        return spk

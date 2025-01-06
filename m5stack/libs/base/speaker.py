import M5


class SpeakerBase:
    _instance = None

    def __new__(cls, _id, sck, ws, sd):
        if cls._instance:
            cls._instance.end()

        if cls._instance is None:
            cls._instance = M5.createSpeaker()

        cls._instance.config(
            pin_data_out=sd,
            pin_bck=sck,
            pin_ws=ws,
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
            i2s_port=_id,
        )
        cls._instance.begin()
        cls._instance.setVolume(80)
        return cls._instance

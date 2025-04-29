# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from driver import es8388
from .mbus import i2c1
import m5audio2
import machine
import M5
import time


class _Expander:
    REG_MICROPHONE_STATUS = 0x00
    """Microphone/LINE Input Configuration Register (R/W)"""

    REG_HEADPHONE_MODE = 0x10
    """Headphone Mode Configuration Register (R/W)"""

    REG_HEADPHONE_INSERT_STATUS = 0x20
    """Headphone Insertion Detection Register (Read-Only)
    """

    REG_RGB_BRIGHTNESS = 0x30
    """RGB LED Brightness Control Register (R/W)
    """

    REG_RGB_LED = 0x40
    """RGB LED Color Control Register (R/W)
    """

    REG_FLASH_WRITE = 0xF0
    """Configuration Save Register (Write-Only)
    """

    REG_FIRMWARE_VERSION = 0xFE
    """Firmware Version Register (Read-Only)"""

    REG_I2C_ADDRESS = 0xFF
    """I2C Address Register (Read-Only)"""

    AUDIO_MIC_CLOSE = 0
    """Disable MIC/LINE input (value: 0)"""

    AUDIO_MIC_OPEN = 1
    """Enable MIC/LINE input (value: 1, default)"""

    AUDIO_HPMODE_NATIONAL = 0
    """National Standard audio mode (value: 0, default)"""

    AUDIO_HPMODE_AMERICAN = 1
    """American Standard audio mode (value: 1)"""

    def __init__(self, i2c, address=0x33):
        self._i2c = i2c
        self._address = address

    def set_mic_status(self, status: int):
        self.write_register(self.REG_MICROPHONE_STATUS, status)

    def set_hp_mode(self, mode: int):
        self.write_register(self.REG_HEADPHONE_MODE, mode)

    def set_color(self, num: int, color: int):
        num = 2 if num > 2 else num
        self._i2c.writeto_mem(self._address, self.REG_RGB_LED + num * 3, color.to_bytes(3, "big"))

    def fill_color(self, color: int):
        self._i2c.writeto_mem(self._address, self.REG_RGB_LED, color.to_bytes(3, "big") * 3)

    def set_brightness(self, br: int):
        br = 100 if br > 100 else br
        self.write_register(self.REG_RGB_BRIGHTNESS, br)

    def set_flash_write_back(self):
        self.write_register(self.REG_FLASH_WRITE, 1)

    def set_i2c_address(self, address: int):
        if address >= 0x08 and address <= 0x77:
            if address != self._address:
                time.sleep_ms(2)
                self.write_register(self.REG_I2C_ADDRESS, address)
                self._address = address
                time.sleep_ms(200)
        else:
            raise ValueError("I2C address error, range:0x08~0x78")

    def get_mic_status(self):
        return self.read_register(self.REG_MICROPHONE_STATUS)

    def get_hp_mode(self):
        return self.read_register(self.REG_HEADPHONE_MODE)

    def get_hp_insert_status(self):
        return self.read_register(self.REG_HEADPHONE_INSERT_STATUS)

    def get_firmware_version(self) -> int:
        return self.read_register(self.REG_FIRMWARE_VERSION)

    def get_i2c_address(self):
        return self.read_register(self.REG_I2C_ADDRESS)

    def write_register(self, reg: int, data: int) -> None:
        self._i2c.writeto_mem(self._address, reg, bytes([data]))

    def read_register(self, reg: int) -> int:
        return self._i2c.readfrom_mem(self._address, reg, 1)[0]


class AudioModule:
    MUX_NATIONAL = _Expander.AUDIO_HPMODE_NATIONAL
    MUX_AMERICAN = _Expander.AUDIO_HPMODE_AMERICAN
    MODE_LINE = 0
    MODE_HEADPHONE = 1

    MONO = 1
    STEREO = 2

    def __init__(
        self,
        i2s_port,
        sample_rate=16000,
        i2s_sck=19,
        i2s_ws=27,
        i2s_di=34,
        i2s_do=2,
        i2s_mclk=0,
        work_mode=MODE_HEADPHONE,
        offset=1,
        mux=MUX_NATIONAL,
    ):
        self._i2c = i2c1
        self.exp = _Expander(self._i2c)
        self.es = es8388.ES8388(self._i2c)
        self.exp.fill_color(0x000000)
        if work_mode == self.MODE_HEADPHONE:
            self.exp.set_hp_mode(mux)
            self.exp.set_mic_status(self.exp.AUDIO_MIC_OPEN)
        else:
            self.exp.set_mic_status(
                self.exp.AUDIO_MIC_OPEN if offset else self.exp.AUDIO_MIC_CLOSE
            )
        self.es.init()
        self.es.set_adc_volume(100)
        self.es.set_dac_volume(60)
        self.es.set_mix_source_select(self.es.MIX_SEL_ADC, self.es.MIX_SEL_ADC)
        self.es.set_bits_per_sample(self.es.WORK_MODE_ADC, self.es.BIT_LENGTH_16BITS)
        # self.es.set_sample_rate(self.es.SAMPLE_RATE_16000HZ)

        M5.Speaker.end()
        M5.Mic.end()
        time.sleep(0.2)

        self.spk = m5audio2.Player(
            i2s_port,
            sck=machine.Pin(i2s_sck),
            ws=machine.Pin(i2s_ws),
            sd=machine.Pin(i2s_do),
            mck=machine.Pin(i2s_mclk),
            rate=sample_rate,
            bits=16,
            channel=2,
        )

        self.mic = m5audio2.Recorder(
            i2s_port,
            sck=machine.Pin(i2s_sck),
            ws=machine.Pin(i2s_ws),
            sd=machine.Pin(i2s_di),
            mck=machine.Pin(i2s_mclk),
            rate=sample_rate,
            bits=16,
            channel=2,
        )

    def play_wav_file(self, file):
        if self.mic.is_running():
            self.mic.deinit()
        self.spk.play_wav_file(file)

    def tone(self, freq, duration):
        if self.mic.is_running():
            self.mic.deinit()
        self.spk.tone(freq, duration)

    def play_wav(self, buf, duration=-1):
        if self.mic.is_running():
            self.mic.deinit()
        self.spk.play_wav(buf, duration=duration)

    def play_raw(self, buf, rate=16000, bits=16, channel=2, duration=-1):
        if self.mic.is_running():
            self.mic.deinit()
        self.spk.play_raw(buf, rate=rate, bits=bits, channel=channel, duration=duration)

    def pause(self):
        self.spk.pause()

    def resume(self):
        self.spk.resume()

    def stop(self):
        self.spk.stop()

    def get_volume(self):
        return self.es.get_dac_volume()

    def set_volume(self, volume):
        self.spk.es.set_dac_volume(volume)

    def record_wav_file(self, path, rate=16000, bits=16, channel=2, duration=3000):
        self.spk.deinit()
        self.mic.record_wav_file(path, rate=rate, bits=bits, channel=channel, duration=duration)

    def record(self, rate=16000, bits=16, channel=2, duration=3000):
        self.spk.deinit()
        return self.mic.record(rate=rate, bits=bits, channel=channel, duration=duration)

    @property
    def pcm_buffer(self):
        return self.mic.pcm_buffer

    def set_color(self, num: int, color: int):
        self.exp.set_color(num, color)

    def fill_color(self, color: int):
        self.exp.fill_color(color)

    def set_brightness(self, br: int):
        self.exp.set_brightness(br)

    def deinit(self):
        self.spk.deinit()
        self.mic.deinit(True)
        self.exp.fill_color(0x000000)

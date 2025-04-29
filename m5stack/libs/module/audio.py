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
    """Initialize the audio module.

    :param i2s_port: I2S port number.
    :param sample_rate: Sample rate (default is 16000).
    :param i2s_sck: I2S clock pin.
    :param i2s_ws: I2S word select pin.
    :param i2s_di: I2S data input pin.
    :param i2s_do: I2S data output pin.
    :param i2s_mclk: I2S master clock pin.
    :param work_mode: Work mode (0: headphone, 1: line in).
    :param offset: Generally speaking, when using line in, offset is False; if the input is connected to an ADC microphone, offset is True. (Only valid in line in mode).
    :param mux: Select the TRRS plug to be used. (default is MUX_NATIONAL).

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import AudioModule

            audio_0 = AudioModule(0, 16000, i2s_sck=7, i2s_ws=6, i2s_di=14, i2s_do=13, i2s_mclk=0, work_mode=AudioModule.MODE_HEADPHONE, offset=False, mux=AudioModule.MUX_NATIONAL)
    """

    MUX_NATIONAL = _Expander.AUDIO_HPMODE_NATIONAL
    """National Standard audio mode (OMTP)"""

    MUX_AMERICAN = _Expander.AUDIO_HPMODE_AMERICAN
    """American Standard audio mode (CTIA)"""

    MODE_LINE = 0
    """Line in mode"""

    MODE_HEADPHONE = 1
    """Headphone mode"""

    MONO = 1
    """Mono"""

    STEREO = 2
    """Stereo"""

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

    def play_wav_file(self, file: str) -> None:
        """Play a WAV file.

        :param str file: The path of the WAV file to play.
        :return: None

        UiFlow2 Code Block:

            |play_wav_file.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.play_wav_file("/flash/res/audio/test.wav")
        """
        if self.mic.is_running():
            self.mic.deinit()
        self.spk.play_wav_file(file)

    def tone(self, freq: int, duration: int) -> None:
        """Play simple tone sound.

        :param int freq: Frequency of the tone in Hz.
        :param int duration: Duration of the tone in milliseconds.
        :return: None

        UiFlow2 Code Block:

            |tone.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.tone(2000, 50)
        """
        if self.mic.is_running():
            self.mic.deinit()
        self.spk.tone(freq, duration)

    def play_wav(self, buf: bytes, duration: int = -1) -> None:
        """Play a WAV buffer.

        :param bytes buf: The WAV buffer to play.
        :param int duration: Duration of the WAV buffer in milliseconds. when duration is -1, it will play until stopped. (default is -1).
        :return: None

        UiFlow2 Code Block:

            |play_wav.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.play_wav(wav_buffer, duration=1000)
        """
        if self.mic.is_running():
            self.mic.deinit()
        self.spk.play_wav(buf, duration=duration)

    def play_raw(
        self, buf: bytes, rate: int = 16000, bits: int = 16, channel: int = 2, duration: int = -1
    ) -> None:
        """Play a pcm buffer.

        :param bytes buf: The PCM buffer to play.
        :param int rate: Sample rate (default is 16000).
        :param int bits: Bit depth (default is 16).
        :param int channel: Number of channels (default is 2).
        :param int duration: Duration of the PCM buffer in milliseconds. when duration is -1, it will play until stopped. (default is -1).
        :return: None

        UiFlow2 Code Block:

            |play_raw.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.play_raw(pcm_buffer, rate=16000, bits=16, channel=2, duration=1000)
        """
        if self.mic.is_running():
            self.mic.deinit()
        self.spk.play_raw(buf, rate=rate, bits=bits, channel=channel, duration=duration)

    def pause(self) -> None:
        """Pause the playback.

        UiFlow2 Code Block:

            |pause.png|

        MicroPython Code Block:

            .. code-block:: python

                audio.tone(2000, 100)
                time.sleep(0.05)
                audio_0.pause()
                time.sleep(0.05)
                audio_0.resume()
        """
        self.spk.pause()

    def resume(self):
        """Resume the playback.

        UiFlow2 Code Block:

            |resume.png|

        MicroPython Code Block:

            .. code-block:: python

                audio.tone(2000, 100)
                time.sleep(0.05)
                audio_0.pause()
                time.sleep(0.05)
                audio_0.resume()
        """
        self.spk.resume()

    def stop(self):
        """Stop the playback.

        UiFlow2 Code Block:

            |stop.png|

        MicroPython Code Block:

            .. code-block:: python

                audio.tone(2000, 100)
                time.sleep(0.05)
                audio_0.stop()
        """
        self.spk.stop()

    def get_volume(self) -> int:
        """Get the speaker volume level.

        :return: The volume level (0-100).

        UiFlow2 Code Block:

            |get_volume.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.get_volume()
        """
        return self.es.get_dac_volume()

    def set_volume(self, volume):
        """Set the speaker volume level.

        :param int volume: The volume level (0-100).

        UiFlow2 Code Block:

            |set_volume.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.set_volume(50)
        """
        self.spk.es.set_dac_volume(volume)

    def record_wav_file(
        self, path: str, rate: int = 16000, bits: int = 16, channel: int = 2, duration: int = 3000
    ):
        """Record audio to a WAV file.

        :param str path: The path to save the WAV file.
        :param int rate: Sample rate (default is 16000).
        :param int bits: Bit depth (default is 16).
        :param int channel: Number of channels (default is 2).
        :param int duration: Duration of the recording in milliseconds (default is 3000).

        UiFlow2 Code Block:

            |record_wav_file.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.record_wav_file("/flash/res/audio/test.wav", rate=16000, bits=16, channel=2, duration=3000)
        """
        self.spk.deinit()
        self.mic.record_wav_file(path, rate=rate, bits=bits, channel=channel, duration=duration)

    def record(self, rate=16000, bits=16, channel=2, duration=3000):
        """Record audio to a PCM buffer.

        :param int rate: Sample rate (default is 16000).
        :param int bits: Bit depth (default is 16).
        :param int channel: Number of channels (default is 2).
        :param int duration: Duration of the recording in milliseconds (default is 3000).

        UiFlow2 Code Block:

            |record.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.record(rate=16000, bits=16, channel=2, duration=3000)
        """
        self.spk.deinit()
        return self.mic.record(rate=rate, bits=bits, channel=channel, duration=duration)

    @property
    def pcm_buffer(self) -> bytes:
        """Get the PCM buffer.

        :return: The PCM buffer.

        UiFlow2 Code Block:

            |pcm_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.pcm_buffer
        """
        return self.mic.pcm_buffer

    def set_color(self, num: int, color: int):
        """Set the RGB LED color.

        :param int num: The LED number (0-2).
        :param int color: The color value (0xRRGGBB).

        UiFlow2 Code Block:

            |set_color.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.set_color(0, 0xFF0000)
        """
        self.exp.set_color(num, color)

    def fill_color(self, color: int):
        """Fill all RGB LEDs with the same color.

        :param int color: The color value (0xRRGGBB).

        UiFlow2 Code Block:

            |fill_color.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.fill_color(0xFF0000)
        """
        self.exp.fill_color(color)

    def set_brightness(self, br: int):
        """Set the RGB LED brightness.

        :param int br: The brightness level (0-100).

        UiFlow2 Code Block:

            |set_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                audio_0.set_brightness(50)
        """
        self.exp.set_brightness(br)

    def deinit(self):
        self.spk.deinit()
        self.mic.deinit(True)
        self.exp.fill_color(0x000000)

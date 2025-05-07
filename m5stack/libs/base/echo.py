# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import driver.es8311 as es8311
import m5audio2
import machine
import M5


class AtomicEchoBase:
    """Create an AtomicEchoBase object.

    :param I2C i2c: I2C object
    :param int address: The I2C address of the ES8311. Default is 0x18.
    :param int i2s_port: The I2S port number. Default is 1.
    :param int sample_rate: The sample rate of the audio. Default is 16000.
    :param int i2s_sck: The I2S SCK pin. Default is -1.
    :param int i2s_ws: The I2S WS pin. Default is -1.
    :param int i2s_di: The I2S DI pin. Default is -1.
    :param int i2s_do: The I2S DO pin. Default is -1.

    UIFLOW2:

        |init.png|

    Micropython::

        from hardware import I2C
        from hardware import Pin
        from base import AtomicEchoBase

        # atom echo
        i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
        base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

        # atom lite
        i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
        base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

        # atom matrix
        i2c1 = I2C(1, scl=Pin(21), sda=Pin(25), freq=100000)
        base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=33, i2s_ws=19, i2s_di=23, i2s_do=22)

        # atoms3 / atoms3 lite
        i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
        base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=8, i2s_ws=6, i2s_di=7, i2s_do=5)

        # atoms3r / atoms3r-cam / atoms3-ext
        i2c1 = I2C(1, scl=Pin(39), sda=Pin(38), freq=100000)
        base_echo = AtomicEchoBase(i2c1, address=0x18, i2s_port=1, sample_rate=44100, i2s_sck=8, i2s_ws=6, i2s_di=7, i2s_do=5)

        base_echo.speaker.tone(2000, 1000)
        base_echo.speaker.playWavFile('res/audio/66.wav')
    """

    _instance = None

    PI4IOE_REG_CTRL = 0x00
    PI4IOE_REG_CHIP_RESET = 0x01
    PI4IOE_REG_IO_DIR = 0x03
    PI4IOE_REG_IO_OUT = 0x05
    PI4IOE_REG_IO_PP = 0x07
    PI4IOE_REG_PULL_EN = 0x0B
    PI4IOE_REG_IO_PULLUP = 0x0D

    MONO = 1
    """Mono"""

    STEREO = 2
    """Stereo"""

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
        sample_rate: int = 16000,
        i2s_sck: int = -1,
        i2s_ws: int = -1,
        i2s_di: int = -1,
        i2s_do: int = -1,
    ) -> None:
        if self._initialized:
            return
        self._i2c = i2c
        self._es8311 = es8311.ES8311(i2c, address)
        self.es_clk = es8311.es8311_clock_config_t()
        self.es_clk.mclk_inverted = False
        self.es_clk.sclk_inverted = False
        self.es_clk.mclk_from_mclk_pin = False  # MCLK taken from SCK pin
        self.es_clk.mclk_frequency = 0  # Not used
        self.es_clk.sample_frequency = sample_rate
        self._es8311.init(
            self.es_clk, es8311.ES8311.ES8311_RESOLUTION_32, es8311.ES8311.ES8311_RESOLUTION_32
        )
        self._es8311.voice_volume_set(80)
        self._es8311.microphone_config(False)

        M5.Speaker.end()
        M5.Mic.end()

        self.spk = m5audio2.Player(
            i2s_port,
            sck=machine.Pin(i2s_sck),
            ws=machine.Pin(i2s_ws),
            sd=machine.Pin(i2s_do),
            rate=sample_rate,
            bits=16,
            channel=2,
        )

        self.mic = m5audio2.Recorder(
            i2s_port,
            sck=machine.Pin(i2s_sck),
            ws=machine.Pin(i2s_ws),
            sd=machine.Pin(i2s_di),
            rate=sample_rate,
            bits=16,
            channel=2,
        )

        self.pi4ioe_init()
        self._initialized = True

    def pi4ioe_init(self):
        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_PP, b"\x00")
        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_PULLUP, b"\xff")
        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_DIR, b"\x6e")
        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_OUT, b"\xff")

    def set_mute(self, mute):
        self._i2c.writeto_mem(0x43, self.PI4IOE_REG_IO_OUT, b"\x00" if mute else b"\xff")

    def change_sample_rate(self, sample_rate: int) -> None:
        self.es_clk.sample_frequency = sample_rate
        self._es8311.clock_config(self.es_clk, es8311.ES8311.ES8311_RESOLUTION_32)

    def play_wav_file(self, file: str) -> None:
        """Play a WAV file.

        :param str file: The path of the WAV file to play.
        :return: None

        UiFlow2 Code Block:

            |play_wav_file.png|

        MicroPython Code Block:

            .. code-block:: python

                base_echo.play_wav_file("/flash/res/audio/test.wav")
        """
        if self.mic.is_running():
            self.mic.deinit()
        self.set_mute(False)
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

                base_echo.tone(2000, 50)
        """
        if self.mic.is_running():
            self.mic.deinit()
        self.set_mute(False)
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

                base_echo.play_wav(wav_buffer, duration=1000)
        """
        if self.mic.is_running():
            self.mic.deinit()
        self.set_mute(False)
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

                base_echo.play_raw(pcm_buffer, rate=16000, bits=16, channel=2, duration=1000)
        """
        if self.mic.is_running():
            self.mic.deinit()
        self.set_mute(False)
        self.spk.play_raw(buf, rate=rate, bits=bits, channel=channel, duration=duration)

    def pause(self) -> None:
        """Pause the playback.

        UiFlow2 Code Block:

            |pause.png|

        MicroPython Code Block:

            .. code-block:: python

                audio.tone(2000, 100)
                time.sleep(0.05)
                base_echo.pause()
                time.sleep(0.05)
                base_echo.resume()
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
                base_echo.pause()
                time.sleep(0.05)
                base_echo.resume()
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
                base_echo.stop()
        """
        self.spk.stop()

    def get_volume(self) -> int:
        """Get the speaker volume level.

        :return: The volume level (0-100).

        UiFlow2 Code Block:

            |get_volume.png|

        MicroPython Code Block:

            .. code-block:: python

                base_echo.get_volume()
        """
        return self._es8311.voice_volume_get()

    def set_volume(self, volume):
        """Set the speaker volume level.

        :param int volume: The volume level (0-100).

        UiFlow2 Code Block:

            |set_volume.png|

        MicroPython Code Block:

            .. code-block:: python

                base_echo.set_volume(50)
        """
        self._es8311.voice_volume_set(volume)

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

                base_echo.record_wav_file("/flash/res/audio/test.wav", rate=16000, bits=16, channel=2, duration=3000)
        """
        self.spk.deinit()
        self.set_mute(True)
        self.change_sample_rate(rate)
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

                base_echo.record(rate=16000, bits=16, channel=2, duration=3000)
        """
        self.spk.deinit()
        self.set_mute(True)
        self.change_sample_rate(rate)
        return self.mic.record(rate=rate, bits=bits, channel=channel, duration=duration)

    @property
    def pcm_buffer(self) -> bytes:
        """Get the PCM buffer.

        :return: The PCM buffer.

        UiFlow2 Code Block:

            |pcm_buffer.png|

        MicroPython Code Block:

            .. code-block:: python

                base_echo.pcm_buffer
        """
        return self.mic.pcm_buffer

    def deinit(self):
        self.spk.deinit()
        self.mic.deinit(True)
        self.set_mute(True)

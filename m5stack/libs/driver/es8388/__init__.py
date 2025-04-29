# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from . import reg


class SampleInfo:
    def __init__(self, bits_per_sample, channel, channel_mask, sample_rate, mclk_multiple) -> None:
        self.bits_per_sample = bits_per_sample
        self.channel = channel
        self.channel_mask = channel_mask
        self.sample_rate = sample_rate
        self.mclk_multiple = mclk_multiple


class ES8388:
    MIX_SEL_LIN1 = 0b000
    MIX_SEL_LIN2 = 0b001
    MIX_SEL_RES = 0b010
    MIX_SEL_ADC = 0b011

    SAMPLE_RATE_8000HZ = 0
    SAMPLE_RATE_11025HZ = 1
    SAMPLE_RATE_16000HZ = 2
    SAMPLE_RATE_24000HZ = 3
    SAMPLE_RATE_32000HZ = 4
    SAMPLE_RATE_44100HZ = 5
    SAMPLE_RATE_48000HZ = 6

    BIT_LENGTH_MIN = -1
    BIT_LENGTH_16BITS = 0x03
    BIT_LENGTH_18BITS = 0x02
    BIT_LENGTH_20BITS = 0x01
    BIT_LENGTH_24BITS = 0x00
    BIT_LENGTH_32BITS = 0x04
    BIT_LENGTH_MAX = 5

    WORK_MODE_NONE = 0
    WORK_MODE_ADC = 1 << 0
    WORK_MODE_DAC = 1 << 1
    WORK_MODE_BOTH = WORK_MODE_ADC | WORK_MODE_DAC
    WORK_MODE_LINE = 1 << 2

    ES_I2S_MIN = -1
    ES_I2S_NORMAL = 0
    ES_I2S_LEFT = 1
    ES_I2S_RIGHT = 2
    ES_I2S_DSP = 3
    ES_I2S_MAX = 4

    ADC_INPUT_MIN = -1
    ADC_INPUT_LINPUT1_RINPUT1 = 0x00
    ADC_INPUT_MIC1 = 0x05
    ADC_INPUT_MIC2 = 0x06
    ADC_INPUT_LINPUT2_RINPUT2 = 0x50
    ADC_INPUT_DIFFERENCE = 0xF0

    DAC_OUTPUT_MIN = -1
    DAC_OUTPUT_LOUT1 = 0x04
    DAC_OUTPUT_LOUT2 = 0x08
    DAC_OUTPUT_SPK = 0x09
    DAC_OUTPUT_ROUT1 = 0x10
    DAC_OUTPUT_ROUT2 = 0x20
    DAC_OUTPUT_ALL = 0x3C

    def __init__(self, i2c, address: int = 0x10) -> None:
        self._i2c = i2c
        self._address = address
        self.is_open = False
        self.enabled = False
        self.codec_mode = self.WORK_MODE_NONE
        self._dac_volume = 0

    def init(self):
        self.write_register(reg.ES8388_MASTERMODE, 0x00)
        self.write_register(reg.ES8388_CHIPPOWER, 0xFF)
        self.write_register(reg.ES8388_DACCONTROL21, 0x80)
        self.write_register(reg.ES8388_CONTROL1, 0x05)
        self.write_register(reg.ES8388_CONTROL2, 0x40)

        # ADC setting
        self.write_register(reg.ES8388_ADCPOWER, 0x00)
        self.write_register(reg.ES8388_ADCCONTROL2, 0x00)
        self.write_register(reg.ES8388_ADCCONTROL3, 0x00)
        self.write_register(reg.ES8388_ADCCONTROL1, 0x88)
        self.write_register(reg.ES8388_ADCCONTROL4, 0x2C)
        self.write_register(reg.ES8388_ADCCONTROL5, 0x02)
        self.write_register(reg.ES8388_ADCCONTROL7, 0x28)
        self.write_register(reg.ES8388_ADCCONTROL8, 0x00)
        self.write_register(reg.ES8388_ADCCONTROL9, 0x00)
        self.write_register(reg.ES8388_ADCCONTROL10, 0xEA)
        self.write_register(reg.ES8388_ADCCONTROL11, 0xC0)
        self.write_register(reg.ES8388_ADCCONTROL12, 0x12)
        self.write_register(reg.ES8388_ADCCONTROL13, 0x06)
        self.write_register(reg.ES8388_ADCCONTROL14, 0xC3)

        # DAC setting
        self.write_register(reg.ES8388_DACPOWER, 0x3F)
        self.write_register(reg.ES8388_DACCONTROL1, 0x18)
        self.write_register(reg.ES8388_DACCONTROL2, 0x02)
        self.write_register(reg.ES8388_DACCONTROL3, 0x00)
        self.write_register(reg.ES8388_DACCONTROL4, 0x05)
        self.write_register(reg.ES8388_DACCONTROL5, 0x05)
        self.write_register(reg.ES8388_DACCONTROL16, 0x00)
        self.write_register(reg.ES8388_DACCONTROL17, 0xD0)
        self.write_register(reg.ES8388_DACCONTROL18, 0x38)
        self.write_register(reg.ES8388_DACCONTROL19, 0x38)
        self.write_register(reg.ES8388_DACCONTROL20, 0xD0)
        self.write_register(reg.ES8388_DACCONTROL21, 0x80)
        self.write_register(reg.ES8388_DACCONTROL24, 0x12)
        self.write_register(reg.ES8388_DACCONTROL25, 0x12)
        self.write_register(reg.ES8388_DACCONTROL26, 0x00)
        self.write_register(reg.ES8388_DACCONTROL27, 0x00)

        # Power up DEM and STM
        self.write_register(reg.ES8388_CHIPPOWER, 0x00)

    def set_adc_volume(self, volume: int) -> None:
        volume = 100 if volume > 100 else volume
        steps = int(((100 - volume) * 192) / 100)
        self.write_register(reg.ES8388_ADCCONTROL8, steps)
        self.write_register(reg.ES8388_ADCCONTROL9, steps)

    def set_dac_volume(self, volume: int) -> None:
        volume = 100 if volume > 100 else volume
        steps = int(((volume) * 33 + 50) / 100)
        steps = 0x21 if steps > 0x21 else steps
        self.write_register(reg.ES8388_DACCONTROL24, steps)
        self.write_register(reg.ES8388_DACCONTROL25, steps)
        self._dac_volume = volume

    def get_dac_volume(self) -> int:
        return self._dac_volume

    def set_dac_output(self, output: int) -> None:
        self.write_register(reg.ES8388_DACPOWER, output)

    def set_mix_source_select(self, lmixsel: int, rmixsel: int) -> None:
        val = 0x00
        val |= (lmixsel & 0x07) << 3
        val |= rmixsel & 0x07
        self.write_register(reg.ES8388_DACCONTROL16, val)

    def set_sample_rate(self, rate):
        adc_fs_ratio = 0x02
        dac_fs_ratio = 0x02
        mclk_div = 0x00

        if rate == self.SAMPLE_RATE_8000HZ:
            adc_fs_ratio = 0x0A
            dac_fs_ratio = 0x0A
        if rate == self.SAMPLE_RATE_11025HZ:
            adc_fs_ratio = 0x07
            dac_fs_ratio = 0x07
        if rate == self.SAMPLE_RATE_16000HZ:
            adc_fs_ratio = 0x06
            dac_fs_ratio = 0x06
        if rate == self.SAMPLE_RATE_24000HZ:
            adc_fs_ratio = 0x04
            dac_fs_ratio = 0x04
        if rate == self.SAMPLE_RATE_32000HZ:
            adc_fs_ratio = 0x03
            dac_fs_ratio = 0x03
        if rate == self.SAMPLE_RATE_44100HZ:
            adc_fs_ratio = 0x02
            dac_fs_ratio = 0x02
            mclk_div = 0x40
        if rate == self.SAMPLE_RATE_48000HZ:
            adc_fs_ratio = 0x02
            dac_fs_ratio = 0x02

        self.write_register(reg.ES8388_MASTERMODE, mclk_div)
        self.write_register(reg.ES8388_ADCCONTROL5, adc_fs_ratio & 0x1F)
        self.write_register(reg.ES8388_DACCONTROL2, dac_fs_ratio & 0x1F)

    def start(self, mode: int) -> None:
        prev_data = self.read_register(reg.ES8388_DACCONTROL21)
        if mode == self.WORK_MODE_LINE:
            self.write_register(
                reg.ES8388_DACCONTROL16, 0x09
            )  # 0x00 audio on LIN1&RIN1,  0x09 LIN2&RIN2 by pass enable
            self.write_register(
                reg.ES8388_DACCONTROL17, 0x50
            )  # left DAC to left mixer enable  and  LIN signal to left mixer enable 0db  : bupass enable
            self.write_register(
                reg.ES8388_DACCONTROL20, 0x50
            )  # right DAC to right mixer enable  and  LIN signal to right mixer enable 0db : bupass enable
            self.write_register(reg.ES8388_DACCONTROL21, 0xC0)  # enable adc
        else:
            self.write_register(reg.ES8388_DACCONTROL21, 0x80)  # enable dac
        data = self.read_register(reg.ES8388_DACCONTROL21)
        if data != prev_data:
            self.write_register(reg.ES8388_CHIPPOWER, 0xF0)  # start state machine
            self.write_register(reg.ES8388_CHIPPOWER, 0x00)  # start state machine
        if mode & self.WORK_MODE_ADC or mode & self.WORK_MODE_LINE:
            self.write_register(reg.ES8388_ADCPOWER, 0x00)  # power up adc and line in
        if mode & self.WORK_MODE_DAC or mode & self.WORK_MODE_LINE:
            self.write_register(reg.ES8388_DACPOWER, 0x3C)  # power up dac and line out
            self.set_voice_mute(False)

    def stop(self, mode: int) -> None:
        if mode == self.WORK_MODE_LINE:
            self.write_register(reg.ES8388_DACCONTROL21, 0x80)  # enable dac
            self.write_register(
                reg.ES8388_DACCONTROL16, 0x00
            )  # 0x00 audio on LIN1&RIN1,  0x09 LIN2&RIN2
            self.write_register(
                reg.ES8388_DACCONTROL17, 0x90
            )  # only left DAC to left mixer enable 0db
            self.write_register(
                reg.ES8388_DACCONTROL20, 0x90
            )  # only right DAC to right mixer enable 0db
        if mode & self.WORK_MODE_DAC:
            self.write_register(reg.ES8388_DACPOWER, 0x00)
            self.set_voice_mute(True)
        if mode & self.WORK_MODE_ADC:
            self.write_register(reg.ES8388_ADCPOWER, 0xFF)
        if mode & self.WORK_MODE_BOTH:
            self.write_register(reg.ES8388_DACCONTROL21, 0x9C)

    def set_adc_dac_volume(self, mode: int, volume: int, dot: int) -> None:
        if volume < -96 or volume > 0:
            volume = -96 if volume < -96 else 0

        dot = 1 if dot >= 5 else 0
        volume = (-volume << 1) + dot
        if mode & self.WORK_MODE_ADC:
            self.write_register(reg.ES8388_ADCCONTROL8, volume)
            self.write_register(reg.ES8388_ADCCONTROL9, volume)
        if mode & self.WORK_MODE_DAC:
            self.write_register(reg.ES8388_DACCONTROL5, volume)
            self.write_register(reg.ES8388_DACCONTROL4, volume)

    def set_voice_mute(self, enable: bool) -> None:
        val = self.read_register(reg.ES8388_DACCONTROL3)
        val &= 0xFB
        self.write_register(reg.ES8388_DACCONTROL3, val | int(enable) << 2)

    def config_fmt(self, mode: int, fmt: int):
        if mode & self.WORK_MODE_ADC:
            val = self.read_register(reg.ES8388_ADCCONTROL4)
            val &= 0xFC
            self.write_register(reg.ES8388_ADCCONTROL4, val | fmt)

        if mode & self.WORK_MODE_DAC:
            val = self.read_register(reg.ES8388_DACCONTROL1)
            val &= 0xF9
            self.write_register(reg.ES8388_DACCONTROL1, val | (fmt << 1))

    def set_mic_gain(self, db: float) -> None:
        # db = 0 to 72
        gain = int(db / 3) if db > 0 else 0
        gain = (gain << 4) + gain
        self.write_register(reg.ES8388_ADCCONTROL1, gain)  # MIC PGA

    def get_bits_enum(self, bits: int) -> int:
        if bits == 16:
            return self.BIT_LENGTH_16BITS
        elif bits == 18:
            return self.BIT_LENGTH_18BITS
        elif bits == 20:
            return self.BIT_LENGTH_20BITS
        elif bits == 24:
            return self.BIT_LENGTH_24BITS
        elif bits == 32:
            return self.BIT_LENGTH_32BITS
        else:
            return self.BIT_LENGTH_MIN

    def set_bits_per_sample(self, mode: int, bits_length: int) -> None:
        bits = self.get_bits_enum(bits_length)

        if mode & self.WORK_MODE_ADC:
            val = self.read_register(reg.ES8388_ADCCONTROL4)
            val &= 0xE3
            # print("val:", val | (bits << 2))
            self.write_register(reg.ES8388_ADCCONTROL4, (val | (bits << 2)) & 0xFF)

        if mode & self.WORK_MODE_DAC:
            val = self.read_register(reg.ES8388_DACCONTROL1)
            val &= 0xC7
            self.write_register(reg.ES8388_DACCONTROL1, val | (bits << 3))

    def pa_power(self, enable: bool) -> None:
        # TODO
        pass

    def open(self):
        # 0x04 mute/0x00 unmute&ramp;
        self.write_register(reg.ES8388_DACCONTROL3, 0x04)
        # Chip Control and Power Management
        self.write_register(reg.ES8388_CONTROL2, 0x50)
        self.write_register(reg.ES8388_CHIPPOWER, 0x00)  # normal all and power up all

        # Disable the internal DLL to improve 8K sample rate
        self.write_register(0x35, 0xA0)
        self.write_register(0x37, 0xD0)
        self.write_register(0x39, 0xD0)

        self.write_register(reg.ES8388_MASTERMODE, 0x00)  # CODEC IN I2S SLAVE MODE

        # dac
        self.write_register(reg.ES8388_DACPOWER, 0xC0)  # disable DAC and disable Lout/Rout/1/2
        self.write_register(
            reg.ES8388_CONTROL1, 0x12
        )  # Enfr=0,Play&Record Mode,(0x17-both of mic&paly)
        # self.write_register(ES8388_CONTROL2, 0)  # LPVrefBuf=0,Pdn_ana=0
        self.write_register(reg.ES8388_DACCONTROL1, 0x18)  # 1a 0x18:16bit iis , 0x00:24
        self.write_register(reg.ES8388_DACCONTROL2, 0x02)  # DACFsMode,SINGLE SPEED; DACFsRatio,256
        self.write_register(
            reg.ES8388_DACCONTROL16, 0x00
        )  # 0x00 audio on LIN1&RIN1,  0x09 LIN2&RIN2
        self.write_register(
            reg.ES8388_DACCONTROL17, 0x90
        )  # only left DAC to left mixer enable 0db
        self.write_register(
            reg.ES8388_DACCONTROL20, 0x90
        )  # only right DAC to right mixer enable 0db
        # set internal ADC and DAC use the same LRCK clock, ADC LRCK as internal LRCK
        self.write_register(reg.ES8388_DACCONTROL21, 0x80)
        self.write_register(reg.ES8388_DACCONTROL23, 0x00)  #  vroi=0
        self.set_adc_dac_volume(self.WORK_MODE_DAC, 0, 0)  # 0db

        self.write_register(
            reg.ES8388_DACCONTROL24, 0x1E
        )  # Set L1 R1 L2 R2 volume. 0x00: -30dB, 0x1E: 0dB, 0x21: 3dB
        self.write_register(reg.ES8388_DACCONTROL25, 0x1E)
        self.write_register(reg.ES8388_DACCONTROL26, 0)
        self.write_register(reg.ES8388_DACCONTROL27, 0)

        # TODO default use DAC_ALL
        tmp = (
            self.DAC_OUTPUT_LOUT1
            | self.DAC_OUTPUT_LOUT2
            | self.DAC_OUTPUT_ROUT1
            | self.DAC_OUTPUT_ROUT2
        )
        self.write_register(reg.ES8388_DACPOWER, tmp)  # 0x3c Enable DAC and Enable Lout/Rout/1/2
        # /* adc */
        self.write_register(reg.ES8388_ADCPOWER, 0xFF)
        self.write_register(reg.ES8388_ADCCONTROL1, 0xBB)  # MIC Left and Right channel PGA gain
        tmp = 0
        # TODO default use ADC LINE1
        # 0x00 LINSEL & RINSEL, LIN1/RIN1 as ADC Input; DSSEL,use one DS Reg11; DSR, LINPUT1-RINPUT1
        self.write_register(reg.ES8388_ADCCONTROL2, self.ADC_INPUT_LINPUT1_RINPUT1)
        self.write_register(reg.ES8388_ADCCONTROL3, 0x02)
        self.write_register(
            reg.ES8388_ADCCONTROL4, 0x0C
        )  # 16 Bits length and I2S serial audio data format
        self.write_register(reg.ES8388_ADCCONTROL5, 0x02)  # ADCFsMode,singel SPEED,RATIO=256
        # ALC for Microphone
        self.set_adc_dac_volume(self.WORK_MODE_ADC, 0, 0)  # 0db
        self.write_register(reg.ES8388_ADCPOWER, 0x09)  # Power on ADC

        self.is_open = True

    def enable(self, enable: bool) -> None:
        if self.is_open is False:
            return

        if self.enabled == enable:
            return

        if enable:
            self.start(self.codec_mode)
            self.pa_power(True)
        else:
            self.stop(self.codec_mode)
            self.pa_power(False)

        self.enabled = enable

    def mute(self, enable: bool) -> None:
        if self.is_open is False:
            return

        self.set_voice_mute(enable)

    def set_vol(self, db_value: float) -> None:
        # TODO
        pass

    def set_fs(self, fs: SampleInfo) -> None:
        if self.is_open is False:
            return

        self.config_fmt(self.WORK_MODE_BOTH, self.ES_I2S_NORMAL)
        self.set_bits_per_sample(self.WORK_MODE_BOTH, fs.bits_per_sample)

    def set_gain(self, db: float) -> None:
        if self.is_open is False:
            return

        self.set_mic_gain(db)

    def close(self) -> None:
        if self.is_open is False:
            return

        self.pa_power(False)
        self.is_open = False

    def dump(self) -> None:
        # if self.is_open == False:
        #     return

        for i in range(0x00, reg.ES8388_DACCONTROL30 + 1):
            value = self.read_register(i)
            print(f"0x{i:02x}: 0x{value:02x}")

    def write_register(self, reg: int, data: int) -> None:
        self._i2c.writeto_mem(self._address, reg, bytes([data]))

    def read_register(self, reg: int) -> int:
        return self._i2c.readfrom_mem(self._address, reg, 1)[0]

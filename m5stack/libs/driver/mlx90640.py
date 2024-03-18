# SPDX-FileCopyrightText: 2019 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import math
import time
import gc

try:
    from typing import List, Optional, Tuple, Union
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_MLX90640.git"

# We match the melexis library naming, and don't want to change
# pylint: disable=invalid-name

eeData = [0] * 832
I2C_READ_LEN = 2048
SCALEALPHA = 0.000001
MLX90640_DEVICEID1 = 0x2407
OPENAIR_TA_SHIFT = 8


class RefreshRate:  # pylint: disable=too-few-public-methods
    """Enum-like class for MLX90640's refresh rate"""

    REFRESH_0_5_HZ = 0b000  # 0.5Hz
    REFRESH_1_HZ = 0b001  # 1Hz
    REFRESH_2_HZ = 0b010  # 2Hz
    REFRESH_4_HZ = 0b011  # 4Hz
    REFRESH_8_HZ = 0b100  # 8Hz
    REFRESH_16_HZ = 0b101  # 16Hz
    REFRESH_32_HZ = 0b110  # 32Hz
    REFRESH_64_HZ = 0b111  # 64Hz


class MLX90640:  # pylint: disable=too-many-instance-attributes
    """Interface to the MLX90640 temperature sensor."""

    kVdd = 0
    vdd25 = 0
    KvPTAT = 0
    KtPTAT = 0
    vPTAT25 = 0
    alphaPTAT = 0
    gainEE = 0
    tgc = 0
    KsTa = 0
    resolutionEE = 0
    calibrationModeEE = 0
    ksTo = [0] * 5
    ct = [0] * 5
    alpha = [0] * 768
    alpha_scale = 0
    offset = [0] * 768
    kta = [0] * 768
    kta_scale = 0
    kv = [0] * 768
    kv_scale = 0
    cpAlpha = [0] * 2
    cpOffset = [0] * 2
    il_chess_c = [0] * 3
    brokenPixels = []
    outlierPixels = []
    cp_kta = 0
    cp_kv = 0

    def __init__(self, i2c_bus, address: int = 0x33) -> None:
        self.i2c_device = i2c_bus
        self.i2c_addr = address
        self._i2cread_words(0x2400, eeData)
        # print(eeData)
        self._extract_parameters()
        self._framebuf = [0] * 768
        self.RefreshRate = RefreshRate()
        self.refresh_rate = self.RefreshRate.REFRESH_0_5_HZ

    @property
    def serial_number(self) -> Tuple[int, int, int]:
        """3-item tuple of hex values that are unique to each MLX90640"""
        serial_words = [0, 0, 0]
        self._i2cread_words(MLX90640_DEVICEID1, serial_words)
        return serial_words

    @property
    def refresh_rate(self) -> int:
        """How fast the MLX90640 will spit out data. Start at lowest speed in
        RefreshRate and then slowly increase I2C clock rate and rate until you
        max out. The sensor does not like it if the I2C host cannot 'keep up'!"""
        control_register = [0]
        self._i2cread_words(0x800D, control_register)
        return (control_register[0] >> 7) & 0x07

    @refresh_rate.setter
    def refresh_rate(self, rate: int) -> None:
        control_register = [0]
        value = (rate & 0x7) << 7
        self._i2cread_words(0x800D, control_register)
        value |= control_register[0] & 0xFC7F
        self._i2cwrite_word(0x800D, value)

    def get_frame(self) -> bytes:
        """Request both 'halves' of a frame from the sensor, merge them
        and calculate the temperature in C for each of 32x24 pixels. Placed
        into the 768-element array passed in!"""
        emissivity = 0.95
        tr = 23.15
        gc.collect()
        mlx90640frame = [0] * 834

        for _ in range(2):
            status = self._get_frame_data(mlx90640frame)
            if status < 0:
                raise RuntimeError("Frame data error")
            # For a MLX90640 in the open air the shift is -8 degC.
            tr = self._get_ta(mlx90640frame) - OPENAIR_TA_SHIFT
            self._calculate_to(mlx90640frame, emissivity, tr, self._framebuf)
        del mlx90640frame
        return self._framebuf

    def _get_frame_data(self, frameData: List[int]) -> int:
        data_ready = 0
        cnt = 0
        status_register = [0]
        control_register = [0]

        while data_ready == 0:
            self._i2cread_words(0x8000, status_register)
            data_ready = status_register[0] & 0x0008
            # print("ready status: 0x%x" % data_ready)

        while (data_ready != 0) and (cnt < 5):
            self._i2cwrite_word(0x8000, 0x0030)
            # print("Read frame", cnt)
            self._i2cread_words(0x0400, frameData, end=832)

            self._i2cread_words(0x8000, status_register)
            data_ready = status_register[0] & 0x0008
            # print("frame ready: 0x%x" % data_ready)
            cnt += 1

        if cnt > 4:
            raise RuntimeError("Too many retries")

        self._i2cread_words(0x800D, control_register)
        frameData[832] = control_register[0]
        frameData[833] = status_register[0] & 0x0001
        return frameData[833]

    def _get_ta(self, frameData: List[int]) -> float:
        vdd = self._get_vdd(frameData)

        ptat = frameData[800]
        if ptat > 32767:
            ptat -= 65536

        ptat_art = frameData[768]
        if ptat_art > 32767:
            ptat_art -= 65536
        ptat_art = (ptat / (ptat * self.alphaPTAT + ptat_art)) * math.pow(2, 18)

        ta = ptat_art / (1 + self.KvPTAT * (vdd - 3.3)) - self.vPTAT25
        ta = ta / self.KtPTAT + 25
        return ta

    def _get_vdd(self, frameData: List[int]) -> int:
        vdd = frameData[810]
        if vdd > 32767:
            vdd -= 65536

        resolution_ram = (frameData[832] & 0x0C00) >> 10
        resolution_correction = math.pow(2, self.resolutionEE) / math.pow(2, resolution_ram)
        vdd = (resolution_correction * vdd - self.vdd25) / self.kVdd + 3.3

        return vdd

    def _calculate_to(
        self, frameData: List[int], emissivity: float, tr: float, result: List[float]
    ) -> None:
        # pylint: disable=too-many-locals, too-many-branches, too-many-statements
        subpage = frameData[833]
        alpha_corr_r = [0] * 4
        ir_data_cp = [0, 0]

        vdd = self._get_vdd(frameData)
        ta = self._get_ta(frameData)

        ta4 = ta + 273.15
        ta4 = ta4 * ta4
        ta4 = ta4 * ta4
        tr4 = tr + 273.15
        tr4 = tr4 * tr4
        tr4 = tr4 * tr4
        ta_tr = tr4 - (tr4 - ta4) / emissivity

        kta_scale = math.pow(2, self.kta_scale)
        kv_scale = math.pow(2, self.kv_scale)
        alpha_scale = math.pow(2, self.alpha_scale)

        alpha_corr_r[0] = 1 / (1 + self.ksTo[0] * 40)
        alpha_corr_r[1] = 1
        alpha_corr_r[2] = 1 + self.ksTo[1] * self.ct[2]
        alpha_corr_r[3] = alpha_corr_r[2] * (1 + self.ksTo[2] * (self.ct[3] - self.ct[2]))

        # --------- Gain calculation -----------------------------------
        gain = frameData[778]
        if gain > 32767:
            gain -= 65536
        gain = self.gainEE / gain

        # --------- to calculation -------------------------------------
        mode = (frameData[832] & 0x1000) >> 5

        ir_data_cp[0] = frameData[776]
        ir_data_cp[1] = frameData[808]
        for i in range(2):
            if ir_data_cp[i] > 32767:
                ir_data_cp[i] -= 65536
            ir_data_cp[i] *= gain

        ir_data_cp[0] -= (
            self.cpOffset[0] * (1 + self.cp_kta * (ta - 25)) * (1 + self.cp_kv * (vdd - 3.3))
        )
        if mode == self.calibrationModeEE:
            ir_data_cp[1] -= (
                self.cpOffset[1] * (1 + self.cp_kta * (ta - 25)) * (1 + self.cp_kv * (vdd - 3.3))
            )
        else:
            ir_data_cp[1] -= (
                (self.cpOffset[1] + self.il_chess_c[0])
                * (1 + self.cp_kta * (ta - 25))
                * (1 + self.cp_kv * (vdd - 3.3))
            )

        for pixel_number in range(768):
            if self._is_pixel_bad(pixel_number):
                # print("Fixing broken pixel %d" % pixel_number)
                result[pixel_number] = -273.15
                continue

            il_pattern = pixel_number // 32 - (pixel_number // 64) * 2
            chess_pattern = il_pattern ^ (pixel_number - (pixel_number // 2) * 2)
            conversion_pattern = (
                (pixel_number + 2) // 4
                - (pixel_number + 3) // 4
                + (pixel_number + 1) // 4
                - pixel_number // 4
            ) * (1 - 2 * il_pattern)

            if mode == 0:
                pattern = il_pattern
            else:
                pattern = chess_pattern

            if pattern == frameData[833]:
                ir_data = frameData[pixel_number]
                if ir_data > 32767:
                    ir_data -= 65536
                ir_data *= gain

                kta = self.kta[pixel_number] / kta_scale
                kv = self.kv[pixel_number] / kv_scale
                ir_data -= (
                    self.offset[pixel_number] * (1 + kta * (ta - 25)) * (1 + kv * (vdd - 3.3))
                )

                if mode != self.calibrationModeEE:
                    ir_data += (
                        self.il_chess_c[2] * (2 * il_pattern - 1)
                        - self.il_chess_c[1] * conversion_pattern
                    )

                ir_data = ir_data - self.tgc * ir_data_cp[subpage]
                ir_data /= emissivity

                alpha_compensated = SCALEALPHA * alpha_scale / self.alpha[pixel_number]
                alpha_compensated *= 1 + self.KsTa * (ta - 25)

                sx = (
                    alpha_compensated
                    * alpha_compensated
                    * alpha_compensated
                    * (ir_data + alpha_compensated * ta_tr)
                )
                sx = math.sqrt(math.sqrt(sx)) * self.ksTo[1]

                to = (
                    math.sqrt(
                        math.sqrt(
                            ir_data / (alpha_compensated * (1 - self.ksTo[1] * 273.15) + sx)
                            + ta_tr
                        )
                    )
                    - 273.15
                )

                if to < self.ct[1]:
                    torange = 0
                elif to < self.ct[2]:
                    torange = 1
                elif to < self.ct[3]:
                    torange = 2
                else:
                    torange = 3

                to = (
                    math.sqrt(
                        math.sqrt(
                            ir_data
                            / (
                                alpha_compensated
                                * alpha_corr_r[torange]
                                * (1 + self.ksTo[torange] * (to - self.ct[torange]))
                            )
                            + ta_tr
                        )
                    )
                    - 273.15
                )

                result[pixel_number] = to

    # pylint: enable=too-many-locals, too-many-branches, too-many-statements

    def _extract_parameters(self) -> None:
        self._extract_vddparameters()
        self._extract_ptatparameters()
        self._extract_gain_parameters()
        self._extract_tgc_parameters()
        self._extract_resolution_parameters()
        self._extract_ks_ta_parameters()
        self._extract_ks_to_parameters()
        self._extract_cpparameters()
        self._extract_alpha_parameters()
        self._extract_offset_parameters()
        self._extract_kta_pixel_parameters()
        self._extract_kv_pixel_parameters()
        self._extract_cilcparameters()
        self._extract_deviating_pixels()

        # debug output
        # print('-'*40)
        # print("kVdd = %d, vdd25 = %d" % (self.kVdd, self.vdd25))
        # print("KvPTAT = %f, KtPTAT = %f, vPTAT25 = %d, alphaPTAT = %f" %
        #      (self.KvPTAT, self.KtPTAT, self.vPTAT25, self.alphaPTAT))
        # print("Gain = %d, Tgc = %f, Resolution = %d" % (self.gainEE, self.tgc, self.resolutionEE))
        # print("KsTa = %f, ksTo = %s, ct = %s" % (self.KsTa, self.ksTo, self.ct))
        # print("cpAlpha:", self.cpAlpha, "cpOffset:", self.cpOffset)
        # print("alpha: ", self.alpha)
        # print("alphascale: ", self.alpha_scale)
        # print("offset: ", self.offset)
        # print("kta:", self.kta)
        # print("kta_scale:", self.kta_scale)
        # print("kv:", self.kv)
        # print("kv_scale:", self.kv_scale)
        # print("calibrationModeEE:", self.calibrationModeEE)
        # print("il_chess_c:", self.il_chess_c)
        # print('-'*40)

    def _extract_vddparameters(self) -> None:
        # extract VDD
        self.kVdd = (eeData[51] & 0xFF00) >> 8
        if self.kVdd > 127:
            self.kVdd -= 256  # convert to signed
        self.kVdd *= 32
        self.vdd25 = eeData[51] & 0x00FF
        self.vdd25 = ((self.vdd25 - 256) << 5) - 8192

    def _extract_ptatparameters(self) -> None:
        # extract PTAT
        self.KvPTAT = (eeData[50] & 0xFC00) >> 10
        if self.KvPTAT > 31:
            self.KvPTAT -= 64
        self.KvPTAT /= 4096
        self.KtPTAT = eeData[50] & 0x03FF
        if self.KtPTAT > 511:
            self.KtPTAT -= 1024
        self.KtPTAT /= 8
        self.vPTAT25 = eeData[49]
        self.alphaPTAT = (eeData[16] & 0xF000) / math.pow(2, 14) + 8

    def _extract_gain_parameters(self) -> None:
        # extract Gain
        self.gainEE = eeData[48]
        if self.gainEE > 32767:
            self.gainEE -= 65536

    def _extract_tgc_parameters(self) -> None:
        # extract Tgc
        self.tgc = eeData[60] & 0x00FF
        if self.tgc > 127:
            self.tgc -= 256
        self.tgc /= 32

    def _extract_resolution_parameters(self) -> None:
        # extract resolution
        self.resolutionEE = (eeData[56] & 0x3000) >> 12

    def _extract_ks_ta_parameters(self) -> None:
        # extract KsTa
        self.KsTa = (eeData[60] & 0xFF00) >> 8
        if self.KsTa > 127:
            self.KsTa -= 256
        self.KsTa /= 8192

    def _extract_ks_to_parameters(self) -> None:
        # extract ksTo
        step = ((eeData[63] & 0x3000) >> 12) * 10
        self.ct[0] = -40
        self.ct[1] = 0
        self.ct[2] = (eeData[63] & 0x00F0) >> 4
        self.ct[3] = (eeData[63] & 0x0F00) >> 8
        self.ct[2] *= step
        self.ct[3] = self.ct[2] + self.ct[3] * step

        ks_to_scale = (eeData[63] & 0x000F) + 8
        ks_to_scale = 1 << ks_to_scale

        self.ksTo[0] = eeData[61] & 0x00FF
        self.ksTo[1] = (eeData[61] & 0xFF00) >> 8
        self.ksTo[2] = eeData[62] & 0x00FF
        self.ksTo[3] = (eeData[62] & 0xFF00) >> 8

        for i in range(4):
            if self.ksTo[i] > 127:
                self.ksTo[i] -= 256
            self.ksTo[i] /= ks_to_scale
        self.ksTo[4] = -0.0002

    def _extract_cpparameters(self) -> None:
        # extract CP
        offset_sp = [0] * 2
        alpha_sp = [0] * 2

        alpha_scale = ((eeData[32] & 0xF000) >> 12) + 27

        offset_sp[0] = eeData[58] & 0x03FF
        if offset_sp[0] > 511:
            offset_sp[0] -= 1024

        offset_sp[1] = (eeData[58] & 0xFC00) >> 10
        if offset_sp[1] > 31:
            offset_sp[1] -= 64
        offset_sp[1] += offset_sp[0]

        alpha_sp[0] = eeData[57] & 0x03FF
        if alpha_sp[0] > 511:
            alpha_sp[0] -= 1024
        alpha_sp[0] /= math.pow(2, alpha_scale)

        alpha_sp[1] = (eeData[57] & 0xFC00) >> 10
        if alpha_sp[1] > 31:
            alpha_sp[1] -= 64
        alpha_sp[1] = (1 + alpha_sp[1] / 128) * alpha_sp[0]

        cp_kta = eeData[59] & 0x00FF
        if cp_kta > 127:
            cp_kta -= 256
        kta_scale1 = ((eeData[56] & 0x00F0) >> 4) + 8
        self.cp_kta = cp_kta / math.pow(2, kta_scale1)

        cp_kv = (eeData[59] & 0xFF00) >> 8
        if cp_kv > 127:
            cp_kv -= 256
        kv_scale = (eeData[56] & 0x0F00) >> 8
        self.cp_kv = cp_kv / math.pow(2, kv_scale)

        self.cpAlpha[0] = alpha_sp[0]
        self.cpAlpha[1] = alpha_sp[1]
        self.cpOffset[0] = offset_sp[0]
        self.cpOffset[1] = offset_sp[1]

    def _extract_alpha_parameters(self) -> None:
        # extract alpha
        acc_rem_scale = eeData[32] & 0x000F
        acc_column_scale = (eeData[32] & 0x00F0) >> 4
        acc_row_scale = (eeData[32] & 0x0F00) >> 8
        alpha_scale = ((eeData[32] & 0xF000) >> 12) + 30
        alpha_ref = eeData[33]
        gc.collect()
        acc_row = [0] * 24
        acc_column = [0] * 32
        alpha_temp = [0] * 768

        for i in range(6):
            p = i * 4
            acc_row[p + 0] = eeData[34 + i] & 0x000F
            acc_row[p + 1] = (eeData[34 + i] & 0x00F0) >> 4
            acc_row[p + 2] = (eeData[34 + i] & 0x0F00) >> 8
            acc_row[p + 3] = (eeData[34 + i] & 0xF000) >> 12

        for i in range(24):
            if acc_row[i] > 7:
                acc_row[i] -= 16

        for i in range(8):
            p = i * 4
            acc_column[p + 0] = eeData[40 + i] & 0x000F
            acc_column[p + 1] = (eeData[40 + i] & 0x00F0) >> 4
            acc_column[p + 2] = (eeData[40 + i] & 0x0F00) >> 8
            acc_column[p + 3] = (eeData[40 + i] & 0xF000) >> 12

        for i in range(32):
            if acc_column[i] > 7:
                acc_column[i] -= 16

        for i in range(24):
            for j in range(32):
                p = 32 * i + j
                alpha_temp[p] = (eeData[64 + p] & 0x03F0) >> 4
                if alpha_temp[p] > 31:
                    alpha_temp[p] -= 64
                alpha_temp[p] *= 1 << acc_rem_scale
                alpha_temp[p] += (
                    alpha_ref + (acc_row[i] << acc_row_scale) + (acc_column[j] << acc_column_scale)
                )
                alpha_temp[p] /= math.pow(2, alpha_scale)
                alpha_temp[p] -= self.tgc * (self.cpAlpha[0] + self.cpAlpha[1]) / 2
                alpha_temp[p] = SCALEALPHA / alpha_temp[p]
        # print("alpha_temp: ", alpha_temp)

        temp = max(alpha_temp)
        # print("temp", temp)

        alpha_scale = 0
        while temp < 32768:
            temp *= 2
            alpha_scale += 1

        for i in range(768):
            temp = alpha_temp[i] * math.pow(2, alpha_scale)
            self.alpha[i] = int(temp + 0.5)

        del acc_row
        del acc_column
        del alpha_temp
        gc.collect()
        self.alpha_scale = alpha_scale

    def _extract_offset_parameters(self) -> None:
        # extract offset
        occ_row = [0] * 24
        occ_column = [0] * 32

        occ_rem_scale = eeData[16] & 0x000F
        occ_column_scale = (eeData[16] & 0x00F0) >> 4
        occ_row_scale = (eeData[16] & 0x0F00) >> 8
        offset_ref = eeData[17]
        if offset_ref > 32767:
            offset_ref -= 65536

        for i in range(6):
            p = i * 4
            occ_row[p + 0] = eeData[18 + i] & 0x000F
            occ_row[p + 1] = (eeData[18 + i] & 0x00F0) >> 4
            occ_row[p + 2] = (eeData[18 + i] & 0x0F00) >> 8
            occ_row[p + 3] = (eeData[18 + i] & 0xF000) >> 12

        for i in range(24):
            if occ_row[i] > 7:
                occ_row[i] -= 16

        for i in range(8):
            p = i * 4
            occ_column[p + 0] = eeData[24 + i] & 0x000F
            occ_column[p + 1] = (eeData[24 + i] & 0x00F0) >> 4
            occ_column[p + 2] = (eeData[24 + i] & 0x0F00) >> 8
            occ_column[p + 3] = (eeData[24 + i] & 0xF000) >> 12

        for i in range(32):
            if occ_column[i] > 7:
                occ_column[i] -= 16

        for i in range(24):
            for j in range(32):
                p = 32 * i + j
                self.offset[p] = (eeData[64 + p] & 0xFC00) >> 10
                if self.offset[p] > 31:
                    self.offset[p] -= 64
                self.offset[p] *= 1 << occ_rem_scale
                self.offset[p] += (
                    offset_ref
                    + (occ_row[i] << occ_row_scale)
                    + (occ_column[j] << occ_column_scale)
                )
        del occ_row
        del occ_column
        gc.collect()

    def _extract_kta_pixel_parameters(self) -> None:  # pylint: disable=too-many-locals
        # extract KtaPixel
        gc.collect()
        kta_rc = [0] * 4
        kta_temp = [0] * 768

        kta_ro_co = (eeData[54] & 0xFF00) >> 8
        if kta_ro_co > 127:
            kta_ro_co -= 256
        kta_rc[0] = kta_ro_co

        kta_re_co = eeData[54] & 0x00FF
        if kta_re_co > 127:
            kta_re_co -= 256
        kta_rc[2] = kta_re_co

        kta_ro_ce = (eeData[55] & 0xFF00) >> 8
        if kta_ro_ce > 127:
            kta_ro_ce -= 256
        kta_rc[1] = kta_ro_ce

        kta_re_ce = eeData[55] & 0x00FF
        if kta_re_ce > 127:
            kta_re_ce -= 256
        kta_rc[3] = kta_re_ce

        kta_scale1 = ((eeData[56] & 0x00F0) >> 4) + 8
        kta_scale2 = eeData[56] & 0x000F

        for i in range(24):
            for j in range(32):
                p = 32 * i + j
                split = 2 * (p // 32 - (p // 64) * 2) + p % 2
                kta_temp[p] = (eeData[64 + p] & 0x000E) >> 1
                if kta_temp[p] > 3:
                    kta_temp[p] -= 8
                kta_temp[p] *= 1 << kta_scale2
                kta_temp[p] += kta_rc[split]
                kta_temp[p] /= math.pow(2, kta_scale1)
                # kta_temp[p] = kta_temp[p] * mlx90640->offset[p];

        temp = abs(kta_temp[0])
        for kta in kta_temp:
            temp = max(temp, abs(kta))

        kta_scale1 = 0
        while temp < 64:
            temp *= 2
            kta_scale1 += 1

        for i in range(768):
            temp = kta_temp[i] * math.pow(2, kta_scale1)
            if temp < 0:
                self.kta[i] = int(temp - 0.5)
            else:
                self.kta[i] = int(temp + 0.5)
        del kta_rc
        del kta_temp
        gc.collect()
        self.kta_scale = kta_scale1

    def _extract_kv_pixel_parameters(self) -> None:
        gc.collect()
        kv_t = [0] * 4
        kv_temp = [0] * 768

        kv_ro_co = (eeData[52] & 0xF000) >> 12
        if kv_ro_co > 7:
            kv_ro_co -= 16
        kv_t[0] = kv_ro_co

        kv_re_co = (eeData[52] & 0x0F00) >> 8
        if kv_re_co > 7:
            kv_re_co -= 16
        kv_t[2] = kv_re_co

        kv_ro_ce = (eeData[52] & 0x00F0) >> 4
        if kv_ro_ce > 7:
            kv_ro_ce -= 16
        kv_t[1] = kv_ro_ce

        kv_re_ce = eeData[52] & 0x000F
        if kv_re_ce > 7:
            kv_re_ce -= 16
        kv_t[3] = kv_re_ce

        kv_scale = (eeData[56] & 0x0F00) >> 8

        for i in range(24):
            for j in range(32):
                p = 32 * i + j
                split = 2 * (p // 32 - (p // 64) * 2) + p % 2
                kv_temp[p] = kv_t[split]
                kv_temp[p] /= math.pow(2, kv_scale)
                # kv_temp[p] = kv_temp[p] * mlx90640->offset[p];

        temp = abs(kv_temp[0])
        for kv in kv_temp:
            temp = max(temp, abs(kv))

        kv_scale = 0
        while temp < 64:
            temp *= 2
            kv_scale += 1

        for i in range(768):
            temp = kv_temp[i] * math.pow(2, kv_scale)
            if temp < 0:
                self.kv[i] = int(temp - 0.5)
            else:
                self.kv[i] = int(temp + 0.5)
        del kv_t
        del kv_temp
        gc.collect()
        self.kv_scale = kv_scale

    def _extract_cilcparameters(self) -> None:
        il_chess_c = [0] * 3

        self.calibrationModeEE = (eeData[10] & 0x0800) >> 4
        self.calibrationModeEE = self.calibrationModeEE ^ 0x80

        il_chess_c[0] = eeData[53] & 0x003F
        if il_chess_c[0] > 31:
            il_chess_c[0] -= 64
        il_chess_c[0] /= 16.0

        il_chess_c[1] = (eeData[53] & 0x07C0) >> 6
        if il_chess_c[1] > 15:
            il_chess_c[1] -= 32
        il_chess_c[1] /= 2.0

        il_chess_c[2] = (eeData[53] & 0xF800) >> 11
        if il_chess_c[2] > 15:
            il_chess_c[2] -= 32
        il_chess_c[2] /= 8.0

        self.il_chess_c = il_chess_c

    def _extract_deviating_pixels(self) -> None:
        # pylint: disable=too-many-branches
        pix_cnt = 0

        while (pix_cnt < 768) and (len(self.brokenPixels) < 5) and (len(self.outlierPixels) < 5):
            if eeData[pix_cnt + 64] == 0:
                self.brokenPixels.append(pix_cnt)
            elif (eeData[pix_cnt + 64] & 0x0001) != 0:
                self.outlierPixels.append(pix_cnt)
            pix_cnt += 1

        if len(self.brokenPixels) > 4:
            raise RuntimeError("More than 4 broken pixels")
        if len(self.outlierPixels) > 4:
            raise RuntimeError("More than 4 outlier pixels")
        if (len(self.brokenPixels) + len(self.outlierPixels)) > 4:
            raise RuntimeError("More than 4 faulty pixels")
        # print("Found %d broken pixels, %d outliers"
        #         % (len(self.brokenPixels), len(self.outlierPixels)))

        for broken_pixel1, broken_pixel2 in self._unique_list_pairs(self.brokenPixels):
            if self._are_pixels_adjacent(broken_pixel1, broken_pixel2):
                raise RuntimeError("Adjacent broken pixels")

        for outlier_pixel1, outlier_pixel2 in self._unique_list_pairs(self.outlierPixels):
            if self._are_pixels_adjacent(outlier_pixel1, outlier_pixel2):
                raise RuntimeError("Adjacent outlier pixels")

        for broken_pixel in self.brokenPixels:
            for outlier_pixel in self.outlierPixels:
                if self._are_pixels_adjacent(broken_pixel, outlier_pixel):
                    raise RuntimeError("Adjacent broken and outlier pixels")

    def _unique_list_pairs(self, inputList: List[int]) -> Tuple[int, int]:
        # pylint: disable=no-self-use
        for i, list_value1 in enumerate(inputList):
            for list_value2 in inputList[i + 1 :]:
                yield list_value1, list_value2

    def _are_pixels_adjacent(self, pix1: int, pix2: int) -> bool:
        # pylint: disable=no-self-use
        pix_pos_dif = pix1 - pix2

        if -34 < pix_pos_dif < -30:
            return True
        if -2 < pix_pos_dif < 2:
            return True
        if 30 < pix_pos_dif < 34:
            return True

        return False

    def _is_pixel_bad(self, pixel: int) -> bool:
        if pixel in self.brokenPixels or pixel in self.outlierPixels:
            return True

        return False

    def _i2cwrite_word(self, writeAddress: int, data: int) -> None:
        cmd = bytearray(4)
        cmd[0] = writeAddress >> 8
        cmd[1] = writeAddress & 0x00FF
        cmd[2] = data >> 8
        cmd[3] = data & 0x00FF
        data_check = [0]

        self.i2c_device.writeto(self.i2c_addr, cmd, True)
        # print("Wrote:", [hex(i) for i in cmd])
        time.sleep(0.001)
        self._i2cread_words(writeAddress, data_check)
        # print("data_check: 0x%x" % data_check[0])
        # if (data_check != data):
        #    return -2

    def _i2cread_words(
        self,
        addr: int,
        buffer: Union[int, List[int]],
        *,
        end: Optional[int] = None,
    ) -> None:
        if end is None:
            readwords = len(buffer)
        else:
            readwords = end

        # print("remainingWords: {}".format(readwords))
        gc.collect()
        # addrbuf = bytearray(2)
        # inbuf = bytearray(2 * readwords)
        # addrbuf[0] = addr >> 8  # MSB
        # addrbuf[1] = addr & 0xFF  # LSB
        self.i2c_device.writeto(self.i2c_addr, struct.pack(">H", addr), False)
        time.sleep_ms(1)
        inbuf = memoryview(bytearray(2 * readwords))
        self.i2c_device.readfrom_into(self.i2c_addr, inbuf)
        outdata = list(struct.unpack(">" + "H" * readwords, inbuf))
        for i in range(0, len(outdata)):
            buffer[i] = outdata[i]

        del inbuf
        del outdata
        gc.collect()

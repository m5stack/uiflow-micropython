# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   dds.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import I2C
import struct
import time
from micropython import const


class DDSUnit:
    """! DDS is a signal source Unit. It uses the AD9833 programmable waveform generator + STM32F0 micro controller.

    @en DDS is a signal source Unit. It uses the AD9833 programmable waveform generator + STM32F0 micro controller. Based on I2C communication interface (addr:0x31) It can easily control the signal source to output multiple waveforms (sine wave, triangle wave, square wave output, sawtooth wave, signal output amplitude 0-0.6V) and adjust the frequency and phase.
    @cn DDS是一个信号源单元。它使用AD9833可编程波形发生器+STM32F0微控制器。基于I2C通信接口（addr:0x31）它可以轻松控制信号源输出多种波形（正弦波、三角波、方波输出、锯齿波、信号输出幅度0-0.6V）并调整频率和相位。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/dds
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/dds/dds_01.webp
    @category unit

    @example
        from hardware import *
        from unit import DDSUnit
        i2c = I2C(1, scl=33, sda=32)
        dds = DDSUnit(i2c)
        dds.quick_output(DDSUnit.WAVE_SINE, 1000, 0)

        for x in i2c.readfrom_mem(0x31, 0x30, 6): print('%02X' %x);

    @attr WAVE_SINE Sine wave output.
    @attr WAVE_TRIANGLE Triangle wave output.
    @attr WAVE_SQUARE Square wave output.
    @attr WAVE_SAWTOOTH Sawtooth wave output.
    @attr WAVE_DC DC wave output.

    @attr SLEEP_MODE_1 Disable mclk but keep dac.
    @attr SLEEP_MODE_2 Disable mclk and dac.

    """

    DDS_DESC_ADDR = const(0x10)
    DDS_MODE_ADDR = const(0x20)
    DDS_CTRL_ADDR = const(0x21)
    DDS_FREQ_ADDR = const(0x30)
    DDS_PHASE_ADDR = const(0x34)

    DDS_FMCLK = const(10000000)

    WAVE_SINE = 0b001
    WAVE_TRIANGLE = 0b010
    WAVE_SQUARE = 0b011
    WAVE_SAWTOOTH = 0b100
    WAVE_DC = 0b101

    SLEEP_MODE_NONE = 0
    SLEEP_MODE_1 = 1
    SLEEP_MODE_2 = 2

    def __init__(self, i2c: I2C, address: int | list | tuple = 0x31) -> None:
        """! Initialize the DDSUnit.

        @param i2c I2C port to use.
        @param address I2C address of the DDSUnit.
        """
        self.i2c = i2c
        self.addr = address
        self._available()

    def _available(self) -> None:
        """! Check if DDSUnit is available on the I2C bus.

        Raises:
            Exception: If the DDSUnit is not found.
        """
        if self.addr not in self.i2c.scan():
            raise Exception("DDSUnit not found on I2C bus.")

    def set_freq(self, index: int = 0, freq: int = 1000):
        """! Set the frequency of the DDS.

        @en %1 Set the frequency %2 of the DDS to %3 Hz.
        @cn %1 将DDS的频率%2设置为%3 Hz。

        @param index The register number of the DDS, range from 0 to 1.
        @param freq The frequency of the DDS in Hz.
        """
        buf = bytearray(4)
        freq = int(freq * 268435456 / self.DDS_FMCLK)
        buf[0] |= ((freq >> 24) & 0xFF | 0xC0) if index == 1 else ((freq >> 24) & 0xFF | 0x80)
        buf[1] |= (freq >> 16) & 0xFF
        buf[2] |= (freq >> 8) & 0xFF
        buf[3] |= (freq >> 0) & 0xFF
        self.i2c.writeto_mem(self.addr, self.DDS_FREQ_ADDR, buf)

    def set_phase(self, index: int = 0, phase: int = 0):
        """! Set the phase of the DDS.

        @en %1 Set the phase %2 of the DDS to %3 degrees.
        @cn %1 将DDS的相位%2设置为%3度。

        @param index The register number of the DDS, range from 0 to 1.
        @param phase The phase of the DDS in degrees.
        """
        buf = bytearray(2)
        phase = int(phase * 2048 / 360)
        buf[0] |= ((phase >> 8) & 0xFF | 0xC0) if index == 1 else ((phase >> 8) & 0xFF | 0x80)
        buf[1] |= phase & 0xFF
        self.i2c.writeto_mem(self.addr, self.DDS_PHASE_ADDR, buf)

    def set_freq_phase(self, f_index: int = 0, freq: int = 1000, p_index: int = 0, phase: int = 0):
        """! Set the frequency and phase of the DDS.

        @en %1 Set freq %2 to %3 Hz and phase %4 to %5 degrees.
        @cn %1 将频率%2设置为%3 Hz，相位%4设置为%5度。

        @param f_index The register number of the frequency. range from 0 to 1.
        @param freq The frequency of the DDS in Hz.
        @param p_index The register number of the phase. range from 0 to 1.
        @param phase The phase of the DDS in degrees.
        """
        buf = bytearray(6)
        freq = int(freq * 268435456 / self.DDS_FMCLK)
        buf[0] |= ((freq >> 24) & 0xFF | 0xC0) if f_index == 1 else ((freq >> 24) & 0xFF | 0x80)
        buf[1] |= (freq >> 16) & 0xFF
        buf[2] |= (freq >> 8) & 0xFF
        buf[3] |= (freq >> 0) & 0xFF

        phase = int(phase * 2048 / 360)
        buf[4] |= ((phase >> 8) & 0xFF | 0xC0) if p_index == 1 else ((phase >> 8) & 0xFF | 0x80)
        buf[5] |= phase & 0xFF
        self.i2c.writeto_mem(self.addr, self.DDS_FREQ_ADDR, buf)

    def set_mode(self, mode: int = WAVE_SINE):
        """! Set the output mode of the DDS.

        @en %1 Set the output mode to %2.
        @cn %1 将输出模式设置为%2。

        @param mode [field_dropdown] The output mode of the DDS.
            @options {
                    [Sine, DDSUnit.WAVE_SINE]
                    [Triangle, DDSUnit.WAVE_TRIANGLE]
                    [Square, DDSUnit.WAVE_SQUARE]
                    [Sawtooth, DDSUnit.WAVE_SAWTOOTH]
                    [DC, DDSUnit.WAVE_DC]
            }
        """
        self.i2c.writeto_mem(self.addr, self.DDS_MODE_ADDR, struct.pack("B", 0x80 | mode))

    def set_ctrl(
        self,
        f_index_sel: int = 0,
        p_index_sel: int = 0,
        disable_mclk=False,
        disable_dac=False,
        reset=False,
    ) -> None:
        """! Set the control bytes of the DDS.

        @en %1 Set the control register of the DDS. Frequency select: %2, Phase select: %3, Disable MCLK: %4, Disable DAC: %5, Reset: %6.
        @cn %1 设置DDS的控制寄存器。频率选择：%2，相位选择：%3，禁用MCLK：%4，禁用DAC：%5，复位：%6。

        @param f_index_sel The frequency register select. range from 0 to 1.
        @param p_index_sel The phase register select. range from 0 to 1.
        @param disable_mclk [field_switch] disable the MCLK.
        @param disable_dac [field_switch] disable the DAC.
        @param reset [field_switch] reset the DDS. If is true, other parameters will be ignored.
        """
        if reset:
            self.reset()
            return

        ctrlbyte = 0x80
        if f_index_sel == 1:
            ctrlbyte |= 0x40
        if p_index_sel == 1:
            ctrlbyte |= 0x20
        if disable_mclk:
            ctrlbyte |= 0x10
        if disable_dac:
            ctrlbyte |= 0x08

        self.i2c.writeto_mem(self.addr, self.DDS_CTRL_ADDR, struct.pack("B", ctrlbyte))

    def select_freq_reg(self, index: int = 0):
        """! Select the frequency register of the DDS.

        @en %1 Select the frequency register of the DDS to %2.
        @cn %1 将DDS的频率寄存器选择为%2。

        @param index The index of the frequency register. range from 0 to 1
        """
        reg = self.i2c.read_u8(self.DDS_CTRL_ADDR)
        reg &= ~0x40
        reg |= (0x80 | 0x40) if index == 1 else (0x80 | 0x00)
        self.i2c.writeto_mem(self.addr, self.DDS_CTRL_ADDR, struct.pack("B", reg))

    def select_phase_reg(self, index: int = 0):
        """!  Select the phase register of the DDS.

        @en %1 Select the phase register of the DDS to %2.
        @cn %1 将DDS的相位寄存器选择为%2。

        @param index The index of the phase register. range from 0 to 1
        """
        reg = self.i2c.read_u8(self.DDS_CTRL_ADDR)
        reg &= ~0x20
        reg |= (0x80 | 0x20) if index == 1 else (0x80 | 0x00)
        self.i2c.writeto_mem(self.addr, self.DDS_CTRL_ADDR, struct.pack("B", reg))

    def quick_output(self, mode: int = WAVE_SINE, freq: int = 1000, phase: int = 0):
        """! Quickly set the output mode, frequency and phase of the DDS.

        @en %1 Quickly set the output mode to %2, frequency to %3 Hz and phase to %4 degrees.
        @cn %1 快速将输出模式设置为%2，频率设置为%3 Hz，相位设置为%4度。

        @param mode [field_dropdown] The output mode of the DDS.
            @options {
                    [Sine, DDSUnit.WAVE_SINE]
                    [Triangle, DDSUnit.WAVE_TRIANGLE]
                    [Square, DDSUnit.WAVE_SQUARE]
                    [Sawtooth, DDSUnit.WAVE_SAWTOOTH]
                    [DC, DDSUnit.WAVE_DC]
            }
        @param freq The frequency of the DDS in Hz.
        @param phase The phase of the DDS in degrees.
        """
        if mode <= self.WAVE_SQUARE:
            self.set_freq_phase(0, freq, 0, phase)
        self.i2c.writeto_mem(self.addr, self.DDS_MODE_ADDR, struct.pack("B", 0x80 | mode))
        self.i2c.writeto_mem(self.addr, self.DDS_CTRL_ADDR, struct.pack("B", 0x80))

    def output(self, f_index: int = 0, p_index: int = 0):
        """! Output the DDS signal.

        @en %1 Output the DDS signal with freq index %2 and phase index %3.
        @cn %1 输出DDS信号，频率%2，相位%3。

        @param f_index The index of the frequency register. range from 0 to 1
        @param p_index The index of the phase register. range from 0 to 1
        """
        reg = self.i2c.readfrom_mem(self.addr, self.DDS_CTRL_ADDR, 1)[0]
        reg &= ~0x60
        reg |= (0x80 | 0x40) if f_index == 1 else (0x80 | 0x00)
        reg |= (0x80 | 0x20) if p_index == 1 else (0x80 | 0x00)
        self.i2c.writeto_mem(self.addr, self.DDS_CTRL_ADDR, struct.pack("B", reg))

    def set_sleep_mode(self, mode: int = WAVE_SINE):
        """! Set the sleep mode of the DDS.

        @en %1 Set the sleep mode of the DDS to %2.
        @cn %1 将DDS的睡眠级别设置为%2。

        @param mode [field_dropdown] The sleep mode of the DDS.
            @options {
                    [None, DDSUnit.SLEEP_MODE_NONE]
                    [Disable MCLK, DDSUnit.SLEEP_MODE_1]
                    [Disable MCLK and DAC, DDSUnit.SLEEP_MODE_2]
            }
        """
        reg = self.i2c.readfrom_mem(self.addr, self.DDS_CTRL_ADDR, 1)[0]
        reg &= ~0x18
        reg |= (0x80 | 0x10) if mode == self.SLEEP_MODE_1 else (0x80 | 0x00)
        reg |= (0x80 | 0x08) if mode == self.SLEEP_MODE_2 else (0x80 | 0x00)
        self.i2c.writeto_mem(self.addr, self.DDS_CTRL_ADDR, struct.pack("B", reg))

    def reset(self):
        """! Reset the DDS.

        @en %1 Reset the DDS.
        @cn %1 重置DDS。
        """
        self.i2c.writeto_mem(self.addr, self.DDS_CTRL_ADDR, struct.pack("B", 0x80 | 0x04))

    def _read_reg_data(self, reg: int = 0, num: int = 0) -> bytearray:
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self.i2c.writeto(self.addr, buf)
        buf = bytearray(num)
        self.i2c.readfrom_into(self.addr, buf)
        return buf

    def _write_reg_data(self, reg, byte_lst):
        buf = bytearray(1 + len(byte_lst))
        buf[0] = reg
        buf[1:] = bytes(byte_lst)
        time.sleep_ms(1)
        self.i2c.writeto(self.addr, buf)

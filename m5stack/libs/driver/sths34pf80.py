# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   ExampleClass
@Time    :   2024/07/15
@Author  :   TINYU
@E-mail  :   tinyu@m5stack.com
@License :   MIT
"""

import time
import sys
from machine import I2C
from micropython import const, schedule

if sys.platform != "esp32":
    from typing import Literal

STHS34PF80_I2C_ADDRESS = const(0x5A)
STHS34PF80_ID = const(0xD3)

STHS34PF80_LPF1 = const(0x0C)
STHS34PF80_LPF2 = const(0x0D)
STHS34PF80_WHOAMI = const(0x0F)
STHS34PF80_AVG_TRIM = const(0x10)
STHS34PF80_CTRL0 = const(0x17)
STHS34PF80_SENS_DATA = const(0x1D)
STHS34PF80_CTRL1 = const(0x20)
STHS34PF80_CTRL2 = const(0x21)
STHS34PF80_CTRL3 = const(0x22)
STHS34PF80_STATUS = const(0x23)
STHS34PF80_FUNC_STATUS = const(0x25)
STHS34PF80_TOBJECT_L = const(0x26)
STHS34PF80_TOBJECT_H = const(0x27)
STHS34PF80_TAMBIENT_L = const(0x28)
STHS34PF80_TAMBIENT_H = const(0x29)
STHS34PF80_TOBJ_COMP_L = const(0x38)
STHS34PF80_TOBJ_COMP_H = const(0x39)
STHS34PF80_TPRESENCE_L = const(0x3A)
STHS34PF80_TPRESENCE_H = const(0x3B)
STHS34PF80_TMOTION_L = const(0x3C)
STHS34PF80_TMOTION_H = const(0x3D)
STHS34PF80_TAMB_SHOCK_L = const(0x3E)
STHS34PF80_TAMB_SHOCK_H = const(0x3F)

# These registers are accessible when the FUNC_CFG_ACCESS bit in CTRL2 is set to 1.
STHS34PF80_FUNC_CFG_ADDR = const(0x08)
STHS34PF80_FUNC_CFG_DATA = const(0x09)
STHS34PF80_PAGE_RW = const(0x11)

# Embedded functions registers
# Detailed write and read procedures for the embedded functions registers are explained in application note AN5867 (refer to sections 2.1.1 and 2.1.2, respectively)
STHS34PF80_PRESENCE_THS = const(0x20)
STHS34PF80_MOTION_THS = const(0x22)
STHS34PF80_TAMB_SHOCK_THS = const(0x24)
STHS34PF80_HYST_MOTION = const(0x26)
STHS34PF80_HYST_PRESENCE = const(0x27)
STHS34PF80_ALGO_CONFIG = const(0x28)
STHS34PF80_HYST_TAMB_SHOCK = const(0x29)
STHS34PF80_RESET_ALGO = const(0x2A)


class STHS34PF80:
    """! UNIT TMOS is a Slide Potentiometer with color indicator.

    @en UNIT TMOS 英文介绍
    @cn UNIT TMOS 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/tmos
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/tmos/tmos_01.webp
    @category unit

    @example

    """

    AMBIENT_TEMPERATURE_SHOCK_DETECT = const(0)
    MOTION_DETECT = const(1)
    PRESENCE_DETECT = const(2)
    AMBIENT_TEMPERATURE_SHOCK_NOT_DETECTED = const(3)
    MOTION_NOT_DETECTED = const(4)
    PRESENCE_NOT_DETECTED = const(5)

    # Table 17. Low-pass filter configuration
    STHS34PF80_LPF_ODR_DIV_9: int = const(0)
    STHS34PF80_LPF_ODR_DIV_20: int = const(1)
    STHS34PF80_LPF_ODR_DIV_50: int = const(2)
    STHS34PF80_LPF_ODR_DIV_100: int = const(3)
    STHS34PF80_LPF_ODR_DIV_200: int = const(4)
    STHS34PF80_LPF_ODR_DIV_400: int = const(5)
    STHS34PF80_LPF_ODR_DIV_800: int = const(6)

    # Table 18. Averaging selection for ambient temperature
    STHS34PF80_AVG_T_8: int = const(0)
    STHS34PF80_AVG_T_4: int = const(1)
    STHS34PF80_AVG_T_2: int = const(2)
    STHS34PF80_AVG_T_1: int = const(3)

    # Table 19. Averaging selection for object temperature and noise
    STHS34PF80_AVG_TMOS_2: int = const(0)
    STHS34PF80_AVG_TMOS_8: int = const(1)
    STHS34PF80_AVG_TMOS_32: int = const(2)
    STHS34PF80_AVG_TMOS_128: int = const(3)
    STHS34PF80_AVG_TMOS_256: int = const(4)
    STHS34PF80_AVG_TMOS_512: int = const(5)
    STHS34PF80_AVG_TMOS_1024: int = const(6)
    STHS34PF80_AVG_TMOS_2048: int = const(7)

    # Datasheet 10.5. Gain mode
    STHS34PF80_GAIN_WIDE_MODE: int = const(0)
    STHS34PF80_GAIN_DEFAULT_MODE: int = const(7)

    # Table 20. ODR configuration
    STHS34PF80_TMOS_ODR_OFF: int = const(0)
    STHS34PF80_TMOS_ODR_AT_0Hz25: int = const(1)
    STHS34PF80_TMOS_ODR_AT_0Hz50: int = const(2)
    STHS34PF80_TMOS_ODR_AT_1Hz: int = const(3)
    STHS34PF80_TMOS_ODR_AT_2Hz: int = const(4)
    STHS34PF80_TMOS_ODR_AT_4Hz: int = const(5)
    STHS34PF80_TMOS_ODR_AT_8Hz: int = const(6)
    STHS34PF80_TMOS_ODR_AT_15Hz: int = const(7)
    STHS34PF80_TMOS_ODR_AT_30Hz: int = const(8)

    # Shot mode set
    STHS34PF80_TMOS_IDLE_MODE: int = const(0)
    STHS34PF80_TMOS_ONE_SHOT: int = const(1)

    # Function config access
    STHS34PF80_MAIN_MEM_BANK: int = const(0)
    STHS34PF80_EMBED_FUNC_MEM_BANK: int = const(1)

    # Table 22. IEN[1:0] configuration
    STHS34PF80_TMOS_INT_HIZ: int = const(0)
    STHS34PF80_TMOS_INT_DRDY: int = const(1)
    STHS34PF80_TMOS_INT_OR: int = const(2)

    # CTRL3 INT MSK
    STHS34PF80_TMOS_INT_NONE: int = const(0)
    STHS34PF80_TMOS_INT_TSHOCK: int = const(1)
    STHS34PF80_TMOS_INT_MOTION: int = const(2)
    STHS34PF80_TMOS_INT_TSHOCK_MOTION: int = const(3)
    STHS34PF80_TMOS_INT_PRESENCE: int = const(4)
    STHS34PF80_TMOS_INT_TSHOCK_PRESENCE: int = const(5)
    STHS34PF80_TMOS_INT_MOTION_PRESENCE: int = const(6)
    STHS34PF80_TMOS_INT_ALL: int = const(7)

    # CTRL3 Interrupt Mode
    STHS34PF80_PUSH_PULL: int = const(0)
    STHS34PF80_OPEN_DRAIN: int = const(1)

    # CTRL3 Drdy Mode
    STHS34PF80_DRDY_PULSED: int = const(0)
    STHS34PF80_DRDY_LATCHED: int = const(1)

    def __init__(self, i2c: I2C, address: int | list | tuple = STHS34PF80_I2C_ADDRESS) -> None:
        """! initialize Function
        set I2C Pins, TMOS Address

        @param i2c I2C port to use.
        @param address I2C address of the HeartUnit.
        """
        self.tmos_i2c = i2c
        self.unit_addr = address
        if self.unit_addr not in self.tmos_i2c.scan():
            raise Exception("TMOS Unit not found on I2C bus.")
        self.tamb_shock_flag = False
        self.mot_flag = False
        self.pres_flag = False
        self._last_states = [False, False, False]  # 对应 tamb_shock_flag, mot_flag, pres_flag
        self._buf = bytearray(1)
        self._handlers = [None] * 6
        self._last_reading = 0
        self.begin()

    def begin(self) -> None:
        # Set boot bit to 1, delay, then reset algorithm
        self.reset()
        # Set temperature object number set average (AVG_TMOS = 32)
        self.set_avg_tobj_num(self.STHS34PF80_AVG_TMOS_32)

        # Set ambient temperature average (AVG_TAMB = 8)
        self.set_avg_tamb_num(self.STHS34PF80_AVG_T_8)

        # Enables the block data update feature for output registers TOBJECT (26h and 27h) and TAMBIENT (28h and 29h)
        self.set_block_data_update(True)

        # Set the data rate (ODR) to 1Hz
        self.set_tmos_odr(self.STHS34PF80_TMOS_ODR_AT_1Hz)

        self.set_gain_mode(self.STHS34PF80_GAIN_WIDE_MODE)

    def reset(self) -> None:
        self.set_boot_otp(True)
        time.sleep_us(300)
        self.reset_algo()

    def set_callback(self, handler, trigger: Literal[0, 1, 2, 3, 4, 5]) -> None:
        """! Set callback function for different triggers.

        @param handler: The callback function to be set.
        @param trigger: The event trigger to set the handler for:
                        0 = tamb_shock_flag,
                        1 = mot_flag,
                        2 = pres_flag.
        """
        self._handlers[trigger] = handler

    def tick_callback(self) -> None:
        if time.ticks_diff(self._last_reading, time.ticks_ms()) * time.ticks_diff(0, 1) < 50:
            return

        self._last_reading = time.ticks_ms()

        self.refresh_state()

        current_states = [self.tamb_shock_flag, self.mot_flag, self.pres_flag]
        detected_callbacks = [
            self.AMBIENT_TEMPERATURE_SHOCK_DETECT,
            self.MOTION_DETECT,
            self.PRESENCE_DETECT,
        ]
        not_detected_callbacks = [
            self.AMBIENT_TEMPERATURE_SHOCK_NOT_DETECTED,
            self.MOTION_NOT_DETECTED,
            self.PRESENCE_NOT_DETECTED,
        ]

        for i, (current, last) in enumerate(zip(current_states, self._last_states)):
            if current:  # 当前检测到
                if self._handlers[detected_callbacks[i]] is not None:
                    schedule(self._handlers[detected_callbacks[i]], self)
            else:  # 当前未检测到
                if last:  # 之前是检测到，现在变为未检测到
                    if self._handlers[not_detected_callbacks[i]] is not None:
                        schedule(self._handlers[not_detected_callbacks[i]], self)
            # 更新上次的状态
            self._last_states[i] = current

    def reset_algo(self) -> None:
        self.write_function_config(STHS34PF80_RESET_ALGO, bytes([0x01]))

    def set_lpf_p_bandwidth(self, val) -> None:
        self._write_reg_pos(STHS34PF80_LPF2, 3, 0b0011_1000, val)

    def get_lpf_p_bandwidth(self) -> int:
        bw = self._read_reg_pos(STHS34PF80_LPF2, 3, 0b0011_1000)
        return self.STHS34PF80_LPF_ODR_DIV_9 if bw > self.STHS34PF80_LPF_ODR_DIV_800 else bw

    def set_lpf_a_t_bandwidth(self, val) -> None:
        self._write_reg_pos(STHS34PF80_LPF2, 0, 0b0000_0111, val)

    def get_lpf_a_t_bandwidth(self) -> int:
        bw = self._read_reg_pos(STHS34PF80_LPF2, 0, 0b0000_0111)
        return self.STHS34PF80_LPF_ODR_DIV_9 if bw > self.STHS34PF80_LPF_ODR_DIV_800 else bw

    def set_lpf_p_m_bandwidth(self, val) -> None:
        self._write_reg_pos(STHS34PF80_LPF1, 3, 0b0011_1000, val)

    def get_lpf_p_m_bandwidth(self) -> int:
        bw = self._read_reg_pos(STHS34PF80_LPF1, 3, 0b0011_1000)
        return self.STHS34PF80_LPF_ODR_DIV_9 if bw > self.STHS34PF80_LPF_ODR_DIV_800 else bw

    def set_lpf_m_bandwidth(self, val):
        self._write_reg_pos(STHS34PF80_LPF1, 0, 0b0000_0111, val)

    def get_lpf_m_bandwidth(self):
        bw = self._read_reg_pos(STHS34PF80_LPF1, 0, 0b0000_0111)
        return self.STHS34PF80_LPF_ODR_DIV_9 if bw > self.STHS34PF80_LPF_ODR_DIV_800 else bw

    def set_avg_tobj_num(self, val):
        self._write_reg_pos(STHS34PF80_AVG_TRIM, 0, 0b0000_0111, val)

    def get_avg_tobj_num(self):
        bw = self._read_reg_pos(STHS34PF80_AVG_TRIM, 0, 0b0000_0111)
        return self.STHS34PF80_AVG_TMOS_128 if bw > self.STHS34PF80_AVG_TMOS_2048 else bw

    def set_avg_tamb_num(self, val) -> None:
        self._write_reg_pos(STHS34PF80_AVG_TRIM, 4, 0b0011_0000, val)

    def get_avg_tamb_num(self) -> int:
        bw = self._read_reg_pos(STHS34PF80_AVG_TRIM, 4, 0b0011_0000)
        return self.STHS34PF80_AVG_T_8 if bw > self.STHS34PF80_AVG_T_1 else bw
        # return self._read_reg_pos(STHS34PF80_AVG_TRIM, 4, 0b0011_0000)

    def set_gain_mode(self, val) -> None:
        """! Set the gain mode of the TMOSUnit.

        @en %1 Set the gain mode of the TMOSUnit to %2.
        @cn %1 将TMOSUnit的增益模式设置为%2。

        @param val [field_dropdown] The gain mode of the TMOSUnit.
            @options {
                    [Reduce gain mode, STHS34PF80_GAIN_WIDE_MODE],
                    [Default mode, STHS34PF80_GAIN_DEFAULT_MODE]
            }
        """
        self._write_reg_pos(STHS34PF80_CTRL0, 4, 0b0111_0000, val)

    def get_gain_mode(self) -> int:
        """! Get the gain mode of TMOSUnit.

        @en %1 Get the gain mode of TMOSUnit.
        @cn %1 获取 TMOSUnit的增益模式。
        @return: int, The gain mode of TMOSUnit, 0 is STHS34PF80_GAIN_WIDE_MODE, 7 is STHS34PF80_GAIN_DEFAULT_MODE.
        """
        mode = self._read_reg_pos(STHS34PF80_CTRL0, 4, 0b0111_0000)
        if mode not in (self.STHS34PF80_GAIN_WIDE_MODE, self.STHS34PF80_GAIN_DEFAULT_MODE):
            mode = self.STHS34PF80_GAIN_DEFAULT_MODE  # Default to GAIN_DEFAULT_MODE if unknown
        return mode

    def get_tmos_sensitivity(self) -> float:
        """! Get the sensitivity of TMOSUnit.

        @en %1 Get the sensitivity of TMOSUnit.
        @cn %1 获取 TMOSUnit的灵敏度。
        @return: float, The sensitivity of TMOSUnit.
        """
        sens_data = self._read_reg_pos(STHS34PF80_SENS_DATA, 0, 0xFF)
        return sens_data * 16 + 2048

    def set_tmos_sensitivity(self, val) -> None:
        """! Set the sensitivity of the TMOSUnit.

        @en %1 Set the sensitivity of the TMOSUnit to %2.
        @cn %1 将TMOSUnit的灵敏度设置为%2。
        """
        val = (val - 2048 + 8) / 16 if val >= 2048 else (val - 2048 - 8) / 16
        val = int(val).to_bytes(1, "big")

        self.tmos_i2c.writeto_mem(self.unit_addr, STHS34PF80_SENS_DATA, val)

    def get_tmos_odr(self) -> int:
        odr = self._read_reg_pos(STHS34PF80_CTRL1, 0, 0b0000_1111)
        return self.STHS34PF80_TMOS_ODR_OFF if odr > self.STHS34PF80_TMOS_ODR_AT_30Hz else odr

    def _set_tmos_odr(self, val: int) -> None:
        self._write_reg_pos(STHS34PF80_CTRL1, 0, 0b0000_1111, val)

    def set_tmos_odr(self, val: int) -> int:
        max_odr = self.STHS34PF80_TMOS_ODR_AT_30Hz
        # bytearray(self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_CTRL1, 1))

        avg_trim = self.get_avg_tobj_num()

        avg_trim_dict = {
            self.STHS34PF80_AVG_TMOS_2: self.STHS34PF80_TMOS_ODR_AT_30Hz,
            self.STHS34PF80_AVG_TMOS_8: self.STHS34PF80_TMOS_ODR_AT_30Hz,
            self.STHS34PF80_AVG_TMOS_32: self.STHS34PF80_TMOS_ODR_AT_30Hz,
            self.STHS34PF80_AVG_TMOS_128: self.STHS34PF80_TMOS_ODR_AT_8Hz,
            self.STHS34PF80_AVG_TMOS_256: self.STHS34PF80_TMOS_ODR_AT_4Hz,
            self.STHS34PF80_AVG_TMOS_512: self.STHS34PF80_TMOS_ODR_AT_2Hz,
            self.STHS34PF80_AVG_TMOS_1024: self.STHS34PF80_TMOS_ODR_AT_1Hz,
            self.STHS34PF80_AVG_TMOS_2048: self.STHS34PF80_TMOS_ODR_AT_0Hz50,
        }

        max_odr = avg_trim_dict.get(avg_trim, self.STHS34PF80_TMOS_ODR_AT_30Hz)
        if val > max_odr:
            return -1

        self.set_safe_tmos_odr_check(val)
        return 0

    def get_block_data_update(self) -> bool:
        return bool(self._read_reg_pos(STHS34PF80_CTRL1, 4, 0b0001_0000))

    def set_block_data_update(self, val: bool) -> None:
        self._write_reg_pos(STHS34PF80_CTRL1, 4, 0b0001_0000, val)

    def get_tmos_one_shot(self) -> int:
        return self._read_reg_pos(STHS34PF80_CTRL2, 0, 0b0000_0001)

    # Self-clearing upon completion
    def set_tmos_one_shot(self, val: bool) -> None:
        self._write_reg_pos(STHS34PF80_CTRL2, 0, 0b0000_0001, val)

    def get_mem_bank(self) -> bool:
        return bool(self._read_reg_pos(STHS34PF80_CTRL2, 4, 0b0001_0000))

    def set_mem_bank(self, val: int) -> None:
        self._write_reg_pos(STHS34PF80_CTRL2, 4, 0b0001_0000, val)

    def get_boot_otp(self) -> bool:
        return bool(self._read_reg_pos(STHS34PF80_CTRL2, 7, 0b1000_0000))

    def set_boot_otp(self, val: bool) -> None:
        self._write_reg_pos(STHS34PF80_CTRL2, 7, 0b1000_0000, val)

    def get_tmos_route_interrupt(self) -> int:
        return self._read_reg_pos(STHS34PF80_CTRL3, 0, 0b0000_0011)

    def set_tmos_route_interrupt(self, val: int) -> None:
        self._write_reg_pos(STHS34PF80_CTRL3, 0, 0b0000_0011, val)

    def get_data_ready_mode(self) -> int:
        return self._read_reg_pos(STHS34PF80_CTRL3, 2, 0b0000_0100)

    def set_data_ready_mode(self, val: int) -> None:
        self._write_reg_pos(STHS34PF80_CTRL3, 2, 0b0000_0100, val)

    def get_tmos_interrupt_or(self) -> int:
        return self._read_reg_pos(STHS34PF80_CTRL3, 3, 0b0011_1000)

    def set_tmos_interrupt_or(self, val: int) -> None:
        self._write_reg_pos(STHS34PF80_CTRL3, 3, 0b0011_1000, val)

    def get_tmos_interrupt_mode(self) -> int:
        return self._read_reg_pos(STHS34PF80_CTRL3, 6, 0b0100_0000)

    def set_tmos_interrupt_mode(self, val: int) -> None:
        self._write_reg_pos(STHS34PF80_CTRL3, 6, 0b0100_0000, val)

    # This bit is reset to 0 when reading the FUNC_STATUS (25h) register.
    def get_data_ready(self) -> bool:
        if time.ticks_diff(self._last_reading, time.ticks_ms()) * time.ticks_diff(0, 1) < 20:
            return

        self._last_reading = time.ticks_ms()
        """! Get data update status of TMOSUnit(TAMBIENT, TOBJECT, TAMB_SHOCK, TPRESENCE, TMOTION).

        @en %1 Get data update status of TMOSUnit(TAMBIENT, TOBJECT, TAMB_SHOCK, TPRESENCE, TMOTION).
        @cn %1 获取 TMOSUnit数据更新状态(TAMBIENT, TOBJECT, TAMB_SHOCK, TPRESENCE, TMOTION)。
        @return: bool, The data update status of TMOSUnit.
        """
        status = self._read_reg_pos(STHS34PF80_STATUS, 2, 0b0000_0100)
        return bool(status)

    def refresh_state(self):
        """! Retrieve the current status of the TMOSUnit, including presence detection, motion detection, and ambient temperature shock detection.

        @en %1 Retrieve the current status of the TMOSUnit, including presence detection, motion detection, and ambient temperature shock detection.
        @cn %1 获取 TMOSUnit 的当前状态，包括存在检测、运动检测和环境温度冲击检测。
        @return: An instance of the TMOSUnit with updated status flags.
        """
        data = self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_FUNC_STATUS, 1)
        func_status = data[0]
        self.tamb_shock_flag = func_status & 0x01
        self.mot_flag = (func_status >> 1) & 0x01
        self.pres_flag = (func_status >> 2) & 0x01
        return self

    def get_motion_state(self) -> bool:
        return bool(self.mot_flag)

    def get_presence_state(self) -> bool:
        return bool(self.pres_flag)

    def get_tamb_shock_state(self) -> bool:
        return bool(self.tamb_shock_flag)

    # object temperature
    def get_tobject_raw_value(self) -> int:
        tobject = self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_TOBJECT_L, 2)
        tobject = (tobject[1] << 8) | tobject[0]
        return tobject

    # temperature data
    def get_temperature_data(self) -> float:
        """! Get object temperature, represents the amount of infrared radiation emitted from the objects inside the field of view.

        @en %1 Get object temperature, represents the amount of infrared radiation emitted from the objects inside the field of view.
        @cn %1 获取物体温度，表示视野内物体发射的红外辐射量。
        @return: float, The object temperature of TMOSUnit.
        """
        sensitivity = 2000
        temp_val_fill = self.get_tobject_raw_value()
        temp_val = float(temp_val_fill) / sensitivity
        return temp_val

    # ambient temperature
    def get_tambient_raw_value(self) -> int:
        """! Get ambient temperature, represents the temperature of the environment in thermal coupling with the sensor.

        @en %1 Get ambient temperature, represents the temperature of the environment in thermal coupling with the sensor.
        @cn %1 获取环境温度，表示与传感器热耦合的环境温度。
        @return: int, The ambient temperature of TMOSUnit.
        """
        tambient = self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_TAMBIENT_L, 2)
        tambient = (tambient[1] << 8) | tambient[0]
        return tambient

    # object compensated temperature
    def get_tobject_compensated_raw_value(self) -> int:
        tobject_comp = self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_TOBJ_COMP_L, 2)
        tobject_comp = (tobject_comp[1] << 8) | tobject_comp[0]
        return tobject_comp

    # ambient temperature shock
    def get_tamb_shock_raw(self) -> int:
        tamb_shock = self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_TAMB_SHOCK_L, 2)
        tamb_shock = (tamb_shock[1] << 8) | tamb_shock[0]
        return tamb_shock

    # presence
    def get_presence_value(self) -> int:
        """! Get presence value(not distance)
        @en %1 Get presence value(not distance)
        @cn %1 获取物体存在值(不表示距离)
        @return: int, The presence value of TMOSUnit.
        """
        presence = self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_TPRESENCE_L, 2)
        presence = (presence[1] << 8) | presence[0]
        return presence

    # motion
    def get_motion_value(self) -> int:
        """! Get motion value(not distance)
        @en %1 Get motion value(not distance)
        @cn %1 获取物体运动值(不表示距离)
        @return: int, The motion value of TMOSUnit.
        """
        motion = self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_TMOTION_L, 2)
        motion = (motion[1] << 8) | motion[0]
        return motion

    # Application Note 3.1 Power-down mode
    def set_safe_tmos_odr_check(self, odr: int) -> None:
        if odr > 0:
            # Do a clean reset algo procedure everytime odr is changed to an operative state.
            self._set_tmos_odr(self.STHS34PF80_TMOS_ODR_OFF)
            self.reset_algo()
        else:
            # if we need to go to power-down from an operative state perform the safe power-down.
            if self.get_tmos_odr() > 0:
                # Read FUNC_STATUS (25h) to reset the DRDY flag.
                self.refresh_state()
                start_time = time.time()
                now_time = time.time()

                status = 1
                while status != 0 and (now_time - start_time) < 2:
                    status = self.get_data_ready()
                    now_time = time.time()
                    time.sleep(0.1)

                self._set_tmos_odr(self.STHS34PF80_TMOS_ODR_OFF)
                # Read FUNC_STATUS (25h) to reset the DRDY flag.
                self.refresh_state()

        odr = odr & 0xF
        self._set_tmos_odr(odr)

    def write_function_config(self, addr: bytes, data: int) -> None:
        # Save current odr and enter PD mode
        odr = self.get_tmos_odr()
        self.set_safe_tmos_odr_check(0)
        # Enable access to embedded functions register
        self.set_mem_bank(self.STHS34PF80_EMBED_FUNC_MEM_BANK)
        # Enable write mode
        self._set_function_page_write(True)

        # Select register address (it will autoincrement when writing)
        self.tmos_i2c.writeto_mem(self.unit_addr, STHS34PF80_FUNC_CFG_ADDR, bytes([addr]))

        self._write_function_cfg_data(data)

        # Disable write mode
        self._set_function_page_write(False)
        # Disable access to embedded functions register
        self.set_mem_bank(self.STHS34PF80_MAIN_MEM_BANK)
        # Set saved odr back
        self.set_safe_tmos_odr_check(odr)

    def read_function_config(self, addr: int, length: int) -> bytearray:
        # Save current odr and enter PD mode
        odr = self.get_tmos_odr()
        self.set_safe_tmos_odr_check(0)
        # Enable access to embedded functions register
        self.set_mem_bank(self.STHS34PF80_EMBED_FUNC_MEM_BANK)
        # Enable read mode
        self._set_function_page_read(True)

        # Select register address (it will autoincrement when reading)
        data = self._read_function_cfg_data(addr, length)

        # Disable read mode
        self._set_function_page_read(False)
        # Disable access to embedded functions register
        self.set_mem_bank(self.STHS34PF80_MAIN_MEM_BANK)
        # Set saved odr back
        self.set_safe_tmos_odr_check(odr)

        return data

    def _set_function_page_read(self, val: bool) -> None:
        self._write_reg_pos(STHS34PF80_PAGE_RW, 5, 0b0010_0000, val)

    def _set_function_page_write(self, val: bool) -> None:
        self._write_reg_pos(STHS34PF80_PAGE_RW, 6, 0b0100_0000, val)

    def _get_function_page_read(self) -> int:
        return self._read_reg_pos(STHS34PF80_PAGE_RW, 5, 0b0010_0000)

    def _get_function_page_write(self) -> int:
        return self._read_reg_pos(STHS34PF80_PAGE_RW, 6, 0b0100_0000)

    def _write_function_cfg_data(self, data: bytes) -> None:
        if isinstance(data, int):
            data = bytes([data])
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes, bytearray, or a single integer")
        for i in range(len(data) - 1, -1, -1):
            self.tmos_i2c.writeto_mem(self.unit_addr, STHS34PF80_FUNC_CFG_DATA, bytes([data[i]]))
            time.sleep(0.1)

    def _read_function_cfg_data(self, addr: int, length: int) -> bytearray:
        data = bytearray(length)
        for i in range(length):
            reg_addr = addr + length - 1 - i  # 先读高位，再读低位
            self.tmos_i2c.writeto_mem(
                self.unit_addr, STHS34PF80_FUNC_CFG_ADDR, bytearray([reg_addr])
            )
            read_data = self.tmos_i2c.readfrom_mem(self.unit_addr, STHS34PF80_FUNC_CFG_DATA, 1)
            data[i] = read_data[0]

        return data

    def get_presence_threshold(self) -> int:
        """! Get the presence threshold for presence detection algorithm.
        @en %1 Get presence threshold for presence detection algorithm.
        @cn %1 获取存在检测算法的阈值。
        @return: int, The presence threshold of TMOSUnit.
        """
        presence_threshold = self.read_function_config(STHS34PF80_PRESENCE_THS, 2)
        return int.from_bytes(presence_threshold, "big") & 0x7FFF

    def set_presence_threshold(self, val: int) -> bool:
        """! Set the presence threshold for presence detection algorithm.
        @en %1 Set presence threshold for presence detection algorithm.
        @cn %1 设置存在检测算法的阈值。
        @return: bool, Is the setting successful?
        """
        if (val & 0x8000) != 0x0:
            return 0
        odr = self.get_tmos_odr()
        self.set_safe_tmos_odr_check(0)

        buff = bytes([(val >> 8) & 0xFF, val & 0xFF])

        self.write_function_config(STHS34PF80_PRESENCE_THS, buff)
        self.reset_algo()
        self.set_safe_tmos_odr_check(odr)
        return 1

    def get_motion_threshold(self) -> int:
        """! Get the motion threshold for motion detection algorithm.
        @en %1 Get motion threshold for motion detection algorithm.
        @cn %1 获取运动检测算法的阈值。
        @return: int, The motion threshold of TMOSUnit.
        """
        motion_threshold = self.read_function_config(STHS34PF80_MOTION_THS, 2)
        return int.from_bytes(motion_threshold, "big") & 0x7FFF

    def set_motion_threshold(self, val: int) -> bool:
        """! Set the the motion threshold for motion detection algorithm.
        @en %1 Set motion threshold for motion detection algorithm.
        @cn %1 设置运动检测算法的阈值。
        @return: int, Is the setting successful?
        """
        if (val & 0x8000) != 0x0:
            return 0
        odr = self.get_tmos_odr()
        self.set_safe_tmos_odr_check(0)

        buff = bytes([(val >> 8) & 0xFF, val & 0xFF])

        self.write_function_config(STHS34PF80_MOTION_THS, buff)
        self.reset_algo()
        self.set_safe_tmos_odr_check(odr)
        return 1

    def get_tambient_shock_threshold(self) -> int:
        """! Get the ambient temperature shock threshold for Tambient shock detection algorithm.
        @en %1 Get ambient temperature shock threshold for Tambient shock detection algorithm.
        @cn %1 获取 Tambient 冲击检测算法的环境温度冲击阈值。
        @return: int, The ambient temperature shock threshold of TMOSUnit.
        """
        tambient_shock_threshold = self.read_function_config(STHS34PF80_TAMB_SHOCK_THS, 2)
        return int.from_bytes(tambient_shock_threshold, "big") & 0x7FFF

    def set_tambient_shock_threshold(self, val: int) -> bool:
        """! Set ambient temperature shock threshold for Tambient shock detection algorithm.
        @en %1 Set ambient temperature shock threshold for Tambient shock detection algorithm.
        @cn %1 设置 Tambient 冲击检测算法的环境温度冲击阈值。
        @return: int, Is the setting successful?
        """
        if (val & 0x8000) != 0x0:
            return 0
        odr = self.get_tmos_odr()
        self.set_safe_tmos_odr_check(0)

        buff = bytes([(val >> 8) & 0xFF, val & 0xFF])

        self.write_function_config(STHS34PF80_TAMB_SHOCK_THS, buff)
        self.reset_algo()
        self.set_safe_tmos_odr_check(odr)
        return 1

    def get_presence_hysteresis(self) -> int:
        """! Get hysteresis value for presence detection algorithm.
        @en %1 Get hysteresis value for presence detection algorithm.
        @cn %1 获取存在检测算法的滞后值。
        @return: int, The presence hysteresis of TMOSUnit.
        """
        presence_hysteresis = self.read_function_config(STHS34PF80_HYST_PRESENCE, 1)
        return int.from_bytes(presence_hysteresis, "big")

    def set_presence_hysteresis(self, val: int) -> None:
        """! Set hysteresis value for presence detection algorithm.
        @en %1 Set hysteresis value for presence detection algorithm.
        @cn %1 设置存在检测算法的滞后值。
        """
        odr = self.get_tmos_odr()
        self.set_safe_tmos_odr_check(0)

        self.write_function_config(STHS34PF80_HYST_PRESENCE, val)
        self.reset_algo()
        self.set_safe_tmos_odr_check(odr)

    def get_motion_hysteresis(self) -> int:
        """! Get hysteresis value for motion detection algorithm.
        @en %1 Get hysteresis value for motion detection algorithm.
        @cn %1 获取运动检测算法的滞后值。
        @return: int, The motion hysteresis of TMOSUnit.
        """
        motion_hysteresis = self.read_function_config(STHS34PF80_HYST_MOTION, 1)
        return int.from_bytes(motion_hysteresis, "big")

    def set_motion_hysteresis(self, val: int) -> None:
        """! Set hysteresis value for motion detection algorithm.
        @en %1 Set hysteresis value for motion detection algorithm.
        @cn %1 设置运动检测算法的滞后值。
        """
        odr = self.get_tmos_odr()
        self.set_safe_tmos_odr_check(0)

        self.write_function_config(STHS34PF80_HYST_MOTION, val)
        self.reset_algo()
        self.set_safe_tmos_odr_check(odr)

    def get_tambient_shock_hysteresis(self) -> int:
        """! Get hysteresis value for ambient temperature shock detection algor.
        @en %1 Get hysteresis value for ambient temperature shock detection algor.
        @cn %1 获取环境温度冲击检测算法的滞后值。
        @return: int, The ambient temperature shock hysteresis of TMOSUnit.
        """
        tambient_shock_hysteresis = self.read_function_config(STHS34PF80_HYST_TAMB_SHOCK, 1)
        return int.from_bytes(tambient_shock_hysteresis, "big")

    def set_tambient_shock_hysteresis(self, val: int) -> None:
        """! Set hysteresis value for ambient temperature shock detection algor.
        @en %1 Set hysteresis value for ambient temperature shock detection algor.
        @cn %1 设置环境温度冲击检测算法的滞后值。
        """
        odr = self.get_tmos_odr()
        self.set_safe_tmos_odr_check(0)

        self.write_function_config(STHS34PF80_HYST_TAMB_SHOCK, val)
        self.reset_algo()
        self.set_safe_tmos_odr_check(odr)

    def get_algo_config(self):
        data = self.read_function_config(STHS34PF80_ALGO_CONFIG, 1)
        tmp = data[0]
        val = {
            "sel_abs": (tmp >> 1) & 0x1,
            "comp_type": (tmp >> 2) & 0x1,
            "int_pulsed": (tmp >> 3) & 0x1,
        }
        return val

    def set_algo_config(self, val: int) -> bool:
        int_pulsed = val["int_pulsed"]
        comp_type = val["comp_type"]
        sel_abs = val["sel_abs"]
        tmp = (int_pulsed << 3) | (comp_type << 2) | (sel_abs << 1)
        tmp_bytes = bytes([tmp])
        self.write_function_config(STHS34PF80_ALGO_CONFIG, tmp_bytes)
        return 1

    def get_interrupt_pulsed(self) -> int:
        config = self.get_algo_config()
        return config["int_pulsed"]

    def set_interrupt_pulsed(self, val: int) -> bool:
        config = self.get_algo_config()
        config["int_pulsed"] = val
        self.set_algo_config(config)
        return 1

    def get_tobject_algo_compensation(self) -> int:
        config = self.get_algo_config()
        return config["comp_type"]

    def set_tobject_algo_compensation(self, val: int) -> bool:
        config = self.get_algo_config()
        config["comp_type"] = val
        self.set_algo_config(config)
        return 1

    def get_presence_abs_value(self) -> int:
        config = self.get_algo_config()
        return config["sel_abs"]

    def set_presence_abs_value(self, val: int) -> bool:
        config = self.get_algo_config()
        config["sel_abs"] = val
        self.set_algo_config(config)
        return 1

    def _read_reg_pos(self, reg, pos, mask):
        self.tmos_i2c.readfrom_mem_into(self.unit_addr, reg, self._buf)
        return (self._buf[0] & mask) >> pos

    def _write_reg_pos(self, reg, pos, mask, value):
        self.tmos_i2c.readfrom_mem_into(self.unit_addr, reg, self._buf)
        self._buf[0] = self._buf[0] & (~mask)
        self._buf[0] = self._buf[0] | ((value << pos) & mask)
        self.tmos_i2c.writeto_mem(self.unit_addr, reg, self._buf)

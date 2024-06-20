# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   heart.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import I2C
from cdriver import max30100
import struct
import _thread, time


class HeartUnit:
    """! HEART is built using the MAX30100 chipset.

    @en MAX30100 is a complete pulse oximetry and heart-rate sensor system solution designed for the demanding requirements of wearable devices.
    @cn MAX30100是一种完整的脉搏血氧饱和度和心率传感器系统解决方案，专为可穿戴设备的严格要求而设计。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/heart
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/heart/heart_01.webp
    @category unit

    @example
        from unit import HeartUnit
        from hardware import I2C
        i2c = I2C(1, scl=33, sda=32)
        heart = HeartUnit(i2c)
        heart.start()
        heart.get_heart_rate();heart.get_spo2()


    @attr MODE_HR_ONLY Detect heart rate only.
    @attr MODE_SPO2_HR Detect heart rate and SpO2.
    """

    MODE_HR_ONLY = 0x02
    MODE_SPO2_HR = 0x03

    LED_CURRENT_0MA = 0x00
    LED_CURRENT_4_4MA = 0x01
    LED_CURRENT_7_6MA = 0x02
    LED_CURRENT_11MA = 0x03
    LED_CURRENT_14_2MA = 0x04
    LED_CURRENT_17_4MA = 0x05
    LED_CURRENT_20_8MA = 0x06
    LED_CURRENT_24MA = 0x07
    LED_CURRENT_27_1MA = 0x08
    LED_CURRENT_30_6MA = 0x09
    LED_CURRENT_33_8MA = 0x0A
    LED_CURRENT_37MA = 0x0B
    LED_CURRENT_40_2MA = 0x0C
    LED_CURRENT_43_6MA = 0x0D
    LED_CURRENT_46_8MA = 0x0E
    LED_CURRENT_50MA = 0x0F

    PULSE_WIDTH_200US_ADC_13 = 0x00
    PULSE_WIDTH_400US_ADC_14 = 0x01
    PULSE_WIDTH_800US_ADC_15 = 0x02
    PULSE_WIDTH_1600US_ADC_16 = 0x03

    SAMPLING_RATE_50HZ = 0x00
    SAMPLING_RATE_100HZ = 0x01
    SAMPLING_RATE_167HZ = 0x02
    SAMPLING_RATE_200HZ = 0x03
    SAMPLING_RATE_400HZ = 0x04
    SAMPLING_RATE_600HZ = 0x05
    SAMPLING_RATE_800HZ = 0x06
    SAMPLING_RATE_1000HZ = 0x07

    def __init__(self, i2c: I2C, address: int | list | tuple = 0x57) -> None:
        """! Initialize the HeartUnit.

        @param i2c I2C port to use.
        @param address I2C address of the HeartUnit.
        """
        self.i2c = i2c
        self.addr = address
        self._available()
        max30100.init(i2c, address)
        self._task_running = False

    def _thread_task(self) -> None:
        while self._task_running:
            max30100.update()
            time.sleep_ms(5)

    def _available(self) -> None:
        """! Check if HeartUnit is available on the I2C bus.

        Raises:
            Exception: If the HeartUnit is not found.
        """
        if self.addr not in self.i2c.scan():
            raise Exception("HeartUnit not found on I2C bus.")

    def stop(self) -> None:
        """! Stop the HeartUnit.

        @en %1 Stop the HeartUnit update.
        @cn %1 停止HeartUnit更新。

        """
        self._task_running = False

    def start(self) -> None:
        """! Start the HeartUnit.

        @en %1 Start the HeartUnit update.
        @cn %1 启动HeartUnit更新。

        """
        self._task_running = True
        _thread.start_new_thread(self._thread_task, ())

    def deinit(self) -> None:
        """! Deinitialize the HeartUnit.

        @en %1 Deinitialize the HeartUnit.
        @cn %1 释放HeartUnit。

        """
        self.stop()
        time.sleep_ms(50)
        max30100.deinit()

    def get_heart_rate(self) -> int:
        """! Get the heart rate.

        @en %1 Get the heart rate.
        @cn %1 获取心率。

        @return Heart rate.
        """
        return max30100.get_heart_rate()

    def get_spo2(self) -> int:
        """! Get the SpO2.

        @en %1 Get the SpO2.
        @cn %1 获取血氧饱和度。

        @return SpO2.
        """
        return max30100.get_spo2()

    def get_ir(self) -> int:
        """! Get the IR value.

        @en %1 Get the IR value.
        @cn %1 获取红外值。

        @return IR value.
        """
        return max30100.get_ir()

    def get_red(self) -> int:
        """! Get the red value.

        @en %1 Get the red value.
        @cn %1 获取红光值。

        @return Red value.
        """
        return max30100.get_red()

    def set_mode(self, mode: int) -> None:
        """! Set the mode of the HeartUnit.

        @en %1 Set the mode of the HeartUnit to %2.
        @cn %1 将HeartUnit的模式设置为%2。

        @param mode [field_dropdown] The detect mode of the HeartUnit.
            @options {
                    [Only heart rate, HeartUnit.MODE_HR_ONLY],
                    [Heart rate and SpO2, HeartUnit.MODE_SPO2_HR]
            }
        """
        max30100.set_mode(mode)

    def set_led_current(self, led_current: int) -> None:
        """! Set the LED current of the HeartUnit.

        @en %1 Set the LED current of the HeartUnit to %2.
        @cn %1 将HeartUnit的LED电流设置为%2。

        @param led_current [field_dropdown] The LED current of the HeartUnit.
            @options {
                    [0mA, HeartUnit.LED_CURRENT_0MA],
                    [4.4mA, HeartUnit.LED_CURRENT_4_4MA],
                    [7.6mA, HeartUnit.LED_CURRENT_7_6MA],
                    [11mA, HeartUnit.LED_CURRENT_11MA],
                    [14.2mA, HeartUnit.LED_CURRENT_14_2MA],
                    [17.4mA, HeartUnit.LED_CURRENT_17_4MA],
                    [20.8mA, HeartUnit.LED_CURRENT_20_8MA],
                    [24mA, HeartUnit.LED_CURRENT_24MA],
                    [27.1mA, HeartUnit.LED_CURRENT_27_1MA],
                    [30.6mA, HeartUnit.LED_CURRENT_30_6MA],
                    [33.8mA, HeartUnit.LED_CURRENT_33_8MA],
                    [37mA, HeartUnit.LED_CURRENT_37MA],
                    [40.2mA, HeartUnit.LED_CURRENT_40_2MA],
                    [43.6mA, HeartUnit.LED_CURRENT_43_6MA],
                    [46.8mA, HeartUnit.LED_CURRENT_46_8MA],
                    [50mA, HeartUnit.LED_CURRENT_50MA]
            }
        """
        max30100.set_led_current(led_current)

    def set_pulse_width(self, pulse_width: int) -> None:
        """! Set the pulse width of the HeartUnit.

        @en %1 Set the pulse width of the HeartUnit to %2.
        @cn %1 将HeartUnit的脉冲宽度设置为%2。

        @param pulse_width [field_dropdown] The pulse width of the HeartUnit.
            @options {
                    [200us, HeartUnit.PULSE_WIDTH_200US_ADC_13],
                    [400us, HeartUnit.PULSE_WIDTH_400US_ADC_14],
                    [800us, HeartUnit.PULSE_WIDTH_800US_ADC_15],
                    [1600us, HeartUnit.PULSE_WIDTH_1600US_ADC_16]
            }
        """
        max30100.set_pulse_width(pulse_width)

    def set_sampling_rate(self, sampling_rate: int) -> None:
        """! Set the sampling rate of the HeartUnit.

        @en %1 Set the sampling rate of the HeartUnit to %2.
        @cn %1 将HeartUnit的采样率设置为%2。

        @param sampling_rate [field_dropdown] The sampling rate of the HeartUnit.
            @options {
                    [50Hz, HeartUnit.SAMPLING_RATE_50HZ],
                    [100Hz, HeartUnit.SAMPLING_RATE_100HZ],
                    [167Hz, HeartUnit.SAMPLING_RATE_167HZ],
                    [200Hz, HeartUnit.SAMPLING_RATE_200HZ],
                    [400Hz, HeartUnit.SAMPLING_RATE_400HZ],
                    [600Hz, HeartUnit.SAMPLING_RATE_600HZ],
                    [800Hz, HeartUnit.SAMPLING_RATE_800HZ],
                    [1000Hz, HeartUnit.SAMPLING_RATE_1000HZ]
            }
        """
        max30100.set_sampling_rate(sampling_rate)

# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import time


class DualKey:
    ADC_BAT_GPIO = 10
    ADC_VBUS_GPIO = 2
    ADC_CHRG_GPIO = 9
    ADC_SW1_GPIO = 8
    ADC_SW2_GPIO = 7
    BATTERY_VOLTAGE_MULTIPLIER = 1.51
    VBUS_VOLTAGE_MULTIPLIER = 1.51
    SWITCH_VOLTAGE_THRESHOLD = 1000
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DualKey, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.adc_bat = machine.ADC(machine.Pin(self.ADC_BAT_GPIO))
        self.adc_vbus = machine.ADC(machine.Pin(self.ADC_VBUS_GPIO))
        self.adc_chrg = machine.ADC(machine.Pin(self.ADC_CHRG_GPIO))
        self.adc_sw1 = machine.ADC(machine.Pin(self.ADC_SW1_GPIO))
        self.adc_sw2 = machine.ADC(machine.Pin(self.ADC_SW2_GPIO))
        for adc in (self.adc_bat, self.adc_vbus, self.adc_chrg, self.adc_sw1, self.adc_sw2):
            adc.atten(machine.ADC.ATTN_11DB)
            adc.width(machine.ADC.WIDTH_12BIT)
        self._initialized = True

    def _read_adc_voltage(self, adc, samples=5):
        total = 0
        for _ in range(samples):
            total += adc.read()
            time.sleep_ms(2)
        avg_raw = total / samples
        return (avg_raw / 4095) * 3.3

    def get_battery_voltage(self):
        """返回电池电压 (mV)"""
        v = self._read_adc_voltage(self.adc_bat)
        v *= self.BATTERY_VOLTAGE_MULTIPLIER
        return int(v * 1000)

    def get_vbus_voltage(self):
        """返回VBUS电压 (mV)"""
        v = self._read_adc_voltage(self.adc_vbus)
        v *= self.VBUS_VOLTAGE_MULTIPLIER
        return int(v * 1000)

    def get_charging_voltage(self):
        return self._read_adc_voltage(self.adc_chrg)

    def get_charging_status(self):
        v = self.get_charging_voltage()
        if 1.4 <= v <= 1.8:
            return "CHARGING"
        elif 1.8 < v <= 2.4:
            return "FULL"
        elif v > 3.0:
            return "NO_CHARGING"
        else:
            return "UNKNOWN"

    def is_charging(self):
        return self.get_charging_status() == "CHARGING"

    def get_switch_position(self):
        """判断拨动开关位置：0 / 1 / 2 / -1"""

        def avg_adc(adc):
            return sum(adc.read() for _ in range(5)) / 5

        mv1 = avg_adc(self.adc_sw1) * 3300 / 4095 * self.BATTERY_VOLTAGE_MULTIPLIER
        mv2 = avg_adc(self.adc_sw2) * 3300 / 4095 * self.BATTERY_VOLTAGE_MULTIPLIER
        th = self.SWITCH_VOLTAGE_THRESHOLD
        if mv1 > th and mv2 <= th:
            return 0
        elif mv1 <= th and mv2 <= th:
            return 1
        elif mv1 <= th and mv2 > th:
            return 2
        else:
            return -1


dualkey = DualKey()

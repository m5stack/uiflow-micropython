# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Carter Nelson for Adafruit Industries
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import time
import struct
from machine import I2C
from micropython import const


_VL53L1X_I2C_SLAVE_DEVICE_ADDRESS = const(0x0001)
_VL53L1X_VHV_CONFIG__TIMEOUT_MACROP_LOOP_BOUND = const(0x0008)
_GPIO_HV_MUX__CTRL = const(0x0030)
_GPIO__TIO_HV_STATUS = const(0x0031)
_PHASECAL_CONFIG__TIMEOUT_MACROP = const(0x004B)
_RANGE_CONFIG__TIMEOUT_MACROP_A_HI = const(0x005E)
_RANGE_CONFIG__VCSEL_PERIOD_A = const(0x0060)
_RANGE_CONFIG__TIMEOUT_MACROP_B_HI = const(0x0061)
_RANGE_CONFIG__VCSEL_PERIOD_B = const(0x0063)
_RANGE_CONFIG__VALID_PHASE_HIGH = const(0x0069)
_SD_CONFIG__WOI_SD0 = const(0x0078)
_SD_CONFIG__INITIAL_PHASE_SD0 = const(0x007A)
_SYSTEM__INTERRUPT_CLEAR = const(0x0086)
_SYSTEM__MODE_START = const(0x0087)
_VL53L1X_RESULT__RANGE_STATUS = const(0x0089)
_VL53L1X_RESULT__FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0 = const(0x0096)
_VL53L1X_IDENTIFICATION__MODEL_ID = const(0x010F)

TB_SHORT_DIST = {
    # ms: (MACROP_A_HI, MACROP_B_HI)
    15: (b"\x00\x1d", b"\x00\x27"),
    20: (b"\x00\x51", b"\x00\x6e"),
    33: (b"\x00\xd6", b"\x00\x6e"),
    50: (b"\x01\xae", b"\x01\xe8"),
    100: (b"\x02\xe1", b"\x03\x88"),
    200: (b"\x03\xe1", b"\x04\x96"),
    500: (b"\x05\x91", b"\x05\xc1"),
}

TB_LONG_DIST = {
    # ms: (MACROP_A_HI, MACROP_B_HI)
    20: (b"\x00\x1e", b"\x00\x22"),
    33: (b"\x00\x60", b"\x00\x6e"),
    50: (b"\x00\xad", b"\x00\xc6"),
    100: (b"\x01\xcc", b"\x01\xea"),
    200: (b"\x02\xd9", b"\x02\xf8"),
    500: (b"\x04\x8f", b"\x04\xa4"),
}


class VL53L1X:
    """Create a VL53L1X object.

    :param I2C i2c: The I2C bus the ToF4M Unit is connected to.
    :param int address: The I2C address of the device. Default is 0x29.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C
            from unit import TOFUnit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            tof_0 = TOFUnit(i2c0)
    """

    def __init__(self, i2c: I2C, address: int = 41):
        self._i2c = i2c
        self._addr = address
        model_id, module_type, mask_rev = self.get_model_info
        if model_id != 0xEA or module_type != 0xCC or mask_rev != 0x10:
            raise RuntimeError("Wrong sensor ID or type!")
        self._sensor_init()
        self._timing_budget = None
        self.set_measurement_timing_budget(50)

    def _sensor_init(self):
        # pylint: disable=line-too-long
        init_seq = bytes(
            [  # value    addr : description
                0x00,  # 0x2d : set bit 2 and 5 to 1 for fast plus mode (1MHz I2C), else don't touch
                0x00,  # 0x2e : bit 0 if I2C pulled up at 1.8V, else set bit 0 to 1 (pull up at AVDD)
                0x00,  # 0x2f : bit 0 if GPIO pulled up at 1.8V, else set bit 0 to 1 (pull up at AVDD)
                0x01,  # 0x30 : set bit 4 to 0 for active high interrupt and 1 for active low (bits 3:0 must be 0x1), use SetInterruptPolarity()
                0x02,  # 0x31 : bit 1 = interrupt depending on the polarity
                0x00,  # 0x32 : not user-modifiable
                0x02,  # 0x33 : not user-modifiable
                0x08,  # 0x34 : not user-modifiable
                0x00,  # 0x35 : not user-modifiable
                0x08,  # 0x36 : not user-modifiable
                0x10,  # 0x37 : not user-modifiable
                0x01,  # 0x38 : not user-modifiable
                0x01,  # 0x39 : not user-modifiable
                0x00,  # 0x3a : not user-modifiable
                0x00,  # 0x3b : not user-modifiable
                0x00,  # 0x3c : not user-modifiable
                0x00,  # 0x3d : not user-modifiable
                0xFF,  # 0x3e : not user-modifiable
                0x00,  # 0x3f : not user-modifiable
                0x0F,  # 0x40 : not user-modifiable
                0x00,  # 0x41 : not user-modifiable
                0x00,  # 0x42 : not user-modifiable
                0x00,  # 0x43 : not user-modifiable
                0x00,  # 0x44 : not user-modifiable
                0x00,  # 0x45 : not user-modifiable
                0x20,  # 0x46 : interrupt configuration 0->level low detection, 1-> level high, 2-> Out of window, 3->In window, 0x20-> New sample ready , TBC
                0x0B,  # 0x47 : not user-modifiable
                0x00,  # 0x48 : not user-modifiable
                0x00,  # 0x49 : not user-modifiable
                0x02,  # 0x4a : not user-modifiable
                0x0A,  # 0x4b : not user-modifiable
                0x21,  # 0x4c : not user-modifiable
                0x00,  # 0x4d : not user-modifiable
                0x00,  # 0x4e : not user-modifiable
                0x05,  # 0x4f : not user-modifiable
                0x00,  # 0x50 : not user-modifiable
                0x00,  # 0x51 : not user-modifiable
                0x00,  # 0x52 : not user-modifiable
                0x00,  # 0x53 : not user-modifiable
                0xC8,  # 0x54 : not user-modifiable
                0x00,  # 0x55 : not user-modifiable
                0x00,  # 0x56 : not user-modifiable
                0x38,  # 0x57 : not user-modifiable
                0xFF,  # 0x58 : not user-modifiable
                0x01,  # 0x59 : not user-modifiable
                0x00,  # 0x5a : not user-modifiable
                0x08,  # 0x5b : not user-modifiable
                0x00,  # 0x5c : not user-modifiable
                0x00,  # 0x5d : not user-modifiable
                0x01,  # 0x5e : not user-modifiable
                0xCC,  # 0x5f : not user-modifiable
                0x0F,  # 0x60 : not user-modifiable
                0x01,  # 0x61 : not user-modifiable
                0xF1,  # 0x62 : not user-modifiable
                0x0D,  # 0x63 : not user-modifiable
                0x01,  # 0x64 : Sigma threshold MSB (mm in 14.2 format for MSB+LSB), default value 90 mm
                0x68,  # 0x65 : Sigma threshold LSB
                0x00,  # 0x66 : Min count Rate MSB (MCPS in 9.7 format for MSB+LSB)
                0x80,  # 0x67 : Min count Rate LSB
                0x08,  # 0x68 : not user-modifiable
                0xB8,  # 0x69 : not user-modifiable
                0x00,  # 0x6a : not user-modifiable
                0x00,  # 0x6b : not user-modifiable
                0x00,  # 0x6c : Intermeasurement period MSB, 32 bits register
                0x00,  # 0x6d : Intermeasurement period
                0x0F,  # 0x6e : Intermeasurement period
                0x89,  # 0x6f : Intermeasurement period LSB
                0x00,  # 0x70 : not user-modifiable
                0x00,  # 0x71 : not user-modifiable
                0x00,  # 0x72 : distance threshold high MSB (in mm, MSB+LSB)
                0x00,  # 0x73 : distance threshold high LSB
                0x00,  # 0x74 : distance threshold low MSB ( in mm, MSB+LSB)
                0x00,  # 0x75 : distance threshold low LSB
                0x00,  # 0x76 : not user-modifiable
                0x01,  # 0x77 : not user-modifiable
                0x0F,  # 0x78 : not user-modifiable
                0x0D,  # 0x79 : not user-modifiable
                0x0E,  # 0x7a : not user-modifiable
                0x0E,  # 0x7b : not user-modifiable
                0x00,  # 0x7c : not user-modifiable
                0x00,  # 0x7d : not user-modifiable
                0x02,  # 0x7e : not user-modifiable
                0xC7,  # 0x7f : ROI center
                0xFF,  # 0x80 : XY ROI (X=Width, Y=Height)
                0x9B,  # 0x81 : not user-modifiable
                0x00,  # 0x82 : not user-modifiable
                0x00,  # 0x83 : not user-modifiable
                0x00,  # 0x84 : not user-modifiable
                0x01,  # 0x85 : not user-modifiable
                0x00,  # 0x86 : clear interrupt, 0x01=clear
                0x00,  # 0x87 : ranging, 0x00=stop, 0x40=start
            ]
        )
        self._write_register(0x002D, init_seq)
        self.set_continuous_start_measurement()
        while not self.get_data_ready:
            time.sleep(0.01)
        self.clear_interrupt()
        self.set_continuous_stop_measurement()
        self._write_register(_VL53L1X_VHV_CONFIG__TIMEOUT_MACROP_LOOP_BOUND, b"\x09")
        self._write_register(0x0B, b"\x00")

    @property
    def get_model_info(self):
        info = self._read_register(_VL53L1X_IDENTIFICATION__MODEL_ID, 3)
        return (info[0], info[1], info[2])  # Model ID, Module Type, Mask Rev

    @property
    def get_distance(self):
        """The distance in units of millimeters.

        :returns: Distance in millimeters or None if measurement is invalid.
        :rtype: int or None

        UiFlow2 Code Block:

            |get_distance.png|

        MicroPython Code Block:

            .. code-block:: python

                distance = tof_0.get_distance
        """
        if self._read_register(_VL53L1X_RESULT__RANGE_STATUS)[0] != 0x09:
            return None
        dist = self._read_register(_VL53L1X_RESULT__FINAL_CROSSTALK_CORRECTED_RANGE_MM_SD0, 2)
        return struct.unpack(">H", dist)[0]

    def set_continuous_start_measurement(self):
        """Starts continuous measure operation.

        UiFlow2 Code Block:

            |set_continuous_start_measurement.png|

        MicroPython Code Block:

            .. code-block:: python

                tof_0.set_continuous_start_measurement()
        """
        self._write_register(_SYSTEM__MODE_START, b"\x40")

    def set_continuous_stop_measurement(self):
        """Stops measure operation.

        UiFlow2 Code Block:

            |set_continuous_stop_measurement.png|

        MicroPython Code Block:

            .. code-block:: python

                tof_0.set_continuous_stop_measurement()
        """
        self._write_register(_SYSTEM__MODE_START, b"\x00")

    def clear_interrupt(self):
        self._write_register(_SYSTEM__INTERRUPT_CLEAR, b"\x01")

    @property
    def get_data_ready(self):
        """Returns true if new data is ready, otherwise false.

        :returns: True if new data is ready.
        :rtype: bool

        UiFlow2 Code Block:

            |get_data_ready.png|

        MicroPython Code Block:

            .. code-block:: python

                if tof_0.get_data_ready:
                    distance = tof_0.get_distance
        """
        if self._read_register(_GPIO__TIO_HV_STATUS)[0] & 0x01 == self._interrupt_polarity:
            return True
        return False

    @property
    def get_measurement_timing_budget(self):
        """Get measurement duration in milliseconds.

        :returns: The timing budget in milliseconds.
        :rtype: int

        UiFlow2 Code Block:

            |get_measurement_timing_budget.png|

        MicroPython Code Block:

            .. code-block:: python

                budget = tof_0.get_measurement_timing_budget
        """
        return self._timing_budget

    def set_measurement_timing_budget(self, val):
        """Set the measurement timing budget in milliseconds.

        :param int val: Timing budget in milliseconds.

        UiFlow2 Code Block:

            |set_measurement_timing_budget.png|

        MicroPython Code Block:

            .. code-block:: python

                tof_0.set_measurement_timing_budget(100)
        """
        reg_vals = None
        mode = self.get_distance_mode
        if mode == 1:
            reg_vals = TB_SHORT_DIST
        if mode == 2:
            reg_vals = TB_LONG_DIST
        if reg_vals is None:
            raise RuntimeError("Unknown distance mode.")
        if val not in reg_vals:
            raise ValueError("Invalid timing budget.")
        self._write_register(_RANGE_CONFIG__TIMEOUT_MACROP_A_HI, reg_vals[val][0])
        self._write_register(_RANGE_CONFIG__TIMEOUT_MACROP_B_HI, reg_vals[val][1])
        self._timing_budget = val

    @property
    def _interrupt_polarity(self):
        int_pol = self._read_register(_GPIO_HV_MUX__CTRL)[0] & 0x10
        int_pol = (int_pol >> 4) & 0x01
        return 0 if int_pol else 1

    @property
    def get_distance_mode(self):
        """Get the distance mode.

        :returns: distance mode(1=short, 2=long).
        :rtype: int

        UiFlow2 Code Block:

            |get_distance_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = tof_0.get_distance_mode
        """
        mode = self._read_register(_PHASECAL_CONFIG__TIMEOUT_MACROP)[0]
        if mode == 0x14:
            return 1  # short distance
        if mode == 0x0A:
            return 2  # long distance
        return None  # unknown

    def set_distance_mode(self, mode):
        """Set the distance mode.

        :param int mode: 1=short, 2=long.

        UiFlow2 Code Block:

            |set_distance_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                tof_0.set_distance_mode(2)  # Long distance mode
        """
        if mode == 1:
            # short distance
            self._write_register(_PHASECAL_CONFIG__TIMEOUT_MACROP, b"\x14")
            self._write_register(_RANGE_CONFIG__VCSEL_PERIOD_A, b"\x07")
            self._write_register(_RANGE_CONFIG__VCSEL_PERIOD_B, b"\x05")
            self._write_register(_RANGE_CONFIG__VALID_PHASE_HIGH, b"\x38")
            self._write_register(_SD_CONFIG__WOI_SD0, b"\x07\x05")
            self._write_register(_SD_CONFIG__INITIAL_PHASE_SD0, b"\x06\x06")
        elif mode == 2:
            # long distance
            self._write_register(_PHASECAL_CONFIG__TIMEOUT_MACROP, b"\x0a")
            self._write_register(_RANGE_CONFIG__VCSEL_PERIOD_A, b"\x0f")
            self._write_register(_RANGE_CONFIG__VCSEL_PERIOD_B, b"\x0d")
            self._write_register(_RANGE_CONFIG__VALID_PHASE_HIGH, b"\xb8")
            self._write_register(_SD_CONFIG__WOI_SD0, b"\x0f\x0d")
            self._write_register(_SD_CONFIG__INITIAL_PHASE_SD0, b"\x0e\x0e")
        else:
            raise ValueError("Unsupported mode.")
        self.set_measurement_timing_budget(self._timing_budget)

    def _write_register(self, address, data, length=None):
        if length is None:
            length = len(data)
        self._i2c.writeto_mem(self._addr, address, data[:length], addrsize=16)

    def _read_register(self, address, length=1):
        return self._i2c.readfrom_mem(self._addr, address, length, addrsize=16)

    def set_i2c_address(self, new_address):
        """Set a new I2C address to the instantiated object.

        :param int new_address: The new I2C address.

        UiFlow2 Code Block:

            |set_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                tof_0.set_i2c_address(42)
        """
        self._write_register(_VL53L1X_I2C_SLAVE_DEVICE_ADDRESS, struct.pack(">B", new_address))

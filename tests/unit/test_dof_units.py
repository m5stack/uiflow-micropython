# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import math
import inspect
import os
import sys
import types
import unittest
from unittest.mock import Mock, patch
from contextlib import ExitStack


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
LIBS = os.path.join(ROOT, "m5stack", "libs")
sys.path.insert(0, LIBS)

machine = types.ModuleType("machine")
machine.I2C = type("I2C", (), {})
sys.modules.setdefault("machine", machine)
micropython = types.ModuleType("micropython")
micropython.const = lambda value: value
sys.modules.setdefault("micropython", micropython)

from driver import bmm350, spl06  # noqa: E402
from driver.complementary import Complementary  # noqa: E402
from unit import bmm350 as bmm350_unit_module  # noqa: E402
from unit import _attrs as unit_attrs  # noqa: E402
from unit.bmm350 import BMM350Unit  # noqa: E402
from unit.dof10 import DoF10Unit  # noqa: E402
from unit.dof6 import DoF6Unit  # noqa: E402
from unit.dof9 import DoF9Unit  # noqa: E402


bmm350.time.sleep_ms = lambda _: None
bmm350.time.sleep_us = lambda _: None
spl06.time.sleep_ms = lambda _: None


def _pack_s24(value):
    value &= 0xFFFFFF
    return bytes((value >> 16, (value >> 8) & 0xFF, value & 0xFF))


def _pack_s24_le(value):
    value &= 0xFFFFFF
    return bytes((value & 0xFF, (value >> 8) & 0xFF, value >> 16))


class FakeBMM350I2C:
    def __init__(self, otp, raw_data, chip_id=0x33):
        self.otp = otp
        self.raw_data = raw_data
        self.chip_id = chip_id
        self.otp_address = 0
        self.writes = []
        self.reads = []

    def writeto_mem(self, address, register, data):
        if address != bmm350.BMM350_ADDR:
            raise AssertionError("unexpected BMM350 address 0x%02x" % address)
        value = data[0]
        self.writes.append((register, value))
        if register == 0x50:
            self.otp_address = value & 0x1F

    def readfrom_mem(self, address, register, size):
        self.reads.append((address, register, size))
        if address != bmm350.BMM350_ADDR:
            raise AssertionError("unexpected BMM350 address 0x%02x" % address)
        payload_size = size - 2
        if register == 0x00:
            payload = bytes((self.chip_id,))
        elif register == 0x55:
            payload = bytes((0x01,))
        elif register == 0x52:
            payload = bytes((self.otp[self.otp_address] >> 8,))
        elif register == 0x53:
            payload = bytes((self.otp[self.otp_address] & 0xFF,))
        elif 0x31 <= register < 0x3D:
            offset = register - 0x31
            payload = self.raw_data[offset : offset + payload_size]
        else:
            raise AssertionError("unexpected BMM350 read 0x%02x" % register)
        payload += bytes(max(0, payload_size - len(payload)))
        return b"\x00\x00" + payload[:payload_size]


class FakeSPL06I2C:
    def __init__(self, coefficients, sample):
        self.coefficients = coefficients
        self.sample = sample
        self.writes = []

    def scan(self):
        return [0x76]

    def readfrom_mem(self, address, register, size):
        if register == 0x0D:
            return bytes((0x10,))
        if register == 0x10:
            return self.coefficients
        if register == 0x28:
            return bytes((0x00,))
        if register == 0x00:
            return self.sample
        raise AssertionError("unexpected SPL06 read 0x%02x" % register)

    def writeto_mem(self, address, register, data):
        self.writes.append((register, data[0]))


def _spl_coefficients(c0=0, c1=0, c00=0, c10=0, c01=0, c11=0, c20=0, c21=0, c30=0):
    c0 &= 0xFFF
    c1 &= 0xFFF
    c00 &= 0xFFFFF
    c10 &= 0xFFFFF
    data = bytearray(18)
    data[0] = c0 >> 4
    data[1] = ((c0 & 0x0F) << 4) | (c1 >> 8)
    data[2] = c1 & 0xFF
    data[3] = c00 >> 12
    data[4] = (c00 >> 4) & 0xFF
    data[5] = ((c00 & 0x0F) << 4) | (c10 >> 16)
    data[6] = (c10 >> 8) & 0xFF
    data[7] = c10 & 0xFF
    for index, value in enumerate((c01, c11, c20, c21, c30)):
        value &= 0xFFFF
        data[8 + index * 2] = value >> 8
        data[9 + index * 2] = value & 0xFF
    return bytes(data)


class BMM350Test(unittest.TestCase):
    def test_direct_i2c_otp_decode_and_compensation(self):
        otp = [0] * 32
        otp[0x0E] = 0x0FFF  # X offset = -1, upper nibble also feeds Y.
        otp[0x0F] = 0x0000
        raw = b"".join(
            (_pack_s24_le(1000), _pack_s24_le(2000), _pack_s24_le(-3000), _pack_s24_le(0))
        )
        sensor = bmm350.BMM350(FakeBMM350I2C(otp, raw))
        field, temperature = sensor.read()
        raw_field, raw_temperature = sensor.read(raw=True)
        self.assertEqual(sensor._offset[0], -1)
        self.assertEqual(raw_field, (1000, 2000, -3000))
        self.assertEqual(raw_temperature, 0)
        self.assertTrue(all(math.isfinite(value) for value in field))
        self.assertAlmostEqual(field[0], 1000 * 0.007069979 - 1, places=5)
        self.assertAlmostEqual(field[1], 2000 * 0.007069979, places=5)
        self.assertAlmostEqual(field[2], -3000 * 0.007174964, places=5)
        self.assertAlmostEqual(temperature, -25.49, places=5)

    def test_constructor_uses_default_address_and_output_data_rate(self):
        i2c = FakeBMM350I2C([0] * 32, bytes(12))
        sensor = bmm350.BMM350(i2c, output_data_rate_hz=25)
        self.assertEqual(sensor.address, 0x14)
        self.assertEqual(sensor.output_data_rate_hz, 25)
        self.assertIn((0x04, 0x26), i2c.writes)

    def test_all_output_data_rates_write_expected_register_value(self):
        i2c = FakeBMM350I2C([0] * 32, bytes(12))
        sensor = bmm350.BMM350(i2c)
        expected = {25: 0x26, 50: 0x25, 100: 0x24, 200: 0x13, 400: 0x02}
        for rate, register_value in expected.items():
            sensor.set_output_data_rate(rate)
            self.assertEqual(i2c.writes[-2:], [(0x04, register_value), (0x06, 0x02)])
            self.assertEqual(sensor.output_data_rate_hz, rate)
        with self.assertRaises(ValueError):
            sensor.set_output_data_rate(10)

    def test_chip_id_and_i2c_errors_are_propagated(self):
        with self.assertRaises(OSError):
            bmm350.BMM350(FakeBMM350I2C([0] * 32, bytes(12), chip_id=0x00))

        class FailingI2C:
            def writeto_mem(self, address, register, data):
                raise OSError("I2C failed")

        with self.assertRaises(OSError):
            bmm350.BMM350(FailingI2C())


class FakeBMM350Sensor:
    def __init__(self, i2c, address=0x14, output_data_rate_hz=100):
        if getattr(i2c, "fail", False):
            raise OSError("BMM350 unavailable")
        self.address = address
        self.output_data_rate_hz = output_data_rate_hz
        self.samples = [((0.0, 0.0, 0.0), 0.0)]
        self.raw_samples = [((0, 0, 0), 0.0)]
        self.read_count = 0

    def read(self, raw=False):
        samples = self.raw_samples if raw else self.samples
        sample = samples[min(self.read_count, len(samples) - 1)]
        self.read_count += 1
        return sample

    def set_output_data_rate(self, rate_hz):
        if rate_hz not in (25, 50, 100, 200, 400):
            raise ValueError("unsupported rate")
        self.output_data_rate_hz = rate_hz


class BMM350UnitTest(unittest.TestCase):
    def setUp(self):
        self.original_sensor_class = bmm350_unit_module.BMM350
        bmm350_unit_module.BMM350 = FakeBMM350Sensor
        self.unit = BMM350Unit(object())

    def tearDown(self):
        bmm350_unit_module.BMM350 = self.original_sensor_class

    def test_constructor_defaults_and_hardware_failure(self):
        self.assertEqual(unit_attrs["BMM350Unit"], "bmm350")
        self.assertEqual(self.unit._sensor.address, 0x14)
        self.assertEqual(self.unit.get_output_data_rate(), 100)
        self.assertEqual(self.unit.get_axis_mapping(), (-2, -1, -3))
        self.assertEqual(BMM350Unit(object(), addr=0x15)._sensor.address, 0x15)
        failing_i2c = type("FailingBus", (), {"fail": True})()
        with self.assertRaises(OSError):
            BMM350Unit(failing_i2c)

    def test_each_measurement_getter_reads_a_fresh_sample(self):
        self.unit._sensor.samples = [
            ((1.0, 2.0, 3.0), 20.0),
            ((4.0, 5.0, 6.0), 21.0),
            ((0.0, 1.0, 0.0), 22.0),
        ]
        self.assertEqual(self.unit.get_mag(), (-2.0, -1.0, -3.0))
        self.assertEqual(self.unit.get_temperature(), 21.0)
        self.assertEqual(self.unit.get_heading(), 180.0)
        self.assertEqual(self.unit._sensor.read_count, 3)

    def test_raw_measurement_getter_returns_register_counts(self):
        self.unit._sensor.raw_samples = [((123, -456, 789), 20.0)]
        self.assertEqual(self.unit.get_mag_raw(), (123, -456, 789))

    def test_all_output_data_rates_and_invalid_value(self):
        for rate in (25, 50, 100, 200, 400):
            self.unit.set_output_data_rate(rate)
            self.assertEqual(self.unit.get_output_data_rate(), rate)
        with self.assertRaises(ValueError):
            self.unit.set_output_data_rate(10)

    def test_axis_mapping_validation_and_immediate_cache_refresh(self):
        self.unit._sensor.samples = [((1.0, 2.0, 3.0), 20.0)]
        self.unit.get_mag()
        self.unit.set_axis_mapping(-2, 1, 3)
        self.assertEqual(self.unit.get_axis_mapping(), (-2, 1, 3))
        self.unit._sensor.samples = [((1.0, 2.0, 3.0), 20.0)]
        self.assertEqual(self.unit.get_mag(), (-2.0, 1.0, 3.0))
        for mapping in ((0, 2, 3), (1, -1, 3), (1, 2, 4), (1.0, 2, 3), (True, 2, 3)):
            with self.assertRaises(ValueError):
                self.unit.set_axis_mapping(*mapping)

    def test_calibration_parameter_validation_and_clear(self):
        self.unit.set_axis_mapping(1, 2, 3)
        self.unit._sensor.samples = [((11.0, 22.0, 33.0), 20.0)]
        self.unit.get_mag()
        self.unit.set_calibration((1, 2, 3), (2, 0.5, 1))
        self.assertEqual(self.unit.get_calibration(), ((1.0, 2.0, 3.0), (2.0, 0.5, 1.0)))
        self.unit._sensor.samples = [((11.0, 22.0, 33.0), 20.0)]
        self.assertEqual(self.unit.get_mag(), (20.0, 10.0, 30.0))
        invalid = (
            ((1, 2), (1, 1, 1)),
            ("123", (1, 1, 1)),
            ((1, "2", 3), (1, 1, 1)),
            ((1, True, 3), (1, 1, 1)),
            ((1, 2, float("nan")), (1, 1, 1)),
            ((1, 2, 3), (1, 0, 1)),
            ((1, 2, 3), (1, -1, 1)),
            ((1, 2, 3), (1, float("inf"), 1)),
        )
        for offsets, scales in invalid:
            with self.assertRaises(ValueError):
                self.unit.set_calibration(offsets, scales)
        self.unit.clear_calibration()
        self.assertEqual(self.unit.get_calibration(), ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)))
        self.unit._sensor.samples = [((11.0, 22.0, 33.0), 20.0)]
        self.assertEqual(self.unit.get_mag(), (11.0, 22.0, 33.0))

    def test_calibration_state_cancel_and_repeated_start(self):
        self.assertFalse(self.unit.is_calibrating())
        self.unit.cancel_calibration()
        self.unit.start_calibration()
        self.assertTrue(self.unit.is_calibrating())
        with self.assertRaises(RuntimeError):
            self.unit.start_calibration()
        self.unit.cancel_calibration()
        self.assertFalse(self.unit.is_calibrating())
        self.unit.cancel_calibration()

    def test_calibration_rejects_insufficient_samples_and_preserves_parameters(self):
        previous = ((1.0, 2.0, 3.0), (1.1, 1.2, 1.3))
        self.unit.set_calibration(*previous)
        self.unit.start_calibration()
        for _ in range(31):
            self.unit.get_mag()
        with self.assertRaises(RuntimeError):
            self.unit.stop_calibration()
        self.assertEqual(self.unit.get_calibration(), previous)
        self.assertFalse(self.unit.is_calibrating())

    def test_calibration_rejects_insufficient_axis_range(self):
        self.unit.start_calibration()
        self.unit._sensor.samples = [((index, index, 0.0), 20.0) for index in range(32)]
        for _ in range(32):
            self.unit.get_mag()
        with self.assertRaises(RuntimeError):
            self.unit.stop_calibration()
        self.assertEqual(self.unit.get_calibration(), ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)))

    def test_synthetic_calibration_calculation_and_cache_refresh(self):
        self.unit.set_axis_mapping(1, 2, 3)
        minimum = (-10.0, -30.0, -50.0)
        maximum = (30.0, 30.0, 50.0)
        samples = [
            tuple(
                minimum[axis] + (maximum[axis] - minimum[axis]) * index / 31 for axis in range(3)
            )
            for index in range(32)
        ]
        self.unit._sensor.samples = [(sample, 21.0) for sample in samples]
        self.unit.start_calibration()
        for _ in samples:
            self.unit.get_mag()
        offsets, scales = self.unit.stop_calibration()
        self.assertEqual(offsets, (10.0, 0.0, 0.0))
        self.assertAlmostEqual(scales[0], 5.0 / 3.0)
        self.assertAlmostEqual(scales[1], 10.0 / 9.0)
        self.assertAlmostEqual(scales[2], 2.0 / 3.0)
        for value in self.unit._magnetic:
            self.assertAlmostEqual(value, 100.0 / 3.0)

    def test_heading_declination_and_wraparound(self):
        self.unit._sensor.samples = [((0.0, -1.0, 0.0), 20.0)]
        self.unit.get_mag()
        self.unit._sensor.samples = [((0.0, -1.0, 0.0), 20.0)]
        self.assertEqual(self.unit.get_heading(), 0.0)
        self.unit.set_magnetic_declination(-1.0)
        self.assertEqual(self.unit.get_magnetic_declination(), -1.0)
        self.assertEqual(self.unit.get_heading(), 359.0)
        self.unit.set_magnetic_declination(361.0)
        self.assertEqual(self.unit.get_heading(), 1.0)
        for value in (float("nan"), float("inf"), "1", True):
            with self.assertRaises(ValueError):
                self.unit.set_magnetic_declination(value)

    def test_default_heading_increases_clockwise_from_product_front(self):
        self.unit._sensor.samples = [
            ((0.0, -1.0, 0.0), 20.0),
            ((1.0, 0.0, 0.0), 20.0),
        ]
        self.assertEqual(self.unit.get_heading(), 0.0)
        self.assertEqual(self.unit.get_heading(), 270.0)

    def test_stop_without_active_calibration(self):
        with self.assertRaises(RuntimeError):
            self.unit.stop_calibration()


class SPL06Test(unittest.TestCase):
    def test_signed_coefficients_and_compensation(self):
        coefficients = _spl_coefficients(c0=-100, c1=50, c00=100000, c10=1000)
        sample = _pack_s24(7864320) + _pack_s24(0)
        sensor = spl06.SPL06(FakeSPL06I2C(coefficients, sample))
        self.assertEqual(sensor.c0, -100)
        self.assertEqual(sensor.c1, 50)
        temperature, pressure = sensor.read()
        self.assertEqual(temperature, -50.0)
        self.assertAlmostEqual(pressure, 1010.0, places=5)
        self.assertEqual(sensor.read_temperature(), -50.0)
        self.assertAlmostEqual(sensor.read_pressure(), 1010.0, places=5)
        self.assertAlmostEqual(spl06.SPL06.altitude(1013.25), 0.0, places=6)


class DoF10InterfaceTest(unittest.TestCase):
    def test_constructor_default_address_and_no_public_update(self):
        for cls in (DoF6Unit, DoF9Unit, DoF10Unit):
            self.assertEqual(list(inspect.signature(cls).parameters), ["i2c", "addr"])
            self.assertEqual(inspect.signature(cls).parameters["addr"].default, 0x68)
            self.assertFalse(hasattr(cls, "update"))

    def test_constructor_routes_selected_address_and_preserves_other_sensors(self):
        for cls in (DoF6Unit, DoF9Unit, DoF10Unit):
            for addr in (None, 0x68, 0x69):
                with self.subTest(cls=cls.__name__, addr=addr), ExitStack() as stack:
                    selected = 0x68 if addr is None else addr
                    bus = Mock()
                    bus.scan.return_value = [selected, 0x14, 0x76]
                    imu = stack.enter_context(patch("unit.dof6.BMI270"))
                    mag = stack.enter_context(patch("unit.dof9.BMM350Unit"))
                    pressure = stack.enter_context(patch("unit.dof10.SPL06"))
                    stack.enter_context(
                        patch("unit.dof6.time.ticks_us", return_value=0, create=True)
                    )
                    unit = cls(bus) if addr is None else cls(bus, addr=addr)
                    imu.assert_called_once_with(bus, address=selected)
                    self.assertIs(unit._imu, imu.return_value)
                    if cls in (DoF9Unit, DoF10Unit):
                        mag.assert_called_once_with(bus, addr=0x14)
                    else:
                        mag.assert_not_called()
                    if cls is DoF10Unit:
                        pressure.assert_called_once_with(bus, 0x76)
                    else:
                        pressure.assert_not_called()

    def test_constructor_rejects_invalid_address_before_bus_access(self):
        for cls in (DoF6Unit, DoF9Unit, DoF10Unit):
            for addr in ("0x68", 104.0, True, None, 0x00, 0x67, 0x6A, 0x80):
                error = (
                    ValueError
                    if isinstance(addr, int) and not isinstance(addr, bool)
                    else TypeError
                )
                with self.subTest(cls=cls.__name__, addr=addr):
                    bus = Mock()
                    with self.assertRaises(error):
                        cls(bus, addr=addr)
                    bus.scan.assert_not_called()

    def test_constructor_does_not_fall_back_to_other_address(self):
        from unit.unit_helper import UnitError

        for cls in (DoF6Unit, DoF9Unit, DoF10Unit):
            for selected, present in ((0x68, 0x69), (0x69, 0x68)):
                with self.subTest(cls=cls.__name__, addr=selected):
                    bus = Mock()
                    bus.scan.return_value = [present, 0x14, 0x76]
                    with patch("unit.dof6.BMI270") as imu:
                        with self.assertRaisesRegex(UnitError, "0x%02x" % selected):
                            cls(bus, addr=selected)
                        imu.assert_not_called()

    def test_pressure_sensor_temperature_and_pressure_getters(self):
        unit = DoF10Unit.__new__(DoF10Unit)

        class PressureSensor:
            def read_temperature(self):
                return 24.5

            def read_pressure(self):
                return 1008.25

        unit._pressure_sensor = PressureSensor()
        unit._sea_level_pressure = 1013.25
        unit._imu = type("IMU", (), {"temperature": lambda self: 22.0})()
        unit._magnetometer_sensor = type(
            "Magnetometer", (), {"get_temperature": lambda self: 33.0}
        )()
        self.assertEqual(unit.get_temperature(), 24.5)
        self.assertEqual(unit.get_temperature("imu"), 22.0)
        self.assertEqual(unit.get_temperature("magnetometer"), 33.0)
        self.assertEqual(unit.get_pressure(), 1008.25)
        self.assertAlmostEqual(unit.get_altitude(), 41.7, places=1)
        with self.assertRaises(ValueError):
            unit.get_temperature("unknown")


class DoF6MeasurementTest(unittest.TestCase):
    def test_si_and_raw_motion_getters(self):
        class IMU:
            def accel(self, raw=False):
                return (1000, -2000, 500) if raw else (1.0, -2.0, 0.5)

            def gyro(self, raw=False):
                return (100, -200, 300) if raw else (10.0, -20.0, 30.0)

        unit = DoF6Unit.__new__(DoF6Unit)
        unit._imu = IMU()
        unit._axis_mapping = {"accelerometer": (1, 2, 3), "gyroscope": (1, 2, 3)}
        unit._gyro_offsets = (0.0, 0.0, 0.0)
        self.assertEqual(unit.get_accel_raw(), (1000, -2000, 500))
        self.assertAlmostEqual(unit.get_accel()[0], 9.80665)
        self.assertAlmostEqual(unit.get_gyro()[0], math.radians(10.0))
        self.assertEqual(unit.get_gyro_raw(), (100, -200, 300))


class DoF9IntegrationTest(unittest.TestCase):
    def test_calibration_and_mapping_delegate_to_bmm350_unit(self):
        class Magnetometer:
            def __init__(self):
                self.calibration = None
                self.mapping = None

            def set_calibration(self, offsets, scales):
                self.calibration = (offsets, scales)

            def _apply_calibration(self, offsets, scales):
                self.calibration = (offsets, scales)

            def get_mag(self):
                return self._magnetic

            def get_temperature(self):
                return 33.0

            def set_axis_mapping(self, x_axis, y_axis, z_axis):
                self.mapping = (x_axis, y_axis, z_axis)

            _magnetic = (4.0, 5.0, 6.0)

        unit = DoF9Unit.__new__(DoF9Unit)
        unit._magnetometer_sensor = Magnetometer()
        unit._magnetometer = (0.0, 0.0, 0.0)
        unit.set_magnetometer_calibration((1, 2, 3), (-1, 1, 1))
        self.assertEqual(unit._magnetometer_sensor.calibration, ((1, 2, 3), (-1, 1, 1)))
        self.assertEqual(unit.get_mag(), (4.0, 5.0, 6.0))
        with self.assertRaises(ValueError):
            unit.set_magnetometer_calibration((1, 2, 3), (0, 1, 1))
        unit.set_axis_mapping("mag", -2, 1, 3)
        self.assertEqual(unit._magnetometer_sensor.mapping, (-2, 1, 3))
        self.assertEqual(unit.get_mag(), (4.0, 5.0, 6.0))

    def test_update_uses_bmm350_unit_field_for_tilt_aware_fusion(self):
        class Magnetometer:
            def get_mag(self):
                return (4.0, 5.0, 6.0)

        class Fusion:
            q = (1.0, 0.0, 0.0, 0.0)

            def __init__(self):
                self.arguments = None

            def update(self, accelerometer, gyroscope, magnetometer, interval):
                self.arguments = (accelerometer, gyroscope, magnetometer, interval)

            def get_attitude(self):
                return (123.0, 4.0, 5.0)

            def get_heading(self):
                return 123.0

        unit = DoF9Unit.__new__(DoF9Unit)
        unit._magnetometer_sensor = Magnetometer()
        unit._fusion = Fusion()
        unit._sample_imu = lambda: None
        unit._sample_interval = lambda: 0.01
        unit._accelerometer = (0.0, 0.0, -1.0)
        unit._gyroscope = (0.0, 0.0, 0.0)
        unit._magnetometer = (0.0, 0.0, 0.0)
        unit._advance_fusion()
        self.assertEqual(
            unit._fusion.arguments,
            ((0.0, 0.0, -1.0), (0.0, 0.0, 0.0), (4.0, 5.0, 6.0), 0.01),
        )
        self.assertEqual(unit.get_mag(), (4.0, 5.0, 6.0))
        self.assertEqual(unit.get_heading(), 123.0)
        self.assertEqual(unit.get_attitude(), (123.0, 4.0, 5.0))


class FusionAndMappingTest(unittest.TestCase):
    def test_axis_mapping_and_validation(self):
        self.assertEqual(DoF6Unit._map_vector((1, 2, 3), (-2, 1, 3)), (-2, 1, 3))
        self.assertEqual(DoF6Unit._validate_mapping(-2, 1, 3), (-2, 1, 3))
        with self.assertRaises(ValueError):
            DoF6Unit._validate_mapping(1, -1, 3)

    def test_complementary_filter_initializes_from_negative_z_gravity(self):
        fusion = Complementary(time_constant=0.5)
        accel = (0.25, -0.3, -0.92)
        fusion.update_imu(accel, (0.0, 0.0, 0.0), 0.01)
        yaw, pitch, roll = fusion.get_attitude()
        self.assertEqual(yaw, 0.0)
        self.assertAlmostEqual(
            pitch, math.degrees(math.atan2(accel[0], math.sqrt(accel[1] ** 2 + accel[2] ** 2)))
        )
        self.assertAlmostEqual(roll, math.degrees(math.atan2(-accel[1], -accel[2])))

    def test_complementary_filter_heading_and_quaternion(self):
        fusion = Complementary(time_constant=0.5)
        fusion.update((0.0, 0.0, -1.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.01)
        self.assertAlmostEqual(fusion.get_heading(), 90.0)
        self.assertAlmostEqual(fusion.get_attitude()[0], 90.0)
        for _ in range(100):
            fusion.update((0.0, 0.0, -1.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0), 0.01)
        self.assertAlmostEqual(math.sqrt(sum(value * value for value in fusion.q)), 1.0, places=6)


if __name__ == "__main__":
    unittest.main()

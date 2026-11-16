"""Host-side protocol regression tests. Run with CPython; no hardware is needed.

Expected bytes follow Renletao/chain e24b786 firmware handlers, independently
of the driver constants. These tests do not establish electrical compatibility.
"""

import ast
import importlib
import struct
import sys
import types
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "m5stack/libs"))
for name in ("machine", "micropython", "m5utils"):
    sys.modules.setdefault(name, types.ModuleType(name))
if not hasattr(time, "ticks_ms"):
    time.ticks_ms = lambda: int(time.monotonic() * 1000)

from chain.chain import ChainBus, ChainLinkLayer
from chain.dlight import DLightChain
from chain.env import ENVChain
from chain.imu import IMUChain
from chain.key import KeyChain


class FakeBus:
    def __init__(self):
        self.chainll = self
        self._device = []
        self._event = {}
        self._running = True
        self.responses = []
        self.calls = []

    register_device = ChainBus.register_device
    register_event = ChainBus.register_event
    set_rgb_color = ChainLinkLayer.set_rgb_color
    get_rgb_color = ChainLinkLayer.get_rgb_color
    set_rgb_brightness = ChainLinkLayer.set_rgb_brightness
    get_rgb_brightness = ChainLinkLayer.get_rgb_brightness
    get_device_uid = ChainLinkLayer.get_device_uid
    get_device_type = ChainLinkLayer.get_device_type
    get_firmware_version = ChainLinkLayer.get_firmware_version
    get_bootloader_version = ChainLinkLayer.get_bootloader_version

    def send(self, device_id, cmd, payload):
        self.calls.append((device_id, cmd, payload))
        if not self.responses:
            raise AssertionError("Unexpected command: %r" % (self.calls[-1],))
        return self.responses.pop(0)


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.bus = FakeBus()
        self.light = DLightChain(self.bus, 1)
        self.env = ENVChain(self.bus, 2)
        self.imu = IMUChain(self.bus, 3)

    def exchange(self, device, method, args, cmd, payload, reply, expected=None, places=None):
        self.bus.responses.append((True, reply))
        actual = (
            getattr(device, method)(**args)
            if isinstance(args, dict)
            else getattr(device, method)(*args)
        )
        if places is None:
            self.assertEqual(actual, expected)
        else:
            self.assertEqual(len(actual), len(expected))
            for value, reference in zip(actual, expected):
                self.assertIsInstance(value, float)
                self.assertAlmostEqual(value, reference, places=places)
        self.assertEqual(self.bus.calls[-1], (device.device_id, cmd, payload))
        self.assertEqual(self.bus.responses, [])

    def test_package_exports(self):
        package = importlib.import_module("chain")
        for name, cls in (
            ("DLightChain", DLightChain),
            ("ENVChain", ENVChain),
            ("IMUChain", IMUChain),
        ):
            # The existing lazy loader uses MicroPython-specific __import__
            # semantics; validate its map without replacing production code.
            module = importlib.import_module("chain." + package._attrs[name])
            self.assertIs(getattr(module, name), cls)

    def test_existing_key_interfaces_are_reused(self):
        for cls in (DLightChain, ENVChain, IMUChain):
            self.assertTrue(issubclass(cls, KeyChain))
            for name in (
                "get_device_uid",
                "get_device_type",
                "get_firmware_version",
                "get_bootloader_version",
                "set_rgb_brightness",
                "get_rgb_brightness",
            ):
                self.assertIs(getattr(cls, name), getattr(KeyChain, name))
            self.assertIs(cls.set_rgb_color, KeyChain.set_rgb_color)
            self.assertIs(cls.get_rgb_color, KeyChain.get_rgb_color)

    def test_expanded_env_and_imu_event_callbacks(self):
        seen = []
        for source in ("TEMPERATURE", "HUMIDITY", "PRESSURE", "ALTITUDE"):
            for suffix in ("HIGH_CLEAR", "HIGH", "LOW", "LOW_CLEAR"):
                event = getattr(ENVChain, "EVENT_" + source + "_" + suffix)
                self.env.set_event_callback(event, seen.append)
        self.env._alarm_mode = ENVChain.ALARM_ALL
        for raw, expected in (
            (0x55, [0x11, 0x21, 0x31, 0x41]),
            (0xAA, [0x12, 0x22, 0x32, 0x42]),
            (0xFF, [0x13, 0x23, 0x33, 0x43]),
            (0, []),
        ):
            seen.clear()
            self.env._on_event(bytes((raw, 0x0F)))
            self.assertEqual(seen, expected)
        for source, expected in ((1, 0x10), (2, 0x20), (4, 0x30), (8, 0x40)):
            self.env._alarm_mode = source
            seen.clear()
            self.env._on_event(b"\x00\x0f")
            self.assertEqual(seen, [expected])
        for suffix in (
            "ACCEL_TRIGGER",
            "ACCEL_CLEAR",
            "GYRO_TRIGGER",
            "GYRO_CLEAR",
            "TEMPERATURE_HIGH",
            "TEMPERATURE_LOW",
            "TEMPERATURE_HIGH_CLEAR",
            "TEMPERATURE_LOW_CLEAR",
        ):
            self.imu.set_event_callback(getattr(IMUChain, "EVENT_" + suffix), seen.append)
        for raw, expected in (
            (0, []),
            (5, [0x11, 0x31]),
            (7, [0x21]),
            (6, [0x10]),
            (2, [0x30]),
            (10, [0x32]),
            (14, [0x33]),
            (2, []),
            (0, [0x20]),
            (8, [0x32]),
            (0, [0x33]),
        ):
            seen.clear()
            self.imu._on_event(bytes((raw, 0x10)))
            self.assertEqual(seen, expected)
        self.assertEqual(self.bus.calls, [])  # Callback registration performs no I/O.

    def test_dlight_lux_and_threshold_order(self):
        self.exchange(self.light, "read_lux", (), 0x30, b"", b"\x78\x56\x24\x00", 2381432)
        self.exchange(
            self.light,
            "set_alarm_thresh",
            (100, 2047),
            0x33,
            b"\xff\x07\x00\x00\x64\x00\x00\x00",
            b"\x01",
        )
        self.exchange(
            self.light,
            "get_alarm_thresh",
            (),
            0x34,
            b"",
            b"\xff\x07\x00\x00\x64\x00\x00\x00",
            (100, 2047),
        )

    def test_dlight_config_encodings(self):
        for method, value, cmd, encoded in (
            ("set_gain", 18, 0x35, 4),
            ("set_resolution", 16, 0x37, 4),
            ("set_measurement_interval_ms", 500, 0x39, 3),
        ):
            self.exchange(self.light, method, (value,), cmd, bytes((encoded,)), b"\x01")
        self.exchange(self.light, "get_gain", (), 0x36, b"", b"\x02", 6)
        self.exchange(self.light, "get_resolution", (), 0x38, b"", b"\x00", 20)
        self.exchange(self.light, "get_measurement_interval_ms", (), 0x3A, b"", b"\x05", 2000)

    def test_all_dlight_option_constants(self):
        # Code 0 for interval means 25 ms on the wire, but firmware rejects it
        # for every resolution. Valid set options must retain codes 1..5.
        groups = (
            ("gain", "GAIN_", "X", (1, 3, 6, 9, 18), (0, 1, 2, 3, 4), 0x35),
            ("resolution", "RESOLUTION_", "BIT", (20, 19, 18, 17, 16), (0, 1, 2, 3, 4), 0x37),
            (
                "measurement_interval_ms",
                "MEASUREMENT_INTERVAL_",
                "MS",
                (50, 100, 500, 1000, 2000),
                (1, 2, 3, 4, 5),
                0x39,
            ),
        )
        for method, prefix, suffix, values, codes, cmd in groups:
            for value, code in zip(values, codes):
                with self.subTest(method=method, value=value):
                    option = getattr(DLightChain, prefix + str(value) + suffix)
                    self.assertEqual(option, value)
                    self.exchange(
                        self.light, "set_" + method, (option,), cmd, bytes((code,)), b"\x01"
                    )
                    self.exchange(
                        self.light, "get_" + method, (), cmd + 1, b"", bytes((code,)), value
                    )
        self.exchange(self.light, "get_measurement_interval_ms", (), 0x3A, b"", b"\x00", 25)
        self.assertFalse(hasattr(DLightChain, "MEASUREMENT_INTERVAL_25MS"))
        calls = len(self.bus.calls)
        with self.assertRaises(ValueError):
            self.light.set_measurement_interval_ms(25)
        self.assertEqual(len(self.bus.calls), calls)

    def test_all_imu_range_constants(self):
        for kind, suffix, values, codes, cmd in (
            ("accel", "G", (2, 4, 8, 16), (0, 2, 3, 1), 0x35),
            ("gyro", "DPS", (125, 250, 500, 1000, 2000), (1, 0, 2, 4, 6), 0x37),
        ):
            self.assertEqual(getattr(IMUChain, kind.upper() + "_RANGES"), values)
            for value, code in zip(values, codes):
                with self.subTest(kind=kind, value=value):
                    option = getattr(IMUChain, kind.upper() + "_RANGE_" + str(value) + suffix)
                    self.assertEqual(option, value)
                    self.exchange(
                        self.imu, "set_" + kind + "_range", (option,), cmd, bytes((code,)), b"\x01"
                    )
                    self.exchange(
                        self.imu, "get_" + kind + "_range", (), cmd + 1, b"", bytes((code,)), value
                    )

    def test_all_imu_odr_constants(self):
        # LSM6DSO accel's 1.6 Hz uses code 11, not its sorted position.
        common = (0, 12.5, 26, 52, 104, 208, 416, 833, 1660, 3330, 6660)
        for kind, values, cmd in (("accel", common + (1.6,), 0x39), ("gyro", common, 0x3B)):
            self.assertEqual(
                getattr(IMUChain, kind.upper() + "_ODR_VALUES"), tuple(sorted(values))
            )
            for code, value in enumerate(values):
                name = (
                    "ODR_POWER_DOWN"
                    if value == 0
                    else "ODR_" + str(value).replace(".", "_") + "HZ"
                )
                with self.subTest(kind=kind, value=value):
                    option = getattr(IMUChain, name)
                    self.assertEqual(option, value)
                    self.exchange(
                        self.imu, "set_" + kind + "_odr", (option,), cmd, bytes((code,)), b"\x01"
                    )
                    self.exchange(
                        self.imu, "get_" + kind + "_odr", (), cmd + 1, b"", bytes((code,)), value
                    )
        calls = len(self.bus.calls)
        with self.assertRaises(ValueError):
            self.imu.set_gyro_odr(IMUChain.ODR_1_6HZ)
        self.assertEqual(len(self.bus.calls), calls)
        self.bus.responses.append((True, b"\x0b"))
        with self.assertRaises(OSError):
            self.imu.get_gyro_odr()

    def test_all_env_odr_constants(self):
        # SPA06 alternate rates use codes 8..15, independently of frequency order.
        values = (1, 2, 4, 8, 16, 32, 64, 128, 1.5625, 3.125, 6.25, 12.5, 25, 50, 100, 200)
        self.assertEqual(ENVChain.ODR_VALUES, tuple(sorted(values)))
        for field, cmd in (("temperature", 0x32), ("pressure", 0x34)):
            for code, value in enumerate(values):
                with self.subTest(field=field, value=value):
                    option = getattr(ENVChain, "ODR_" + str(value).replace(".", "_") + "HZ")
                    self.assertEqual(option, value)
                    self.exchange(
                        self.env, "set_" + field + "_rate", (option,), cmd, bytes((code,)), b"\x01"
                    )
                    self.exchange(
                        self.env, "get_" + field + "_rate", (), cmd + 1, b"", bytes((code,)), value
                    )

    def test_alarm_modes_and_uid(self):
        for device, mask, selected in (
            (self.imu, 7, IMUChain.ALARM_ACCEL | IMUChain.ALARM_GYRO | IMUChain.ALARM_TEMPERATURE),
            (
                self.env,
                15,
                ENVChain.ALARM_TEMPERATURE
                | ENVChain.ALARM_HUMIDITY
                | ENVChain.ALARM_PRESSURE
                | ENVChain.ALARM_ALTITUDE,
            ),
        ):
            self.assertEqual(selected, mask)
            self.assertEqual(device.ALARM_ALL, mask)
            self.assertEqual(device.ALARM_NONE, 0)
            self.exchange(
                device, "set_alarm_mode", (device.ALARM_ALL,), 0xE1, bytes((mask,)), b"\x01"
            )
            self.exchange(device, "set_alarm_mode", (device.ALARM_NONE,), 0xE1, b"\x00", b"\x01")
        for device in (self.light, self.env, self.imu):
            for option, code, data in (
                (device.UID_4_BYTES, 0, b"1234"),
                (device.UID_12_BYTES, 1, b"123456789012"),
            ):
                self.assertEqual(option, code)
                self.exchange(
                    device, "get_uid", (option,), 0xF8, bytes((code,)), b"\x01" + data, data
                )

    def test_fixed_options_reject_invalid_values_without_io(self):
        for device, method, invalid in (
            (self.light, "set_gain", 2),
            (self.light, "set_resolution", 15),
            (self.light, "set_measurement_interval_ms", 200),
            (self.env, "set_temperature_rate", 0),
            (self.env, "set_pressure_rate", 104),
            (self.imu, "set_accel_range", 3),
            (self.imu, "set_gyro_range", 4000),
            (self.imu, "set_accel_odr", 25),
            (self.imu, "set_gyro_odr", 1.6),
        ):
            for value, error in (
                (invalid, ValueError),
                (True, TypeError),
                (str(invalid), TypeError),
            ):
                with self.subTest(method=method, value=value):
                    with self.assertRaises(error):
                        getattr(device, method)(value)
        self.assertEqual(self.bus.calls, [])

    def test_public_api_documentation_and_examples(self):
        repo = Path(__file__).resolve().parents[2]
        for module, cls in (
            ("dlight", DLightChain),
            ("env", ENVChain),
            ("imu", IMUChain),
        ):
            rst = (repo / "docs/source/chain" / (module + ".rst")).read_text(encoding="utf-8")
            self.assertIn(".. autoclass:: chain." + module + "." + cls.__name__, rst)
            members_line = next(
                line for line in rst.splitlines() if line.strip().startswith(":members:")
            )
            members = set(members_line.split(":members:", 1)[1].strip().split(", "))
            hidden = {
                "get_uid",
                "read_i2c_mem",
                "write_i2c_mem",
                "EVENT_TYPES",
                "EVENT_ACCEL",
                "EVENT_GYRO",
                "EVENT_TEMPERATURE",
                "EVENT_HUMIDITY",
                "EVENT_PRESSURE",
                "EVENT_ALTITUDE",
            }
            public = {
                name
                for name in cls.__dict__
                if not name.startswith(("_", "CMD_", "UID_"))
                and not name.endswith("_thresholds")
                and name not in hidden
            }
            self.assertEqual(members, public, module)
            self.assertNotIn(":inherited-members:", rst)
            self.assertIn(":show-inheritance:", rst)
            # Published Python examples must reference existing methods and
            # constants, so future renames cannot silently leave stale samples.
            examples = list((repo / "examples/chain" / module).glob("*.py"))
            for path in examples:
                tree = ast.parse(path.read_text(encoding="utf-8"))
                for node in ast.walk(tree):
                    if (
                        isinstance(node, ast.Attribute)
                        and isinstance(node.value, ast.Name)
                        and node.value.id in ("device", cls.__name__)
                    ):
                        self.assertTrue(hasattr(cls, node.attr), (path, node.attr))

    def test_sensor_gates_and_modes(self):
        for device, enable, disable, query, set_cmd, get_cmd in (
            (
                self.light,
                "enable_threshold_detection",
                "disable_threshold_detection",
                "is_threshold_detection_enabled",
                0x31,
                0x32,
            ),
            (
                self.light,
                "enable_event_reporting",
                "disable_event_reporting",
                "is_event_reporting_enabled",
                0xE1,
                0xE2,
            ),
        ):
            self.exchange(device, enable, (), set_cmd, b"\x01", b"\x01")
            self.exchange(device, disable, (), set_cmd, b"\x00", b"\x01")
            self.exchange(device, query, (), get_cmd, b"", b"\x00", False)
        for device, mask in ((self.env, 15), (self.imu, 7)):
            self.exchange(device, "set_alarm_mode", (mask,), 0xE1, bytes((mask,)), b"\x01")
            self.exchange(device, "get_alarm_mode", (), 0xE2, b"", bytes((mask,)), mask)

    def test_env_negative_temperature_and_altitude(self):
        self.exchange(
            self.env, "read_temperature_humidity", (), 0x30, b"", b"\x2e\xfb\x41", (-12.34, 65)
        )
        self.exchange(
            self.env,
            "read_pressure_temperature_altitude",
            (),
            0x31,
            b"",
            b"\x9c\xff\x95\x27\x2e\xfb\xff\xff",
            (-1.0, 101330, -12.34),
        )
        self.exchange(
            self.env,
            "read_temperature",
            (1,),
            0x31,
            b"",
            b"\x9c\xff\x95\x27\x00\x00\x00\x00",
            -1.0,
        )

    def test_env_sampling_and_reference_pressure(self):
        self.exchange(self.env, "set_temperature_rate", (1.5625,), 0x32, b"\x08", b"\x01")
        self.exchange(self.env, "get_temperature_rate", (), 0x33, b"", b"\x08", 1.5625)
        self.exchange(self.env, "set_pressure_rate", (200,), 0x34, b"\x0f", b"\x01")
        self.exchange(self.env, "get_pressure_rate", (), 0x35, b"", b"\x0f", 200)
        self.exchange(self.env, "set_sea_level_pressure", (101330,), 0x36, b"\x95\x27", b"\x01")
        self.exchange(self.env, "get_sea_level_pressure", (), 0x37, b"", b"\x95\x27", 101330)

    def test_env_alarm_payloads(self):
        fixtures = (
            ("temperature", (10, 40, 1), 0xE3, 0xE4, b"\x01\x0a\x28", (10, 40, 1)),
            ("humidity", (20, 80), 0xE5, 0xE6, b"\x14\x50", (20, 80)),
            ("pressure", (95000, 105000), 0xE7, 0xE8, b"\x1c\x25\x04\x29", (95000, 105000)),
            (
                "altitude",
                (-12.34, 1000),
                0xE9,
                0xEA,
                b"\x2e\xfb\xff\xff\xa0\x86\x01\x00",
                (-12.34, 1000),
            ),
        )
        for name, args, set_cmd, get_cmd, payload, result in fixtures:
            self.exchange(
                self.env, "set_" + name + "_alarm_thresh", args, set_cmd, payload, b"\x01"
            )
            self.exchange(
                self.env, "get_" + name + "_alarm_thresh", (), get_cmd, b"", payload, result
            )

    def test_imu_units_and_signed_raw_values(self):
        self.exchange(
            self.imu,
            "read_accel",
            (),
            0x30,
            b"",
            b"\x18\xfc\x00\x00\xe8\x03",
            (-9.80665, 0.0, 9.80665),
            places=9,
        )
        self.exchange(
            self.imu,
            "read_accel",
            (),
            0x30,
            b"",
            b"\xff\xff\x01\x00\x7b\x00",
            (-0.00980665, 0.00980665, 1.20621795),
            places=9,
        )
        self.exchange(
            self.imu,
            "read_gyro",
            (),
            0x31,
            b"",
            b"\x4c\xff\x00\x00\xb4\x00",
            (-3.141592653589793, 0.0, 3.141592653589793),
            places=9,
        )
        self.exchange(
            self.imu,
            "read_gyro",
            (),
            0x31,
            b"",
            b"\xff\xff\x00\x00\x01\x00",
            (-0.017453292519943295, 0.0, 0.017453292519943295),
            places=9,
        )
        for name, cmd in (("read_accel_raw", 0x32), ("read_gyro_raw", 0x33)):
            self.exchange(
                self.imu, name, (), cmd, b"", b"\x00\x80\xff\xff\xff\x7f", (-32768, -1, 32767)
            )
        self.exchange(self.imu, "read_temperature", (), 0x34, b"", b"\x40\x9c", 400.0)
        self.exchange(self.imu, "read_temperature", (), 0x34, b"", b"\x00\x00", 0.0)

    def test_imu_sparse_range_and_rate_encodings(self):
        self.exchange(self.imu, "set_accel_range", {"accel_scale": 16}, 0x35, b"\x01", b"\x01")
        self.exchange(self.imu, "get_accel_range", (), 0x36, b"", b"\x02", 4)
        for value, wire in ((125, 1), (250, 0), (500, 2), (1000, 4), (2000, 6)):
            self.exchange(
                self.imu, "set_gyro_range", {"gyro_scale": value}, 0x37, bytes((wire,)), b"\x01"
            )
            self.exchange(self.imu, "get_gyro_range", (), 0x38, b"", bytes((wire,)), value)
        self.exchange(self.imu, "set_accel_odr", {"accel_odr": 1.6}, 0x39, b"\x0b", b"\x01")
        self.exchange(self.imu, "get_accel_odr", (), 0x3A, b"", b"\x01", 12.5)
        self.exchange(self.imu, "set_gyro_odr", {"gyro_odr": 0}, 0x3B, b"\x00", b"\x01")
        self.exchange(self.imu, "get_gyro_odr", (), 0x3C, b"", b"\x0a", 6660)

    def test_imu_thresholds(self):
        self.exchange(
            self.imu,
            "set_motion_alarm_thresh",
            {"accel_mg": 100, "gyro_dps": 20},
            0xE3,
            b"\x64\x14",
            b"\x01",
        )
        self.exchange(self.imu, "get_motion_alarm_thresh", (), 0xE4, b"", b"\x64\x14", (100, 20))
        self.exchange(
            self.imu, "set_temperature_alarm_thresh", (10, 40), 0xE5, b"\x0a\x28", b"\x01"
        )
        self.exchange(
            self.imu, "get_temperature_alarm_thresh", (), 0xE6, b"", b"\x0a\x28", (10, 40)
        )

    def test_common_rgb_and_identity(self):
        for device, index in ((self.light, 0), (self.env, 0), (self.imu, 0)):
            self.exchange(
                device,
                "set_rgb_color",
                (0x123456,),
                0x20,
                bytes((index, 1, 0x12, 0x34, 0x56)),
                b"\x01",
                True,
            )
            self.exchange(
                device,
                "get_rgb_color",
                (),
                0x21,
                bytes((index, 1)),
                b"\x01\x12\x34\x56",
                0x123456,
            )
            self.exchange(
                device, "set_rgb_brightness", (25, True), 0x22, b"\x19\x01", b"\x01", True
            )
            self.exchange(device, "get_rgb_brightness", (), 0x23, b"", b"\x19", 25)
            self.exchange(device, "get_uid", (), 0xF8, b"\x00", b"\x01ABCD", b"ABCD")
            self.exchange(
                device, "get_uid", (1,), 0xF8, b"\x01", b"\x01ABCDEFGHIJKL", b"ABCDEFGHIJKL"
            )
            self.exchange(device, "get_bootloader_version", (), 0xF9, b"", b"\xf0", 240)
            self.exchange(device, "get_firmware_version", (), 0xFA, b"", b"\xf2", 242)
            self.exchange(device, "get_device_type", (), 0xFB, b"", b"\x11\x00", 17)

    def test_i2c_framing_and_transfer_limits(self):
        for device, limit in ((self.light, 64), (self.env, 32), (self.imu, 64)):
            self.exchange(
                device,
                "read_i2c_mem",
                (0x6B, 0x1234, 2, 16),
                0x13,
                b"\x6b\x02\x34\x12\x02",
                b"\x01\xa5\x5a",
                b"\xa5\x5a",
            )
            self.exchange(
                device,
                "write_i2c_mem",
                (0x6B, 0x10, b"\x60\x40"),
                0x14,
                b"\x6b\x01\x10\x00\x02\x60\x40",
                b"\x01",
            )
            self.exchange(
                device,
                "read_i2c_mem",
                (0x6B, 0, limit),
                0x13,
                bytes((0x6B, 1, 0, 0, limit)),
                b"\x01" + bytes(limit),
                bytes(limit),
            )
            with self.assertRaises(ValueError):
                device.read_i2c_mem(0x6B, 0, limit + 1)

    def test_reject_invalid_arguments_before_io(self):
        fixtures = (
            (self.light, "set_alarm_thresh", (2, 1), ValueError),
            (self.light, "set_alarm_thresh", (0, 2516581), ValueError),
            (self.light, "set_gain", (2,), ValueError),
            (self.light, "set_resolution", (15,), ValueError),
            (self.env, "set_temperature_alarm_thresh", (-1, 40), ValueError),
            (self.env, "set_humidity_alarm_thresh", (0, 101), ValueError),
            (self.env, "set_pressure_alarm_thresh", (29990, 100000), ValueError),
            (self.env, "set_sea_level_pressure", (101325,), ValueError),
            (self.env, "set_altitude_alarm_thresh", (0.001, 100), ValueError),
            (self.env, "set_altitude_alarm_thresh", (float("nan"), 100), ValueError),
            (self.imu, "set_gyro_range", (3,), ValueError),
            (self.imu, "set_gyro_odr", (1.6,), ValueError),
            (self.imu, "set_alarm_mode", (8,), ValueError),
            (self.light, "read_i2c_mem", (0x80, 0, 1), ValueError),
            (self.light, "read_i2c_mem", (0x6B, 256, 1), ValueError),
            (self.light, "read_i2c_mem", (0x6B, 0, 1, 12), ValueError),
            (self.light, "write_i2c_mem", (0x6B, 0, []), TypeError),
            (self.light, "write_i2c_mem", (0x6B, 0, b""), ValueError),
            (self.env, "set_event_callback", (5,), ValueError),
        )
        for device, method, args, error in fixtures:
            with self.subTest(method=method, args=args), self.assertRaises(error):
                getattr(device, method)(*args)
        self.assertEqual(self.bus.calls, [])

    def test_transport_failure_is_not_a_zero_reading(self):
        for state, reply in ((False, b""), (True, b""), (True, b"\x01"), (True, bytes(5))):
            self.bus.responses.append((state, reply))
            with self.assertRaises(OSError):
                self.light.read_lux()
        for device, method, reply in (
            (self.light, "get_gain", b"\xff"),
            (self.imu, "get_gyro_range", b"\x03"),
        ):
            self.bus.responses.append((True, reply))
            with self.assertRaises(OSError):
                getattr(device, method)()

    def test_dlight_block_callbacks_and_lifecycle(self):
        low, high, legacy = [], [], []
        self.light.set_event_callback(DLightChain.EVENT_LOW, low.append)
        self.light.set_event_callback(DLightChain.EVENT_HIGH, high.append)
        for payload in (b"\x00\x11", b"\x01\x11", b"\x02\x11", b"\x00\x10", b"\x00"):
            self.light._on_event(payload)
        self.assertEqual((low, high), ([0], [1]))
        self.light.set_event_callback(DLightChain.EVENT_LOW, None)
        self.light._on_event(b"\x00\x11")
        self.light._on_event(b"\x01\x11")
        self.assertEqual((low, high), ([0], [1, 1]))
        self.light.set_event_callback(callback=legacy.append)
        self.light._on_event(b"\x00\x11")
        self.light._on_event(b"\x01\x11")
        self.assertEqual(legacy, [0, 1])
        self.light.set_event_callback(DLightChain.EVENT_LOW, low.append)
        self.light._on_event(b"\x01\x11")
        self.assertEqual(legacy, [0, 1])
        for event, handler, error in (
            (True, low.append, TypeError),
            (2, low.append, ValueError),
            (0, 1, TypeError),
        ):
            with self.assertRaises(error):
                self.light.set_event_callback(event, handler)
        self.light._on_event(b"\x00\x11")
        self.assertEqual(low, [0, 0])
        self.light.set_event_callback(None)
        self.assertNotIn(self.light, self.bus._event)
        self.light.set_event_callback(1, high.append)
        self.light.deinit()
        self.light.deinit()
        self.light._on_event(b"\x01\x11")
        self.assertEqual(high, [1, 1])
        self.assertEqual(self.light._event_callbacks, {})
        with self.assertRaises(RuntimeError):
            self.light.set_event_callback(0, low.append)

    def test_imu_block_callbacks_and_lifecycle(self):
        accel, gyro, temperature, legacy = [], [], [], []
        self.imu.set_event_callback(IMUChain.EVENT_ACCEL, accel.append)
        self.imu.set_event_callback(IMUChain.EVENT_GYRO, gyro.append)
        self.imu.set_event_callback(IMUChain.EVENT_TEMPERATURE, temperature.append)
        for payload in (
            b"\x01\x10",
            b"\x02\x10",
            b"\x04\x10",
            b"\x03\x10",
            b"\x08\x10",
            b"\x00\x10",
        ):
            self.imu._on_event(payload)
        self.assertEqual(accel, [1, 2, 3, 8])
        self.assertEqual(gyro, [2, 4, 3, 8])
        self.assertEqual(temperature, [4, 3, 8, 0])

        self.imu.set_event_callback(IMUChain.EVENT_ACCEL, None)
        self.imu._on_event(b"\x01\x10")
        self.imu._on_event(b"\x02\x10")
        self.assertEqual(accel, [1, 2, 3, 8])
        self.assertEqual(gyro, [2, 4, 3, 8, 2])
        self.imu.set_event_callback(callback=legacy.append)
        self.imu._on_event(b"\x0f\x10")
        self.assertEqual(legacy, [15])
        self.imu.set_event_callback(IMUChain.EVENT_TEMPERATURE, temperature.append)
        self.imu._on_event(b"\x04\x10")
        self.assertEqual(legacy, [15])

        for event, handler, error in (
            (True, accel.append, TypeError),
            (8, accel.append, ValueError),
            (IMUChain.EVENT_ACCEL, 1, TypeError),
        ):
            with self.assertRaises(error):
                self.imu.set_event_callback(event, handler)

        self.imu.set_event_callback(None)
        self.assertNotIn(self.imu, self.bus._event)
        self.imu.set_event_callback(IMUChain.EVENT_ACCEL, accel.append)
        self.imu.deinit()
        self.imu.deinit()
        self.imu._on_event(b"\x01\x10")
        self.assertEqual(accel, [1, 2, 3, 8])
        self.assertEqual(self.imu._event_callbacks, {})
        with self.assertRaises(RuntimeError):
            self.imu.set_event_callback(IMUChain.EVENT_ACCEL, accel.append)

    def test_inherited_uid_and_common_failure_returns(self):
        for device in (self.light, self.env, self.imu):
            for kind, length in ((0, 4), (1, 12)):
                uid = bytes(range(length))
                self.exchange(
                    device,
                    "get_device_uid",
                    (kind,),
                    0xF8,
                    bytes((kind,)),
                    b"\x01" + uid,
                    tuple(uid),
                )
            self.bus.responses.append((True, b"\x00ABCD"))
            self.assertEqual(device.get_uid(), b"")
            self.bus.responses.append((False, b""))
            self.assertEqual(device.get_device_uid(0), ())
            self.bus.responses.append((False, b""))
            self.assertEqual(device.get_rgb_brightness(), -1)
            self.bus.responses.append((False, b""))
            self.assertFalse(device.set_rgb_color(0))

    def test_combined_events_and_legacy_callback_compatibility(self):
        scheduled = []
        sys.modules["micropython"].schedule = lambda callback, arg: scheduled.append(
            (callback, arg)
        )
        events = []
        self.env.set_event_callback(events.append)
        payload_map = self.bus._event[self.env][0xE0]
        # Combined temperature high + humidity low + altitude low recovery.
        ChainBus._dispatch_event(self.bus, payload_map, b"\xc9\x0f")
        self.assertEqual(events, [])
        callback, arg = scheduled.pop()
        callback(arg)
        self.assertEqual(events, [0xC9])
        self.imu.set_event_callback(events.append)
        for payload in (b"\x0f\x10", b"\x00\x10"):
            self.imu._on_event(payload)
        self.assertEqual(events[-2:], [15, 0])
        self.light.set_event_callback(events.append)
        self.light._on_event(b"\x00\x11")
        self.light._on_event(b"\x01\x11")
        self.assertEqual(events[-2:], [0, 1])
        legacy = lambda arg: None
        ChainBus._dispatch_event(self.bus, {b"\x01\x04": legacy, None: events.append}, b"\x01\x04")
        self.assertEqual(scheduled.pop(), (legacy, None))

    def test_callback_replacement_removal_and_lifecycle(self):
        old = []
        new = []
        self.env.set_event_callback(old.append)
        self.env.set_event_callback(new.append)
        self.env._on_event(b"\x01\x10")  # Wrong report type.
        self.env._on_event(b"\x01")
        self.env._on_event(b"\x00\x0f")
        self.assertEqual(old, [])
        self.assertEqual(new, [0])
        self.env.set_event_callback(None)
        self.assertNotIn(self.env, self.bus._event)
        self.env._on_event(b"\x01\x0f")
        self.assertEqual(new, [0])
        self.env.set_event_callback(new.append)
        self.env.deinit()
        self.env.deinit()
        self.env._on_event(b"\x01\x0f")
        self.assertEqual(new, [0])
        self.assertNotIn(self.env, self.bus._device)
        self.assertNotIn(self.env, self.bus._event)
        self.assertTrue(self.bus._running)
        with self.assertRaises(RuntimeError):
            self.env.read_temperature()
        with self.assertRaises(RuntimeError):
            self.env.set_event_callback(new.append)
        self.bus._running = False
        with self.assertRaises(RuntimeError):
            self.light.read_lux()
        with self.assertRaises(RuntimeError):
            DLightChain(self.bus, 5)

    def test_chain_wire_checksum_remains_compatible(self):
        class UART:
            def write(self, packet):
                self.packet = bytes(packet)

        uart = UART()
        link = ChainLinkLayer(uart)
        link._send_packet(1, 0x30, b"")
        # Firmware sums index + command + data; length is NOT in the checksum.
        self.assertEqual(uart.packet, b"\xaa\x55\x03\x00\x01\x30\x31\x55\xaa")


if __name__ == "__main__":
    unittest.main()

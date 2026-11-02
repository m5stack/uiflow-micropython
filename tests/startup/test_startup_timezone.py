"""Shared boot timezone defaults, including devices with preserved NVS."""

import csv
import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]


class Network(types.ModuleType):
    def __getattr__(self, name):
        return name


class Boards:
    def __getattr__(self, name):
        return name


class NVS:
    def __init__(self, zone=None):
        self.zone = zone

    def get_str(self, key):
        if key != "tz":
            return ""
        if self.zone is None:
            raise OSError("ESP_ERR_NVS_NOT_FOUND")
        return self.zone


class TimezoneTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location(
            "timezone_test_startup", ROOT / "m5stack/modules/startup/__init__.py"
        )
        self.startup = importlib.util.module_from_spec(spec)
        with mock.patch.dict(
            sys.modules,
            {
                "M5": types.SimpleNamespace(getBoard=lambda: 32),
                "esp32": types.SimpleNamespace(),
                "network": Network("network"),
            },
        ):
            spec.loader.exec_module(self.startup)
        self.apply_zone = mock.Mock()
        self.startup.time = types.SimpleNamespace(timezone=self.apply_zone)

    def test_unconfigured_device_uses_east_eight_in_shared_boot(self):
        self.startup.esp32.NVS = lambda namespace: NVS()
        self.startup._prepare_board = lambda board: None
        self.startup._apply_boot_input_override = lambda option, board, nvs: option
        self.startup.startup(self.startup.BOOT_OPT_NOTHING)
        self.apply_zone.assert_called_once_with("GMT+8")

    def test_empty_zone_uses_east_eight(self):
        self.startup._load_timezone(NVS(""))
        self.apply_zone.assert_called_once_with("GMT+8")

    def test_saved_utc_and_fractional_timezones_are_preserved(self):
        for zone in ("GMT0", "GMT+5:30", "GMT-3:30", "GMT+8"):
            with self.subTest(zone=zone):
                self.apply_zone.reset_mock()
                self.startup._load_timezone(NVS(zone))
                self.apply_zone.assert_called_once_with(zone)

    def test_factory_nvs_matches_shared_default(self):
        with (ROOT / "m5stack/partition_nvs.csv").open() as source:
            zone = next(
                row["value"] for row in csv.DictReader(source) if row["key"] == "tz"
            )
        self.assertEqual(zone, self.startup.DEFAULT_TIMEZONE)

    def test_default_lcd_brightness_is_ninety_percent(self):
        lcd = types.SimpleNamespace(isEPD=lambda: False, setBrightness=mock.Mock(), clear=mock.Mock())
        self.startup.M5.BOARD = Boards()
        self.startup.M5.Lcd = lcd
        self.startup._prepare_board(32)
        lcd.setBrightness.assert_called_once_with(230)

    def test_epaper_does_not_receive_a_backlight_setting(self):
        lcd = types.SimpleNamespace(isEPD=lambda: True, setBrightness=mock.Mock(), clear=mock.Mock())
        self.startup.M5.BOARD = Boards()
        self.startup.M5.Lcd = lcd
        self.startup._prepare_board(32)
        lcd.setBrightness.assert_not_called()


if __name__ == "__main__":
    unittest.main()

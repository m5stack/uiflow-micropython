"""Host regressions for unnecessary LCD writes during the Captain launcher loop."""

import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest import mock


class Graphics:
    FONTS = types.SimpleNamespace(
        **{f"Montserrat{size}": size for size in (12, 16, 18, 24)}
    )

    def __init__(self, parent=None):
        self.parent = parent
        self.calls = []
        self.canvases = []

    def newCanvas(self, *args):  # noqa: N802 - match the device API
        canvas = Graphics(self)
        self.canvases.append(canvas)
        return canvas

    def push(self, x, y):
        self.parent.calls.append(("push", x, y))

    def __getattr__(self, name):
        return lambda *args: self.calls.append((name, *args))


class Startup:
    state = 2
    rssi = -48

    def connect_status(self):
        return self.state

    def get_rssi(self):
        return self.rssi


class StatusRefreshTests(unittest.TestCase):
    def setUp(self):
        package = types.ModuleType("captain_test_startup")
        package.__path__ = []
        package.Startup = Startup
        package.print_access_info = lambda *args: None
        self.lcd = Graphics()
        self.battery = 86
        self.charging = 0
        self.minute = 41
        self.service = 2
        self.access_code = "A8F2C6"
        self.nickname = "M5-Lab"
        modules = {
            package.__name__: package,
            "M5": types.SimpleNamespace(
                Lcd=self.lcd,
                Power=types.SimpleNamespace(
                    getBatteryLevel=lambda: self.battery,
                    isCharging=lambda: self.charging,
                ),
            ),
            "network": types.SimpleNamespace(STAT_GOT_IP=2, STAT_CONNECTING=1),
            "esp32": types.SimpleNamespace(firmware_info=lambda: (0, 0, 0, "v2.5.4")),
            "M5Things": types.SimpleNamespace(
                status=lambda: self.service,
                accesscode=lambda: self.access_code,
                nick_name=lambda: self.nickname,
            ),
        }
        source = (
            Path(__file__).resolve().parents[2]
            / "m5stack/modules/startup/chain_captain.py"
        )
        icon_spec = importlib.util.spec_from_file_location(
            package.__name__ + ".chain_captain_icons",
            source.with_name("chain_captain_icons.py"),
        )
        icons = importlib.util.module_from_spec(icon_spec)
        icon_spec.loader.exec_module(icons)
        modules[icon_spec.name] = icons
        spec = importlib.util.spec_from_file_location(
            package.__name__ + ".chain_captain", source
        )
        self.controller = importlib.util.module_from_spec(spec)
        with mock.patch.dict(sys.modules, modules):
            spec.loader.exec_module(self.controller)
        self.controller.time = types.SimpleNamespace(
            localtime=lambda: (2026, 11, 2, 9, self.minute, 0, 0, 0)
        )
        self.app = self.controller.ChainCaptain_Startup()
        self.app._draw_static()
        self.app._refresh()
        self.clear_calls()

    def clear_calls(self):
        self.lcd.calls.clear()
        for canvas in self.lcd.canvases:
            canvas.calls.clear()

    def test_unchanged_loop_performs_no_drawing_or_sprite_allocation(self):
        canvases = tuple(self.lcd.canvases)
        for _ in range(120):
            self.app._refresh()
        self.assertEqual(self.lcd.calls, [])
        self.assertTrue(all(not canvas.calls for canvas in canvases))
        self.assertEqual(tuple(self.lcd.canvases), canvases)

    def test_initial_screen_contains_no_identity_placeholder(self):
        self.app._draw_static()
        text = [call[1] for call in self.lcd.calls if call[0] == "drawCenterString"]
        self.assertIn("Access Code", text)
        self.assertIn("Nickname", text)
        self.assertFalse(any("Waiting" in value for value in text))
        self.assertEqual(
            [
                call
                for call in self.lcd.calls
                if call[0] == "drawCenterString" and call[3] in (112, 181)
            ],
            [],
        )

    def test_empty_cloud_identity_stays_blank(self):
        self.access_code = self.nickname = ""
        self.app._refresh()
        values = [
            (call[1], call[3])
            for call in self.lcd.calls
            if call[0] == "drawCenterString" and call[3] in (112, 181)
        ]
        self.assertEqual(values, [("", 112), ("", 181)])

    def test_available_code_does_not_fill_missing_nickname(self):
        self.nickname = ""
        self.app._refresh()
        values = [
            (call[1], call[3])
            for call in self.lcd.calls
            if call[0] == "drawCenterString" and call[3] in (112, 181)
        ]
        self.assertEqual(values, [("A8F2C6", 112), ("", 181)])

    def test_minute_change_pushes_only_the_clock(self):
        self.minute = 42
        self.app._refresh()
        self.assertEqual(self.lcd.calls, [("push", 85, 0)])
        self.assertIn(("drawCenterString", "09:42", 35, 6), self.lcd.canvases[1].calls)

    def test_subpixel_battery_change_does_not_redraw(self):
        self.battery = 87
        self.app._refresh()
        self.assertEqual(self.lcd.calls, [])

    def test_low_battery_and_charging_update_only_the_battery(self):
        self.battery = 8
        self.app._refresh()
        self.assertEqual(self.lcd.calls, [("push", 201, 0)])
        self.clear_calls()
        self.charging = 1
        self.app._refresh()
        self.assertEqual(self.lcd.calls, [("push", 201, 0)])

    def test_signal_level_change_does_not_touch_clock_or_battery(self):
        self.app.rssi = -85
        self.app._refresh()
        self.assertEqual(self.lcd.calls, [("push", 10, 0)])
        self.clear_calls()
        self.app.rssi = -82
        self.app._refresh()
        self.assertEqual(self.lcd.calls, [])

    def test_connection_failure_and_recovery_leave_other_status_fields_untouched(self):
        self.app.state = -1
        self.app._refresh("Network not found")
        self.assertEqual(
            [call for call in self.lcd.calls if call[0] == "push"], [("push", 10, 0)]
        )
        self.clear_calls()
        self.app.state = 2
        self.app._refresh()
        self.assertEqual(
            [call for call in self.lcd.calls if call[0] == "push"], [("push", 10, 0)]
        )
        self.assertEqual(self.app._error, "")


if __name__ == "__main__":
    unittest.main()

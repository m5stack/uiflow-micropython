"""Controller checks with deterministic network, power and NVS substitutes."""
import importlib.util
from pathlib import Path
import sys
import time
import types
import unittest
from unittest import mock


root = Path(__file__).resolve().parent
if not (root / "corep4x.py").exists():
    root = root.parents[1] / "m5stack" / "modules" / "startup"
package = types.ModuleType("startup")
package.__path__ = [str(root)]
package.print_access_info = lambda *args: None
substitutes = {"startup": package}
view_module = types.ModuleType("startup.corep4x_ui")
view_module.CoreP4XView = object
view_module.ACCENT, view_module.CHARGING, view_module.DANGER = 1, 2, 3
substitutes[view_module.__name__] = view_module
for name in ("M5", "esp32", "m5ui", "network", "M5Things"):
    substitutes[name] = types.ModuleType(name)
network = substitutes["network"]
for index, name in enumerate(
    (
        "STAT_IDLE",
        "STAT_CONNECTING",
        "STAT_GOT_IP",
        "STAT_WRONG_PASSWORD",
        "STAT_NO_AP_FOUND",
        "STAT_NO_AP_FOUND_IN_RSSI_THRESHOLD",
        "STAT_NO_AP_FOUND_IN_AUTHMODE_THRESHOLD",
        "STAT_NO_AP_FOUND_W_COMPATIBLE_SECURITY",
        "STAT_ASSOC_FAIL",
        "STAT_HANDSHAKE_TIMEOUT",
        "STAT_BEACON_TIMEOUT",
    )
):
    setattr(network, name, index)
spec = importlib.util.spec_from_file_location("startup.corep4x", root / "corep4x.py")
controller = importlib.util.module_from_spec(spec)
with mock.patch.dict(sys.modules, substitutes):
    spec.loader.exec_module(controller)
controller.time = types.SimpleNamespace(
    ticks_add=lambda now, delay: (now + delay) % (1 << 30),
    ticks_diff=lambda left, right: ((left - right + (1 << 29)) % (1 << 30)) - (1 << 29),
    localtime=time.localtime,
)


class NVS:
    def __init__(self):
        self.values = {"ssid0": "saved-network", "pswd0": "saved-password"}
        self.commits = 0
        self.fail_commit = False

    def set_str(self, key, value):
        self.values[key] = value

    set_u8 = set_str

    def get_u8(self, key):
        if key not in self.values:
            raise OSError("missing key")
        return self.values[key]

    def commit(self):
        if self.fail_commit:
            raise OSError("flash write failed")
        self.commits += 1


class WLAN:
    def __init__(self):
        self.network = self
        self.state = network.STAT_IDLE
        self.connections = []
        self.dhcp = False
        self.scan_records = []
        self.scan_error = None
        self.scan_count = 0

    def scan(self):
        self.scan_count += 1
        if self.scan_error:
            raise self.scan_error
        return self.scan_records

    def disconnect(self):
        self.state = network.STAT_IDLE

    def ipconfig(self, dhcp4):
        self.dhcp = dhcp4

    def connect_network(self, ssid, password, **config):
        self.connections.append((ssid, password, config))
        self.state = network.STAT_CONNECTING
        return True

    def connect_status(self):
        return self.state

    wifi_status_str = m5things_status_str = staticmethod(str)

    def local_ip(self):
        return "192.0.2.2"

    def get_rssi(self):
        return -48


class View:
    editing_password = False

    def is_password_editing(self):
        return self.editing_password

    def set_connection_info(self, *args):
        self.connection_info = args

    def set_timezone_result(self, message, success):
        self.timezone_result = message, success

    def set_timezone_offset(self, offset):
        self.timezone_offset = offset

    def set_saved_network(self, ssid, password):
        self.saved_network = ssid, password

    def set_scan_state(self, message, busy=False, error=False):
        self.scan_state = message, busy, error

    def set_scan_results(self, networks):
        self.networks = networks

    def set_network_result(self, message, color=1, busy=False):
        self.result, self.busy = message, busy

    def set_brightness(self, value):
        self.brightness = value

    def set_identity(self, code, nickname):
        self.identity = code, nickname

    def set_status(self, *args):
        self.status = args


class StartupTests(unittest.TestCase):
    def setUp(self):
        self.wlan, self.nvs = WLAN(), NVS()
        package.Startup = lambda: self.wlan
        controller.esp32.NVS = lambda name: self.nvs
        self.backlight = []
        controller.M5.Lcd = types.SimpleNamespace(
            setBrightness=self.backlight.append, getBrightness=lambda: 128
        )
        controller.M5.Power = types.SimpleNamespace(
            getBatteryLevel=lambda: 86, isCharging=lambda: 0
        )
        controller.M5.update = lambda: None
        controller.M5Things.status = lambda: 0
        controller.M5Things.accesscode = lambda: "ACTUAL"
        controller.M5Things.nick_name = lambda: "Actual device"
        self.app = controller.CoreP4X_Startup()
        self.app._wlan = self.wlan
        self.app._view = View()

    def connect(self, now=0):
        self.app._queue_wifi("new-network", "new-password")
        self.assertEqual(self.wlan.connections, [])
        self.assertEqual(self.nvs.commits, 0)
        self.app._step(now)

    def test_connect_saves_only_after_ip_and_enables_dhcp(self):
        self.connect()
        self.assertTrue(self.wlan.dhcp)
        self.assertEqual(self.nvs.values["ssid0"], "saved-network")
        self.wlan.state = network.STAT_GOT_IP
        self.app._step(200)
        self.assertEqual(self.nvs.values["ssid0"], "new-network")
        self.assertEqual(self.nvs.values["protocol"], "DHCP")
        self.assertEqual(self.nvs.commits, 1)
        self.assertEqual(self.app._view.result, "Connected")
        self.assertFalse(self.app._view.busy)

    def test_wrong_password_preserves_saved_credentials_and_allows_retry(self):
        self.connect()
        self.wlan.state = network.STAT_WRONG_PASSWORD
        self.app._step(100)
        self.assertEqual(self.app._view.result, "Wrong password")
        self.assertEqual(self.nvs.values["pswd0"], "saved-password")
        self.assertEqual(self.nvs.commits, 0)
        self.app._queue_wifi("retry", "")
        self.app._step(200)
        self.assertEqual(self.wlan.connections[-1][:2], ("retry", ""))

    def test_timeout_across_tick_wrap_cancels_connection(self):
        start = (1 << 30) - 1000
        self.connect(start)
        self.app._step(controller.time.ticks_add(start, 60000))
        self.assertEqual(self.app._view.result, "Connection timed out")
        self.assertEqual(self.wlan.state, network.STAT_IDLE)
        self.assertEqual(self.nvs.commits, 0)

    def test_failed_save_does_not_claim_saved_connection(self):
        self.connect()
        self.nvs.fail_commit = True
        self.wlan.state = network.STAT_GOT_IP
        self.app._step(100)
        self.assertEqual(self.app._view.result, "Connected; could not save settings")
        self.assertFalse(self.app._view.busy)

    def test_static_saved_config_is_used_without_overwriting_it(self):
        config = {
            "protocol": "STATIC",
            "ip": "192.0.2.5",
            "netmask": "255.255.255.0",
            "gateway": "192.0.2.1",
            "dns": "192.0.2.1",
        }
        self.app._queue_connection("saved-network", "saved-password", False, config)
        self.app._step(0)
        self.assertEqual(self.wlan.connections[-1][2], config)
        self.assertFalse(self.wlan.dhcp)
        self.wlan.state = network.STAT_GOT_IP
        self.app._step(100)
        self.assertEqual(self.nvs.commits, 0)

    def test_byte_limits_reject_multibyte_overflow(self):
        self.app._queue_wifi("网" * 11, "")
        self.assertIsNone(self.app._pending_connect)
        self.app._queue_wifi("valid", "密" * 22)
        self.assertIsNone(self.app._pending_connect)
        self.assertEqual(self.wlan.connections, [])

    def test_brightness_coalesces_and_persists_after_drag_stops(self):
        for value in range(30, 81):
            self.app._queue_brightness(value)
        self.assertEqual(self.backlight, [])
        self.app._step(0)
        self.assertEqual(self.backlight, [204])
        self.app._step(400)
        self.assertEqual(self.nvs.commits, 0)
        self.app._step(500)
        self.assertEqual(self.nvs.values[controller._BRIGHTNESS_KEY], 80)
        self.assertEqual(self.nvs.commits, 1)

    def test_offline_clears_stale_cloud_identity_and_unknown_charge_is_not_green(self):
        controller.M5Things.status = lambda: 2
        controller.M5.Power.getBatteryLevel = lambda: -1
        controller.M5.Power.isCharging = lambda: 2
        self.wlan.state = network.STAT_GOT_IP
        self.app._refresh_state()
        self.assertEqual(self.app._view.identity, ("ACTUAL", "Actual device"))
        self.assertEqual(self.app._view.status[:4], ("connected", "online", None, False))
        self.wlan.state = network.STAT_IDLE
        self.app._refresh_state()
        self.assertEqual(self.app._view.identity, ("", ""))
        self.assertEqual(self.app._view.status[:2], ("unconfigured", "offline"))

    def test_saved_network_distinguishes_disconnected_from_unconfigured(self):
        self.app._refresh_state()
        self.assertEqual(self.app._view.status[:2], ("unconfigured", "offline"))
        self.app._configured = True
        self.app._refresh_state()
        self.assertEqual(self.app._view.status[:2], ("disconnected", "offline"))

    def test_service_is_online_only_after_cloud_connection(self):
        self.wlan.state = network.STAT_GOT_IP
        for status in (-2, -1, 0, 1, 2, 3):
            controller.M5Things.status = lambda status=status: status
            self.app._refresh_state()
            self.assertEqual(self.app._view.status[1], "online" if status == 2 else "offline")

    def test_scan_thread_start_failure_allows_retry(self):
        with mock.patch.object(
            controller._thread, "start_new_thread", side_effect=OSError("no memory")
        ):
            self.app._queue_scan()
            self.app._step(0)
        self.assertFalse(self.app._scanning)
        self.assertTrue(self.app._view.scan_state[2])
        self.app._queue_scan()
        self.assertTrue(self.app._scan_requested)

    def test_scan_omits_hidden_and_invalid_names_and_keeps_strongest(self):
        records = [
            (b"Lab", b"a", 1, -80, 3, False),
            (b"Lab", b"b", 6, -40, 3, False),
            (b"Lab", b"c", 6, -50, 0, False),
            ("办公室".encode(), b"d", 11, -30, 3, False),
            (b"", b"e", 1, -20, 3, True),
            (b"\xff", b"f", 1, -10, 3, False),
        ]
        self.assertEqual(
            self.app._scan_networks(records),
            [("办公室", -30, True), ("Lab", -40, True), ("Lab", -50, False)],
        )

    def test_scan_is_queued_once_and_waits_for_connection_to_finish(self):
        jobs = []
        with mock.patch.object(
            controller._thread,
            "start_new_thread",
            side_effect=lambda function, args: jobs.append((function, args)),
        ):
            self.connect()
            self.app._queue_scan()
            self.app._queue_scan()
            self.app._step(100)
            self.assertEqual(jobs, [])
            self.wlan.state = network.STAT_GOT_IP
            self.app._step(200)
            self.assertEqual(len(jobs), 1)
            self.assertEqual(self.wlan.scan_count, 0)
            self.app._queue_scan()
            self.app._step(300)
            self.assertEqual(len(jobs), 1)
            jobs[0][0](*jobs[0][1])
            self.assertFalse(hasattr(self.app._view, "networks"))
            self.app._step(400)
            self.assertEqual(self.app._view.networks, [])
            self.assertFalse(self.app._scanning)

    def test_failed_scan_allows_retry_and_preserves_credentials(self):
        jobs = []
        with mock.patch.object(
            controller._thread,
            "start_new_thread",
            side_effect=lambda function, args: jobs.append((function, args)),
        ):
            self.wlan.scan_error = OSError("busy")
            self.app._queue_scan()
            self.app._step(0)
            jobs.pop()[0]()
            self.app._step(100)
            self.assertTrue(self.app._view.scan_state[2])
            self.assertFalse(self.app._scanning)
            self.wlan.scan_error = None
            self.wlan.scan_records = [(b"Lab", b"a", 1, -40, 3, False)]
            self.app._queue_scan()
            self.app._step(200)
            jobs.pop()[0]()
            self.app._step(300)
            self.assertEqual(self.app._view.networks, [("Lab", -40, True)])
            self.assertEqual(self.nvs.values["ssid0"], "saved-network")
            self.assertEqual(self.nvs.commits, 0)

    def apply_timezone(self, offset):
        self.rtc_writes = []
        self.zone_writes = []
        machine = types.ModuleType("machine")
        machine.RTC = lambda: types.SimpleNamespace(datetime=self.rtc_writes.append)
        with mock.patch.dict(sys.modules, {"machine": machine}), mock.patch.multiple(
            controller.time,
            timezone=self.zone_writes.append,
            create=True,
        ):
            self.app._queue_timezone(offset)
            self.assertEqual(self.zone_writes, [])
            self.assertEqual(self.rtc_writes, [])
            self.app._apply_timezone()
            self.assertEqual(self.rtc_writes, [])

    def test_beijing_timezone_changes_local_display_without_writing_rtc(self):
        self.apply_timezone(480)
        self.assertEqual(self.nvs.values["tz"], "GMT+8:00")
        self.assertEqual(self.zone_writes, ["GMT+8:00"])
        self.assertEqual(self.app._view.timezone_result, ("Saved", True))
        self.assertEqual(self.app._view.timezone_offset, 480)
        self.assertEqual(self.nvs.commits, 1)

    def test_fractional_negative_and_positive_timezones(self):
        self.apply_timezone(-210)
        self.assertEqual(self.nvs.values["tz"], "GMT-3:30")
        self.assertEqual(self.zone_writes, ["GMT-3:30"])
        self.apply_timezone(345)
        self.assertEqual(self.nvs.values["tz"], "GMT+5:45")
        self.assertEqual(self.zone_writes, ["GMT+5:45"])

    def test_invalid_timezone_does_not_change_clock_or_configuration(self):
        for offset in (-721, 841, 480.5, "480"):
            self.apply_timezone(offset)
            self.assertEqual(self.zone_writes, [])
            self.assertEqual(self.nvs.commits, 0)
            self.assertFalse(self.app._view.timezone_result[1])

    def test_timezone_save_failure_reports_applied_but_not_saved_and_allows_retry(self):
        self.nvs.fail_commit = True
        self.apply_timezone(345)
        self.assertFalse(self.app._view.timezone_result[1])
        self.assertIn("not saved", self.app._view.timezone_result[0])
        self.assertEqual(self.app._view.timezone_offset, 345)
        self.nvs.fail_commit = False
        self.apply_timezone(345)
        self.assertEqual(self.app._view.timezone_result, ("Saved", True))

    def test_password_editing_defers_telemetry_and_refreshes_after_exit(self):
        self.app._view.editing_password = True
        with mock.patch.object(self.app, "_refresh_state") as refresh:
            for now in (0, 1000, 2000):
                self.app._step(now)
            refresh.assert_not_called()
            self.app._view.editing_password = False
            self.app._step(2100)
            refresh.assert_called_once()

    def test_password_editing_does_not_block_pending_connection(self):
        self.app._view.editing_password = True
        self.connect()
        self.assertEqual(self.wlan.connections[-1][:2], ("new-network", "new-password"))
        self.wlan.state = network.STAT_GOT_IP
        self.app._step(200)
        self.assertEqual(self.app._view.result, "Connected")


if __name__ == "__main__":
    unittest.main()

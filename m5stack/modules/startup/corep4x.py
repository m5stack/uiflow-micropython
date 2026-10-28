# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import asyncio
import esp32
import M5
import m5ui
import network
import startup
import time
import _thread

from .corep4x_ui import CoreP4XView, ACCENT, CHARGING, DANGER

try:
    import M5Things
except ImportError:
    M5Things = None


_BRIGHTNESS_KEY = "p4x_brightness"
_MODULE_MESSAGE = "Wi-Fi module unavailable\nCheck connection and restart"
_WIFI_ERRORS = {
    network.STAT_WRONG_PASSWORD: "Wrong password",
    network.STAT_NO_AP_FOUND: "Network not found",
    network.STAT_NO_AP_FOUND_IN_RSSI_THRESHOLD: "Network signal too weak",
    network.STAT_NO_AP_FOUND_IN_AUTHMODE_THRESHOLD: "Unsupported network security",
    network.STAT_NO_AP_FOUND_W_COMPATIBLE_SECURITY: "Unsupported network security",
    network.STAT_ASSOC_FAIL: "Connection failed",
    network.STAT_HANDSHAKE_TIMEOUT: "Connection timed out",
    network.STAT_BEACON_TIMEOUT: "Network signal lost",
}


def create_lan():
    from machine import Pin, unique_id

    nic = network.LAN(
        0,
        phy_addr=1,
        phy_type=network.PHY_IP101,
        mdc=Pin(31),
        mdio=Pin(36),
        power=Pin(52),
        ref_clk=Pin(32),
        tx_en=Pin(33),
        txd0=Pin(41),
        txd1=Pin(35),
        crs_dv=Pin(28),
        rxd0=Pin(29),
        rxd1=Pin(30),
    )
    nic.config(mac=unique_id())
    return nic


class CoreP4X_Startup:
    def __init__(self) -> None:
        self._wlan = None
        self._nvs = esp32.NVS("uiflow")
        self._view = None
        self._pending_connect = None
        self._connection = None
        self._pending_brightness = None
        self._pending_timezone = None
        self._brightness_save_at = None
        self._brightness = 70
        self._last_refresh = None
        self._last_log_state = None
        self._wifi_error = False
        self._timeout_ms = 60000
        self._configured = False
        self._scan_requested = False
        self._scanning = False
        self._scan_result = None
        self._lan = None
        self._net_mode = "WIFI"
        self._pending_mode = None
        self._active_config = {"protocol": "DHCP"}
        self._eth_static = False
        self._eth_error = ""
        self._mode_save_error = ""
        self._wifi_attempted = False
        self._saved_ssid = ""
        self._saved_password = ""

    def startup(
        self,
        ssid: str,
        pswd: str,
        protocol: str = "",
        ip: str = "",
        netmask: str = "",
        gateway: str = "",
        dns: str = "",
        timeout: int = 60,
        net_mode: str = "WIFI",
    ) -> None:
        self._timeout_ms = max(1, timeout) * 1000
        M5.Lcd.setRotation(0)
        m5ui.init()
        try:
            self._view = CoreP4XView(
                self._get_version(),
                self._queue_brightness,
                self._queue_wifi,
                self._queue_scan,
                self._queue_mode,
                self._get_timezone,
                self._queue_timezone,
            )
            self._load_brightness()
            self._view.set_timezone_offset(self._get_timezone())
            self._configured = bool(ssid)
            self._saved_ssid, self._saved_password = ssid, pswd
            self._net_mode = "ETH" if net_mode == "ETH" else "WIFI"
            self._view.set_network_mode(self._net_mode)
            self._view.set_saved_network(ssid, pswd)
            self._view.set_wifi_available(False)
            battery, charging = self._power_state()
            self._view.set_status("checking", "offline", battery, charging, self._clock())
            config = {
                "protocol": protocol or "DHCP",
                "ip": ip,
                "netmask": netmask,
                "gateway": gateway,
                "dns": dns,
            }
            asyncio.run(self._main(ssid, pswd, config))
        finally:
            self._save_brightness()
            m5ui.deinit()

    @staticmethod
    def _get_version():
        try:
            version = str(esp32.firmware_info()[3]).lstrip("vV")
            return "v" + version if version else "v--"
        except (OSError, IndexError, TypeError):
            return "v--"

    def _load_brightness(self):
        try:
            value = self._nvs.get_u8(_BRIGHTNESS_KEY)
        except OSError:
            value = (M5.Lcd.getBrightness() * 100 + 127) // 255
        self._brightness = max(10, min(100, value))
        M5.Lcd.setBrightness((self._brightness * 255 + 50) // 100)
        self._view.set_brightness(self._brightness)

    def _queue_brightness(self, value):
        self._pending_brightness = value

    @staticmethod
    def _get_timezone():
        now = time.time()
        # MicroPython mktime() uses UTC regardless of time.timezone().
        return (time.mktime(time.localtime(now)) - time.mktime(time.gmtime(now))) // 60

    def _queue_timezone(self, offset):
        self._pending_timezone = offset

    def _apply_timezone(self):
        if self._pending_timezone is None:
            return
        offset, self._pending_timezone = self._pending_timezone, None
        if not isinstance(offset, int) or not -720 <= offset <= 840:
            self._view.set_timezone_result("Invalid time zone", False)
            return
        zone = "GMT%s%d:%02d" % ("+" if offset >= 0 else "-", abs(offset) // 60, abs(offset) % 60)
        try:
            # Change local display time only; never write the system/RTC clock.
            time.timezone(zone)
        except (OSError, RuntimeError, ValueError) as error:
            self._view.set_timezone_result(str(error), False)
            return
        self._last_refresh = None
        self._view.set_timezone_offset(offset)
        try:
            self._nvs.set_str("tz", zone)
            self._nvs.commit()
        except OSError:
            self._view.set_timezone_result("Applied; time zone was not saved", False)
            return
        self._view.set_timezone_result("Saved", True)

    def _apply_brightness(self, now):
        if self._pending_brightness is not None:
            value, self._pending_brightness = self._pending_brightness, None
            try:
                M5.Lcd.setBrightness((value * 255 + 50) // 100)
                self._brightness = value
                self._brightness_save_at = time.ticks_add(now, 500)
            except (OSError, RuntimeError) as error:
                self._view.set_brightness(self._brightness)
                print("[Display]: brightness update failed:", error)
        if self._brightness_save_at is not None:
            if time.ticks_diff(now, self._brightness_save_at) >= 0:
                self._save_brightness()

    def _save_brightness(self):
        if self._brightness_save_at is None:
            return
        self._brightness_save_at = None
        try:
            self._nvs.set_u8(_BRIGHTNESS_KEY, self._brightness)
            self._nvs.commit()
        except OSError as error:
            print("[Display]: brightness save failed:", error)

    def _queue_wifi(self, ssid, password):
        if self._net_mode != "WIFI":
            return
        if self._wlan is None:
            self._view.set_network_result(_MODULE_MESSAGE, DANGER)
            return
        if self._scanning:
            self._view.set_network_result("Wait for scan to finish", DANGER)
            return
        self._queue_connection(ssid, password, True, {"protocol": "DHCP"})

    def _queue_scan(self):
        if self._net_mode != "WIFI":
            return
        if self._wlan is None:
            self._view.set_scan_state(_MODULE_MESSAGE, error=True)
            return
        if self._scanning or self._scan_requested:
            return
        self._scan_requested = True
        self._view.set_scan_state("Scanning...", True)

    @staticmethod
    def _scan_networks(records):
        # The same SSID can have multiple BSSIDs. Keep the strongest per
        # security class; an open AP must not hide a secured AP of that name.
        unique = {}
        for raw_ssid, bssid, channel, rssi, authmode, hidden in records:
            try:
                ssid = raw_ssid.decode("utf-8")
            except UnicodeError:
                continue
            if not ssid:
                continue
            key = ssid, authmode != 0
            if key not in unique or rssi > unique[key][1]:
                unique[key] = ssid, rssi, authmode != 0
        return sorted(unique.values(), key=lambda ap: ap[1], reverse=True)

    def _scan_worker(self):
        # scan() releases the GIL while ESP-Hosted scans. This worker only
        # returns data; LVGL and NVS remain on the main interpreter thread.
        try:
            result = self._scan_networks(self._wlan.network.scan())
            self._scan_result = True, result
        except Exception as error:
            print("[Wi-Fi]: scan failed:", error)
            self._scan_result = False, None

    def _poll_scan(self):
        if self._wlan is None:
            self._scan_result = None
            return
        if self._scan_result is not None:
            success, result = self._scan_result
            self._scan_result = None
            self._scanning = False
            if success:
                self._view.set_scan_results(result)
            else:
                self._view.set_scan_state("Scan failed. Tap Refresh to retry", error=True)
        if (
            self._scan_requested
            and not self._scanning
            and self._connection is None
            and self._pending_connect is None
            and self._pending_mode is None
        ):
            self._scan_requested = False
            self._scanning = True
            try:
                _thread.start_new_thread(self._scan_worker, ())
            except (OSError, RuntimeError):
                self._scanning = False
                self._view.set_scan_state("Scan failed. Tap Refresh to retry", error=True)

    def _queue_mode(self, mode):
        if mode in ("WIFI", "ETH"):
            self._pending_mode = mode
            if self._scanning:
                self._view.set_connection_info("connecting", message="Waiting for Wi-Fi scan")

    def _activate_mode(self, mode, config, save=False):
        self._pending_connect = None
        self._connection = None
        self._scan_requested = False
        self._wifi_error = False
        self._eth_error = ""
        self._mode_save_error = ""
        self._last_log_state = None
        self._view.set_network_result("")
        # This runs on the main interpreter thread, after any scan has finished.
        interfaces = (self._wlan.network if self._wlan is not None else None, self._lan)
        for nic in interfaces:
            if nic is not None:
                try:
                    if nic.active():
                        nic.active(False)
                except (OSError, RuntimeError) as error:
                    print("[NET]: interface stop failed:", error)
        self._net_mode = mode
        self._active_config = config
        self._view.set_network_mode(mode)
        self._view.set_wifi_available(False)
        try:
            if mode == "ETH":
                if self._lan is None:
                    self._lan = create_lan()
                if config["protocol"] == "STATIC":
                    self._lan.ifconfig(
                        tuple(config[key] for key in ("ip", "netmask", "gateway", "dns"))
                    )
                    self._eth_static = True
                elif self._eth_static:
                    self._lan.ifconfig("dhcp")
                    self._eth_static = False
                self._lan.active(True)
                if self._lan.set_default_netif() != 0:
                    raise OSError("Unable to select Ethernet route")
            else:
                if self._wlan is None:
                    if self._wifi_attempted:
                        raise RuntimeError("Wi-Fi module unavailable; restart to retry")
                    self._wifi_attempted = True
                    self._wlan = startup.Startup()
                else:
                    self._wlan.network.active(True)
                if not self._wlan.network.set_default():
                    raise OSError("Unable to select Wi-Fi route")
                self._view.set_wifi_available(True)
                if self._saved_ssid:
                    self._queue_connection(self._saved_ssid, self._saved_password, False, config)
        except (OSError, RuntimeError, ValueError) as error:
            if mode == "WIFI":
                self._module_unavailable(error)
            else:
                self._eth_error = "Ethernet unavailable. Tap Reconnect to retry"
                print("[Ethernet]: initialization failed:", error)
            return
        if save:
            try:
                self._nvs.set_str("net_mode", mode)
                self._nvs.set_str("protocol", config["protocol"])
                self._nvs.commit()
            except OSError as error:
                print("[NET]: mode save failed:", error)
                self._mode_save_error = "Could not save network mode"

    def _queue_connection(self, ssid, password, save, config):
        if self._wlan is None:
            return
        if self._pending_connect is not None or self._connection is not None:
            return
        if not ssid or len(ssid.encode()) > 32:
            self._view.set_network_result("SSID must be 1-32 bytes", DANGER)
            return
        if len(password.encode()) > 63:
            self._view.set_network_result("Password must be at most 63 bytes", DANGER)
            return
        # The LVGL callback only queues work; network/NVS calls run in _main.
        self._pending_connect = ssid, password, save, config
        self._view.set_network_result("Connecting...", ACCENT, True)

    def _start_connection(self, now):
        ssid, password, save, config = self._pending_connect
        self._pending_connect = None
        self._wifi_error = False
        try:
            self._wlan.network.disconnect()
            if config["protocol"] != "STATIC":
                self._wlan.network.ipconfig(dhcp4=True)
            self._wlan.connect_network(ssid, password, **config)
            self._connection = ssid, password, save, time.ticks_add(now, self._timeout_ms)
            print("Connecting to " + ssid)
        except (OSError, RuntimeError) as error:
            print("[Wi-Fi]: connection start failed:", error)
            self._fail_connection("Unable to start Wi-Fi")

    def _fail_connection(self, message):
        self._connection = None
        self._wifi_error = True
        try:
            self._wlan.network.disconnect()
        except (OSError, RuntimeError):
            pass
        self._view.set_network_result(message, DANGER)

    def _poll_connection(self, now):
        if self._connection is None:
            return
        try:
            status = self._wlan.connect_status()
        except (OSError, RuntimeError) as error:
            self._module_unavailable(error)
            return
        ssid, password, save, deadline = self._connection
        if status == network.STAT_GOT_IP:
            self._connection = None
            self._wifi_error = False
            if save:
                try:
                    self._nvs.set_str("ssid0", ssid)
                    self._nvs.set_str("pswd0", password)
                    self._nvs.set_str("net_mode", "WIFI")
                    self._nvs.set_str("protocol", "DHCP")
                    self._nvs.commit()
                except OSError as error:
                    print("[Wi-Fi]: configuration save failed:", error)
                    self._view.set_network_result("Connected; could not save settings", DANGER)
                    return
                self._configured = True
                self._saved_ssid, self._saved_password = ssid, password
                self._view.set_saved_network(ssid, password)
            self._view.set_network_result("Connected", CHARGING)
        elif status in _WIFI_ERRORS:
            self._fail_connection(_WIFI_ERRORS[status])
        elif time.ticks_diff(now, deadline) >= 0:
            self._fail_connection("Connection timed out")

    @staticmethod
    def _cloud_state():
        if M5Things is not None:
            try:
                return M5Things.status()
            except (OSError, RuntimeError):
                pass
        return 0

    @staticmethod
    def _identity(cloud_status):
        if M5Things is not None and cloud_status == 2:
            try:
                return M5Things.accesscode() or "", M5Things.nick_name() or ""
            except (OSError, RuntimeError):
                pass
        return "", ""

    @staticmethod
    def _power_state():
        try:
            battery = M5.Power.getBatteryLevel()
            battery = battery if 0 <= battery <= 100 else None
            # M5Unified returns 2 for unknown, which must not appear green.
            charging = M5.Power.isCharging() == 1
            return battery, charging
        except (OSError, RuntimeError):
            return None, False

    @staticmethod
    def _clock():
        value = time.localtime()
        return "%02d:%02d" % (value[3], value[4]) if value[0] >= 2024 else "--:--"

    def _refresh_state(self):
        status = None
        ip = ""
        if self._net_mode == "ETH":
            wifi = "unavailable" if self._eth_error else "disconnected"
            if self._lan is not None and not self._eth_error:
                try:
                    status = self._lan.status()
                    if self._lan.isconnected():
                        ip = self._lan.ifconfig()[0]
                        wifi = "connected" if ip != "0.0.0.0" else "connecting"
                    elif status == network.ETH_CONNECTED:
                        wifi = "connecting"
                except (OSError, RuntimeError) as error:
                    print("[Ethernet]: status failed:", error)
                    wifi = "unavailable"
            message = self._eth_error or (
                "Connect a network cable" if wifi == "disconnected" else ""
            )
        elif self._wlan is not None:
            try:
                status = self._wlan.connect_status()
                ip = self._wlan.local_ip() if status == network.STAT_GOT_IP else ""
            except (OSError, RuntimeError) as error:
                self._module_unavailable(error)
        if self._net_mode == "WIFI":
            if self._wlan is None:
                wifi = "unavailable"
            elif status == network.STAT_GOT_IP:
                wifi = "connected"
            elif self._pending_connect is not None or self._connection is not None:
                wifi = "connecting"
            elif self._wifi_error or status in _WIFI_ERRORS:
                wifi = "disconnected"
            elif status == network.STAT_CONNECTING:
                wifi = "connecting"
            else:
                wifi = "disconnected" if self._configured else "unconfigured"
            message = _MODULE_MESSAGE if self._wlan is None else ""
        self._view.set_connection_info(
            wifi, ip if wifi == "connected" else "", self._mode_save_error or message
        )
        cloud_status = self._cloud_state() if wifi == "connected" else 0
        if wifi != "connected":
            service = "offline"
        elif cloud_status == 2:
            service = "online"
        else:
            service = "offline"
        access_code, nickname = self._identity(cloud_status if wifi == "connected" else 0)
        self._view.set_identity(access_code, nickname)
        startup.print_access_info(nickname, access_code)
        battery, charging = self._power_state()
        rssi = None
        if wifi == "connected" and self._net_mode == "WIFI":
            try:
                rssi = self._wlan.get_rssi()
            except (OSError, RuntimeError):
                pass
        self._view.set_status(wifi, service, battery, charging, self._clock(), rssi)
        log_state = self._net_mode, status, cloud_status
        if log_state != self._last_log_state:
            self._last_log_state = log_state
            if self._net_mode == "ETH":
                print("[NET]: Ethernet %s | [MQTT]: %s" % (wifi, cloud_status))
                return
            if self._wlan is None:
                print("[NET]: MODULE_UNAVAILABLE | [MQTT]: STANDBY")
                return
            print(
                "[NET]: %s | [MQTT]: %s"
                % (
                    self._wlan.wifi_status_str(status),
                    self._wlan.m5things_status_str(cloud_status),
                )
            )

    def _step(self, now):
        M5.update()
        self._apply_brightness(now)
        self._apply_timezone()
        if self._pending_mode is not None and not self._scanning:
            mode, self._pending_mode = self._pending_mode, None
            config = self._active_config if mode == self._net_mode else {"protocol": "DHCP"}
            self._activate_mode(mode, config, save=True)
        if self._pending_connect is not None:
            self._start_connection(now)
        self._poll_connection(now)
        self._poll_scan()
        # ESP-Hosted status/RSSI calls and power I/O are synchronous. The
        # password page has no live telemetry; refresh as soon as editing ends.
        if self._view.is_password_editing():
            return
        if self._last_refresh is None or time.ticks_diff(now, self._last_refresh) >= 1000:
            self._last_refresh = now
            self._refresh_state()

    def _module_unavailable(self, error):
        # Do not retry partial WLAN initialization in this boot: the native
        # driver may already own netifs. A reboot provides a clean retry.
        print("[Wi-Fi]: module unavailable:", error)
        self._wlan = None
        self._pending_connect = None
        self._connection = None
        self._scan_requested = False
        self._scanning = False
        self._view.set_wifi_available(False)
        self._view.set_network_result(_MODULE_MESSAGE, DANGER)
        self._view.set_scan_state(_MODULE_MESSAGE, error=True)

    async def _main(self, ssid, password, config):
        # Let m5ui draw the launcher before the blocking ESP-Hosted handshake.
        await asyncio.sleep_ms(100)
        self._activate_mode(self._net_mode, config)
        self._refresh_state()
        while True:
            self._step(time.ticks_ms())
            await asyncio.sleep_ms(100)

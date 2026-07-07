# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# PaperColor startup script
from startup import Startup, print_access_info
from M5 import Widgets
import M5
import time
import esp32
import network
import asyncio
import machine
import binascii

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

STARTUP_BG_IMG = "/system/papercolor/background.png"
WIFI_STATUS_OK_IMG = "/system/papercolor/wifi_ok.png"
WIFI_STATUS_ERROR_IMG = "/system/papercolor/wifi_error.png"
CLOUD_STATUS_OK_IMG = "/system/papercolor/cloud_ok.png"
CLOUD_STATUS_ERROR_IMG = "/system/papercolor/cloud_error.png"


class AppBase:
    def __init__(self) -> None:
        self._task = None

    def on_install(self):
        pass

    def on_launch(self):
        pass

    def on_view(self):
        pass

    def on_ready(self):
        self._task = asyncio.create_task(self.on_run())

    async def on_run(self):
        while True:
            await asyncio.sleep_ms(500)

    def on_hide(self):
        if self._task is not None:
            self._task.cancel()
            self._task = None

    def on_exit(self):
        pass

    def on_uninstall(self):
        pass

    def install(self):
        self.on_install()

    def start(self):
        self.on_launch()
        self.on_view()
        self.on_ready()

    def stop(self):
        self.on_hide()
        self.on_exit()


class Framework:
    def __init__(self, app: AppBase) -> None:
        self._app = app

    def start(self):
        asyncio.run(self.run())

    async def run(self):
        self._app.start()
        while True:
            M5.update()
            await asyncio.sleep_ms(100)


class PaperColorCloudApp(AppBase):
    WEB_IDE = "uiflow2.m5stack.com"
    POLL_INTERVAL_MS = 500
    REFRESH_GRACE_MS = 10000

    def __init__(self, data) -> None:
        super().__init__()
        self._wifi = data[0]
        self._ssid = str(data[1] or "")
        self._timeout = data[2]
        self._last_screen_key = None
        self._had_access_code = False
        self._logged_wifi_connected = False
        self._logged_ip = None
        self._logged_access_code = None
        self._wait_stage = None

    def on_launch(self):
        M5.Lcd.setRotation(1)
        M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_FASTEST)

    def _format_mac(self) -> str:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        return ":".join(mac[i : i + 2] for i in range(0, len(mac), 2))

    def _new_sprite(self):
        sprite = M5.Lcd.newCanvas(600, 400, 24, True)
        sprite.drawPng(STARTUP_BG_IMG, 0, 0)
        sprite.setFont(Widgets.FONTS.Montserrat18)
        sprite.setTextColor(0xFFFFFF, 0x000000)
        sprite.drawString(esp32.firmware_info()[3], 160, 90)
        sprite.setTextColor(0x000000, 0xFFFFFF)
        sprite.drawString("Device MAC:", 30, 160)
        sprite.drawString("Access Code:", 30, 240)
        sprite.drawString("Nickname:", 30, 320)
        sprite.drawString("WI-FI SSID:", 330, 160)
        sprite.drawString("IP Address:", 330, 240)
        sprite.drawString("Web IDE:", 330, 320)
        return sprite

    def _collect_state(self):
        wifi_status = self._wifi.connect_status()
        wifi_ok = wifi_status == network.STAT_GOT_IP
        ip_addr = self._wifi.local_ip() if wifi_ok else ""
        cloud_status = 0
        access_code = ""
        nick_name = ""

        if wifi_ok and _HAS_SERVER:
            cloud_status = M5Things.status()
            if cloud_status == 2:
                access_code = M5Things.accesscode()
                nick_name = M5Things.nick_name()

        cloud_ok = wifi_ok and _HAS_SERVER and cloud_status == 2 and access_code != ""
        return {
            "wifi_ok": wifi_ok,
            "cloud_ok": cloud_ok,
            "access_code": access_code,
            "nick_name": nick_name,
            "ip_addr": ip_addr,
        }

    def _screen_payload(self, state, access_text: str, nick_name: str = None):
        return (
            state["wifi_ok"],
            state["cloud_ok"],
            access_text,
            nick_name if nick_name is not None else (state["nick_name"] or "-"),
            self._ssid or "-",
            state["ip_addr"] if state["wifi_ok"] else "-",
        )

    def _log_state_events(self, state) -> None:
        if state["wifi_ok"] and not self._logged_wifi_connected:
            print(f"Wi-Fi connected: {self._ssid}")
            self._logged_wifi_connected = True

        if state["ip_addr"] and state["ip_addr"] != self._logged_ip:
            print(f"IP address: {state['ip_addr']}")
            self._logged_ip = state["ip_addr"]

        if state["access_code"] and state["access_code"] != self._logged_access_code:
            self._logged_access_code = state["access_code"]

        print_access_info(state.get("nick_name", ""), state.get("access_code", ""))

    def _log_wait_stage(self, state) -> None:
        if not state["wifi_ok"]:
            stage = "wifi"
            message = f"Waiting for Wi-Fi connection: {self._ssid}"
        elif not _HAS_SERVER:
            stage = "server-unavailable"
            message = "Waiting for server skipped: M5Things unavailable"
        elif not state["cloud_ok"] and not state["access_code"]:
            cloud_status = M5Things.status()
            if cloud_status != 2:
                stage = "server"
                message = "Waiting for server connection"
            else:
                stage = "access-code"
                message = "Waiting for access code"
        else:
            stage = None
            message = None

        if stage != self._wait_stage:
            self._wait_stage = stage
            if message:
                print(message)

    def _log_refresh_reason(self, old_payload, new_payload, reason: str) -> None:
        if old_payload is None:
            print(f"Screen refresh: {reason} (initial)")
            return

        names = (
            "wifi_ok",
            "cloud_ok",
            "access_text",
            "nick_name",
            "ssid",
            "ip_addr",
        )
        changes = []
        for index, name in enumerate(names):
            if old_payload[index] != new_payload[index]:
                changes.append(f"{name}: {old_payload[index]} -> {new_payload[index]}")

        if changes:
            print(f"Screen refresh: {reason} | " + "; ".join(changes))
        else:
            print(f"Screen refresh: {reason}")

    def _push_screen(self, payload) -> None:
        wifi_ok, cloud_ok, access_text, nick_name, ssid_text, ip_text = payload
        sprite = self._new_sprite()
        sprite.drawPng(WIFI_STATUS_OK_IMG if wifi_ok else WIFI_STATUS_ERROR_IMG, 360, 20)
        sprite.drawPng(CLOUD_STATUS_OK_IMG if cloud_ok else CLOUD_STATUS_ERROR_IMG, 450, 20)

        sprite.setFont(Widgets.FONTS.Montserrat18)
        sprite.setTextColor(0x0000FF, 0xFFFFFF)
        sprite.drawString(self._format_mac(), 30, 190)
        sprite.drawString(nick_name, 30, 350)
        sprite.drawString(ssid_text, 330, 190)
        sprite.drawString(ip_text, 330, 270)
        sprite.drawString(self.WEB_IDE, 330, 350)

        sprite.setFont(Widgets.FONTS.Montserrat24)
        sprite.setTextColor(0x00AA00 if cloud_ok else 0xCC0000, 0xFFFFFF)
        sprite.drawString(access_text, 30, 270)
        sprite.push(0, 0)

    def _render_if_changed(self, payload, reason: str = "state changed") -> None:
        if payload != self._last_screen_key:
            self._log_refresh_reason(self._last_screen_key, payload, reason)
            self._push_screen(payload)
            self._last_screen_key = payload

    async def _wait_result(self):
        start = time.ticks_ms()
        state = self._collect_state()

        while time.ticks_diff(time.ticks_ms(), start) < self._timeout * 1000:
            state = self._collect_state()
            self._log_state_events(state)
            self._log_wait_stage(state)
            if state["cloud_ok"]:
                self._had_access_code = True
                return state, False
            await asyncio.sleep_ms(self.POLL_INTERVAL_MS)

        return state, True

    async def on_run(self):
        state, timed_out = await self._wait_result()
        access_text = state["access_code"] if not timed_out and state["cloud_ok"] else "TIMEOUT"
        if state["cloud_ok"]:
            self._had_access_code = True
        self._render_if_changed(self._screen_payload(state, access_text), "startup result")

        wifi_bad_since = None
        cloud_bad_since = None
        while True:
            now = time.ticks_ms()
            state = self._collect_state()
            self._log_state_events(state)

            if state["wifi_ok"]:
                wifi_bad_since = None
            elif wifi_bad_since is None:
                wifi_bad_since = now

            if state["cloud_ok"]:
                cloud_bad_since = None
                self._had_access_code = True
                self._render_if_changed(
                    self._screen_payload(state, state["access_code"]), "cloud recovered"
                )
            else:
                if cloud_bad_since is None:
                    cloud_bad_since = now

                offline_text = "OFFLINE" if self._had_access_code else "TIMEOUT"
                if (
                    wifi_bad_since is not None
                    and time.ticks_diff(now, wifi_bad_since) >= self.REFRESH_GRACE_MS
                ):
                    self._render_if_changed(
                        self._screen_payload(state, offline_text), "wifi offline grace reached"
                    )
                elif (
                    cloud_bad_since is not None
                    and time.ticks_diff(now, cloud_bad_since) >= self.REFRESH_GRACE_MS
                ):
                    self._render_if_changed(
                        self._screen_payload(state, offline_text), "cloud offline grace reached"
                    )

            await asyncio.sleep_ms(self.POLL_INTERVAL_MS)


class PaperColor_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def _show_no_wifi_config(self) -> None:
        M5.Lcd.setRotation(1)
        M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_FASTEST)

        cloud_app = PaperColorCloudApp((self._wifi, "", 0))
        state = {
            "wifi_ok": False,
            "cloud_ok": False,
            "access_code": "",
            "nick_name": "-",
            "ip_addr": "",
        }
        cloud_app._render_if_changed(
            cloud_app._screen_payload(state, "NO WIFI", nick_name="NOT CONFIGURED"),
            "wifi not configured",
        )
        print("Wi-Fi not configured")

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
    ) -> None:
        if not ssid:
            self._show_no_wifi_config()
            return

        self._wifi.connect_network(
            ssid, pswd, protocol=protocol, ip=ip, netmask=netmask, gateway=gateway, dns=dns
        )
        print(f"Try to connect {ssid}...")
        M5.Speaker.setVolume(100)
        M5.Speaker.tone(4000, 50)

        cloud_app = PaperColorCloudApp((self._wifi, ssid, timeout))
        fw = Framework(cloud_app)
        fw.start()

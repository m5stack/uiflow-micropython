# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from startup import Startup, print_access_info
import M5
import asyncio
import machine
import widgets

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


class PaperDIYCloudApp:
    POLL_INTERVAL_MS = 1500

    def __init__(self) -> None:
        self._labels = ()
        self._state_text = ""
        self._access_code_text = ""
        self._nick_name_text = ""
        self._last_printed = None

    @staticmethod
    def _get_state() -> str:
        if _HAS_SERVER:
            try:
                if M5Things.status() == 2:
                    return "ONLINE"
            except Exception:
                pass
        return "OFFLINE"

    @staticmethod
    def _get_access_code() -> str:
        if _HAS_SERVER:
            try:
                if M5Things.status() == 2:
                    return M5Things.accesscode() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_nick_name() -> str:
        if _HAS_SERVER:
            try:
                if M5Things.status() == 2:
                    return M5Things.nick_name() or ""
            except Exception:
                pass
        return ""

    @staticmethod
    def _get_mac() -> str:
        return ":".join(f"{byte:02X}" for byte in machine.unique_id())

    def show(self) -> None:
        self._state_text = self._get_state()
        self._access_code_text = self._get_access_code()
        self._nick_name_text = self._get_nick_name()

        M5.Lcd.drawImage("/system/paperdiy/flow.png", 0, 0)

        # Keep the PaperS3 layout while identifying the target board correctly.
        M5.Lcd.fillRect(360, 920, 180, 40, 0xFFFFFF)
        M5.Lcd.setTextColor(0x000000, 0xFFFFFF)
        M5.Lcd.setFont(M5.Lcd.FONTS.Montserrat18)
        footer = "M5PAPERDIY"
        M5.Lcd.drawString(footer, 531 - M5.Lcd.textWidth(footer), 928)

        state_label = widgets.Label(
            self._state_text,
            89,
            452,
            w=360,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.Montserrat40,
            parent=M5.Lcd,
        )
        mac_label = widgets.Label(
            self._get_mac(),
            89,
            572,
            w=360,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.Montserrat40,
            parent=M5.Lcd,
        )
        access_code_label = widgets.Label(
            self._access_code_text,
            89,
            692,
            w=360,
            h=50,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.Montserrat40,
            parent=M5.Lcd,
        )
        access_code_label.set_long_mode(access_code_label.LONG_DOT)
        nick_name_label = widgets.Label(
            self._nick_name_text,
            89,
            812,
            w=360,
            h=50,
            fg_color=0x000000,
            bg_color=0xE3E3E3,
            font=M5.Lcd.FONTS.Montserrat40,
            parent=M5.Lcd,
        )
        nick_name_label.set_long_mode(nick_name_label.LONG_DOT)

        # Label construction only stores text; draw each initial value explicitly.
        state_label.set_text()
        mac_label.set_text()
        access_code_label.set_text()
        nick_name_label.set_text()

        self._labels = (
            state_label,
            mac_label,
            access_code_label,
            nick_name_label,
        )

    def _print_access_info(self) -> None:
        credentials = (self._nick_name_text, self._access_code_text)
        if all(credentials) and credentials != self._last_printed:
            print_access_info(*credentials)
            self._last_printed = credentials

    async def run(self) -> None:
        state_label, _, access_code_label, nick_name_label = self._labels

        while True:
            M5.update()

            state = self._get_state()
            if state != self._state_text:
                self._state_text = state
                state_label.set_text(state)

            access_code = self._get_access_code()
            if access_code != self._access_code_text:
                self._access_code_text = access_code
                access_code_label.set_text(access_code)

            nick_name = self._get_nick_name()
            if nick_name != self._nick_name_text:
                self._nick_name_text = nick_name
                nick_name_label.set_text(nick_name)

            self._print_access_info()
            await asyncio.sleep_ms(self.POLL_INTERVAL_MS)


class PaperDIY_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    @staticmethod
    def _configure_display() -> None:
        M5.Lcd.setRotation(0)
        M5.Lcd.setEpdMode(M5.Lcd.EPDMode.EPD_FASTEST)

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
        self._configure_display()
        app = PaperDIYCloudApp()
        app.show()

        if ssid:
            self._wifi.connect_network(
                ssid,
                pswd,
                protocol=protocol,
                ip=ip,
                netmask=netmask,
                gateway=gateway,
                dns=dns,
            )
            print(f"Try to connect {ssid}...")
        else:
            print("Wi-Fi not configured")

        asyncio.run(app.run())

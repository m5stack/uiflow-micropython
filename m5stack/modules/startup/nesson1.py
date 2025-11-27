# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from . import Startup
import M5
import network
import widgets
import os
import sys
import gc
import asyncio
import esp32
import machine
import binascii
from microdot import Microdot
from microdot import send_file
from microdot import Response

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

DEBUG = False

CHARGE_ICON = "/system/nesso-n1/CHG.jpg"
NO_CHARGE_ICON = "/system/nesso-n1/noCHG.jpg"
CLOUD_ICON = "/system/nesso-n1/1a.jpg"
USB_ICON = "/system/nesso-n1/1b.jpg"
APPLIST_ICON = "/system/nesso-n1/1c.jpg"
LORACHAT_ICON = "/system/nesso-n1/1d.jpg"
SETUP_ICON = "/system/nesso-n1/1e.jpg"
USB_IMG = "/system/nesso-n1/usb.jpg"
APPLIST_IMG = "/system/nesso-n1/APPLIST.jpg"
CLOUD_IMG = "/system/nesso-n1/a11.jpg"
NG_IMG = "/system/nesso-n1/ng.jpg"
WIFI_OK_IMG = "/system/nesso-n1/wifi_ok.jpg"
SERVER_OK_IMG = "/system/nesso-n1/server_ok.jpg"
PLACEHOLDER_IMG = "/system/nesso-n1/placeholder.jpg"
STATE_WIFI_NO_SET_IMG = "/system/nesso-n1/wifiNeverSet.jpg"
STATE_WIFI_NG_IMG = "/system/nesso-n1/wifiNG.jpg"
STATE_WIFI_OK_IMG = "/system/nesso-n1/wifiOKServerNG.jpg"
STATE_SERVER_OK_IMG = "/system/nesso-n1/wifiOKServerOK.jpg"
SETUP_AP_IMG = "/system/nesso-n1/a1.jpg"
SETUP_WEB_IMG = "/system/nesso-n1/a2.jpg"
SETUP_WIFI_IMG = "/system/nesso-n1/a3.jpg"
SETUP_WIFI_NG_IMG = "/system/nesso-n1/a4.jpg"
SETUP_WIFI_OK_IMG = "/system/nesso-n1/a7.jpg"
SETUP_SERVER_NG_IMG = "/system/nesso-n1/a9.jpg"
SETUP_SERVER_OK_IMG = "/system/nesso-n1/a11.jpg"


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
        self._task.cancel()

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

    def pause(self):
        self.on_hide()

    def resume(self):
        self.on_ready()

    def stop(self):
        self.on_hide()
        self.on_exit()

    def uninstall(self):
        self.on_uninstall()


class AppSelector:
    def __init__(self, apps: list) -> None:
        self._apps = apps
        self._id = 0

    def prev(self):
        self._id = (self._id - 1) % len(self._apps)
        return self._apps[self._id]

    def next(self):
        self._id = (self._id + 1) % len(self._apps)
        return self._apps[self._id]

    def current(self):
        return self._apps[self._id]

    def select(self, app):
        self._id = self._apps.index(app)

    def index(self, id):
        self._id = id % len(self._apps)
        return self._apps[self._id]


class UsbApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        self._battery_label = widgets.Label(
            str(None),
            135 - 14,
            6,
            w=135,
            h=20,
            font_align=widgets.Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu12,
        )

        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)

    def on_view(self):
        self._bg_img.set_src(USB_IMG)

    async def on_run(self):
        while True:
            # battery
            self._battery_label.set_text(str(M5.Power.getBatteryLevel()))
            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._battery_label

    async def _keycode_enter_event_handler(self, fw: "Framework") -> None:
        DEBUG and print("_keycode_enter_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_dpad_down_event_handler(self, fw: "Framework") -> None:
        DEBUG and print("_keycode_dpad_down_event_handler")


class RunApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_ready(self):
        M5.Lcd.clear()
        execfile("main.py", {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt


class ListApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        self._battery_label = widgets.Label(
            str(None),
            135 - 14,
            6,
            w=135,
            h=20,
            font_align=widgets.Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFFFFFF,
            font=M5.Lcd.FONTS.DejaVu12,
        )
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)

        self._labels = []
        self._label0 = None
        self._label1 = None
        self._label2 = None
        self._lebals = []
        self._lebal0 = None
        self._lebal1 = None
        self._lebal2 = None

        self._files = []
        for file in os.listdir("apps"):
            if file.endswith(".py"):
                self._files.append(file)
        self._files_number = len(self._files)
        self._cursor_pos = 0
        self._file_pos = 0

    def on_view(self):
        self._bg_img.set_src(APPLIST_IMG)
        if self._label0 is None:
            self._label0 = widgets.Label(
                "",
                25,
                108,
                w=85,
                h=22,
                fg_color=0xFFFFFF,
                bg_color=0x333333,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label0.set_long_mode(widgets.Label.LONG_DOT)
        if self._label1 is None:
            self._label1 = widgets.Label(
                "",
                25,
                108 + 22 + 5,
                w=85,
                h=22,
                fg_color=0x999999,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label1.set_long_mode(widgets.Label.LONG_DOT)
        if self._label2 is None:
            self._label2 = widgets.Label(
                "",
                25,
                108 + 22 + 5 + 22 + 5,
                w=85,
                h=22,
                fg_color=0x4D4D4D,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._label2.set_long_mode(widgets.Label.LONG_DOT)

        if len(self._labels) != 3:
            self._labels.clear()
            self._labels.append(self._label0)
            self._labels.append(self._label1)
            self._labels.append(self._label2)

        if self._lebal0 is None:
            self._lebal0 = widgets.Label(
                "",
                25,
                108 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x999999,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal0.set_long_mode(widgets.Label.LONG_DOT)

        if self._lebal1 is None:
            self._lebal1 = widgets.Label(
                "",
                25,
                108 - 22 - 5 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x4D4D4D,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal1.set_long_mode(widgets.Label.LONG_DOT)

        if self._lebal2 is None:
            self._lebal2 = widgets.Label(
                "",
                25,
                108 - 22 - 5 - 22 - 5 - 22 - 5,
                w=85,
                h=22,
                fg_color=0x333333,
                bg_color=0x000000,
                font=M5.Lcd.FONTS.DejaVu18,
            )
            self._lebal2.set_long_mode(widgets.Label.LONG_DOT)

        if len(self._lebals) != 3:
            self._lebals.clear()
            self._lebals.append(self._lebal0)
            self._lebals.append(self._lebal1)
            self._lebals.append(self._lebal2)

        for label, file in zip(self._labels, self._files):
            # print("file:", file)
            file and label and label.set_text(file)

    async def on_run(self):
        while True:
            # battery
            self._battery_label.set_text(str(M5.Power.getBatteryLevel()))
            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._battery_label, self._labels, self._files, self._lebals

    async def _keycode_enter_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_enter_event_handler")
        M5.Lcd.clear()
        execfile("/".join(["apps/", self._files[self._file_pos]]), {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_dpad_down_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_dpad_down_event_handler")
        self._file_pos += 1

        if self._file_pos >= len(self._files):
            self._file_pos = 0

        for label in self._labels:
            label.set_text("")

        for label, file in zip(self._labels, self._files[self._file_pos :]):
            file and label and label.set_text(file)

        for label in self._lebals:
            label.set_text("")

        files = self._files[: self._file_pos]
        files.reverse()

        for label, file in zip(self._lebals, files):
            file and label and label.set_text(file)


class LoRaChatApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_view(self):
        M5.Lcd.clear(0x000000)
        M5.Lcd.drawImage(PLACEHOLDER_IMG, 0, 0, 135, 240)

    async def _keycode_enter_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_enter_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_dpad_down_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_dpad_down_event_handler")


class DNSServer:
    """DNS Server implementation for captive portal"""

    DNS_PORT = 53
    DNS_QR_FLAG = 1 << 15
    DNS_QTYPE_A = 0x0001
    DNS_QCLASS_IN = 0x0001
    DNS_ANSWER_TTL = 300

    def __init__(self, ip_address="192.168.4.1"):
        """Initialize DNS server

        Args:
            ip_address: IP address to respond with for all queries
        """
        self._ip = ip_address
        self._socket = None
        self._running = False
        self._buffer = bytearray(512)

    def start(self):
        """Start DNS server on port 53"""
        if self._running:
            return

        try:
            import socket

            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._socket.bind(("0.0.0.0", self.DNS_PORT))
            self._socket.setblocking(False)
            self._running = True
            DEBUG and print(
                f"DNS Server started on port {self.DNS_PORT}, responding with {self._ip}"
            )
        except Exception as e:
            print(f"DNS Server start failed: {e}")
            self._socket = None

    def stop(self):
        """Stop DNS server"""
        if self._socket:
            try:
                self._socket.close()
            except:
                pass
            self._socket = None
        self._running = False
        DEBUG and print("DNS Server stopped")

    def process_next_request(self):
        """Process one DNS request if available"""
        if not self._running or not self._socket:
            return

        try:
            # Try to receive data (non-blocking)
            data, addr = self._socket.recvfrom(512)
            if len(data) < 12:  # Minimum DNS header size
                return

            # Parse DNS header
            transaction_id = data[0:2]  # noqa: F841
            flags = (data[2] << 8) | data[3]
            qd_count = (data[4] << 8) | data[5]

            # Check if it's a standard query
            if (flags & self.DNS_QR_FLAG) or qd_count != 1:
                return

            # Parse domain name (skip it, we redirect everything)
            pos = 12
            domain_parts = []
            while pos < len(data) and data[pos] != 0:
                label_len = data[pos]
                if label_len > 63 or pos + label_len + 1 > len(data):
                    return
                domain_parts.append(data[pos + 1 : pos + 1 + label_len].decode("utf-8", "ignore"))
                pos += label_len + 1

            domain_name = ".".join(domain_parts)

            if pos >= len(data):
                return
            pos += 1  # Skip null terminator

            # Check question type and class
            if pos + 4 > len(data):
                return
            qtype = (data[pos] << 8) | data[pos + 1]
            qclass = (data[pos + 2] << 8) | data[pos + 3]

            # Only handle A record queries
            if qtype != self.DNS_QTYPE_A or qclass != self.DNS_QCLASS_IN:
                return

            # Build response
            response = bytearray(data[: pos + 4])  # Copy query

            # Set response flags: QR=1, AA=1 (authoritative answer)
            response[2] = 0x81
            response[3] = 0x80

            # Set answer count to 1
            response[6] = 0x00
            response[7] = 0x01

            # Add answer section
            # Name pointer (points to name in question)
            response.extend(b"\xc0\x0c")  # Pointer to offset 12

            # Type A
            response.extend(b"\x00\x01")

            # Class IN
            response.extend(b"\x00\x01")

            # TTL
            ttl = self.DNS_ANSWER_TTL
            response.extend(
                bytes([(ttl >> 24) & 0xFF, (ttl >> 16) & 0xFF, (ttl >> 8) & 0xFF, ttl & 0xFF])
            )

            # Data length (4 bytes for IPv4)
            response.extend(b"\x00\x04")

            # IP address
            ip_parts = self._ip.split(".")
            response.extend(bytes([int(p) for p in ip_parts]))

            # Send response
            self._socket.sendto(response, addr)
            print(f"DNS: {domain_name} -> {self._ip} (from {addr[0]})")

        except OSError as e:
            # EAGAIN/EWOULDBLOCK is expected for non-blocking socket
            if e.args[0] not in (11, 35, 115):  # EAGAIN, EWOULDBLOCK variations
                print(f"DNS error: {e}")
        except Exception as e:
            print(f"DNS error: {e}")


class SetupApp(AppBase):
    _STATE_AP = 0
    _STATE_WEB = 1
    _STATE_WAIT_WIFI = 2
    _STATE_WIFI_NG = 3
    _STATE_WIFI_OK = 4
    _STATE_SERVER_NG = 5
    _STATE_SERVER_OK = 6

    def __init__(self, data=None) -> None:
        super().__init__()
        self._wifi = data
        self._sta = data.wlan

        self._ap = network.WLAN(network.WLAN.IF_AP)

        self.app = Microdot()
        self.register_routes()
        self._state = self._STATE_AP
        self._clients = set()

        # Initialize DNS server for captive portal
        self._dns_server = DNSServer("192.168.4.1")

    def register_routes(self):
        @self.app.get("/")
        async def handle_index(request):
            self._clients.add(request.client_addr[0])
            response = send_file("/system/nesso-n1/index.html")
            return response

        # Captive portal detection endpoints for various platforms
        @self.app.get("/generate_204")
        async def handle_generate_204(request):
            """Android captive portal detection"""
            self._clients.add(request.client_addr[0])
            return Response.redirect("http://192.168.4.1/")

        @self.app.get("/hotspot-detect.html")
        async def handle_hotspot_detect(request):
            """iOS captive portal detection"""
            self._clients.add(request.client_addr[0])
            return Response.redirect("http://192.168.4.1/")

        @self.app.get("/library/test/success.html")
        async def handle_apple_success(request):
            """iOS alternative detection"""
            self._clients.add(request.client_addr[0])
            return Response.redirect("http://192.168.4.1/")

        @self.app.get("/connecttest.txt")
        async def handle_windows_connect(request):
            """Windows captive portal detection"""
            self._clients.add(request.client_addr[0])
            return Response.redirect("http://192.168.4.1/")

        @self.app.get("/redirect")
        async def handle_windows_redirect(request):
            """Windows redirect page"""
            self._clients.add(request.client_addr[0])
            return Response.redirect("http://192.168.4.1/")

        @self.app.get("/success.txt")
        async def handle_firefox_success(request):
            """Firefox captive portal detection"""
            self._clients.add(request.client_addr[0])
            return Response.redirect("http://192.168.4.1/")

        @self.app.get("/config.json")
        async def handle_config(request):
            """{
                "name": "ESP-AP",
                "mac": "24:0A:C4:12:34:56",
                "aps": [
                    {}
                    ,{"ssid":"Hermione","rssi":-50,"lock":0}
                    ,{"ssid":"Neville","rssi":-65,"lock":1}
                    ,{"ssid":"Gandalf the Grey","rssi":-85,"lock":1}
                    ,{"ssid":"Hagrid","rssi":-95,"lock":0}
                ]
            }
            """
            points = self._sta.scan()

            return {
                "name": self._ap.config("ssid"),
                "mac": binascii.hexlify(machine.unique_id()).upper().decode(),
                "aps": [
                    {
                        "ssid": ssid.decode("utf-8"),
                        "rssi": rssi,
                        "lock": 1 if authmode > 0 else 0,
                    }
                    for ssid, bssid, channel, rssi, authmode, hidden in points
                ],
            }

        @self.app.get("/wifisave")
        async def handler_wifisave(request):
            self.ssid = request.args.get("ssid")
            self.password = request.args.get("psk")
            print("Saving Wi-Fi config:", self.ssid, self.password)
            self._wifisave = True
            self.nvs.set_str("ssid0", self.ssid)
            self.nvs.set_str("pswd0", self.password)
            self.nvs.commit()
            return Response.redirect("/?save")

        # Catch-all route to redirect any unhandled requests to main page
        @self.app.route("/<path:path>")
        async def handle_catchall(request, path):
            """Redirect all other requests to main page"""
            self._clients.add(request.client_addr[0])
            return Response.redirect("http://192.168.4.1/")

    def on_launch(self):
        self.nvs = esp32.NVS("uiflow")
        # self._sta.active(False)
        # self._sta.active(True)
        self.ssid = self.nvs.get_str("ssid0")
        self.password = self.nvs.get_str("pswd0")
        self._wifisave = False
        self._state = self._STATE_AP

        # Disconnect station if connected
        self._sta.disconnect()

        # Setup Access Point
        ap_name = "N1_" + binascii.hexlify(machine.unique_id()).upper().decode()[-4:]
        self._ap.active(True)
        self._ap.config(essid=ap_name, authmode=self._ap.SEC_OPEN)
        self._ap.config(max_clients=2)

        # Start DNS server for captive portal
        self._dns_server.start()

        # Start web server
        self._server = asyncio.create_task(
            self.app.start_server(host="0.0.0.0", port=80, debug=True)
        )

    def on_view(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)
        self._bg_img.set_src(SETUP_AP_IMG)

        self._ap_label = widgets.Label(
            str(self._ap.config("ssid")),
            67,
            130,
            w=103,
            h=29,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xF3F3F3,
            font=M5.Lcd.FONTS.DejaVu24,
        )
        self._ap_label.set_text(self._ap.config("ssid"))
        offset_y = M5.Lcd.fontHeight(M5.Lcd.FONTS.DejaVu24)
        w = M5.Lcd.textWidth(str(self._ap.config("ssid")), M5.Lcd.FONTS.DejaVu24)
        M5.Lcd.fillRect((135 - w) // 2, 130 + offset_y, w, 2, 0x000000)
        self._state = self._STATE_AP

    async def on_run(self):
        while True:
            # Process DNS requests for captive portal
            self._dns_server.process_next_request()

            if self._state == self._STATE_AP:
                if self._ap.status("stations"):
                    self._state = self._STATE_WEB
                    self._bg_img.set_src(SETUP_WEB_IMG)
                    M5.Lcd.drawQR("http://192.168.4.1", 13, 49, 109, 1)

            if self._state == self._STATE_WEB:
                if self._clients:
                    self._state = self._STATE_WAIT_WIFI
                    self._bg_img.set_src(SETUP_WIFI_IMG)

            if self._state == self._STATE_WAIT_WIFI:
                # 等待 /wifisave 请求
                if self._wifisave:
                    self._wifi.connect_network(self.ssid, self.password)
                    self._wifisave = False
                if self._wifi.connect_status() in (network.STAT_IDLE, network.STAT_CONNECTING):
                    pass
                elif self._wifi.connect_status() == network.STAT_GOT_IP:
                    self._state = self._STATE_WIFI_OK
                    self._bg_img.set_src(SETUP_WIFI_OK_IMG)
                else:
                    self._state = self._STATE_WIFI_NG
                    self._bg_img.set_src(SETUP_WIFI_NG_IMG)

            if self._state == self._STATE_WIFI_NG:
                if self._wifi.connect_status() == network.STAT_GOT_IP:
                    self._state = self._STATE_WIFI_OK
                    self._bg_img.set_src(SETUP_WIFI_OK_IMG)

            if self._state == self._STATE_WIFI_OK:
                if _HAS_SERVER:
                    if M5Things.status() < 2:
                        pass
                    if M5Things.status() == 2:
                        if M5Things.paircode() != "":
                            self._state = self._STATE_SERVER_OK
                            self._bg_img.set_src(SETUP_SERVER_OK_IMG)

                            self._net_status_img = widgets.Image(use_sprite=False)
                            self._net_status_img.set_x(98)
                            self._net_status_img.set_y(2)
                            self._net_status_img.set_size(34, 24)
                            self._net_status_img.set_src(WIFI_OK_IMG)

                            self._server_status_img = widgets.Image(use_sprite=False)
                            self._server_status_img.set_x(98)
                            self._server_status_img.set_y(30)
                            self._server_status_img.set_size(34, 24)
                            self._server_status_img.set_src(SERVER_OK_IMG)

                            self._pair_code_label = widgets.Label(
                                M5Things.paircode(),
                                67,
                                185,
                                w=103,
                                h=29,
                                font_align=widgets.Label.CENTER_ALIGNED,
                                fg_color=0x000000,
                                bg_color=0xCBDFE0,
                                font=M5.Lcd.FONTS.DejaVu24,
                            )
                            self._pair_code_label.set_text(M5Things.paircode())
                    elif M5Things.status() > 2:
                        self._state = self._STATE_SERVER_NG
                        self._bg_img.set_src(SETUP_SERVER_NG_IMG)
                else:
                    self._state = self._STATE_SERVER_NG
                    self._bg_img.set_src(SETUP_SERVER_NG_IMG)

            if self._state == self._STATE_SERVER_NG:
                if _HAS_SERVER:
                    self._state = self._STATE_WIFI_OK

            if self._state == self._STATE_SERVER_OK:
                pass

            await asyncio.sleep_ms(100)

            # await self._server

    def on_exit(self):
        # Stop DNS server
        self._dns_server.stop()
        self.app.shutdown()
        # self._ap.disconnect()
        self._ap.active(False)
        if self._wifi.connect_status() == network.STAT_IDLE:
            self._wifi.connect_network(self.nvs.get_str("ssid0"), self.nvs.get_str("pswd0"))
        del self.nvs

    async def _keycode_enter_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_enter_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_dpad_down_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_dpad_down_event_handler")


class CloudApp(AppBase):
    def __init__(self, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._user_id = None
        self._server = None
        self._wifi_status = False
        self._cloud_status = False
        self._pair_code = ""

    def _get_wifi_status(self) -> bool:
        return self._wifi.connect_status() == network.STAT_GOT_IP

    def _get_cloud_status(self) -> bool:
        if self._get_wifi_status() and _HAS_SERVER:
            return M5Things.status() == 2
        else:
            return False

    def on_launch(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)
        self._bg_img.set_src(CLOUD_IMG)

        self._net_status_img = widgets.Image(use_sprite=False)
        self._net_status_img.set_x(98)
        self._net_status_img.set_y(2)
        self._net_status_img.set_size(34, 24)
        self._net_status_img.set_src(NG_IMG)

        self._server_status_img = widgets.Image(use_sprite=False)
        self._server_status_img.set_x(98)
        self._server_status_img.set_y(30)
        self._server_status_img.set_size(34, 24)
        self._server_status_img.set_src(NG_IMG)

        self._pair_code_label = widgets.Label(
            str(""),
            67,
            185,
            w=103,
            h=29,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xCBDFE0,
            font=M5.Lcd.FONTS.DejaVu24,
        )

    def on_view(self):
        self._net_status_img.set_src(WIFI_OK_IMG if self._get_wifi_status() else NG_IMG)
        self._server_status_img.set_src(SERVER_OK_IMG if self._get_cloud_status() else NG_IMG)
        self._pair_code_label.set_text(self._pair_code)

    async def on_run(self):
        while True:
            t = self._get_wifi_status()
            if t is not self._wifi_status:
                self._wifi_status = t
                self._net_status_img.set_src(WIFI_OK_IMG if t else NG_IMG)

            t = self._get_cloud_status()
            if t is not self._cloud_status:
                self._cloud_status = t
                self._server_status_img.set_src(SERVER_OK_IMG if t else NG_IMG)

            if _HAS_SERVER:
                t = M5Things.paircode()
                if t != self._pair_code:
                    self._pair_code = t
                    self._pair_code_label.set_text(t)

            await asyncio.sleep_ms(1000)

    def on_exit(self):
        del self._bg_img, self._net_status_img, self._server_status_img

    async def _keycode_enter_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_enter_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        self.stop()
        fw._app_selector.select(fw._launcher)
        fw._launcher.start()

    async def _keycode_dpad_down_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_dpad_down_event_handler")


def _charge_ico(icos):
    try:
        len(icos)
    except TypeError:
        cache = []
        for i in icos:
            yield i
            cache.append(i)
        icos = cache
    while icos:
        yield from icos


class LauncherApp(AppBase):
    def __init__(self, data=None) -> None:
        self._cloud_app = data
        self._icons = (
            CLOUD_ICON,
            USB_ICON,
            APPLIST_ICON,
            LORACHAT_ICON,
            SETUP_ICON,
        )

    def on_launch(self):
        self._icon_selector = _charge_ico(self._icons)
        self._img_src = next(self._icon_selector)
        self._id = 0
        self._nvs = esp32.NVS("uiflow")

    def on_view(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_x(0)
        self._bg_img.set_y(0)
        self._bg_img.set_size(135, 240)
        self._bg_img.set_src(self._img_src)

        self._chg_img = widgets.Image(use_sprite=False)
        self._chg_img.set_x(59)
        self._chg_img.set_y(3)
        self._chg_img.set_size(16, 22)
        if M5.Power.isCharging():
            self._chg_img.set_src(CHARGE_ICON)
        else:
            self._chg_img.set_src(NO_CHARGE_ICON)

        self._battery_label = widgets.Label(
            str(None),
            132,
            5,
            w=47,
            h=21,
            font_align=widgets.Label.RIGHT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xCCCCCC,
            font=M5.Lcd.FONTS.DejaVu18,
        )

        self._version_label = widgets.Label(
            str(esp32.firmware_info()[3]),
            67,
            152,
            w=135,
            h=22,
            font_align=widgets.Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0x67C94D,
            font=M5.Lcd.FONTS.DejaVu18,
        )
        self._version_label.set_text(esp32.firmware_info()[3])

        self._state_img = widgets.Image(use_sprite=False)
        self._state_img.set_x(6)
        self._state_img.set_y(6)
        self._state_img.set_size(16, 16)
        self._state_img.set_src(self._get_state_img())

    def _get_state_img(self) -> str:
        ssid0 = self._nvs.get_str("ssid0")
        if ssid0 == "":
            return STATE_WIFI_NO_SET_IMG
        if not self._cloud_app._get_wifi_status():
            return STATE_WIFI_NG_IMG
        if not self._cloud_app._get_cloud_status():
            return STATE_WIFI_OK_IMG
        return STATE_SERVER_OK_IMG

    async def on_run(self):
        last_battery = -1
        last_charging = False
        last_state_img = ""
        while True:
            # connection status
            if last_state_img != self._get_state_img():
                last_state_img = self._get_state_img()
                self._state_img.set_src(last_state_img)

            # charging status
            if last_charging != M5.Power.isCharging():
                last_charging = M5.Power.isCharging()
                self._chg_img.set_src(CHARGE_ICON if last_charging else NO_CHARGE_ICON)

            # battery level
            if last_battery != M5.Power.getBatteryLevel():
                last_battery = M5.Power.getBatteryLevel()
                self._battery_label.set_text(str(last_battery) + "%")

            await asyncio.sleep_ms(200)

    def on_exit(self):
        del self._bg_img, self._icon_selector
        del self._nvs

    async def _keycode_enter_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_enter_event_handler")
        self.stop()
        app = fw._app_selector.index(self._id + 1)
        app.start()

    async def _keycode_back_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw: "Framework"):
        DEBUG and print("_keycode_dpad_down_event_handler")
        self._id = self._id + 1 if self._id + 1 < len(self._icons) else 0
        self._img_src = next(self._icon_selector)
        self._bg_img.set_src(self._img_src)
        self._chg_img.set_src(CHARGE_ICON if M5.Power.isCharging() else NO_CHARGE_ICON)
        self._battery_label.set_text(str(M5.Power.getBatteryLevel()) + "%")
        self._version_label.set_text(esp32.firmware_info()[3])
        self._state_img.set_src(self._get_state_img())


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._app_selector = AppSelector(self._apps)
        self._launcher = None

    def install_launcher(self, launcher: AppBase):
        self._launcher = launcher

    def install(self, app: AppBase):
        app.install()
        self._apps.append(app)

    def start(self):
        # asyncio.create_task(self.gc_task())
        asyncio.run(self.run())

    async def unload(self, app: AppBase):
        # app = self._apps.pop()
        app.stop()

    async def load(self, app: AppBase):
        app.start()

    async def reload(self, app: AppBase):
        app.stop()
        app.start()

    async def run(self):
        if self._launcher:
            self._app_selector.select(self._launcher)
            self._launcher.start()

        # asyncio.create_task(self.gc_task())
        while True:
            M5.update()
            if M5.BtnA.wasSingleClicked():
                M5.Speaker.tone(4000, 50)
                app = self._app_selector.current()
                if hasattr(app, "_keycode_enter_event_handler"):
                    await app._keycode_enter_event_handler(self)
            if M5.BtnA.wasDoubleClicked():
                M5.Speaker.tone(3500, 50)
                app = self._app_selector.current()
                if hasattr(app, "_keycode_back_event_handler"):
                    await app._keycode_back_event_handler(self)
            if M5.BtnB.wasSingleClicked():
                M5.Speaker.tone(6000, 50)
                app = self._app_selector.current()
                if hasattr(app, "_keycode_dpad_down_event_handler"):
                    await app._keycode_dpad_down_event_handler(self)

            await asyncio.sleep_ms(100)

    async def gc_task(self):
        while True:
            gc.collect()
            DEBUG and print("heap RAM free:", gc.mem_free())
            DEBUG and print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)


class NessoN1_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wifi.connect_network(ssid, pswd)
        M5.Speaker.setVolume(255)
        M5.Speaker.tone(4000, 50)

        DEBUG and print("Run startup menu")

        cloud_app = CloudApp((self._wifi, ssid))
        usb_app = UsbApp()
        list_app = ListApp()
        lorachat_app = LoRaChatApp()
        setup_app = SetupApp(data=self._wifi)
        launcher = LauncherApp(data=cloud_app)

        fw = Framework()
        fw.install_launcher(launcher)
        fw.install(launcher)
        fw.install(cloud_app)
        fw.install(usb_app)
        fw.install(list_app)
        fw.install(lorachat_app)
        fw.install(setup_app)
        fw.start()

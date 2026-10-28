# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

"""CoreP4X startup view. Hardware work is delegated to its controller."""

import lvgl as lv


BG = 0xF0F2F5
CARD = 0xFFFFFF
INK = 0x20252D
MUTED = 0x6B7482
ACCENT = 0x1769E0
TINT = 0xE6EFFF
LINE = 0xDDE0E8
WARNING = 0x9A5700
DANGER = 0xC83D35
CHARGING = 0x1D9A62
CN = lv.AlibabaPuHuiTi_CN24
TIMEZONE_OFFSETS = (
    -720,
    -660,
    -600,
    -570,
    -540,
    -480,
    -420,
    -360,
    -300,
    -240,
    -210,
    -180,
    -120,
    -60,
    0,
    60,
    120,
    180,
    210,
    240,
    270,
    300,
    330,
    345,
    360,
    390,
    420,
    480,
    525,
    540,
    570,
    600,
    630,
    660,
    720,
    765,
    780,
    840,
)


def timezone_label(offset):
    return "UTC%s%02d:%02d" % ("+" if offset >= 0 else "-", abs(offset) // 60, abs(offset) % 60)


_NETWORK_ICON_POINTS = [
    {"x": 12, "y": 6},
    {"x": 12, "y": 12},
    {"x": 3, "y": 12},
    {"x": 3, "y": 18},
    {"x": 3, "y": 12},
    {"x": 21, "y": 12},
    {"x": 21, "y": 18},
    {"x": 21, "y": 12},
    {"x": 12, "y": 12},
    {"x": 12, "y": 18},
]
_CLOCK_ICON_POINTS = [{"x": 12, "y": 5}, {"x": 12, "y": 12}, {"x": 17, "y": 15}]


def text(
    parent, value, x, y, width, font=lv.font_montserrat_18, color=INK, align=lv.TEXT_ALIGN.LEFT
):
    obj = lv.label(parent)
    obj.set_text(value)
    obj.set_pos(x, y)
    if width is not None:
        obj.set_width(width)
    obj.set_style_text_font(font, 0)
    obj.set_style_text_color(lv.color_hex(color), 0)
    obj.set_style_text_align(align, 0)
    obj.remove_flag(lv.obj.FLAG.CLICKABLE)
    return obj


def surface(parent, x, y, width, height, color=CARD, radius=26):
    obj = lv.obj(parent)
    obj.remove_style_all()
    obj.set_pos(x, y)
    obj.set_size(width, height)
    obj.set_style_bg_color(lv.color_hex(color), 0)
    obj.set_style_bg_opa(255, 0)
    obj.set_style_radius(radius, 0)
    obj.remove_flag(lv.obj.FLAG.SCROLLABLE)
    obj.remove_flag(lv.obj.FLAG.CLICKABLE)
    return obj


def network_icon(parent, color):
    obj = lv.obj(parent)
    obj.remove_style_all()
    obj.set_size(24, 24)
    obj.remove_flag(lv.obj.FLAG.SCROLLABLE)
    obj.remove_flag(lv.obj.FLAG.CLICKABLE)
    lines = lv.line(obj)
    lines.set_points(_NETWORK_ICON_POINTS, len(_NETWORK_ICON_POINTS))
    lines.set_style_line_width(2, 0)
    lines.set_style_line_color(lv.color_hex(color), 0)
    lines.set_style_line_rounded(True, 0)
    lines.remove_flag(lv.obj.FLAG.CLICKABLE)
    surface(obj, 9, 0, 6, 6, color, 1)
    for x in (0, 9, 18):
        surface(obj, x, 18, 6, 6, color, 1)
    return obj


def clock_icon(parent, color):
    obj = surface(parent, 0, 0, 24, 24, TINT, 12)
    obj.set_style_border_width(2, 0)
    obj.set_style_border_color(lv.color_hex(color), 0)
    hand = lv.line(obj)
    hand.set_points(_CLOCK_ICON_POINTS, len(_CLOCK_ICON_POINTS))
    hand.set_style_line_width(2, 0)
    hand.set_style_line_color(lv.color_hex(color), 0)
    hand.set_style_line_rounded(True, 0)
    obj.center()
    return obj


def button(
    parent,
    value,
    x,
    y,
    width,
    height,
    callback=None,
    color=CARD,
    foreground=INK,
    icon=None,
    radius=20,
):
    obj = lv.button(parent)
    obj.remove_style_all()
    obj.set_pos(x, y)
    obj.set_size(width, height)
    obj.set_style_radius(radius, 0)
    obj.set_style_bg_color(lv.color_hex(color), 0)
    obj.set_style_bg_opa(255, 0)
    obj.set_style_bg_color(lv.color_hex(0xDCE9FB if color == CARD else 0x1253B3), lv.STATE.PRESSED)
    obj.set_style_outline_color(lv.color_hex(ACCENT), lv.STATE.FOCUS_KEY)
    obj.set_style_outline_width(2, lv.STATE.FOCUS_KEY)
    obj.set_flex_flow(lv.FLEX_FLOW.ROW)
    obj.set_flex_align(lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
    obj.set_style_pad_column(12, 0)
    if icon:
        if callable(icon):
            icon(obj, foreground)
        else:
            text(obj, icon, 0, 0, None, lv.font_montserrat_24, foreground)
    if value:
        text(obj, value, 0, 0, None, lv.font_montserrat_18, foreground)
    if callback:
        obj.add_event_cb(callback, lv.EVENT.CLICKED, None)
    return obj


class CoreP4XView:
    def __init__(
        self,
        version,
        on_brightness=None,
        on_connect=None,
        on_scan=None,
        on_mode=None,
        on_timezone_load=None,
        on_timezone_save=None,
    ):
        access_code, nickname = "", ""
        self.access_code = access_code
        self.nickname = nickname
        self.version = version
        self.on_brightness = on_brightness
        self.on_connect = on_connect
        self.on_scan = on_scan
        self.on_mode = on_mode
        self.on_timezone_load = on_timezone_load
        self.on_timezone_save = on_timezone_save
        self.network_mode = "WIFI"
        self.saved_ssid = ""
        self.saved_password = ""
        self.selected_ssid = ""
        self.network_busy = False
        self.wifi_available = True
        self.scanning = False
        self.ap_buttons = []
        self.brightness = 70
        self.wifi_state = "unconfigured"
        self.wifi_rssi = None
        self.service_state = "offline"
        self.battery = None
        self.charging = False
        self.clock = "--:--"
        self.current_page = "home"
        self.wifi_return = "home"
        self.active_field = None
        self.make_home()
        self.make_settings()
        self.make_timezone_settings()
        self.make_wifi()
        self.make_networks()
        self.make_connection()
        self.set_status()
        self.show_home()

    def screen(self):
        obj = lv.obj()
        obj.remove_style_all()
        obj.set_size(480, 480)
        obj.set_style_bg_color(lv.color_hex(BG), 0)
        obj.set_style_bg_opa(255, 0)
        obj.remove_flag(lv.obj.FLAG.SCROLLABLE)
        return obj

    def header(self, screen, title, back):
        button(screen, "", 24, 24, 48, 48, back, icon=lv.SYMBOL.LEFT, foreground=ACCENT, radius=16)
        text(screen, title, 88, 33, 360, lv.font_montserrat_24)

    def make_home(self):
        self.home = self.screen()
        self.make_status_bar()
        self.version_label = text(
            self.home,
            "UiFlow2 " + self.version,
            24,
            365,
            432,
            lv.font_montserrat_18,
            MUTED,
            lv.TEXT_ALIGN.LEFT,
        )
        self.version_label.set_long_mode(lv.label.LONG_MODE.DOTS)
        self.wifi_chip = self.status_chip(24)
        self.service_chip = self.status_chip(248)
        access = surface(self.home, 24, 124, 432, 132)
        text(access, "Access Code", 24, 20, 384, color=MUTED, align=lv.TEXT_ALIGN.CENTER)
        self.code_label = text(
            access,
            self.access_code,
            24,
            60,
            384,
            lv.font_montserrat_48,
            ACCENT,
            lv.TEXT_ALIGN.CENTER,
        )
        self.code_label.set_style_text_letter_space(2, 0)
        name_card = surface(self.home, 24, 272, 432, 76)
        text(name_card, "Nickname", 24, 8, 384, lv.font_montserrat_16, MUTED, lv.TEXT_ALIGN.CENTER)
        self.nickname_label = text(
            name_card,
            self.nickname,
            24,
            34,
            384,
            lv.font_montserrat_24,
            INK,
            lv.TEXT_ALIGN.CENTER,
        )
        self.nickname_label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        button(
            self.home,
            "Network",
            24,
            397,
            208,
            56,
            self.show_connection,
            color=ACCENT,
            foreground=CARD,
            icon=network_icon,
        )
        button(
            self.home,
            "Settings",
            248,
            397,
            208,
            56,
            self.show_settings,
            color=ACCENT,
            foreground=CARD,
            icon=lv.SYMBOL.SETTINGS,
        )

    def make_status_bar(self):
        # Standard LVGL / Font Awesome Wi-Fi glyph, with fixed signal states.
        # Keep both the PNG bytes and their descriptors alive for LVGL.
        self.wifi_icons = []
        for name in ("0", "1", "2", "3", "disconnected"):
            with open("/system/corep4x/wifi_" + name + ".png", "rb") as image:
                data = image.read()
            descriptor = lv.image_dsc_t(
                {
                    "header": {
                        "magic": lv.IMAGE_HEADER_MAGIC,
                        "cf": lv.COLOR_FORMAT.RAW_ALPHA,
                        "w": 32,
                        "h": 32,
                    },
                    "data_size": len(data),
                    "data": data,
                }
            )
            self.wifi_icons.append((data, descriptor))
        self.wifi_signal = lv.image(self.home)
        self.wifi_signal.set_pos(24, 6)
        self.ethernet_icon = text(self.home, "ETH", 24, 13, 48, lv.font_montserrat_16, ACCENT)
        self.ethernet_icon.add_flag(lv.obj.FLAG.HIDDEN)
        self.clock_label = text(
            self.home, self.clock, 180, 8, 120, lv.font_montserrat_24, ACCENT, lv.TEXT_ALIGN.CENTER
        )
        self.battery_frame = surface(self.home, 408, 11, 44, 22, BG, 4)
        self.battery_frame.set_style_border_width(2, 0)
        self.battery_tip = surface(self.home, 452, 18, 4, 8, ACCENT, 1)
        self.battery_cells = [
            surface(self.battery_frame, 3 + index * 9, 3, 6, 12, ACCENT, 1) for index in range(4)
        ]

    def status_chip(self, x):
        card = surface(self.home, x, 64, 208, 40, TINT, 14)
        dot = surface(card, 14, 16, 8, 8, ACCENT, 4)
        label = text(card, "", 32, 11, 164, lv.font_montserrat_16)
        return card, dot, label

    def set_status(
        self, wifi=None, service=None, battery=-1, charging=None, clock=None, rssi=None
    ):
        """None battery means unavailable, -1 leaves the previous value unchanged."""
        if wifi is not None:
            self.wifi_state = wifi
        if service is not None:
            self.service_state = service
        if battery != -1:
            self.battery = None if battery is None else max(0, min(100, battery))
        if charging is not None:
            self.charging = charging
        if clock is not None:
            self.clock = clock
        self.wifi_rssi = rssi
        labels = {
            "checking": "Checking",
            "unavailable": "Unavailable",
            "unconfigured": "Setup",
            "disconnected": "Disconnected",
            "connecting": "Connecting",
            "connected": "Connected",
            "online": "Online",
            "offline": "Offline",
        }
        for chip, name, state in (
            (self.wifi_chip, "ETH" if self.network_mode == "ETH" else "Wi-Fi", self.wifi_state),
            (self.service_chip, "Service", self.service_state),
        ):
            color, background = MUTED, CARD
            if state in ("connected", "online"):
                color, background = ACCENT, TINT
            elif state in ("checking", "connecting"):
                color, background = WARNING, 0xFFF0D6
            elif state in ("unavailable", "unconfigured", "disconnected", "offline"):
                color, background = DANGER, 0xFFE9E6
            card, dot, label = chip
            card.set_style_bg_color(lv.color_hex(background), 0)
            dot.set_style_bg_color(lv.color_hex(color), 0)
            label.set_style_text_color(lv.color_hex(color), 0)
            label.set_text(name + " " + labels[state])
        self.clock_label.set_text(self.clock)
        if self.network_mode == "ETH":
            self.wifi_signal.add_flag(lv.obj.FLAG.HIDDEN)
            self.ethernet_icon.remove_flag(lv.obj.FLAG.HIDDEN)
        else:
            self.wifi_signal.remove_flag(lv.obj.FLAG.HIDDEN)
            self.ethernet_icon.add_flag(lv.obj.FLAG.HIDDEN)
        connected = self.wifi_state == "connected"
        strength = 0
        if connected and rssi is not None:
            strength = 3 if rssi >= -55 else (2 if rssi >= -67 else (1 if rssi >= -78 else 0))
        self.signal_strength = strength
        self.wifi_signal.set_src(self.wifi_icons[strength if connected else 4][1])
        level = self.battery
        color = (
            CHARGING
            if self.charging
            else (DANGER if level is not None and level <= 20 else ACCENT)
        )
        if level is None:
            color = MUTED
        self.battery_frame.set_style_border_color(lv.color_hex(color), 0)
        self.battery_tip.set_style_bg_color(lv.color_hex(color), 0)
        self.battery_segments = 0 if level is None else (level + 24) // 25
        for index, cell in enumerate(self.battery_cells):
            cell.set_style_bg_color(
                lv.color_hex(color if index < self.battery_segments else LINE), 0
            )

    def make_settings(self):
        self.settings = self.screen()
        self.header(self.settings, "Settings", self.show_home)
        card = surface(self.settings, 24, 104, 432, 120)
        text(card, "Brightness", 24, 20, 280, lv.font_montserrat_24)
        self.brightness_label = text(
            card, "70%", 312, 20, 96, lv.font_montserrat_24, ACCENT, lv.TEXT_ALIGN.RIGHT
        )
        self.slider = lv.slider(card)
        self.slider.set_pos(32, 78)
        self.slider.set_size(368, 16)
        self.slider.set_range(10, 100)
        self.slider.set_value(self.brightness, False)
        self.slider.set_style_bg_color(lv.color_hex(TINT), lv.PART.MAIN)
        self.slider.set_style_bg_opa(255, lv.PART.MAIN)
        self.slider.set_style_bg_color(lv.color_hex(ACCENT), lv.PART.INDICATOR)
        self.slider.set_style_bg_color(lv.color_hex(ACCENT), lv.PART.KNOB)
        self.slider.set_style_shadow_width(0, lv.PART.KNOB)
        self.slider.add_event_cb(self.brightness_changed, lv.EVENT.VALUE_CHANGED, None)
        wifi = button(self.settings, "", 24, 240, 432, 88, self.show_connection, radius=26)
        # This row uses explicit columns, rather than the centered button layout.
        wifi.set_layout(lv.LAYOUT.NONE)
        badge = surface(wifi, 20, 20, 48, 48, TINT, 16)
        icon = text(badge, "NET", 0, 0, None, lv.font_montserrat_16, ACCENT)
        icon.center()
        text(wifi, "Network", 88, 16, 280, lv.font_montserrat_24)
        text(wifi, "Wi-Fi / Ethernet", 88, 50, 280, lv.font_montserrat_16, MUTED)
        text(wifi, lv.SYMBOL.RIGHT, 390, 32, 24, lv.font_montserrat_24, MUTED)
        date = button(self.settings, "", 24, 344, 432, 88, self.show_timezone_settings, radius=26)
        date.set_layout(lv.LAYOUT.NONE)
        badge = surface(date, 20, 20, 48, 48, TINT, 16)
        clock_icon(badge, ACCENT)
        text(date, "Time zone", 88, 16, 280, lv.font_montserrat_24)
        self.timezone_summary = text(
            date, timezone_label(480), 88, 50, 280, lv.font_montserrat_16, MUTED
        )
        text(date, lv.SYMBOL.RIGHT, 390, 32, 24, lv.font_montserrat_24, MUTED)

    def make_timezone_settings(self):
        self.timezone_settings = self.screen()
        self.header(self.timezone_settings, "Time zone", self.show_settings)
        card = surface(self.timezone_settings, 24, 104, 432, 144)
        text(card, "Time zone", 24, 20, 384, lv.font_montserrat_24)
        self.timezone = lv.dropdown(card)
        self.timezone.set_pos(24, 70)
        self.timezone.set_size(384, 52)
        self.timezone.set_options("\n".join(timezone_label(n) for n in TIMEZONE_OFFSETS))
        self.timezone.set_style_text_font(lv.font_montserrat_18, 0)
        self.timezone.set_style_text_color(lv.color_hex(ACCENT), 0)
        self.timezone.set_style_bg_color(lv.color_hex(TINT), 0)
        self.timezone.set_style_bg_opa(255, 0)
        self.timezone.set_style_border_width(0, 0)
        self.timezone.set_style_radius(16, 0)
        self.timezone.set_style_pad_top(14, 0)
        self.timezone.add_event_cb(self.timezone_changed, lv.EVENT.VALUE_CHANGED, None)
        self.timezone.add_event_cb(self.style_timezone_list, lv.EVENT.READY, None)
        self.timezone_message = text(
            self.timezone_settings,
            "",
            24,
            360,
            432,
            lv.font_montserrat_16,
            MUTED,
            lv.TEXT_ALIGN.CENTER,
        )
        button(
            self.timezone_settings,
            "Save",
            24,
            408,
            432,
            48,
            self.save_timezone_clicked,
            color=ACCENT,
            foreground=CARD,
        )
        self.edit_offset = 480

    def style_timezone_list(self, event):
        popup = self.timezone.get_list()
        popup.set_style_text_font(lv.font_montserrat_18, 0)
        popup.set_style_text_color(lv.color_hex(INK), 0)
        popup.set_style_text_line_space(12, 0)
        popup.set_style_bg_color(lv.color_hex(CARD), 0)
        popup.set_style_border_width(0, 0)
        popup.set_style_radius(16, 0)
        popup.set_style_shadow_width(0, 0)
        popup.set_style_bg_color(lv.color_hex(TINT), lv.PART.SELECTED)
        popup.set_style_text_color(lv.color_hex(ACCENT), lv.PART.SELECTED)
        popup.set_style_bg_color(lv.color_hex(TINT), lv.PART.SELECTED | lv.STATE.CHECKED)
        popup.set_style_text_color(lv.color_hex(ACCENT), lv.PART.SELECTED | lv.STATE.CHECKED)

    def show_timezone_settings(self, event=None):
        offset = self.on_timezone_load() if self.on_timezone_load else 480
        # Include a custom fixed offset already saved on the device.
        self.timezone_offsets = sorted(set(TIMEZONE_OFFSETS + (offset,)))
        self.timezone.set_options("\n".join(timezone_label(n) for n in self.timezone_offsets))
        self.timezone.set_selected(self.timezone_offsets.index(offset), False)
        self.edit_offset = offset
        self.timezone_message.set_text("")
        self.current_page = "timezone"
        lv.screen_load(self.timezone_settings)

    def timezone_changed(self, event):
        self.edit_offset = self.timezone_offsets[self.timezone.get_selected()]
        self.timezone_message.set_text("")

    def save_timezone_clicked(self, event):
        if self.on_timezone_save:
            self.on_timezone_save(self.edit_offset)

    def set_timezone_result(self, message, success):
        self.timezone_message.set_style_text_color(
            lv.color_hex(CHARGING if success else DANGER), 0
        )
        self.timezone_message.set_text(message)

    def set_timezone_offset(self, offset):
        self.timezone_summary.set_text(timezone_label(offset))

    def make_connection(self):
        self.connection = self.screen()
        self.header(self.connection, "Network", self.back_from_connection)
        self.mode_buttons = {}
        for x, mode, title in ((24, "WIFI", "Wi-Fi"), (248, "ETH", "Ethernet")):
            self.mode_buttons[mode] = button(
                self.connection,
                title,
                x,
                104,
                208,
                56,
                lambda event, value=mode: self.select_mode(value),
            )
        card = surface(self.connection, 24, 184, 432, 164)
        self.connection_title = text(
            card, "Wi-Fi", 24, 20, 384, lv.font_montserrat_24, align=lv.TEXT_ALIGN.CENTER
        )
        self.connection_state = text(
            card, "Setup", 24, 62, 384, lv.font_montserrat_24, ACCENT, lv.TEXT_ALIGN.CENTER
        )
        self.connection_ip = text(
            card, "", 24, 112, 384, lv.font_montserrat_18, MUTED, lv.TEXT_ALIGN.CENTER
        )
        self.connection_message = text(
            self.connection, "", 24, 356, 432, lv.font_montserrat_16, MUTED, lv.TEXT_ALIGN.CENTER
        )
        self.connection_action = button(
            self.connection,
            "Select network",
            24,
            400,
            432,
            56,
            self.connection_clicked,
            color=ACCENT,
            foreground=CARD,
        )
        self.set_network_mode("WIFI")

    def set_network_mode(self, mode):
        self.network_mode = mode
        for value, obj in self.mode_buttons.items():
            selected = value == mode
            obj.set_style_bg_color(lv.color_hex(ACCENT if selected else CARD), 0)
            obj.get_child(0).set_style_text_color(lv.color_hex(CARD if selected else INK), 0)
        self.connection_title.set_text("Ethernet" if mode == "ETH" else "Wi-Fi")
        self.connection_action.get_child(0).set_text(
            "Reconnect" if mode == "ETH" else "Select network"
        )
        self.set_connection_info("checking", "")

    def set_connection_info(self, state, ip="", message=""):
        names = {
            "checking": "Checking",
            "unavailable": "Unavailable",
            "unconfigured": "Setup",
            "disconnected": "Disconnected",
            "connecting": "Connecting",
            "connected": "Connected",
        }
        color = (
            ACCENT
            if state == "connected"
            else (WARNING if state in ("checking", "connecting") else DANGER)
        )
        self.connection_state.set_text(names[state])
        self.connection_state.set_style_text_color(lv.color_hex(color), 0)
        self.connection_ip.set_text("IP: " + ip if ip else "")
        self.connection_message.set_text(message)

    def select_mode(self, mode):
        if mode != self.network_mode and self.on_mode:
            self.on_mode(mode)

    def connection_clicked(self, event=None):
        if self.network_mode == "WIFI":
            self.open_wifi()
        elif self.on_mode:
            self.on_mode("ETH")

    def show_connection(self, event=None):
        self.connection_return = self.current_page
        self.current_page = "connection"
        lv.screen_load(self.connection)

    def back_from_connection(self, event=None):
        if self.connection_return == "settings":
            self.show_settings()
        else:
            self.show_home()

    def set_identity(self, access_code, nickname):
        access_code = str(access_code or "")
        nickname = str(nickname or "")
        if access_code != self.access_code:
            self.access_code = access_code
            self.code_label.set_text(access_code)
        if nickname != self.nickname:
            self.nickname = nickname
            self.nickname_label.set_text(nickname)

    def set_brightness(self, value):
        self.brightness = max(10, min(100, value))
        self.slider.set_value(self.brightness, False)
        self.brightness_label.set_text("%d%%" % self.brightness)

    def set_network_result(self, message, color=ACCENT, busy=False):
        self.network_busy = busy
        self.network_message.set_text(message)
        self.network_message.set_style_text_color(lv.color_hex(color), 0)
        self.connect_label.set_text("Connecting..." if busy else "Connect")
        self._update_network_controls()

    def _update_network_controls(self):
        disabled = not self.wifi_available or self.network_busy or self.scanning
        self.refresh.get_child(0).set_style_text_color(
            lv.color_hex(MUTED if disabled else ACCENT), 0
        )
        if not self.wifi_available or self.network_busy or self.scanning or not self.selected_ssid:
            self.connect.add_state(lv.STATE.DISABLED)
        else:
            self.connect.remove_state(lv.STATE.DISABLED)
        for obj in [self.refresh] + self.ap_buttons:
            if not self.wifi_available or self.network_busy or self.scanning:
                obj.add_state(lv.STATE.DISABLED)
            else:
                obj.remove_state(lv.STATE.DISABLED)

    def set_wifi_available(self, available):
        self.wifi_available = available
        if not available:
            self.hide_keyboard()
        self._update_network_controls()

    def set_saved_network(self, ssid, password):
        self.saved_ssid, self.saved_password = ssid, password

    def make_networks(self):
        self.networks = self.screen()
        self.header(self.networks, "Wi-Fi", self.back_from_wifi)
        text(self.networks, "Select network", 24, 102, 280, color=MUTED)
        self.refresh = button(
            self.networks,
            "Refresh",
            344,
            88,
            112,
            48,
            self.refresh_clicked,
            foreground=ACCENT,
            radius=16,
        )
        self.refresh.set_style_bg_color(lv.color_hex(LINE), lv.STATE.DISABLED)
        self.ap_list = surface(self.networks, 24, 152, 432, 296, BG, 0)
        self.ap_list.add_flag(lv.obj.FLAG.SCROLLABLE)
        self.ap_list.set_scroll_dir(lv.DIR.VER)
        self.ap_list.set_scrollbar_mode(lv.SCROLLBAR_MODE.AUTO)
        self.scan_message = text(
            self.networks, "", 48, 248, 384, lv.font_montserrat_18, MUTED, lv.TEXT_ALIGN.CENTER
        )
        self._update_network_controls()

    def set_scan_state(self, message, busy=False, error=False):
        self.scanning = busy
        self.scan_message.set_text(message)
        self.scan_message.set_style_text_color(lv.color_hex(DANGER if error else MUTED), 0)
        self.scan_message.remove_flag(lv.obj.FLAG.HIDDEN)
        self.ap_list.add_flag(lv.obj.FLAG.HIDDEN)
        self._update_network_controls()

    def set_scan_results(self, networks):
        self.scanning = False
        self.ap_list.clean()
        self.ap_list.scroll_to_y(0, False)
        self.ap_buttons = []
        if not networks:
            self.set_scan_state("No networks found\nMove closer and refresh")
            return
        for index, (ssid, rssi, secured) in enumerate(networks):
            row = button(self.ap_list, "", 0, index * 72, 424, 64, radius=18)
            row.set_layout(lv.LAYOUT.NONE)
            row.add_event_cb(
                lambda event, name=ssid, lock=secured: self.select_network(name, lock),
                lv.EVENT.CLICKED,
                None,
            )
            name = text(row, ssid, 20, 17, 330, CN)
            name.set_height(30)
            name.set_long_mode(lv.label.LONG_MODE.DOTS)
            if secured:
                shackle = surface(row, 379, 18, 10, 13, CARD, 5)
                shackle.set_style_border_width(2, 0)
                shackle.set_style_border_color(lv.color_hex(MUTED), 0)
                body = surface(row, 376, 26, 16, 13, MUTED, 3)
                surface(body, 7, 4, 2, 5, CARD, 1)
            else:
                text(row, lv.SYMBOL.WIFI, 374, 22, 28, lv.font_montserrat_18, MUTED)
            self.ap_buttons.append(row)
        self.scan_message.add_flag(lv.obj.FLAG.HIDDEN)
        self.ap_list.remove_flag(lv.obj.FLAG.HIDDEN)
        self._update_network_controls()

    def refresh_clicked(self, event=None):
        if self.wifi_available and not self.scanning and not self.network_busy and self.on_scan:
            self.on_scan()

    def select_network(self, ssid, secured):
        if not self.wifi_available or self.scanning or self.network_busy:
            return
        self.hide_keyboard()
        self.selected_ssid = ssid
        self.ssid.set_text(ssid)
        self.password.set_password_mode(True)
        self.eye_icon.set_text(lv.SYMBOL.EYE_OPEN)
        self.password.set_text(self.saved_password if secured and ssid == self.saved_ssid else "")
        self.set_network_result("")
        self.current_page = "wifi"
        lv.screen_load(self.wifi)
        if secured:
            self.password_title.remove_flag(lv.obj.FLAG.HIDDEN)
            self.password.get_parent().remove_flag(lv.obj.FLAG.HIDDEN)
            self.open_network.add_flag(lv.obj.FLAG.HIDDEN)
            self.show_keyboard()
        else:
            self.password_title.add_flag(lv.obj.FLAG.HIDDEN)
            self.password.get_parent().add_flag(lv.obj.FLAG.HIDDEN)
            self.open_network.remove_flag(lv.obj.FLAG.HIDDEN)

    def input_field(self, card):
        frame = surface(card, 20, 64, 392, 52, TINT, 14)
        frame.set_style_border_width(1, 0)
        frame.set_style_border_color(lv.color_hex(ACCENT), 0)
        field = lv.textarea(frame)
        field.remove_style_all()
        field.set_pos(12, 0)
        field.set_one_line(True)
        field.set_max_length(63)
        field.set_password_mode(True)
        field.set_password_show_time(0)
        field.set_style_text_font(lv.font_montserrat_18, 0)
        field.set_style_text_color(lv.color_hex(INK), 0)
        field.set_style_anim_duration(0, 0)
        field.set_style_pad_ver(14, 0)
        field.set_style_pad_hor(0, 0)
        field.set_style_pad_right(12, 0)
        field.set_style_bg_opa(0, lv.PART.CURSOR)
        field.set_style_border_color(lv.color_hex(ACCENT), lv.PART.CURSOR)
        field.set_style_border_width(1, lv.PART.CURSOR)
        field.set_style_border_side(lv.BORDER_SIDE.LEFT, lv.PART.CURSOR)
        field.set_style_pad_all(0, lv.PART.CURSOR)
        field.set_style_anim_duration(0, lv.PART.CURSOR)
        field.set_size(326, 52)
        field.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)
        field.remove_flag(lv.obj.FLAG.SCROLL_ON_FOCUS)
        field.add_event_cb(self.field_clicked, lv.EVENT.CLICKED, None)
        return field

    def make_wifi(self):
        self.wifi = self.screen()
        self.header(self.wifi, "Wi-Fi", self.back_to_networks)
        card = surface(self.wifi, 24, 88, 432, 120)
        text(card, "SSID", 20, 10, 56, lv.font_montserrat_16, MUTED)
        self.ssid = text(card, "", 84, 4, 328, CN)
        self.ssid.set_height(30)
        self.ssid.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        self.password_title = text(card, "Password", 20, 38, 392, lv.font_montserrat_16, MUTED)
        self.password = self.input_field(card)
        self.open_network = text(
            card, "Open network - no password", 20, 68, 392, lv.font_montserrat_18, MUTED
        )
        self.open_network.add_flag(lv.obj.FLAG.HIDDEN)
        self.eye = lv.button(self.password.get_parent())
        self.eye.remove_style_all()
        self.eye.set_pos(344, 8)
        self.eye.set_size(36, 36)
        self.eye.set_ext_click_area(4)
        # This action belongs to the input and must not take its focus.
        self.eye.remove_flag(lv.obj.FLAG.CLICK_FOCUSABLE)
        self.eye.remove_flag(lv.obj.FLAG.SCROLLABLE)
        self.eye.set_style_radius(8, 0)
        self.eye.set_style_bg_color(lv.color_hex(TINT), lv.STATE.PRESSED)
        self.eye.set_style_bg_opa(255, lv.STATE.PRESSED)
        self.eye.add_event_cb(self.toggle_password, lv.EVENT.CLICKED, None)
        self.eye_icon = text(
            self.eye, lv.SYMBOL.EYE_OPEN, 0, 0, None, lv.font_montserrat_18, MUTED
        )
        self.eye_icon.center()
        self.network_message = text(
            self.wifi, "", 24, 208, 432, lv.font_montserrat_16, ACCENT, lv.TEXT_ALIGN.CENTER
        )
        self.connect = button(
            self.wifi,
            "Connect",
            248,
            408,
            208,
            52,
            self.connect_clicked,
            color=ACCENT,
            foreground=0xFFFFFF,
        )
        button(self.wifi, "Cancel", 24, 408, 208, 52, self.back_to_networks)
        self.connect_label = self.connect.get_child(0)
        self.connect.set_style_bg_color(lv.color_hex(0x93B4E6), lv.STATE.DISABLED)
        self.keyboard = lv.keyboard(self.wifi)
        self.keyboard.set_align(lv.ALIGN.TOP_LEFT)
        self.keyboard.set_pos(10, 232)
        self.keyboard.set_size(460, 170)
        self.keyboard.set_mode(lv.keyboard.MODE.TEXT_LOWER)
        self.keyboard.set_popovers(False)
        self.keyboard.set_style_bg_color(lv.color_hex(BG), 0)
        self.keyboard.set_style_bg_opa(255, 0)
        self.keyboard.set_style_border_width(0, 0)
        self.keyboard.set_style_radius(18, 0)
        self.keyboard.set_style_pad_all(4, 0)
        self.keyboard.set_style_pad_row(6, 0)
        self.keyboard.set_style_pad_column(4, 0)
        self.keyboard.set_style_text_font(lv.font_montserrat_16, lv.PART.ITEMS)
        self.keyboard.set_style_text_color(lv.color_hex(INK), lv.PART.ITEMS)
        self.keyboard.set_style_bg_color(lv.color_hex(CARD), lv.PART.ITEMS)
        # Keep keys visually stable on touch; the keyboard does not need a
        # pressed animation for this compact preview.
        self.keyboard.set_style_bg_color(lv.color_hex(CARD), lv.PART.ITEMS | lv.STATE.PRESSED)
        self.keyboard.set_style_color_filter_opa(0, lv.PART.ITEMS | lv.STATE.PRESSED)
        self.keyboard.set_style_border_width(0, lv.PART.ITEMS)
        self.keyboard.set_style_radius(8, lv.PART.ITEMS)
        self.keyboard.set_style_shadow_width(0, lv.PART.ITEMS)
        self.keyboard_mode = None
        self.keyboard_single_press()
        self.keyboard.add_event_cb(self.keyboard_single_press, lv.EVENT.VALUE_CHANGED, None)
        self.keyboard.add_event_cb(self.keyboard_done, lv.EVENT.READY, None)
        self.keyboard.add_event_cb(self.keyboard_done, lv.EVENT.CANCEL, None)
        self.keyboard.add_flag(lv.obj.FLAG.HIDDEN)

    def show_home(self, event=None):
        self.current_page = "home"
        lv.screen_load(self.home)

    def show_settings(self, event=None):
        self.current_page = "settings"
        lv.screen_load(self.settings)

    def open_wifi(self, event=None):
        self.wifi_return = self.current_page
        self.back_to_networks()
        self.refresh_clicked()

    def back_to_networks(self, event=None):
        self.hide_keyboard()
        self.current_page = "networks"
        lv.screen_load(self.networks)

    def back_from_wifi(self, event=None):
        self.hide_keyboard()
        if self.wifi_return == "connection":
            self.current_page = "connection"
            lv.screen_load(self.connection)
        elif self.wifi_return == "settings":
            self.show_settings()
        else:
            self.show_home()

    def brightness_changed(self, event):
        self.set_brightness(self.slider.get_value())
        if self.on_brightness:
            self.on_brightness(self.brightness)

    def connect_clicked(self, event):
        if (
            self.wifi_available
            and self.on_connect
            and self.selected_ssid
            and not self.network_busy
            and not self.scanning
        ):
            self.hide_keyboard()
            self.on_connect(self.selected_ssid, self.password.get_text())

    def field_clicked(self, event):
        self.show_keyboard()

    def show_keyboard(self):
        if self.is_password_editing():
            return
        if self.active_field != self.password:
            self.keyboard.set_mode(lv.keyboard.MODE.TEXT_LOWER)
        self.keyboard_single_press()
        self.active_field = self.password
        self.password.add_state(lv.STATE.FOCUSED)
        self.password.get_parent().add_state(lv.STATE.FOCUSED)
        self.keyboard.set_textarea(self.active_field)
        self.keyboard.remove_flag(lv.obj.FLAG.HIDDEN)

    def hide_keyboard(self):
        self.keyboard.set_textarea(None)
        self.keyboard.add_flag(lv.obj.FLAG.HIDDEN)
        self.password.remove_state(lv.STATE.FOCUSED)
        self.password.get_parent().remove_state(lv.STATE.FOCUSED)
        self.active_field = None

    def is_password_editing(self):
        return self.current_page == "wifi" and self.active_field is not None

    def keyboard_done(self, event):
        self.hide_keyboard()

    def keyboard_single_press(self, event=None):
        # Only a map change resets LVGL's flags. Ordinary characters must not
        # invalidate every key by setting those flags again on each keystroke.
        mode = self.keyboard.get_mode()
        if mode == self.keyboard_mode:
            return
        self.keyboard_mode = mode
        lv.buttonmatrix.__cast__(self.keyboard).set_button_ctrl_all(
            lv.buttonmatrix.CTRL.NO_REPEAT | lv.buttonmatrix.CTRL.CLICK_TRIG
        )

    def toggle_password(self, event):
        cursor = self.password.get_cursor_pos()
        masked = not self.password.get_password_mode()
        self.password.set_password_mode(masked)
        # Recalculate the visible range for the new glyph widths without
        # animating through the beginning of a long password.
        self.password.update_layout()
        self.password.set_cursor_pos(0)
        self.password.set_cursor_pos(cursor)
        position = lv.point_t()
        self.password.get_label().get_letter_pos(cursor, position)
        font = self.password.get_style_text_font(0)
        self.password.scroll_to_x(
            max(0, position.x - self.password.get_content_width() + font.line_height), False
        )
        # The icon describes the available action: show, or hide.
        self.eye_icon.set_text(lv.SYMBOL.EYE_OPEN if masked else lv.SYMBOL.EYE_CLOSE)

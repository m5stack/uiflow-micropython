# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import asyncio
import binascii
import builtins
from collections import namedtuple
import esp32
import machine
import M5
from M5 import Widgets as M5Widgets
import network
import os
from startup import Startup, print_access_info
import time
import widgets

try:
    import M5Things

    HAS_SERVER = True
except ImportError:
    HAS_SERVER = False


M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FASTEST)
M5.begin()
M5Widgets.setRotation(0)
M5Widgets.fillScreen(0xFFFFFF)

REFERENCE_WIDTH = 540
REFERENCE_HEIGHT = 960
TEST_VERSION = "papermono-startup-dynamic-shadow-12"
FRAMEWORK_REGISTRY = "_papermono_startup_test_framework"
DYNAMIC_BG_COLOR = 0xAAAAAA

SCREEN_WIDTH = M5.Display.width()
SCREEN_HEIGHT = M5.Display.height()
SCALE = min(SCREEN_WIDTH / REFERENCE_WIDTH, SCREEN_HEIGHT / REFERENCE_HEIGHT)
OFFSET_X = int((SCREEN_WIDTH - REFERENCE_WIDTH * SCALE) / 2 + 0.5)
OFFSET_Y = int((SCREEN_HEIGHT - REFERENCE_HEIGHT * SCALE) / 2 + 0.5)


def px(value):
    return OFFSET_X + int(value * SCALE + 0.5)


def py(value):
    return OFFSET_Y + int(value * SCALE + 0.5)


def size(value):
    return int(value * SCALE + 0.5)


def load_asset(name):
    return binascii.a2b_base64(EMBEDDED_ASSETS[name])


def draw_background(name):
    M5.Display.drawImage(load_asset(name), 0, 0)


def large_font():
    return M5.Display.FONTS.Montserrat36


def app_list_font():
    return M5.Display.FONTS.Montserrat24


Descriptor = namedtuple("Descriptor", ("x", "y", "w", "h"))


class AppBase:
    def __init__(self):
        self._task = None

    def install(self):
        self.on_install()

    def start(self):
        self.on_launch()
        self.on_view()
        self._task = asyncio.create_task(self.on_run())

    def stop(self):
        if self._task is not None:
            self._task.cancel()
            self._task = None
        self.on_exit()

    def on_install(self):
        pass

    def on_launch(self):
        pass

    def on_view(self):
        pass

    async def on_run(self):
        while True:
            await asyncio.sleep_ms(500)

    def on_exit(self):
        pass


class AppSelector:
    def __init__(self, apps):
        self._apps = apps
        self._index = 0

    def current(self):
        return self._apps[self._index]

    def select(self, app):
        self._index = self._apps.index(app)


class StatusBarApp(AppBase):
    WIFI_OK = "wifi_icon_ok_40@925.jpg"
    WIFI_ERROR = "wifi_icon_error_40@925.jpg"
    SERVER_OK = "server_icon_ok_80@925.jpg"
    SERVER_ERROR = "server_icon_error_80@925.jpg"

    def __init__(self, wifi):
        super().__init__()
        self._wifi = wifi
        self._wifi_state = None
        self._server_state = None

    def on_view(self):
        self._wifi_image = widgets.Image(use_sprite=False)
        self._wifi_image.set_pos(px(40), py(925))
        self._wifi_image.set_size(size(32), size(26))

        self._server_image = widgets.Image(use_sprite=False)
        self._server_image.set_pos(px(80), py(925))
        self._server_image.set_size(size(32), size(26))

    def _wifi_connected(self):
        return self._wifi.connect_status() == network.STAT_GOT_IP

    @staticmethod
    def _server_connected():
        try:
            return HAS_SERVER and M5Things.status() == 2
        except Exception:
            return False

    def refresh(self):
        self._wifi_state = None
        self._server_state = None

    async def on_run(self):
        while True:
            wifi_state = self._wifi_connected()
            server_state = self._server_connected()
            if wifi_state != self._wifi_state:
                self._wifi_image.set_src(
                    load_asset(self.WIFI_OK if wifi_state else self.WIFI_ERROR)
                )
                self._wifi_state = wifi_state
            if server_state != self._server_state:
                self._server_image.set_src(
                    load_asset(self.SERVER_OK if server_state else self.SERVER_ERROR)
                )
                self._server_state = server_state
            await asyncio.sleep_ms(1000)


class DevApp(AppBase):
    def __init__(self, wifi):
        super().__init__()
        self._wifi = wifi

    def on_install(self):
        self.descriptor = Descriptor(470, 1, 100, 181)

    def _state(self):
        try:
            return "ONLINE" if HAS_SERVER and M5Things.status() == 2 else "OFFLINE"
        except Exception:
            return "OFFLINE"

    @staticmethod
    def _access_code():
        try:
            if HAS_SERVER and M5Things.status() == 2:
                return M5Things.accesscode() or ""
        except Exception:
            pass
        return ""

    @staticmethod
    def _nickname():
        try:
            if HAS_SERVER and M5Things.status() == 2:
                return M5Things.nick_name() or ""
        except Exception:
            pass
        return ""

    def on_launch(self):
        self._state_text = self._state()
        self._access_code_text = self._access_code()
        self._nickname_text = self._nickname()

    def on_view(self):
        draw_background("flow.png")
        font = large_font()
        label_args = {
            "w": size(349),
            "h": size(46),
            "fg_color": 0x000000,
            "bg_color": DYNAMIC_BG_COLOR,
            "font": font,
            "parent": M5.Lcd,
        }
        self._state_label = widgets.Label("", px(89), py(452), **label_args)
        self._mac_label = widgets.Label("", px(89), py(572), **label_args)
        self._access_code_label = widgets.Label("", px(89), py(692), **label_args)
        self._nickname_label = widgets.Label("", px(89), py(812), **label_args)
        self._access_code_label.set_long_mode(widgets.Label.LONG_DOT)
        self._nickname_label.set_long_mode(widgets.Label.LONG_DOT)
        self._state_label.set_text(self._state_text)
        self._mac_label.set_text(binascii.hexlify(machine.unique_id()).decode().upper())
        self._access_code_label.set_text(self._access_code_text)
        self._nickname_label.set_text(self._nickname_text)

    async def on_run(self):
        while True:
            state = self._state()
            access_code = self._access_code()
            nickname = self._nickname()
            state_changed = state != self._state_text
            access_code_changed = access_code != self._access_code_text
            nickname_changed = nickname != self._nickname_text
            if state_changed or access_code_changed or nickname_changed:
                M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FAST)
                M5.Display.startWrite()
                try:
                    if state_changed:
                        self._state_text = state
                        self._state_label.set_text(state)
                    if access_code_changed:
                        self._access_code_text = access_code
                        self._access_code_label.set_text(access_code)
                    if nickname_changed:
                        self._nickname_text = nickname
                        self._nickname_label.set_text(nickname)
                finally:
                    M5.Display.endWrite()
                    M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FASTEST)
            print_access_info(nickname, access_code)
            await asyncio.sleep_ms(1500)

    def on_exit(self):
        del self._state_label
        del self._mac_label
        del self._access_code_label
        del self._nickname_label


class SettingsApp(AppBase):
    def on_install(self):
        self.descriptor = Descriptor(470, 164, 100, 181)

    def on_view(self):
        draw_background("config.png")
        nvs = esp32.NVS("uiflow")
        ssid = nvs.get_str("ssid0")
        server = nvs.get_str("server")
        label_args = {
            "w": size(333),
            "h": size(30),
            "font_align": widgets.Label.LEFT_ALIGNED,
            "fg_color": 0x000000,
            "bg_color": DYNAMIC_BG_COLOR,
            "font": M5.Lcd.FONTS.Montserrat20,
            "parent": M5.Lcd,
        }
        self._ssid_label = widgets.Label("", px(87), py(620), **label_args)
        self._server_label = widgets.Label("", px(87), py(737), **label_args)
        self._ssid_label.set_long_mode(widgets.Label.LONG_DOT)
        self._server_label.set_long_mode(widgets.Label.LONG_DOT)
        self._ssid_label.set_text(ssid)
        self._server_label.set_text(server)

    def on_exit(self):
        del self._ssid_label
        del self._server_label


class Rectangle:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        M5.Lcd.fillRect(x, y, width, height, 0x000000)

    def set_pos(self, x, y):
        M5.Lcd.fillRect(self._x, self._y, self._width, self._height, 0xFFFFFF)
        self._x = x
        self._y = y
        M5.Lcd.fillRect(x, y, self._width, self._height, 0x000000)


class AppListApp(AppBase):
    def on_install(self):
        self.descriptor = Descriptor(470, 321, 100, 181)

    def on_launch(self):
        try:
            self._files = sorted(name for name in os.listdir("apps") if name.endswith(".py"))
        except OSError:
            self._files = []
        self._selected = 0

    def on_view(self):
        draw_background("applist.png")
        self._cursor = Rectangle(px(65), py(438), size(10), size(42))
        self._labels = []
        for index in range(9):
            text = self._files[index] if index < len(self._files) else ""
            label = widgets.Label(
                text,
                px(80),
                py(440 + 48 * index),
                w=size(324),
                h=size(32),
                fg_color=0x000000,
                bg_color=0xFFFFFF,
                font=app_list_font(),
                parent=M5.Lcd,
            )
            label.set_long_mode(widgets.Label.LONG_DOT)
            label.set_text(text)
            self._labels.append(label)
        M5.Display.setFont(app_list_font())
        print("App list font height:", M5.Display.fontHeight())

    def select_row(self, reference_y):
        index = int((reference_y - 435) // 48)
        if 0 <= index < min(9, len(self._files)):
            self._selected = index
            M5.Display.startWrite()
            try:
                self._cursor.set_pos(px(65), py(438 + 48 * index))
            finally:
                M5.Display.endWrite()

    def on_exit(self):
        del self._labels
        del self._cursor


class Framework:
    def __init__(self, wifi):
        previous = getattr(builtins, FRAMEWORK_REGISTRY, None)
        if previous is not None:
            print("Stopping previous PaperMono test instance")
            previous.shutdown()

        self._apps = [DevApp(wifi), SettingsApp(), AppListApp()]
        for app in self._apps:
            app.install()
        self._selector = AppSelector(self._apps)
        self._current = self._apps[0]
        self._status_bar = StatusBarApp(wifi)
        self._running = True
        setattr(builtins, FRAMEWORK_REGISTRY, self)
        print("PaperMono test instance registered")
        print(
            "Page descriptors:",
            [(app.__class__.__name__, app.descriptor) for app in self._apps],
        )

    def shutdown(self):
        self._running = False
        for app in self._apps:
            if app._task is not None:
                app.stop()
        if self._status_bar._task is not None:
            self._status_bar.stop()

    @staticmethod
    def _contains(descriptor, x, y):
        return (
            descriptor.x <= x <= descriptor.x + descriptor.w
            and descriptor.y <= y <= descriptor.y + descriptor.h
        )

    @staticmethod
    def _to_reference(x, y, width, height):
        scale = min(width / REFERENCE_WIDTH, height / REFERENCE_HEIGHT)
        offset_x = (width - REFERENCE_WIDTH * scale) / 2
        offset_y = (height - REFERENCE_HEIGHT * scale) / 2
        return ((x - offset_x) / scale, (y - offset_y) / scale)

    @classmethod
    def _touch_candidates(cls, x, y):
        if SCREEN_WIDTH <= SCREEN_HEIGHT:
            rotated_x = y * SCREEN_WIDTH / SCREEN_HEIGHT
            rotated_y = (SCREEN_WIDTH - 1 - x) * SCREEN_HEIGHT / SCREEN_WIDTH
            return [
                cls._to_reference(
                    rotated_x,
                    rotated_y,
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                ),
                cls._to_reference(x, y, SCREEN_WIDTH, SCREEN_HEIGHT),
            ]

        candidates = [cls._to_reference(x, y, SCREEN_WIDTH, SCREEN_HEIGHT)]
        portrait_width = SCREEN_HEIGHT
        portrait_height = SCREEN_WIDTH
        candidates.extend(
            (
                cls._to_reference(
                    y,
                    SCREEN_WIDTH - 1 - x,
                    portrait_width,
                    portrait_height,
                ),
                cls._to_reference(
                    SCREEN_HEIGHT - 1 - y,
                    x,
                    portrait_width,
                    portrait_height,
                ),
            )
        )
        return candidates

    def _handle_touch(self, x, y):
        selected = None
        reference_point = None
        candidates = self._touch_candidates(x, y)
        print(
            "Touch candidates:",
            [
                (index, int(reference_x), int(reference_y))
                for index, (reference_x, reference_y) in enumerate(candidates)
            ],
        )
        for candidate_index, (reference_x, reference_y) in enumerate(candidates):
            for app in self._apps:
                if self._contains(app.descriptor, reference_x, reference_y):
                    selected = app
                    reference_point = (reference_x, reference_y)
                    print(
                        "Touch hit: candidate={}, page={}".format(
                            candidate_index, app.__class__.__name__
                        )
                    )
                    break
            if selected is not None:
                break

        if selected is not None:
            self._switch_to(selected)
            print(
                "Page touch: raw=({}, {}), reference=({}, {})".format(
                    x,
                    y,
                    int(reference_point[0]),
                    int(reference_point[1]),
                )
            )
            return

        if isinstance(self._current, AppListApp):
            for reference_x, reference_y in candidates:
                if 60 <= reference_x <= 450 and 435 <= reference_y <= 872:
                    print("Touch hit: app list row")
                    self._current.select_row(reference_y)
                    return
        print("Touch miss: no page or app-list row matched")

    def _switch_to(self, app):
        if app is self._current:
            print("Page switch skipped: already on", app.__class__.__name__)
            return
        print(
            "Page switch: {} -> {}".format(
                self._current.__class__.__name__, app.__class__.__name__
            )
        )
        self._current.stop()
        self._selector.select(app)
        self._current = app
        self._start_current_page()
        self._status_bar.refresh()

    def _start_current_page(self):
        M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FAST)
        M5.Display.startWrite()
        try:
            self._current.start()
        finally:
            M5.Display.endWrite()
            M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FASTEST)

    async def run(self):
        self._start_current_page()
        self._status_bar.start()
        touch_locked = False
        release_samples = 0
        last_touch_count = -1
        last_heartbeat = time.ticks_ms()
        while self._running:
            M5.update()
            touch_count = M5.Touch.getCount()
            now = time.ticks_ms()
            if touch_count != last_touch_count:
                print(
                    "Touch count: {} -> {}, locked={}".format(
                        last_touch_count, touch_count, touch_locked
                    )
                )
                last_touch_count = touch_count
            if time.ticks_diff(now, last_heartbeat) >= 3000:
                print(
                    "Touch heartbeat: count={}, locked={}, release_samples={}".format(
                        touch_count, touch_locked, release_samples
                    )
                )
                last_heartbeat = now
            if touch_count > 0:
                release_samples = 0
                if not touch_locked:
                    touch_locked = True
                    touch_x = M5.Touch.getX()
                    touch_y = M5.Touch.getY()
                    try:
                        touch_detail = M5.Touch.getDetail(0)
                    except Exception as error:
                        touch_detail = "getDetail failed: {}".format(error)
                    print(
                        "Touch press: raw=({}, {}), detail={}".format(
                            touch_x, touch_y, touch_detail
                        )
                    )
                    self._handle_touch(touch_x, touch_y)
            elif touch_locked:
                release_samples += 1
                if release_samples >= 5:
                    touch_locked = False
                    release_samples = 0
                    print("Touch rearmed after stable release")
            await asyncio.sleep_ms(10)


def main():
    print("Test version:", TEST_VERSION)
    print("PaperMono Widgets rotation 0: {}x{}".format(SCREEN_WIDTH, SCREEN_HEIGHT))
    print(
        "Layout: reference={}x{}, scale={}, offset=({}, {})".format(
            REFERENCE_WIDTH,
            REFERENCE_HEIGHT,
            SCALE,
            OFFSET_X,
            OFFSET_Y,
        )
    )
    nvs = esp32.NVS("uiflow")
    ssid = nvs.get_str("ssid0")
    password = nvs.get_str("pswd0")
    wifi = Startup()
    if ssid:
        wifi.connect_network(ssid, password)
        print("Try to connect {}...".format(ssid))
    else:
        print("Wi-Fi not configured")

    framework = Framework(wifi)
    M5.Display.setEpdMode(M5.Display.EPDMode.EPD_FAST)
    draw_background("startup.png")
    time.sleep(1)
    asyncio.run(framework.run())


EMBEDDED_ASSETS = {
    "startup.png": (
        b"iVBORw0KGgoAAAANSUhEUgAAAeAAAAMgCAIAAAB0wSZfAAAPm0lEQVR42u3d3ZKquAKA0fRUv2J4SHlI9wXVliMY"
        b"QkggyloXU2dOtz/A+JmOAX/u93tobxiGcIYYY4wxAHyg/+wCAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgA"
        b"BBpAoAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgAgQZAoAEQaACBBkCgAQQaAIEGQKAB"
        b"BBoAgQYQaAAEGkCgARBoAAQaQKABuGagY4wxRscJEOju6qzRgED3W2eNBq7p91NmNqZ/HcfRMQOMoLubdzaOBgS6"
        b"308FNRoQ6H7XbGg0IND9rqjTaECg+13vrNGAQPd7NopGAwLd77mCGg0IdL9ncms0INAVTgts1FbrpgGBrnxmYMV6"
        b"ajHwfX7u97u9AGAOGgCBBhBoAAQaQKABEGgABBpAoAEQaACBBkCgARBoAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQa"
        b"QKABEGgABBpAoAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgAgQZAoAEQaACBBkCgAQQa"
        b"AIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgAgQZAoAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGkCgARBo"
        b"AAQaQKABEGgAgQZAoAEQaACBBkCgAQQaAIEGEGgABBoAgQYQaAAEGkCgARBoAAQaQKABEGgAgQZAoAEQaACBBkCg"
        b"AQQaAIEGEGgABBoAgQYQaAAEGkCgARBoAAQaQKABEGgAgQZAoAEEGgCBBkCgAQQaAIEGEGgABBoAgQYQaAAEGkCg"
        b"ARBoAIEGQKABEGgAgQZAoAEEGgCBBkCgAQQaAIEGEGgABBpAoO0CAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKAB"
        b"EGgABBpAoAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgAgQZAoAEQaACBBkCgAQQaAIEG"
        b"QKABBBoAgQYQaAAEGkCgARBoAAQaQKABEGgAgQZAoAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGkCgARBoAAQa"
        b"QKABEGgAgQZAoAEQaACBBkCgAQQaAIEGEGgABBoAgQYQaAAEGkCgARBoAAQaQKABEGgAgQZAoAEEGgCBBkCgAT7d"
        b"r11wQeM4Nr3/GOPHPe1GzxkEmm2Zax3oFr074Gkf0Oj0JniTQKAJnxjojx5BT8/8+Z+JR5dpBPrSYoymCw7+kyW9"
        b"wx/tfuw6+xCBhpPTvHiTqc4ajUBDL3WeT+ZodLDMDuinzo97GIbhgE8LEGhQ5xIaLdBAvysCj1kWiUCDOgs0Ag3f"
        b"tcZcowUa6HG0q84CDfRbUhMdAg10Os5VZ4EGZBSBBtQfgQYQaMAgGoGGcNHrxNoJAg2AQAOGzwg0aCgCDeos/Qg0"
        b"aDQCDZyV0RijOgs00GlJBVqgge4abfgs0ECnSRXoK/u1C6DRdMT+M7Nvt5s6CzTQXaPVGYGG7hod/9iNAg00nIwe"
        b"/+RnXZ0RaDhuKD2V+t2A+vE7VtQh0HDa2SvT/35kev4jEGg4P9MQrIMGEGgABBpAoAEQaAAEGkCgARBoAIEGQKAB"
        b"glO9gT32X54/+GZCBBoaGYahUUPHcXStO4EGeh9HE8xBA6Hj6+Eh0IDhOQINgEADCDQAAg0g0AAINIBAAyDQAAg0"
        b"gEADINAAAg2AQAMg0AACDYBAAwg0AAINgEADCDQAAg0g0AAINIBAAyDQAAg0gEADINAAAg2AQAMg0DQzjqOdAAIN"
        b"INBgEA0CjToDAo1Gg0BzvUBrNAg0Gg3f6dcuoPUsR4zR3gCBpsdBdIxxarRSg0DTaabNeIBAY10HBB8SAiDQAALN"
        b"d/NJHQg0Gg0INBoNAg2AQGP4DAKNRgMCTVeB1mgQaAyiAYFGo0GgMcsBCDQG0SDQGEQDAo1GAwKNRkNwwX4+fhra"
        b"NfVBoNFoQKDRaBBoNBoQaDQaglUcXLTRt9vtdrtZ2gFG0PQ7lI4xjuNoNA0CTafTHTINAs3HDKXFGgSaHk84HMdx"
        b"6vXzTyUbqvu53+/2AsW+qcs7PxQ9YFf42FagAQiW2QEg0AACDYBAAwg0AAINgEADCDQAwanehM0nv1U8BW7x+2ff"
        b"XWjpmC+r3bmNj0uRbHrE+cM9b+z+X0Cg+fI0V69z4nTkxKM0jc4wDDu3cbrwyKbn+S6viR3y/NPxj1O9McVx3Tq3"
        b"uIJoVwUZhqHKNo7jON1V+IRLgiDQuMhR76on1RWxEWiOm9zw9mO/IdDwPX8iaDTBh4Sc6Ha7hQt87UBY+2gRBJru"
        b"6vzFH1LFP6u/ZqRMMMXBx40ur7CBVhwj0Hzbdz7ZDxBMcRB6XeBh7AkCTb8rHwQagikOTA6AQAMg0AAEc9CEyhMU"
        b"1g6DQNNpoE1Ag0DjUz4I5qABEGgABBpAoIGwdaGLxTAINL5269AvT5nuMPMzWI0mWMVBP40+ZvXIMAzT1xG8e7jp"
        b"+bS4YP/0zbOrF5PyxVoINH2NVcvqPN1w622nSibq3K6Pj3tefIhG37OOQENYvQZpIj17wlQQ9xM7+O6hdZlgDprr"
        b"nP/S4hHPvdq1c4gEGr7hy7RaPFz+HZ776Ag0fECjK349eea3zRb88il3yKf4ud/v9kLwvVZHNbTu/G/+ooidc9wF"
        b"e6bWR47SLNBYgHz0n9K1Mr36hKsk8qwtlWaBFmiAYA4aAIEGEGgABBpAoAEQaAAEGkCgARBoAIEGQKABEGgAgQZA"
        b"oAEEGgCBBhBoAAQaAIEGEGgABBpAoAEQaAAEGkCgARBoAIEGQKABBBoAgQZAoAEEGgCBBhBoAAQaAIEGEGgABBpA"
        b"oAEQaACBBkCgARBoAIEGQKABBBoAgQZAoAEEGgCBBhBoAAQaAIEGEGgABBpAoAEQaACBBkCgARBoAIEGQKABBBoA"
        b"gQZAoAEEGgCBBhBoAAQaQKABEGgABBpAoAEQaACBBkCgARBoAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgA"
        b"BBpAoAEQaACBBkCgARBoAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgABBpAoAEQaACBBkCgAQQaAIEGQKAB"
        b"BBoAgQYQaAAEGgCBBhBoAAQaQKABEGgAgQZAoAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGkCg7QIAgQZAoAEE"
        b"GgCBBhBoAAQaAIEGEGgABBpAoAEQaAAEGkCgARBoAIEGQKABBBoAgQZAoAEEGgCBBhBoAAQaAIEGEGgABBpAoAEQ"
        b"aACBBkCgARBoAIEGQKABBBoAgQZAoAEEGgCBBhBoAAQaQKABEGgABBpAoAEQaACBBkCgARBoAIEGQKABBBoAgQZA"
        b"oAEEGgCBBhBoAAQaQKABEGgABBpAoAEQaACBBkCgARBoAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgABBpA"
        b"oAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGgCBBhBoAAQaQKABEGgABBpAoAEQaACBBkCgAQQaAIEGQKABBBoA"
        b"gQYQaAAEGgCBBhBoAAQaQKABEGgAgQZAoAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGkCgARBoAAQaQKABEGgA"
        b"gQZAoAEQaACBBkCgAQQaAIEGQKABBBoAgQYQaAAEGkCgARBoAAQaQKABEGgAgQZAoAH482sXnGgcx3EcX/7PGGOM"
        b"8d3vP/6ZvsniPc+93DDnVs+//+55OmQFhwwEuq+X+mG3yqlt8RO4Tmh6OGQEUxx8UB3mfcwswv6wSk+tQwYC/Rkv"
        b"4ET1qje60Z/8DplGE0xxfHEF5nPKx6c2Pa/K6YcMgeYI02s7/ZJ+/DT9y/PIlg3W0jfMqU+V2erM94zWDz2/ecVD"
        b"VmWTCzbBxwwCTYXZ261jsdPHbo8n8BKI6V8XX+05swTpe5jfT+YN50F8ef6b8lp8CNLPfNMfNPNNyEnt4hPI3O0I"
        b"tEaHslgcv1GrE7WroVzczEcm5vMJ6UfPvOFzjLbONe88ZOlnnn7y73q6uPfSOz+x1ekngECzeSIifwxVpfiJF/ni"
        b"C77s3SsR2U0TDpkf+lVPUtmi9WmrVxP5+OnW95LMo2YcLdAXnYCuskxi/suLt93T6PTzSaRt61KHxM3niU9/wpkZ"
        b"7vzd1fSQvdvwnAHs6pvQ1l23enMEmv8NvnaOdnNeY4sD88UB8suvpf91cW43Mcx/Hg8mNjzz1MpNm/8yk9vokC3G"
        b"MbFocnW/ze+kYNdtenNFoC9R3nd/a89HxPtfLcWTDOkBZv7AKuc3X84pzx8FLzYuv7bPhUo8zxaHrGzJTTrxW3fd"
        b"u3fZl3G0QbRAh0tdzyHzhbdpejT/z/zicxGLp5IL7vZl89Njw8yY5owfGx2yl/sseDPYef5L/vRXzmcACLSVHhsS"
        b"PG/Nu8nE4ozuGXpXfJGvDp9bX5+k+JC12Cfp2YnET2VXoCl8TeZ05+VT/tU/VIuHuolh5unzlVs3sCDuFQ9Zb//J"
        b"abRAk7umYnFVbDp/tV5gmyZPVp9b+i/0+V/6+QU86zydiofsgDOPfMQn0DR8tdRa7Fzx4cLGtWJVVkScFZoWh6zK"
        b"8Sp+b9N3gSbUvZBF/vhx8YyGd0Vo8fJLT3/3MGXU1SH7rP9ifdWAQCt41uth62LViqPsPWfKlY3Q8595/gWVKnZn"
        b"6yFbXJFS/WquxxxxBDpc+RPCrYPQxeFz2el/x/8x8W6NdnFr6i4gaXTIms4+7dn2/LWACPTlGl18Qlf6hO/067zK"
        b"N608T6HknyiRcw+rJ6G83Lb6O1DTQ5Z45i3mT95dum/PQmkE+lqfEIbsq0OsXlbigBfYy/kjZRfeTN9D4ky5+dkr"
        b"O+t84iFLv63mf8FC/vkve97XEehrNbpgpnV1scT8Ghf9fLnq6tU+E6dxv7sIdc7y7a4O2aYNb/FNEb6jK/hOQra+"
        b"4DNPaM45DaHFdXDSH4ttem2n76f4UebvTI2mVusestUN3z8BnbPr9jwHjKC/f/Y5/wU/n4HNv5jRnhfhy1/fOfeT"
        b"c276y2xG2Dj5u2nbzzpkq5+Rtqtz5nOQ5rP83O93e4HQwUWjjNHAFAeAQAMg0IQPX81icgMEmvAd51WCQENfp+1A"
        b"sMwODJkhWGYHQDDFASDQAAg0gEADINAACDSAQAMg0AACDYBAAwg0AAINgEADCDQAAg0g0AAINAACDSDQAAg0gEAD"
        b"INAAAg2AQAMg0AACDYBAAwg0AAINgEADCDQAAg0g0AAINIBAAyDQAAg0gEADINAAAg2AQAMg0AACDYBAAwg0AAIN"
        b"gEADdOofVgY+3j+wb24AAAAASUVORK5CYII="
    ),
    "flow.png": (
        b"iVBORw0KGgoAAAANSUhEUgAAAeAAAAMgCAIAAAB0wSZfAAAygklEQVR42u3d27aiOrcG0FitXlEeEh/S/4Jd2Vkc"
        b"QoCAQXu/WG3WXIqI048wcuDxfr9DscfjEXZ5Pp/hE57P56deGmjQ6/Xquq56OJyUM3+3PqHv+61P6bru9XoJSqAp"
        b"Q1JXbAtWT7k/l7Vk/TUA390wf71etwxogF9okteNaQEN0GhTWkADNNqU/utQApzRlA6He+C0oAEaLXcIaIBwarlj"
        b"d0YLaICLyh0CGqC5gN6X0QIaILRZ6BDQAI0WOgQ0QKOFDgEN0GgjWkADNBrQZhICvy5dKXT3xL8zVrMT0MBPG9a4"
        b"PzIh+7z17gU08NPp3PJq9WrQQPjZykbjeyigAaVnAQ2gJR7UoAHCpQsbCWiA0yf77cjo5/N5RrIrcQAcSufz2t0C"
        b"GiDoJARAQAMIaACCURwAockRzcMoDoslAZyYzrsz2jA7gPA7c1sENEDQSQiAgAYQ0ABB72IwzA4gNNe5d/tbXp33"
        b"BgCOrI7U8kCOP24tAxDUoAEQ0AACGoBgFAdAPX3fh72diqM7gnddJ6ABwkfGL4zGaYwCuu/7MzJaiQNgc6ynd4kd"
        b"fjhjrJqABji6MOlJI4n/3OJM5Q8C+MGp3n/ucjXhjwAIrU5BPON2KqHlTsL0ImL473mrYgOU3NRq1GEYo+mkdPp7"
        b"l1azjAbqOjLu4rxQDo2XOJZqGmodQDCTsNmKs4wGBHS7/YEyGhDQ7Y7WkNGAgG53LJ2MBgR0uyOdZTTBDZkQ0M3O"
        b"Q5HRBPPTENDNzhKU0Xxr87nrOo3oYD3ou8/hXprDIru5dTrHuy1vXbYYLegKMwMrpqcsRiUaLeh2M1RGQ/jcnOnZ"
        b"S1htf+tBA20t7YaABoJRKAIaXMJ3j6qGDX5Hw1PzWUDDV2XQ14TaUn1Dn5CABoL6hoAGUN8IPzRRBbQH1TcQ0HCI"
        b"8bzOZwIafuta/tZBZvizgAatwpudtNQ3gk5CwJlMQAOobwhoQH2DoAYNYdtU729agnFo/x559aXmc2aDw1PEt4CG"
        b"e0zH+FQ6D+ebK1/99c/zH39UAhqYSckPzk+JT5TRQQ0aqJvO++obbreoBQ2h5ZmEJxWyN5U1Tp3evfVouOWKgIbw"
        b"2WLxUtP1smyqmM51j9KwY0rSAhqua6umt5mfTcbLOsoqljVq1Tdm97DvexktoOGKVmQL0XxeOtcN6PCv3CGjBTR8"
        b"LBYvHl52WVmjMJ3jeStfklbuENBwdYt1KDdfFj0lYyT2tViPNJ/Tyo8ReAIaPh/N1zecV8sau3fp4PL8w8PyTXsl"
        b"aQENlXvMPl5uLi9rnDGybdN7HHYgv59G4AloOCuadxcQzk7ng3tVq79xCN98S98IPAEN9+4J3DRa43g6V1y+Lj4l"
        b"n9HKHQIabtkTeEHR+dQpPCUlaSPwBDTcMprLi85V0vm89fwKS9K/We4Q0LAzCmNkrA4gO2m50bOLzifVN/aVpH+z"
        b"ES2gYU8UpqEck2XIkcI0OV5gXZ39cXa0GQwnoOFOS/iPIjucP38v81pDceB4kp76di4YfyKggfCpNfZOHQtxan3j"
        b"vEmPwYL9wMczuu/71TkdZyyQf7xVvrpXw7szzA7Ieb/fZ1zm14qeU8dCnPHGPzXpUUCDNfs/1pReHQux9b2cUd9Q"
        b"dBbQoCR94vS8I8vzf3BaTVCDBr6mJF2xviGdBTRQ1LdWktF16xur6TycWqRzUOIA5Y4rbz9oLJ0WNFBtjNo1c22M"
        b"pRPQ8LtKStKbMrpujVjRWUBDOD7h7VHVsMHLZoTvaKKecfduReegBg3hqpU3QpOrW1QpSZ+6hxrOWtDA5hF4q83n"
        b"KuuLSmcBDeycP129vhGfqKwRlDjgI/O8C+dSX1zf2JrRmeHPGs4CGkKDYyE2TcTIJFHJDV6bXVfk4O0F/CEJaAgt"
        b"9BN+PIVbmJ+CgIYmWp2jXMu0oNu/N+7Zw58JOgkBtx8U0EAw4hsBDahvCGgA9Q0BDahvIKAB9Y1gmB0E81mC+gYC"
        b"Gm4UZG3muPqGgAY5/lTfIKhBA+obWtAQfrx77QuCTBYLaPjaZmbhWhzNvgUBLaDh20YNp/+dDejhh/bjL/MWENBw"
        b"syHD+WEP8f8OP7S/XL04FtDwDa3mruv2Zbq7iiCg4WMN5yr3xAIBDXXSOZO208cPG3HjVAQ0nDuVI84JzN8/Zfrc"
        b"WJh2YBHQUDmdh2geJWz6mHTwxvP5HDXABTQCGuoPQct09GUCd3jK6/WKHYyx29DhJZjqDVWaz0eGYYyea32iYOq8"
        b"gIZ2ZtxpMgtoAQ1n1TfqRrxGNAIaGpr9HDcincOP3c9BCxogfMdMegENG75U2rzukHtl74VhdrD+1ar7ZTbh+1tX"
        b"hpodN3lk4qiAhkvX5p8O2nNUv2b96+mfR9d1R15LQEPRlzlO2u66bvddX9OJKtL5+0oc8dYNce5oOHaPYAEN26oc"
        b"Q8imzaKSZvXudUq53frXtdJZQMPmRnS6Il3JxfLSekkWtHMOENBwVlfh0BzO39Eqc0Ms6fwLt6mMJ3IBDed+5fq+"
        b"n9YoliLYHVr9wcTlsXZntHHQsC2jj6/FobgRfmnMz/P5HM7rO7olBTRsjtd9DaIjz+W+ZbHhZDx0LG/NaCUO2PPF"
        b"e7/fhbcojEVqreafLUbHcR1b/wYENByd7DC6T8qoB18uk/6dbPp7ENBQbTSVLCYsF6OHKocWNHzDytEtz7tzKtpR"
        b"jO77fmuVQ0DDKTODC2vTjb/T2erN0nWD1F79uLdOJRXQ4FZV4wHdJWejaXbHorykDu7qDZc5Yw2NdsZ1LE1G371Q"
        b"X+bG5whouM3i7h9PsdECexXvgy6mg3sSgtA/Es3nLbAXt+82NAIa2JyeF0TnZS8koCHoIQz370I8o6wR1or4MlpA"
        b"wyn6vn8v6/8pefzH1+K4Pp1ltIAGI/DaTWcZLaCBdtP5Rhn9er0e//WpfTbMDowbOTRYe+sA6uN3Rr9+2PuwjMaO"
        b"udoCGgyb2zCLpDyUC5MoveV54RTERjJ6djeW3sLSbp/6XpQ44NL4a3kyZLylwNYJJsPj43PvUugY7erqNPfZB5x6"
        b"phHQUL+2m0nDj1SBS9KwPF4LI/4W83QO7sapM30ENBxtNS99RVd/eeU06NUYqnubxMJJ3o1kdOwDLC/pxI7E4W/g"
        b"8XicFNNq0LA55pYKGumNM4Yvf/qdHz3rynTOR+EZN7GNN0vNlHTb6SqMN97OH6v0/44SOf24K74vAQ2lGVe4xPNq"
        b"jofG5uCcF5R9398oow8+LK4PpcQBbY3eHWqvsa/ss7FYXkm4oMyS2f4tTmCf7SsW0BCOd4ulSbea0Y2k8zVllsIz"
        b"lqGWQYkDqq+1P5txMZVGV8RNLZF85XkijpX+nT8MAQ0f+O5t6ut/v9/pHaF+cwbNqDR/r1mFn12VRUDDuY3NNgPI"
        b"vU5ucUWiBg2/eMfYi9/R158PhjdY/WJFQAPBAiZKHMCPpnB+sF2bjevR4JP8QGkTVeAGLUGF3aV25Y0GcsxWk4dJ"
        b"N4WDoIdwP/7HIKBh/5V4frDd0naE+O3SOc4SLDzH1GpNC2jYPME3fuumX9elYdHa17cuIu+4CKhSuhHQULNrKz+v"
        b"+jcje4iqu9Q3hl093ogOatBw01gffv6ROdCZk5Dh2MEwO/jlcdCzO39xe9bNvLWgIVww4mo1azKra7qAuPWgwOuX"
        b"3xPQULk1vXSnu4/UYZdetJE7t7Z2aRKPyejgDP/cdNuUWLA+8h4FNJzVWly9Cak76oYmR+xMR9oNUVv+LuIll2F2"
        b"0Fwul9x75eNLfXZd936/1TeWRjGnH9Bq23n0+FofroCGc29U2Ox60EHXa9VW/xlvR0DDuUWMOMfhU3k0Hb1bfcmI"
        b"kkv+2WP1Zeeq6mV9AQ1nFTFCM+N8R4l8/VqjYXLL8y9L55M6XQU0nFJcbip9WjhPpDe9/soiz2zvooCGD1ckl25R"
        b"2NRCmh/fGZV3AQ1XN0vz85j1yIUfW1SrbiNaQEOd0WPfnYCF6/ahBQ0fa35OFzyK/V2xhvCVySWOwyfuGyugYUMn"
        b"WyxGj1qUo7D+gqSenorykX33BI9z//JzUuKYxWsuKQQ07Ezqpc7D+MvbJXX5YJWlosdNz0xpyzezZMrz+Yz3shpu"
        b"Qnj2FCQBDRXus3f3pH79U2Wsy42SOg3WwoEucbzgMPvm9XpVr2wIaJDU1aI5M2uj2Yx+Pp8HlyK5YHS5gIazknq2"
        b"VJ1Oovvs/JEzonk2pu+y/MjqjQevP+UIaDjxez7K63Zu7z0qoV4wB/ou9/fK3Df2+PrOAhpaHC+8dUHh70jn0Sve"
        b"IqOHmnKYu5X79bMxBTRsjt1b39Sq67qP7OeQ0e2XO+LupaeTT+2zgIaiUPuaN/LBs0h86RuVpIO7egPhN249da/b"
        b"XwVTvSF8aT/hUsnyI02zfXXnzG2c0lvJtLB0soAGsbuhy6ipeuumGF1aQDW/Pkl56/iMpZMFNPyo2RkNN8qXwujc"
        b"N49mNEm6fKa4gBbQQFHzuUqTNl1LKP+iCh1BJyGwmpXDLJKKWTlscHWbegu1oIFLlzDOL6Kt0KEFDeGM4cM3bfFl"
        b"dvvsnrp821wLWgsaalYJSoY33CWdLxtkkll+CC1oqDyaeGhQ36VZnV+b7ZqAXlqFQ3BrQcOJNx+56d0Irx+jrR0t"
        b"oOHqcLnp3Qilc1DigPAtQx0Kx40NBZDH4/HZZYnuckpwiLSg4aJbW93lNldNNfCNtBPQUD+pQ9nqnfe9yTdBiQPC"
        b"VwwujjWQzLDfLtHCusxf+XJa0MCeWxGO+hV/ZEW3uPhq+/UWLWj48mb10Igewreka/FHGtGzryidtaDhA51vad9X"
        b"2oS8fm7L7BC3ixeTU+UQ0NDudX2m4vGpAciXrZqfOSdpQQto+Ng8w8Ybj7Em09qtthDQcFYuF96+pJFpkOftjHQW"
        b"0BBamOvxeDw2LYJxZUDnM/qk8SSr6dzUPRsFNPxiS7mFKSqrS2F0Xff85+BswPKDI50FNPxuLu/oysvv81JJZMcw"
        b"Fc1nAQ01w6u8stzg4ht935eUg2NMj/oPZ9/RkTEq0llAQ6h1y6s75nJ5JXqppZw+fimdb7EatYCG8INdhTe6A1Z+"
        b"yvWVk02WbrCCgIZquXyvZuDBgJbOAhravaPKF6wXWl6MPi+dFTcENFx029ObvpePLAmi9Cyg4ctvQVLx7VyW0d90"
        b"hhPQEH5kpf8PTl0Z6jZnN6U1nAU0hDsO2vt4o/LUmBbNAhpoK6ZjP6poFtBA5bGDo2mB5UtquCWugAauu2154V1X"
        b"hLKABgxfEdBAcFc9BDT8WFtS0COgIVy5mh0IaAjqG/yOPw4BgBY04AogGB8ioOHSm65evB1pKKCBUH3RjNfrdXGX"
        b"4/Uri26dDoOAhuB2t03tmAVIg05CAAEN6CEMBi8KaAABDYCABiAYxQHBHI3QRBna0RDQ0NyNSyAocQBGcWhBA1rx"
        b"wZKtAhq4Ux18qDVrMgtouNPFuHo0AhpavDz/ncUoNJ+DTkIAAQ2AgAaCIn5QgwbCjxSLTeET0BAMSpPOS43ozx7V"
        b"WzTqBTQYQfGLrfhbnHQFNASrFH2kufrBiGzzNmACGjSf/z+hronITBR+tgVd8QgMmxqNlx+m1MdZlDteTkCDEsfP"
        b"FXyf/9QtmPR9HzP6+XwOfcvD/xqOgICGj0VP/Dn9HjZb6+y6ru/7C3ZvKZ0/fmSqX0M8n8/3+z00lod0ju99+I2A"
        b"hutyeamUmf4yttQaTOp49X3evrVc7T3pXadt8+Hwdl2377UENOxJnPLQiQ+uflm9KS8+UokesunHV4lKP/1gJiGc"
        b"+mXrum5fk/DIc89rKp63S6unsV/I6OH8lDlHCmg4vT246Rt7/dL1+SgcdqluTK+ejX6kBZ1Wt3a8ZSUOOJTO+UvX"
        b"2VbksKmLp4+nAwwyRfMquVnlTPZNAb378Apo2Jk46SCq1e/nKKmvHIa8qSKx1KU5HSW29JuSAv01o0ea6oYdRnFs"
        b"/dAFNGweKLa1uy+WINOU3zcw9khTLt+IHsV0GiWzbzb+JuayVesyJQ4TVeCKgI4TEA5G5Eda0IVdVaO0TZN6eky2"
        b"hvLvNJ9nCx1a0NBcOreQ0aN66I4jcLyB/JGBhu0UOoJRHNDy1IZRQl1cEzh4grFwa62J4AIaGl1HYlS9vT4sPpXR"
        b"P1jcCG55BVf2DX5Hg+76jJbOAhosIrwhoy9LTOkcrAcN542R+r61N6+ptHxqBRItaPjdReyqNMM/HltDO/qk5u2p"
        b"G9eCBormcRysazeyen08c9QaSyeXBTRcvVznkXXuR+sHNRVhMVLTNn55WB9cFQgBDXUm4A3rr29qJE6X42i2jZkm"
        b"dX7I9mj/5bKAho/VakcraWSWFipZP6jlOEvfmvwV0HCzQsf0binThnamPtB415ksvvhmhgIaQpUllTM3ISys2BrY"
        b"YMZ/MMwOzsjoI/F68fQQWrvtmRY0XLrCr5FnPyVG87AA/9kfqICG/Ve4owU8Z4fQGXn2BaXk4ZGjhnMccHleSVpA"
        b"Q52YDifc3O/LJpe31hu5KZ1nL5jOzmgBDd8//kH7veSkNXuUZtvOsxmtBQ181SJ8n63Lj5bPn83ZfDqfndECGn7i"
        b"ltIuOMoPV7pXhQM2Tspow+wAitZOKR/goQUNH7sW/o4LfKqvK1u9HS2g4WOjIKTz952V62a0EgdAzVNyxestLWgI"
        b"13SCfc39DH9hadlGPiwBDaFkCY5vnSrC7FiO0eqyF/+1CGi4olg8XaffmnY3XQH8I/cvV4OGU2qXw5pns+O0+r5/"
        b"v9/S+RYZ/cF01oKGsyqYs63mdta027Ebs83J8gg7aahiO+3oMy6JBDRUnlTdeDTvq9tkaugl27lvCb4wo031hhus"
        b"424l6B/sM7RYEtyy4awn8O4dwnF1jqWMPvUjFtDwKzUN9nUJxlsuHBl7J6BBNLOzsVzS2znN6LOvkAQ0KDf/aDrv"
        b"+KRGDW33JATRzOkLbpR/dld+ygIaDtU0RLO1k3QSQmht4faYy0NHvxVHw82XssrckzD/MbmrN7TYgEqXdd+R0RVX"
        b"1eHgrRozQzhWF7c773MU0GCBOp/g/81EH0VtZqzOdBb7GTFtsSSA/6xylf635DQ8POyMIdICGoJKMW1eVylxQGiw"
        b"WFzllBD7MFvYJSc5AQ2/O4fi1K0d3IiRiAIavvBKuUquzY4RvH4jVXZDQANfVfWuWDBR5biSTkIAAQ2AgAYQ0AAI"
        b"aAABDUBoYKSKYXbhyNLdAPFOK9XXHRXQQhn4z+reo/+WLK9Rd1a9gJ5Zz/eCww2EJpdYmf2yD6ldHtDBTMIL7sqc"
        b"Rnb5XXuHrV2wqs5lLwS/c9Gcv6NKMNW7hVt/hrmluFdvOjek+RmrwX7qheBHciB+r5e+4J+9jP4jnQsfn2lrxw2e"
        b"+lle9kKg5ylYLOkW6Zy/0jnpNgoVdxsIVrO79f0ORl2Cs7Xp4ZfTupXb3wEC+qykG3rb0uQd+m2nLdbC7oLLehU+"
        b"230BCOjT03lpeE3f96OMLmzGrobm0na2pu2OFxLoIKDv1407bY1mRm7kOwwz43gy9wme7U3e90KZ11odkQII6NBI"
        b"p+1QyljKrMxY46Uuu/j70Tbzw65HNe70iVtfKP9a8VXENAjo28xYGU30nG3A7k601XSeTkI58lqr4z2OvwogoOv3"
        b"jC1N3IwBmiZ1rfwqTOfj73HTaDx9jCCgKy+aMfwwHXpxMKDzSX2knDKbzmnxZGt8Z+o2s72CS3syO3AQCNaD3iGd"
        b"zhd/3hptw/CM8tboYFrreL/f7/d72q/4/mc0bm86dCSalhriy216odkuwfS1pi9k8gsI6LNKBPsagOUZvbWCnHm5"
        b"1HSfDzZj82vyhbVuUl8DENCVhzAfLAts6iLLL8dRvtps+YiLTa+VWSlx9ZcCGoIadGhyfe5NreMqFdv4WvtKNJsu"
        b"Mso3rhgNAvpQg3dUMI0Je3BQR5yosprUB3vVDpZKTh06Ip1BiaPaNJODQyxmxzj3ff9+v2OvWsVFi2J/o3oC8IUB"
        b"Hbva0h/OWAo27dOrtbZcvjH72Ul9VzbqgfCtNeh0vt+RqRzTrZXXVWol4AWddeW5r74BArpOiWM1WMtn2b1er/f7"
        b"3cICpyctOyd5IShx3OIuNUt3hDx1qNnqenJVdmD2pPVKTGdjqmyAgG493IeOu1FcrhZn8yeJ8kF7cer57r7H2TvC"
        b"LBU64o0Ihnd9fHA3IKDPbX3HtEqrKEttzNVoHuI+k7mzr7U15UteaPTWRq+lEQ1BDbrNySmzayvPtqPz3W7TrQ2r"
        b"S6drLs8+Jg3ofWs8jV5oqVcz/1pWhQYB3VZGZ9q2Vcrf06Lzjjbyvu7HpTNQrZtsAUocp4+n3vHEzN0LVwvEq6+Y"
        b"WdCu/IW2Noot2A8CutGMLs+mzOMz944azXtcyuiljU/vOljyQqMZPbWOAKDE0dxKSSX37ks3lV9b7v1+Tx82e6/Y"
        b"Iy80rXVMHy+a4RYem2ZqPB6PHfWBrutabq/lA9qfCITvugfpBxPp8dgWuW4aWzOF0/FzOx42qmkcf6HZ4dKAEoes"
        b"DzvWaTrjpCKXIegkBEBAAwhoAAQ0AAIaQEADEAyzC4fmpADhhpMPtKABENAACGgAAQ2AgAYQ0AAIaAABDYCABkBA"
        b"AwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIaAAENgIAG+JSu6/q+3/SUv44awKler5cW"
        b"NECL6fx8PoeMfj6fAhqgFbvTWUADnN6CHhrRAhqg6Xa0gAZoqPk8DN7QggZoMZ2DURwAjQyqi6XnYKIKQGip3Ly7"
        b"Y1BAA5zVfH48HlXSOZhJCFC3srG7S1BAA1SeJRgrzkMuV4lmAQ0QDpabu66LP1eMZgENcHQUXRrNx4dtCGiAo+vS"
        b"dV33/CdGsxY0wOmrgI6iNj4yjp/r+z59TPVo/sWAPukgAt8XCGkop085MjNQQAOEwlucFD7yylAW0EDQv5dvQc9W"
        b"OS6+ChfQwI+OXy4scZw0hE5AA+QayJl2dAtdVtbiAH53CEfjAwcENICABkBAAwhoAAQ0gIAGQEADIKABBDQAwVRv"
        b"CPdZcdhqtwhoCJYgR0ADuYbz9IYdn1oUjaAGHW6yRPejQPdP5qY4TcXB6H3dYrdHbyHzWez7QAsPwnQLRz734bOI"
        b"fzwjw2vd7tNBC7rR0mFcN7bxhs8Xf+fzb+3gG483Zp4uFrxvUyX7M7rfKGhBH22favU0mNHnfShbt1yezv6oENCn"
        b"1EZ8nb7yvkfHA3prOvujQkD/dEZ/2dd+qc/t+NvMbGFTc3j2wUMRo+/7vu+XqhkCmqAGHTber3fpK9d1XebL1tq7"
        b"+PqbXxwvQIe129btS+dpifn5fM42tEvuXoqADgarjn6z+7p19uva2mDbpRZfs+9xmmLVm89936cjRgqjsySd099P"
        b"r8MENAJ6T+otfZ2W8iheiY+eEr+uJRGT+a4uxeKm7cTdm+5k+a2Ol97jlTE9u/+70zl+QOnvV6Mz03zO/F1pRCOg"
        b"q8V0YXsn0+JOv4Gj544G+Wa+20O//9KDC7cz3cg0efMF09X3WCumZ7OyYootnURHL5r5uGdPCas7OTwgPlEuE3QS"
        b"HmxHVxk1NX3MdOObxhXkm2lhroCen/SR7wvd9x5r1W1GR2Zf9anW0zMHv+SvJfYcDufCNns1END3GJ+w2jeVaZau"
        b"xl/hN/P4pOFNkTRb2Cl/j7U+o0wd6fjRmH2h2VNm9ZR//pcY4vYBHWfKxsmy7YxPmk3PtIm0aYWzwhZ0pvpcWNko"
        b"38mt7/GCT2cpYSvWsna8F2nL77ag02Zd/PlTMZ3OBV/qLkuHwWa+8/n/m0/t3Q3wGKxxJzMhO/se808vb25vqnJU"
        b"CcHZt7PjlAkCOteKabPve3rdunUnZ3v591XGy4vXo5BK/1myhQtyLR1/crAAvVTf2NoxoBGNgA4nzSKrsjOF19qZ"
        b"yuamumeVxF9K2MKeq8wg37ofUOHb3FTJXRoY99kLMgiG2VXvNtw04iIf65nBfNVnhWwagbCp5FL9Kmd2sF3dGE2H"
        b"P86Oht70Loxo5ucCemjQzQ71be37UKt/LL6v6QY/Pqv7ykv+2aw8MgFyqVZW8sSSWYXSmR9tQY+G98/O+2inEb2p"
        b"qTU9A5ldljloFQvQobg/s+LHYZYK4ctq0OmqYPnlwb5sTbh93YNfczGxWtreWoCuO5hy32cRp/PEu65IIm7fgk4n"
        b"+17Tulwaazxdpez4l3Y0A3hpDEYL6Vz+Hs/Y27ohe3DBpt2PGf3XZEK+ocRxxpoMR5qBS6sxnFdvrVsoWBq8PBp5"
        b"9tnBZPmaxjXN56Xw3bHykfYy3zyK4+xG2epYsXwrPg309GFVpnfXbWdlRi7HKSHR0joYB9/jvRYJmIbv9OBMFw0f"
        b"DciZndKp+UywWFL5wghxZnmmgbzUSzlq4w9f4PROz0vLCZ30Rc3PvJj+sPROM5tN32Pm0J0xLrD8bDctFr3XlMy+"
        b"WVqXKr5iOhpntkNSOmMcdMjMIN+0pP3S6v6jLqC0oT07Anop9TKzurd+k0cBOtvKizu5aXL28PRR+pw0ROH4sI0d"
        b"lah4ll295/fSw4a/gczgd81nBHTlK9+lKc6ZQuTs9pfGMi992w/m3dKVeKYjNL1Inx2Hnn96rdzJBGX52p478n3p"
        b"3DZb11o6CCUzQqUzShyh1n3/Vi/2SzoY8zNNTvrGbtrJ2eVENr3H1nJn32CYwvVO9y0carlRBHTNUdiZ71J5993q"
        b"IzedA86Ig6WHle9Dxc7MTB384B0Ud2f00ilt07uWzgjoyhNkVlMp/7Dy7/CRMMqXO/M7mX9AyaE46f4gR0b7HZwJ"
        b"MhujSxss+VO5cqYVQQ36K0fprQ4EXi31TsecbWpebW3ulS9wOruT5XuYefrxQvnBk1Zhjm9tum46X44q5nUPEb/m"
        b"8X6/Nzz68dixUs9oWChA+FxvROzf/vi6Y1rQO4dtVLltx5FNHZzYsvUpB3ey1oCNTXcAKH/A8enyu7dgXSS0oAG+"
        b"sAWtkxBAQAMgoAEENAACGkBAAxCMgw53W7IdCE3edkMLGgABDSCgHQIAAQ2AgAYQ0AAIaAABDYCABkBAAwhoAAQ0"
        b"gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIaAAENgIAGENAACGgAAQ2AgAYQ0AAIaAAENICABkBA"
        b"AwhoAAQ0AAIaQEADIKABBDQAAhrg1/39qXf7fD595IAWNAACGkBAAyCgAQQ0AAIaAAENIKABENAAAhoAAQ2AgAYQ"
        b"0AAIaAABDYCABkBAAwjo9nVd9/ivruscFnZ7vV6jv6jX6+WwIKD3fJemX57ZXwII6KsD2kEABPQ9ms+CGxDQd81u"
        b"AAH94fqGgEbFjE/567s0+jr1fZ+O3xge8Hw+j39FN21kuoXLnr6UL1du4VMHecdOHvykTtoUAvoLHf8+xMQffdni"
        b"lldf4vXPdN+G5+a3MPv05/M5nGZWn7tU2CnfwlJdqPwIHDnIJTuZeaflW1jaSMlnVP6pielf995iaGBuNTzr3aTR"
        b"0Rj2c/R9eD6fhftf8kXKbKrv+9Ut5Hdm9en5Vy88hx15+8f/GEr2M/8SJVtY/dDzH9bw9JK9KvnQm/363FH8XDJ/"
        b"ye34o1a42o4uLCl2XVfyyKWHvV6vki0sPazw6V3XzU7AGZ5eeNBmH1n49jc9snz/y1+icAuZS4GSo114PPOvUuWI"
        b"EXQSfkdAZy5s636Fpg/eOlzkyLSa6SPL0zmzhU37v2+W5qZXWTqNlW/hgvGX5fsjo9Wgf717cEjnWIJM/2++qzBf"
        b"Ml5KtHRrs1tIr5FHiRb3J/5309O7rhuurJfe1OhcVbL/mVefTeStXa+zZ5GtB3nHFoZjdfDjLv+zia81uzPq0WrQ"
        b"rdega20qXyIsLCAu1V6nD848ZrYkOtrC9DGxSDpbxFx9enzubM199T2OHrP69mf3f9PndfAgz/7f6T6sfhYlR3up"
        b"HJ8e8yOfGmrQ4YsHWmytb+Svamdb4rNZUP5a02/v6Cn5KvnoCmB2WELmmiDTQhyddzddnQxvqnAL+8afZQ7y0i6V"
        b"dO7NtmTLP+7CNxWvaTJbVuVQ4giNrzk3ewVdq76xlHGbBkQvPSbd53x9YGmzmYye7sBokNb07aQPGO1D13XpRp7/"
        b"ZF5x6VilowOPnFxLMnoUr/mDvLXAsvT4TI1oR55O/w6FsoC+R8k4LSA+Ho+S8UlH5npNvxs7ZqzsiIOlIDs+BWPH"
        b"IYrbyY/Cns2RdAtVMrrkaEx/v/VTmz03p/Xl8u1kxoMvjeQxR5H7BfTScqD7Kh6Z7sFNX4/YQffZmcHTp28dI1HS"
        b"3IsHbWiirl5wLIX1amP8mppYg11t5cMc9RMK6BuMWa74l7ppjNpXfj2GCe6F47iXquSFJ7mPxPTWTD+1raohTDAO"
        b"+oyvxxd/tYaOu8LQnKZ57AAs7B9r+UgKULSgjzZq9rW/DkbDqPurzXTY3YOaVir2HajyLexbhWrf8TxemL6ghX6w"
        b"3xsB/eGhdZkVfC5uXo1GU2ydlZAfX7F1C7NPP9J9Ot2rpT6ApeAr3MLxT2G6D7GSe9JKQ8erH5nJQfKIGw+z6/s+"
        b"rWDu+7M+fivY1aZfZnxx+G/35lJAT6fAjU5RaX/d6m7k43u0zdfrNZ1kOPxz6dClozVGHYmFW6jYAbj7IKehv2mM"
        b"/OrHvWmMUPqpTYdFC6ygBt1sI3o0d27f+I0d89nyL7Q0B2T1W5r/zk9PBluXoZjOXB/WCYoL/cQNxt+npYlRVOUX"
        b"KhltMH31Km3nwoO86UpiuoWlSfOz3aGre7L1XaejkuIB7P4pXAyLYKr3fZcbLZmkO51WnplmXT4/OH/kl+ZcZKYX"
        b"p6eW/B4uddzFB+RffXUHlt7+jhnSW9cIPf4ppPu5epxXp3HnlzMdvd+DHzq/MNX7rxsM7pgNMb2qzUzGm33R0Xd4"
        b"9oI333YuWTg/vwPp4vSZV1/dgdktDNWMzBa2XgOtvspst1vJx5QfIzibkrNjz7de6FT/0NGCvnEL+sh6PattmU1d"
        b"8LOvu2kLJasRbdqBrUMICpcHqrsI/aa5o8cPcmYn9424OPipWSnJYkm/Nfx507d9da2l8juSzD6yfAtLF79HdqD8"
        b"6ZkdKD+e+6bpl09vyUyXL3/pzCNLDlfJrh780Ak6CX+2vrFjPbx8QzJO5cg/YHUL+dTYvQMl4ZV5TOFElU0RueNV"
        b"jj+g5KNcfSPly/Ud/ND5bo/pYr65Rz8eOy7u4vLwrS3Pv3X5ocItTPv0t05smd4RddMWqjx9uv/Hd6BuFXW6nNO+"
        b"JaWObGFpTajZv5nV4XpHPjW2Lru26apRQAMI6PCjt7w6PlN86xamLdB9r3h8VdXd0+Kr7P+pzcBGdnLpk9ox08St"
        b"rdCCBrSge52EAAhoAAENgIAGENAACGgAgnHQwb3mILR4jyS0oAEENAACGkBAAyCgARDQAAIaAAENIKABENAAAhoA"
        b"AQ2AgAYQ0AAIaAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIaAAENgIAG"
        b"ENAACGgAAQ2AgAYQ0AAIaAAENICABqCmvz/1bp/Pp48c0IIGQEADCGgABDSAgAZAQAMgoAEENAACGkBAAyCgARDQ"
        b"AAIaAAENIKABENAACGgAAd2Oruse//V6vTY9peu60QNer9fWbW5y9vYBAd2o42EnLgEBfVZAH0xYtzoEBHQ4r+6h"
        b"FQwI6C8sdAh34Ax/HYK00LGvWPF8PkdPVPQABHTljN4d0FUa3Z+K9dHOlO/G0qXDvjdSshsVd9VJFAH9E43oTWn7"
        b"+mfp8VXSbbTZpZeb3ZnnPyU9q0vvfWkLs3tSshtHdnW2Kzg+UVIjoMNdegvf7/fxcSB935dH8/T0sDUyXq/XdHT2"
        b"KLlGD3i/37PPinvS933mHDP7xOl7mR6H0RP7vi/ZjSO7unTMjxxwCDoJ79JbWPL1zqfzKPsK9yG2DWfTOUbb7A6v"
        b"huzSbqw+MT9+cXqsSnbjyK7mD+amAw4C+tIhE9ML5JO+rptGWxfuQywOzKZzvpJbErLTLZenc+EbKdnaBbsqo1Hi"
        b"qJDLMY+GAKpyZTptZu7uLdyUzunl//QBJfuwVJadLbCsnp9m92G0G7Mng9ED9l2CZHZjesRmH7NpV/cdcBDQRS2p"
        b"ruuG79vx79WQaOnGYzDV+tJOm3LTsulqOJbk/mqPWSbKn89nviGZb6rvvsSZ7sbj8ZhN57QfdbSr03TOdydOizxH"
        b"xlnCT5c4Mv08tb5Rs3FZZeOrrc7ZkCpsPq9uuTAWS4rpw1NS08dvOkMsvejSZjPjRkpGsxirjhb0daXn6uk8apHV"
        b"2n75CNxRRu+omWxqPldfeGS25FLlMKZjLeJ/yxv7Szsw2ogWNAK6UWkbLdYlNkXewQb+phc60nY+o2Ngd+dt9X3O"
        b"BPfSEGxT9hHQoW6ZOI3Uiu3o+3YcXVlCXZr6EVpdC7DWrkJQgy75Jp8xDWzaCL3XF/uaXR361srHpdUaaXPNoZDj"
        b"COj9jeih5rDUQ3VGENwroM/e29XBxWq4EH6zBj1cwscOvZMCejrkruWT1pU1maUTwGj4WguTPkZH5iMFevitgE6j"
        b"+bzv27S38Pr2b8nCSfFcctLgk8LREVUmqlzQTyigUeK4uhLd+EtsrZLHYWpDkbdkFPPWpS3OOJk1damRWRcpPXmk"
        b"/Zy6EBHQ9xtyFy65w9b0h02nkCpz+SoOIGkk6Wb7EmZnEsYOT8txIKB/sZ0+G/ex1RaT4uCk7Y8s/ROjeeldXB/Z"
        b"S9Wh0e6NWs3a0QQ16HsF9HTkdd3evHyrc2s6f2QEd4Nt5/wxye9t+SJToAX9VY3ozBL++YWBDo7grpibmZukNNj2"
        b"3Lq30hkBfTMVv7Tlq4DuG+K9NIK7bjt6tfAyfZsfjO/yI3nSsHoQ0J/vLSyfU5cPgtUHbFqL44xkzN8DcJhA1NRU"
        b"vdU5TeXHHIIa9MWFi9VvZuFimPsGWY8GPudzZPUVV9u2VQo7syt/jtaZG+40uJSYoykk5+1qfqlSdyOkfY9N90h9"
        b"PB47rvqPLwsHEKouV7Dp3kNa0J+Zy7CjnrDU9bSjcVdeJi7cfuZhx7ewaf8zB7nk+G99zNbDqLmAFrQWNKAFHXQS"
        b"AgSjOAAQ0AACGgABDYCABghmEga3VQVCO7fd0IIGQEADCGgABDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIaAAEN"
        b"IKABENAACGgAAQ2AgAYQ0AAIaAAENICABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEQ0AACGgABDSCgARDQ"
        b"AAhoAAENgIAGENAACGiAn/P3p97t8/n0kQNa0AAIaAABDYCABhDQAAhoAAQ0gIAGQEADCGgABDQAAhpAQAMgoAEE"
        b"NAACGgABDSCgARDQAAIaAAENIKABENAACGgAAQ2AgAYQ0AB8xN+b7vfr9Xq9Xs/n8/l8pr/p+z79X13Xpc8aHjx6"
        b"Yvr09JHP53P0Kkv/HH4ePXe0w8OepM9N92T21eNLxFeZvtboKcOr9H2/+tbSR8YHjJ649NyS38dNZTYOfG0LepRT"
        b"6T+Xfh6iZBQuaQ6O/jkNxNFzY84uPSDz+67rRq84+5S4G6sbfCXSX47OUksvNH2VpecuHa7Zf2aOCfCdLehyz+cz"
        b"bbtl0rPv+5jIscGb5leaQcM/08by8MMQu9O8S08Ms4G71ICNezW6DhheKH1K13XpJUJ8I+kRmL79uJ3pJcXSc/OH"
        b"a+k8unSmAdSgF9vg08JFLDtMQyf9Z4yezOPTR46eO9tiLWlszl4fZJ6VvtCo/LKUzpnnTotL0ypNPBr5ExLw6wE9"
        b"tO8GmUbcqCE8W9xIHzaNntnwGgVW5rlxV0dJF/c8/eXSOx1l5dLlwmxDeOt1yeo/lTVAQF9RJBmF41L0ZErGo4b2"
        b"bH1jqCeklZD4lBjTmdh9Jo6HY5UtaEFDUIM+WIOeJt00nac9crPjQEoapF3XjcrN6VP6vo+N/bTwEgN6tjaS1oLz"
        b"73FaNJ/d54MpP7T9Zwe0AL/Vgt4XJWlUTdvI0/+bVj9GWxjCMZ/OR3rJYuO6ZOPTt7B0rOKQu/IDONtC1wEIWtDz"
        b"TbyYR4UjbWdHLsdGa2yNjtI2zaDpUN90BMXoJab12WnGxUdONzWqbmfSOX37j8cjvoV45kgHX49OMKPHxJ2cPjdu"
        b"M93n+Pt0n4f9qVJvAQF9s3SOsz/yg4UzBYFRYo6GqZWXktPRIGlBefjN+/3O9KeNitdpPqbD1+IpYWnsx+iUMMr0"
        b"6Qi86elqOu5i6bnp4cocfG1qOOgxio+VRz8eO+aDrV7716pszDY8p0kxbdDNtqkz4+RW+wxLWtPT/ZytnOQH+eU3"
        b"Prt7s0/ZvQNLj1/aGQgNDOua9k4JaN9PQEAHw+wAglEcAAhoAAENgIAGQEADCGgABDRAMNU7nHp3QZ8EEIqX6xLQ"
        b"V0Tz7B0CAVYXSvuFmP7z8QWPAKRHoyUOa7oDtBvQPgaAYBQHgIAGQEADCGgABDSAgAZAQAMQbjQOGggFiyKU3N5+"
        b"9nbsq1MN8jdon70f/OzjS+Y0TB9W+O5+c8KEu3oD7uqtBQ3sXe5xtCJCjJjpcmN9308XIEufPjw3ZtPSg4eHlbSg"
        b"4z5kdnL0QqP9Sf85PGzYvdG+/eCyEAIabpDRo4iMV/3pz6NMjxEcgzJ9biwszD44PmBajkgfPLRGY5gu7WR8ZNzg"
        b"8PPoXDLdw+kWfu1aXEBDuPtybvHn9If4c9/3XdfF1X1j3mUePPxzNqBHv8yvFbyUrekuTSvRaVM9ngyGRv2PrDIa"
        b"jOKAe2Vx2q6ctpeHEJyNy/jLtBCxtA77KDS7f1YXbc/v5PSMMuxDpngyu4VfWz5eCxpuUOKYVgNG9dyhgdl13dDt"
        b"H7vC4tPjU6Yt0NkHLwV3+uBRDXppJ0siNX1HaEHDvQsaMW1j+E7bm4MYuMNThhyfjq5LH5xuPJrdgenvZ3cyZMf2"
        b"WXZYCxq+pLcwFojTXrtRC3S1fy+WdLeOjohRHosq0xca7eRs8WQaytO3EC8IMv2WAhpoYq5KHCGXFnnjAInYuVc+"
        b"3SNfgsj8Pja34yiOzE5OHxlHdEznyKRdlOk/RycYAQ00VN+ITdfRL2MUxlLGUj13lG7DE2czPR28PC03j4Z/pA3b"
        b"2Z1M9zO+9PQxo7Z8LKzPPiuYSWgmIWAmoRY0UKc2XX12TN1+vB27+strcQhoCN80xiO0fTfnHZv95Ytvw+wABDQA"
        b"AhpAQAMgoAEENAACGgABDSCgAQgfmUk4vZUkAGf4H1y6fRcBf9FVAAAAAElFTkSuQmCC"
    ),
    "config.png": (
        b"iVBORw0KGgoAAAANSUhEUgAAAeAAAAMgCAIAAAB0wSZfAAAjiklEQVR42u3dW5biuLYFUFEjumg30jSS+6FTui4/"
        b"hC2/ZDznR42sSCAckLEQW1vS6/P5hMVer1co0jRNuELTNFd9a6BC7/e7bdv4567r3u/3LjlzUMr9rb1D13Vr79K2"
        b"7fv9FpRAJWKO7ZLO6XFiyjVNs2Pc/YWzRrL+TQD12Pfj9ftf+8bdn9cJCE8td+wb97F+0jRNQaVBQAMc9ck+VjZi"
        b"NL9er67rtj++gAYI+04Vdl0Xh9IbCyn/eFoBdg/rNA+5pZAioAEOzOjYxiagAUJVk5CxEi2gAaobRMeMjuPogr4R"
        b"AQ1w+MxhLEavnTAU0ABn1KMLJgwFNEA4uhhdVokW0AAnFaPXZrSFKgAnFaPTRnoCGiCcuTvH7rvCCWhALv9vv9At"
        b"Ab37XqMCGjB3915beTiNSUIgPHnurtp0FtCA46+CgAZAQAMsO6Sq8os0SQhoqgvbu+WOONtbQAP8p1WunkOuBTTA"
        b"sLUjVLBKRUADDPecq2cEbZIQIOjiAEBAA4RQSSk5qEEDhG1dd6/XKx4haJIQoDrFi7+PmGNU4gAIatAACGgAAQ2A"
        b"gAZ4Fl0cQNDyvNej3XI3u6qWtwNUtWvdxQEtnYFwk/2gLVQBsKpbQANsHkGP0zzd/bigF9CAEXSlA3ABDTg0dvWk"
        b"Yv/ux803CmhAiWPFaVjxv/09leIXi7fBCxaqANQzHhfQAGePx/eN6X80kwPUuZLwHwt+ADa2cMSY2r3K8XeLt6P4"
        b"3yNKPADF6RxDKU0P7j6U/LvLqFlGA/uGTEHfRcql8QgyPKTNbq6mIaMBC1XqrTjLaAgVtwl70n45oJfMB8posJeQ"
        b"gK63W0NGQ4UrLzRc/WxAr31pZTQcp23bgl+u9/vddZ2MDj/WB132xuvtGiXg2lYtH7TiWUDfch2KjCYoAXtTCUoc"
        b"ta4SVOvgh0vAlwxBBr9NXy/Ab99vBvRe//jmMtr4mvumc9zN8rh9LHf8PS0rWBPqKXFMrgzcMT1lMSrRSjFG0PVm"
        b"qIyGGvY1jqN+z6QTVeDK8eza4uzlsVVwyOkR1xwvQ4gLaDikNBx6G5jlh6KDQL/qc17aSz6d2LR2XVjB9GbmGq59"
        b"NgQ0PLocPDlvFrPpkqUc/beKFJQpH9M0+1x9I1+1GG+FPBgjTz7yhc+GgIbw2x3KmVjJl3Hbtj05lTKx2x/M9k9B"
        b"3XhKSL9HsLZnI+jigN+ePcun8yDpxml+ZmPGkkm/8TXvWBFa8t396xLQcMEsYtcz+Mhff6Pe8v7rLdVkq8MFNFww"
        b"XO3H1lVrAsfD+SUlhfSOsnwicfAmtOpmAlpAw6lj1XEM9fMuzdSdPHaO1zAe1BdH88KYTm8Mk80bBtHBJCGcPHy+"
        b"dvnGOPX60dn/Q39Ob/tFprnBtm0HjSL9Bo984wcCGkpyp5+2/VgZDJ9rawqcDN+Unru/fzRN8/l88oeuCmgBDYdv"
        b"NZfpIM4v9zguj8bX87U6vCTrxx8RNu4VPMhoy8QFNJSPClOgxM/vC6vPqxr1jpgbLO41Ttc8ue5m44LAQUDbx0NA"
        b"w6aA7rouZd/kkLmGfNlrwm1hF3Nx/XrwfBpEB10ccNzumjXsL5GfG9x3jcng9gWrXa5dxSOg4QcH0ZNzgF/TOc6b"
        b"LekXPmhu86B03rgiUUArcUDYvUWhbDfRS5arLP+mcyE7nhKcnBeNd6+hiUVAg1pHuEXDycIx+1wvytzak8w2dcu/"
        b"nSFzUOKAJ1teIB5/LMg0pcwVfJbPLk6udfR6CWi48bFSX6vkk/vl53NzsnU6U8LuLzlZW9OYu5jLT8gV0PD0aE7Z"
        b"dFBMz01XLsnoyRaLr6PacbDOfaNMv8fc7GtQgwZO6E0+YtvlrxtiLNwjf8nS8IM+PTj+yggarjzJsKxNeJdyxzlT"
        b"oFvWE0pnAQ2XRfNcVeGEVFqY0ZmdrPftaB5vwerIq6DEAefXmucS6uQDCQvWqmhVFNDwrFrzJZ/lvx7bevnTJaMF"
        b"NJy0A1E90WwELaAhPGq5R9m82YUxVDaCPi3N7dMfTBLCVXsq1bC53ZL3lV12lVuyOcl4XXjZxkwCGrj3J/ctvX0F"
        b"g+4ld5l8ZmS0gIazkzHmziXRk19LveT8rbVXvnCdy1zbX74fUUAD37cYzRtkX0rJk2O6IJ0nI3X5kvRVRyBmdgux"
        b"uZ2AhjNKz+O4PGeEOFd0XrLTxTg04zV/PVJ28B2/Vt4zu4UIaAENF8T014WFJ+9vt3ARTeaa53Y+Wvi9Jt8zBHTQ"
        b"ZgfnzBM2TTPIr7Sf/Tk7t61twY63zOzBn24wl6Srlm6Pz41FQMN5GR2DeDKDzllHF1uhl5/IFd9UJo+z+jrCtbGG"
        b"EgfcLKbTcbHhol1B1oZmWc6W3avsaEcBDRxVCz70RJW5Zoy1abs8cIs3pVvV/hGUOIAT9tE/NIzGO2+U1VLS1c4V"
        b"N1JVuuwHKWj/ENDAvdcZjmfeygodg5hesrxl42JF6Syg4XFD9fwgesmIvri4nPmmg4A2wSigIey16ejXNLm2ujoO"
        b"6JjR/aROtYv4h70isr8mcLClX7oGpWcBDUct0vvakjFeuHzyrtDjQXT/uNjJddVt226/yEFlefDGMHhvUH0W0HDq"
        b"nv1zjRMxqs78ID85W5hfZpLytCAxM5tppO+b+qylc9BmB+e0si3fUOLMpd7j9YoLtwRZuyp9+e0ntwqRzgIadqir"
        b"fg2UJa1jZ243sWVwuvw6t2xyZG5QQMM1s4hdT7/8enJGr93aad9Now56/whq0EDxurh++hy9gHDthkTjNSapuWJh"
        b"c97X3frTHWNGT74tSWcBDRcMn8dj0n5bxbjj7YSMHpRoxoWXsneR8e0Ho+b07QYrEg2fBTRcNnw+f+O6ULogML+i"
        b"ZNWVf13tcuY7U1CDhvCwzo0UxP1QHgyff2OV+UE1GeksoOHwwXIaln7tMNt9I4sKuz6Eb1DigAvDK6VwXHS3sPoc"
        b"1jTq3WuRzngtDAIawuXtEJPB9HvjR+dRBSUO+IHNQk/ebeOmu6FiBA3H9kJMrlfOp3M8+Cq/CedvL4JHQMMZMZSi"
        b"du3As/782nLStnQW0KAUcOrCFsNnAQ0oViCgIVzWEZFq0NUuZgmlq1QEuoCGcNO1LeP8qnzFs8AN2uwAENAAAhoA"
        b"AQ1BTx7BJCEE+/GDgIb60nmwg11BF4eIR0BDjYNo6UxQgwYwggZufy7M5AGyWz4imA4V0BAu2T9o34NlLy+p91O1"
        b"LKnTQd2DA3N3zH0BDZzRKldtGTom7Kp3oPizTO5KOjizUUwHNWjQonfa9cQI/rpn9JLjdB++H4uABr5XWubOup27"
        b"+/LYldHp04aABi7I9zvWds65qjhwLmuiF9DAiu35y+Y565kdPX/9fVqgVFCON0kIl2XBVbNn46xcns5lZxXWtvn1"
        b"+e8WZZOlAhrOc/kpKhtTMpNr/b66yfFyv+26koDeMab7P/7gPWxLg6aABraWKcYTjLHq+sAunfFZ71veldWgISi/"
        b"bBk+T6bz5Cf6n+/l2DedjaDhsqplVQXZrxczN3zOlFYfvnvfLktPBTSE5f28+04ZVX5o7JL3p8z1p5+xzjJ0/RX/"
        b"oMQBqhlfPx8UDJ8dK7PLKkoBDWI6NwGY+SubbBy9ilKJAw4Zh07epuaabNu24+m+zKru/PD5UaWMgidWQMPZiw7S"
        b"cGlugqiSXSnmwiIuR05/m1/+l0+c1BBt0L0lowU0hGcumcnvFLp9XZxN7LZ/pFCDhjOa8H4srZZkjYDevhuJgIag"
        b"S3ft6Lusb/rhVemCjBbQoJJ++L0o+0ghoCE8uRK9tpF5+bh7cEvJHtavdTJJCE/P6IWbiK5K83jLz+eT9o2TzkGb"
        b"HRBK69HjTTj7u2iWJazjvQU0VNHVkGLodnmUrn881JWtAhp+obcsv7Xb+AYVZp84FtDwlJ4H8UewWRKAgAZAQAME"
        b"NWggLNp/fUmfxt0PSQmmH0erbMp20hDQUMXhzfkwmsymawPr9XrVv3CxngWW8ZDy8zNaQMPhg9PJbYPudSZheHy7"
        b"ziVn4ApoKPyQbjvNR3W7j8/AFdBQ18Dq66FWmeAW6KHKfUiWvC5zn3XSv4qDXlwBDTvPdPVvk3a3kM41v+l+fYH6"
        b"S+H79x2/1gIaQm3l5v45fmHxvL8CdD0xHecAl6zmf7/fg1nE/iMIaKhuTN3fBy5/0Krd3ULF5Y6vJ+FmpnbjMY/7"
        b"ZrSAhq3D5x/I5YWHwA5+xvzm/bcr7Cx8dfIt8AIaasnlfCiH++yGvHArqLXHDD6t8r77Cy2gYV0u5w8f6SfdjeoY"
        b"+U/3a//2sf3datBw5ZHMc7+Bv11c/lqZNfkpoKG6X79YhDXjx0E1dwENKwaSk2u40yd6Sf3wvbSCPmi4/NS+cedG"
        b"6oaW1AhoqOJk1cGgqf8hV/XjN+oV8bVe0uVyxE4dAhrKJ80+n8/c5GHM7ps2dTzcYL1JfH3ze6WmF3rfxf0CGvbp"
        b"IO6PucYDsf64W1LfKJ37X1+yn3X/Y9b2qrQjr2C3pO56xq3B8Tc2/dczdrtOjFUv3C7HwBtBwwXTiYMxNb8X9Lu8"
        b"sgIajl2bMN7ojmojtbbXSEBD+Ydfe0386uceAQ1PX8j7G4f1hcVnY/vXIqDhBgPPy9s5TojOOw638wcPLn+L2usc"
        b"LAENJQu+M0eL3iKzTE4uOYGheEdWfdBw2ahTO/NDmnD6K/i/7nxtsyQw5Ay3LsLe4mksewN2aCxwp5a1VUdkEawk"
        b"BLjLZywBDXBBD6KABjh1MxYBDRDUoAEQ0ADhBouzMzfTBw1w7GZYc9N98QZzO/cfsc23ETQQnryoJx6hkM5SCN/O"
        b"W4n/HcTxQYcwGEGDj/OPHjUveSrGu0Wngwp33HlDQMNdD9cIe5+856WZfBImX6+5V/Dop1GJA44deNrE4zde5Us+"
        b"cxhBw+pPxAs30+mfRmgDvB/4xHN+RgtoWD22SsXH5cXN+OfJ2X9CfaWP8et7SVFIQMPqT775jRcyU09t2x6xIJhf"
        b"rdGrQcPquuSSvdvL/hYENBw1QzjI3zheHlQ2agholZZbUOKAQ1ajDbY3a5omrWXozzT+2PaYPisIaLhHnTqlc4zj"
        b"zHHRPzmCls5BiQPqr1OnHrv0xX4Hnm5xBDQcO+oc7LYzuLHMQkDDGek8Tttx9dkzhoCGCzI6bnuWEnnQ+Dw5/zYZ"
        b"2XKcYJIQdszofifGqkrIkh2HwQgajmpNO6F9DQENrD65+esy7nE7BwQlDtg3oyd3qsvHbrqBjg4ENBxb6+ivBlw1"
        b"Iv754fPk3qo+NAhosJ2Fp0hAA4QvJ/gNijn2WRXQcIMVzIaWCGjwgR0BDQ/bSnQ7n/cR0FBviePyXaEJFqoAIKAB"
        b"ghIHPNdc+TjVqedWFVZyVjQCGsLTOjq+bgld1alX2l0ENITnLM3IfLHC+UBbgghoMMqu0ev18gIFk4QACGgAAQ2A"
        b"gAYQ0AAEXRwQfvUMkbnOjcmzV/QLI6AhnLP/3NfArWcHuxOuZPf9/wQ08IjVcSf8ONI5qEFDePa+0r+9L6uABk7K"
        b"rLZHkCGgAQQ0AAIaQEADIKAh6NKDoA8agtYxBDT8DicKrl347qkQ0EClMS2jgxo0gBE0EFTVzZQKaKjuA/vn8wmb"
        b"q9j1TDaKSwEN/G+4WlUgXjLhqSotoIFKuwalczBJCCCgARDQAEENGgiHL66z1g4BDRbXIaCBsKJ94vKY9j4hoIH/"
        b"9EGnhSpN03Rdd2FzdNd1XpRgkhAAAQ0goAEQ0AACGgi6Jgi6OCDYXQgENARnEiKgAR8IglKPgAZu92nA6phgkhBA"
        b"QEN42pmEG/mAj4CGoObLDxz6pQYN2Pc1HFHZ73+X9/tdsDeWgAYEdNhrFjRldNywcOM2swIarGzc4UHu2CS++3av"
        b"caIiDpZjOqdCSvqKgAZO6nh7/+uOHdAHXVJ/eN40zfv9btu2bMwuoMGZhIdH85PP+tpyho6ABmcSHhXNaaj+2HSO"
        b"Z+h0XSeggYqi+eED536Jo/hJENDA0s/pC2cCRXP/qYitHWVFLQEN16xruEt+iebtjSKpr2PtaFpAQzh/g6GYYhee"
        b"6m0m8OTJYQtVADOB9cZ0QTuHgAbMBJ5U6AgmCaH+dQ119kGL5kP/5XRd93q9Pp+PgAYtzGYCgxNVgKfUNESzgAZE"
        b"MwIaRLNoFtBAuGFPd4rmGOVbVuv8wP5QAhqsJKxuoL3XQznVW0CDlYQEh8YCIKABghIHEHY7Jiot8J0s5qpvhDsv"
        b"3RbQEO67zjuG8rhyrWvNon8BDdV1GdfTU6yhYuOLe87rKKDhWdGsuhI2nzGYugaPfhpNEsKe0Zx+gQeHHp3wy8xx"
        b"ve1pM6n+XfphbQQN9xs4y+Vw/1Jy/9iq8YA6vsQHTRsKaHhETYOvw+fJFysm7/iD0TijjaBBNBMOWho6mbP5dD46"
        b"o9WgoTCdlZt/ckw9eE2/pvOqmxlBwxnRPNfa/POnrjyqCWRV7B5RjxbQsKmm8asFjfRjjv8wuX3ojz0DZe0Zu9c6"
        b"BDQUDpz7ubz297nmTF+4l//gR/69zxBlmxfum9ECGq7ZK7nC7UZXneo992zENYp3j+ktr2zbtquO7hbQwFHRPDnw"
        b"vO9M6VzLc7DdKFBJR8r2mN7xfIPzd6rbslfJjvucGEHD0oHVjr949ZRrJ5tSdnzkm+7KFF/ugmfGJCHYYKj2dH5m"
        b"Ru9e2BHQECx3Ln5nWtLscd+jF1dl9BFldwENulC+9wJm9qn4+lCH7lZRSUYf9AMKaNh/THqLMMqEztzqm37X82CV"
        b"Sr4P5L6D6DRnmHm6bJYEN1huN5lfdQZTZsCbiZvMzxIDfa6ofaNCx+AiU7v6XEYf+uFAQMP+vcP9vK5zLfjkZW+/"
        b"1EyQVR7QmS6d9EZb1tchoKHeZR39I+wqSai5i9/lCm+U0f2LWdJqMv7Rjq6tC2g4Y9HdoPpRoR2zJpU7Kk/ngusZ"
        b"DLSP/okENGwdfs79qg9uWfn84b4XNg7on9lA9cxXUEBDeTrnCxfj3oZqF27sfkm3GETv1TBukhCqW3e3ZPH3uLeh"
        b"hn6GgrHt5GbQdx9E93+KuRclzR98bcUT0HDLrTkGk0sXBvTkt15yMQuPWC27gBo+DGVaOL5OORz3kUhAQ8koctXv"
        b"ZBqFlZ3TcXkBerLsXlblqPYFTbukFkwIT9432G4U6k/nyRUr9U+gXbjhfT1rjha268SbHdEiLaDhZ0OHu/8jEdCw"
        b"TzXg3fO18ba2rPfeUycBDbtlWTxGJLP4+/JYnNwe5OtllC3o8DYQTBKCbfvrHEEvX9GDgIYDO9UefkI5QYkDfmzc"
        b"/dvDSYlvBA2nhuyq7qun1UmWbGfqX5GAhgPTuXhsWE8Z4ZwlJEbQQYkDbjQ9WLBl2kHLiE8YzA72LzVDaAQNVed7"
        b"Grfmo6r+E7OW9/MZRwtoOCl0Pp/Pxq7hhYF7dC7H/ZtOSM+njZr3/XkFNDw0cdQcjnjD2/cpVYMG+P+3q8F/V33i"
        b"2f0NzwgaeKivpwsub3exYT/AUaWq/IkqQZsdQKjs0Nhry/QCGjCIDhaqACCgAQQ0AAIaQEADIKABENAAAhoAAQ0g"
        b"oAEQ0AAIaAABDYCABhDQAAhoAAENgIAGQEADCGgABDSAgAZAQAMgoAEENAACGkBAAyCgAQQ0AAIaAAENIKABENAA"
        b"AhoAAQ2AgAYQ0AAIaAABDYCABhDQAAhoAAQ0gIAGQEADCGgABDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIaAAEN"
        b"IKABENAACGgAAQ2AgAYQ0ABs17Zt13Wr7vLnWQM41Pv9NoIGqDGdm6aJGd00jYAGqEVxOgtogMNH0HEQLaABqh5H"
        b"C2iAiobPsXnDCBqgxnQOujgAKmmqS6XnYKEKQKip3Fw8MSigAY4aPr9er13SOVhJCLBvZaN4SvB3Arp46SRQbWXg"
        b"pqsEU8U5/hQ7/iBG0ADlbypt26Y/7/4eI6AByrvo+tG8vW1DQANsLa62bdv8K0WzETTA4VNZg6hNt0z9c13X9W9z"
        b"UAFdQAPBtGQmvvs5HqP5tCsU0EB47BEnC295ZigLaCCY38uPoCerHCf3Agpo4KGnnCwscRzUQiegAXID5Mw4uoaF"
        b"M/biAJ7bwlH58kUBDSCgARDQAAIaAAENIKABENAACGgAAQ2AgAYQ0AAIaAAENICABkBAAwhoAAQ0gIAGQEADIKAB"
        b"BDQAAhpAQAMgoAEQ0AACGgABDSCgARDQAAIaAAENwCJ/noK2bT0JsEXXdZ4EI2gAI+gnaZrGkwAIaAENEJQ4AAQ0"
        b"AAIaQEADIKABENAAAhoAAQ0goAEQ0ABY6j3l/X4P/hB668L3Whr+fr/Hj//1W6y6V//Gg/3G5vbwiw9i+TsI6Bpz"
        b"eTL+xpG3JannQrZ/Gfm0XX6v/DtQ5knY8a0IENDhzF2hU1yu3Ql3nLMxB/tfHKdt2b22v13JaBDQFw+c86Pmr8m+"
        b"arDZ/179O8Y/pPeJOIbdeK+wbDO/uXcCGQ0CurqBc6YOO1kGiaG2ZCg9l7P9L/bzcfIG4y92Xbclo8ePv9ejAUEX"
        b"x17p3DRN13WZEXG8QbzNEUdnTY6aVw3wt3wayF8GYAQdrtq2f9UMW7z9oDyyy3hzPBLvD6vPORTu60AeMII+6SyV"
        b"r51tS2J9ScTn5/1OqJg7aAaMoO8U0HO15nGDxORd0lB6YaINBqcLG9rK7mUQDQL6pw4kXNJuPJ4SXJ5fk+1xKQEz"
        b"te+CewECOjywG7pt2+Ky7zhtl6wQKbsXENSgf7jlLtmxbSO1i6yqMufvtUsbCWAEHeosd/RrzXNNyoN69C6tI+OS"
        b"d6axeu5eG8f1gBH0DTrt5kapaQy7765Jc0Pjr90aZfcKJ/ZTAwI67BuUX+cSMwl+xHdfda8jglV1G4ISR6h4i7td"
        b"QiqViZcMwNM3XXKvJYtZjKBBQP/mJkr7dkqUJX7mXsels+EzBCWOarft3zEEv+5xMZmMq+61yzBfQIOArtq4HLy9"
        b"QWIQtYMoHIzZ5wJ64b1WfVCI2rYd9OrpCYGgxFFtRqfA2iuq+o+ZP8Kq7F5llZMTNmACjKD3z+iy5oqvj7l2a72y"
        b"exW3G0pnMIIOd9yvY68QnDyUdsd7TRZJBl/fcd0NIKCfHv2r7rU2u4GgxAGAgAYQ0AAIaAABDYCABkBAAwhoAAQ0"
        b"gIAGQEADCGgAgs2SQr0np0zuHJQ5r2TV7T24B//VB7fl1kFen89nxa1fr4Jtgtu23f0YbEeaQrC5Y1F0xLMvbrHp"
        b"uRIHgIAGQEADCGgABDSAgAZAQAMgoAEENAACGkBAAyCgARDQAAIaAAENIKABENAAAhoAAQ2AgAYQ0AAIaAABDYCA"
        b"BkBAAwhoAAQ0gIAGQEADCGgABDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIaAAENIKA9BQACGgABDSCgARDQAM/y"
        b"5yl4v9/pz03T5G8wsOr2HtyD1/zgWy5m7gER0Dtomub9fs/9I5v828ztx/9ePfjcr/GqxPnJp2V8+6ue8/j1tQ+e"
        b"vwEbvT6fz4pbv15d1639Hm3bdl2376uY+cUGbjpOOucTc9u28dsVpFlQgwZAQAMIaAAENICABkBAAwhoAAQ0AAIa"
        b"QEADIKABgs2SCMdtCzDYEsy+M4CAriuaB1+sfw8XIChx/KS2bfO78cXdtgAjaJYOcncpQcw9Zvx6+tu4R6tXAQQ0"
        b"3+sP6esbY7r/yP0ITo+ZbmArdBDQLErn/METex2vFY+oWP44yy9jy2VvPOhor28NAlo6v69NnHxGD8rTc5OK6Wb9"
        b"+kl68PS/4ztm/nb85Ex+nkg3i3/Vv2AZDcEk4aHpvOXMrcHRc3O36bpufEhYOqpn1aTiZCU9cw1zVzU3sZm5qsxf"
        b"AQL62HMOt6fPqkcYd0z3o3b3KMzk+OSo2b8fUOK4fuw8SNi1c4Zd1/XDNJ1fmX+Q/l3GlYf8pOL4wVMVZXye9OSk"
        b"Zb9Ckr7er5bkD6JW2QAj6LPTufjuk5Xftm2/9kePy7j9+Ju872Q+fk3MTNquqtjsfpo7CGjpfGxtJJNck3XbgsaJ"
        b"soufqzKb4gMljnsH/dr8imPbwfqUycpJPkOLpysH1YmvbwMKzSCgq54Y3DGg+1E46H7LPOBeF5xp5sv8IDIaghLH"
        b"aer52B6765b04R30LiV8wQj60UG/aiXh5CB6xw065gbR+jHACPqnRtDLAzq5fJg/10jntwIE9O9k9PJH2H0zvHBi"
        b"LV4NBAT0BQFdnJvjFX1h267QkztXDArT4w0xYg/1Lm8t+a9MtgAuad8Gghr0+RldEIj9KvNkl9s4GfvrD+fuVdbq"
        b"t6QsPtioevIHURsBAf0jFZWvy0PGk4GDMD3iMIH8AsLMd3e2AChx/E5GZ9ZAx79dda+NVZotHzLmrtZ8I2z3+nw+"
        b"K279ehWMleLpTfv+uip6gun6suhIZbr6P/kZQQMIaAAENICABkBAAwhoAAQ0AAIaQEADIKABBDQAAjpcd25sZn+P"
        b"VWdprz14e+Ptd3zwyb867mkpePC52x965Yc+54f+6zrhBbUrTrBZUjhys6SvGyKvPf161e0zP8j2i3Hl9Vz5bz8t"
        b"u/x22yxJQAPBbnZ2swNAQAMIaAAENICABkBAAyCgAQQ0AAIaQEADIKABENAAAhoAAQ0goAEQ0AAIaAABDYCABhDQ"
        b"AAhoAAENgIAGQEADCGgABDSAgAZAQAMgoAEENAACGkBAAyCgAQQ0AAIaAAENIKABENAAAhoAAQ2AgAYQ0AAIaAAB"
        b"DYCABhDQANToz1Pwfr/Tn5umyd9gYNXtPbgH/9UHn7wB270+n8+KW79eXdet/R5t23Zdt+9LmPnHBNzROSn/fr/b"
        b"to3friDNlDgAENAAAhoAAQ0goAEQ0AACGgABDYCABhDQAAhoAAENgIAGQEADCGgABDSAgAZAQAMIaAAENAACGkBA"
        b"AyCgAQQ0AAIaAAENIKABENAAAhoAAQ0goAEQ0AAIaAABDYCABhDQAAhoAAQ0gIAGQEADCGgABDQAAhpAQO+taRov"
        b"HvDb/u576TIaMIIGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIaAAENgIAGENAACGgAAQ2AgAYQ0AAI"
        b"aAAENICABkBAAwhoAAQ0AAIaQEADIKABBDQAAhoAAQ0goAEQ0AACGgABDSCgARDQAAhoAAENgIAGENAACGgABDSA"
        b"gAZAQAMIaAAENICABkBAAyCgAQQ0AAIaQEADIKABENAAAhoAAQ0goAEQ0AACGgABDYCABhDQAAhoAAENgIAGQEAD"
        b"CGgABDTAb/q7/Are7/f7/fZKAEs0TdM0jYA+I5qbphHQwNqMjumhxHHss+yfGiA96i1xPOoDC8DNAtrLABB0cQAI"
        b"aAAENICABkBAAwhoAAQ0AOFGfdBAWLApQv4G4b+rCvrbJ3xdajB54/EGDPGvBl/v337JmobxzRb+dM9cMPH6fD4r"
        b"bv16dV239nu0bdt1nQUpQA3vdm3bxsQvSDMjaGC43eNgR4QUMePtxrquG29A1r97vG/Kprkbx5stGUGna8hc5OAb"
        b"Da6n/7/xZvHyBtf2wG0hBDTcIKMHEZk+9ff/PMj0FMEpKPv3TYWFyRunG4zLEf0bx9FoCtO5i0y3TA8Y/zx4Lxlf"
        b"4fgRnvZZXEBDuPt2bunP/T+kP3dd17Zt2t035V3mxvF/JwN68MX8XsFz2dq/pHEluj9UT28GcVD/kF1Ggy4OuFcW"
        b"98eV4/FyDMHJuExf7Bci5vZhH4Rm+6+vm7bnL3L8jhKvIVM8mXyEp20fbwQNNyhxjKsBg3puHGC2bRun/dNUWLp7"
        b"ust4BDp547ng7t94UIOeu8glkdr/iTCChnsXNFLapvAdjzejFLjxLjHHx911/Rv3HzyZvIDx1ycvMmR7+2w7bAQN"
        b"PzJbmArE/Vm7wQj06/xeKumu7Y5IUZ6KKuNvNLjIyeLJOJTHP0L6QJCZtxTQQBVrVVKHXL/Imxok0uTe8uUe+RJE"
        b"5utpuJ26ODIXOb5l6ugYr5HpT1H2/3fwBiOggYrqG2noOvhiisJUypir5w7SLd5xMtP7zcvjcvOg/aM/sJ28yP51"
        b"pm89vs1gLJ8K65P3ClYSWkkIWEloBA3sU5vefXXMvvN4BZf65L04BDSEX+rxCHWf5lzwsE/+8K3NDkBAAyCgAQQ0"
        b"AAIaQEADIKABENAAAhqAcMlKwvFRkgAc4f8Aayx/K6RtAKcAAAAASUVORK5CYII="
    ),
    "applist.png": (
        b"iVBORw0KGgoAAAANSUhEUgAAAeAAAAMgCAIAAAB0wSZfAAAgvklEQVR42u3dWXakOLcGUFHLU4RBEoOM/4FbuhSt"
        b"ABEI2PshV6YTB9HYH+Koq77fb0hWVVXYpa7rcIW6rq86NVCgz+fTNE3397ZtP59Plpw5KeX+tn5D27Zbv6Vpms/n"
        b"IyiBQnQ5liWd4+N0KVfXdca4+wu/asn6mQDKkff2+vOvvHH353MCwlvLHXnjvquf1HW9o9IgoAHOurPvKhtdNFdV"
        b"1bbt8ccX0AAhb1dh27ZdU/pgIeUfbytA9rCO/ZBHCikCGuDEjO6GsQlogFBUJ2RXiRbQAMU1oruM7trRO8aNCGiA"
        b"03sOu2L01g5DAQ3wi3r0jg5DAQ0Qzi5G76tEC2iAHxWjt2a0iSoAPypGx4X0BDRA+OXqHNlXhRPQgFz+v/VCjwR0"
        b"9rVGBTSg7+6ztfLwMzoJgfDmvrti01lAA7a/CgIaAAENkLZJVeFPUichYFBdOD5a7oy9vQU0wH+GypWzybWABhgO"
        b"7QgFzFIR0ADDNefKaUHrJAQIRnEAIKABQiiklBzUoAHCsVF3VVV1WwjqJAQozu7J32f0MSpxAAQ1aAAENICABkBA"
        b"A7yLURxAMOQ516PdcjW7oqa3AxS1at3FAS2dgXCT9aBNVAEwq1tAAxxuQY/TPH77eUEvoAEt6EIb4AIasGns5k7F"
        b"/ref198ooAEljg27YXV/9tdU6r64exm8YKIKQDntcQEN8Ov2eN6Y/sdgcoAyZxL+Y8IPwMEhHF1MZa9y/N3ictT9"
        b"eUaJB2B3OnehFLsHszcl/+7SapbRQN6Q2THuIubSuAUZXjLMbq6mIaMBE1XKrTjLaAgFDxP2pj05oFP6A2U0WEtI"
        b"QJc7WkNGQ4EzLwy4emxAb/1oZTScp2maHb9cn8+nbVsZHR42DnrfhdflGiXg0mYtnzTjWUDfch6KjCYoAbuoBCWO"
        b"UmcJqnXw4BLwJU2QwW/T6hPw2/fMgM71wzeX0drX3Dedu9Usz1vHMuPv6b6CNaGcEsfkzMCM6SmLUYlWitGCLjdD"
        b"ZTS3y9ACf2KP9/J1rX4/FXZUAU3IPReS9Cd8xkvrnoYQF9Dwi7w70oL+TU7FteTjjk1b54Xt6N5ceA7xtYtpAQ35"
        b"iwBZSsM/i6f+E45BGfMxdrPPva7lqsV4KeRBG3nykbuvmNgioKG4aC6hrDxozPZ3QT24S0h/jODyO9Y0jYwW0JBt"
        b"6Ft43JIaJ111Eh9Wp2KwaSwUtWfzLyNp9zNPH399pJpsdrgWNGQO6H4kFdsAHLf6U8oOMZo3DfaID7vwyPFNGxym"
        b"ES2gIU8632j4wdz02tinN87TrdGcGNODDsnBc5sb+IGAhs0ZdJd0HofvuNUfIzXXS4sx3TTNXC6vDvxAQMP+9Ck/"
        b"ShZqMuNBGtlfUV3X3+93edNVAS2g4ZRCwR2L5rs7LSen5Bzc0HqyEa3QIaDh4ctKjPsGd481jkE/vkodnxA4CGi9"
        b"hcEwO3j8shu5Rq01TdMtJbrwgN3FYN+Ko+OVVA25E9CwP47Lj4/lvsFNbfD0Fxtj+vhqJAJaQMPDY3qh1Js9nQ9O"
        b"thTQQQ0act31327tiE2F3bmQHXcJTpYjum+/dgsYAQ1vHFp3x4zetGjcXAl48tvn5qSkD8a46eJTAhqKy+h+jvSn"
        b"YNyi17F7wikN28nR05NPsr9e3aDRnXINm0tnozgENOQZtHvwYc8oBXRBPNmwXb6uzM3PnpvG0p9y0rbtpurzQiFF"
        b"eSToJIQdYXqXxt1cs3e19291AY30AXNzJ1oY79G2rXQW0LA/o+8S011iTubdQnT+YDuuubKGZfsFNORpnHZpUn6g"
        b"HKkYbH11R+YT2pwwqEFDxmHRd1kyKbFAPLmk6sGu1LnK9eBEyhoCGt477XvHXBXvYVDiAH4zQLDYscYGQQtoCC9f"
        b"kK/YhqoWtIAGLehPmQ1bMwkFNLz3ZjxxAaMsq8qlbBEwOX1GRgtoOBpzVVVtXYQzfmP83l+G0b4lQPcFdOJLm0xt"
        b"GS2gIUPzeccSyf3v3b22/b4ryqYpIeMW9NZFSlOGRc+Nq/vZOyOg4WnpHIMjsVNruel6pGF7UjpPRmp8kNXc3LQF"
        b"4tzTsLidgIZw9sCDlJQ5L4nmis4pK12MX1qX0avr0g3OuDpuZGG1EAEtoOHEdB7n42Qe/eyOPn2li8nQXCg+zK18"
        b"lHiuyWuGgA5mEkL6IOLjpdgYWPs2hTpjZbvlK9DCGvzxgLm3ZdOyRzuWKtWCBjKM6h2H46CL7Gct6PQTLTS346CU"
        b"hba/RekENNxjrPRk03XQoD47o9M3oDqes/u+K713UUADO8Miy4JwuWoa4XCxe9Pi17sXdN40/ENAAztjupygmRwd"
        b"cWTV/4VBzf1jjg84sTB00EkIB4sYq+PDrg2acc/bvkLHYD/GlOktBycrSmcBDfsbpJMzViZbggXucruwXWzK7JJc"
        b"F7O54oYORgENYd9uhDGCJ4egbbpP3zovMcvgjdiI7id1nCjY/SVXRPbnBA52no3PQelZQMMFi2QmpvPZwTRuRDdN"
        b"EyN4cl510zTHdwgc3E8MLgyDa4Pqs4CGH+3sl9IIHZSqfzwCetBkXhiWtyMxFxbTiOftHlbfoICG/Bm9EG2JofbL"
        b"HQLnegvTR08nRmf6OkeTh0lnAQ3ZigarMwZTNgW/qrdw60z3szdG0TcooCH/TJDlUQql7XqV8nLytuvjIy+UhhQ3"
        b"BDS8esPTyQJ6bMjHVzF5c5DYiF5eIqpbfkRxQ0ADSwX0hTJLzOLjO8wOFhGNpxss/6/5LKCB9QmByzNKNsXo6myX"
        b"5adBsBYHKMtcuJe5dBbQQIbF8IRvUOKAkp205ceNirALo79tUiWgocR4esOdvv2oghIHEAwfREADxZawCUoccEYD"
        b"M2UhpPIrtkd22pbOAhouDq8wX66N+Tt32Hh1//Intmg+C2gIT+owvPvYBmkroOEhVY64Jv3q/f6NgntHC9rPhoAG"
        b"DOcIRnEAIKABENAAAhoAAQ0goIGwthWs8Q8Ew+yghH1X+4d9v9+QsI+1txQBDcVNqyukcd1NNzddUECDKRuhzFmC"
        b"3Z+DTbgR0EBBYd1PajV0AQ1v31SlwBCU1AIagirHjdrUStUZ39Wtb6OAhnDVvnzlD+dQqs4YzU3TbP3EBTRcs7hz"
        b"N3TvRnn3vALIb97/mM47ziWg4cnpcHBkd2JS3zSsf/Oc41u94/5DQMMbxR2tYtoeTOp4vblFUsfXfvazjTs57KsO"
        b"CWjI1tSKSbd8fCGbqsQ87Rea9z23ft7dJamPvN5Nd0VdB0Z3RdSChmt68/pN0YXjj7RYf5DU3d93P8lxp2KZSX1S"
        b"b+c4go+ks4CGU34t79X7N75R6ML64NiVwjsVT+r47V+ful3e27bd/cIFNBgindrk3Neyjt91JKpu9KnFy1tM590X"
        b"bAENbMvoMgs1hQ8h14KGp90yF77ydYxpYT1+l7q6c2K/sYCGX0zieOcqrMfHgTz4hiOu7BrsqAKXpPOgP62rPy4f"
        b"+aTKtZWVFnqPB01pLWj4UTVj4RdvXHwcH3y7RBt0dmk4J87mb9u2W4jDOGg4PZTn8qi7q+3ayF0c98fbDlrZ9x2H"
        b"p59w31gRE1UgnLea3Woejac/zKXYHdNZl+DBPsOu8LXpoxfQkGGERn8pzu5X8ZKZbCX3gr65Qh3vpQQ0XNA51v+t"
        b"W+0XKmq+xtmLVNicJfSK0VsnZwpo2L+Mw1zo9Fe36I+ELTaqUro9d7xLxnUcvIEQ0LBtGFnib9pgQkfJuZyryayx"
        b"HOxJCKHI1ezuuD9sllAOxkELaCAUs8uiXBbQQLhd/R0BDVyQy0JZQANyGQENKC4LaEBxGQENKGKEvOvHXjX5U0BD"
        b"eO3Ibrkc0sYgNk0TZ/D/8k2zYD+8vaZhDayQsDBWXD/2l1udCWjA+hhJq0RNHnDqdU5AA+8tNB9s/zZNc3BOpoAG"
        b"mM3oqqo2rWYVF8DqvrH7y0kxrZMQ9uzFd/cC7iW7ohT7pnUbBq6uttr/30Eid1mffUiMgIbUtd/GI4Xvm9Sn3pgv"
        b"dEsW+44lviELhw22oBTQcMG6yTFlDISw8dXqVu4CGq4MaxM9OK/2JaAhw1aqkvqS/Hr86HIBDSFl3l1i95FFLYIC"
        b"joCGSzq40jv6+x1ikvolV/HsH7Rx0LAtptt/Lf82dkndTYXo/rxkZFs5nXVFvfxTL+Fa0FDEosn9qWhzv59ldipu"
        b"qpaOl3YrdjCfEgcw0R7s6tTLNZD+f107UC/9vJOvJeXb795kHlyHli82JqpAcc2lyXVz0qvVd6xNv6GePlm/att2"
        b"NaPjx51rNVcBDeduHDVYAu3u7crHD5WbTOc4NSnx48vVmtZJCD/qWjSW4773BzvSNsuVWAsafjHt8NljGJ5Ug55b"
        b"MGRrIzqoQYNQvkuVww2EgIZ75PKNFlqabEsuZHT3X++8aRDQUOgQjtUxv7GOebu25OSL7VfV+6u4dQdPvhu3eOHL"
        b"154fX3UENOxfzW5TY/m+9/iThdduoMJgNHd32H3np8R0ntyiYdPryrL+tYCGUyrLT1rfbrVFOQjoW9egBzcH/UtU"
        b"evM5TnI5+KoFNCT90ib+cub6zQzljQ5e3kzkMTX3/s3BpvpV//hcL1ZAw9ERYy9ZDPrICLPbvTM7ys1nvEYBDUfX"
        b"G3rDALL+rMjLl7G3owqwMqPsbQN7u/mQWzsAu+9627bCAhrk8jUZvamn9A3pHOZ7FwU0hB+vPOlatTqqwa7nAhq4"
        b"OKMHnagv348xeyNaQANHx0drKZ/EcqMAocx9Y7WgAf6/m2F5mEqcwD2uv59xG6EFDSGltljllj47kd+0fFc7NuPG"
        b"C9227j/oFNWChnDJ2vOX7x3148tDmXXqfrAmfiJx5f444vC87XIENATbO73z5X+/3yxTSYNhdkDIWrS5amb8jYYP"
        b"Ht+ZUEBD+EGNcrkgMB4IXPhmfZc8h+PrI1+7b+zvn7+Ahgytv6qqEqcdvnwvqPLrKl1NeXyTccnVRUDDS7evZvkS"
        b"0r/QXnVdEdDAXVfjfHxj3zhoeH73F8FUbwCFoKDEATdduL2QnNrU5B885/TvFcoCGsrar28Q0P1/9odwXFsVSV/h"
        b"ejzsJLGk8/LxKkGJA8psRPfX2ein83jklnFyaEHDT/frmyx07C4UIKCBnIWO5QrsfQd+3GuonIAGhqUMw/IQ0HC/"
        b"jD5vacrSGtF6CAU0lDhppcum+Gd/FbQHtJ1XhxLOjf3w4yGgoaCFKx92yUlvRE82n2V0MMwOzJ07e2jdeMigEdBa"
        b"0GDIcEGXn6qqxh2ec+ms+Syg4TbN4Xut6za3z4jGsoAGzeGyhnhb8E9AQ3jwDn736khcaES7vAloCA/r7otbK93r"
        b"HmLHW/GAod8CGnjIVEnpHAyzAy5ZEyqx4d8dLJ0FNNyjh/AxU1e6mJ57OTGapXNQ4oBw9fL2cQHoLpvC2mrRj5kq"
        b"acizgIZQ/toU7i0IShwAAhrQikRAg4wGAQ3h0nq0lSsQ0HBZC3ohgvvxrdGNgIZSGtFFbTLSNE31W3EkIsEwO7hw"
        b"LaGmacbTNAbDn69tQf8+K20HLqChlAU5l4vRooqgxAE/ngBtfWQENJSb0cvJawkhghIHXL5IxbhL8Em7fSOg4TkL"
        b"CcllBDSYXhjOWLEPAQ1cNkzQ+xB0EgIgoAEENAACGkBAAyCgARDQAAIaAAENIKABENAAAhoAAQ1AsJodhPM36g63"
        b"XUPO4qICGh5isCH3AxaMtrhoUOIAQEADBCUOIDyjsB4UVQQ0hAdtDfWY7jWJKaDhgQ3PB0TbSd2edj4U0MDN6hva"
        b"7EEnIYCABkBAAwhoAAQ0AMEoDiAYUCGggduwml3IN9Zw4WrXP8WOi6KAhqTfwEsGDnP324iDpxDQoL350rbz71vQ"
        b"W/NaQAMCOsOjjfN3vM/D1iu9URwA+bfdGfxz3zokAhooemOwe70DTdNMNs/3BbQSB7z6Nj9jR5mhewuVjX1vjoCG"
        b"cOGehBeGWpcj3RPo/7l7sNog8eX18U9ZQMNli3Nens6D7rKtDb3Pvybfq/pfdngIpnoDv7zk9Out+w5QlxfQQFJA"
        b"b2rtduEb0qpDl+zeEkqqj+3OaCUOeF3312RenJHO42L3azN6Xz+hgIZgJmF683lrOh9MqJePmRHQcFk/YTmBtan5"
        b"/ObNdn+817CAhhdVObqYOBKyy9+78OAKHTtuIwQ0kCGduypQlz77yiAEozjAHOi89Y1uqG+/ij03+NeSrVuvWwIa"
        b"Tq9BP2O+xtw7MPnqDk7QIChxwKaBZXE+9NYmZ78Hv8CkTikNz90ELBRVJ7/+8jK0gIZzlw9OH442Xn/y4NI54bqu"
        b"zn1Dpwd9htI5qEHD5RXk5VnOl0+AHqfk8vOZewdWbyYG/yudBTRcPKEjZQxDaYtUDJ7zoNm7Y0jG5JrIOgkFNFxZ"
        b"IpiMs8l13crM6H4Zp/vKXDovF2om/0sLOqhBw4XjNyb30Yh5V9d1CQOEu6c0fl2DuSQHrx+ThREZrQUN1wytm9yG"
        b"rj86eDD47MIW9PJG1Ktl95cvrCGg4faBPtlQ7Uf2hRNYjgzNTvxezWcBDYUO9ogpVmwqHQloG8gKaCgiwtIHPt+r"
        b"tbhvsl96ceOpY+x+uZWXgIYMVelx8/lGO+alB+6mgyfX6Aj3Xxk8vq4fzGU3igPCwc1BxkPrbrT4RrxLWChK7Gsz"
        b"9h/5Gc3nwYCcLq9PHZYjoGHboLRuUY6Fjr70LCsktvpJOrhLyFJGf0w6xybzYN2+8zJaQEPSL+dgct1CD9hyHpVc"
        b"DCm8V/PsbtLlz3SuoHFqRgtoSG09pfwSrlZpjW0odtb+3NzO1XLzeRmtkxCyjXlI6UPrd509u636GSl2hcKFdQq7"
        b"z2t1MamTPk0taNic0UeGPD+v6yx9KHSB8w+XP7iYzquL9sVj8l6HBDTs7087Ukd+cDo/49qz77qbdw0sAQ1BvJJr"
        b"NnxXjM6V0WrQADlXg8p48RbQ8Ovb/6qqmqapqsqIDgQ0PGqPcAr/gDJ+uAIaINtqfHk7CQU0QJ6ozb6NmYAGyBC4"
        b"Z2wyKaCBYAziwdg9aQtgAQ0vbRtWJ3tMR+hq+J63QbuJKhBeOOjCMJKtGT03Mvq8dBbQkPr76U14/DV4+VOOGd1N"
        b"ZI9/nnqpE9CA625ILDTHdnSXzmdfuQU0oHK1IdPjDjs/KBMJaIBfzGER0BBOWjpHRZvfE9AQfjmwt5DhE3kvOZe3"
        b"NAU04JLzqJF8/Tdh9y7Ap75SAQ28cUeVwXr8kxsnJm6q0n3XGZUrAQ0YwhEmdxSMAb3cRp7cCE1AA/yizrPagj7p"
        b"jsFaHABBJyFgw1kENNwhoCU1Aho0nwk2jQVAQANl3yXEP1OGEhOUOIBfxvT3+/U+aEHDY0vVP1g0Ay1oYGeJwBsi"
        b"oAGDPQhFrQwloIG3p+rc5TBuPLh6NT1pbVUBDbz0HiXmcpet44TtYjdluVEtaIBT9hNYiNduE0LrQQOUWDi+cOcB"
        b"w+wAgnHQAAhoAAENgIAGENAACGgABDSAgAZAQAMIaAAENAACGkBAAyCgAQQ0AAIaQEADIKABENAAAhoAAQ0goAEQ"
        b"0AAIaAABDcBOfw97PZ/Px4cKN1LXtTdBQAPSWUD7vAEEtIAGgk5CAAQ0AAIaQEADIKABBDQAAhpAQAMgoAEQ0AAC"
        b"GgABDSCgARDQAAhoAAENgIAGENAACGgAAQ2AgAZAQAMIaAAENICABkBAAyCgAQQ0AAIaQEADIKABBDQAAhoAAQ1Q"
        b"mrquBTSAgAbgnHQOIfw97C34fD7jd2Twxcm3LMsxTuRETrT1mB2xdd+A3vpinxzQ/fdi7udm9ZgsD+JETuREq7+k"
        b"0vn5AT33FqS8NavHZHkQJ3IiJ3phcWPfq66+3++Go6uqbdut52iapm3bF34qQIE32U3TdKG5UJDJa3cA6iQEKDGd"
        b"BTRAoeksoAEKTWcBDVBoOofnjeIACAWM2cgyLEJAA+RM5x1D3QQ0wD0azgIaoNxoFtAAeaYInjQRT0ADFBfNAhqg"
        b"oIKGgAbYuQrbz3JZQAOsLLYX/37VWm8CGgivnexX+IKoAhp4dS9fmF+Y9PKkthYHEN65MHRI26NLQAPcYyNXAQ2A"
        b"gAYQ0AAIaAABDYCABhDQAAhoAAQ0gIAGQEADCGgABDQAAhpAQAMgoAEENAACGkBAA1CQv0duBBn+u+FYyr6QWY5x"
        b"Iidyoq3HFL4roIA+K6D7H/zcz83qMVkexImcyIlWf0l5fkDPfd4pPwerx2R5ECdyIieSvImq7/e74eiqatt26zma"
        b"pmnb1qcClHCT3TRNd53YkWZBJyEAAhpAQAMgoAEENAACGkBAAyCgARDQAAIaAAENIKABENAACGgAAQ2AgAYQ0AAI"
        b"aAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIagKv9Pez1fD6f/j/ruh5/"
        b"cXxArmOcyImcaOsx8eu8K6D7H/zcz83qMVkexImcyIlWf0l5fkDPfd4pPwerx2R5ECdyIieSvImq7/e74eiqatt2"
        b"6zmapmnb1qcClHCT3TRNd53YkWZBJyEAAhpAQAMgoAEENAACGkBAAyCgARDQAAIaAAENIKABENAACGgAAQ2AgAYQ"
        b"0AAIaAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIagKv9Pez1fD6f/j/r"
        b"uh5/cXxArmOcyImcaOsx8eu8K6D7H/zcz83qMVkexImcyIlWf0l5fkDPfd4pPwerx2R5ECdyIieSvImq7/e74eiq"
        b"att26zmapmnb1qcClHCT3TRNd53YkWZBJyEAAhpAQAMgoAEENAACGkBAAyCgARDQAAIaAAENIKABENAACGgAAQ2A"
        b"gAYQ0AAIaAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIagKv9Pez1fD6f"
        b"/j/ruh5/cXxArmOcyImcaOsx8eu8K6D7H/zcz83qMVkexImcyIlWf0l5fkDPfd4pPwerx2R5ECdyIieSvImq7/e7"
        b"4eiqatt26zmapmnb1qcClHCT3TRNd53YkWZBJyEAAhpAQAMgoAEENAACGkBAAyCgARDQAAIaAAENIKABENAACGgA"
        b"AQ2AgAYQ0AAIaAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIagKv9Pez1"
        b"fD6f/j/ruh5/cXxArmOcyImcaOsx8eu8K6D7H/zcz83qMVkexImcyIlWf0l5fkDPfd4pPwerx2R5ECdyIieSvImq"
        b"7/e74eiqatt26zmapmnb1qcClHCT3TRNd53YkWZBJyEAAhpAQAMgoAEENAACGkBAAyCgARDQAAIaAAENIKABENAA"
        b"CGgAAQ2AgAYQ0AAIaAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIagKv9"
        b"Pez1fD6f/j/ruh5/cXxArmOcyImcaOsx8eu8K6D7H/zcz83qMVkexImcyIlWf0l5fkDPfd4pPwerx2R5ECdyIieS"
        b"vImq7/e74eiqatt26zmapmnb1qcClHCT3TRNd53YkWZBJyEAAhpAQAMgoAEENAACGkBAAyCgARDQAAIaAAENIKAB"
        b"ENAACGgAAQ2AgAYQ0AAIaAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQAAIa"
        b"gKv9Pez1fD6f/j/ruh5/cXxArmOcyImcaOsx8eu8K6D7H/zcz83qMVkexImcyIlWf0l5fkDPfd4pPwerx2R5ECdy"
        b"IieSvImq7/e74eiqatt26zmapmnb1qcClHCT3TRNd53YkWZBJyEAAhpAQAMgoAEENAACGkBAAyCgARDQAAIaAAEN"
        b"IKABENAACGgAAQ2AgAYQ0AAIaAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCgARDQ"
        b"AAIagKv9Pez1fD6f/j/ruh5/cXxArmOcyImcaOsx8eu8K6D7H/zcz83qMVkexImcyIlWf0l5fkDPfd4pPwerx2R5"
        b"ECdyIieSvImq7/e74eiqatt26zmapmnb1qcClHCT3TRNd53YkWZBJyEAAhpAQAMgoAEENAACGkBAAyCgARDQAAIa"
        b"AAENIKABENAACGgAAQ2AgAYQ0AAIaAABDYCABkBAAwhoAAQ0gIAGQEADIKABBDQAAhpAQAMgoAEENAACGgABDSCg"
        b"ARDQAAIaAAENgIAGENAAHPZ3+TP4fD6fz8cnAaSo67quawH9i2iu61pAA1szuksPJY5z32U/aoD0KLfE8aobFoCb"
        b"BbSPASAYxQEgoAEQ0AACGgABDSCgARDQAIQbjYMGQsKiCMsHhP/OKugvn7A61WDy4PECDN1/Db7ePz5lTsP4sMRX"
        b"984JE9X3+91wdFW1bbv1HE3TtG1rQgpQwtWuaZou8XekmRY0MFzucbAiQoyY8XJjbduOFyDrf3v3vTGb5g7uDktp"
        b"QcfnsPAkBycaPJ/+P7vDuqc3eG4vXBZCQMMNMnoQkfGuv//3QabHCI5B2f/eWFiYPDgeMC5H9A/uWqMxTOeeZDwy"
        b"PmD398G1ZPwMx4/wtntxAQ3h7su5xb/3/xL/3rZt0zRxdd+YdwsHd/+cDOjBF5fXCp7L1v5TGlei+031eDHoGvUv"
        b"WWU0GMUB98rifrty3F7uQnAyLuMX+4WIuXXYB6HZ/Gt10fblJzm+onTPYaF4MvkIb1s+XgsablDiGFcDBvXcroHZ"
        b"NE3X7R+7wuK3x28Zt0AnD54L7v7Bgxr03JNMidT+K0ILGu5d0IhpG8N33N7sxMDtvqXL8fHouv7B/QePJp/A+OuT"
        b"TzIsju2z7LAWNDyktzAWiPu9doMW6Gr/Xizpbh0dEaM8FlXGJxo8ycniyTiUxy8h3hAs9FsKaKCIuSpxhFy/yBsH"
        b"SMTOvfTpHssliIWvx+Z2HMWx8CTHR8YRHeM5Mv0uyv4/BxcYAQ0UVN+ITdfBF2MUxlLGXD13kG7dN05men/w8rjc"
        b"PBj+0W/YTj7J/vOMpx4fM2jLx8L65HcFMwnNJATMJNSCBvLUprPPjsnbj7fjqb55LQ4BDeFJYzxC2bs573jYN998"
        b"G2YHIKABENAAAhoAAQ0goAEQ0AAIaAABDUC4ZCbheCtJAM7wPy3OUJyQ3SigAAAAAElFTkSuQmCC"
    ),
    "wifi_icon_ok_40@925.jpg": (
        b"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4R"
        b"DgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU"
        b"FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAAWABsDASIAAhEBAxEB/8QAGAAAAwEBAAAAAAAAAAAAAAAA"
        b"AAcIBAn/xAAnEAABBAEEAgEEAwAAAAAAAAABAgMEBQYAERIhBwgTIjEyYRQVUf/EABQBAQAAAAAAAAAAAAAAAAAA"
        b"AAD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCvvZH2OzLCs0heP8Bw6wtMmnxhLZslRVvMcAtI"
        b"WEJCSlW3IBSlKSE7no7EhR3OP+zzc5T1lnNfRSZW8n+A7cx2fiCiTxSnscQd0jYkddE6tHP6O0yTDbatpLZdFbyG"
        b"SmLYoBJYcBBSeiOtxsf0T0ftrn5kfr347xHI1wvKXmSWvOp8lKrFMdh6WiOpTSCkuOubniU8PqITvz349KVoGBJ8"
        b"3+wHrcmIrP8AGXcxoA43GEiElLz77jro4hLiD+f5IAWEpG4JIGxNsVMx2xqoUp6MuG8+yh1cZzfk0pSQSg7gdgnb"
        b"7D7anz1U8HzPG3zWlZ5KsMswaTGS3UwnOZbUkfTzX8hUeSQkJCkEcgNz1sNUdoDSG9gvVGm86ZXit47I/rXa+Txt"
        b"EsJCF2MQjptS+JIUg9pI2PZG4GjRoHdVVMGirmK+thR6+BHTwZixGktNNp/xKUgAD9DWvRo0H//Z"
    ),
    "wifi_icon_error_40@925.jpg": (
        b"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4R"
        b"DgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU"
        b"FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAAWABsDASIAAhEBAxEB/8QAGAAAAwEBAAAAAAAAAAAAAAAA"
        b"AAcIBgn/xAAnEAABAwMEAgICAwAAAAAAAAABAgMEBQYRAAcSIQgxFCITMiRSYf/EABQBAQAAAAAAAAAAAAAAAAAA"
        b"AAD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCvvJHyOvKyr0hbf2DZ1QqlzT4wls1JUVbzHALS"
        b"FhCQkpVjkApSlJCcno4JCjrNv+Tzc5T1Svmn0KTKzJ+A7WY7P4gok8Up7HEHKRgkddE6tG/6HVLks2rU2iVZdCq8"
        b"hkpi1FAJLDgIKT0R1kYP+E9H1qA6rsBY9lXaGL63OiXHu/Kkh6PQqpIk/AkzSylTbMl4/ZaFN5VhRbCiQeilRIbm"
        b"Tvf5AeNyYir/ALZdvGgBxuMJEJKXn33HXRxCXEH9/wBkALCUjIJIGCbYpMx2o0qFKejLhvPsodXGczyaUpIJQcgd"
        b"gnHoetQPtpufcG324kO29vaRXZtcq7zEGpWNXHHF0+2ktK/kSGnVOclhTYATn0EoBOCTroHoDSc3k8caZufXWrlh"
        b"uxKbdEWE7HjS5EJL6OZSoNuKSeipBVkFQUU4SU8SMk0aBf2p4Vr25ti3JtrXZLY3Ip00TZ1xTVKdTUg4tJksuJ/o"
        b"pIUEdYSTniR9dVHo0aD/2Q=="
    ),
    "server_icon_ok_80@925.jpg": (
        b"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4R"
        b"DgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU"
        b"FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAAWABsDASIAAhEBAxEB/8QAGQAAAgMBAAAAAAAAAAAAAAAA"
        b"AAgCBgcE/8QAKBAAAQQBBAAFBQEAAAAAAAAAAQIDBAUGAAcREggTIjFRFCFBQmEV/8QAFAEBAAAAAAAAAAAAAAAA"
        b"AAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/AHs8Re6OSYRJw+hxQwottkMt4LsZ7RfREjMN"
        b"+Y8sNJPZR6nnkAgBKgeCpJFcw5W9OfYvWZFRbjYvLqLJlMiK+5QPsKWg+xLbnVaT/FAEfkan4yJdYxj+Kocrbubk"
        b"K7FSqh6itU1r8daWypxXnqSsJ9AP6E/BGl8ra3cmewqbWUm7s+LJV3E2v3GZfZkEAJ7pdbiFLg4SAFAkEAcHjQMV"
        b"UZdufgu82DYtmd1SZBXZU3YJQa+EqOuMqMyl3tyT6ueevH9J/A0wGku8P0cY7vrQRs3xLOIGRWMSb/gWOVXyLNpt"
        b"aE+ZJSgBppSFKQ4o9uFA+rnqVDs6Ogy3fTZ2Xuixj8+otkVOQUEsyYSpbXnw3QsBLiHmj9lApBAPuOSP2OqjR7ab"
        b"2YxTw6mmy3CqmqhthmNBg0HksMIHshCE8JSkfAHGjRoO7HNns/s908Wy7PMrqrVvGm5n0MaqgFgqXIaDS+5J+6eo"
        b"5+eQPk63LRo0H//Z"
    ),
    "server_icon_error_80@925.jpg": (
        b"/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4R"
        b"DgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQU"
        b"FBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wAARCAAWABsDASIAAhEBAxEB/8QAGQAAAgMBAAAAAAAAAAAAAAAA"
        b"AAgCBgcE/8QAKRAAAQQBBAAFBAMAAAAAAAAAAQIDBAUGAAcREggTISJCFDFBYRZRgv/EABQBAQAAAAAAAAAAAAAA"
        b"AAAAAAD/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwB7PEXujkmEScPocUMKLbZDLeC7Ge0X0RIz"
        b"DfmPLDST2Uep55AIASoHgqSRXMOVvTn2L1mRUW42Ly6iyZTIivuUD7CloP2Jbc6rSf0oAj8jU/GRLrGMfxVDlbdz"
        b"chXYqVUPUVqmtfjrS2VOK89SVhPsB+BP9EaxFujy+TtraZeugzjK2oDyEuQrHNk2Knq88+e9XutsJbU57fQhXxT7"
        b"gCSA3Woy7c/Bd5sGxbM7qkyCuypuwSg18JUdcZUZlLvbkn3c89eP2T+BpgNJP4acgp8x3sr5GJxbjMsfgJmfU5ll"
        b"9sqRIhyFBwIjQ09UAOK4fU8gpPooEKPVXDsaDLd9NnZe6LGPz6i2RU5BQSzJhKltefDdCwEuIeaPooFIIB+45I+R"
        b"1R5OxO51nt2jC/5zT4xSFSIa2MVqkwUt15SpLjTPQAsqHI6lBH+ePU0aDq2v8NMzavcmBf0Fk1UY8uMuNaY2l5cq"
        b"O+pDZTHlNFaQW5AClJcUnjuCrnnslKGA0aNB/9k="
    ),
}


main()

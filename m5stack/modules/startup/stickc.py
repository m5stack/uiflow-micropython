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
import time
import esp32
import machine
import requests
import binascii

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False

DEBUG = True

# launcher
LAUNCHER_IMG = "res/stickc/launcher.jpeg"

# menu
MENU_DEV_IMG = "res/stickc/menu_dev.jpeg"
MENU_APPRUN_IMG = "res/stickc/menu_apprun.jpeg"
MENU_APPLIST_IMG = "res/stickc/menu_applist.jpeg"

# app.run
APPRUN_IMG = "res/stickc/apprun.jpeg"
RUN_ONCE_SELECT_IMG = "res/stickc/run_once_select.jpeg"
RUN_ONCE_UNSELECT_IMG = "res/stickc/run_once_unselect.jpeg"
RUN_ALWAYS_SELECT_IMG = "res/stickc/run_always_select.jpeg"
RUN_ALWAYS_UNSELECT_IMG = "res/stickc/run_always_unselect.jpeg"

# app.list
APPLIST_IMG = "res/stickc/applist.jpeg"

# app.cloud
CLOUD_WAIT_IMG = "res/stickc/wifi_wait.jpeg"
CLOUD_CONNECTED_IMG = "res/stickc/wifi_connect.jpeg"
CLOUD_DISCONNECTED_IMG = "res/stickc/wifi_disconnected.jpeg"
CLOUD_ERROR_IMG = "res/stickc/wifi_error.jpeg"
CLOUD_READY_IMG = "res/stickc/wifi_ready.jpeg"

# statusbar
BAT_IMG_PATH = "res/stickc/battery/"

# develop
AVATAR_IMG = "res/img/avatar.jpeg"
DEVELOP_PRIVATE_IMG = "res/stickc/develop_private.jpeg"
DEVELOP_PUBLIC_IMG = "res/stickc/develop_public.jpeg"

# font
MontserratMedium10_VLW = "res/stickc/Montserrat-Medium-10.vlw"
MontserratMedium12_VLW = "res/stickc/Montserrat-Medium-12.vlw"


class AppBase:
    def __init__(self) -> None:
        self._task = None

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
        self.on_exit()


class DevApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        self._mac_text = self._get_mac()
        self._account_text = self._get_account()
        self._bg_src = self._get_bg_src()
        self._avatar_src = self._get_avatar()

    def on_view(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_pos(0, 12)
        self._bg_img.set_size(80, 148)
        self._bg_img.set_src(self._bg_src)

        self._mac_label = widgets.Label(
            "aabbcc112233",
            6,
            68,
            w=64,
            h=26,
            fg_color=0xFFFFFF,
            bg_color=0x1C1C1E,
            font=MontserratMedium10_VLW,
        )
        self._mac_label.set_text(self._mac_text)

        self._account_label = widgets.Label(
            "XXABC",
            6,
            104,
            w=64,
            h=34,
            fg_color=0xFFFFFF,
            bg_color=0x1C1C1E,
            font=MontserratMedium12_VLW,
        )
        self._account_label.set_text(self._account_text)

        self._avatar_img = widgets.Image(use_sprite=False)
        self._avatar_img.set_pos(24, 20)
        self._avatar_img.set_size(32, 32)
        self._avatar_img.set_scale(0.16, 0.16)
        self._avatar_img.set_src(self._avatar_src)

    def on_ready(self):
        super().on_ready()

    async def on_run(self):
        refresh = False
        while True:
            t = self._get_bg_src()
            if t != self._bg_src:
                self._bg_src = t
                self._bg_img.set_src(self._bg_src)
                refresh = True

            refresh and self._mac_label.set_text(self._mac_text)

            t = self._get_account()
            if t != self._account_text or refresh:
                self._account_text = t
                self._account_label.set_text(self._account_text)

            t = self._get_avatar()
            if t != self._avatar_src:
                self._avatar_src = t
                try:
                    os.stat(self._avatar_src)
                    self._avatar_img.set_src(self._avatar_src)
                except OSError:
                    self._dl_task = asyncio.create_task(self._dl_avatar(self._avatar_src))
            elif refresh:
                self._avatar_img._draw(False)

            refresh = False
            await asyncio.sleep_ms(1500)

    def on_hide(self):
        self._task.cancel()

    def on_exit(self):
        del (
            self._bg_img,
            self._mac_label,
            self._account_label,
        )

    async def _dl_avatar(self, dst):
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            if len(infos[4]) == 0:
                self._avatar_img.set_src(AVATAR_IMG)
            else:
                try:
                    rsp = requests.get("http://community.m5stack.com" + str(infos[4]))
                    length = int(rsp.headers["Content-Length"])
                    block_len = 1024
                    source = rsp.raw
                    read = 0
                    with open(dst, "wb") as f:
                        # 逐块读取数据
                        while read < length:
                            to_read = block_len if (length - read) >= block_len else length - read
                            buf = source.read(to_read)
                            read += len(buf)
                            f.write(buf)
                    self._avatar_img.set_src(dst)
                except:
                    self._avatar_img.set_src(AVATAR_IMG)
        else:
            self._avatar_img.set_src(AVATAR_IMG)

    async def _keycode_dpad_down_event_handler(self, fw):
        pass

    async def _keycode_enter_event_handler(self, fw):
        pass

    async def _keycode_back_event_handler(self, fw):
        pass

    @staticmethod
    def _get_mac():
        return binascii.hexlify(machine.unique_id()).upper()

    @staticmethod
    def _get_account():
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            return "None" if len(infos[1]) == 0 else infos[1]
        else:
            return "None"

    @staticmethod
    def _get_avatar():
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            # print(infos)
            if len(infos[4]) == 0:
                return AVATAR_IMG
            else:
                return "res/img/" + str(infos[4]).split("/")[-1]
        else:
            return AVATAR_IMG

    @staticmethod
    def _get_bg_src():
        if _HAS_SERVER is True and M5Things.status() == 2:
            infos = M5Things.info()
            if infos[0] == 0:
                return DEVELOP_PRIVATE_IMG
            elif infos[0] in (1, 2):
                return DEVELOP_PUBLIC_IMG
        else:
            return DEVELOP_PRIVATE_IMG


class RunApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        (
            self._date_text,
            self._mtime_text,
            self._account_text,
            self._ver_text,
        ) = self._get_file_info("main.py")
        self._enter_handler = self._handle_run_once
        # print("date:", self._date_text)

    def on_view(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_pos(0, 12)
        self._bg_img.set_size(80, 148)
        self._bg_img.set_src(APPRUN_IMG)

        self._date_label = widgets.Label(
            "",
            24,
            32,
            w=46,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x1C1C1E,
            font=MontserratMedium10_VLW,
        )
        self._date_label.set_text(self._date_text)

        self._mtime_label = widgets.Label(
            "",
            24,
            45,
            w=46,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x1C1C1E,
            font=MontserratMedium10_VLW,
        )
        self._mtime_label.set_text(self._mtime_text)

        self._account_label = widgets.Label(
            "",
            24,
            56,
            w=46,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x1C1C1E,
            font=MontserratMedium10_VLW,
        )
        self._account_label.set_text(self._account_text)

        self._ver_label = widgets.Label(
            "",
            24,
            67,
            w=46,
            h=25,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x1C1C1E,
            font=MontserratMedium10_VLW,
        )
        self._ver_label.set_text(self._ver_text)

        M5.Lcd.drawImage(RUN_ONCE_SELECT_IMG, 4, 104)
        M5.Lcd.drawImage(RUN_ALWAYS_UNSELECT_IMG, 4, 132)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        if self._enter_handler == self._handle_run_once:
            M5.Lcd.drawImage(RUN_ONCE_UNSELECT_IMG, 4, 104)
            M5.Lcd.drawImage(RUN_ALWAYS_SELECT_IMG, 4, 132)
            self._enter_handler = self._handle_run_always
        else:
            M5.Lcd.drawImage(RUN_ONCE_SELECT_IMG, 4, 104)
            M5.Lcd.drawImage(RUN_ALWAYS_UNSELECT_IMG, 4, 132)
            self._enter_handler = self._handle_run_once

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        self._enter_handler(None)

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    def _handle_run_once(self, fw):
        M5.Lcd.clear(0xFFFFFF)
        execfile("main.py", {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt

    def _handle_run_always(self, fw):
        M5.Lcd.clear(0xFFFFFF)
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", 2)
        nvs.commit()
        machine.reset()

    @staticmethod
    def _get_file_info(path):
        date = None
        mtime = None
        account = None
        ver = f"Ver: UIFLOW2 {esp32.firmware_info()[3]}"

        try:
            stat = os.stat(path)
            mtime = time.localtime(stat[8])
        except OSError:
            pass

        if mtime is None or mtime[0] < 2024:
            date = "--/--/--"
            mtime = "--:--:--"
        else:
            # print("mtime:", mtime)
            date = "{:04d}/{:d}/{:d}".format(mtime[0] - 2000, mtime[1], mtime[2])
            mtime = "{:02d}:{:02d}:{:02d}".format(mtime[3], mtime[4], mtime[5])

        with open(path, "r") as f:
            for line in f:
                if line.find("Account") != -1:
                    account = line.split(":")[1].strip()
                if line.find("Ver") != -1:
                    ver = line.split(":")[1].strip()
                if account is not None and ver is not None:
                    break

        if account is None and _HAS_SERVER and M5Things.status() == 2:
            infos = M5Things.info()
            account = "None" if len(infos[1]) == 0 else "{:s}".format(infos[1])
        else:
            account = "None"

        return (date, mtime, account, ver)


class ListApp(AppBase):
    def __init__(self) -> None:
        super().__init__()

    def on_launch(self):
        self._labels = []
        self._files = []

        for file in os.listdir("apps"):
            if file.endswith(".py"):
                self._files.append(file)

    def on_view(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_pos(0, 12)
        self._bg_img.set_size(80, 148)
        self._bg_img.set_src(APPLIST_IMG)

        if len(self._files) > 0:
            self._label0 = widgets.Label(
                "",
                12,
                65,
                w=52,
                h=15,
                fg_color=0xFFFFFF,
                bg_color=0x343434,
                font=MontserratMedium12_VLW,
            )
            self._label0.set_long_mode(widgets.Label.LONG_DOT)
            self._labels.append(self._label0)
        if len(self._files) > 1:
            self._label1 = widgets.Label(
                "",
                18,
                85,
                w=52,
                h=15,
                fg_color=0x9B9B9B,
                bg_color=0x000000,
                font=MontserratMedium12_VLW,
            )
            self._label1.set_long_mode(widgets.Label.LONG_DOT)
            self._labels.append(self._label1)
        if len(self._files) > 2:
            self._label2 = widgets.Label(
                "",
                18,
                45,
                w=52,
                h=15,
                fg_color=0x9B9B9B,
                bg_color=0x000000,
                font=MontserratMedium12_VLW,
            )
            self._label2.set_long_mode(widgets.Label.LONG_DOT)
            self._labels.append(self._label2)

        for label, file in zip(self._labels, self._files):
            # print("file:", file)
            file and label and label.set_text(file)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        del (
            self._bg_img,
            self._labels,
            self._files,
        )

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        M5.Lcd.clear()
        execfile("/".join(["apps/", self._files[self._file_pos]]), {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        file = self._files.pop(0)
        self._files.append(file)
        for label, file in zip(self._labels, self._files):
            file and label and label.set_text(file)

    @staticmethod
    def approximate(number):
        tolerance = 20
        for v in (0, 20, 40, 60, 80, 100):
            if abs(number - v) < tolerance:
                return v


class CloudApp(AppBase):
    bg_table = {
        0: CLOUD_WAIT_IMG,
        1: CLOUD_CONNECTED_IMG,
        2: CLOUD_ERROR_IMG,
        3: CLOUD_DISCONNECTED_IMG,
        4: CLOUD_READY_IMG,
    }

    def __init__(self, data) -> None:
        self._wifi = data[0]
        self._ssid = str(data[1]) if len(data[1]) else str(None)
        self._server = None
        self._cloud_status = 0

    def _load_data(self):
        self._server = self._get_server()
        self._cloud_status = self._get_cloud_status()

    def _update_data(self):
        self._cloud_status = self._get_cloud_status()

    def on_launch(self):
        self._server = self._get_server()
        self._cloud_status = self._get_cloud_status()

    def on_view(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_pos(0, 12)
        self._bg_img.set_size(80, 148)
        self._bg_img.set_src(self.bg_table.get(self._cloud_status, CLOUD_ERROR_IMG))

        self._ssid_label = widgets.Label(
            "",
            7,
            30,
            w=64,
            h=38,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x1C1C1E,
            font=MontserratMedium10_VLW,
        )
        self._ssid_label.set_text(self._ssid)

        self._server_label = widgets.Label(
            "",
            7,
            90,
            w=64,
            h=38,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x1C1C1E,
            font=MontserratMedium10_VLW,
        )
        self._server_label.set_text(self._server)

    async def on_run(self):
        while True:
            t = self._get_cloud_status()
            if t is not self._cloud_status:
                self._cloud_status = t
                self._bg_img.set_src(self.bg_table.get(self._cloud_status, CLOUD_ERROR_IMG))
                self._ssid_label.set_text(self._ssid)
                self._server_label.set_text(self._server)
                await asyncio.sleep_ms(1000)
            else:
                await asyncio.sleep_ms(1000)

    def on_exit(self):
        del (
            self._ssid_label,
            self._server_label,
            self._bg_img,
        )

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        pass

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        pass

    @staticmethod
    def _get_server():
        nvs = esp32.NVS("uiflow")
        return nvs.get_str("server")

    def _get_cloud_status(self):
        _cloud_status = {
            network.STAT_IDLE: 0,
            network.STAT_CONNECTING: 0,
            network.STAT_GOT_IP: 1,
            network.STAT_NO_AP_FOUND: 2,
            network.STAT_WRONG_PASSWORD: 2,
            network.STAT_BEACON_TIMEOUT: 2,
            network.STAT_ASSOC_FAIL: 2,
            network.STAT_HANDSHAKE_TIMEOUT: 2,
        }[self._wifi.connect_status()]

        if _cloud_status != 1 or _HAS_SERVER is not True:
            return _cloud_status

        if M5Things.status() == 2:
            _cloud_status = 4
        elif M5Things.status() > 2:
            _cloud_status = 3
        return _cloud_status


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


class MenuApp(AppBase):
    def __init__(self, data=None) -> None:
        self._cloud_app = data
        self._menus = (
            (DevApp(None), MENU_DEV_IMG),
            (RunApp(), MENU_APPRUN_IMG),
            (ListApp(), MENU_APPLIST_IMG),
        )

    def on_launch(self):
        self._icos = _charge_ico(self._menus)
        self._app, self._img_src = next(self._icos)

    def on_view(self):
        self._status_img = widgets.Image(use_sprite=False)
        self._status_img.set_pos(0, 12)
        self._status_img.set_size(135, 240)
        self._status_img.set_src(self._img_src)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        if self._app:
            await fw.unload(self)
            await fw.load(self._app)

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        self._app, src = next(self._icos)
        self._status_img.set_src(src)


class StatusBarApp(AppBase):
    def __init__(self, icos: dict, wifi) -> None:
        pass

    def on_launch(self):
        self._time_text = self._get_local_time_text()

    def on_view(self):
        M5.Lcd.fillRect(0, 0, 80, 12, 0x000000)
        self._time_label = widgets.Label(
            "12:23",
            2,
            0,
            w=32,
            font_align=widgets.Label.LEFT_ALIGNED,
            fg_color=0xFFFFFF,
            bg_color=0x000000,
            font=MontserratMedium10_VLW,
        )
        self._time_label.set_text(self._time_text)

        self._battery_img = widgets.Image(use_sprite=False)
        self._battery_img.set_pos(58, 0)
        self._battery_img.set_size(22, 12)
        self._brightness = self.approximate(M5.Power.getBatteryLevel())
        self._battery_img.set_src("{}{}.jpeg".format(BAT_IMG_PATH, self._brightness))

    def on_ready(self):
        pass

    async def on_run(self):
        while True:
            self._time_label.set_text(self._get_local_time_text())
            self._brightness = self.approximate(M5.Power.getBatteryLevel())
            self._battery_img.set_src("{}{}.jpeg".format(BAT_IMG_PATH, self._brightness))
            await asyncio.sleep_ms(5000)

    def on_hide(self):
        pass

    @staticmethod
    def _get_local_time_text():
        struct_time = time.localtime()
        return "{:02d}:{:02d}".format(struct_time[3], struct_time[4])

    @staticmethod
    def approximate(number):
        tolerance = 20
        for v in (0, 20, 40, 60, 80, 100):
            if abs(number - v) < tolerance:
                return v


class LauncherApp(AppBase):
    def __init__(self, data=None) -> None:
        self._cloud_app, self._menu_app = data

    def on_view(self):
        self._bg_img = widgets.Image(use_sprite=False)
        self._bg_img.set_pos(0, 0)
        self._bg_img.set_size(80, 160)
        self._bg_img.set_src(LAUNCHER_IMG)

    def on_exit(self):
        del self._bg_img

    async def _keycode_enter_event_handler(self, fw):
        # print("_keycode_enter_event_handler")
        await fw.unload(self)
        await fw.load(self._cloud_app)

    async def _keycode_back_event_handler(self, fw):
        # print("_keycode_back_event_handler")
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        # print("_keycode_dpad_down_event_handler")
        await fw.unload(self)
        await fw.load(self._menu_app)


class Framework:
    def __init__(self) -> None:
        self._apps = []
        self._launcher = None

    def install_launcher(self, launcher: AppBase):
        self._launcher = launcher

    def install_bar(self, bar: AppBase):
        self._bar = bar

    def install(self, app: AppBase):
        self._apps.append(app)

    async def unload(self, app: AppBase):
        # app = self._apps.pop()
        app.on_hide()

    async def load(self, app: AppBase):
        self._apps.append(app)
        app.on_launch()
        app.on_view()
        app.on_ready()
        self._bar.stop()
        if app is not self._launcher:
            self._bar.start()

    async def reload(self, app: AppBase):
        app.on_hide()
        app.on_ready()

    async def run(self):
        asyncio.create_task(self.load(self._launcher))
        # asyncio.create_task(self.gc_task())
        while True:
            M5.update()
            if M5.BtnA.wasClicked():
                app = self._apps[-1]
                asyncio.create_task(app._keycode_enter_event_handler(self))
            if M5.BtnB.wasClicked():
                app = self._apps[-1]
                asyncio.create_task(app._keycode_dpad_down_event_handler(self))
            if M5.BtnPWR.wasClicked():
                if self._apps and len(self._apps) > 1:
                    app = self._apps.pop()
                    await app._keycode_back_event_handler(self)
                    app.on_hide()
                    app.on_exit()
                    app = self._apps[-1]
                    app.on_launch()
                    app.on_view()
                    app.on_ready()
            await asyncio.sleep_ms(100)

    async def gc_task(self):
        while True:
            gc.collect()
            print("heap RAM free:", gc.mem_free())
            print("heap RAM alloc:", gc.mem_alloc())
            await asyncio.sleep_ms(5000)


class StickC_Startup:
    def __init__(self) -> None:
        self._wifi = Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wifi.connect_network(ssid, pswd)

        M5.Lcd.drawImage(LAUNCHER_IMG)
        M5.Lcd.setBrightness(0)

        for i in range(0, 128, 20):
            M5.Lcd.setBrightness(i)
            time.sleep_ms(80)
        DEBUG and print("Run startup menu")

        statusbar = StatusBarApp(icos=None, wifi=self._wifi)
        cloud_app = CloudApp((self._wifi, ssid))
        menu_app = MenuApp(data=cloud_app)
        launcher = LauncherApp(data=(cloud_app, menu_app))

        fw = Framework()
        fw.install_launcher(launcher)
        fw.install_bar(statusbar)
        asyncio.run(fw.run())

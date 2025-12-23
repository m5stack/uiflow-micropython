# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# UnitC6L startup script
import M5
import time
import network
import machine
import binascii
import os
import sys
import gc
import asyncio
import esp32
from . import Startup

try:
    import M5Things

    _HAS_SERVER = True
except ImportError:
    _HAS_SERVER = False


def _draw_textbox(x, y, w, h, r, text, invert=False, is_title=False):
    max_chars = 8
    if len(text) > max_chars:
        if is_title:
            text = text[:3] + "..." + text[-3:]
        else:
            text = text[:3] + ".." + text[-3:]
    M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu9)
    text_w = M5.Lcd.textWidth(text)
    cursor_x = x + (w - text_w) // 2
    cursor_y = y + (5 if is_title else 3)
    M5.Lcd.setCursor(cursor_x, cursor_y)
    if invert:
        M5.Lcd.fillRoundRect(x, y, w, h, r, M5.Lcd.COLOR.WHITE)
        M5.Lcd.setTextColor(M5.Lcd.COLOR.BLACK, M5.Lcd.COLOR.WHITE)
    else:
        M5.Lcd.fillRoundRect(x, y, w, h, r, M5.Lcd.COLOR.BLACK)
        M5.Lcd.drawRoundRect(x, y, w, h, r, M5.Lcd.COLOR.WHITE)
        M5.Lcd.setTextColor(M5.Lcd.COLOR.WHITE, M5.Lcd.COLOR.BLACK)
    M5.Lcd.print(text)


def title_set_text(text, invert=False):
    _draw_textbox(0, -3, 64, 18, 4, text, invert, is_title=True)


def label1_set_text(text, invert=False):
    _draw_textbox(3, 16, 58, 15, 4, text, invert, is_title=False)


def label2_set_text(text, invert=False):
    _draw_textbox(3, 32, 58, 15, 4, text, invert, is_title=False)


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
        if self._task:
            self._task.cancel()

    def on_exit(self):
        pass

    async def _keycode_enter_event_handler(self, fw):
        pass

    async def _keycode_back_event_handler(self, fw):
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        pass

    def set_internal_mode(self, in_internal: bool):
        pass


# CloudApp - 显示网络连接状态和云服务状态
class CloudApp(AppBase):
    def __init__(self, wifi, ssid) -> None:
        super().__init__()
        self._wifi = wifi
        self._ssid = ssid
        self._cloud_status = 0

    def on_launch(self):
        self._cloud_status = self._get_cloud_status()
        self._internal = False

    def on_view(self):
        M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
        title_set_text("Cloud", False)
        label1_set_text(str(self._ssid) if self._ssid else "None", self._internal)
        status = self._wifi.connect_status()
        status_text = {
            network.STAT_GOT_IP: "CONNECTED",
            network.STAT_CONNECTING: "CONNECTING",
            network.STAT_NO_AP_FOUND: "NO AP",
            network.STAT_WRONG_PASSWORD: "WRONG PSK",
            network.STAT_HANDSHAKE_TIMEOUT: "HANDSHAKE ERR",
        }.get(status, "DISCONNECTED")
        label2_set_text(status_text, self._internal)

    async def on_run(self):
        while True:
            status = self._wifi.connect_status()
            if status != self._cloud_status:
                self._cloud_status = status
                status_text = {
                    network.STAT_GOT_IP: "CONNECTED",
                    network.STAT_CONNECTING: "CONNECTING",
                    network.STAT_NO_AP_FOUND: "NO AP",
                    network.STAT_WRONG_PASSWORD: "WRONG PSK",
                    network.STAT_HANDSHAKE_TIMEOUT: "HANDSHAKE ERR",
                }.get(status, "DISCONNECTED")
                label2_set_text(status_text, self._internal)
            await asyncio.sleep_ms(1000)

    def set_internal_mode(self, in_internal: bool):
        self._internal = in_internal
        label1_set_text(str(self._ssid) if self._ssid else "None", self._internal)
        status = self._wifi.connect_status()
        status_text = {
            network.STAT_GOT_IP: "CONNECTED",
            network.STAT_CONNECTING: "CONNECTING",
            network.STAT_NO_AP_FOUND: "NO AP",
            network.STAT_WRONG_PASSWORD: "WRONG PSK",
            network.STAT_HANDSHAKE_TIMEOUT: "HANDSHAKE ERR",
        }.get(status, "DISCONNECTED")
        label2_set_text(status_text, self._internal)

    def _get_cloud_status(self):
        if self._wifi.connect_status() != network.STAT_GOT_IP:
            return 0
        if _HAS_SERVER and M5Things.status() == 2:
            return 1
        return 0


# RunApp - 显示 main.py 文件信息并提供运行选项
class RunApp(AppBase):
    def __init__(self) -> None:
        super().__init__()
        self._run_mode = 0  # 0: run once, 1: run always

    def on_launch(self):
        self._mtime_text, self._account_text, self._ver_text = self._get_file_info("main.py")

    def on_view(self):
        M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
        title_set_text("main.py", False)
        label1_set_text("RUN ONCE", self._run_mode == 0)
        label2_set_text("ALWAYS", self._run_mode == 1)

    async def _keycode_dpad_down_event_handler(self, fw):
        self._run_mode = (self._run_mode + 1) % 2
        self.on_view()

    async def _keycode_enter_event_handler(self, fw):
        if self._run_mode == 0:
            # Run once
            M5.Lcd.clear(0xFFFFFF)
            execfile("main.py", {"__name__": "__main__"})
            raise KeyboardInterrupt
        else:
            # Run always
            M5.Lcd.clear(0xFFFFFF)
            nvs = esp32.NVS("uiflow")
            nvs.set_u8("boot_option", 2)
            nvs.commit()
            machine.reset()

    @staticmethod
    def _get_file_info(path):
        mtime = None
        account = None
        ver = f"UIFLOW2 {esp32.firmware_info()[3]}"

        try:
            stat = os.stat(path)
            mtime = time.localtime(stat[8])
        except OSError:
            pass

        if mtime is None or mtime[0] < 2024:
            mtime = "----/--/--"
        else:
            mtime = "{:04d}/{:d}/{:d}".format(mtime[0] - 2000, mtime[1], mtime[2])

        if account is None and _HAS_SERVER and M5Things.status() == 2:
            infos = M5Things.info()
            account = "None" if len(infos[1]) == 0 else infos[1]
        else:
            account = "None"

        return (mtime, account, ver)


# ListApp - 显示 apps 目录下的应用列表
class ListApp(AppBase):
    def __init__(self) -> None:
        super().__init__()
        self._files = []
        self._file_pos = 0

    def on_launch(self):
        self._files = []
        try:
            for file in os.listdir("apps"):
                if file.endswith(".py"):
                    self._files.append(file)
        except OSError:
            pass

    def on_view(self):
        M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
        title_set_text("LIST.APP", False)

        if len(self._files) > 0:
            current_file = self._files[self._file_pos]
            if len(current_file) > 8:
                current_file = current_file[:5] + "..."
            label1_set_text(current_file, True)

            if len(self._files) > 1:
                next_file = self._files[(self._file_pos + 1) % len(self._files)]
                if len(next_file) > 8:
                    next_file = next_file[:5] + "..."
                label2_set_text(next_file, False)
            else:
                label2_set_text("", False)
        else:
            label1_set_text("No Apps", False)
            label2_set_text("", False)

    async def _keycode_dpad_down_event_handler(self, fw):
        if len(self._files) > 0:
            self._file_pos = (self._file_pos + 1) % len(self._files)
            self.on_view()

    async def _keycode_enter_event_handler(self, fw):
        if len(self._files) > 0:
            M5.Lcd.clear(0xFFFFFF)
            execfile("/".join(["apps/", self._files[self._file_pos]]), {"__name__": "__main__"})  # noqa: F821
            raise KeyboardInterrupt


# 框架类 - 直接管理3个app的切换
class Framework:
    def __init__(self, cloud_app, run_app, list_app) -> None:
        self._apps = [cloud_app, run_app, list_app]
        self._app_names = ["Cloud", "main.py", "LIST.APP"]
        self._current_app_index = 0
        self._current_app = None
        self._in_app_mode = False  # False: 切换app模式, True: app内部模式
        self._last_click_time = 0
        self._click_count = 0
        # 单击/双击判定
        self._pending_single = False
        self._last_click_ms = 0
        self._double_window_ms = 350
        # 长按判定
        self._pressing = False
        self._press_start_ms = 0
        self._long_fired = False

    async def start(self):
        """启动框架，显示第一个app"""
        self._current_app = self._apps[self._current_app_index]
        self._current_app.on_launch()
        self._current_app.on_view()
        self._current_app.on_ready()
        # 开机默认处于 app 切换模式：单击在三个 app 之间切换
        self._in_app_mode = False
        self._update_display()
        await self.run()

    async def run(self):
        while True:
            M5.update()
            now_ms = time.ticks_ms()
            if M5.BtnA.wasClicked():
                try:
                    M5.Speaker.tone(666, 100)
                except Exception:
                    pass
                # 延迟触发单击：先记录第一次点击，窗口内再次点击视为双击
                if (
                    self._pending_single
                    and time.ticks_diff(now_ms, self._last_click_ms) <= self._double_window_ms
                ):
                    # 双击：取消单击，执行双击动作
                    self._pending_single = False
                    if not self._in_app_mode:
                        self._in_app_mode = True
                        self._update_display()
                        if hasattr(self._current_app, "set_internal_mode"):
                            try:
                                self._current_app.set_internal_mode(True)
                            except Exception:
                                pass
                    else:
                        await self._current_app._keycode_enter_event_handler(self)
                else:
                    # 记录首次点击，等待窗口超时来判定单击
                    self._pending_single = True
                    self._last_click_ms = now_ms

            # 处理长按事件 - 使用持续按下时间判定，避免与单击冲突
            if M5.BtnA.isPressed():
                if not self._pressing:
                    self._pressing = True
                    self._press_start_ms = now_ms
                    self._long_fired = False
                else:
                    if (
                        not self._long_fired
                        and time.ticks_diff(now_ms, self._press_start_ms) > 700
                    ):
                        self._long_fired = True
                        if self._in_app_mode:
                            try:
                                M5.Speaker.tone(666, 200)
                            except Exception:
                                pass
                            self._in_app_mode = False
                            self._pending_single = False
                            self._update_display()
                            if hasattr(self._current_app, "set_internal_mode"):
                                try:
                                    self._current_app.set_internal_mode(False)
                                except Exception:
                                    pass
            else:
                self._pressing = False
                self._long_fired = False

            # 单击延迟触发：超过双击窗口且仍挂起，则执行单击动作
            if (
                self._pending_single
                and time.ticks_diff(now_ms, self._last_click_ms) > self._double_window_ms
            ):
                if not self._in_app_mode:
                    await self._switch_to_next_app()
                else:
                    await self._current_app._keycode_dpad_down_event_handler(self)
                    self._update_display()
                self._pending_single = False

            await asyncio.sleep_ms(100)

    async def _switch_to_next_app(self):
        """切换到下一个app"""
        if self._current_app:
            self._current_app.on_hide()
        self._current_app_index = (self._current_app_index + 1) % len(self._apps)
        self._current_app = self._apps[self._current_app_index]
        self._in_app_mode = False
        self._current_app.on_launch()
        self._current_app.on_view()
        self._current_app.on_ready()

    def _update_display(self):
        """更新显示，根据模式显示不同的标题状态"""
        if self._current_app:
            if self._in_app_mode:
                title_set_text(self._app_names[self._current_app_index], True)
            else:
                title_set_text(self._app_names[self._current_app_index], False)


# UnitC6L startup menu
class UnitC6L_Startup(Startup):
    def __init__(self) -> None:
        super().__init__()

    def show_hits(self, hits: str) -> None:
        print(hits)

    def show_msg(self, msg: str) -> None:
        print(msg)

    def show_ssid(self, ssid: str) -> None:
        if len(ssid) > 9:
            self.show_msg(ssid[:7] + "...")
        else:
            self.show_msg(ssid)

    def show_mac(self) -> None:
        mac = binascii.hexlify(machine.unique_id()).decode("utf-8").upper()
        print(mac[0:6] + "_" + mac[6:])

    def show_error(self, ssid: str, error: str) -> None:
        self.show_ssid(ssid)
        self.show_hits(error)
        self.show_mac()
        print("SSID: " + ssid + "\r\nNotice: " + error)

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
        M5.Speaker.begin()
        M5.Speaker.setVolumePercentage(1)
        # 显示启动画面
        M5.Lcd.fillRect(0, 0, 64, 48, M5.Lcd.COLOR.BLACK)
        M5.Lcd.setFont(M5.Lcd.FONTS.DejaVu12)
        M5.Lcd.fillRect(0, 0, 64, 15, M5.Lcd.COLOR.WHITE)
        M5.Lcd.setTextColor(M5.Lcd.COLOR.BLACK, M5.Lcd.COLOR.WHITE)
        M5.Lcd.drawCenterString("UiFlow2", 32, 2)
        M5.Lcd.setTextColor(M5.Lcd.COLOR.WHITE, M5.Lcd.COLOR.BLACK)
        M5.Lcd.drawCenterString("Unit C6L", 32, 26)
        M5.Speaker.tone(888, 200)
        self.show_mac()
        # 连接网络
        if super().connect_network(
            ssid=ssid,
            pswd=pswd,
            protocol=protocol,
            ip=ip,
            netmask=netmask,
            gateway=gateway,
            dns=dns,
        ):
            self.show_ssid(ssid)
            count = 1
            status = super().connect_status()
            start = time.time()
            while status is not network.STAT_GOT_IP:
                time.sleep_ms(300)
                if status is network.STAT_NO_AP_FOUND:
                    self.show_error(ssid, "NO AP FOUND")
                    break
                elif status is network.STAT_WRONG_PASSWORD:
                    self.show_error(ssid, "WRONG PASSWORD")
                    break
                elif status is network.STAT_HANDSHAKE_TIMEOUT:
                    self.show_error(ssid, "HANDSHAKE ERR")
                    break
                elif status is network.STAT_CONNECTING:
                    self.show_hits("." * count)
                    count = count + 1
                    if count > 5:
                        count = 1
                status = super().connect_status()
                # connect to network timeout
                if (time.time() - start) > timeout:
                    self.show_error(ssid, "TIMEOUT")
                    break

            if status is network.STAT_GOT_IP:
                self.show_hits(super().local_ip())
                print("Local IP: " + super().local_ip())
        else:
            self.show_error("Not Found", "Use Burner setup")
        self._start_menu_system(ssid)

    def _start_menu_system(self, ssid):
        """启动app切换系统"""
        try:
            cloud_app = CloudApp(self, ssid)
            run_app = RunApp()
            list_app = ListApp()
            fw = Framework(cloud_app, run_app, list_app)
            asyncio.run(fw.start())
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"App system error: {e}")

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


def charge_ico(icos):
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


class WiFiSetting(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self.x = 4
        self.y = 20 + 4 + 56 + 4
        self.w = 312
        self.h = 108
        self._ssid_label = Label(
            "ssid",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12,
            w=180,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._pwd_label = Label(
            "pwd",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12 + 35,
            w=180,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._server_label = Label(
            "server",
            4 + 56 + 2,
            20 + 4 + 56 + 4 + 12 + 35 + 34,
            w=190,
            font_align=Label.LEFT_ALIGNED,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=MontserratMedium16.FONT,
        )
        self._apps = [
            Rect(4, 20 + 4 + 56 + 4, 244, 108),  # option select
            Rect(4 + 249, 20 + 4 + 56 + 4, 63, 64),  # save & link
            Rect(4 + 249, 20 + 4 + 56 + 4 + 64, 63, 44),  # option select
        ]
        self._option_views = charge_ico(
            (
                (0, self._select_ssid_option),
                (1, self._select_psd_option),
                (2, self._select_server_option),
            )
        )
        self._app_layout = (
            (self._apps[0],),
            (self._apps[1],),
        )
        self._cursor_row = 0
        self._cursor_col = 0
        self._option = -1
        self._wifi = data
        self.focus = False

    def mount(self):
        self.get_data()
        self._select_default_option()

    def _select_default_option(self):
        _draw_png("res/sys/cores3/Setting/wifiServer.png")
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * 20)
        self._server_label.setText(self.server_tmp)

    def _select_ssid_option(self):
        _draw_png("res/sys/cores3/Setting/ssid.png")
        self._ssid_label.setTextColor(0x000000, 0xDCDDDD)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * 20)
        self._server_label.setText(self.server_tmp)

    def _select_psd_option(self):
        _draw_png("res/sys/cores3/Setting/pass.png")
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xDCDDDD)
        self._server_label.setTextColor(0x000000, 0xFEFEFE)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * 20)
        self._server_label.setText(self.server_tmp)

    def _select_server_option(self):
        _draw_png("res/sys/cores3/Setting/server.png")
        self._ssid_label.setTextColor(0x000000, 0xFEFEFE)
        self._pwd_label.setTextColor(0x000000, 0xFEFEFE)
        self._server_label.setTextColor(0x000000, 0xDCDDDD)
        self._ssid_label.setText(self.ssid_tmp)
        self._pwd_label.setText("*" * 20)
        self._server_label.setText(self.server_tmp)

    def get_data(self):
        self.nvs = esp32.NVS("uiflow")
        self.ssid = self.nvs.get_str("ssid0")
        self.pswd = self.nvs.get_str("pswd0")
        self.server = self.nvs.get_str("server")
        self.ssid_tmp = self.ssid
        self.pswd_tmp = self.pswd
        self.server_tmp = self.server

    def set_data(self):
        is_save = False
        if self.ssid != self.ssid_tmp:
            self.ssid = self.ssid_tmp
            self.nvs.set_str("ssid0", self.ssid)
            DEBUG and print("set new ssid: ", self.ssid)
            is_save = True
        if self.pswd != self.pswd_tmp:
            self.pswd = self.pswd_tmp
            self.nvs.set_str("pswd0", self.pswd)
            DEBUG and print("set new ssid: ", self.ssid)
            is_save = True
        if self.server != self.server_tmp:
            self.server = self.server_tmp
            self.nvs.set_str("server", self.server)
            DEBUG and print("set new server: ", self.server)
            is_save = True

        if is_save is True:
            self.nvs.commit()
            self._wifi.wlan.disconnect()
            self._wifi.wlan.active(False)
            self._wifi.wlan.active(True)
            self._wifi.connect_network(self.ssid, self.pswd)

    def handle(self, x, y):
        if self.is_select_option(self._apps[0], x, y):
            self._option, view_fn = next(self._option_views)
            view_fn()
        elif self.is_select_option(self._apps[1], x, y):
            self._select_default_option()
            self.set_data()
        if self.is_select_option(self._apps[2], x, y):
            self._option, view_fn = next(self._option_views)
            view_fn()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            event.status = True
            self.focus = True
            self._option, view_fn = next(self._option_views)
            view_fn()

        if self.focus is False:
            return

        if event.key == KeyCode.KEYCODE_ESC:
            self.ssid_tmp = self.ssid
            self.pswd_tmp = self.pswd
            self.server_tmp = self.server
            self._select_default_option()
            self.focus = False
            event.status = True

        if event.key == KeyCode.KEYCODE_BACKSPACE and self._option in (0, 1, 2):
            if self._option == 0:
                self.ssid_tmp = self.ssid_tmp[:-1]
                self._ssid_label.setText(self.ssid_tmp)
            elif self._option == 1:
                if self.pswd_tmp == self.pswd:
                    self.pswd_tmp = ""
                else:
                    self.pswd_tmp = self.pswd_tmp[:-1]
                self._pwd_label.setText(self.pswd_tmp)
            elif self._option == 2:
                self.server_tmp = self.server_tmp[:-1]
                self._server_label.setText(self.server_tmp)
            event.status = True

        if event.key in (
            KeyCode.KEYCODE_DOWN,
            KeyCode.KEYCODE_RIGHT,
            KeyCode.KEYCODE_LEFT,
            KeyCode.KEYCODE_UP,
        ):
            if event.key == KeyCode.KEYCODE_DOWN:
                self._cursor_row += 1
                self._cursor_col = 0
            if event.key == KeyCode.KEYCODE_RIGHT:
                self._cursor_col += 1
            if event.key == KeyCode.KEYCODE_LEFT:
                self._cursor_col -= 1
            if event.key == KeyCode.KEYCODE_UP:
                self._cursor_row -= 1
                self._cursor_col = 0
            if event.key == KeyCode.KEYCODE_ESC:
                self._cursor_row = 0
                self._cursor_col = 0

            if self._cursor_row >= len(self._app_layout):
                self._cursor_row = len(self._app_layout) - 1
            if self._cursor_row < 0:
                self._cursor_row = 0

            if self._cursor_col >= 0:
                self._cursor_col = self._cursor_col % len(self._app_layout[self._cursor_row])
            if self._cursor_col < 0:
                self._cursor_col = len(self._app_layout[self._cursor_row]) - 1

            if self._cursor_col == 1:
                self._select_default_option()
                self.set_data()
            event.status = True
        elif event.key >= 0x20 and event.key <= 126:
            if self._option == 0:
                self.ssid_tmp += chr(event.key)
                self._ssid_label.setText(self.ssid_tmp)
            elif self._option == 1:
                if self.pswd_tmp == self.pswd:
                    self.pswd_tmp = ""
                else:
                    self.pswd_tmp += chr(event.key)
                self._pwd_label.setText(self.pswd_tmp)
            elif self._option == 2:
                self.server_tmp += chr(event.key)
                self._server_label.setText(self.server_tmp)
            event.status = True

    def umount(self) -> None:
        self._select_default_option()

    @staticmethod
    def is_select_option(rect: Rect, x, y):
        if x < rect.x:
            return False
        if x > (rect.x + rect.w):
            return False
        if y < rect.y:
            return False
        if y > (rect.y + rect.h):
            return False
        return True


CURRENT_OPTION = (
    (
        100,
        ImageDesc1(
            src="res/sys/cores3/Setting/charge100.png",
            x=4,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        500,
        ImageDesc1(
            src="res/sys/cores3/Setting/charge500.png",
            x=4,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        900,
        ImageDesc1(
            src="res/sys/cores3/Setting/charge900.png",
            x=4,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        1000,
        ImageDesc1(
            src="res/sys/cores3/Setting/charge1000.png",
            x=4,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    # (1500, ImageDesc1(src="res/sys/cores3/Setting/charge1500.png", x=4, y=20 + 4 + 56 + 4 + 108 + 4, w=60, h=44)),
    # (2000, ImageDesc1(src="res/sys/cores3/Setting/charge2000.png", x=4, y=20 + 4 + 56 + 4 + 108 + 4, w=60, h=44)),
)


class BatteryChargeSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = charge_ico(CURRENT_OPTION)
        self._current, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        self.get_data()
        while True:
            current, self.descriptor = next(self.icos)
            if current == self._current:
                break
        _draw_image(self.descriptor)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._current, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._current, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def get_data(self):
        self.nvs = esp32.NVS("uiflow")
        try:
            self._current = self.nvs.get_i32("charge_current")
        except OSError:
            self._current = 500

    def set_data(self):
        M5.Power.setBatteryCharge(True)
        M5.Power.setChargeCurrent(self._current)
        self.nvs.set_i32("charge_current", self._current)
        self.nvs.commit()

    def umount(self) -> None:
        pass


BOOT_OPTION = (
    (
        0,
        ImageDesc1(
            src="res/sys/cores3/Setting/bootNo.png",
            x=4 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        1,
        ImageDesc1(
            src="res/sys/cores3/Setting/bootYes.png",
            x=4 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
)


class BootScreenSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = charge_ico(BOOT_OPTION)
        self.boot_option, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        self.get_data()
        while True:
            boot_option, self.descriptor = next(self.icos)
            if boot_option == self.boot_option:
                break
        self._load_view()

    def _load_view(self):
        _draw_image(self.descriptor)

    def handle(self, x, y):
        if self.is_select(x, y):
            self.boot_option, self.descriptor = next(self.icos)
            self._load_view()
            self.set_data()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self.boot_option, self.descriptor = next(self.icos)
            self._load_view()
            self.set_data()

    def get_data(self):
        nvs = esp32.NVS("uiflow")
        self.boot_option = nvs.get_u8("boot_option")

    def set_data(self):
        nvs = esp32.NVS("uiflow")
        boot_option = nvs.set_u8("boot_option", self.boot_option)
        nvs.commit()
        return boot_option

    def umount(self) -> None:
        pass


class ComLinkSetting(AppBase):
    # TODO

    def __init__(self, icos: dict) -> None:
        self.icos = charge_ico(
            (
                "res/sys/cores3/Setting/comxEnable.png",
                "res/sys/cores3/Setting/comxDisable.png",
            )
        )
        self.src = next(self.icos)
        self.descriptor = _IMAGE_LIST.get(self.src)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        _draw_png(self.src)

    def handle(self, x, y):
        if self.is_select(x, y):
            self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self.src = next(self.icos)
            self.descriptor = _IMAGE_LIST.get(self.src)
            self.mount()

    def umount(self) -> None:
        pass


USBPOWER_OPTION = (
    (
        False,
        ImageDesc1(
            src="res/sys/cores3/Setting/usbInput.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        True,
        ImageDesc1(
            src="res/sys/cores3/Setting/usbOutput.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
)


class USBPowerSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = charge_ico(USBPOWER_OPTION)
        self._data, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        self.get_data()
        while True:
            data, self.descriptor = next(self.icos)
            if data == self._data:
                break
        _draw_image(self.descriptor)

    def get_data(self):
        self._data = M5.Power.getUsbOutput()

    def set_data(self):
        M5.Power.setUsbOutput(self._data)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._data, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._data, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def umount(self) -> None:
        pass


BUSPOWER_OPTION = (
    (
        False,
        ImageDesc1(
            src="res/sys/cores3/Setting/busInput.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
    (
        True,
        ImageDesc1(
            src="res/sys/cores3/Setting/busOutput.png",
            x=4 + 60 + 3 + 60 + 3 + 60 + 3 + 60 + 3,
            y=20 + 4 + 56 + 4 + 108 + 4,
            w=60,
            h=44,
        ),
    ),
)


class BUSPowerSetting(AppBase):
    def __init__(self, icos: dict) -> None:
        self.icos = charge_ico(BUSPOWER_OPTION)
        self._data, self.descriptor = next(self.icos)
        self.x = self.descriptor.x
        self.y = self.descriptor.y
        self.w = self.descriptor.w
        self.h = self.descriptor.h

    def mount(self):
        self.get_data()
        while True:
            data, self.descriptor = next(self.icos)
            if data == self._data:
                break
        _draw_image(self.descriptor)

    def get_data(self):
        self._data = M5.Power.getExtOutput()

    def set_data(self):
        M5.Power.setExtOutput(self._data)

    def handle(self, x, y):
        if self.is_select(x, y):
            self._data, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def handle_input(self, event: KeyEvent):
        if event.key == KeyCode.KEYCODE_ENTER:
            self._data, self.descriptor = next(self.icos)
            self.set_data()
            self.mount()

    def umount(self) -> None:
        pass


class SettingsApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        self.icos = icos
        self.descriptor = self.icos.get(False)
        self._apps = [
            WiFiSetting(None, data=data),
            BatteryChargeSetting(None),
            BootScreenSetting(None),
            ComLinkSetting(None),
            USBPowerSetting(None),
            BUSPowerSetting(None),
        ]

        self._app_layout = (
            (self._apps[0],),
            (
                self._apps[1],
                self._apps[2],
                self._apps[3],
                self._apps[4],
                self._apps[5],
            ),
        )
        self._cursor_row = 0
        self._cursor_col = 0
        self._focus = True

    def mount(self):
        _draw_image(self.icos.get(True))
        for app in self._apps:
            app.mount()

    def handle(self, x, y):
        app = None
        for app in self._apps:
            if app.is_select(x, y):
                break

        if app is not None:
            app.handle(x, y)

    def handle_input(self, event: KeyEvent):
        self._app_layout[self._cursor_row][self._cursor_col].handle_input(event)

        if event.status is True:
            return

        if event.key == KeyCode.KEYCODE_DOWN:
            self._cursor_row += 1
            self._cursor_col = 0
            event.status = True
        if event.key == KeyCode.KEYCODE_RIGHT:
            self._cursor_col += 1
            event.status = True
        if event.key == KeyCode.KEYCODE_LEFT:
            self._cursor_col -= 1
            event.status = True
        if event.key == KeyCode.KEYCODE_UP:
            self._cursor_row -= 1
            self._cursor_col = 0
            event.status = True
        if event.key == KeyCode.KEYCODE_ESC:
            self._cursor_row = 0
            self._cursor_col = 0

        if self._cursor_row >= len(self._app_layout):
            self._cursor_row = len(self._app_layout) - 1
        if self._cursor_row < 0:
            self._cursor_row = 0

        if self._cursor_col >= 0:
            self._cursor_col = self._cursor_col % len(self._app_layout[self._cursor_row])
        if self._cursor_col < 0:
            self._cursor_col = len(self._app_layout[self._cursor_row]) - 1

    def umount(self) -> None:
        for app in self._apps:
            app.umount()
        _draw_image(self.icos.get(False))
        M5.Lcd.fillRect(0, 80, 320, 160, 0x000000)

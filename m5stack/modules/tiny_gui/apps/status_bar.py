# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
class StatusBarApp:
    def __init__(self, icos: dict, wifi) -> None:
        self.id = 0
        self.x = 0
        self.y = 0
        self.w = 320
        self.h = 20

        self._wifi = wifi
        self._time_label = Label(
            "12:23",
            160,
            2,
            w=312,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xEEEEEF,
            font=MontserratMedium16.FONT,
        )
        self._battery_label = Label(
            "78%",
            320 - 56 + 22,
            4,
            w=312,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x534D4C,
            bg_color=0xFEFEFE,
            font=MontserratMedium10.FONT,
        )
        self._wifi_status = WiFiStatus.INIT
        if _HAS_SERVER is False:
            self._server_status = ServerStatus.DISCONNECTED

    def registered(self):
        pass

    def mount(self):
        self._load_view()

    def _load_view(self):
        _draw_png("res/sys/cores3/Title/title_blue.png")
        self.handle(None, None)

    def _update_time(self, struct_time):
        self._time_label.setText("{:02d}:{:02d}".format(struct_time[3], struct_time[4]))

    def _update_wifi(self, status):
        self._wifi_status = status
        src = _WIFI_STATUS_ICO.get(self._wifi_status, "res/sys/cores3/WiFi/wifi_empty.png")
        _draw_png(src)

    def _update_server(self, status):
        self._server_status = status
        src = _SERVER_STATUS_ICO.get(self._server_status, "res/sys/cores3/Server/server_error.png")
        _draw_png(src)

    def _update_battery(self, battery, charging):
        src = ""
        if battery > 0 and battery <= 100:
            if battery < 20:
                src = (
                    "res/sys/cores3/Battery/battery_Red_Charge.png"
                    if charging
                    else "res/sys/cores3/Battery/battery_Red.png"
                )
            elif battery <= 100:
                src = (
                    "res/sys/cores3/Battery/battery_Green_Charge.png"
                    if charging
                    else "res/sys/cores3/Battery/battery_Green.png"
                )
            _draw_png(src)
            self._battery_label.setText("{:d}%".format(battery))
        else:
            src = (
                "res/sys/cores3/Battery/battery_Black_Charge.png"
                if charging
                else "res/sys/cores3/Battery/battery_Black.png"
            )
            _draw_png(src)

    @staticmethod
    def get_local_time():
        return time.localtime()

    def get_wifi_status(self):
        status = self._wifi.connect_status()
        if status is network.STAT_GOT_IP:
            rssi = self._wifi.get_rssi()
            if rssi <= -80:
                return WiFiStatus.RSSI_WORSE
            elif rssi <= -60:
                return WiFiStatus.RSSI_MID
            else:
                return WiFiStatus.RSSI_GOOD
        else:
            return WiFiStatus.DISCONNECTED

    @staticmethod
    def get_server_status():
        if _HAS_SERVER is True:
            status = M5Things.status()
            DEBUG and print(
                "Server connect status: %d(%s)" % (status, M5THINGS_STATUS.get(status))
            )
            if status in (0, 1):
                return ServerStatus.INIT
            elif status == 2:
                return ServerStatus.CONNECTED
            elif status in (-2, -1, 3):
                return ServerStatus.DISCONNECTED
        else:
            return ServerStatus.DISCONNECTED

    # def get_battery_status(self):
    #     return M5.Power.getBatteryLevel(), M5.Power.isCharging()

    def handle(self, x, y):
        self._update_time(self.get_local_time())
        self._update_wifi(self.get_wifi_status())
        self._update_server(self.get_server_status())
        self._update_battery(M5.Power.getBatteryLevel(), M5.Power.isCharging())

    def umount(self):
        pass

    def _disappear_view(self):
        pass

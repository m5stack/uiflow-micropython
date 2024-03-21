# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "BATTERY_BLACK_CHARGE_IMG": "/system/fire/Battery/battery_Black_Charge.png",
    "BATTERY_BLACK_IMG": "/system/fire/Battery/battery_Black.png",
    "BATTERY_GRAY_IMG": "/system/fire/Battery/battery_Gray.png",
    "BATTERY_GREEN_CHARGE_IMG": "/system/fire/Battery/battery_Green_Charge.png",
    "BATTERY_GREEN_IMG": "/system/fire/Battery/battery_Green.png",
    "BATTERY_RED_CHARGE_IMG": "/system/fire/Battery/battery_Red_Charge.png",
    "BATTERY_RED_IMG": "/system/fire/Battery/battery_Red.png",
    "BATTERY_YELLOW_IMG": "/system/fire/Battery/battery_Yellow.png",
    "SERVER_BLUE_IMG": "/system/fire/Server/server_blue.png",
    "SERVER_EMPTY_IMG": "/system/fire/Server/server_empty.png",
    "SERVER_ERROR_IMG": "/system/fire/Server/server_error.png",
    "SERVER_GREEN_IMG": "/system/fire/Server/Server_Green.png",
    "SERVER_RED_IMG": "/system/fire/Server/server_red.png",
    "WIFI_DISCONNECTED_IMG": "/system/fire/WiFi/wifi_disconnected.png",
    "WIFI_EMPTY_IMG": "/system/fire/WiFi/wifi_empty.png",
    "WIFI_GOOD_IMG": "/system/fire/WiFi/wifi_good.png",
    "WIFI_MID_IMG": "/system/fire/WiFi/wifi_mid.png",
    "WIFI_WORSE_IMG": "/system/fire/WiFi/wifi_worse.png",
    "APPLIST_SELECTED_IMG": "/system/fire/appList_selected.png",
    "APPLIST_UNSELECTED_IMG": "/system/fire/appList_unselected.png",
    "APPLIST_IMG": "/system/fire/applist.png",
    "APPLIST_LEFT_IMG": "/system/fire/applistLeft.png",
    "APPLIST_RIGHT_IMG": "/system/fire/applistRight.png",
    "APPRUN_SELECTED_IMG": "/system/fire/appRun_selected.png",
    "APPRUN_UNSELECTED_IMG": "/system/fire/appRun_unselected.png",
    "BAR1_IMG": "/system/fire/bar1.png",
    "BAR2_IMG": "/system/fire/bar2.png",
    "BAR3_IMG": "/system/fire/bar3.png",
    "BAR4_IMG": "/system/fire/bar4.png",
    "BAR5_IMG": "/system/fire/bar5.png",
    "BOOT_NO_IMG": "/system/fire/boot_No.png",
    "BOOT_YES_IMG": "/system/fire/boot_Yes.png",
    "DEVELOP_SELECTED_IMG": "/system/fire/develop_selected.png",
    "DEVELOP_UNSELECTED_IMG": "/system/fire/develop_unselected.png",
    "DEVELOP_PRIVATE_IMG": "/system/fire/developPrivate.png",
    "DEVELOP_PUBLIC_IMG": "/system/fire/developPublic.png",
    "EZDATA_SELECTED_IMG": "/system/fire/ezdata_selected.png",
    "EZDATA_UNSELECTED_IMG": "/system/fire/ezdata_unselected.png",
    "LOGO_IMG": "/system/fire/logo.png",
    "RUN_IMG": "/system/fire/run.png",
    "SCREEN25_IMG": "/system/fire/screen25.png",
    "SCREEN50_IMG": "/system/fire/screen50.png",
    "SCREEN75_IMG": "/system/fire/screen75.png",
    "SCREEN100_IMG": "/system/fire/screen100.png",
    "SETTING_SELECTED_IMG": "/system/fire/setting_selected.png",
    "SETTING_UNSELECTED_IMG": "/system/fire/setting_unselected.png",
    "SETTING_SELECT_IMG": "/system/fire/settingSelect.png",
    "SETTING_UNSELECT_IMG": "/system/fire/settingUnselect.png",
    "SETTING_WIFI_IMG": "/system/fire/SettingWifi.png",
}


def __getattr__(attr):
    value = _attrs.get(attr, None)
    if value is None:
        raise AttributeError(attr)
    globals()[attr] = value
    return value

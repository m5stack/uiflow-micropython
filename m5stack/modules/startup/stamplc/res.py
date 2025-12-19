# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "LOGO_IMG": "/system/stamplc/boot/boot_logo_1.jpeg",
    # apprun
    "RUN_INFO_IMG": "/system/stamplc/apprun/run_info.jpeg",
    "RUN_ONCE_SELECT_IMG": "/system/stamplc/apprun/run_once_select.jpeg",
    "RUN_ONCE_UNSELECT_IMG": "/system/stamplc/apprun/run_once_unselect.jpeg",
    "RUN_ALWAYS_SELECT_IMG": "/system/stamplc/apprun/run_always_select.jpeg",
    "RUN_ALWAYS_UNSELECT_IMG": "/system/stamplc/apprun/run_always_unselect.jpeg",
    # develop
    "DEVELOP_PRIVATE_IMG": "/system/stamplc/develop/private.jpeg",
    "DEVELOP_PUBLIC_IMG": "/system/stamplc/develop/public.jpeg",
    "AVATAR_IMG": "/system/common/img/avatar.jpeg",
    # ezdata
    # launcher
    "APPLIST_ICO": "/system/stamplc/applist.jpeg",
    "DEVELOP_ICO": "/system/stamplc/develop.jpeg",
    "APPRUN_ICO": "/system/stamplc/apprun.jpeg",
    "EZDATA_ICO": "/system/stamplc/ezdata.jpeg",
    "SETTING_ICO": "/system/stamplc/setting.jpeg",
    "RIGHT_ICO": "/system/stamplc/right.jpeg",
    "LEFT_ICO": "/system/stamplc/left.jpeg",
    # setting
    "WLAN_ICO_IMG": "/system/stamplc/setting/wlan.jpeg",
    "ETHERNET_ICO_IMG": "/system/stamplc/setting/ethernet.jpeg",
    "GENERAL_ICO_IMG": "/system/stamplc/setting/general.jpeg",
    "CARET_RIGHT": "/system/stamplc/setting/caret_right.jpeg",
    "SUBMIT_SELECT_BUTTON_IMG": "/system/stamplc/setting/submit_select.jpeg",
    "SUBMIT_UNSELECT_BUTTON_IMG": "/system/stamplc/setting/submit_unselect.jpeg",
    # wlan
    "WIFI_DEFAULT_IMG": "/system/stamplc/setting/wlan/input_default.jpeg",
    "WIFI_SSID_IMG": "/system/stamplc/setting/wlan/input_ssid.jpeg",
    "WIFI_PSK_IMG": "/system/stamplc/setting/wlan/input_psk.jpeg",
    "WIFI_SERVER_IMG": "/system/stamplc/setting/wlan/input_server.jpeg",
    # ethernet
    "ETHERNET_DEFAULT_IMG": "/system/stamplc/setting/ethernet/input_default.jpeg",
    "ETHERNET_IP_IMG": "/system/stamplc/setting/ethernet/input_ip.jpeg",
    "ETHERNET_MASK_IMG": "/system/stamplc/setting/ethernet/input_mask.jpeg",
    "ETHERNET_SERVER_IMG": "/system/stamplc/setting/ethernet/input_server.jpeg",
    # general
    "DISABLE_IMG": "/system/stamplc/setting/general/disable.jpeg",
    "ENABLE_IMG": "/system/stamplc/setting/general/enable.jpeg",
    # statusbar
    "BATTERY_BLACK_CHARGE_IMG": "/system/stamplc/statusbar/battery/black_charge.jpeg",
    "BATTERY_BLACK_IMG": "/system/stamplc/statusbar/battery/black.jpeg",
    "BATTERY_GREEN_CHARGE_IMG": "/system/stamplc/statusbar/battery/green_charge.jpeg",
    "BATTERY_GREEN_IMG": "/system/stamplc/statusbar/battery/green.jpeg",
    "BATTERY_RED_CHARGE_IMG": "/system/stamplc/statusbar/battery/red_charge.jpeg",
    "BATTERY_RED_IMG": "/system/stamplc/statusbar/battery/red.jpeg",
    "SERVER_EMPTY_IMG": "/system/stamplc/statusbar/cloud/empty.jpeg",
    "SERVER_ERROR_IMG": "/system/stamplc/statusbar/cloud/error.jpeg",
    "SERVER_GREEN_IMG": "/system/stamplc/statusbar/cloud/green.jpeg",
    "WIFI_DISCONNECTED_IMG": "/system/stamplc/statusbar/wifi/disconnected.jpeg",
    "WIFI_EMPTY_IMG": "/system/stamplc/statusbar/wifi/empty.jpeg",
    "WIFI_GOOD_IMG": "/system/stamplc/statusbar/wifi/good.jpeg",
    "WIFI_MID_IMG": "/system/stamplc/statusbar/wifi/mid.jpeg",
    "WIFI_WORSE_IMG": "/system/stamplc/statusbar/wifi/worse.jpeg",
    "ETHERNET_ONLINE_IMG": "/system/stamplc/statusbar/ethernet/online.jpeg",
    "ETHERNET_OFFLINE_IMG": "/system/stamplc/statusbar/ethernet/offline.jpeg",
    "BLUE_TITLE_IMG": "/system/stamplc/statusbar/title_blue.jpeg",
    # common
    "CARD_228x32_SELECT_IMG": "/system/stamplc/common/card_228x32_select.jpeg",
    "CARD_228x32_UNSELECT_IMG": "/system/stamplc/common/card_228x32_unselect.jpeg",
    # font
    "MontserratMedium10_VLW": "/system/common/font/Montserrat-Medium-10.vlw",
    "MontserratMedium12_VLW": "/system/common/font/Montserrat-Medium-12.vlw",
    "MontserratMedium16_VLW": "/system/common/font/Montserrat-Medium-16.vlw",
    "MontserratMedium18_VLW": "/system/common/font/Montserrat-Medium-18.vlw",
    # path
    "USER_AVATAR_PATH": "/system/common/img/",
}


def __getattr__(attr):
    value = _attrs.get(attr, None)
    if value is None:
        raise AttributeError(attr)
    globals()[attr] = value
    return value

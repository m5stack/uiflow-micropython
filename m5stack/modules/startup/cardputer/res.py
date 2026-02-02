# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "LOGO_IMG": "/system/cardputer/boot/boot_logo_1.jpeg",
    # apprun
    "RUN_INFO_IMG": "/system/cardputer/apprun/run_info.jpeg",
    "RUN_ONCE_SELECT_IMG": "/system/cardputer/apprun/run_once_select.jpeg",
    "RUN_ONCE_UNSELECT_IMG": "/system/cardputer/apprun/run_once_unselect.jpeg",
    "RUN_ALWAYS_SELECT_IMG": "/system/cardputer/apprun/run_always_select.jpeg",
    "RUN_ALWAYS_UNSELECT_IMG": "/system/cardputer/apprun/run_always_unselect.jpeg",
    # develop
    "DEVELOP_PRIVATE_IMG": "/system/cardputer/develop/private.jpeg",
    "DEVELOP_PUBLIC_IMG": "/system/cardputer/develop/public.jpeg",
    "AVATAR_IMG": "/system/common/img/avatar.jpg",
    # ezdata
    # launcher
    "APPLIST_ICO": "/system/cardputer/applist.jpeg",
    "DEVELOP_ICO": "/system/cardputer/develop.jpeg",
    "APPRUN_ICO": "/system/cardputer/apprun.jpeg",
    "EZDATA_ICO": "/system/cardputer/ezdata.jpeg",
    "SETTING_ICO": "/system/cardputer/setting.jpeg",
    "RIGHT_ICO": "/system/cardputer/right.jpeg",
    "LEFT_ICO": "/system/cardputer/left.jpeg",
    # setting
    "WLAN_ICO_IMG": "/system/cardputer/setting/wlan.jpeg",
    "GENERAL_ICO_IMG": "/system/cardputer/setting/general.jpeg",
    "CARET_RIGHT": "/system/cardputer/setting/caret_right.jpeg",
    # wlan
    "WIFI_DEFAULT_IMG": "/system/cardputer/setting/wlan/input_default.jpeg",
    "WIFI_SSID_IMG": "/system/cardputer/setting/wlan/input_ssid.jpeg",
    "WIFI_PSK_IMG": "/system/cardputer/setting/wlan/input_psk.jpeg",
    "WIFI_SERVER_IMG": "/system/cardputer/setting/wlan/input_server.jpeg",
    "SUBMIT_SELECT_BUTTON_IMG": "/system/cardputer/setting/wlan/submit_select.jpeg",
    "SUBMIT_UNSELECT_BUTTON_IMG": "/system/cardputer/setting/wlan/submit_unselect.jpeg",
    # general
    "DISABLE_IMG": "/system/cardputer/setting/general/disable.jpeg",
    "ENABLE_IMG": "/system/cardputer/setting/general/enable.jpeg",
    # sidebar
    "Aa_IMG": "/system/cardputer/sidebar/Aa.jpeg",
    "Aa0_IMG": "/system/cardputer/sidebar/Aa0.jpeg",
    "ALT_IMG": "/system/cardputer/sidebar/alt.jpeg",
    "ALT0_IMG": "/system/cardputer/sidebar/alt0.jpeg",
    "CTRL_IMG": "/system/cardputer/sidebar/ctrl.jpeg",
    "CTRL0_IMG": "/system/cardputer/sidebar/ctrl0.jpeg",
    "FN_IMG": "/system/cardputer/sidebar/fn.jpeg",
    "FN0_IMG": "/system/cardputer/sidebar/fn0.jpeg",
    "OPT_IMG": "/system/cardputer/sidebar/opt.jpeg",
    "OPT0_IMG": "/system/cardputer/sidebar/opt0.jpeg",
    # statusbar
    "BATTERY_BLACK_CHARGE_IMG": "/system/cardputer/statusbar/battery/black_charge.jpeg",
    "BATTERY_BLACK_IMG": "/system/cardputer/statusbar/battery/black.jpeg",
    "BATTERY_GREEN_CHARGE_IMG": "/system/cardputer/statusbar/battery/green_charge.jpeg",
    "BATTERY_GREEN_IMG": "/system/cardputer/statusbar/battery/green.jpeg",
    "BATTERY_RED_CHARGE_IMG": "/system/cardputer/statusbar/battery/red_charge.jpeg",
    "BATTERY_RED_IMG": "/system/cardputer/statusbar/battery/red.jpeg",
    "SERVER_EMPTY_IMG": "/system/cardputer/statusbar/cloud/empty.jpeg",
    "SERVER_ERROR_IMG": "/system/cardputer/statusbar/cloud/error.jpeg",
    "SERVER_GREEN_IMG": "/system/cardputer/statusbar/cloud/green.jpeg",
    "WIFI_DISCONNECTED_IMG": "/system/cardputer/statusbar/wifi/disconnected.jpeg",
    "WIFI_EMPTY_IMG": "/system/cardputer/statusbar/wifi/empty.jpeg",
    "WIFI_GOOD_IMG": "/system/cardputer/statusbar/wifi/good.jpeg",
    "WIFI_MID_IMG": "/system/cardputer/statusbar/wifi/mid.jpeg",
    "WIFI_WORSE_IMG": "/system/cardputer/statusbar/wifi/worse.jpeg",
    "BLUE_TITLE_IMG": "/system/cardputer/statusbar/title_blue.jpeg",
    # common
    "CARD_228x32_SELECT_IMG": "/system/cardputer/common/card_228x32_select.jpeg",
    "CARD_228x32_UNSELECT_IMG": "/system/cardputer/common/card_228x32_unselect.jpeg",
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

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

_attrs = {
    "LOGO_IMG": "/system/cardputeradv/boot/boot_logo_1.jpeg",
    # apprun
    "RUN_INFO_IMG": "/system/cardputeradv/apprun/run_info.jpeg",
    "RUN_ONCE_SELECT_IMG": "/system/cardputeradv/apprun/run_once_select.jpeg",
    "RUN_ONCE_UNSELECT_IMG": "/system/cardputeradv/apprun/run_once_unselect.jpeg",
    "RUN_ALWAYS_SELECT_IMG": "/system/cardputeradv/apprun/run_always_select.jpeg",
    "RUN_ALWAYS_UNSELECT_IMG": "/system/cardputeradv/apprun/run_always_unselect.jpeg",
    # develop
    "DEVELOP_PRIVATE_IMG": "/system/cardputeradv/develop/private.jpeg",
    "DEVELOP_PUBLIC_IMG": "/system/cardputeradv/develop/public.jpeg",
    "AVATAR_IMG": "/system/common/img/avatar.jpeg",
    # ezdata
    # launcher
    "APPLIST_ICO": "/system/cardputeradv/applist.jpeg",
    "DEVELOP_ICO": "/system/cardputeradv/develop.jpeg",
    "APPRUN_ICO": "/system/cardputeradv/apprun.jpeg",
    "EZDATA_ICO": "/system/cardputeradv/ezdata.jpeg",
    "SETTING_ICO": "/system/cardputeradv/setting.jpeg",
    "RIGHT_ICO": "/system/cardputeradv/right.jpeg",
    "LEFT_ICO": "/system/cardputeradv/left.jpeg",
    # setting
    "WLAN_ICO_IMG": "/system/cardputeradv/setting/wlan.jpeg",
    "GENERAL_ICO_IMG": "/system/cardputeradv/setting/general.jpeg",
    "CARET_RIGHT": "/system/cardputeradv/setting/caret_right.jpeg",
    # wlan
    "WIFI_DEFAULT_IMG": "/system/cardputeradv/setting/wlan/input_default.jpeg",
    "WIFI_SSID_IMG": "/system/cardputeradv/setting/wlan/input_ssid.jpeg",
    "WIFI_PSK_IMG": "/system/cardputeradv/setting/wlan/input_psk.jpeg",
    "WIFI_SERVER_IMG": "/system/cardputeradv/setting/wlan/input_server.jpeg",
    "SUBMIT_SELECT_BUTTON_IMG": "/system/cardputeradv/setting/wlan/submit_select.jpeg",
    "SUBMIT_UNSELECT_BUTTON_IMG": "/system/cardputeradv/setting/wlan/submit_unselect.jpeg",
    # general
    "DISABLE_IMG": "/system/cardputeradv/setting/general/disable.jpeg",
    "ENABLE_IMG": "/system/cardputeradv/setting/general/enable.jpeg",
    # sidebar
    "Aa_IMG": "/system/cardputeradv/sidebar/Aa.jpeg",
    "Aa0_IMG": "/system/cardputeradv/sidebar/Aa0.jpeg",
    "ALT_IMG": "/system/cardputeradv/sidebar/alt.jpeg",
    "ALT0_IMG": "/system/cardputeradv/sidebar/alt0.jpeg",
    "CTRL_IMG": "/system/cardputeradv/sidebar/ctrl.jpeg",
    "CTRL0_IMG": "/system/cardputeradv/sidebar/ctrl0.jpeg",
    "FN_IMG": "/system/cardputeradv/sidebar/fn.jpeg",
    "FN0_IMG": "/system/cardputeradv/sidebar/fn0.jpeg",
    "OPT_IMG": "/system/cardputeradv/sidebar/opt.jpeg",
    "OPT0_IMG": "/system/cardputeradv/sidebar/opt0.jpeg",
    # statusbar
    "BATTERY_BLACK_CHARGE_IMG": "/system/cardputeradv/statusbar/battery/black_charge.jpeg",
    "BATTERY_BLACK_IMG": "/system/cardputeradv/statusbar/battery/black.jpeg",
    "BATTERY_GREEN_CHARGE_IMG": "/system/cardputeradv/statusbar/battery/green_charge.jpeg",
    "BATTERY_GREEN_IMG": "/system/cardputeradv/statusbar/battery/green.jpeg",
    "BATTERY_RED_CHARGE_IMG": "/system/cardputeradv/statusbar/battery/red_charge.jpeg",
    "BATTERY_RED_IMG": "/system/cardputeradv/statusbar/battery/red.jpeg",
    "SERVER_EMPTY_IMG": "/system/cardputeradv/statusbar/cloud/empty.jpeg",
    "SERVER_ERROR_IMG": "/system/cardputeradv/statusbar/cloud/error.jpeg",
    "SERVER_GREEN_IMG": "/system/cardputeradv/statusbar/cloud/green.jpeg",
    "WIFI_DISCONNECTED_IMG": "/system/cardputeradv/statusbar/wifi/disconnected.jpeg",
    "WIFI_EMPTY_IMG": "/system/cardputeradv/statusbar/wifi/empty.jpeg",
    "WIFI_GOOD_IMG": "/system/cardputeradv/statusbar/wifi/good.jpeg",
    "WIFI_MID_IMG": "/system/cardputeradv/statusbar/wifi/mid.jpeg",
    "WIFI_WORSE_IMG": "/system/cardputeradv/statusbar/wifi/worse.jpeg",
    "BLUE_TITLE_IMG": "/system/cardputeradv/statusbar/title_blue.jpeg",
    # common
    "CARD_228x32_SELECT_IMG": "/system/cardputeradv/common/card_228x32_select.jpeg",
    "CARD_228x32_UNSELECT_IMG": "/system/cardputeradv/common/card_228x32_unselect.jpeg",
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

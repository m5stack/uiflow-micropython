_attrs = {
    "LOGO_IMG": "/system/station/boot/boot_logo_1.jpeg",
    # apprun
    "RUN_INFO_IMG": "/system/station/apprun/run_info.jpeg",
    "RUN_ONCE_SELECT_IMG": "/system/station/apprun/run_once_select.jpeg",
    "RUN_ONCE_UNSELECT_IMG": "/system/station/apprun/run_once_unselect.jpeg",
    "RUN_ALWAYS_SELECT_IMG": "/system/station/apprun/run_always_select.jpeg",
    "RUN_ALWAYS_UNSELECT_IMG": "/system/station/apprun/run_always_unselect.jpeg",
    # develop
    "DEVELOP_PRIVATE_IMG": "/system/station/develop/private.jpeg",
    "DEVELOP_PUBLIC_IMG": "/system/station/develop/public.jpeg",
    "AVATAR_IMG": "/system/common/img/avatar.jpeg",
    # ezdata
    # launcher
    "APPLIST_ICO": "/system/station/applist.jpeg",
    "DEVELOP_ICO": "/system/station/develop.jpeg",
    "APPRUN_ICO": "/system/station/apprun.jpeg",
    "EZDATA_ICO": "/system/station/ezdata.jpeg",
    "SETTING_ICO": "/system/station/setting.jpeg",
    "RIGHT_ICO": "/system/station/right.jpeg",
    "LEFT_ICO": "/system/station/left.jpeg",
    # setting
    "WLAN_ICO_IMG": "/system/station/setting/wlan.jpeg",
    "GENERAL_ICO_IMG": "/system/station/setting/general.jpeg",
    "CARET_RIGHT": "/system/station/setting/caret_right.jpeg",
    # wlan
    "WIFI_DEFAULT_IMG": "/system/station/setting/wlan/input_default.jpeg",
    "WIFI_SSID_IMG": "/system/station/setting/wlan/input_ssid.jpeg",
    "WIFI_PSK_IMG": "/system/station/setting/wlan/input_psk.jpeg",
    "WIFI_SERVER_IMG": "/system/station/setting/wlan/input_server.jpeg",
    "SUBMIT_SELECT_BUTTON_IMG": "/system/station/setting/wlan/submit_select.jpeg",
    "SUBMIT_UNSELECT_BUTTON_IMG": "/system/station/setting/wlan/submit_unselect.jpeg",
    # general
    "DISABLE_IMG": "/system/station/setting/general/disable.jpeg",
    "ENABLE_IMG": "/system/station/setting/general/enable.jpeg",
    # statusbar
    "BATTERY_BLACK_CHARGE_IMG": "/system/station/statusbar/battery/black_charge.jpeg",
    "BATTERY_BLACK_IMG": "/system/station/statusbar/battery/black.jpeg",
    "BATTERY_GREEN_CHARGE_IMG": "/system/station/statusbar/battery/green_charge.jpeg",
    "BATTERY_GREEN_IMG": "/system/station/statusbar/battery/green.jpeg",
    "BATTERY_RED_CHARGE_IMG": "/system/station/statusbar/battery/red_charge.jpeg",
    "BATTERY_RED_IMG": "/system/station/statusbar/battery/red.jpeg",
    "SERVER_EMPTY_IMG": "/system/station/statusbar/cloud/empty.jpeg",
    "SERVER_ERROR_IMG": "/system/station/statusbar/cloud/error.jpeg",
    "SERVER_GREEN_IMG": "/system/station/statusbar/cloud/green.jpeg",
    "WIFI_DISCONNECTED_IMG": "/system/station/statusbar/wifi/disconnected.jpeg",
    "WIFI_EMPTY_IMG": "/system/station/statusbar/wifi/empty.jpeg",
    "WIFI_GOOD_IMG": "/system/station/statusbar/wifi/good.jpeg",
    "WIFI_MID_IMG": "/system/station/statusbar/wifi/mid.jpeg",
    "WIFI_WORSE_IMG": "/system/station/statusbar/wifi/worse.jpeg",
    "BLUE_TITLE_IMG": "/system/station/statusbar/title_blue.jpeg",
    # common
    "CARD_228x32_SELECT_IMG": "/system/station/common/card_228x32_select.jpeg",
    "CARD_228x32_UNSELECT_IMG": "/system/station/common/card_228x32_unselect.jpeg",
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

_attrs = {
    "LOGO_IMG": "/system/dinmeter/boot/boot_logo_1.jpeg",
    # apprun
    "RUN_INFO_IMG": "/system/dinmeter/apprun/run_info.jpeg",
    "RUN_ONCE_SELECT_IMG": "/system/dinmeter/apprun/run_once_select.jpeg",
    "RUN_ONCE_UNSELECT_IMG": "/system/dinmeter/apprun/run_once_unselect.jpeg",
    "RUN_ALWAYS_SELECT_IMG": "/system/dinmeter/apprun/run_always_select.jpeg",
    "RUN_ALWAYS_UNSELECT_IMG": "/system/dinmeter/apprun/run_always_unselect.jpeg",
    # develop
    "DEVELOP_PRIVATE_IMG": "/system/dinmeter/develop/private.jpeg",
    "DEVELOP_PUBLIC_IMG": "/system/dinmeter/develop/public.jpeg",
    "AVATAR_IMG": "/system/common/img/avatar.jpeg",
    # ezdata
    # launcher
    "APPLIST_ICO": "/system/dinmeter/applist.jpeg",
    "DEVELOP_ICO": "/system/dinmeter/develop.jpeg",
    "APPRUN_ICO": "/system/dinmeter/apprun.jpeg",
    "EZDATA_ICO": "/system/dinmeter/ezdata.jpeg",
    "SETTING_ICO": "/system/dinmeter/setting.jpeg",
    "RIGHT_ICO": "/system/dinmeter/right.jpeg",
    "LEFT_ICO": "/system/dinmeter/left.jpeg",
    # setting
    "WLAN_ICO_IMG": "/system/dinmeter/setting/wlan.jpeg",
    "GENERAL_ICO_IMG": "/system/dinmeter/setting/general.jpeg",
    "CARET_RIGHT": "/system/dinmeter/setting/caret_right.jpeg",
    # wlan
    "WIFI_DEFAULT_IMG": "/system/dinmeter/setting/wlan/input_default.jpeg",
    "WIFI_SSID_IMG": "/system/dinmeter/setting/wlan/input_ssid.jpeg",
    "WIFI_PSK_IMG": "/system/dinmeter/setting/wlan/input_psk.jpeg",
    "WIFI_SERVER_IMG": "/system/dinmeter/setting/wlan/input_server.jpeg",
    "SUBMIT_SELECT_BUTTON_IMG": "/system/dinmeter/setting/wlan/submit_select.jpeg",
    "SUBMIT_UNSELECT_BUTTON_IMG": "/system/dinmeter/setting/wlan/submit_unselect.jpeg",
    # general
    "DISABLE_IMG": "/system/dinmeter/setting/general/disable.jpeg",
    "ENABLE_IMG": "/system/dinmeter/setting/general/enable.jpeg",
    # statusbar
    "BATTERY_BLACK_CHARGE_IMG": "/system/dinmeter/statusbar/battery/black_charge.jpeg",
    "BATTERY_BLACK_IMG": "/system/dinmeter/statusbar/battery/black.jpeg",
    "BATTERY_GREEN_CHARGE_IMG": "/system/dinmeter/statusbar/battery/green_charge.jpeg",
    "BATTERY_GREEN_IMG": "/system/dinmeter/statusbar/battery/green.jpeg",
    "BATTERY_RED_CHARGE_IMG": "/system/dinmeter/statusbar/battery/red_charge.jpeg",
    "BATTERY_RED_IMG": "/system/dinmeter/statusbar/battery/red.jpeg",
    "SERVER_EMPTY_IMG": "/system/dinmeter/statusbar/cloud/empty.jpeg",
    "SERVER_ERROR_IMG": "/system/dinmeter/statusbar/cloud/error.jpeg",
    "SERVER_GREEN_IMG": "/system/dinmeter/statusbar/cloud/green.jpeg",
    "WIFI_DISCONNECTED_IMG": "/system/dinmeter/statusbar/wifi/disconnected.jpeg",
    "WIFI_EMPTY_IMG": "/system/dinmeter/statusbar/wifi/empty.jpeg",
    "WIFI_GOOD_IMG": "/system/dinmeter/statusbar/wifi/good.jpeg",
    "WIFI_MID_IMG": "/system/dinmeter/statusbar/wifi/mid.jpeg",
    "WIFI_WORSE_IMG": "/system/dinmeter/statusbar/wifi/worse.jpeg",
    "BLUE_TITLE_IMG": "/system/dinmeter/statusbar/title_blue.jpeg",
    # common
    "CARD_228x32_SELECT_IMG": "/system/dinmeter/common/card_228x32_select.jpeg",
    "CARD_228x32_UNSELECT_IMG": "/system/dinmeter/common/card_228x32_unselect.jpeg",
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

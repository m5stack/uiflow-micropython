# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "tab5/launcher/common/ezdata.py",
        "tab5/launcher/common/common.py",
        "tab5/launcher/common/__init__.py",
        "tab5/launcher/common/indicator.py",
        "tab5/launcher/apps/app.py",
        "tab5/launcher/apps/app_i2c_scan.py",
        "tab5/launcher/apps/app_app_list.py",
        "tab5/launcher/apps/app_wifi_scan.py",
        "tab5/launcher/apps/app_dummy.py",
        "tab5/launcher/apps/app_uiflow.py",
        "tab5/launcher/apps/__init__.py",
        "tab5/launcher/apps/app_ezdata.py",
        "tab5/launcher/apps/app_wifi.py",
        "tab5/launcher/apps/app_uart.py",
        "tab5/launcher/apps/app_gpio.py",
        "tab5/launcher/apps/app_adc.py",
        "tab5/launcher/hal.py",
        "tab5/launcher/components/ezdata_dock.py",
        "tab5/launcher/components/status_bar.py",
        "tab5/launcher/components/__init__.py",
        "tab5/launcher/components/app_dock.py",
        "tab5/launcher/launcher.py",
        "tab5/launcher/__init__.py",
        "tab5/hal_tab5.py",
        "tab5/__init__.py",
    ),
    base_path="..",
    opt=3,
)

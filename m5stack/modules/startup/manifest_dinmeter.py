# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "dinmeter/__init__.py",
        "dinmeter/app_base.py",
        "dinmeter/framework.py",
        "dinmeter/res.py",
        "dinmeter/apps/dev.py",
        "dinmeter/apps/ezdata.py",
        "dinmeter/apps/launcher.py",
        "dinmeter/apps/settings.py",
        "dinmeter/apps/statusbar.py",
    ),
    base_path="..",
    opt=3,
)

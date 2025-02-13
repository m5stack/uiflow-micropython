# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "stampplc/__init__.py",
        "stampplc/app_base.py",
        "stampplc/framework.py",
        "stampplc/res.py",
        "stampplc/apps/app_list.py",
        "stampplc/apps/app_run.py",
        "stampplc/apps/dev.py",
        "stampplc/apps/ezdata.py",
        "stampplc/apps/launcher.py",
        "stampplc/apps/settings.py",
        "stampplc/apps/statusbar.py",
    ),
    base_path="..",
    opt=3,
)

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "stamplc/__init__.py",
        "stamplc/app_base.py",
        "stamplc/framework.py",
        "stamplc/res.py",
        "stamplc/apps/app_list.py",
        "stamplc/apps/app_run.py",
        "stamplc/apps/dev.py",
        "stamplc/apps/ezdata.py",
        "stamplc/apps/launcher.py",
        "stamplc/apps/settings.py",
        "stamplc/apps/statusbar.py",
    ),
    base_path="..",
    opt=3,
)

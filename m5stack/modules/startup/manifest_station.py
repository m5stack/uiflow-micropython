# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "station/__init__.py",
        "station/app.py",
        "station/framework.py",
        "station/res.py",
        "station/apps/app_list.py",
        "station/apps/app_run.py",
        "station/apps/dev.py",
        "station/apps/ezdata.py",
        "station/apps/launcher.py",
        "station/apps/settings.py",
        "station/apps/statusbar.py",
    ),
    base_path="..",
    opt=0,
)

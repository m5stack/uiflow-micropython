# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "fire/__init__.py",
        "fire/app.py",
        "fire/framework.py",
        "fire/res.py",
        "fire/apps/app_list.py",
        "fire/apps/app_run.py",
        "fire/apps/dev.py",
        "fire/apps/ezdata.py",
        "fire/apps/settings.py",
    ),
    base_path="..",
    opt=3,
)

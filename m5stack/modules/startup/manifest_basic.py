# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "basic/__init__.py",
        "basic/app.py",
        "basic/framework.py",
        "basic/res.py",
        "basic/apps/app_list.py",
        "basic/apps/app_run.py",
        "basic/apps/dev.py",
        "basic/apps/ezdata.py",
        "basic/apps/settings.py",
    ),
    base_path="..",
    opt=3,
)

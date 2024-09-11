# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "dial/__init__.py",
        "dial/app_base.py",
        "dial/framework.py",
        "dial/res.py",
        "dial/apps/app_list.py",
        "dial/apps/app_run.py",
        "dial/apps/dev.py",
        "dial/apps/ezdata.py",
        "dial/apps/settings.py",
        "dial/apps/status_bar.py",
    ),
    base_path="..",
    opt=3,
)

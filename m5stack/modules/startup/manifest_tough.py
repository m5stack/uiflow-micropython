# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "tough/__init__.py",
        "tough/app_base.py",
        "tough/framework.py",
        "tough/apps/app_list.py",
        "tough/apps/app_run.py",
        "tough/apps/dev.py",
        "tough/apps/ezdata.py",
        "tough/apps/settings.py",
        "tough/apps/status_bar.py",
    ),
    base_path="..",
    opt=3,
)

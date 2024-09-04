# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "cores3/__init__.py",
        "cores3/app.py",
        "cores3/framework.py",
        "cores3/apps/__init__.py",
        "cores3/apps/app_list.py",
        "cores3/apps/app_run.py",
        "cores3/apps/dev.py",
        "cores3/apps/ezdata.py",
        "cores3/apps/settings.py",
        "cores3/apps/status_bar.py",
    ),
    base_path="..",
    opt=3,
)

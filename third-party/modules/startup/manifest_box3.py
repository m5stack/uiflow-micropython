# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(  # noqa: F821
    "startup",
    (
        "__init__.py",
        "box3/__init__.py",
        "box3/app.py",
        "box3/framework.py",
        "box3/apps/app_list.py",
        "box3/apps/app_run.py",
        "box3/apps/dev.py",
        "box3/apps/ezdata.py",
        "box3/apps/settings.py",
        "box3/apps/status_bar.py",
    ),
    base_path="..",
    opt=3,
)

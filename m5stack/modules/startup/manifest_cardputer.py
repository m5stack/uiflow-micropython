# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "cardputer/__init__.py",
        "cardputer/app.py",
        "cardputer/framework.py",
        "cardputer/res.py",
        "cardputer/apps/app_list.py",
        "cardputer/apps/app_run.py",
        "cardputer/apps/dev.py",
        "cardputer/apps/ezdata.py",
        "cardputer/apps/launcher.py",
        "cardputer/apps/settings.py",
        "cardputer/apps/statusbar.py",
    ),
    base_path="..",
    # opt=0,
)

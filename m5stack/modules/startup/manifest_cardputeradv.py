# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

package(
    "startup",
    (
        "__init__.py",
        "cardputeradv/__init__.py",
        "cardputeradv/app_base.py",
        "cardputeradv/framework.py",
        "cardputeradv/res.py",
        "cardputeradv/apps/app_list.py",
        "cardputeradv/apps/app_run.py",
        "cardputeradv/apps/dev.py",
        "cardputeradv/apps/ezdata.py",
        "cardputeradv/apps/launcher.py",
        "cardputeradv/apps/settings.py",
        "cardputeradv/apps/statusbar.py",
    ),
    base_path="..",
    opt=3,
)

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

include("$(MPY_DIR)/../third-party/modules/startup/manifest_xiaos3.py")  # noqa: F821
freeze("$(MPY_DIR)/../third-party/modules", "M5.py")  # noqa: F821

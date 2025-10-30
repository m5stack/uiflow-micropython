# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

include("$(MPY_DIR)/../m5stack/modules/startup/manifest_cores3.py")
include("$(MPY_DIR)/../m5stack/libs/m5ui/manifest.py")
include("$(MPY_DIR)/../m5stack/libs/module/manifest.py")
include("$(MPY_DIR)/../m5stack/libs/unit/manifest.py")
include("$(MPY_DIR)/../m5stack/libs/usb/manifest.py")
freeze("$(MPY_DIR)/../m5stack/libs/", "m5camera.py")

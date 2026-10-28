# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

require("requests")
include("$(MPY_DIR)/extmod/asyncio")
include("$(MPY_DIR)/../m5stack/modules/manifest.py")
include("$(MPY_DIR)/../m5stack/libs/manifest_basic.py")
include("$(MPY_DIR)/../m5stack/modules/startup/manifest_corep4x.py")
include("$(MPY_DIR)/../m5stack/libs/m5ui/manifest.py")
include("$(MPY_DIR)/../m5stack/libs/module/manifest.py")
include("$(MPY_DIR)/../m5stack/libs/unit/manifest.py")
include("$(MPY_DIR)/../m5stack/libs/usb/manifest.py")
freeze("$(MPY_DIR)/../m5stack/libs/", "m5camera.py")
include("$(MPY_DIR)/../m5stack/libs/chain/manifest.py")

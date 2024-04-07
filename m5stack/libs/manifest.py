# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

include("bleuart/manifest.py")
include("driver/manifest.py")
include("ezdata/manifest.py")
include("hardware/manifest.py")
include("hat/manifest.py")
include("image_plus/manifest.py")
include("module/manifest.py")
include("umqtt/manifest.py")
include("unit/manifest.py")
include("base/manifest.py")
# freeze("$(MPY_DIR)/../m5stack/libs/unit")
include("utility/manifest.py")
module("boot_option.py")
module("label_plus.py")
module("m5camera.py")

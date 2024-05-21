# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

include("manifest_m5stack.py")  # noqa: F821
require("mip")  # noqa: F821
require("ntptime")  # noqa: F821
require("dht")  # noqa: F821
require("onewire")  # noqa: F821
include("$(MPY_DIR)/extmod/asyncio")  # noqa: F821
require("webrepl")  # noqa: F821
require("upysh")  # noqa: F821

# freeze("$(MPY_DIR)/tools", ("upip.py", "upip_utarfile.py"))
# freeze("$(MPY_DIR)/ports/esp8266/modules", "ntptime.py")
# freeze("$(MPY_DIR)/drivers/dht", "dht.py")
# freeze("$(MPY_DIR)/drivers/onewire")
# include("$(MPY_DIR)/extmod/uasyncio/manifest.py")
# include("$(MPY_DIR)/extmod/webrepl/manifest.py")

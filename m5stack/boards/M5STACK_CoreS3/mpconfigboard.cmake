# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(IDF_TARGET esp32s3)

# https://github.com/m5stack/m5stack-board-id/blob/main/board.csv#L12
set(BOARD_ID 10)

# Enable camera module
set(M5_CAMERA_MODULE_ENABLE TRUE)

set(SDKCONFIG_DEFAULTS
    ./boards/M5STACK_CoreS3/sdkconfig.board
    ./boards/sdkconfig.base
    ./boards/sdkconfig.240mhz
    ./boards/sdkconfig.disable_iram
    ./boards/sdkconfig.ble
    ./boards/sdkconfig.usb
    ./boards/sdkconfig.flash_16mb
    ./boards/sdkconfig.spiram_sx
)

# If not enable LVGL, ignore this...
set(LV_CFLAGS -DLV_COLOR_DEPTH=16 -DLV_COLOR_16_SWAP=0)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_SOURCE_DIR}/boards/manifest.py)
endif()

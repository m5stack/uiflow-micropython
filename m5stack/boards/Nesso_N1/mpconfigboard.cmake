# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(IDF_TARGET esp32c6)

# nanoc6 https://github.com/m5stack/m5stack-board-id/blob/main/board.csv#L25
set(BOARD_ID 23)
set(MICROPY_PY_LVGL 0)

set(SDKCONFIG_DEFAULTS
    ./boards/sdkconfig.base
    ${SDKCONFIG_IDF_VERSION_SPECIFIC}
    ./boards/sdkconfig.flash_16mb
    ./boards/sdkconfig.c6
    ./boards/sdkconfig.ble
    ./boards/sdkconfig.usb
    ./boards/sdkconfig.freertos
    ./boards/Nesso_N1/sdkconfig.board
)

# If not enable LVGL, ignore this...
set(LV_CFLAGS -DLV_COLOR_DEPTH=16 -DLV_COLOR_16_SWAP=0)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_SOURCE_DIR}/boards/manifest.py)
endif()

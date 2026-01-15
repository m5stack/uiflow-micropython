# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(IDF_TARGET esp32s3)

# sticks3 https://github.com/m5stack/m5stack-board-id/blob/main/board.csv#L28
set(BOARD_ID 26)
set(MICROPY_PY_LVGL 0)

set(SDKCONFIG_DEFAULTS
    ./boards/sdkconfig.base
    ${SDKCONFIG_IDF_VERSION_SPECIFIC}
    ./boards/sdkconfig.240mhz
    ./boards/sdkconfig.disable_iram
    ./boards/sdkconfig.ble
    ./boards/sdkconfig.usb
    ./boards/sdkconfig.usb_cdc
    ./boards/sdkconfig.flash_8mb
    ./boards/sdkconfig.spiram
    ./boards/sdkconfig.spiram_oct
    ./boards/sdkconfig.freertos
    ./boards/M5STACK_StickS3/sdkconfig.board
)

#  If not enable LVGL, ignore this...
set(LV_CFLAGS -DLV_COLOR_DEPTH=16 -DLV_COLOR_16_SWAP=0)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_SOURCE_DIR}/boards/manifest.py)
endif()

set(ADF_MODULE_ENABLE TRUE)

set(ADF_COMPS     "$ENV{ADF_PATH}/components")

set(ADF_BOARD_INIT_SRC
    $ENV{ADF_PATH}/components
    M5STACK_StickS3/board_init.c
)

list(APPEND EXTRA_COMPONENT_DIRS
    $ENV{ADF_PATH}/components/audio_pipeline
    $ENV{ADF_PATH}/components/audio_sal
    $ENV{ADF_PATH}/components/esp-adf-libs
    $ENV{ADF_PATH}/components/esp-sr
    ${CMAKE_SOURCE_DIR}/boards
)

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(IDF_TARGET esp32s3)

# dial https://github.com/m5stack/m5stack-board-id/blob/main/board.csv#L14
set(BOARD_ID 12)

set(SDKCONFIG_DEFAULTS
    ./boards/sdkconfig.base
    ${SDKCONFIG_IDF_VERSION_SPECIFIC}
    ./boards/sdkconfig.240mhz
    ./boards/sdkconfig.disable_iram
    ./boards/sdkconfig.ble
    ./boards/sdkconfig.usb
    ./boards/sdkconfig.usb_cdc
    ./boards/sdkconfig.flash_8mb
    ./boards/sdkconfig.freertos
    ./boards/M5STACK_Dial/sdkconfig.board
)

# If not enable LVGL, ignore this...
set(LV_CFLAGS -DLV_COLOR_DEPTH=16 -DLV_COLOR_16_SWAP=0)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_SOURCE_DIR}/boards/manifest.py)
endif()

# NOTE: 这里的配置是无效的，仅为了兼容ADF，保证编译通过
set(ADF_COMPS     "$ENV{ADF_PATH}/components")
set(ADF_BOARD_DIR "$ENV{ADF_PATH}/components/audio_board/esp32_s3_box_3")

list(APPEND EXTRA_COMPONENT_DIRS
    $ENV{ADF_PATH}/components/audio_pipeline
    $ENV{ADF_PATH}/components/audio_sal
    $ENV{ADF_PATH}/components/esp-adf-libs
    $ENV{ADF_PATH}/components/esp-sr
    ${CMAKE_SOURCE_DIR}/boards
)
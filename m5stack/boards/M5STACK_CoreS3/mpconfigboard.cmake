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

set(ADF_MODULE_ENABLE TRUE)

set(ADF_COMPS     "$ENV{ADF_PATH}/components")
set(ADF_BOARD_DIR "$ENV{ADF_PATH}/components/audio_board/cores3")

set(ADF_BOARD_CODEC_SRC
    ${ADF_COMPS}/audio_hal/driver/es8311/es8311.c
    ${ADF_COMPS}/audio_hal/driver/es7210/es7210.c
)

set(ADF_BOARD_CODEC_INC
    ${ADF_COMPS}/audio_hal/driver/es8311
    ${ADF_COMPS}/audio_hal/driver/es7210
)

set(ADF_BOARD_INIT_SRC
    $ENV{ADF_PATH}/components
    M5STACK_CoreS3/board_init.c
)

list(APPEND EXTRA_COMPONENT_DIRS
    $ENV{ADF_PATH}/components/audio_pipeline
    $ENV{ADF_PATH}/components/audio_sal
    $ENV{ADF_PATH}/components/esp-adf-libs
    $ENV{ADF_PATH}/components/esp-sr
    ${CMAKE_SOURCE_DIR}/boards
)

message(STATUS "cores3 CMakeLists.txt: EXTRA_COMPONENT_DIRS=${EXTRA_COMPONENT_DIRS}")
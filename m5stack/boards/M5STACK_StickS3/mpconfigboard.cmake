# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(IDF_TARGET esp32s3)
set(WEB_REPL_ENABLE 1)

# sticks3 https://github.com/m5stack/m5stack-board-id/blob/main/board.csv#L28
set(BOARD_ID 26)
set(MICROPY_PY_LVGL 0)

# Font Support
set(FONT_MONTSERRAT_12 1)
set(FONT_MONTSERRAT_14 1)
set(FONT_MONTSERRAT_16 1)
set(FONT_MONTSERRAT_18 1)
set(FONT_MONTSERRAT_20 0)
set(FONT_MONTSERRAT_22 0)
set(FONT_MONTSERRAT_24 1)
set(FONT_MONTSERRAT_30 0)
set(FONT_MONTSERRAT_36 0)
set(FONT_MONTSERRAT_40 1)
set(FONT_MONTSERRAT_44 1)
set(FONT_MONTSERRAT_48 1)
set(FONT_ALIBABAPUHUITI_CN24 1)
set(FONT_ALIBABASANS_JA24 1)
set(FONT_ALIBABASANS_KR24 1)

set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.base
    boards/sdkconfig.ble
    boards/sdkconfig.240mhz
    boards/sdkconfig.flash_8mb
    boards/sdkconfig.flash_qio
    boards/sdkconfig.freertos
    boards/sdkconfig.spiram
    boards/sdkconfig.spiram_oct
    boards/M5STACK_StickS3/sdkconfig.board
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

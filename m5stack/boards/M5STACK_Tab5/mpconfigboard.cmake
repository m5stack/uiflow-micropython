# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(IDF_TARGET esp32p4)

# https://github.com/m5stack/m5stack-board-id/blob/main/board.csv#L12
set(BOARD_ID 22)
set(MICROPY_PY_LVGL 1)

# Font Support
set(FONT_MONTSERRAT_12 1)
set(FONT_MONTSERRAT_14 1)
set(FONT_MONTSERRAT_16 1)
set(FONT_MONTSERRAT_18 1)
set(FONT_MONTSERRAT_20 1)
set(FONT_MONTSERRAT_22 1)
set(FONT_MONTSERRAT_24 1)
set(FONT_MONTSERRAT_30 1)
set(FONT_MONTSERRAT_36 1)
set(FONT_MONTSERRAT_40 1)
set(FONT_MONTSERRAT_44 1)
set(FONT_MONTSERRAT_48 1)
set(FONT_ALIBABAPUHUITI_CN24 1)
set(FONT_ALIBABASANS_JA24 1)
set(FONT_ALIBABASANS_KR24 1)

# Enable camera module
# set(M5_CAMERA_MODULE_ENABLE TRUE)

set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.base
    boards/sdkconfig.p4
    boards/sdkconfig.p4_wifi_common
    boards/sdkconfig.p4_wifi_c6
    boards/sdkconfig.flash_16mb_omv
    boards/sdkconfig.flash_qio
    boards/sdkconfig.freertos
    boards/sdkconfig.spiram_hex
    boards/M5STACK_Tab5/sdkconfig.freertos
    boards/M5STACK_Tab5/sdkconfig.adf
    boards/M5STACK_Tab5/sdkconfig.esp_hosted
)

list(APPEND MICROPY_DEF_BOARD
    MICROPY_PY_NETWORK_WLAN=1
    MICROPY_PY_BLUETOOTH=1
)

# If not enable LVGL, ignore this...
set(LV_CFLAGS
    -DLV_COLOR_DEPTH=16
    -DLV_COLOR_16_SWAP=0
    -DLV_FONT_MONTSERRAT_12=${FONT_MONTSERRAT_12}
    -DLV_FONT_MONTSERRAT_14=${FONT_MONTSERRAT_14}
    -DLV_FONT_MONTSERRAT_16=${FONT_MONTSERRAT_16}
    -DLV_FONT_MONTSERRAT_18=${FONT_MONTSERRAT_18}
    -DLV_FONT_MONTSERRAT_20=${FONT_MONTSERRAT_20}
    -DLV_FONT_MONTSERRAT_22=${FONT_MONTSERRAT_22}
    -DLV_FONT_MONTSERRAT_24=${FONT_MONTSERRAT_24}
    -DLV_FONT_MONTSERRAT_30=${FONT_MONTSERRAT_30}
    -DLV_FONT_MONTSERRAT_36=${FONT_MONTSERRAT_36}
    -DLV_FONT_MONTSERRAT_40=${FONT_MONTSERRAT_40}
    -DLV_FONT_MONTSERRAT_44=${FONT_MONTSERRAT_44}
    -DLV_FONT_MONTSERRAT_48=${FONT_MONTSERRAT_48}
    -DUSR_FONT_ALIBABAPUHUITI_CN24=${FONT_ALIBABAPUHUITI_CN24}
    -DUSR_FONT_ALIBABASANS_JA24=${FONT_ALIBABASANS_JA24}
    -DUSR_FONT_ALIBABASANS_KR24=${FONT_ALIBABASANS_KR24}
)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_SOURCE_DIR}/boards/manifest.py)
endif()

set(ADF_MODULE_ENABLE TRUE)

set(ADF_COMPS     "$ENV{ADF_PATH}/components")

set(ADF_BOARD_INIT_SRC
    $ENV{ADF_PATH}/components
    M5STACK_Tab5/board_init.c
)

list(APPEND EXTRA_COMPONENT_DIRS
    ${CMAKE_SOURCE_DIR}/boards
    $ENV{ADF_PATH}/components/audio_pipeline
    $ENV{ADF_PATH}/components/audio_sal
    $ENV{ADF_PATH}/components/esp-adf-libs
    $ENV{ADF_PATH}/components/esp-sr
)

message(STATUS "M5STACK_Tab5/CMakeLists.txt: EXTRA_COMPONENT_DIRS=${EXTRA_COMPONENT_DIRS}")

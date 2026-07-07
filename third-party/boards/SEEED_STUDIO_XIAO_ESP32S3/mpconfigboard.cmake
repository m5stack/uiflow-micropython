# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(IDF_TARGET esp32s3)

# https://github.com/m5stack/m5stack-board-id/blob/main/board.csv#L12
set(BOARD_ID 136)
set(M5THINGS_BOARD_NAME "xiao-s3")

# Enable camera module
set(M5_CAMERA_MODULE_ENABLE TRUE)

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
    boards/SEEED_STUDIO_XIAO_ESP32S3/sdkconfig.board
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

# NOTE: 这里的配置是无效的，仅为了兼容ADF，保证编译通过
set(ADF_COMPS     "$ENV{ADF_PATH}/components")
set(ADF_BOARD_DIR "$ENV{ADF_PATH}/components/audio_board/esp32_s3_box_3")

list(APPEND EXTRA_COMPONENT_DIRS
    $ENV{ADF_PATH}/components/audio_pipeline
    $ENV{ADF_PATH}/components/audio_sal
    $ENV{ADF_PATH}/components/esp-adf-libs
    $ENV{ADF_PATH}/components/esp-sr
    ${CMAKE_SOURCE_DIR}/boards
    # esp_codec_dev
)

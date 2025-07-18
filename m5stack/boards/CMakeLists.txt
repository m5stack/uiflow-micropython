# SPDX-FileCopyrightText: 2019 <ESPRESSIF SYSTEMS (SHANGHAI) CO., LTD>
#
# SPDX-License-Identifier: MIT

if(IDF_TARGET STREQUAL "esp32" OR IDF_TARGET STREQUAL "esp32s3" OR IDF_TARGET STREQUAL "esp32p4")
set(
    srcs
        ${ADF_BOARD_INIT_SRC}
        # ${ADF_BOARD_CODEC_SRC}
        # ${ADF_BOARD_DIR}/board_pins_config.c
        ${ADF_COMPS}/audio_hal/audio_hal.c
        ${ADF_COMPS}/audio_hal/audio_volume.c
        ${ADF_COMPS}/audio_stream/http_stream.c
        ${ADF_COMPS}/audio_stream/i2s_stream_idf5.c
        # ${ADF_COMPS}/audio_stream/i2s_stream.c
        ${ADF_COMPS}/audio_stream/raw_stream.c
        ${ADF_COMPS}/audio_stream/http_playlist.c
        ${ADF_COMPS}/audio_stream/lib/gzip/gzip_miniz.c
        ${ADF_COMPS}/audio_stream/lib/hls/hls_parse.c
        ${ADF_COMPS}/audio_stream/lib/hls/hls_playlist.c
        ${ADF_COMPS}/audio_stream/lib/hls/join_path.c
        ${ADF_COMPS}/audio_stream/lib/hls/line_reader.c
        ${ADF_COMPS}/esp_peripherals/driver/i2c_bus/i2c_bus.c
)

set(
    includes
        ${ADF_BOARD_DIR}/
        # ${ADF_BOARD_CODEC_INC}
        include
        ${ADF_COMPS}/audio_board/include
        ${ADF_COMPS}/audio_hal/include
        ${ADF_COMPS}/audio_hal/driver/include
        ${ADF_COMPS}/audio_stream/include
        ${ADF_COMPS}/audio_stream/lib/gzip/include
        ${ADF_COMPS}/audio_stream/lib/hls/include
        ${ADF_COMPS}/esp_peripherals/include
        ${ADF_COMPS}/esp_peripherals/driver/i2c_bus
        ${ADF_COMPS}/display_service/include
        ${ADF_COMPS}/esp_dispatcher/include
)


idf_component_register(
    SRCS
        "${srcs}"
    INCLUDE_DIRS
        "${includes}"
    REQUIRES
        audio_pipeline
        audio_sal
        driver
        esp-adf-libs
        esp_http_client
        esp_lcd
        esp_codec_dev
)

message(STATUS "boards/CMakeLists.txt: EXTRA_COMPONENT_DIRS=${EXTRA_COMPONENT_DIRS}")
endif()
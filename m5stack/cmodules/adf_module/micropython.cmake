# SPDX-FileCopyrightText: 2019 <ESPRESSIF SYSTEMS (SHANGHAI) CO., LTD>
#
# SPDX-License-Identifier: MIT

add_library(adf_module INTERFACE)

set(ADF_COMPS  "$ENV{ADF_PATH}/components")

target_sources(adf_module INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/audio_player.c
    ${CMAKE_CURRENT_LIST_DIR}/audio_recorder.c
    ${CMAKE_CURRENT_LIST_DIR}/vfs_stream.c
    ${CMAKE_CURRENT_LIST_DIR}/modaudio.c
)

target_include_directories(adf_module INTERFACE
    ${ADF_COMPS}/audio_stream/include
    ${ADF_COMPS}/audio_stream/lib/gzip/include
    ${ADF_COMPS}/audio_stream/lib/hls/include
    ${CMAKE_CURRENT_LIST_DIR}
)

target_compile_options(adf_module INTERFACE "-g")
target_link_libraries(usermod INTERFACE adf_module)
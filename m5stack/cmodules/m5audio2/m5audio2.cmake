# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Create an INTERFACE library for our C module.
add_library(usermod_m5audio INTERFACE)

# Add our source files to the lib
target_sources(usermod_m5audio INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modaudio2.c
    ${CMAKE_CURRENT_LIST_DIR}/audio2_player.c
    ${CMAKE_CURRENT_LIST_DIR}/audio2_recorder.c
    ${CMAKE_CURRENT_LIST_DIR}/i2s_helper.c
    ${CMAKE_CURRENT_LIST_DIR}/vfs_stream.c
)

# Add the current directory as an include directory.
target_include_directories(usermod_m5audio INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_compile_options(usermod_m5audio INTERFACE "-g")

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE usermod_m5audio)

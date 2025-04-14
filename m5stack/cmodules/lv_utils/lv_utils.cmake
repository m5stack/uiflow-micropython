# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

add_library(usermod_lv_utils INTERFACE)

target_sources(usermod_lv_utils INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modlv_utils.c
)

target_include_directories(usermod_lv_utils INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_lv_utils)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/modlv_utils.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers -Wno-implicit-int"
)

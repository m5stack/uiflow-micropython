# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

add_library(usermod_M5UTILS INTERFACE)

target_sources(usermod_M5UTILS INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/m5utils.c
    ${CMAKE_CURRENT_LIST_DIR}/timer.c
)

target_include_directories(usermod_M5UTILS INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_M5UTILS)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/m5utils.c
    ${CMAKE_CURRENT_LIST_DIR}/timer.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers -Wno-implicit-int"
)

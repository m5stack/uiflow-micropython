# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

add_library(usermod_M5UNIFIED INTERFACE)

target_sources(usermod_M5UNIFIED INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_display.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_touch.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified_widgets.c
    ${CMAKE_CURRENT_LIST_DIR}/m5unified.c
    ${CMAKE_CURRENT_LIST_DIR}/mpy_m5gfx.cpp
    ${CMAKE_CURRENT_LIST_DIR}/mpy_m5touch.cpp
    ${CMAKE_CURRENT_LIST_DIR}/mpy_m5unified.cpp
    ${CMAKE_CURRENT_LIST_DIR}/mpy_m5widgets.cpp
)

target_include_directories(usermod_M5UNIFIED INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

if (TINY_FLAG)
    target_compile_definitions(usermod_M5UNIFIED INTERFACE TINY_FONT=1)
endif()

target_link_libraries(usermod INTERFACE usermod_M5UNIFIED)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/m5unified.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers -Wno-implicit-int"
)

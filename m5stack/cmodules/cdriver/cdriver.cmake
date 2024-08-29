# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

add_library(usermod_DRIVER INTERFACE)

target_sources(usermod_DRIVER INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/cdriver.c
    ${CMAKE_CURRENT_LIST_DIR}/max30100/max30100.c
    ${CMAKE_CURRENT_LIST_DIR}/max30100/driver_max30100.c
    ${CMAKE_CURRENT_LIST_DIR}/max30102/max30102.c
    ${CMAKE_CURRENT_LIST_DIR}/max30102/driver_max30102.c
    ${CMAKE_CURRENT_LIST_DIR}/esp_dmx/driver_esp_dmx.c
)

target_include_directories(usermod_DRIVER INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_DRIVER)

set_source_files_properties(
    ${CMAKE_CURRENT_LIST_DIR}/cdriver.c
    PROPERTIES COMPILE_FLAGS
    "-Wno-discarded-qualifiers -Wno-implicit-int"
)

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Set location of base MicroPython directory.
if(NOT MICROPY_DIR)
    get_filename_component(MICROPY_DIR ${PROJECT_DIR}/../micropython/ ABSOLUTE)
endif()

# Set location of the ESP32 port directory.
if(NOT MICROPY_PORT_DIR)
    get_filename_component(MICROPY_PORT_DIR ${CMAKE_CURRENT_LIST_DIR}/.. ABSOLUTE)
endif()

set(MICROPY_PY_TINYUSB ON)

# include(${MICROPY_PORT_DIR}/esp32_common.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/../esp32_common.cmake)

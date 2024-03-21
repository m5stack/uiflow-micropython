# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Set location of base MicroPython directory.
if(NOT MICROPY_DIR)
    get_filename_component(MICROPY_DIR ${PROJECT_DIR}/../micropython/ ABSOLUTE)
endif()

# include(${MICROPY_PORT_DIR}/esp32_common.cmake)
include(${CMAKE_CURRENT_SOURCE_DIR}/../esp32_common.cmake)
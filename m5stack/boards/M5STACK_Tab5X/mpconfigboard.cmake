# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Tab5X uses the same board implementation as Tab5.  Only the board ID and
# minimum ESP32-P4 silicon revision differ.
include(${CMAKE_CURRENT_LIST_DIR}/../M5STACK_Tab5/mpconfigboard.cmake)

set(BOARD_ID 35)
list(APPEND SDKCONFIG_DEFAULTS
    boards/M5STACK_Tab5X/sdkconfig.p4x
)

message(STATUS "M5STACK_Tab5X reuses M5STACK_Tab5 board configuration")

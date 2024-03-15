# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# LVGL support
if(BUILD_WITH_LVGL)
    message(STATUS "Build with LVGL enable...")
    include(${PROJECT_DIR}/CMakeListsLvgl.cmake)
else()
    include(${PROJECT_DIR}/CMakeListsDefault.cmake)
endif()

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Top-level cmake file for building MicroPython on ESP32.

cmake_minimum_required(VERSION 3.16)

set(CMAKE_C_FLAGS "-Wno-unused-variable -Wno-unused-but-set-variable")
set(CMAKE_CXX_FLAGS "-Wno-unused-variable -Wno-unused-but-set-variable -Wno-pmf-conversions -Wno-error=narrowing")

# Set the location of this port's directory.
set(MICROPY_PORT_DIR ${CMAKE_SOURCE_DIR}/../micropython/ports/esp32)

# Set the board if it's not already set.
if(NOT MICROPY_BOARD)
    set(MICROPY_BOARD M5STACK_4MB)
endif()

# Set the board directory and check that it exists.
if(NOT MICROPY_BOARD_DIR)
    set(MICROPY_BOARD_DIR ${CMAKE_SOURCE_DIR}/boards/${MICROPY_BOARD})
endif()
if(NOT EXISTS ${MICROPY_BOARD_DIR}/mpconfigboard.cmake)
    message(FATAL_ERROR "Invalid MICROPY_BOARD specified: ${MICROPY_BOARD}")
endif()

# Define the output sdkconfig so it goes in the build directory.
set(SDKCONFIG ${CMAKE_BINARY_DIR}/sdkconfig)

# Save the manifest file set from the cmake command line.
set(MICROPY_USER_FROZEN_MANIFEST ${MICROPY_FROZEN_MANIFEST})

# Include board config; this is expected to set SDKCONFIG_DEFAULTS (among other options).
include(${MICROPY_BOARD_DIR}/mpconfigboard.cmake)

# Set the frozen manifest file. Note if MICROPY_FROZEN_MANIFEST is set from the cmake
# command line, then it will override the default and any manifest set by the board.
if (MICROPY_USER_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${MICROPY_USER_FROZEN_MANIFEST})
elseif (NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_CURRENT_LIST_DIR}/boards/manifest.py)
endif()

# Add sdkconfig fragments that depend on the IDF version.
if(IDF_VERSION_MAJOR EQUAL 4 AND IDF_VERSION_MINOR LESS 2)
    set(SDKCONFIG_DEFAULTS ${SDKCONFIG_DEFAULTS} boards/sdkconfig.nimble_core0)
else()
    set(SDKCONFIG_DEFAULTS ${SDKCONFIG_DEFAULTS} boards/sdkconfig.nimble_core1)
endif()

# Concatenate all sdkconfig files into a combined one for the IDF to use.
file(WRITE ${CMAKE_BINARY_DIR}/sdkconfig.combined.in "")
foreach(SDKCONFIG_DEFAULT ${SDKCONFIG_DEFAULTS})
    file(READ ${SDKCONFIG_DEFAULT} CONTENTS)
    file(APPEND ${CMAKE_BINARY_DIR}/sdkconfig.combined.in "${CONTENTS}")
endforeach()
configure_file(${CMAKE_BINARY_DIR}/sdkconfig.combined.in ${CMAKE_BINARY_DIR}/sdkconfig.combined COPYONLY)
set(SDKCONFIG_DEFAULTS ${CMAKE_BINARY_DIR}/sdkconfig.combined)

if(BUILD_WITH_LVGL)
    # Include LVGL component, ignore KCONFIG
    idf_build_set_property(LV_MICROPYTHON 1)
    idf_build_component(${CMAKE_SOURCE_DIR}/components/lv_bindings/lvgl)
    idf_build_set_property(COMPILE_DEFINITIONS "-DLV_KCONFIG_IGNORE" APPEND)
    separate_arguments(LV_CFLAGS_ENV UNIX_COMMAND $ENV{LV_CFLAGS})
    list(APPEND LV_CFLAGS ${LV_CFLAGS_ENV})
    idf_build_set_property(COMPILE_DEFINITIONS "${LV_CFLAGS}" APPEND)
endif()

# Include main IDF cmake file.
include($ENV{IDF_PATH}/tools/cmake/project.cmake)

# Set the location of the main component for the project (one per target).
list(APPEND EXTRA_COMPONENT_DIRS main_${IDF_TARGET})
list(APPEND EXTRA_COMPONENT_DIRS ../m5stack/components/esp32-camera)
list(APPEND EXTRA_COMPONENT_DIRS ../m5stack/components/libffi)
# list(APPEND EXTRA_COMPONENT_DIRS ../m5stack/components/lv_bindings)
list(APPEND EXTRA_COMPONENT_DIRS ../m5stack/components/M5Unified/M5GFX)
list(APPEND EXTRA_COMPONENT_DIRS ../m5stack/components/M5Unified/M5Unified)
list(APPEND EXTRA_COMPONENT_DIRS ./components/BOX3GFX)
list(APPEND EXTRA_COMPONENT_DIRS ../m5stack/components/uiflow_utility)
# list(APPEND EXTRA_COMPONENT_DIRS ./boards)

# Define the project.
project(micropython)

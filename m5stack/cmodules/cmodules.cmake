# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# add cdrivers
include(${CMAKE_CURRENT_LIST_DIR}/cdriver/cdriver.cmake)
include(${CMAKE_CURRENT_LIST_DIR}/m5utils/m5utils.cmake)

if (M5_CAMERA_MODULE_ENABLE)
    if (BOARD_TYPE STREQUAL "cores3")
        # Add OMV modules
        include(${CMAKE_CURRENT_LIST_DIR}/omv/micropython.cmake)
    else()
        # Add M5Camera module
        include(${CMAKE_CURRENT_LIST_DIR}/m5camera/m5camera.cmake)
    endif()
endif()

# add m5can module
include(${CMAKE_CURRENT_LIST_DIR}/m5can/m5can.cmake)

# add m5things module
include(${CMAKE_CURRENT_LIST_DIR}/m5things/m5things.cmake)

# add m5unified module
include(${CMAKE_CURRENT_LIST_DIR}/m5unified/m5unified.cmake)

if(ADF_MODULE_ENABLE)
    include(${CMAKE_CURRENT_LIST_DIR}/adf_module/micropython.cmake)
endif()

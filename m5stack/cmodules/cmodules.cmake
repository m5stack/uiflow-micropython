# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# add m5camera module
if(M5_CAMERA_MODULE_ENABLE)
    include(${CMAKE_CURRENT_LIST_DIR}/m5camera/m5camera.cmake)
endif()

# add m5can module
include(${CMAKE_CURRENT_LIST_DIR}/m5can/m5can.cmake)

# add m5things module
include(${CMAKE_CURRENT_LIST_DIR}/m5things/m5things.cmake)

# add m5unified module
include(${CMAKE_CURRENT_LIST_DIR}/m5unified/m5unified.cmake)

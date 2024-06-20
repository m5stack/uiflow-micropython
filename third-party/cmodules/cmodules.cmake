# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

if(M5_CAMERA_MODULE_ENABLE)
    # add m5camera module
    include(${CMAKE_CURRENT_LIST_DIR}/../../m5stack/cmodules/m5camera/m5camera.cmake)
endif()

# add m5can module
include(${CMAKE_CURRENT_LIST_DIR}/../../m5stack/cmodules/m5can/m5can.cmake)

# add m5unified module
if(M5_UNIFIED_MODULE_ENABLE)
    include(${CMAKE_CURRENT_LIST_DIR}/m5unified/m5unified.cmake)
endif()
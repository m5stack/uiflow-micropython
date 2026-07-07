# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
include(${CMAKE_CURRENT_LIST_DIR}/../../m5stack/cmodules/m5utils/m5utils.cmake)

if(M5_CAMERA_MODULE_ENABLE)
    # add m5camera module
    include(${CMAKE_CURRENT_LIST_DIR}/../../m5stack/cmodules/m5camera/m5camera.cmake)
endif()

# add m5can module
include(${CMAKE_CURRENT_LIST_DIR}/../../m5stack/cmodules/m5can/m5can.cmake)

if(MICROPY_BOARD STREQUAL "ESPRESSIF_ESP32_S3_BOX_3" OR MICROPY_BOARD STREQUAL "SEEED_STUDIO_XIAO_ESP32S3")
    # add m5things module
    include(${CMAKE_CURRENT_LIST_DIR}/../../m5stack/cmodules/m5things/m5things.cmake)
    target_include_directories(usermod_M5THING INTERFACE
        ${CMAKE_CURRENT_LIST_DIR}/../../m5stack/components/m5things/include
    )
endif()

# add m5unified module
if(M5_UNIFIED_MODULE_ENABLE)
    include(${CMAKE_CURRENT_LIST_DIR}/m5unified/m5unified.cmake)
endif()

if(ADF_MODULE_ENABLE)
    include(${CMAKE_CURRENT_LIST_DIR}/../../m5stack/cmodules/adf_module/micropython.cmake)
endif()

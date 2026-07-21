# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

add_library(usermod_LT6911 INTERFACE)

target_sources(usermod_LT6911 INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/lt6911.c
)

target_include_directories(usermod_LT6911 INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/driver/include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/conversions/include
    $ENV{IDF_PATH}/components/esp_driver_cam/include
    $ENV{IDF_PATH}/components/esp_driver_cam/csi/include
    $ENV{IDF_PATH}/components/esp_driver_isp/include
)

target_link_libraries(usermod INTERFACE usermod_LT6911)

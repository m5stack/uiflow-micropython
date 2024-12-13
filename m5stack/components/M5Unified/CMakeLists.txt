# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(COMPONENT_ADD_INCLUDEDIRS
    M5Unified/src
    M5GFX/src/
    .
)

file(GLOB SRCS
    M5GFX/src/*.cpp
    M5GFX/src/lgfx/Fonts/efont/*.c
    M5GFX/src/lgfx/Fonts/IPA/*.c
    M5GFX/src/lgfx/utility/*.c
    M5GFX/src/lgfx/v1/*.cpp
    M5GFX/src/lgfx/v1/misc/*.cpp
    M5GFX/src/lgfx/v1/panel/*.cpp
    M5GFX/src/lgfx/v1/platforms/esp32/*.cpp
    M5GFX/src/lgfx/v1/platforms/esp32c3/*.cpp
    M5GFX/src/lgfx/v1/touch/*.cpp
    M5Unified/src/*.cpp
    M5Unified/src/utility/*.cpp
    M5Unified/src/utility/imu/*.cpp
    *.cpp
)

set(COMPONENT_SRCS ${SRCS})
if (IDF_VERSION_MAJOR GREATER_EQUAL 5)
    set(COMPONENT_REQUIRES esp_adc nvs_flash efuse driver esp_timer epdiy main_${IDF_TARGET})
else()
    set(COMPONENT_REQUIRES esp_adc_cal nvs_flash efuse main)
endif()

register_component()
target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-format")
target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-array-bounds")
target_compile_definitions(${COMPONENT_LIB} PRIVATE BOARD_ID=${BOARD_ID})
target_compile_definitions(${COMPONENT_LIB} PRIVATE M5GFX_BOARD=${BOARD_ID})

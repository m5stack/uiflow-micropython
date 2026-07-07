# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(COMPONENT_ADD_INCLUDEDIRS
    M5Unified/src
    M5GFX/src/
    LGFX_Fonts/src/
    ../../cmodules/lv_binding_micropython
    .
)

file(GLOB SRCS
    fonts/*.c
    M5GFX/src/*.cpp
    M5GFX/src/lgfx/Fonts/efont/*.c
    M5GFX/src/lgfx/Fonts/IPA/*.c
    M5GFX/src/lgfx/Fonts/lvgl/*.c
    M5GFX/src/lgfx/utility/*.c
    M5GFX/src/lgfx/v1/*.cpp
    M5GFX/src/lgfx/v1/lv_font/*.c
    M5GFX/src/lgfx/v1/misc/*.cpp
    M5GFX/src/lgfx/v1/panel/*.cpp
    M5GFX/src/lgfx/v1/platforms/esp32/*.cpp
    M5GFX/src/lgfx/v1/platforms/esp32c3/*.cpp
    M5GFX/src/lgfx/v1/platforms/esp32s3/*.cpp
    M5GFX/src/lgfx/v1/platforms/esp32p4/*.cpp
    M5GFX/src/lgfx/v1/touch/*.cpp
    LGFX_Fonts/src/*.cpp
    LGFX_Fonts/src/Fonts/lvgl/*.c
    LGFX_Fonts/src/utility/lvgl/*.c
    LGFX_Fonts/src/utility/lvgl/*.cpp
    LGFX_Fonts/src/utility/emojis/*.cpp
    M5Unified/src/*.cpp
    M5Unified/src/utility/*.cpp
    M5Unified/src/utility/imu/*.cpp
    M5Unified/src/utility/led/*.cpp
    M5Unified/src/utility/power/*.cpp
    M5Unified/src/utility/rtc/*.cpp
    *.cpp
)

set(COMPONENT_SRCS ${SRCS})
if (IDF_VERSION_MAJOR GREATER_EQUAL 5)
    set(COMPONENT_REQUIRES esp_adc nvs_flash efuse driver esp_timer esp_lcd main)
else()
    set(COMPONENT_REQUIRES esp_adc_cal nvs_flash efuse esp_lcd main)
endif()

register_component()
target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-format")
target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-array-bounds")
target_compile_definitions(${COMPONENT_LIB} PRIVATE BOARD_ID=${BOARD_ID})
target_compile_definitions(${COMPONENT_LIB} PRIVATE M5GFX_BOARD=${BOARD_ID})
target_compile_definitions(${COMPONENT_LIB} PRIVATE
    LV_FONT_MONTSERRAT_12=${FONT_MONTSERRAT_12}
    LV_FONT_MONTSERRAT_14=${FONT_MONTSERRAT_14}
    LV_FONT_MONTSERRAT_16=${FONT_MONTSERRAT_16}
    LV_FONT_MONTSERRAT_18=${FONT_MONTSERRAT_18}
    LV_FONT_MONTSERRAT_20=${FONT_MONTSERRAT_20}
    LV_FONT_MONTSERRAT_22=${FONT_MONTSERRAT_22}
    LV_FONT_MONTSERRAT_24=${FONT_MONTSERRAT_24}
    LV_FONT_MONTSERRAT_30=${FONT_MONTSERRAT_30}
    LV_FONT_MONTSERRAT_36=${FONT_MONTSERRAT_36}
    LV_FONT_MONTSERRAT_40=${FONT_MONTSERRAT_40}
    LV_FONT_MONTSERRAT_44=${FONT_MONTSERRAT_44}
    LV_FONT_MONTSERRAT_48=${FONT_MONTSERRAT_48}
    USR_FONT_ALIBABAPUHUITI_CN24=${FONT_ALIBABAPUHUITI_CN24}
    USR_FONT_ALIBABASANS_JA24=${FONT_ALIBABASANS_JA24}
    USR_FONT_ALIBABASANS_KR24=${FONT_ALIBABASANS_KR24}
)

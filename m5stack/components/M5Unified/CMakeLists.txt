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
    *.cpp
)

set(COMPONENT_SRCS ${SRCS})
set(COMPONENT_REQUIRES esp_adc_cal nvs_flash efuse main)

register_component()

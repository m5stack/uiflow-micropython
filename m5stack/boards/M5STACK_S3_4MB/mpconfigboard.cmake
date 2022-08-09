set(IDF_TARGET esp32s3)

set(SDKCONFIG_DEFAULTS
    ./boards/sdkconfig.base
    ./boards/sdkconfig.usb
    ./boards/sdkconfig.ble
    ./boards/M5STACK_S3_4MB/sdkconfig.board
    ./boards/sdkconfig.flash_4mb
)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_SOURCE_DIR}/boards/manifest.py)
endif()

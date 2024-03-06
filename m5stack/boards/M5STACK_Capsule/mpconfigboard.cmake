set(IDF_TARGET esp32s3)

# capsule https://github.com/m5stack/m5stack-board-id/blob/558d0c4e4fc55a72805827c65a5255aa4b844515/board.csv#L29
set(BOARD_ID 139)

set(SDKCONFIG_DEFAULTS
    ./boards/M5STACK_S3_8MB/sdkconfig.board
    ./boards/sdkconfig.base
    ./boards/sdkconfig.240mhz
    ./boards/sdkconfig.disable_iram
    ./boards/sdkconfig.ble
    ./boards/sdkconfig.usb
    ./boards/sdkconfig.flash_8mb
)

# If not enable LVGL, ignore this...
set(LV_CFLAGS -DLV_COLOR_DEPTH=16 -DLV_COLOR_16_SWAP=0)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_SOURCE_DIR}/boards/manifest.py)
endif()

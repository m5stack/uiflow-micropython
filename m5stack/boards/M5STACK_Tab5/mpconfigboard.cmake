set(IDF_TARGET esp32p4)

# https://github.com/m5stack/m5stack-board-id/blob/main/board.csv#L12
set(BOARD_ID 22)
set(MICROPY_PY_LVGL 1)
# Enable camera module
# set(M5_CAMERA_MODULE_ENABLE TRUE)

set(SDKCONFIG_DEFAULTS
    # boards/M5STACK_Tab5/sdkconfig.board
    ./boards/sdkconfig.base
    ${SDKCONFIG_IDF_VERSION_SPECIFIC}
    # ./boards/sdkconfig.240mhz
    ./boards/sdkconfig.disable_iram
    # ./boards/sdkconfig.ble
    # ./boards/sdkconfig.usb
    # ./boards/sdkconfig.usb_cdc
    ./boards/sdkconfig.flash_16mb_omv
    ./boards/sdkconfig.freertos
    ./boards/M5STACK_Tab5/sdkconfig.freertos
    ./boards/M5STACK_Tab5/sdkconfig.spiram_hex
    ./boards/M5STACK_Tab5/sdkconfig.adf
    ./boards/M5STACK_Tab5/sdkconfig.esp_hosted
)

# If not enable LVGL, ignore this...
set(LV_CFLAGS 
    -DLV_COLOR_DEPTH=16
    -DLV_COLOR_16_SWAP=0
    -DLV_FONT_MONTSERRAT_24=1
    -DLV_FONT_MONTSERRAT_22=1
    -DLV_FONT_MONTSERRAT_20=1
    -DLV_FONT_MONTSERRAT_18=1
    -DLV_FONT_MONTSERRAT_14=1
    -DLV_FONT_MONTSERRAT_30=1
)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${CMAKE_SOURCE_DIR}/boards/manifest.py)
endif()

set(ADF_MODULE_ENABLE TRUE)

set(ADF_COMPS     "$ENV{ADF_PATH}/components")

set(ADF_BOARD_INIT_SRC
    $ENV{ADF_PATH}/components
    M5STACK_Tab5/board_init.c
)

list(APPEND EXTRA_COMPONENT_DIRS
    ${CMAKE_SOURCE_DIR}/boards
    $ENV{ADF_PATH}/components/audio_pipeline
    $ENV{ADF_PATH}/components/audio_sal
    $ENV{ADF_PATH}/components/esp-adf-libs
    $ENV{ADF_PATH}/components/esp-sr
)

message(STATUS "M5STACK_Tab5/CMakeLists.txt: EXTRA_COMPONENT_DIRS=${EXTRA_COMPONENT_DIRS}")

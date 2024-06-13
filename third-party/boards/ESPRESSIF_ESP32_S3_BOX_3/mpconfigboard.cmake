set(IDF_TARGET esp32s3)

set(BOARD_ID 2)

set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.spiram_sx
    boards/sdkconfig.spiram_oct
    boards/sdkconfig.base
    boards/sdkconfig.ble
    boards/sdkconfig.240mhz
    boards/sdkconfig.flash_16mb
    boards/sdkconfig.usb
    boards/sdkconfig.disable_iram
    # $ENV{ADF_PATH}/micropython_adf/sdkconfig.adf
    boards/ESPRESSIF_ESP32_S3_BOX_3/sdkconfig.s3box3
)

# Enable unified module
set(M5_UNIFIED_MODULE_ENABLE TRUE)

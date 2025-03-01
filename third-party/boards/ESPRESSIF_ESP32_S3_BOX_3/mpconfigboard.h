#define MICROPY_HW_BOARD_NAME               "Espressif ESP32-S3-BOX-3"
#define MICROPY_HW_MCU_NAME                 "ESP32S3"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB.
#define MICROPY_HW_ENABLE_UART_REPL         (1)

// #define MICROPY_HW_I2C0_SCL                 (9)
// #define MICROPY_HW_I2C0_SDA                 (8)

#define MICROPY_HW_USB_CDC_INTERFACE_STRING  "Espressif ESP32-S3-BOX-3(UiFlow2)"

#define AUDIO_RECORDER_DOWN_CH (1)
#define MICROPY_PY_MACHINE_I2S (0)
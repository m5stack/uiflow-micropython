#define MICROPY_HW_BOARD_NAME               "M5STACK Dial"
#define MICROPY_HW_MCU_NAME                 "ESP32-S3-FN8"

#define MICROPY_PY_MACHINE_DAC              (0)

// Enable UART REPL for modules that have an external USB-UART and don't use native USB.
#define MICROPY_HW_ENABLE_UART_REPL         (1)

#define MICROPY_HW_I2C0_SCL                 (9)
#define MICROPY_HW_I2C0_SDA                 (8)

// If not enable LVGL, ignore this...
#include "./../mpconfiglvgl.h"

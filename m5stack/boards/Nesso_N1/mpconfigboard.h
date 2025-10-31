#define MICROPY_HW_BOARD_NAME    "Nesso N1"
#define MICROPY_HW_MCU_NAME      "ESP32C6"

#define MICROPY_HW_ENABLE_SDCARD (0)
#define MICROPY_PY_MACHINE_I2S   (0)

#define MICROPY_HW_I2C0_SCL      (4)
#define MICROPY_HW_I2C0_SDA      (5)

// ESP32-C6 SPI configuration
// ESP32-C6 only has SPI2 (HSPI), SPI3 is not available
// Default SPI2 pins for ESP32-C6
#define MICROPY_HW_SPI1_SCK      (6)   // GPIO6 - SCLK
#define MICROPY_HW_SPI1_MOSI     (7)   // GPIO7 - MOSI  
#define MICROPY_HW_SPI1_MISO     (2)   // GPIO2 - MISO

// #define MICROPY_HW_USB_CDC_INTERFACE_STRING  "M5Stack UnitC6L(UiFlow2)"

// #ifndef MICROPY_HW_ENABLE_USB_RUNTIME_DEVICE
// #define MICROPY_HW_ENABLE_USB_RUNTIME_DEVICE (1) // Support machine.USBDevice
// #endif


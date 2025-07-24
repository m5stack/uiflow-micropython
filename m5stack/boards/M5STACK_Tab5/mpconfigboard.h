// Both of these can be set by mpconfigboard.cmake if a BOARD_VARIANT is
// specified.

#ifndef MICROPY_HW_BOARD_NAME
#define MICROPY_HW_BOARD_NAME "M5STACK Tab5"
#endif

#ifndef MICROPY_HW_MCU_NAME
#define MICROPY_HW_MCU_NAME "ESP32P4"
#endif

#define MICROPY_HW_ENABLE_USBDEV (0)
#define MICROPY_PY_ESPNOW (0)

// #ifndef MICROPY_HW_ENABLE_USB_RUNTIME_DEVICE
// #define MICROPY_HW_ENABLE_USB_RUNTIME_DEVICE (1) // Support machine.USBDevice
// #endif

#define MICROPY_GC_INITIAL_HEAP_SIZE (128 * 1024)
#define MICROPY_CACHE_SIZE (1024)

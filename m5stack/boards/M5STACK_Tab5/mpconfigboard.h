// Both of these can be set by mpconfigboard.cmake if a BOARD_VARIANT is
// specified.

#ifndef MICROPY_HW_BOARD_NAME
#define MICROPY_HW_BOARD_NAME "M5STACK Tab5"
#endif

#ifndef MICROPY_HW_MCU_NAME
#define MICROPY_HW_MCU_NAME "ESP32P4"
#endif

#define MICROPY_HW_USB_VID 0x303A
#define MICROPY_HW_USB_PID 0x817A
#define MICROPY_HW_USB_MANUFACTURER_STRING "M5Stack"
#define MICROPY_HW_USB_PRODUCT_FS_STRING "Tab5(UiFlow2)"
#define MICROPY_HW_USB_CDC_INTERFACE_STRING "Tab5(UiFlow2)"

#define MICROPY_PY_ESPNOW (0)

#define MICROPY_GC_INITIAL_HEAP_SIZE (128 * 1024)

// USB-C: full-speed OTG device (CDC/REPL and machine.USBDevice).
// USB-A: reserve the high-speed OTG controller for the HID Host driver.
#define MICROPY_HW_USB_HS (0)
#define MICROPY_HW_USB_FS_PHY (0)
#define CFG_TUSB_RHPORT0_MODE (OPT_MODE_DEVICE | OPT_MODE_FULL_SPEED)
#define MICROPY_HW_ESP_USB_SERIAL_JTAG (0)
#define MICROPY_HW_USB_HOST_HID (1)

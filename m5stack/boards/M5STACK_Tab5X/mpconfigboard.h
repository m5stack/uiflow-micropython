#pragma once

// Tab5X shares all hardware definitions with Tab5.
#include "../M5STACK_Tab5/mpconfigboard.h"

#undef MICROPY_HW_BOARD_NAME
#define MICROPY_HW_BOARD_NAME "M5STACK Tab5X"

#undef MICROPY_HW_USB_PRODUCT_FS_STRING
#define MICROPY_HW_USB_PRODUCT_FS_STRING "Tab5X(UiFlow2)"

#undef MICROPY_HW_USB_CDC_INTERFACE_STRING
#define MICROPY_HW_USB_CDC_INTERFACE_STRING "Tab5X(UiFlow2)"

#ifndef MICROPY_HW_BOARD_NAME
#define MICROPY_HW_BOARD_NAME "M5Stack CoreP4X"
#endif

#ifndef MICROPY_HW_MCU_NAME
#define MICROPY_HW_MCU_NAME "ESP32P4"
#endif

#define MICROPY_PY_ESPNOW                (0)
#define MICROPY_PY_BLUETOOTH            (1)
#define MICROPY_HW_ENABLE_SDCARD        (1)
#define MICROPY_PY_MACHINE_I2C_TARGET   (0)
#define MICROPY_PY_MACHINE_I2S          (1)
#define MICROPY_TASK_STACK_SIZE          (48 * 1024)
#define MICROPY_BOARD_STARTUP boardctrl_startup

void boardctrl_startup(void);

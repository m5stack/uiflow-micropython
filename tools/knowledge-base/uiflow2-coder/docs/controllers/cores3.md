# CoreS3

Support the following products:

    CoreS3

## Supported Components

CoreS3 supports the following components:

- `M5UI`: The `m5ui` LVGL component library.
- `Module`: The `module` package for expansion modules.
- `Unit`: The `unit` package containing Unit drivers.
- `USB`: The `usb.device` package for HID devices.
- [M5Camera](../advanced/camera.md): The frozen `m5camera.py` camera helper.
- `Chain`: The `chain` package for Chain devices.

## Supported Display Fonts

The CoreS3 firmware includes the following Montserrat fonts for LVGL and M5UI:
`lv.font_montserrat_12`, `lv.font_montserrat_14`, `lv.font_montserrat_16`,
`lv.font_montserrat_18`, `lv.font_montserrat_24`, `lv.font_montserrat_40`,
`lv.font_montserrat_44`, and `lv.font_montserrat_48`.

For `M5.Lcd.FONTS`, the firmware also provides `AlibabaPuHuiTiCN24`,
`AlibabaSansJA24`, and `AlibabaSansKR24` for Chinese, Japanese, and Korean
text respectively.

## Board Features

CoreS3 supports the following built-in functions and board peripherals:

- [Display](../hardware/display.md): 2.0-inch, 320 x 240 color LCD output.
- [Touch](../hardware/touch.md): Capacitive touch input.
- [IMU](../hardware/imu.md): BMI270 accelerometer and gyroscope, and BMM150 magnetometer readings.
- [ALS](../hardware/als.md): Built-in LTR-553ALS-WA ambient light sensor readings.
- [Camera](../advanced/camera.md): Image capture with the built-in GC0308 camera.
- [Speaker](../hardware/speaker.md) playback and [microphone](../hardware/mic.md) recording.
- BM8563 real-time clock for date and time keeping.
- [Power](../system/power.md): Battery, charging, and external output power management.
- microSD card access through `hardware.SDCard`.
- Grove and M-BUS expansion interfaces.

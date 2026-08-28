# ToughC5

Support the following products:

    ToughC5

## Supported Components

The ToughC5 firmware includes the following user-facing packages:

- `M5UI`: The `m5ui` LVGL component library.
- `Module`: The `module` package for M-BUS expansion modules.
- `Unit`: The `unit` package containing Unit drivers.
- `Chain`: The `chain` package for Chain devices.
- `Hardware`: The `hardware` package for `Speaker`,
  `Touch`, `SDCard`, and `PWR485`.

## Supported Display Fonts

The ToughC5 firmware includes the following Montserrat fonts for LVGL and M5UI:
`lv.font_montserrat_12`, `lv.font_montserrat_14`, `lv.font_montserrat_16`,
`lv.font_montserrat_18`, `lv.font_montserrat_24`, `lv.font_montserrat_40`,
`lv.font_montserrat_44`, and `lv.font_montserrat_48`.

For `M5.Lcd.FONTS`, the firmware also provides `AlibabaPuHuiTiCN24`,
`AlibabaSansJA24`, and `AlibabaSansKR24` for Chinese, Japanese, and Korean
text respectively.

## Board Features

ToughC5 supports the following built-in functions and peripherals:

- ESP32-C5 microcontroller.
- 320 x 240 ILI9342 color LCD output through `M5.Display`.
- CHSC6540 capacitive touch input through `M5.Touch`.
- Buzzer tone output through `M5.Speaker`.
- RX8130 real-time clock through `M5.Rtc`.
- Battery, VBUS, charging, and external output power management through `M5.Power`.
- microSD card access through `hardware.SDCard`. The SD interface uses SPI pins
  GPIO9 (SCK), GPIO7 (MOSI), GPIO8 (MISO), and GPIO10 (CS).
- Port A I2C through `M5.Ex_I2C`. Port A uses GPIO3 (SCL) and GPIO2 (SDA)
  and shares the internal I2C bus.
- Port B GPIO on GPIO1 and GPIO6, and Port C GPIO on GPIO12 and GPIO11.

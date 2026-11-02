# M5Stack Chain Captain

## Overview

- MCU: ESP32-S3R8
- Flash: 16 MB, DIO at 80 MHz
- PSRAM: 8 MB Octal PSRAM at 80 MHz
- Runtime config: `board.json`
- Board name: `M5STACK_ChainCaptain`

## Build

```bash
cd /home/loki/uiflow_dev/uiflow_micropython
make submodules
make patch
make littlefs
make mpy-cross
make BOARD=M5STACK_ChainCaptain pack_all
```

## Display

- `interface`: `spi`
- `driver`: `st7789`
- Resolution: `240x240`
- SPI host: `SPI2_HOST`
- SPI baudrate: `40000000`
- Pins: SCK `GPIO15`, MOSI `GPIO16`, MISO `-1`, CS `GPIO45`, DC `GPIO46`
- Control: power `M5IOE1_G12`, reset `M5IOE1_G1`, backlight `M5IOE1_G11` / `PWM_CH3`
- Config: `x_gap: 0`, `y_gap: 80`, `color_order: rgb`, `rgb565_endian: big`, `invert_color: true`, `swap_xy: false`, `mirror_x: true`, `mirror_y: true`

## Buttons

- `btn_a` (`K1`): GPIO `1`, active low
- `btn_b` (`K2`): GPIO `4`, active low
- `btn_c` (`K3`): GPIO `5`, active low
- Power button: managed by M5PM1; single press resets, double press powers off, and long press enters download mode

## Audio

- Codec: ES8311 at 7-bit I2C address `0x18` on system I2C
- Microphone: production part pending confirmation (the V0.2 change record replaces MSM381A3729H9BPC with LMA3729T381-0Y3S)
- Speaker PA: AW8737A on `GPIO21`, using one-wire mode selection; test firmware uses the 1 W mode
- I2S port: `I2S0`
- I2S pins: MCLK `GPIO40`, BCLK `GPIO38`, WS `GPIO41`, DOUT `GPIO42`, DIN `GPIO39`
- Default input sample rate: 16 kHz
- Default output sample rate: 44.1 kHz
- Audio rail: `M5IOE1_G5`, active high
- Recording and playback are supported by the sample-test firmware

## Power / Backlight

- PMIC: M5PM1 at 7-bit I2C address `0x6E`
- I/O expander: M5IOE1 at 7-bit I2C address `0x4F`
- Charger: LGS4056; charging is enabled through `M5PM1_CHG_EN`, and `M5IOE1_G3` is active low while charging
- Battery boost: `M5IOE1_G4`, active high
- PORT.A/GROVE output: `M5PM1_G0`, active high
- PORT.B/CHAIN output: `M5PM1_G3`, active high
- USB and PORT.A/GROVE share the M5PM1 5 V input measurement path; 5VIN and PORT.B/CHAIN share the M5PM1 5 V input/output measurement path
- LCD rail: `M5IOE1_G12`, active high
- Backlight: `M5IOE1_G11`, `PWM_CH3`, adjustable from 0 to 100%
- RTC uses the always-on `3V3_L0` rail and can wake the PMIC; tested low-power firmware also supports IMU wakeup

## Other Hardware

- System I2C: port `0`, SDA `GPIO3`, SCL `GPIO2`
- IMU: BMI270 at `0x68`; interrupt is routed through `M5PM1_G4` to the PMIC interrupt path
- Magnetometer: BMM150 at `0x10` through the BMI270 auxiliary interface
- RTC: RX8130CE at `0x32`; interrupt is routed through `M5PM1_G2`
- PMIC interrupt output: `M5PM1_G1` to `GPIO14`
- IR: power `M5IOE1_G2`, TX `GPIO48`, RX `GPIO47`; test firmware uses a 38 kHz carrier
- RGB LED: red `M5IOE1_G10` / `PWM_CH4`, green `M5IOE1_G8` / `PWM_CH2`, blue `M5IOE1_G9` / `PWM_CH1`
- PORT.A/GROVE: `GPIO6`, `GPIO7`, with power controlled by `M5PM1_G0`
- PORT.B/CHAIN: `GPIO17`, `GPIO18`, with power controlled by `M5PM1_G3`
- 15-pin header: 5VIN, VBAT, 3V3_L2, CHIP_EN, `GPIO0` boot, `GPIO44` U0RXD, `GPIO43` U0TXD, `GPIO8` through `GPIO13`, switched 5VOUT, and GND

## Notes

- The public product and board names are `Chain Captain` and `M5STACK_ChainCaptain`; older test and factory sources use the legacy name `Chain Head`.
- Automatic board detection uses the I2C device signature RX8130 `0x32` + M5IOE1 `0x4F` + BMI270 `0x68` + M5PM1 `0x6E` on system I2C (`SDA GPIO3`, `SCL GPIO2`), and validates the M5PM1 device ID before accepting the board.
- LCD uses `SPI2_HOST`; reset is controlled by `M5IOE1_G1`.
- Audio uses `I2S0`, with the M5Unified defaults of 16 kHz input and 44.1 kHz output used by the established ES8311 path.
- The current V0.5 software test report confirms M5IOE1 at `0x4F`; the top-level legacy hardware notes still contain `0x6F`.
- Controller examples are not implemented at this documentation stage. Hardware validation must cover board ID, full-screen red/green/blue/white/black fills, all buttons, audio recording/playback, power paths, ports, IMU/magnetometer, RTC, IR, and RGB LED.

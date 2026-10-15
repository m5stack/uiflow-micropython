# M5Stack PaperDIY

- **MCU**: ESP32-S3
- **Module**: ESP32-S3-WROOM-1-N16R8
- **PSRAM**: 8MB Octal
- **Flash**: 16MB
- **Display**: 960x540 4.7-inch monochrome EPD

-----------
## Hardware

* **Board Identity**
    * Board ID -- 34 (`board_M5PaperDIY`)
    * Detection -- M5PM1 on System I2C at address `0x6E`.
* **System I2C**
    * SCL -- G42
    * SDA -- G41
    * Pull-ups -- 2.2K to `3V3_L2`
* **M5PM1**
    * Controller: M5PM1
    * Interface: System I2C at address `0x6E`.
    * `PY_MPWR_EN` / pin 14: `3V3_L2` DC/DC enable.
    * `EPD_PWR` / G2 / pin 20: EPD power control.
    * `BAT_ADC_EN` / pin 1: Battery measurement enable.
    * `CHG_STAT` / G3 / pin 13: Charger status input.
    * `PY_LED` / pin 5: Onboard red LED control.
    * `PY_BTN` / pin 7: Power button input.
* **Power**
    * USB-C input protection: AW32901.
    * Battery charger: LGS4056H; the schematic overview specifies an adjustable 0.5-1A charging current.
    * `3V3_L0`: Always-on 3.3V rail.
    * `3V3_L2`: SY8089AAAC switched 3.3V rail, enabled by PMIC `PY_MPWR_EN`.
    * Battery measurement: `BAT_ADC`, gated by PMIC `BAT_ADC_EN`.
    * Power modes: L0 shipping, L1 standby, L2 deep sleep, L3A core active, and L3B all active.
* **Display**
    * Panel: AXE544127 monochrome raw EPD.
    * Resolution: 960x540.
    * Interface: 8-bit parallel GPIO.
    * D0 -- G6
    * D1 -- G14
    * D2 -- G7
    * D3 -- G12
    * D4 -- G9
    * D5 -- G11
    * D6 -- G8
    * D7 -- G10
    * XCL -- G16
    * XLE -- G15
    * XSTL -- G13
    * SPV -- G17
    * CKV -- G18
    * `BST_EN` -- G46
    * `EPD_PWR` -- M5PM1 G2 / pin 20
    * EPD power circuit: MT9700 load switch and MT3608 boost converter.
    * Backlight: Not present.
    * Touch panel: Not present in the detailed schematic.
* **Buttons**
    * KEY1 -- G4, active low, 10K pull-up to `3V3_L0`.
    * KEY2 -- G3, active low, 10K pull-up to `3V3_L0`.
    * PWR_BTN -- M5PM1 `PY_BTN`, active low, 10K pull-up to `3V3_L0`; not connected directly to ESP32-S3.
* **TF Card**
    * MISO -- G40
    * CS -- G47
    * SCK -- G39
    * MOSI -- G38
    * Detect -- G48
    * Power -- `3V3_L2`
* **Stamp / I2S Expansion (JP2)**
    * SCLK -- G5 / pin 1
    * MCLK -- G45 / pin 10
    * DOUT -- G0 / pin 9
    * DSDIN -- G1 / pin 8
    * LRCK -- G2 / pin 7
    * System I2C SDA -- G41 / pin 4
    * System I2C SCL -- G42 / pin 5
    * PMIC `PY_G0` -- pin 3
    * GND -- pins 2 and 6
    * `3V3_L2` -- pins 11 and 12
    * No onboard codec, microphone, speaker, or amplifier is present.
* **Expansion (JP3)**
    * SCK -- G39 / pin 1
    * CS -- G21 / pin 3
    * MOSI -- G38 / pin 4
    * MISO -- G40 / pin 5
    * RST -- PMIC `PY_G4` / pin 7
    * BUSY -- G43 / pin 8
    * IRQ -- G44 / pin 9
    * SW -- PMIC `PY_G1` / pin 10
    * GND -- pins 2 and 6
    * `3V3_L2` -- pins 11 and 12
* **USB-C**
    * USB D- -- G19
    * USB D+ -- G20
    * Used for power input and ESP32-S3 native USB programming.

## Notes

* Hardware source: `[SCH]_PaperDIY_V0.4_20260424_2026_04_29_18_43_29.pdf`, dated 2026-04-24.
* The ESP32-S3-WROOM-1-N16R8 module and 960x540 4.7-inch panel are developer-confirmed values.
* The PMIC is M5PM1 at address `0x6E`; this developer-confirmed identity overrides the erroneous controller label in the schematic.
* The display panel, EPD timing, waveform, rotation, and refresh implementation are the same as M5PaperS3; PaperDIY has no touch panel.
* Schematic conflict: page 1 labels the always-on 3.3V LDO as ME6211C33, while the detailed circuit on page 3 uses LP5907. Confirm the populated part before implementation.

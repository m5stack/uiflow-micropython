# M5Stack StampP4X

## Overview

- MCU: ESP32-P4NRW32, chip revision 3.0 or later (`esp_chip_info_t.revision >= 300`)
- Flash: 16 MB
- PSRAM: 32 MB Octal
- Board ID: `156` (`stampp4x`)
- Runtime config: `board.json`

## Build

```bash
cd /home/loki/uiflow_dev/uiflow_micropython/m5stack
make submodules
make patch
make littlefs
make mpy-cross
make BOARD=M5STACK_StampP4X pack_all
```

## Display

- Not present (headless board)

## Buttons

- No runtime button is configured by the existing StampP4 UiFlow2 support.
- BOOT and RESET button availability, GPIO mapping, and active levels: to be confirmed from the StampP4X hardware source.

## Audio

- Codec/microphone/amplifier: Not configured by the existing StampP4 UiFlow2 support.
- I2S/PDM: Not configured.
- Default input/output sample rate: Not applicable.
- Audio power/PA control: Not configured.
- Runtime support and initialization behavior: No onboard audio path is enabled at this stage.

## Power / Backlight

- Backlight: Not present.
- PMIC, battery, charging, hold, and wakeup integration: Not configured by the existing StampP4 UiFlow2 support.
- Supply rails and power input behavior are unchanged from StampP4; the exact hardware table is to be confirmed from the StampP4X hardware source.

## Other Hardware

- Wi-Fi/BLE coprocessor: ESP32-C6 through ESP-Hosted.
- ESP-Hosted bus: SDIO slot `1`, 4-bit, 40 MHz.
- ESP-Hosted pins: `CMD GPIO44`, `CLK GPIO43`, `D0 GPIO45`, `D1 GPIO46`, `D2 GPIO47`, `D3 GPIO48`, coprocessor reset `GPIO42` active high.
- Flash mode: QIO; external flash size: 16 MB; external PSRAM support: enabled.
- External connectors, exposed GPIOs, USB interfaces, boot straps, and reserved pins are unchanged from StampP4; the exact connector table is to be confirmed from the StampP4X hardware source.

## Notes

- StampP4X is hardware-compatible with StampP4 except for the ESP32-P4 chip revision. StampP4X uses revision 3.0 or later.
- M5Unified should first retain the existing GPIO-based checks for Tab5 and UnitPoEP4, then distinguish the remaining Stamp board by `esp_chip_info_t.revision`: revision `>= 300` is `board_M5StampP4X`; lower revisions are `board_M5StampP4`.
- The StampP4X board sdkconfig must disable `CONFIG_ESP32P4_SELECTS_REV_LESS_V3` and select `CONFIG_ESP32P4_REV_MIN_300=y` instead of `CONFIG_ESP32P4_REV_MIN_0=y`:

  ```ini
  # CONFIG_ESP32P4_SELECTS_REV_LESS_V3 is not set
  CONFIG_ESP32P4_REV_MIN_300=y
  ```
- M5GFX and m5stack-board-id already define `board_M5StampP4X = 156`; the board is headless, so M5Unified owns runtime identification.
- Validation must print the chip revision and `M5.getBoard()`, verify StampP4X reports board ID `156`, verify StampP4 still reports board ID `150`, and exercise ESP-Hosted Wi-Fi/BLE startup.

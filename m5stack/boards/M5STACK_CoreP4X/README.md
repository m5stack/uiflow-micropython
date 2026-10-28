# M5Stack CoreP4X

- **MCU**: ESP32-P4
- **Module**: ESP32-P4NRW32
- **PSRAM**: 32MB
- **Flash**: 16MB
- **Display**: 480x480 ST7102 MIPI DSI LCD with capacitive touch

-----------
## Hardware

* **Board identity and detection**
    * UiFlow2 board name: `M5STACK_CoreP4X`.
    * Board ID: `31` (`corep4x`, `ESP32-P4NRW32`, 16MB flash, 32MB PSRAM).
    * ESP32-P4 silicon revision: `>= 3.0`; the board sdkconfig must select `CONFIG_ESP32P4_REV_MIN_300=y`.

* **System I2C1**
    * SCL -- G9.
    * SDA -- G11.
    * M5IOE1 address: `0x4F`.
    * M5STP2 / PM1 address: `0x6E`.

* **Display**
    * Controller: ST7102.
    * Interface: MIPI DSI, 2 lanes, 600 Mbps per lane.
    * Resolution: 480x480, RGB565.
    * DSI LDO: channel 3, 2500 mV.
    * DPI clock: 24 MHz.
    * Timing: hsync 2, hbp 40, hfp 40, vsync 4, vbp 8, vfp 200.
    * LCD power: M5IOE1_G10, active high.
    * LCD reset: M5IOE1_G11.
    * Backlight: M5IOE1_G9 / PWM1.

* **Touch panel**
    * Controller: CST3530 on I2C1.
    * Resolution: 480x480; X and Y are mirrored by the current panel orientation.
    * Interrupt: G1.
    * Reset: M5IOE1_G8.
    * The M5IOE1 G-numbering above is the board signal name; driver index conversion must follow the M5IOE1 driver convention.

* **Audio**
    * Codec pair: ES8311 speaker DAC and ES7210 microphone ADC.
    * Control interface: I2C1; ES8311 address `0x30`, ES7210 address `0x40`.
    * Data interface: I2S0.
    * MCLK -- G2; BCLK -- G6; WS -- G4; DOUT -- G3; DIN -- G5.
    * Microphone configuration follows verified M5Tab5 settings at 24 kHz; UiFlow2 exposes the legacy stereo API while the codec remains 4-slot TDM.
    * ES7210 CH1 and CH2 connect to MIC1 and MIC2; ES7210 CH3 is the AEC input.
    * Audio rail enable: M5IOE1_G1.
    * ES7210 input remains Tab5-compatible 4-slot TDM: CH1/MIC1, CH3/AEC, CH2/MIC2, CH4.
    * Speaker power amplifier enable: M5IOE1_G3.

* **Power and charging**
    * PMIC: M5STP2 / PM1 on I2C1 at `0x6E`.
    * PM1 reports VIN/5VIN, VBAT, and 5VINOUT voltage rails and controls charging, reboot, and power-off behavior.
    * Charge status: M5IOE1_G6 (driver index 5), active low.
    * PORT.A 5V enable: M5IOE1_G5.
    * USB host 5V enable: M5IOE1_G2.
    * Shared MBUS 3V3 rail enable: M5IOE1_G12. This rail supplies the MBUS, TD_CARD, IMU, infrared, and Ethernet functions.

* **MBUS expansion interface**
    * MBUS is the 2x15-pin expansion interface and is distinct from Unit `PORT.A`.
    * Physical positions: 1 GND, 2 G17; 3 GND, 4 G20; 5 GND, 6 CHIP_EN; 7 G7, 8 G21; 9 G8, 10 G22; 11 G10, 12 3V3; 13 G38/U0RX, 14 G37/U0TX; 15 G15, 16 G14; 17 G11/SDA, 18 G9/SCL; 19 G18, 20 G16; 21 G39, 22 G12; 23 G34, 24 G23; 25 reserved, 26 G19; 27 reserved, 28 5V; 29 reserved, 30 VBAT.
    * M5IOE1_G12 must be enabled before using MBUS peripherals.

* **PORT.A (Unit)**
    * Pin 1 -- GND.
    * Pin 2 -- 5V, controlled by M5IOE1_G5.
    * Pin 3 -- G18 / host UART TX.
    * Pin 4 -- G16 / host UART RX.
    * PORT.B and PORT.C mappings are not yet confirmed.

* **Wi-Fi and Bluetooth**
    * Wi-Fi coprocessor: ESP32-C6 using ESP-Hosted SDIO.
    * Reset -- G42.
    * SDIO CMD -- G44; CLK -- G43; D0 -- G45; D1 -- G46; D2 -- G47; D3 -- G48.
    * Bluetooth uses the ESP-Hosted NimBLE path.

* **IMU**
    * Controller: BMI270 on I2C1 at `0x68`.
    * Interrupt: G0.
    * Shared 3V3 power: M5IOE1_G12.
    * Axis sign: `[1, 1, -1]`.

* **RTC**
    * Controller: RX8130CE on I2C1 at `0x51`.
    * Interrupt: G4.

* **Infrared**
    * RX -- G13.
    * TX -- G49.
    * Shared 3V3 power: M5IOE1_G12.

* **Ethernet**
    * PHY: IP101, address `1`, RMII interface.
    * REF_CLK -- G32; MDC -- G31; MDIO -- G36.
    * TX_EN -- G33; TXD0 -- G41; TXD1 -- G35.
    * CRS_DV -- G28; RXD0 -- G29; RXD1 -- G30.
    * PHY reset -- G52.
    * Shared 3V3 power: M5IOE1_G12.

* **Buttons and switches**
    * GPIO mapping and active levels are not yet confirmed in the supplied hardware source.

## Notes

* Hardware source: `/home/loki/aiflow-dev/m5stack/boards/M5STACK_CoreP4X`.
* Board ID source: `m5stack-board-id/board.csv`, entry `31`.
* The previously published CoreP4X README incorrectly listed 8MB PSRAM; the confirmed board configuration is 32MB PSRAM.
* PORT.B/C and button/switch details remain intentionally unimplemented until their hardware mappings are confirmed.

# uiflow_micropython

## How to build

### Setting up ESP-IDF and the build environment

```shell
mkdir uiflow_workspace && cd uiflow_workspace
git clone https://github.com/m5stack/esp-idf.git
git -C esp-idf checkout 014ee65f1f5e291230e398c4913020be9a6278a1
git -C esp-idf submodule update --init --recursive
./esp-idf/install.sh
. ./esp-idf/export.sh 
```

### Building the firmware

```shell
git clone https://github.com/m5stack/uiflow_micropython
cd uiflow_micropython/m5stack
make submodules # Only need once
make littlefs
make mpy-cross
# atoms3, atoms3-lite
make BOARD=M5STACK_S3_8MB BOARD_TYPE=atoms3 flash # Build and flash to atoms3 baord
# stamps3
make BOARD=M5STACK_S3_8MB BOARD_TYPE=stamps3 flash
# cores3
make BOARD=M5STACK_S3_SPIRAM_16MB BOARD_TYPE=cores3 flash
# atoms3u
make BOARD=M5STACK_S3_8MB BOARD_TYPE=atoms3u flash
# core2,tough
make BOARD=M5STACK_SPIRAM_16MB BOARD_TYPE=core2 flash
# stickcplus2
make BOARD=M5STACK_SPIRAM_8MB BOARD_TYPE=stickcplus2 flash
# stickcplus
make BOARD=M5STACK_4MB BOARD_TYPE=stickcplus flash
```

## License

- [micropython][] Copyright (c) 2013-2023 Damien P. George and licensed under MIT License.
- [umqtt][] Copyright (c) 2013-2014 micropython-lib contributors and licensed under MIT License.
- [urequests][] Copyright (c) 2013-2014 micropython-lib contributors and licensed under MIT License.
- [ir][] Copyright (c) 2020 Peter Hinch and licensed under MIT License.
- [neopixel][] Copyright (c) 2013-2014 micropython-lib contributors and licensed under MIT License.
- [bh1750fvi][] Copyright (c) 2022 Sebastian Wicki and licensed under MIT License.
- [bmp280][] Copyright (c) 2020 Sebastian Wicki and licensed under MIT License.
- [checksum][] Copyright (c) 2022 Sebastian Wicki and licensed under MIT License.
- [dht12][] Copyright (c) 2020 Sebastian Wicki and licensed under MIT License.
- [pcf8563][] Copyright (c) 2020 Sebastian Wicki and licensed under MIT License.
- [qmp6988][] Copyright (c) 2022 Sebastian Wicki and licensed under MIT License.
- [scd40][] Copyright (c) 2022 Sebastian Wicki and licensed under MIT License.
- [sgp30][] Copyright (c) 2022 Sebastian Wicki and licensed under MIT License.
- [sht4x][] Copyright (c) 2021 ladyada for Adafruit and licensed under MIT License.
- [vl53l0x][] Copyright (c) 2017 Tony DiCola for Adafruit Industries and licensed under MIT License.
- [camera][] Copyright (c) 2021 Mauro Riva and licensed under Apache License Version 2.0.

[micropython]: https://github.com/micropython/micropython
[umqtt]: https://github.com/micropython/micropython-lib
[urequests]: https://github.com/micropython/micropython-lib
[ir]: https://github.com/peterhinch/micropython_ir
[neopixel]: https://github.com/micropython/micropython-lib
[bh1750fvi]: https://github.com/gandro/micropython-m5stamp-c3u
[bmp280]: https://github.com/gandro/micropython-m5stickc-plus
[checksum]: https://github.com/gandro/micropython-m5stamp-c3u
[dht12]: https://github.com/gandro/micropython-m5stickc-plus
[pcf8563]: https://github.com/gandro/micropython-m5stickc-plus
[qmp6988]: https://github.com/gandro/micropython-m5stamp-c3u
[scd40]: https://github.com/gandro/micropython-m5stamp-c3u
[sgp30]: https://github.com/gandro/micropython-m5stamp-c3u
[sht4x]: https://github.com/adafruit/Adafruit_CircuitPython_SHT4x
[vl53l0x]: https://github.com/adafruit/Adafruit_CircuitPython_VL53L0X
[camera]: https://github.com/lemariva/micropython-camera-driver

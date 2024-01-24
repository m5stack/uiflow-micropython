# uiflow_micropython

## How to build

### Setting up ESP-IDF and the build environment

```shell
mkdir uiflow_workspace && cd uiflow_workspace
git clone https://github.com/m5stack/esp-idf.git
git -C esp-idf checkout 8fbf4ba6058bcf736317d8a7aa75d0578563c38b
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
# Build and flash
# atoms3
make BOARD=M5STACK_AtomS3 pack_all flash
# atoms3-lite
make BOARD=M5STACK_AtomS3_Lite pack_all flash
# atoms3u
make BOARD=M5STACK_AtomS3U pack_all flash
# core(BASIC/M5GO/GRAY) (Falsh 16MB)
make BOARD=M5STACK_Basic pack_all flash
# core(BASIC/M5GO/GRAY) (Falsh 4MB)
make BOARD=M5STACK_Basic_4MB pack_all flash
# capsule
make BOARD=M5STACK_Capsule pack_all flash
# core2,tough
make BOARD=M5STACK_Core2 pack_all flash
# cores3
make BOARD=M5STACK_CoreS3 pack_all flash
# dial
make BOARD=M5STACK_Dial pack_all flash
# fire
make BOARD=M5STACK_Fire pack_all flash
# stamps3
make BOARD=M5STACK_StampS3 pack_all flash
# stickcplus
make BOARD=M5STACK_StickC_PLUS pack_all flash
# stickcplus2
make BOARD=M5STACK_StickC_PLUS2 pack_all flash
```

## Documentation

API documentation for this library can be found on [Read the Docs](https://uiflow-micropython.readthedocs.io/en/latest/).

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

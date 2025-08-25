# uiflow_micropython

## How to build

### Setting up ESP-IDF and the build environment

```shell
mkdir uiflow_workspace && cd uiflow_workspace
git clone --depth 1 --branch v5.4.2 https://github.com/espressif/esp-idf.git
git -C esp-idf submodule update --init --recursive
./esp-idf/install.sh
. ./esp-idf/export.sh
```

### Building the firmware

```shell
git clone https://github.com/m5stack/uiflow_micropython
cd uiflow_micropython/m5stack
make submodules
make patch
make littlefs
make mpy-cross
make flash_all
```

The default board build the M5STACK_AtomS3 one, You can use the `make BOARD=<board> pack_all` command to specify different development boards for compilation. More BOARD type definitions are located in the [m5stack/boards](./m5stack/boards/) path.

More command support, you can check the [Makefile](./m5stack/Makefile).

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
- [haptic][] Copyright (c) 2022 lbuque and licensed under MIT License.

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
[haptic]: https://github.com/lbuque/haptic

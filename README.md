# uiflow_micropython

## How to build
### Setting up ESP-IDF and the build environment
```shell
mkdir uiflow_workspace && cd uiflow_workspace
git clone https://github.com/m5stack/esp-idf.git
git -C esp-idf checkout 014ee65f1f5e291230e398c4913020be9a6278a1
git -C esp-idf submodule update --init --recursive
./esp-idf/install.sh
```

### Building the firmware
```shell
git clone https://github.com/m5stack/uiflow_micropython
cd uiflow_micropython/m5stack
make submodules
make mpy-cross
make -j
make deploy PORT=/dev/ttyUSBx BAUD=1500000
```

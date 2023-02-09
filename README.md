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
make BOARD=M5STACK_S3_8MB BOARD_TYPE=atoms3 flash # Build and flash to atoms3 baord
```

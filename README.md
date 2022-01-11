# uiflow_micropython

## build

```shell
git clone https://github.com/m5stack/uiflow_micropython --recursive
cd uiflow_micropython/m5stack
make submodules
make mpy-cross
make -j
make deploy PORT=/dev/ttyUSBx BAUD=1500000
```

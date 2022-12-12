## micropython-lib

The drivers in the folder are from this [repository](https://github.com/micropython/micropython-lib).

### How to compile
```shell
export PATH=$PATH:/path/to/micropython/mpy-cross
python ../micropython/tools/mpy_cross_all.py ./libs-py -o ./fs/libs/
```
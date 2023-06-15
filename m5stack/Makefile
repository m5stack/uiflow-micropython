# Makefile for MicroPython on ESP32.
#
# This is a simple, convenience wrapper around idf.py (which uses cmake).

# Select the mcu type to build, default is M5STACK_8MB
# M5STACK_xxx    -> ESP32
# M5STACK_C3_xxx -> ESP32 C3
# M5STACK_S3_xxx -> ESP32 S3

BOARD ?= M5STACK_8MB


# Board type list
BOARD_TYPE_DEF := none atoms3 stamps3 cores3 atoms3u

# Select the board type to build, default is None
# This value affects which folder in the "./fs/res/sys/" directory is pack into "fs.bin"
# If use default value, it means no directory will pack into "fs.bin"
BOARD_TYPE ?= none

ifneq ($(filter $(BOARD_TYPE),$(BOARD_TYPE_DEF)),)
else
    $(error Board type $(BOARD_TYPE) does not exist in list [$(BOARD_TYPE_DEF)])
endif

# esp32c3's bootloader is different with esp32
ifeq (C3, $(findstring C3,${BOARD}))
CHIP ?= esp32c3
BOOTLOADR_OFFSET ?= 0x0
else ifeq (S3, $(findstring S3,${BOARD}))
CHIP ?= esp32s3
BOOTLOADR_OFFSET ?= 0x0
else
CHIP ?= esp32
BOOTLOADR_OFFSET ?= 0x1000
endif

# If the build directory is not given, make it reflect the board name.
BUILD ?= build-$(BOARD)

# Device serial settings.
#PORT ?= /dev/ttyS8
PORT ?= /dev/ttyUSB0
BAUD ?= 1500000

PYTHON ?= python3

GIT_SUBMODULES = lib/berkeley-db-1.xx 

.PHONY: all clean deploy erase mpy-cross submodules fs nvs FORCE

MAKEFILE_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))

USER_C_MODULES = $(MAKEFILE_DIR)cmodules/cmodules.cmake

CMAKE_ARGS =
ifdef USER_C_MODULES
	CMAKE_ARGS += -DUSER_C_MODULES=${USER_C_MODULES}
endif

IDFPY_FLAGS += -DMICROPY_BOARD=$(BOARD) -DBUILD_WITH_LVGL=$(LVGL) -B$(BUILD) $(CMAKE_ARGS)
ifdef FROZEN_MANIFEST
       IDFPY_FLAGS += -D MICROPY_FROZEN_MANIFEST=$(FROZEN_MANIFEST)
endif

LVGL_FLAG = 0
ifdef LVGL
	LVGL_FLAG = 1
endif

GIT_VERSION := $(shell git describe --abbrev=7 --always)

all: build fs nvs
	@$(PYTHON) makeimg.py \
		$(BUILD)/sdkconfig \
		$(BUILD)/bootloader/bootloader.bin \
		$(BUILD)/partition_table/partition-table.bin \
		$(BUILD)/nvs.bin \
		$(BUILD)/micropython.bin \
		$(BUILD)/fs.bin \
		$(BOARD_TYPE) \
		$(LVGL_FLAG) \
		$(BUILD)/uiflow-$(GIT_VERSION).bin \
		$(BUILD)/uiflow-Sx-$(GIT_VERSION).uf2

$(BUILD)/bootloader/bootloader.bin $(BUILD)/partition_table/partition-table.bin $(BUILD)/micropython.bin: FORCE

build:
	idf.py $(IDFPY_FLAGS) build

clean:
	idf.py $(IDFPY_FLAGS) fullclean
	cd ./../micropython && \
	git apply --reverse ./../m5stack/patches/0001_mpconfigport_lvgl_support.patch && cd -
	cd ./components/lv_bindings && \
	git apply --reverse ./../../patches/0002_avoid_lv_bindings_compile_error.patch && cd -
	cd ./components/M5Unified/M5Unified && \
	git apply --reverse ./../../../patches/2000-M5Unified-support-atoms3u.patch && cd -
	cd ./components/M5Unified/M5Unified && \
	git apply --reverse ./../../../patches/2001-Support-LTR553.patch && cd -

deploy:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) flash

monitor:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) monitor

erase:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) erase_flash

flash: all
	esptool.py --chip $(CHIP) --port $(PORT) --baud $(BAUD) write_flash $(BOOTLOADR_OFFSET) $(BUILD)/uiflow-$(GIT_VERSION).bin

fs: build
	@$(PYTHON) ./../tools/fs_packed.py ./../tools/littlefs/prebuilt/littlefs2 $(BOARD_TYPE) ./fs $(BUILD)/fs.bin $(BUILD)/partition_table/partition-table.bin

nvs:
	@$(PYTHON) ./../tools/nvs_partition_gen.py generate partition_nvs.csv $(BUILD)/nvs.bin 0x6000 # fixed size

littlefs:
	cd ./../tools/littlefs && rm -rf ./build && mkdir build && cd build && cmake .. && make -j && cp ./littlefs2 ./../prebuilt/

mpy-cross:
	make -C ../micropython/mpy-cross

# The two submodules do not belong to the same repository
# micropython submodule belong to uiflow_micropython
# berkeley-db-1.xx submodule belong to micropython submodule
# TODO: need update this :)
submodules:
	git submodule update --init ../tools/littlefs/mbed-littlefs
	git submodule update --init ./components/esp32-camera
	git submodule update --init ./components/M5Unified/M5GFX
	git submodule update --init ./components/M5Unified/M5Unified
	git submodule update --init --recursive ./components/lv_bindings
	git submodule update --init ../micropython
	cd ./../micropython && git submodule update --init $(addprefix ./,$(GIT_SUBMODULES)) && \
	git apply ./../m5stack/patches/0001_mpconfigport_lvgl_support.patch && cd -
	cd ./components/lv_bindings && \
	git apply ./../../patches/0002_avoid_lv_bindings_compile_error.patch && cd -
	cd ./components/M5Unified/M5Unified && \
	git apply ./../../../patches/2000-M5Unified-support-atoms3u.patch && cd -
	cd ./components/M5Unified/M5Unified && \
	git apply ./../../../patches/2001-Support-LTR553.patch && cd -

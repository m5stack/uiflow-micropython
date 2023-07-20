# Makefile for MicroPython on ESP32.
#
# This is a simple, convenience wrapper around idf.py (which uses cmake).

# Select the mcu type to build, default is M5STACK_8MB
# M5STACK_xxx    -> ESP32
# M5STACK_C3_xxx -> ESP32 C3
# M5STACK_S3_xxx -> ESP32 S3

BOARD ?= M5STACK_8MB


# Board type list
BOARD_TYPE_DEF := none atoms3 stamps3 cores3 atoms3u core2

# Select the board type to build, default is None
# This value affects which folder in the "./fs/system/" directory is pack into "fs-system.bin"
# If use default value, it means no directory will pack into "fs-system.bin"
BOARD_TYPE ?= none

ifneq ($(filter $(BOARD_TYPE),$(BOARD_TYPE_DEF)),)
else
    $(error Board type $(BOARD_TYPE) does not exist in list [$(BOARD_TYPE_DEF)])
endif

# esp32c3's bootloader is different with esp32
ifeq (C3, $(findstring C3,${BOARD}))
	CHIP ?= esp32c3
else ifeq (S3, $(findstring S3,${BOARD}))
	CHIP ?= esp32s3
else
	CHIP ?= esp32
endif

# If the build directory is not given, make it reflect the board name.
BUILD ?= build-$(BOARD)

# Device serial settings.
#PORT ?= /dev/ttyS8
PORT ?= /dev/ttyUSB0
BAUD ?= 1500000

PYTHON ?= python3

GIT_SUBMODULES = lib/berkeley-db-1.xx lib/micropython-lib

MAKEFILE_DIR:=$(dir $(abspath $(lastword $(MAKEFILE_LIST))))

USER_C_MODULES = $(MAKEFILE_DIR)cmodules/cmodules.cmake

CMAKE_ARGS =
ifdef USER_C_MODULES
	CMAKE_ARGS += -DUSER_C_MODULES=${USER_C_MODULES}
endif

IDFPY_FLAGS += -DMICROPY_BOARD=$(BOARD) -DBUILD_WITH_LVGL=$(LVGL) -B$(BUILD) $(CMAKE_ARGS)
IDFPY_FLAGS += -DBOARD_TYPE=$(BOARD_TYPE)
ifdef FROZEN_MANIFEST
       IDFPY_FLAGS += -D MICROPY_FROZEN_MANIFEST=$(FROZEN_MANIFEST)
endif

LVGL_FLAG = 0
ifdef LVGL
	LVGL_FLAG = 1
endif

GIT_VERSION := $(shell git describe --abbrev=7 --always)

define pack_fw
	$(1) makeimg.py \
		$(BUILD)/sdkconfig \
		$(BUILD)/bootloader/bootloader.bin \
		$(BUILD)/partition_table/partition-table.bin \
		$(BUILD)/nvs.bin \
		$(BUILD)/micropython.bin \
		$(BUILD)/fs-system.bin \
		$(2) \
		$(BOARD_TYPE) \
		$(LVGL_FLAG) \
		$(BUILD)/uiflow-$(GIT_VERSION).bin \
		$(BUILD)/uiflow-Sx-$(GIT_VERSION).uf2
endef

.PHONY: all build deploy flash flash_all clean erase nvs fs pack pack_all littlefs mpy-cross submodules FORCE

all: nvs fs pack
	@echo ""
	@echo "Done, default packed firmware don't include vfs filesystem, if need vfs filesystem, please use 'make pack_all' command."

$(BUILD)/bootloader/bootloader.bin $(BUILD)/partition_table/partition-table.bin $(BUILD)/micropython.bin: FORCE

# Build the MicroPython firmware.
build: nvs
	idf.py $(IDFPY_FLAGS) build

# Deploy the MicroPython.
deploy: build
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) flash

# Deploy the MicroPython and system filesystem.
flash: pack
	esptool.py --chip $(CHIP) --port $(PORT) --baud $(BAUD) write_flash 0x0 $(BUILD)/uiflow-$(GIT_VERSION).bin

# Deploy the MicroPython, system filesystem and user filesystem.
flash_all: pack_all
	esptool.py --chip $(CHIP) --port $(PORT) --baud $(BAUD) write_flash 0x0 $(BUILD)/uiflow-$(GIT_VERSION).bin

# Clean the build directory.
clean:
	idf.py $(IDFPY_FLAGS) fullclean
	# cd ./../micropython && \
	# git apply --reverse ./../m5stack/patches/0001_mpconfigport_lvgl_support.patch && cd -
	cd ./components/lv_bindings && \
	git apply --reverse ./../../patches/0002_avoid_lv_bindings_compile_error.patch && cd -
	cd ./components/M5Unified/M5Unified && \
	git apply --reverse ./../../../patches/2003-Support-LTR553.patch && cd -

# Erase the flash chip.
erase:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) erase_flash

# Run the serial monitor.
monitor:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) monitor

# Build the NVS partition firmware.
# fixed size 0x6000
nvs:
	@$(PYTHON) ./../tools/nvs_partition_gen.py generate partition_nvs.csv $(BUILD)/nvs.bin 0x6000

# Build the system and user filesystem firmware.
fs: build
	@$(PYTHON) ./../tools/fs_packed.py ./../tools/littlefs/prebuilt/littlefs2 $(BOARD_TYPE) ./fs/system $(BUILD)/fs-system.bin $(BUILD)/partition_table/partition-table.bin
	@$(PYTHON) ./../tools/fs_packed.py ./../tools/littlefs/prebuilt/littlefs2 $(BOARD_TYPE) ./fs/user $(BUILD)/fs-user.bin $(BUILD)/partition_table/partition-table.bin

# Pack the firmware into a single binary without user filesystem.
# Released firmware needn't user filesystem.
pack: fs
	$(call pack_fw,$(PYTHON),none)

# Pack the firmware into a single binary with user filesystem.
pack_all: fs
	$(call pack_fw,$(PYTHON),$(BUILD)/fs-user.bin)

# Build littlefs tool
littlefs:
	cd ./../tools/littlefs && rm -rf ./build && mkdir build && cd build && cmake .. && make -j && cp ./littlefs2 ./../prebuilt/

# Build mpy-cross compiler
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
	# git submodule update --init ../micropython
	cd ./../micropython && git submodule update --init $(addprefix ./,$(GIT_SUBMODULES)) && cd -
	cd ./components/lv_bindings && \
	git apply ./../../patches/0002_avoid_lv_bindings_compile_error.patch && cd -
	cd ./components/M5Unified/M5Unified && \
	git apply ./../../../patches/2003-Support-LTR553.patch && cd -

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Makefile for MicroPython on ESP32.
#
# This is a simple, convenience wrapper around idf.py (which uses cmake).

-include .workenv

BOARD ?= SEEED_STUDIO_XIAO_ESP32S3

boards := \
	SEEED_STUDIO_XIAO_ESP32S3:xiao-s3             \
	SEEED_STUDIO_XIAO_ESP32S3_Sense:xiao-s3-sense \
	ESPRESSIF_ESP32_S3_BOX_3:box3

define find_board
$(if $(filter $(1):%,$(boards)),$(word 2,$(subst :, ,$(filter $(1):%,$(boards)))),none)
endef

# Board type list
BOARD_TYPE_DEF := \
	none          \
	xiao-s3       \
	xiao-s3-sense \
	box3

# Select the board type to build, default is None
# This value affects which folder in the "./fs/system/" directory is pack into "fs-system.bin"
# If use default value, it means no directory will pack into "fs-system.bin"
BOARD_TYPE ?= $(call find_board,$(BOARD))

ifneq ($(filter $(BOARD_TYPE),$(BOARD_TYPE_DEF)),)
else
    $(error Board type $(BOARD_TYPE) does not exist in list [$(BOARD_TYPE_DEF)])
endif

TINY_BOARD_TYPE_DEF = none

ifneq ($(filter $(BOARD),$(TINY_BOARD_TYPE_DEF)),)
TINY_FLAG ?= 1
else
TINY_FLAG ?= 0
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

GIT_VERSION := $(shell git rev-parse --short HEAD)

include ../m5stack/include/files.mk

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

export ADF_PATH=$(abspath ../esp-adf)

.PHONY: all menu build deploy flash flash_all clean erase nvs fs pack pack_all littlefs mpy-cross submodules FORCE

all: nvs fs pack
	@echo ""
	@echo "Done, default packed firmware don't include vfs filesystem, if need vfs filesystem, please use 'make pack_all' command."

$(BUILD)/bootloader/bootloader.bin $(BUILD)/partition_table/partition-table.bin $(BUILD)/micropython.bin: FORCE

# Config menu
menu:
	idf.py $(IDFPY_FLAGS) menuconfig

# Show the size summary
size: 
	idf.py $(IDFPY_FLAGS) size

# Build the MicroPython firmware
build: nvs
	idf.py $(IDFPY_FLAGS) build

# Deploy the MicroPython firmware
deploy: build
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) flash

# Deploy the MicroPython and system filesystem
flash: pack
	esptool.py --chip $(CHIP) --port $(PORT) --baud $(BAUD) write_flash 0x0 $(BUILD)/uiflow-$(GIT_VERSION).bin

# Deploy the MicroPython, system filesystem and user filesystem
flash_all: pack_all
	esptool.py --chip $(CHIP) --port $(PORT) --baud $(BAUD) write_flash 0x0 $(BUILD)/uiflow-$(GIT_VERSION).bin

# Clean the build directory
clean:
	idf.py $(IDFPY_FLAGS) fullclean

# Erase the flash chip
erase:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) erase_flash

# Run the serial monitor
monitor:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) monitor

# Build the NVS partition firmware
# fixed size 0x6000
nvs:
	@$(PYTHON) ./../tools/nvs_partition_gen.py generate partition_nvs.csv $(BUILD)/nvs.bin 0x6000

# Build the system and user filesystem firmware
ifeq ($(TINY_FLAG),1)
fs: build
	@if [ ! -d $(BUILD)/base-files ]; then \
		mkdir -p $(BUILD)/base-files; \
	fi
	$(call base-files/install,$(BOARD_TYPE),$(BUILD)/base-files)
	@$(PYTHON) \
			./../tools/fs_packed.py \
			./../tools/littlefs/prebuilt/littlefs2 \
			$(BOARD_TYPE) \
			$(BUILD)/base-files \
			$(BUILD)/fs-user.bin \
			$(BUILD)/partition_table/partition-table.bin
else
fs: build
	@$(PYTHON)                                     \
			./../tools/fs_packed.py                \
			./../tools/littlefs/prebuilt/littlefs2 \
			$(BOARD_TYPE)                          \
			./fs/system                            \
			$(BUILD)/fs-system.bin                 \
			$(BUILD)/partition_table/partition-table.bin
	@$(PYTHON)                                     \
			./../tools/fs_packed.py                \
			./../tools/littlefs/prebuilt/littlefs2 \
			$(BOARD_TYPE)                          \
			./fs/user                              \
			$(BUILD)/fs-user.bin                   \
			$(BUILD)/partition_table/partition-table.bin
endif

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

# Running the build with ECHO_SUBMODULES set will trigger py/mkrules.cmake to
# print out the value of the GIT_SUBMODULES variable, prefixed with
# "GIT_SUBMODULES", and then abort. This extracts out that line from the idf.py
# output and passes the list of submodules to py/mkrules.mk which does the
# `git submodule init` on each.
submodules:
	git submodule update --init ../tools/littlefs/mbed-littlefs
	git submodule update --init ./components/esp32-camera
	git submodule update --init ./components/M5Unified/M5GFX
	git submodule update --init ./components/M5Unified/M5Unified
	git submodule update --init --recursive ./components/lv_bindings
	git submodule update --init ../micropython
	git submodule update --init ../esp-adf
	cd ../esp-adf && \
		git submodule update --init components/esp-adf-libs && \
		git submodule update --init components/esp-sr && \
		cd -
	cd ../micropython && \
		git submodule update --init lib/berkeley-db-1.xx && \
		git submodule update --init lib/tinyusb && \
		git submodule update --init lib/micropython-lib && \
		cd -

LV_BINDING_PATH = $(abspath ./cmodules/lv_binding_micropython)
MICROPYTHON_PATH = $(abspath ./../micropython)
M5UNIFIED_PATH = $(abspath ./components/M5Unified/M5Unified)
M5GFX_PATH = $(abspath ./components/M5Unified/M5GFX)
ESP32_CAMERA_PATH = $(abspath ./components/esp32-camera)

LV_BINDING_PATCH_SERIES = \
	6000-avoid-lv_bindings-compile-error.patch \
	6001-avoid-lvgl-font-redefine.patch

MICROPYTHON_PATCH_SERIES = \
	0022-micropython-1.27.0-modtime.patch \
	0023-micropython-1.27.0-add-set-default-netif-method.patch \
	0024-micropython-1.27.0-i2c-probe.patch \
	0025-micropython-1.27.0-add-uart-mode.patch \
	0026-micropython-1.27.0-add-getsockname.patch \
	0027-micropython-1.27.0-fix-mpnimbleport.patch

IDF_PATH_PATCH_SERIES = \
	1005-idf_v5.5_freertos.patch

M5UNIFIED_PATCH_SERIES = \
	2006-Support-LTR553.patch \
	2007-Support-UnitC6L.patch \
	2009-fix-SoftI2C.patch \
	2010-Support-Nesso-N1.patch \
	2011-Fix-PowerHub-Charge-Status-Detection.patch \
	2018-fix-Rtc-setAlarmIRQ.patch \
	2028-Pin-M5GFX-git-dependency.patch

ADF_PATCH_SERIES = \
	3003-modify-i2s_stream_idf5.5.patch

M5GFX_PATCH_SERIES = \
	4004-I2C-repeated-initialization.patch

ESP32_CAMERA_PATCH_SERIES = \
	5002-Add-software-i2c-support.patch

# Apply patches
patch: unpatch
	$(call Patch/prepare,$(LV_BINDING_PATH),$(LV_BINDING_PATCH_SERIES))
	$(call Patch/prepare,$(MICROPYTHON_PATH),$(MICROPYTHON_PATCH_SERIES))
	$(call Patch/prepare,$(IDF_PATH),$(IDF_PATH_PATCH_SERIES))
	$(call Patch/prepare,$(M5UNIFIED_PATH),$(M5UNIFIED_PATCH_SERIES))
	$(call Patch/prepare,$(ADF_PATH),$(ADF_PATCH_SERIES))
	$(call Patch/prepare,$(M5GFX_PATH),$(M5GFX_PATCH_SERIES))
	$(call Patch/prepare,$(ESP32_CAMERA_PATH),$(ESP32_CAMERA_PATCH_SERIES))

# Unapply patches
unpatch:
	$(call Patch/clean,$(LV_BINDING_PATH),$(LV_BINDING_PATCH_SERIES))
	$(call Patch/clean,$(MICROPYTHON_PATH),$(MICROPYTHON_PATCH_SERIES))
	$(call Patch/clean,$(IDF_PATH),$(IDF_PATH_PATCH_SERIES))
	$(call Patch/clean,$(M5UNIFIED_PATH),$(M5UNIFIED_PATCH_SERIES))
	$(call Patch/clean,$(ADF_PATH),$(ADF_PATCH_SERIES))
	$(call Patch/clean,$(M5GFX_PATH),$(M5GFX_PATCH_SERIES))
	$(call Patch/clean,$(ESP32_CAMERA_PATH),$(ESP32_CAMERA_PATCH_SERIES))

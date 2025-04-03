# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Makefile for MicroPython on ESP32.
#
# This is a simple, convenience wrapper around idf.py (which uses cmake).

-include .workenv

BOARD ?= M5STACK_AtomS3

boards := \
	M5STACK_AtomS3:atoms3            \
	M5STACK_AtomS3_Lite:atoms3-lite  \
	M5STACK_StampS3:stamps3          \
	M5STACK_CoreS3:cores3            \
	M5STACK_AtomS3U:atoms3u          \
	M5STACK_Core2:core2              \
	M5STACK_Tough:tough              \
	M5STACK_StickC_PLUS2:stickcplus2 \
	M5STACK_StickC_PLUS:stickcplus   \
	M5STACK_Fire:fire                \
	M5STACK_NanoC6:nanoc6            \
	M5STACK_Basic:basic              \
	M5STACK_Basic_4MB:basic          \
	M5STACK_Capsule:capsule          \
	M5STACK_CoreInk:coreink          \
	M5STACK_AirQ:airq                \
	M5STACK_Dial:dial                \
	M5STACK_Cardputer:cardputer      \
	M5STACK_Paper:paper              \
	M5STACK_PaperS3:papers3          \
	M5STACK_DinMeter:dinmeter        \
	M5STACK_StickC:stickc            \
	M5STACK_Station:station          \
	M5STACK_Atom_Lite:atom-lite      \
	M5STACK_Stamp_PICO:stamppico     \
	M5STACK_Atom_Matrix:atommatrix   \
	M5STACK_AtomU:atomu              \
	M5STACK_Atom_Echo:atomecho       \
	M5STACK_AtomS3R:atoms3r          \
	M5STACK_StamPLC:stamplc

define find_board
$(if $(filter $(1):%,$(boards)),$(word 2,$(subst :, ,$(filter $(1):%,$(boards)))),none)
endef

# Board type list
BOARD_TYPE_DEF := \
	none        \
	atoms3      \
	atoms3-lite \
	stamps3     \
	cores3      \
	atoms3u     \
	core2       \
	tough       \
	stickcplus2 \
	stickcplus  \
	fire        \
	nanoc6      \
	basic       \
	capsule     \
	coreink     \
	airq        \
	dial        \
	cardputer   \
	paper       \
	papers3     \
	dinmeter    \
	stickc      \
	station     \
	atom-lite   \
	stamppico   \
	atommatrix  \
	atomu       \
	atomecho    \
	atoms3r     \
	stamplc

# Select the board type to build, default is None
# This value affects which folder in the "./fs/system/" directory is pack into "fs-system.bin"
# If use default value, it means no directory will pack into "fs-system.bin"
BOARD_TYPE ?= $(call find_board,$(BOARD))

ifneq ($(filter $(BOARD_TYPE),$(BOARD_TYPE_DEF)),)
else
    $(error Board type $(BOARD_TYPE) does not exist in list [$(BOARD_TYPE_DEF)])
endif

TINY_BOARD_TYPE_DEF = \
	M5STACK_StickC_PLUS \
	M5STACK_Basic_4MB   \
	M5STACK_CoreInk     \
	M5STACK_StickC      \
	M5STACK_Atom_Lite   \
	M5STACK_Stamp_PICO  \
	M5STACK_Atom_Matrix \
	M5STACK_AtomU       \
	M5STACK_Atom_Echo   \
	M5STACK_NanoC6

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

include ./include/files.mk

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
	git submodule update --init ./components/esp_dl
	git submodule update --init ./components/esp-code-scanner
	git submodule update --init ./components/esp_zigbee_host
	git submodule update --init ./components/epdiy
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

# Apply patches
patch:
	$(call Package/patche,$(abspath ./components/lv_bindings),$(abspath ./patches/0002_avoid_lv_bindings_compile_error.patch))
	$(call Package/patche,$(abspath ./../micropython),$(abspath ./patches/0004-micropython-1.24-machine-adc-v5.x.diff))
	$(call Package/patche,$(abspath ./../micropython),$(abspath ./patches/0005-micropython-fix-SDCard-16223.patch))
	$(call Package/patche,$(abspath ./../micropython),$(abspath ./patches/0006-modtime-add-timezone-method.patch))
	$(call Package/patche,$(abspath ./../micropython),$(abspath ./patches/0007-Add-set-default-netif-method.patch))
	$(call Package/patche,$(abspath ./../micropython),$(abspath ./patches/0008-machine_uart-add-uart-mode.patch))
	$(call Package/patche,$(abspath $(IDF_PATH)),$(abspath ./patches/1003-WIP-Compatible-with-esp-adf-v2.7.diff))
	$(call Package/patche,$(abspath ./components/M5Unified/M5Unified),$(abspath ./patches/2005-Support-LTR553.patch))
	$(call Package/patche,$(abspath $(ADF_PATH)),$(abspath ./patches/3002-Modify-i2s_stream_idf5.patch))
	$(call Package/patche,$(abspath ./components/epdiy),$(abspath ./patches/4001-Avoid-epdiy-compilation-failure-on-esp32-c6.patch))

# Unapply patches
unpatch:
	$(call Package/unpatche,$(abspath ./components/lv_bindings),$(abspath ./patches/0002_avoid_lv_bindings_compile_error.patch))
	$(call Package/unpatche,$(abspath ./../micropython),$(abspath ./patches/0008-machine_uart-add-uart-mode.patch))
	$(call Package/unpatche,$(abspath ./../micropython),$(abspath ./patches/0007-Add-set-default-netif-method.patch))
	$(call Package/unpatche,$(abspath ./../micropython),$(abspath ./patches/0006-modtime-add-timezone-method.patch))
	$(call Package/unpatche,$(abspath ./../micropython),$(abspath ./patches/0005-micropython-fix-SDCard-16223.patch))
	$(call Package/unpatche,$(abspath ./../micropython),$(abspath ./patches/0004-micropython-1.24-machine-adc-v5.x.diff))
	$(call Package/unpatche,$(abspath $(IDF_PATH)),$(abspath ./patches/1003-WIP-Compatible-with-esp-adf-v2.7.diff))
	$(call Package/unpatche,$(abspath ./components/M5Unified/M5Unified),$(abspath ./patches/2005-Support-LTR553.patch))
	$(call Package/unpatche,$(abspath $(ADF_PATH)),$(abspath ./patches/3002-Modify-i2s_stream_idf5.patch))
	$(call Package/unpatche,$(abspath ./components/epdiy),$(abspath ./patches/4001-Avoid-epdiy-compilation-failure-on-esp32-c6.patch))

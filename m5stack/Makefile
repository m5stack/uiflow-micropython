# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Makefile for MicroPython on ESP32.
#
# This is a simple, convenience wrapper around idf.py (which uses cmake).

-include .workenv

BOARD ?= M5STACK_AtomS3

boards := \
	Nesso_N1:nesso-n1                \
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
	M5STACK_AtomS3R_CAM:atoms3r_cam  \
	M5STACK_Atom_EchoS3R:atom_echos3r\
	M5STACK_StamPLC:stamplc          \
	M5STACK_Tab5:tab5                \
	M5STACK_CardputerADV:cardputeradv\
	M5STACK_Unit_C6L:unit_c6l        \
	M5STACK_PowerHub:powerhub        \
	M5STACK_DualKey:dualkey          \
	M5STACK_StickS3:sticks3          \
	M5STACK_Unit_PoEP4:unit_poep4

define find_board
$(if $(filter $(1):%,$(boards)),$(word 2,$(subst :, ,$(filter $(1):%,$(boards)))),none)
endef

# Board type list
BOARD_TYPE_DEF := \
	none        \
	nesso-n1    \
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
	atoms3r_cam \
	atom_echos3r\
	stamplc     \
	tab5        \
	cardputeradv\
	unit_c6l    \
	powerhub    \
	dualkey     \
	sticks3     \
	unit_poep4

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

CHIP ?= auto

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
	rm -rf ../tools/littlefs/mbed-littlefs && git submodule update --init ../tools/littlefs/mbed-littlefs
	rm -rf ./components/esp32-camera && git submodule update --init ./components/esp32-camera
	rm -rf ./components/esp_dl && git submodule update --init ./components/esp_dl
	rm -rf ./components/esp-code-scanner && git submodule update --init ./components/esp-code-scanner
	rm -rf ./components/esp_zigbee_host && git submodule update --init ./components/esp_zigbee_host
	rm -rf ./components/M5Unified/M5GFX && git submodule update --init ./components/M5Unified/M5GFX
	rm -rf ./components/M5Unified/M5Unified && git submodule update --init ./components/M5Unified/M5Unified
	#git submodule update --init --recursive ./components/lv_bindings
	rm -rf ./cmodules/lv_binding_micropython && git submodule update --init --recursive ./cmodules/lv_binding_micropython
	rm -rf ../micropython && git submodule update --init ../micropython
	rm -rf ../esp-adf && git submodule update --init ../esp-adf
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
	0006-modtime-add-timezone-method.patch              \
	0007-Add-set-default-netif-method.patch             \
	0009-micropython-1.25.0-add-esp32p4-pins.patch      \
	0010-micropython-1.25.0-machine-adc-v5.x.patch      \
	0011-micropython-1.25.0-fix-esp32-p4-pwm.patch      \
	0012-micropython-1.25.0-fix-esp32-p4-modesp32.patch \
	0013-micropython-1.25.0-fix-touchpad.patch          \
	0014-micropython-1.25.0-fix-timer.patch             \
	0015-micropython-1.25.0-fix-hostname.patch          \
	0016-micropython-1.25.0-fix-mpnimbleport.patch      \
	0017-micropython-1.25.0-add-uart-mode.patch         \
	0018-micropython-1.25.0-support-esp-idf-v5.4.2.patch \
	0019-micropython-1.25.0-add-getsockname.patch \
	0020-micropython-1.25.0-modtime.patch

IDF_PATH_PATCH_SERIES = \
	1004-idf_v5.4_freertos.patch

M5UNIFIED_PATCH_SERIES = \
	2006-Support-LTR553.patch \
	2007-Support-UnitC6L.patch \
	2008-Only-use-old-rmt-driver.patch \
	2009-fix-SoftI2C.patch \
	2010-Support-Nesso-N1.patch \
	2011-Fix-PowerHub-Charge-Status-Detection.patch

ADF_PATCH_SERIES = \
	3002-Modify-i2s_stream_idf5.patch

M5GFX_PATCH_SERIES = \
	4004-I2C-repeated-initialization.patch

ESP32_CAMERA_PATCH_SERIES = \
	5002-Add-software-i2c-support.patch

PACKAGES = \
	lv_binding_micropython \
	micropython            \
	esp-idf                \
	M5Unified              \
	esp-adf                \
	M5GFX                  \
	esp32-camera

PACKAGES_PATH = \
	lv_binding_micropython:$(LV_BINDING_PATH) \
	micropython:$(MICROPYTHON_PATH)           \
	esp-idf:$(IDF_PATH)                       \
	M5Unified:$(M5UNIFIED_PATH)               \
	esp-adf:$(ADF_PATH)                       \
	M5GFX:$(M5GFX_PATH)                       \
	esp32-camera:$(ESP32_CAMERA_PATH)

define find_package
$(if $(filter $(1):%,$(PACKAGES_PATH)),$(word 2,$(subst :, ,$(filter $(1):%,$(PACKAGES_PATH)))),none)
endef

.PHONY: $(PACKAGES) prepare
PKG := $(firstword $(MAKECMDGOALS))

PKG_PATH ?= $(call find_package,$(PKG))
PKG_PATCH_SERIES := $(strip \
	$(if $(filter lv_binding_micropython,$(PKG)),$(LV_BINDING_PATCH_SERIES)) \
	$(if $(filter micropython,$(PKG)),$(MICROPYTHON_PATCH_SERIES))           \
	$(if $(filter esp-idf,$(PKG)),$(IDF_PATH_PATCH_SERIES))                  \
	$(if $(filter M5Unified,$(PKG)),$(M5UNIFIED_PATCH_SERIES))               \
	$(if $(filter esp-adf,$(PKG)),$(ADF_PATCH_SERIES))                       \
	$(if $(filter esp32-camera,$(PKG)),$(ESP32_CAMERA_PATCH_SERIES))         \
	$(if $(filter M5GFX,$(PKG)),$(M5GFX_PATCH_SERIES))                       \
)
# $(info PKG_PATCH_SERIES for $(PKG) is [$(PKG_PATCH_SERIES)])

prepare:
	$(call Patch/prepare,$(abspath $(PKG_PATH)),$(PKG_PATCH_SERIES))

.PHONY: $(PACKAGES) update
update:
	$(call Patch/update,$(abspath $(PKG_PATH)),$(abspath ./patches))

.PHONY: $(PACKAGES) unprepare
unprepare:
	$(call Patch/clean,$(abspath $(PKG_PATH)),$(PKG_PATCH_SERIES))

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

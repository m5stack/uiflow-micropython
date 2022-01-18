# Makefile for MicroPython on ESP32.
#
# This is a simple, convenience wrapper around idf.py (which uses cmake).

# Select the board to build for, defaulting to GENERIC.
BOARD ?= m5stack
CHIP ?= esp32

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

USER_C_MODULES = $(MAKEFILE_DIR)/cmodules/cmodules.cmake

CMAKE_ARGS =

ifdef USER_C_MODULES
	CMAKE_ARGS += -DUSER_C_MODULES=${USER_C_MODULES}
endif

IDFPY_FLAGS += -D MICROPY_BOARD=$(BOARD) -B $(BUILD) $(CMAKE_ARGS)

ifdef FROZEN_MANIFEST
       IDFPY_FLAGS += -D MICROPY_FROZEN_MANIFEST=$(FROZEN_MANIFEST)
endif

GIT_VERSION := $(shell git describe --abbrev=7 --dirty --always --tags)

all: fs nvs
	idf.py $(IDFPY_FLAGS) build
	@$(PYTHON) makeimg.py \
		$(BUILD)/sdkconfig \
		$(BUILD)/bootloader/bootloader.bin \
		$(BUILD)/partition_table/partition-table.bin \
		$(BUILD)/nvs.bin \
		$(BUILD)/micropython.bin \
		$(BUILD)/fs.bin \
		$(BUILD)/uiflow-$(GIT_VERSION).bin

$(BUILD)/bootloader/bootloader.bin $(BUILD)/partition_table/partition-table.bin $(BUILD)/micropython.bin: FORCE

clean:
	idf.py $(IDFPY_FLAGS) fullclean

deploy:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) flash

monitor:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) monitor

erase:
	idf.py $(IDFPY_FLAGS) -p $(PORT) -b $(BAUD) erase_flash

flash: all
	esptool.py --chip $(CHIP) --port $(PORT) --baud $(BAUD) \
	write_flash 0x1000 $(BUILD)/uiflow-$(GIT_VERSION).bin

fs:
	./../tools/littlefs/prebuilt/linux/littlefs2 -c -v -i ./fs \
	-o $(BUILD)/fs.bin -s 0x14e000 # defined in partitions.csv

nvs:
	python ./../tools/nvs_partition_gen.py generate partition_nvs.csv \
	$(BUILD)/nvs.bin 0x6000 # defined in partitions.csv

mpy-cross:
	make -C ../micropython/mpy-cross

# The two submodules do not belong to the same repository
# micropython submodule belong to uiflow_micropython
# berkeley-db-1.xx submodule belong to micropython submodule
submodules:
	git submodule update --init ../micropython
	cd ./../micropython && git submodule update --init $(addprefix ./,$(GIT_SUBMODULES)) && cd -	

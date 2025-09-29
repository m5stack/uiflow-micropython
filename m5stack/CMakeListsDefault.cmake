# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Set location of base MicroPython directory.
if(NOT MICROPY_DIR)
    get_filename_component(MICROPY_DIR ${PROJECT_DIR}/../micropython/ ABSOLUTE)
endif()

# Set location of the ESP32 port directory.
if(NOT MICROPY_PORT_DIR)
    get_filename_component(MICROPY_PORT_DIR ${MICROPY_DIR}/ports/esp32 ABSOLUTE)
endif()

# RISC-V specific inclusions
if(CONFIG_IDF_TARGET_ARCH_RISCV)
    list(APPEND MICROPY_SOURCE_LIB
        ${MICROPY_DIR}/shared/runtime/gchelper_native.c
        ${MICROPY_DIR}/shared/runtime/gchelper_rv32i.s
    )
endif()

if(NOT DEFINED MICROPY_PY_TINYUSB)
    if(CONFIG_IDF_TARGET_ESP32S2 OR CONFIG_IDF_TARGET_ESP32S3)
        set(MICROPY_PY_TINYUSB ON)
    endif()
endif()

# Include core source components.
include(${MICROPY_DIR}/py/py.cmake)

# CMAKE_BUILD_EARLY_EXPANSION is set during the component-discovery phase of
# `idf.py build`, so none of the extmod/usermod (and in reality, most of the
# micropython) rules need to happen. Specifically, you cannot invoke add_library.
if(NOT CMAKE_BUILD_EARLY_EXPANSION)
    # Enable extmod components that will be configured by extmod.cmake.
    # A board may also have enabled additional components.
    set(MICROPY_PY_BTREE ON)

    include(${MICROPY_DIR}/py/usermod.cmake)
    include(${MICROPY_DIR}/extmod/extmod.cmake)
endif()

list(APPEND MICROPY_QSTRDEFS_PORT
    ${PROJECT_DIR}/../micropython/ports/esp32/qstrdefsport.h
)

list(APPEND MICROPY_SOURCE_SHARED
    ${MICROPY_DIR}/shared/readline/readline.c
    ${MICROPY_DIR}/shared/netutils/netutils.c
    ${MICROPY_DIR}/shared/timeutils/timeutils.c
    ${MICROPY_DIR}/shared/runtime/interrupt_char.c
    ${MICROPY_DIR}/shared/runtime/mpirq.c
    ${MICROPY_DIR}/shared/runtime/stdout_helpers.c
    ${MICROPY_DIR}/shared/runtime/sys_stdio_mphal.c
    ${MICROPY_DIR}/shared/runtime/pyexec.c
)

list(APPEND MICROPY_SOURCE_LIB
    ${MICROPY_DIR}/lib/littlefs/lfs1.c
    ${MICROPY_DIR}/lib/littlefs/lfs1_util.c
    ${MICROPY_DIR}/lib/littlefs/lfs2.c
    ${MICROPY_DIR}/lib/littlefs/lfs2_util.c
    ${MICROPY_DIR}/lib/mbedtls_errors/esp32_mbedtls_errors.c
    ${MICROPY_DIR}/lib/oofatfs/ff.c
    ${MICROPY_DIR}/lib/oofatfs/ffunicode.c
)

list(APPEND MICROPY_SOURCE_DRIVERS
    ${MICROPY_DIR}/drivers/bus/softspi.c
    ${MICROPY_DIR}/drivers/dht/dht.c
)

list(APPEND GIT_SUBMODULES lib/tinyusb)
if(MICROPY_PY_TINYUSB)
    set(TINYUSB_SRC "${MICROPY_DIR}/lib/tinyusb/src")
    string(TOUPPER OPT_MCU_${IDF_TARGET} tusb_mcu)

    list(APPEND MICROPY_DEF_TINYUSB
        CFG_TUSB_MCU=${tusb_mcu}
    )

    list(APPEND MICROPY_SOURCE_TINYUSB
        ${TINYUSB_SRC}/tusb.c
        ${TINYUSB_SRC}/common/tusb_fifo.c
        ${TINYUSB_SRC}/device/usbd.c
        ${TINYUSB_SRC}/device/usbd_control.c
        ${TINYUSB_SRC}/class/cdc/cdc_device.c
        ${TINYUSB_SRC}/portable/synopsys/dwc2/dcd_dwc2.c
        ${MICROPY_DIR}/shared/tinyusb/mp_usbd.c
        ${MICROPY_DIR}/shared/tinyusb/mp_usbd_cdc.c
        ${MICROPY_DIR}/shared/tinyusb/mp_usbd_descriptor.c
        ${MICROPY_DIR}/shared/tinyusb/mp_usbd_runtime.c
    )

    list(APPEND MICROPY_INC_TINYUSB
        ${TINYUSB_SRC}
        ${MICROPY_DIR}/shared/tinyusb/
    )

    list(APPEND MICROPY_LINK_TINYUSB
        -Wl,--wrap=dcd_event_handler
    )
endif()

list(APPEND MICROPY_SOURCE_PORT
    ${PROJECT_DIR}/board.cpp
    ${PROJECT_DIR}/../micropython/ports/esp32/panichandler.c
    ${PROJECT_DIR}/../micropython/ports/esp32/adc.c
    ${PROJECT_DIR}/main.c
    ${PROJECT_DIR}/../micropython/ports/esp32/ppp_set_auth.c
    ${PROJECT_DIR}/../micropython/ports/esp32/uart.c
    ${PROJECT_DIR}/../micropython/ports/esp32/usb.c
    ${PROJECT_DIR}/../micropython/ports/esp32/usb_serial_jtag.c
    ${PROJECT_DIR}/../micropython/ports/esp32/gccollect.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mphalport.c
    ${PROJECT_DIR}/../micropython/ports/esp32/fatfs_port.c
    ${PROJECT_DIR}/../micropython/ports/esp32/help.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_bitstream.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_timer.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_pin.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_touchpad.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_dac.c
    ${PROJECT_DIR}/machine_i2c.c
    ${PROJECT_DIR}/../micropython/ports/esp32/network_common.c
    ${PROJECT_DIR}/network_lan.c
    ${PROJECT_DIR}/network_ppp.c
    ${PROJECT_DIR}/network_wlan.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mpnimbleport.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modsocket.c
    ${PROJECT_DIR}/../micropython/ports/esp32/lwip_patch.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modesp.c
    ${PROJECT_DIR}/esp32_nvs.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_partition.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_rmt.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_ulp.c
    ${PROJECT_DIR}/modesp32.c
    # ${PROJECT_DIR}/../micropython/ports/esp32/machine_hw_spi.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mpthreadport.c
    ${PROJECT_DIR}/machine_rtc.c
    # ${PROJECT_DIR}/../micropython/ports/esp32/machine_sdcard.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modespnow.c
    ${PROJECT_DIR}/_vfs_stream.c
)

if (
    BOARD_TYPE STREQUAL "cores3" 
    OR BOARD_TYPE STREQUAL "core2" 
    OR BOARD_TYPE STREQUAL "paper" 
    OR BOARD_TYPE STREQUAL "papers3" 
    OR BOARD_TYPE STREQUAL "basic"
    OR BOARD_TYPE STREQUAL "fire"
    OR BOARD_TYPE STREQUAL "capsule"
    OR BOARD_TYPE STREQUAL "tough"
    OR BOARD_TYPE STREQUAL "stamplc"
    OR BOARD_TYPE STREQUAL "unit_c6l"
)
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/machine_hw_spi.c)
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/machine_sdcard.c)
else()
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/../micropython/ports/esp32/machine_hw_spi.c)
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/../micropython/ports/esp32/machine_sdcard.c)
endif()

# list(TRANSFORM MICROPY_SOURCE_PORT PREPEND ${MICROPY_PORT_DIR}/)
list(APPEND MICROPY_SOURCE_PORT ${CMAKE_BINARY_DIR}/pins.c)

set(MICROPY_SOURCE_M5UNIFIED
    ${PROJECT_DIR}/components/M5Unified/mpy_m5btn.cpp
    ${PROJECT_DIR}/components/M5Unified/mpy_m5gfx.cpp
    ${PROJECT_DIR}/components/M5Unified/mpy_m5power.cpp
    ${PROJECT_DIR}/components/M5Unified/mpy_m5spk.cpp
    ${PROJECT_DIR}/components/M5Unified/mpy_m5touch.cpp
    ${PROJECT_DIR}/components/M5Unified/mpy_m5unified.cpp
    ${PROJECT_DIR}/components/M5Unified/mpy_m5widgets.cpp
)

if (M5_CAMERA_MODULE_ENABLE)
    set(MICROPY_SOURCE_M5CAMERA
        ${PROJECT_DIR}/cmodules/m5camera/m5camera.c
    )
endif()

set(MICROPY_SOURCE_QSTR
    ${MICROPY_SOURCE_PY}
    ${MICROPY_SOURCE_EXTMOD}
    ${MICROPY_SOURCE_USERMOD}
    ${MICROPY_SOURCE_SHARED}
    ${MICROPY_SOURCE_LIB}
    ${MICROPY_SOURCE_PORT}
    ${MICROPY_SOURCE_BOARD}
    ${MICROPY_SOURCE_TINYUSB}
    ${MICROPY_SOURCE_M5UNIFIED}
    ${MICROPY_SOURCE_M5CAMERA}
)

list(APPEND IDF_COMPONENTS
    app_update
    bootloader_support
    bt
    driver
    esp_adc
    esp_app_format
    esp_common
    esp_eth
    esp_event
    esp_hw_support
    esp_netif
    esp_partition
    esp_pm
    esp_psram
    esp_ringbuf
    esp_rom
    esp_system
    esp_timer
    esp_wifi
    freertos
    hal
    heap
    log
    lwip
    mbedtls
    newlib
    nvs_flash
    sdmmc
    soc
    spi_flash
    ulp
    usb
    vfs
    esp_http_client
    esp-tls
    libffi
    json
    M5Unified
    esp32-camera
    uiflow_utility
    esp_dmx
    esp_mm
    esp_driver_ppa
)

if(CONFIG_IDF_TARGET_ESP32 OR CONFIG_IDF_TARGET_ESP32S2 OR CONFIG_IDF_TARGET_ESP32S3)
    list(APPEND IDF_COMPONENTS xtensa)
endif()

if (M5_CAMERA_MODULE_ENABLE AND BOARD_TYPE STREQUAL "cores3")
list(APPEND IDF_COMPONENTS
    esp-dl
    human_face_detect
    pedestrian_detect
    human_face_recognition
    esp-code-scanner
    quirc
)
endif()

if (M5_CAMERA_MODULE_ENABLE AND BOARD_TYPE STREQUAL "atoms3r_cam")
list(APPEND IDF_COMPONENTS
    esp-code-scanner
    quirc
)
endif()

if(IDF_TARGET STREQUAL "esp32" OR IDF_TARGET STREQUAL "esp32s3" OR IDF_TARGET STREQUAL "esp32p4")
    list(APPEND IDF_COMPONENTS boards)
    list(APPEND IDF_COMPONENTS audio_pipeline)
    list(APPEND IDF_COMPONENTS audio_sal)
    list(APPEND IDF_COMPONENTS esp-adf-libs)
    list(APPEND IDF_COMPONENTS esp-sr)
    list(APPEND IDF_COMPONENTS esp_codec_dev)
endif()

# Provide the default LD fragment if not set
if (MICROPY_USER_LDFRAGMENTS)
    set(MICROPY_LDFRAGMENTS ${MICROPY_USER_LDFRAGMENTS})
endif()

if (UPDATE_SUBMODULES)
    # ESP-IDF checks if some paths exist before CMake does. Some paths don't
    # yet exist if this is an UPDATE_SUBMODULES pass on a brand new checkout, so remove
    # any path which might not exist yet. A "real" build will not set UPDATE_SUBMODULES.
    unset(MICROPY_SOURCE_TINYUSB)
    unset(MICROPY_SOURCE_EXTMOD)
    unset(MICROPY_SOURCE_LIB)
    unset(MICROPY_INC_TINYUSB)
    unset(MICROPY_INC_CORE)
endif()

# Register the main IDF component.
idf_component_register(
    SRCS
        ${MICROPY_SOURCE_PY}
        ${MICROPY_SOURCE_EXTMOD}
        ${MICROPY_SOURCE_SHARED}
        ${MICROPY_SOURCE_LIB}
        ${MICROPY_SOURCE_DRIVERS}
        ${MICROPY_SOURCE_PORT}
        ${MICROPY_SOURCE_BOARD}
        ${MICROPY_SOURCE_TINYUSB}
    INCLUDE_DIRS
        ${MICROPY_INC_CORE}
        ${MICROPY_INC_USERMOD}
        ${MICROPY_INC_TINYUSB}
        ${MICROPY_PORT_DIR}
        ${MICROPY_BOARD_DIR}
        ${CMAKE_BINARY_DIR}
        ${CMAKE_CURRENT_LIST_DIR}
    LDFRAGMENTS
        ${MICROPY_LDFRAGMENTS}
    REQUIRES
        ${IDF_COMPONENTS}
)

# Set the MicroPython target as the current (main) IDF component target.
set(MICROPY_TARGET ${COMPONENT_TARGET})

# Define mpy-cross flags, for use with frozen code.
if(CONFIG_IDF_TARGET_ARCH_XTENSA)
    set(MICROPY_CROSS_FLAGS -march=xtensawin)
elseif(CONFIG_IDF_TARGET_ARCH_RISCV)
    set(MICROPY_CROSS_FLAGS -march=rv32imc)
endif()

if (M5_CAMERA_MODULE_ENABLE AND BOARD_TYPE STREQUAL "cores3")
target_compile_definitions(${MICROPY_TARGET} PUBLIC
    USE_OMV=1
)
endif()

# Set compile options for this port.
target_compile_definitions(${MICROPY_TARGET} PUBLIC
    ${MICROPY_DEF_CORE}
    ${MICROPY_DEF_BOARD}
    ${MICROPY_DEF_TINYUSB}
    MICROPY_ESP_IDF_4=1
    MICROPY_VFS_FAT=1
    MICROPY_VFS_LFS2=1
    ESP_PLATFORM=1  # M5GFX platform determine
    FFCONF_H=\"${MICROPY_OOFATFS_DIR}/ffconf.h\"
    LFS1_NO_MALLOC LFS1_NO_DEBUG LFS1_NO_WARN LFS1_NO_ERROR LFS1_NO_ASSERT
    LFS2_NO_MALLOC LFS2_NO_DEBUG LFS2_NO_WARN LFS2_NO_ERROR LFS2_NO_ASSERT
    BOARD_ID=${BOARD_ID}
    MICROPY_PY_LVGL=${MICROPY_PY_LVGL}
)

# Disable some warnings to keep the build output clean.
target_compile_options(${MICROPY_TARGET} PUBLIC
    -Wno-clobbered
    -Wno-deprecated-declarations
    -Wno-missing-field-initializers
)

target_link_options(${MICROPY_TARGET} PUBLIC
    ${MICROPY_LINK_TINYUSB}
)

# Additional include directories needed for private NimBLE headers.
target_include_directories(${MICROPY_TARGET} PUBLIC
    ${IDF_PATH}/components/bt/host/nimble/nimble
)

# Add additional extmod and usermod components.
target_link_libraries(${MICROPY_TARGET} micropy_extmod_btree)
target_link_libraries(${MICROPY_TARGET} usermod)

# Extra linker options
# (when wrap symbols are in standalone files, --undefined ensures
# the linker doesn't skip that file.)
target_link_options(${MICROPY_TARGET} PUBLIC
  # Patch LWIP memory pool allocators (see lwip_patch.c)
  -Wl,--undefined=memp_malloc
  -Wl,--wrap=memp_malloc
  -Wl,--wrap=memp_free

  # Enable the panic handler wrapper
  -Wl,--undefined=esp_panic_handler
  -Wl,--wrap=esp_panic_handler
)

# Collect all of the include directories and compile definitions for the IDF components,
# including those added by the IDF Component Manager via idf_components.yaml.
foreach(comp ${__COMPONENT_NAMES_RESOLVED})
    micropy_gather_target_properties(__idf_${comp})
    micropy_gather_target_properties(${comp})
endforeach()

# Include the main MicroPython cmake rules.
include(${MICROPY_DIR}/py/mkrules.cmake)

# Generate source files for named pins (requires mkrules.cmake for MICROPY_GENHDR_DIR).

set(GEN_PINS_PREFIX "${MICROPY_PORT_DIR}/boards/pins_prefix.c")
set(GEN_PINS_MKPINS "${MICROPY_PORT_DIR}/boards/make-pins.py")
set(GEN_PINS_SRC "${CMAKE_BINARY_DIR}/pins.c")
set(GEN_PINS_HDR "${MICROPY_GENHDR_DIR}/pins.h")

if(EXISTS "${MICROPY_BOARD_DIR}/pins.csv")
    set(GEN_PINS_BOARD_CSV "${MICROPY_BOARD_DIR}/pins.csv")
    set(GEN_PINS_BOARD_CSV_ARG --board-csv "${GEN_PINS_BOARD_CSV}")
endif()

target_sources(${MICROPY_TARGET} PRIVATE ${GEN_PINS_HDR})

add_custom_command(
    OUTPUT ${GEN_PINS_SRC} ${GEN_PINS_HDR}
    COMMAND ${Python3_EXECUTABLE} ${GEN_PINS_MKPINS} ${GEN_PINS_BOARD_CSV_ARG}
        --prefix ${GEN_PINS_PREFIX} --output-source ${GEN_PINS_SRC} --output-header ${GEN_PINS_HDR}
    DEPENDS
        ${MICROPY_MPVERSION}
        ${GEN_PINS_MKPINS}
        ${GEN_PINS_BOARD_CSV}
        ${GEN_PINS_PREFIX}
    VERBATIM
    COMMAND_EXPAND_LISTS
)

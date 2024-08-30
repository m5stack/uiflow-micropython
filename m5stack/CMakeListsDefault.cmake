# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Set location of base MicroPython directory.
if(NOT MICROPY_DIR)
    get_filename_component(MICROPY_DIR ${PROJECT_DIR}/../micropython/ ABSOLUTE)
endif()

# Include core source components.
include(${MICROPY_DIR}/py/py.cmake)

if(NOT CMAKE_BUILD_EARLY_EXPANSION)
    # Enable extmod components that will be configured by extmod.cmake.
    # A board may also have enabled additional components.
    set(MICROPY_PY_BTREE ON)

    include(${MICROPY_DIR}/py/usermod.cmake)
    include(${MICROPY_DIR}/extmod/extmod.cmake)
endif()

set(MICROPY_QSTRDEFS_PORT
    ${PROJECT_DIR}/../micropython/ports/esp32/qstrdefsport.h
)

set(MICROPY_SOURCE_SHARED
    ${MICROPY_DIR}/shared/readline/readline.c
    ${MICROPY_DIR}/shared/netutils/netutils.c
    ${MICROPY_DIR}/shared/timeutils/timeutils.c
    ${MICROPY_DIR}/shared/runtime/interrupt_char.c
    ${MICROPY_DIR}/shared/runtime/stdout_helpers.c
    ${MICROPY_DIR}/shared/runtime/sys_stdio_mphal.c
    ${MICROPY_DIR}/shared/runtime/pyexec.c
)

set(MICROPY_SOURCE_LIB
    ${MICROPY_DIR}/lib/littlefs/lfs1.c
    ${MICROPY_DIR}/lib/littlefs/lfs1_util.c
    ${MICROPY_DIR}/lib/littlefs/lfs2.c
    ${MICROPY_DIR}/lib/littlefs/lfs2_util.c
    # ${MICROPY_DIR}/lib/mbedtls_errors/mp_mbedtls_errors.c
    ${MICROPY_DIR}/lib/oofatfs/ff.c
    ${MICROPY_DIR}/lib/oofatfs/ffunicode.c
)
if(IDF_TARGET STREQUAL "esp32c3")
    list(APPEND MICROPY_SOURCE_LIB ${MICROPY_DIR}/shared/runtime/gchelper_generic.c)
endif()

set(MICROPY_SOURCE_DRIVERS
    ${MICROPY_DIR}/drivers/bus/softspi.c
    ${MICROPY_DIR}/drivers/dht/dht.c
)

set(MICROPY_SOURCE_PORT
    ${PROJECT_DIR}/board.cpp
    ${PROJECT_DIR}/main.c
    ${PROJECT_DIR}/../micropython/ports/esp32/adc.c
    ${PROJECT_DIR}/../micropython/ports/esp32/ppp_set_auth.c
    ${PROJECT_DIR}/../micropython/ports/esp32/uart.c
    ${PROJECT_DIR}/../micropython/ports/esp32/usb.c
    ${PROJECT_DIR}/../micropython/ports/esp32/usb_serial_jtag.c
    ${PROJECT_DIR}/../micropython/ports/esp32/gccollect.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mphalport.c
    ${PROJECT_DIR}/../micropython/ports/esp32/fatfs_port.c
    ${PROJECT_DIR}/../micropython/ports/esp32/help.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modtime.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_bitstream.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_timer.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_pin.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_touchpad.c
    # ${PROJECT_DIR}/../micropython/ports/esp32/machine_adc.c
    # ${PROJECT_DIR}/../micropython/ports/esp32/machine_adcblock.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_dac.c
    ${PROJECT_DIR}/machine_i2c.c
    # ${PROJECT_DIR}/../micropython/ports/esp32/machine_i2s.c
    # ${PROJECT_DIR}/../micropython/ports/esp32/machine_uart.c
    # ${PROJECT_DIR}/../micropython/ports/esp32/modmachine.c
    ${PROJECT_DIR}/../micropython/ports/esp32/network_common.c
    ${PROJECT_DIR}/../micropython/ports/esp32/network_lan.c
    ${PROJECT_DIR}/../micropython/ports/esp32/network_ppp.c
    ${PROJECT_DIR}/../micropython/ports/esp32/network_wlan.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mpnimbleport.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modsocket.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modesp.c
    ${PROJECT_DIR}/esp32_nvs.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_partition.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_rmt.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_ulp.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modesp32.c
    # ${PROJECT_DIR}/../micropython/ports/esp32/machine_wdt.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mpthreadport.c
    ${PROJECT_DIR}/machine_rtc.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modespnow.c
)

if (BOARD_TYPE STREQUAL "cores3" OR BOARD_TYPE STREQUAL "core2" OR BOARD_TYPE STREQUAL "paper" OR BOARD_TYPE STREQUAL "basic")
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/machine_sdcard.c)
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/machine_hw_spi.c)
else()
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/../micropython/ports/esp32/machine_sdcard.c)
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/../micropython/ports/esp32/machine_hw_spi.c)
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

if(M5_CAMERA_MODULE_ENABLE)
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
    ${MICROPY_SOURCE_M5UNIFIED}
    ${MICROPY_SOURCE_M5CAMERA}
)

set(IDF_COMPONENTS
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
    vfs
    boards
    audio_pipeline
    audio_sal
    esp-adf-libs
    esp-sr
    esp_codec_dev
    xtensa
    esp_http_client
    esp-tls
    libffi
    json
    M5Unified
    esp32-camera
    uiflow_utility
    esp_dmx
)

if(IDF_VERSION_MINOR GREATER_EQUAL 1 OR IDF_VERSION_MAJOR GREATER_EQUAL 5)
    list(APPEND IDF_COMPONENTS esp_netif)
endif()

if(IDF_VERSION_MINOR GREATER_EQUAL 2 OR IDF_VERSION_MAJOR GREATER_EQUAL 5)
    list(APPEND IDF_COMPONENTS esp_system)
    list(APPEND IDF_COMPONENTS esp_timer)
endif()

if(IDF_VERSION_MINOR GREATER_EQUAL 3 OR IDF_VERSION_MAJOR GREATER_EQUAL 5)
    list(APPEND IDF_COMPONENTS esp_hw_support)
    list(APPEND IDF_COMPONENTS esp_pm)
    list(APPEND IDF_COMPONENTS hal)
endif()

# if(IDF_TARGET STREQUAL "esp32")
#     list(APPEND IDF_COMPONENTS esp32)
# elseif(IDF_TARGET STREQUAL "esp32c3")
#     list(APPEND IDF_COMPONENTS esp32c3)
#     list(APPEND IDF_COMPONENTS riscv)
# elseif(IDF_TARGET STREQUAL "esp32s2")
#     list(APPEND IDF_COMPONENTS esp32s2)
#     list(APPEND IDF_COMPONENTS tinyusb)
# elseif(IDF_TARGET STREQUAL "esp32s3")
    # list(APPEND IDF_COMPONENTS esp32s3)
    # list(APPEND IDF_COMPONENTS tinyusb)
    # list(APPEND IDF_COMPONENTS esp_tinyusb)
# endif()

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
    INCLUDE_DIRS
        ${MICROPY_INC_CORE}
        ${MICROPY_INC_USERMOD}
        ${MICROPY_PORT_DIR}
        ${MICROPY_BOARD_DIR}
        ${CMAKE_BINARY_DIR}
    REQUIRES
        ${IDF_COMPONENTS}
)

# Set the MicroPython target as the current (main) IDF component target.
set(MICROPY_TARGET ${COMPONENT_TARGET})

# Define mpy-cross flags, for use with frozen code.
if(NOT IDF_TARGET STREQUAL "esp32c3")
set(MICROPY_CROSS_FLAGS -march=xtensawin)
endif()

# Set compile options for this port.
target_compile_definitions(${MICROPY_TARGET} PUBLIC
    ${MICROPY_DEF_CORE}
    ${MICROPY_DEF_BOARD}
    MICROPY_ESP_IDF_4=1
    MICROPY_VFS_FAT=1
    MICROPY_VFS_LFS2=1
    ESP_PLATFORM=1  # M5GFX platform determine
    FFCONF_H=\"${MICROPY_OOFATFS_DIR}/ffconf.h\"
    LFS1_NO_MALLOC LFS1_NO_DEBUG LFS1_NO_WARN LFS1_NO_ERROR LFS1_NO_ASSERT
    LFS2_NO_MALLOC LFS2_NO_DEBUG LFS2_NO_WARN LFS2_NO_ERROR LFS2_NO_ASSERT
    BOARD_ID=${BOARD_ID}
)

# Disable some warnings to keep the build output clean.
target_compile_options(${MICROPY_TARGET} PUBLIC
    -Wno-clobbered
    -Wno-deprecated-declarations
    -Wno-missing-field-initializers
)

# Additional include directories needed for private NimBLE headers.
target_include_directories(${MICROPY_TARGET} PUBLIC
    ${IDF_PATH}/components/bt/host/nimble/nimble
)

# Add additional extmod and usermod components.
target_link_libraries(${MICROPY_TARGET} micropy_extmod_btree)
target_link_libraries(${MICROPY_TARGET} usermod)


# Collect all of the include directories and compile definitions for the IDF components.
foreach(comp ${IDF_COMPONENTS})
    micropy_gather_target_properties(__idf_${comp})
    micropy_gather_target_properties(${comp})
endforeach()

if(IDF_VERSION_MINOR GREATER_EQUAL 2 OR IDF_VERSION_MAJOR GREATER_EQUAL 5)
    # These paths cannot currently be found by the IDF_COMPONENTS search loop above,
    # so add them explicitly.
    list(APPEND MICROPY_CPP_INC_EXTRA ${IDF_PATH}/components/soc/soc/${IDF_TARGET}/include)
    list(APPEND MICROPY_CPP_INC_EXTRA ${IDF_PATH}/components/soc/soc/include)
    if(IDF_VERSION_MINOR GREATER_EQUAL 3)
        list(APPEND MICROPY_CPP_INC_EXTRA ${IDF_PATH}/components/tinyusb/additions/include)
        list(APPEND MICROPY_CPP_INC_EXTRA ${IDF_PATH}/components/tinyusb/tinyusb/src)
    endif()
endif()

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

target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-format")
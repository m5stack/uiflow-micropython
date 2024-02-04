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
    ${MICROPY_DIR}/lib/mbedtls_errors/mp_mbedtls_errors.c
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
    ${PROJECT_DIR}/main.c
    ${PROJECT_DIR}/../micropython/ports/esp32/uart.c
    ${PROJECT_DIR}/../micropython/ports/esp32/usb.c
    ${PROJECT_DIR}/../micropython/ports/esp32/usb_serial_jtag.c
    ${PROJECT_DIR}/../micropython/ports/esp32/gccollect.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mphalport.c
    ${PROJECT_DIR}/../micropython/ports/esp32/fatfs_port.c
    ${PROJECT_DIR}/../micropython/ports/esp32/help.c
    ${PROJECT_DIR}/modutime.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_bitstream.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_timer.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_pin.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_touchpad.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_adc.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_adcblock.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_dac.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_i2c.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_i2s.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_uart.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modmachine.c
    ${PROJECT_DIR}/../micropython/ports/esp32/network_common.c
    ${PROJECT_DIR}/../micropython/ports/esp32/network_lan.c
    ${PROJECT_DIR}/../micropython/ports/esp32/network_ppp.c
    ${PROJECT_DIR}/network_wlan.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mpnimbleport.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modsocket.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modesp.c
    ${PROJECT_DIR}/esp32_nvs.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_partition.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_rmt.c
    ${PROJECT_DIR}/../micropython/ports/esp32/esp32_ulp.c
    ${PROJECT_DIR}/../micropython/ports/esp32/modesp32.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_wdt.c
    ${PROJECT_DIR}/../micropython/ports/esp32/mpthreadport.c
    ${PROJECT_DIR}/machine_rtc.c
    ${PROJECT_DIR}/../micropython/ports/esp32/machine_sdcard.c
)

if (BOARD_TYPE STREQUAL "cores3" OR BOARD_TYPE STREQUAL "core2")
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/machine_hw_spi.c)
else()
    LIST(APPEND MICROPY_SOURCE_PORT ${PROJECT_DIR}/../micropython/ports/esp32/machine_hw_spi.c)
endif()

# Include LVGL bindings rules
if(NOT CMAKE_BUILD_EARLY_EXPANSION)
    include(${PROJECT_DIR}/components/lv_bindings/mkrules.cmake)
endif()

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
    ${LV_SRC}
)

set(IDF_COMPONENTS
    app_update
    bootloader_support
    bt
    driver
    # esp_adc_cal
    esp_adc
    esp_common
    esp_eth
    esp_event
    esp_ringbuf
    esp_rom
    esp_wifi
    freertos
    heap
    log
    lwip
    mbedtls
    mdns
    newlib
    nvs_flash
    sdmmc
    soc
    spi_flash
    tcpip_adapter
    ulp
    vfs
    xtensa
    esp_http_client
    esp-tls
    nghttp
    libffi
    json
    M5Unified
    esp32-camera
    m5things
    mqtt
    uiflow_utility
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

if(IDF_TARGET STREQUAL "esp32")
    list(APPEND IDF_COMPONENTS esp32)
elseif(IDF_TARGET STREQUAL "esp32c3")
    list(APPEND IDF_COMPONENTS esp32c3)
    list(APPEND IDF_COMPONENTS riscv)
elseif(IDF_TARGET STREQUAL "esp32s2")
    list(APPEND IDF_COMPONENTS esp32s2)
    list(APPEND IDF_COMPONENTS tinyusb)
elseif(IDF_TARGET STREQUAL "esp32s3")
    list(APPEND IDF_COMPONENTS esp32s3)
    list(APPEND IDF_COMPONENTS tinyusb)
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
        ${LV_SRC}
        ${MICROPY_SOURCE_BOARD}
    INCLUDE_DIRS
        ${MICROPY_INC_CORE}
        ${MICROPY_INC_USERMOD}
        ${MICROPY_PORT_DIR}
        ${MICROPY_BOARD_DIR}
        ${CMAKE_BINARY_DIR}
        ${LV_INCLUDE}
    REQUIRES
        ${IDF_COMPONENTS}
)

# Set the MicroPython target as the current (main) IDF component target.
set(MICROPY_TARGET ${COMPONENT_TARGET})

# Define mpy-cross flags, for use with frozen code.
set(MICROPY_CROSS_FLAGS -march=xtensawin)

# Set compile options for this port.
target_compile_definitions(${MICROPY_TARGET} PUBLIC
    ${MICROPY_DEF_CORE}
    MICROPY_ESP_IDF_4=1
    MICROPY_VFS_FAT=1
    MICROPY_VFS_LFS2=1
    ESP_PLATFORM=1  # M5GFX platform determine
    FFCONF_H=\"${MICROPY_OOFATFS_DIR}/ffconf.h\"
    LFS1_NO_MALLOC LFS1_NO_DEBUG LFS1_NO_WARN LFS1_NO_ERROR LFS1_NO_ASSERT
    LFS2_NO_MALLOC LFS2_NO_DEBUG LFS2_NO_WARN LFS2_NO_ERROR LFS2_NO_ASSERT
    LV_KCONFIG_IGNORE
    MICROPY_PY_LVGL=1
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

# Add lv_bindings rules
all_lv_bindings()
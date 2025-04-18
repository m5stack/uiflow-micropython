# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Create an INTERFACE library for our C module.
add_library(moudle_omv INTERFACE)

add_compile_definitions(USE_OMV)

# Add our source files to the lib
target_sources(moudle_omv INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/imlib/draw.c
    ${CMAKE_CURRENT_LIST_DIR}/imlib/font.c
    ${CMAKE_CURRENT_LIST_DIR}/imlib/fmath.c
    ${CMAKE_CURRENT_LIST_DIR}/imlib/imlib.c
    ${CMAKE_CURRENT_LIST_DIR}/modules/py_camera.c
    ${CMAKE_CURRENT_LIST_DIR}/modules/py_helper.c
    ${CMAKE_CURRENT_LIST_DIR}/modules/py_image.c
    ${CMAKE_CURRENT_LIST_DIR}/modules/py_jpg.c
    ${CMAKE_CURRENT_LIST_DIR}/modules/py_code_scanner.c
    ${CMAKE_CURRENT_LIST_DIR}/utils/utils.c
)

# Add the current directory as an include directory.
target_include_directories(moudle_omv INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
    ${CMAKE_CURRENT_LIST_DIR}/imlib/
    ${CMAKE_CURRENT_LIST_DIR}/utils/
    ${CMAKE_CURRENT_LIST_DIR}/modules/
    # esp32-camera
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/driver/include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/driver/private_include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/conversions/include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/conversions/private_include
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp32-camera/sensors/private_include
    # esp-code-scanner
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp-code-scanner/include
)

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE moudle_omv)



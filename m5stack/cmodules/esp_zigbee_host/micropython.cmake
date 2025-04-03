# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Create an INTERFACE library for our C module.
add_library(moudle_esp_zigbee_host INTERFACE)

# Add our source files to the lib
target_sources(moudle_esp_zigbee_host INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/py_esp_zigbee_host.c
)

# Add the current directory as an include directory.
target_include_directories(moudle_esp_zigbee_host INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
    # esp_zigbee_host
    ${CMAKE_CURRENT_LIST_DIR}/../../components/esp_zigbee_host/include
)

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE moudle_esp_zigbee_host)

# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
# SPDX-License-Identifier: MIT

add_library(module_usbhost INTERFACE)
target_sources(module_usbhost INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/py_usbhost.c
    ${CMAKE_CURRENT_LIST_DIR}/usbhost_backend.c
    ${CMAKE_CURRENT_LIST_DIR}/usbhost_power.cpp
    ${CMAKE_CURRENT_LIST_DIR}/hid_report.c
)
target_include_directories(module_usbhost INTERFACE ${CMAKE_CURRENT_LIST_DIR})
target_link_libraries(module_usbhost INTERFACE idf::espressif__usb_host_hid)
target_link_libraries(usermod INTERFACE module_usbhost)

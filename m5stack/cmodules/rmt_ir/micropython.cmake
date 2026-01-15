# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Create an INTERFACE library for our C module.
add_library(module_rmt_ir INTERFACE)

# Add our source files to the lib
target_sources(module_rmt_ir INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/py_rmt_ir.c
)

# Add the current directory as an include directory.
target_include_directories(module_rmt_ir INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE module_rmt_ir)


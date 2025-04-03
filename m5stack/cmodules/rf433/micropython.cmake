# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Create an INTERFACE library for our C module.
add_library(moudle_rf433 INTERFACE)

# Add our source files to the lib
target_sources(moudle_rf433 INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/py_rf433.c
)

# Add the current directory as an include directory.
target_include_directories(moudle_rf433 INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE moudle_rf433)



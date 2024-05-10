# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# Create an INTERFACE library for our C module.
add_library(usermod_m5can INTERFACE)

# Add our source files to the lib
target_sources(usermod_m5can INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/modcan.c
)

# Add the current directory as an include directory.
target_include_directories(usermod_m5can INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

# Link our INTERFACE library to the usermod target.
target_link_libraries(usermod INTERFACE usermod_m5can)

# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(COMPONENT_ADD_INCLUDEDIRS
    .
)

file(GLOB SRCS
    *.cpp
)

set(COMPONENT_SRCS ${SRCS})
set(COMPONENT_REQUIRES M5Unified M5GFX)


register_component()
target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-format")

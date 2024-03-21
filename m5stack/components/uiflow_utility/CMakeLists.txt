# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

set(COMPONENT_ADD_INCLUDEDIRS
    .
)

file(GLOB SRCS
    *.c
)

set(COMPONENT_SRCS ${SRCS})
set(COMPONENT_REQUIRES nvs_flash)


register_component()
target_compile_options(${COMPONENT_LIB} PRIVATE "-Wno-format")

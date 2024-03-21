# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

cmake_minimum_required (VERSION 3.16)

project(littlefs2)

include_directories(mbed-littlefs)
aux_source_directory(mbed-littlefs/littlefs DIR_SRCS)

add_executable(littlefs2 littlefs2.c ${DIR_SRCS})
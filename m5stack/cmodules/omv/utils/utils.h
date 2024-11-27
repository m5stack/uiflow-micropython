/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#ifndef __UTILS_H
#define __UTILS_H


#include "imlib.h"
#include "py_image.h"


void mono_to_stereo(uint16_t *data, uint32_t len);
int utf8_to_unicode(const char *utf8_in, uint64_t *unicode_out);
void convert_image_endian(uint16_t *buffer, int width, int height);


#endif // __UTILS_H

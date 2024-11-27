/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include "utils.h"
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include <math.h>
#include <assert.h>
#include "esp_log.h"

#include "imlib.h"


static const char *TAG = "usils";



static int get_utf8_byte_size(const char input_byte) {
    if (input_byte < 0x80) {
        return 1;
    }
    if (input_byte < 0xC0) {
        return -1;
    }
    if (input_byte < 0xE0) {
        return 2;
    }
    if (input_byte < 0xF0) {
        return 3;
    }
    if (input_byte < 0xF8) {
        return 4;
    }
    if (input_byte < 0xFC) {
        return 5;
    }
    return 6;
}

int utf8_to_unicode(const char *utf8_input, uint64_t *unicode_output) {
    assert(utf8_input != NULL && unicode_output != NULL);
    *unicode_output = 0;

    int utf_bytes = get_utf8_byte_size(*utf8_input);
    uint8_t *output = (uint8_t *)unicode_output;

    switch (utf_bytes) {
        case 1:
            *output = *utf8_input;
            break;
        case 2:
            if ((*(utf8_input + 1) & 0xC0) != 0x80) {
                return 0;
            }
            *output = (*utf8_input << 6) + (*(utf8_input + 1) & 0x3F);
            output[1] = (*utf8_input >> 2) & 0x07;
            break;
        case 3:
            if ((*(utf8_input + 1) & 0xC0) != 0x80 || (*(utf8_input + 2) & 0xC0) != 0x80) {
                return 0;
            }
            *output = (*(utf8_input + 1) << 6) + (*(utf8_input + 2) & 0x3F);
            output[1] = (*utf8_input << 4) + ((*(utf8_input + 1) >> 2) & 0x0F);
            break;
        case 4:
            if ((*(utf8_input + 1) & 0xC0) != 0x80 || (*(utf8_input + 2) & 0xC0) != 0x80
                || (*(utf8_input + 3) & 0xC0) != 0x80) {
                return 0;
            }
            *output = (*(utf8_input + 2) << 6) + (*(utf8_input + 3) & 0x3F);
            output[1] = (*(utf8_input + 1) << 4) + ((*(utf8_input + 2) >> 2) & 0x0F);
            output[2] = ((*utf8_input << 2) & 0x1C) + ((*(utf8_input + 1) >> 4) & 0x03);
            break;
        case 5:
            if ((*(utf8_input + 1) & 0xC0) != 0x80 || (*(utf8_input + 2) & 0xC0) != 0x80
                || (*(utf8_input + 3) & 0xC0) != 0x80 || (*(utf8_input + 4) & 0xC0) != 0x80) {
                return 0;
            }
            *output = (*(utf8_input + 3) << 6) + (*(utf8_input + 4) & 0x3F);
            output[1] = (*(utf8_input + 2) << 4) + ((*(utf8_input + 3) >> 2) & 0x0F);
            output[2] = (*(utf8_input + 1) << 2) + ((*(utf8_input + 2) >> 4) & 0x03);
            output[3] = (*utf8_input << 6);
            break;
        case 6:
            if ((*(utf8_input + 1) & 0xC0) != 0x80 || (*(utf8_input + 2) & 0xC0) != 0x80
                || (*(utf8_input + 3) & 0xC0) != 0x80 || (*(utf8_input + 4) & 0xC0) != 0x80
                || (*(utf8_input + 5) & 0xC0) != 0x80) {
                return 0;
            }
            *output = (*(utf8_input + 4) << 6) + (*(utf8_input + 5) & 0x3F);
            output[1] = (*(utf8_input + 3) << 4) + ((*(utf8_input + 4) >> 2) & 0x0F);
            output[2] = (*(utf8_input + 2) << 2) + ((*(utf8_input + 3) >> 4) & 0x03);
            output[3] = ((*utf8_input << 6) & 0x40) + (*(utf8_input + 1) & 0x3F);
            break;
        default:
            return 0;
    }

    return utf_bytes;
}

void convert_image_endian(uint16_t *buffer, int width, int height) {
    for (int i = 0; i < width * height; i++) {
        buffer[i] = (buffer[i] >> 8) | (buffer[i] << 8);
    }
}

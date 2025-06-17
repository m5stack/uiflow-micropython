/*
* SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#ifndef _M5_CRYPTO_H_
#define _M5_CRYPTO_H_

#include <stddef.h>
#include <stdint.h>

int m5_hmac_sha256(const uint8_t *key, size_t key_len, const uint8_t *data,
                size_t data_len, uint8_t *mac);

char * m5_base64_encode(const void *src, size_t len, size_t *out_len);
char * m5_base64_url_encode(const void *src, size_t len, size_t *out_len);
unsigned char * m5_base64_decode(const char *src, size_t len, size_t *out_len);
unsigned char * m5_base64_url_decode(const char *src, size_t len, size_t *out_len);

#endif

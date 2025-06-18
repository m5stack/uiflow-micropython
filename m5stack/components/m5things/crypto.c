/*
* SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "crypto.h"
#include "mbedtls/md.h"
#include <string.h>
#include <stdlib.h>


static int hmac_vector(mbedtls_md_type_t md_type,
    const uint8_t *key, size_t key_len,
    size_t num_elem, const uint8_t *addr[],
    const size_t *len, uint8_t *mac) {
    size_t i;
    const mbedtls_md_info_t *md_info;
    mbedtls_md_context_t md_ctx;
    int ret;

    mbedtls_md_init(&md_ctx);

    md_info = mbedtls_md_info_from_type(md_type);
    if (!md_info) {
        return -1;
    }

    ret = mbedtls_md_setup(&md_ctx, md_info, 1);
    if (ret != 0) {
        return ret;
    }

    ret = mbedtls_md_hmac_starts(&md_ctx, key, key_len);
    if (ret != 0) {
        return ret;
    }

    for (i = 0; i < num_elem; i++) {
        ret = mbedtls_md_hmac_update(&md_ctx, addr[i], len[i]);
        if (ret != 0) {
            return ret;
        }

    }

    ret = mbedtls_md_hmac_finish(&md_ctx, mac);

    mbedtls_md_free(&md_ctx);

    return ret;
}


static int hmac_sha256_vector(const uint8_t *key, size_t key_len, size_t num_elem,
    const uint8_t *addr[], const size_t *len, uint8_t *mac) {
    return hmac_vector(MBEDTLS_MD_SHA256, key, key_len, num_elem, addr,
        len, mac);
}

int m5_hmac_sha256(const uint8_t *key, size_t key_len, const uint8_t *data,
    size_t data_len, uint8_t *mac) {
    return hmac_sha256_vector(key, key_len, 1, &data, &data_len, mac);
}



static const char base64_table[65] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
static const char base64_url_table[65] =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_";


static char *base64_gen_encode(const unsigned char *src, size_t len,
    size_t *out_len, const char *table, int add_pad) {
    char *out, *pos;
    const unsigned char *end, *in;
    size_t olen;
    int line_len;

    if (len >= SIZE_MAX / 4) {
        return NULL;
    }
    olen = len * 4 / 3 + 4;     /* 3-byte blocks to 4-byte */
    if (add_pad) {
        olen += olen / 72;         /* line feeds */
    }
    olen++;     /* nul termination */
    if (olen < len) {
        return NULL;         /* integer overflow */
    }
    out = malloc(olen);
    if (out == NULL) {
        return NULL;
    }

    end = src + len;
    in = src;
    pos = out;
    line_len = 0;
    while (end - in >= 3) {
        *pos++ = table[(in[0] >> 2) & 0x3f];
        *pos++ = table[(((in[0] & 0x03) << 4) | (in[1] >> 4)) & 0x3f];
        *pos++ = table[(((in[1] & 0x0f) << 2) | (in[2] >> 6)) & 0x3f];
        *pos++ = table[in[2] & 0x3f];
        in += 3;
        line_len += 4;
        if (add_pad && line_len >= 72) {
            *pos++ = '\n';
            line_len = 0;
        }
    }

    if (end - in) {
        *pos++ = table[(in[0] >> 2) & 0x3f];
        if (end - in == 1) {
            *pos++ = table[((in[0] & 0x03) << 4) & 0x3f];
            if (add_pad) {
                *pos++ = '=';
            }
        } else {
            *pos++ = table[(((in[0] & 0x03) << 4) |
                (in[1] >> 4)) & 0x3f];
            *pos++ = table[((in[1] & 0x0f) << 2) & 0x3f];
        }
        if (add_pad) {
            *pos++ = '=';
        }
        line_len += 4;
    }

    if (add_pad && line_len) {
        *pos++ = '\n';
    }

    *pos = '\0';
    if (out_len) {
        *out_len = pos - out;
    }
    return out;
}


static unsigned char *base64_gen_decode(const char *src, size_t len,
    size_t *out_len, const char *table) {
    unsigned char dtable[256], *out, *pos, block[4], tmp;
    size_t i, count, olen;
    int pad = 0;
    size_t extra_pad;

    memset(dtable, 0x80, 256);
    for (i = 0; i < sizeof(base64_table) - 1; i++) {
        dtable[(unsigned char)table[i]] = (unsigned char)i;
    }
    dtable['='] = 0;

    count = 0;
    for (i = 0; i < len; i++) {
        if (dtable[(unsigned char)src[i]] != 0x80) {
            count++;
        }
    }

    if (count == 0) {
        return NULL;
    }
    extra_pad = (4 - count % 4) % 4;

    olen = (count + extra_pad) / 4 * 3;
    pos = out = malloc(olen);
    if (out == NULL) {
        return NULL;
    }

    count = 0;
    for (i = 0; i < len + extra_pad; i++) {
        unsigned char val;

        if (i >= len) {
            val = '=';
        } else {
            val = src[i];
        }
        tmp = dtable[val];
        if (tmp == 0x80) {
            continue;
        }

        if (val == '=') {
            pad++;
        }
        block[count] = tmp;
        count++;
        if (count == 4) {
            *pos++ = (block[0] << 2) | (block[1] >> 4);
            *pos++ = (block[1] << 4) | (block[2] >> 2);
            *pos++ = (block[2] << 6) | block[3];
            count = 0;
            if (pad) {
                if (pad == 1) {
                    pos--;
                } else if (pad == 2) {
                    pos -= 2;
                } else {
                    /* Invalid padding */
                    free(out);
                    return NULL;
                }
                break;
            }
        }
    }

    *out_len = pos - out;
    return out;
}


/**
 * m5_base64_encode - Base64 encode
 * @src: Data to be encoded
 * @len: Length of the data to be encoded
 * @out_len: Pointer to output length variable, or %NULL if not used
 * Returns: Allocated buffer of out_len bytes of encoded data,
 * or %NULL on failure
 *
 * Caller is responsible for freeing the returned buffer. Returned buffer is
 * nul terminated to make it easier to use as a C string. The nul terminator is
 * not included in out_len.
 */
char *m5_base64_encode(const void *src, size_t len, size_t *out_len) {
    return base64_gen_encode(src, len, out_len, base64_table, 1);
}


char *m5_base64_url_encode(const void *src, size_t len, size_t *out_len) {
    return base64_gen_encode(src, len, out_len, base64_url_table, 0);
}

/**
 * m5_base64_decode - Base64 decode
 * @src: Data to be decoded
 * @len: Length of the data to be decoded
 * @out_len: Pointer to output length variable
 * Returns: Allocated buffer of out_len bytes of decoded data,
 * or %NULL on failure
 *
 * Caller is responsible for freeing the returned buffer.
 */
unsigned char *m5_base64_decode(const char *src, size_t len, size_t *out_len) {
    return base64_gen_decode(src, len, out_len, base64_table);
}


unsigned char *m5_base64_url_decode(const char *src, size_t len, size_t *out_len) {
    return base64_gen_decode(src, len, out_len, base64_url_table);
}

/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#ifndef _I2S_HELPER_H_
#define _I2S_HELPER_H_

#include "driver/i2s_std.h"

typedef enum i2s_mode_t {
    I2S_MODE_TX = 0,
    I2S_MODE_RX,
} i2s_mode_t;

typedef enum {
    MONO = 1,
    STEREO = 2,
} channel_t;

esp_err_t i2s_std_init_helper(int id, i2s_mode_t mode, int sck, int ws, int sd, int mck, int rate, int bits, int channel, i2s_chan_handle_t *i2s_chan_handle);
esp_err_t i2s_std_deinit_helper(i2s_chan_handle_t i2s_chan_handle);

#endif

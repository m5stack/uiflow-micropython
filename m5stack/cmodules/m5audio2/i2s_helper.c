/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include "i2s_helper.h"
#include "esp_log.h"

const static char *TAG = "I2S_HELPER";

#define DMA_BUF_LEN_IN_I2S_FRAMES (256)

esp_err_t i2s_std_init_helper(int id, i2s_mode_t mode, int sck, int ws, int sd, int mck, int rate, int bits, int channel, i2s_chan_handle_t *i2s_chan_handle) {
    i2s_chan_config_t chan_config = I2S_CHANNEL_DEFAULT_CONFIG(id, I2S_ROLE_MASTER);
    chan_config.dma_desc_num = 8;
    chan_config.dma_frame_num = DMA_BUF_LEN_IN_I2S_FRAMES;
    chan_config.auto_clear = true;
    esp_err_t ret = ESP_OK;

    if (mode == I2S_MODE_TX) {
        ret = i2s_new_channel(&chan_config, i2s_chan_handle, NULL);
    } else {
        ret = i2s_new_channel(&chan_config, NULL, i2s_chan_handle);
    }
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to create I2S channel");
        return ret;
    }

    i2s_std_slot_config_t slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(bits, channel);
    slot_cfg.slot_mask = I2S_STD_SLOT_BOTH;

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(rate),
        .slot_cfg = slot_cfg,
        .gpio_cfg = {
            .mclk = mck,
            .bclk = sck,
            .ws = ws,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv = false,
            },
        },
    };

    if (mode == I2S_MODE_TX) {
        std_cfg.gpio_cfg.dout = sd;
        std_cfg.gpio_cfg.din = I2S_GPIO_UNUSED;
    } else {
        std_cfg.gpio_cfg.dout = I2S_GPIO_UNUSED,
        std_cfg.gpio_cfg.din = sd;
    }

    ret = i2s_channel_init_std_mode(*i2s_chan_handle, &std_cfg);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to initialize I2S channel");
        i2s_del_channel(*i2s_chan_handle);
        return ret;
    }
    // check_esp_err(i2s_channel_register_event_callback(self->i2s_chan_handle, &i2s_callbacks, self));
    ret = i2s_channel_enable(*i2s_chan_handle);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to enable I2S channel");
        i2s_del_channel(*i2s_chan_handle);
        return ret;
    }
    return ret;
}


esp_err_t i2s_std_deinit_helper(i2s_chan_handle_t i2s_chan_handle) {
    esp_err_t ret = i2s_channel_disable(i2s_chan_handle);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to disable I2S channel");
        return ret;
    }
    ret = i2s_del_channel(i2s_chan_handle);
    if (ret != ESP_OK) {
        ESP_LOGE(TAG, "Failed to delete I2S channel");
        return ret;
    }
    return ret;
}

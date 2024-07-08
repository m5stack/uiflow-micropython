/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/
// NOTE: 使用IDF5会导致 i2s 驱动冲突，暂时不使用。
#define USE_IDF5 (0)

// #include "esp_idf_version.h"
#if USE_IDF5
#include "driver/i2s_std.h"
#include "driver/i2s_tdm.h"
#include "soc/soc_caps.h"
#else
#include "driver/i2s.h"
#endif

#if ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(5, 3, 0)
#include "driver/i2c_master.h"
#define USE_IDF_I2C_MASTER
#else
#include "driver/i2c.h"
#endif

#include "board_init.h"
#include "esp_log.h"
#include "driver/gpio.h"
#include "esp_codec_dev.h"
#include "esp_codec_dev_defaults.h"

static char *TAG = "s3_box_3_board";
static void *audio_hal = NULL;

static int ut_i2c_init(uint8_t port);
static int ut_i2s_init(uint8_t port);

void * board_codec_init(void)
{
    if (audio_hal) {
        return audio_hal;
    }
    ESP_LOGI(TAG, "init");

    int ret = ut_i2c_init(0);
    ret |= ut_i2s_init(0);

    audio_codec_i2s_cfg_t i2s_cfg = {
        .port = 0
#if USE_IDF5
        .rx_handle = i2s_keep[0]->rx_handle,
        .tx_handle = i2s_keep[0]->tx_handle,
#endif
    };
    const audio_codec_data_if_t *data_if = audio_codec_new_i2s_data(&i2s_cfg);

    audio_codec_i2c_cfg_t i2c_cfg = {
        .port = 0,
        .addr = ES8311_CODEC_DEFAULT_ADDR
    };
#ifdef USE_IDF_I2C_MASTER
    i2c_cfg.bus_handle = i2c_bus_handle;
#endif
    const audio_codec_ctrl_if_t *out_ctrl_if = audio_codec_new_i2c_ctrl(&i2c_cfg);

    const audio_codec_gpio_if_t *gpio_if = audio_codec_new_gpio();

    es8311_codec_cfg_t es8311_cfg = {
        .ctrl_if = out_ctrl_if,
        .gpio_if = gpio_if,
        .codec_mode = ESP_CODEC_DEV_WORK_MODE_BOTH,
        .pa_pin = GPIO_NUM_46,
        .use_mclk = true,
        // .digital_mic = false,
        // .invert_mclk = false,
        // .invert_sclk = false,
        // .hw_gain = {
        //     .pa_voltage = 5.0,
        //     .codec_dac_voltage = 3.3,
        //     .pa_gain = 0.0,
        // },
        // .no_dac_ref = true,
        // .mclk_div = 256,
    };
    const audio_codec_if_t *out_codec_if = es8311_codec_new(&es8311_cfg);

    esp_codec_dev_cfg_t dev_cfg = {
        .codec_if = out_codec_if,
        .data_if = data_if,
        .dev_type = ESP_CODEC_DEV_TYPE_IN_OUT,
    };
    audio_hal = esp_codec_dev_new(&dev_cfg);

    esp_codec_dev_sample_info_t fs = {
        .sample_rate = 48000,
        .channel = 2,
        .bits_per_sample = 16,
    };
    esp_codec_dev_open(audio_hal, &fs);

    return audio_hal;
}


// NOTE: 使用内联函数???
int board_codec_volume_set(void *hd, int vol)
{
    return esp_codec_dev_set_out_vol(hd, vol);
}


// NOTE: 使用内联函数???
int board_codec_volume_get(void *hd, int *vol)
{
    return esp_codec_dev_get_out_vol(hd, vol);
}


static int ut_i2c_init(uint8_t port)
{
#ifdef USE_IDF_I2C_MASTER
    i2c_master_bus_config_t i2c_bus_config = {0};
    i2c_bus_config.clk_source = I2C_CLK_SRC_DEFAULT;
    i2c_bus_config.i2c_port = port;
    i2c_bus_config.scl_io_num = TEST_BOARD_I2C_SCL_PIN;
    i2c_bus_config.sda_io_num = TEST_BOARD_I2C_SDA_PIN;
    i2c_bus_config.glitch_ignore_cnt = 7;
    i2c_bus_config.flags.enable_internal_pullup = true;
    return i2c_new_master_bus(&i2c_bus_config, &i2c_bus_handle);
#else
    i2c_config_t i2c_cfg = {
        .mode = I2C_MODE_MASTER,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = 100000,
    };
    i2c_cfg.sda_io_num = 8;
    i2c_cfg.scl_io_num = 18;
    esp_err_t ret = i2c_param_config(port, &i2c_cfg);
    if (ret != ESP_OK) {
        return -1;
    }
    return i2c_driver_install(port, i2c_cfg.mode, 0, 0, 0);
#endif
}


static int ut_i2s_init(uint8_t port)
{
#if USE_IDF5
    if (port >= I2S_MAX_KEEP) {
        return -1;
    }
    // Already installed
    if (i2s_keep[port]) {
        return 0;
    }
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM_0, I2S_ROLE_MASTER);
    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(16000),
        .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(16, I2S_SLOT_MODE_STEREO),
        .gpio_cfg ={
            .mclk = 0,
            .bclk = 34,
            .ws = 33,
            .dout = 13,
            .din = -1,
        },
    };
    i2s_keep[port] = (i2s_keep_t *) calloc(1, sizeof(i2s_keep_t));
    if (i2s_keep[port] == NULL) {
        return -1;
    }
#if SOC_I2S_SUPPORTS_TDM 
    i2s_tdm_slot_mask_t slot_mask = I2S_TDM_SLOT0 | I2S_TDM_SLOT1 | I2S_TDM_SLOT2 | I2S_TDM_SLOT3;
    i2s_tdm_config_t tdm_cfg = {
        .slot_cfg = I2S_TDM_PHILIPS_SLOT_DEFAULT_CONFIG(16, I2S_SLOT_MODE_STEREO, slot_mask),
        .clk_cfg  = I2S_TDM_CLK_DEFAULT_CONFIG(16000),
        .gpio_cfg = {
            .mclk = 0,
            .bclk = 34,
            .ws = 33,
            .dout = 13,
            .din = -1,
        },
    };
    tdm_cfg.slot_cfg.total_slot = 4;
#endif
    int ret = i2s_new_channel(&chan_cfg, &i2s_keep[port]->tx_handle, &i2s_keep[port]->rx_handle);
    if (i2s_out_mode == I2S_COMM_MODE_STD) {
        ret = i2s_channel_init_std_mode(i2s_keep[port]->tx_handle, &std_cfg);
    }
#if SOC_I2S_SUPPORTS_TDM 
    else if (i2s_out_mode == I2S_COMM_MODE_TDM) {
        ret = i2s_channel_init_tdm_mode(i2s_keep[port]->tx_handle, &tdm_cfg);
    }
#endif
    if (i2s_in_mode == I2S_COMM_MODE_STD) {
        ret = i2s_channel_init_std_mode(i2s_keep[port]->rx_handle, &std_cfg);
    } 
#if SOC_I2S_SUPPORTS_TDM 
    else if (i2s_in_mode == I2S_COMM_MODE_TDM) {
        ret = i2s_channel_init_tdm_mode(i2s_keep[port]->rx_handle, &tdm_cfg);
    }
#endif
    // For tx master using duplex mode
    i2s_channel_enable(i2s_keep[port]->tx_handle);
#else
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t) (I2S_MODE_TX | I2S_MODE_RX | I2S_MODE_MASTER),
        .sample_rate = 48000,
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
        .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL2 | ESP_INTR_FLAG_IRAM,
        .dma_buf_count = 2,
        .dma_buf_len = 128,
        .use_apll = true,
        .tx_desc_auto_clear = true,
    };
    int ret = i2s_driver_install(port, &i2s_config, 0, NULL);
    i2s_pin_config_t i2s_pin_cfg = {
        .mck_io_num = GPIO_NUM_2,
        .bck_io_num = GPIO_NUM_17,
        .ws_io_num = GPIO_NUM_45,
        .data_out_num = GPIO_NUM_15,
        .data_in_num = GPIO_NUM_16,
    };
    i2s_set_pin(port, &i2s_pin_cfg);
#endif
    return ret;
}
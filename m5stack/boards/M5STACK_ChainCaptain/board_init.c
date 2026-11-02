/*
* SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

// NOTE: 使用IDF5的 i2s 驱动
#define USE_IDF5 (1)

#if USE_IDF5
#include "driver/i2s_std.h"
#include "driver/i2s_tdm.h"
#include "soc/soc_caps.h"
#else
#include "driver/i2s.h"
#endif

#include "string.h"
#include "board_init.h"
#include "esp_log.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_codec_dev.h"
#include "esp_codec_dev_defaults.h"

#if ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(5, 3, 0)
#include "driver/i2c_master.h"
#define USE_IDF_I2C_MASTER
#else
#include "driver/i2c.h"
#endif

static char *TAG = "chain_captain";
static void *audio_hal = NULL;

// M5Unified board_M5ChainCaptain audio pins
#define AUDIO_I2S_GPIO_MCLK      GPIO_NUM_40
#define AUDIO_I2S_GPIO_WS        GPIO_NUM_41
#define AUDIO_I2S_GPIO_BCLK      GPIO_NUM_38
#define AUDIO_I2S_GPIO_DIN       GPIO_NUM_39
#define AUDIO_I2S_GPIO_DOUT      GPIO_NUM_42
#define AUDIO_CODEC_I2C_SDA_PIN  GPIO_NUM_3
#define AUDIO_CODEC_I2C_SCL_PIN  GPIO_NUM_2
#define AUDIO_CODEC_ES8311_ADDR  ES8311_CODEC_DEFAULT_ADDR
#define AUDIO_CODEC_GPIO_PA      GPIO_NUM_21

// M5IOE1@0x4F (ChainCaptain), register map aligned with M5Unified
#define M5IOE1_I2C_ADDR          0x4F
#define M5IOE1_REG_I2C_CFG       0x23
#define M5IOE1_REG_GPIO_MODE_L   0x03
#define M5IOE1_REG_GPIO_MODE_H   0x04
#define M5IOE1_REG_GPIO_OUT_L    0x05
#define M5IOE1_REG_GPIO_OUT_H    0x06
#define M5IOE1_REG_GPIO_DRV_L    0x13
#define M5IOE1_REG_GPIO_DRV_H    0x14
#define M5IOE1_G5_AUDIO_PWR      (1u << 4)   // M5IOE1 G5 / Audio Power

#if USE_IDF5

#define I2S_MAX_KEEP SOC_I2S_NUM

typedef struct {
    i2s_chan_handle_t tx_handle;
    i2s_chan_handle_t rx_handle;
} i2s_keep_t;

static i2s_comm_mode_t i2s_in_mode = I2S_COMM_MODE_STD;
static i2s_comm_mode_t i2s_out_mode = I2S_COMM_MODE_STD;
static i2s_keep_t *i2s_keep[I2S_MAX_KEEP];
#endif

#ifdef USE_IDF_I2C_MASTER
static i2c_master_bus_handle_t i2c_bus_handle;
static bool first_i2c_init = false;
static bool m5ioe1_gpio_inited = false;
#endif

static int ut_i2c_init(uint8_t port);
static int ut_i2c_deinit(uint8_t port);

static int ut_i2s_init(uint8_t port);
static int ut_i2s_deinit(uint8_t port);

static void m5ioe1_gpio_init_once(void);
static void m5ioe1_codec_power_set(bool on);
static void m5ioe1_pa_set(bool on);

esp_err_t get_i2s_pins(int port, board_i2s_pin_t *i2s_config)
{
    ESP_LOGI(TAG, "get_i2s_pins");
    AUDIO_NULL_CHECK(TAG, i2s_config, return ESP_FAIL);
    if (port == 0) {
        i2s_config->bck_io_num = AUDIO_I2S_GPIO_BCLK;
        i2s_config->ws_io_num = AUDIO_I2S_GPIO_WS;
        i2s_config->data_out_num = AUDIO_I2S_GPIO_DOUT;
        i2s_config->data_in_num = AUDIO_I2S_GPIO_DIN;
        i2s_config->mck_io_num = AUDIO_I2S_GPIO_MCLK;
    } else {
        memset(i2s_config, -1, sizeof(board_i2s_pin_t));
        ESP_LOGE(TAG, "I2S PORT %d is not supported, please use I2S PORT 0", port);
        return ESP_FAIL;
    }
    return ESP_OK;
}

void * board_codec_init(void)
{
    if (audio_hal) {
        // Speaker.end() may power off G5; re-enable codec supply for record/play.
        m5ioe1_codec_power_set(true);
        return audio_hal;
    }
    ESP_LOGI(TAG, "init");

    if (ut_i2c_init(1) != ESP_OK) {
        ESP_LOGE(TAG, "ut_i2c_init failed");
        return NULL;
    }
    m5ioe1_gpio_init_once();
    m5ioe1_codec_power_set(true);
    int ret = ut_i2s_init(0);

    audio_codec_i2s_cfg_t i2s_cfg = {
        .port = 0,
#if USE_IDF5
        .rx_handle = i2s_keep[0]->rx_handle,
        .tx_handle = i2s_keep[0]->tx_handle,
#endif
    };
    const audio_codec_data_if_t *data_if = audio_codec_new_i2s_data(&i2s_cfg);

    audio_codec_i2c_cfg_t i2c_cfg = {
        .port = 1,
        .addr = AUDIO_CODEC_ES8311_ADDR,
    };
#ifdef USE_IDF_I2C_MASTER
    i2c_cfg.bus_handle = i2c_bus_handle;
#endif
    const audio_codec_ctrl_if_t *ctrl_if = audio_codec_new_i2c_ctrl(&i2c_cfg);
    const audio_codec_gpio_if_t *gpio_if = audio_codec_new_gpio();

    es8311_codec_cfg_t es8311_cfg = {};
    es8311_cfg.ctrl_if = ctrl_if;
    es8311_cfg.gpio_if = gpio_if;
    es8311_cfg.codec_mode = ESP_CODEC_DEV_WORK_MODE_BOTH;
    es8311_cfg.pa_pin = AUDIO_CODEC_GPIO_PA;
    es8311_cfg.use_mclk = true;
    es8311_cfg.hw_gain.pa_voltage = 5.0;
    es8311_cfg.hw_gain.codec_dac_voltage = 3.3;
    es8311_cfg.pa_reverted = false;
    const audio_codec_if_t *codec_if = es8311_codec_new(&es8311_cfg);

    esp_codec_dev_cfg_t dev_cfg = {
        .dev_type = ESP_CODEC_DEV_TYPE_IN_OUT,
        .codec_if = codec_if,
        .data_if = data_if,
    };
    audio_hal = esp_codec_dev_new(&dev_cfg);

    esp_codec_dev_sample_info_t fs = {
        .bits_per_sample = 16,
        .channel = 1,
        .channel_mask = 0,
        .sample_rate = (uint32_t)48000,
        .mclk_multiple = 0,
    };
    esp_codec_dev_open(audio_hal, &fs);
    esp_codec_dev_set_in_gain(audio_hal, 50.0);
    esp_codec_dev_set_out_vol(audio_hal, 60);

    ut_i2s_deinit(0);
    m5ioe1_pa_set(true);

    return audio_hal;
}

int board_codec_volume_set(void *hd, int vol)
{
    return esp_codec_dev_set_out_vol(hd, vol);
}

int board_codec_volume_get(void *hd, int *vol)
{
    return esp_codec_dev_get_out_vol(hd, vol);
}

static int ut_i2c_init(uint8_t port)
{
#ifdef USE_IDF_I2C_MASTER
    if (i2c_master_get_bus_handle(port, &i2c_bus_handle) != ESP_OK) {
        first_i2c_init = true;
        i2c_master_bus_config_t i2c_bus_config = {0};
        i2c_bus_config.clk_source = I2C_CLK_SRC_DEFAULT;
        i2c_bus_config.i2c_port = port;
        i2c_bus_config.scl_io_num = AUDIO_CODEC_I2C_SCL_PIN;
        i2c_bus_config.sda_io_num = AUDIO_CODEC_I2C_SDA_PIN;
        i2c_bus_config.glitch_ignore_cnt = 7;
        i2c_bus_config.flags.enable_internal_pullup = true;
        return i2c_new_master_bus(&i2c_bus_config, &i2c_bus_handle);
    }
    return ESP_OK;
#else
    i2c_config_t i2c_cfg = {
        .mode = I2C_MODE_MASTER,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = 100000,
    };
    i2c_cfg.scl_io_num = AUDIO_CODEC_I2C_SCL_PIN;
    i2c_cfg.sda_io_num = AUDIO_CODEC_I2C_SDA_PIN;
    esp_err_t ret = i2c_param_config(port, &i2c_cfg);
    if (ret != ESP_OK) {
        return -1;
    }
    return i2c_driver_install(port, i2c_cfg.mode, 0, 0, 0);
#endif
}

static int ut_i2c_deinit(uint8_t port)
{
#ifdef USE_IDF_I2C_MASTER
    if (i2c_bus_handle && first_i2c_init) {
        i2c_del_master_bus(i2c_bus_handle);
    }
    i2c_bus_handle = NULL;
    return 0;
#else
    return i2c_driver_delete(port);
#endif
}

#if USE_IDF5
static void ut_set_i2s_mode(i2s_comm_mode_t out_mode, i2s_comm_mode_t in_mode)
{
    i2s_in_mode = in_mode;
    i2s_out_mode = out_mode;
}

static void ut_clr_i2s_mode(void)
{
    i2s_in_mode = I2S_COMM_MODE_STD;
    i2s_out_mode = I2S_COMM_MODE_STD;
}
#endif

static int ut_i2s_init(uint8_t port)
{
#if USE_IDF5
    if (port >= I2S_MAX_KEEP) {
        return -1;
    }
    if (i2s_keep[port]) {
        return 0;
    }
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(port, I2S_ROLE_MASTER);
    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(16000),
        .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_CONFIG(16, I2S_SLOT_MODE_STEREO),
        .gpio_cfg = {
            .mclk = AUDIO_I2S_GPIO_MCLK,
            .bclk = AUDIO_I2S_GPIO_BCLK,
            .ws = AUDIO_I2S_GPIO_WS,
            .dout = AUDIO_I2S_GPIO_DOUT,
            .din = AUDIO_I2S_GPIO_DIN,
        },
    };
    i2s_keep[port] = (i2s_keep_t *) calloc(1, sizeof(i2s_keep_t));
    if (i2s_keep[port] == NULL) {
        return -1;
    }
    int ret = i2s_new_channel(&chan_cfg, &i2s_keep[port]->tx_handle, &i2s_keep[port]->rx_handle);
    if (i2s_out_mode == I2S_COMM_MODE_STD) {
        ret = i2s_channel_init_std_mode(i2s_keep[port]->tx_handle, &std_cfg);
    }
    if (i2s_in_mode == I2S_COMM_MODE_STD) {
        ret = i2s_channel_init_std_mode(i2s_keep[port]->rx_handle, &std_cfg);
    }
    i2s_channel_enable(i2s_keep[port]->tx_handle);
    i2s_channel_enable(i2s_keep[port]->rx_handle);
#else
    i2s_config_t i2s_config = {
        .mode = (i2s_mode_t)(I2S_MODE_TX | I2S_MODE_RX | I2S_MODE_MASTER),
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
        .mck_io_num = AUDIO_I2S_GPIO_MCLK,
        .bck_io_num = AUDIO_I2S_GPIO_BCLK,
        .ws_io_num = AUDIO_I2S_GPIO_WS,
        .data_out_num = AUDIO_I2S_GPIO_DOUT,
        .data_in_num = AUDIO_I2S_GPIO_DIN,
    };
    i2s_set_pin(port, &i2s_pin_cfg);
#endif
    return ret;
}

static int ut_i2s_deinit(uint8_t port)
{
#if USE_IDF5
    if (port >= I2S_MAX_KEEP) {
        return -1;
    }
    if (i2s_keep[port] == NULL) {
        return 0;
    }
    i2s_channel_disable(i2s_keep[port]->tx_handle);
    i2s_channel_disable(i2s_keep[port]->rx_handle);
    i2s_del_channel(i2s_keep[port]->tx_handle);
    i2s_del_channel(i2s_keep[port]->rx_handle);
    free(i2s_keep[port]);
    i2s_keep[port] = NULL;
#else
    i2s_driver_uninstall(port);
#endif
    return 0;
}

static int m5ioe1_write_reg(i2c_master_dev_handle_t dev, uint8_t reg, uint8_t value)
{
    uint8_t buf[2] = { reg, value };
    return i2c_master_transmit(dev, buf, sizeof(buf), -1);
}

static int m5ioe1_read_reg(i2c_master_dev_handle_t dev, uint8_t reg, uint8_t *value)
{
    return i2c_master_transmit_receive(dev, &reg, 1, value, 1, -1);
}

static int m5ioe1_update_reg(i2c_master_dev_handle_t dev, uint8_t reg, uint8_t mask, bool set)
{
    uint8_t value = 0;
    if (m5ioe1_read_reg(dev, reg, &value) != ESP_OK) {
        return -1;
    }
    if (set) {
        value |= mask;
    } else {
        value &= (uint8_t)~mask;
    }
    return m5ioe1_write_reg(dev, reg, value);
}

#ifdef USE_IDF_I2C_MASTER
static i2c_master_dev_handle_t m5ioe1_dev_open(void)
{
    i2c_device_config_t i2c_dev_conf = {
        .dev_addr_length = I2C_ADDR_BIT_LEN_7,
        .scl_speed_hz = 100000,
        .device_address = M5IOE1_I2C_ADDR,
    };
    i2c_master_dev_handle_t dev_handle = NULL;
    if (i2c_bus_handle == NULL) {
        ESP_LOGE(TAG, "m5ioe1: i2c bus not ready");
        return NULL;
    }
    if (i2c_master_bus_add_device(i2c_bus_handle, &i2c_dev_conf, &dev_handle) != ESP_OK) {
        ESP_LOGE(TAG, "m5ioe1: i2c add device failed");
    }
    return dev_handle;
}

static void m5ioe1_dev_close(i2c_master_dev_handle_t dev)
{
    if (dev) {
        i2c_master_bus_rm_device(dev);
    }
}
#endif

// M5IOE1 pin mode / default level — same as M5Unified board_M5ChainCaptain boot init
static void m5ioe1_gpio_init_once(void)
{
#ifdef USE_IDF_I2C_MASTER
    if (m5ioe1_gpio_inited) {
        return;
    }
    i2c_master_dev_handle_t dev = m5ioe1_dev_open();
    if (dev == NULL) {
        return;
    }
    m5ioe1_write_reg(dev, M5IOE1_REG_I2C_CFG, 0x00);
    m5ioe1_update_reg(dev, M5IOE1_REG_GPIO_DRV_L, M5IOE1_G5_AUDIO_PWR, false);
    m5ioe1_update_reg(dev, M5IOE1_REG_GPIO_MODE_L, M5IOE1_G5_AUDIO_PWR, true);
    m5ioe1_update_reg(dev, M5IOE1_REG_GPIO_OUT_L, M5IOE1_G5_AUDIO_PWR, false);
    gpio_reset_pin(AUDIO_CODEC_GPIO_PA);
    gpio_set_direction(AUDIO_CODEC_GPIO_PA, GPIO_MODE_OUTPUT);
    gpio_set_level(AUDIO_CODEC_GPIO_PA, 0);
    m5ioe1_gpio_inited = true;
    m5ioe1_dev_close(dev);
#else
    #error "Not implemented"
#endif
}

// G5: codec / audio power (output level only)
static void m5ioe1_codec_power_set(bool on)
{
#ifdef USE_IDF_I2C_MASTER
    if (!m5ioe1_gpio_inited) {
        m5ioe1_gpio_init_once();
    }
    i2c_master_dev_handle_t dev = m5ioe1_dev_open();
    if (dev == NULL) {
        return;
    }
    m5ioe1_update_reg(dev, M5IOE1_REG_GPIO_OUT_L, M5IOE1_G5_AUDIO_PWR, on);
    m5ioe1_dev_close(dev);
#else
    #error "Not implemented"
#endif
}

// GPIO21: AW8737A PA enable (runtime toggle via Speaker.setPA in Python)
static void m5ioe1_pa_set(bool on)
{
    if (!m5ioe1_gpio_inited) {
        m5ioe1_gpio_init_once();
    }
    gpio_set_level(AUDIO_CODEC_GPIO_PA, on ? 1 : 0);
}

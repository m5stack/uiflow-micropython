#include "board_init.h"
#include "esp_log.h"
#include "driver/gpio.h"

static char *TAG = "s3_box_3_board";
static audio_hal_handle_t audio_hal = NULL;

#define AUDIO_CODEC_DEFAULT_CONFIG(){                   \
        .adc_input  = AUDIO_HAL_ADC_INPUT_LINE1,        \
        .dac_output = AUDIO_HAL_DAC_OUTPUT_ALL,         \
        .codec_mode = AUDIO_HAL_CODEC_MODE_BOTH,        \
        .i2s_iface = {                                  \
            .mode = AUDIO_HAL_MODE_SLAVE,               \
            .fmt = AUDIO_HAL_I2S_NORMAL,                \
            .samples = AUDIO_HAL_48K_SAMPLES,           \
            .bits = AUDIO_HAL_BIT_LENGTH_16BITS,        \
        },                                              \
};

audio_hal_handle_t board_codec_init(void)
{
    if (audio_hal) {
        return audio_hal;
    }
    ESP_LOGI(TAG, "init");
    audio_hal_codec_config_t audio_codec_cfg = AUDIO_CODEC_DEFAULT_CONFIG();
    audio_hal = audio_hal_init(&audio_codec_cfg, &AUDIO_CODEC_ES8311_DEFAULT_HANDLE);
    audio_hal_ctrl_codec(audio_hal, AUDIO_HAL_CODEC_MODE_DECODE, AUDIO_HAL_CTRL_START);

    audio_hal_handle_t adc_hal = audio_hal_init(&audio_codec_cfg, &AUDIO_CODEC_ES7210_DEFAULT_HANDLE);
    audio_hal_ctrl_codec(adc_hal, AUDIO_HAL_CODEC_MODE_ENCODE, AUDIO_HAL_CTRL_START);

    return audio_hal;
}

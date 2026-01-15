/*
* SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#if (ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(4, 2, 0) && ESP_IDF_VERSION < ESP_IDF_VERSION_VAL(5, 0, 0))
#include "driver/i2s.h"
#else
#include "driver/i2s_pdm.h"
#include "driver/i2s_tdm.h"
#include "driver/i2s_std.h"
#endif

#define BOARD_TASK_CORE (1)

// mp3 decoder
#define BOARD_MP3_DECODER_CONFIG() {                    \
    .out_rb_size        = MP3_DECODER_RINGBUFFER_SIZE,  \
    .task_stack         = MP3_DECODER_TASK_STACK_SIZE,  \
    .task_core          = BOARD_TASK_CORE,              \
    .task_prio          = MP3_DECODER_TASK_PRIO,        \
    .stack_in_ext       = true,                         \
}

// amr decoder
#define BOARD_AMR_DECODER_CONFIG() {                        \
        .out_rb_size        = AMR_DECODER_RINGBUFFER_SIZE,  \
        .task_stack         = AMR_DECODER_TASK_STACK_SIZE,  \
        .task_core          = BOARD_TASK_CORE,              \
        .task_prio          = AMR_DECODER_TASK_PRIO,        \
        .stack_in_ext       = true,                         \
    }

// wav decoder
#define BOARD_WAV_DECODER_CONFIG() {                    \
    .out_rb_size        = WAV_DECODER_RINGBUFFER_SIZE,  \
    .task_stack         = WAV_DECODER_TASK_STACK,       \
    .task_core          = BOARD_TASK_CORE,              \
    .task_prio          = WAV_DECODER_TASK_PRIO,        \
    .stack_in_ext       = true,                         \
}

// pcm decoder
#define BOARD_PCM_DECODER_CONFIG() {                    \
    .out_rb_size        = PCM_DECODER_RINGBUFFER_SIZE,  \
    .task_stack         = PCM_DECODER_TASK_STACK,       \
    .task_core          = BOARD_TASK_CORE,              \
    .task_prio          = PCM_DECODER_TASK_PRIO,        \
    .stack_in_ext       = true,                         \
    .rate               = 8000,                         \
    .bits               = 16,                           \
    .channels           = 1,                            \
}

// i2s stream
#if (ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(4, 2, 0) && ESP_IDF_VERSION < ESP_IDF_VERSION_VAL(5, 0, 0))
#define BOARD_I2S_STREAM_CFG_DEFAULT() {                                        \
    .type = AUDIO_STREAM_WRITER,                                                \
    .i2s_config = {                                                             \
        .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_RX),      \
        .sample_rate = 48000,                                                   \
        .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,                           \
        .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,                           \
        .communication_format = I2S_COMM_FORMAT_STAND_I2S,                      \
        .intr_alloc_flags = ESP_INTR_FLAG_LEVEL2 | ESP_INTR_FLAG_IRAM,          \
        .dma_buf_count = 3,                                                     \
        .dma_buf_len = 300,                                                     \
        .use_apll = true,                                                       \
        .tx_desc_auto_clear = true,                                             \
        .fixed_mclk = 0                                                         \
    },                                                                          \
    .i2s_port = I2S_NUM_0,                                                      \
    .use_alc = false,                                                           \
    .volume = 0,                                                                \
    .out_rb_size = I2S_STREAM_RINGBUFFER_SIZE,                                  \
    .task_stack = I2S_STREAM_TASK_STACK,                                        \
    .task_core = BOARD_TASK_CORE,                                               \
    .task_prio = I2S_STREAM_TASK_PRIO,                                          \
    .stack_in_ext = false,                                                      \
    .multi_out_num = 0,                                                         \
    .uninstall_drv = false,                                                     \
    .need_expand = false,                                                       \
    .expand_src_bits = I2S_BITS_PER_SAMPLE_16BIT,                               \
    .buffer_len = I2S_STREAM_BUF_SIZE,                                          \
}
#else
#define BOARD_I2S_STREAM_CFG_DEFAULT() {                                        \
    .type = AUDIO_STREAM_WRITER,                                                \
    .std_cfg = {                                                                \
        .clk_cfg  = I2S_STD_CLK_DEFAULT_CONFIG(48000),                          \
        .slot_cfg = I2S_STD_PHILIPS_SLOT_DEFAULT_ADF_CONFIG(I2S_DATA_BIT_WIDTH_16BIT, I2S_SLOT_MODE_STEREO),     \
        .gpio_cfg = {                                                           \
            .invert_flags = {                                                   \
                .mclk_inv = false,                                              \
                .bclk_inv = false,                                              \
            },                                                                  \
        },                                                                      \
    },                                                                          \
    .transmit_mode = I2S_COMM_MODE_STD,                                         \
    .chan_cfg = {                                                               \
        .id = I2S_NUM_0,                                                        \
        .role = I2S_ROLE_MASTER,                                                \
        .dma_desc_num = 3,                                                      \
        .dma_frame_num = 300,                                                   \
        .auto_clear = true,                                                     \
    },                                                                          \
    .use_alc = false,                                                           \
    .volume = 0,                                                                \
    .out_rb_size = I2S_STREAM_RINGBUFFER_SIZE,                                  \
    .task_stack = I2S_STREAM_TASK_STACK,                                        \
    .task_core = BOARD_TASK_CORE,                                               \
    .task_prio = I2S_STREAM_TASK_PRIO,                                          \
    .stack_in_ext = false,                                                      \
    .multi_out_num = 0,                                                         \
    .uninstall_drv = false,                                                     \
    .need_expand = false,                                                       \
    .expand_src_bits = I2S_DATA_BIT_WIDTH_16BIT,                                \
    .buffer_len = I2S_STREAM_BUF_SIZE,                                          \
}
#endif

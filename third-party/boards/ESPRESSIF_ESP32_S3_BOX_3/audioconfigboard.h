/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

// mp3 decoder
#define BOARD_MP3_DECODER_CONFIG() {                  \
    .out_rb_size        = MP3_DECODER_RINGBUFFER_SIZE,  \
    .task_stack         = MP3_DECODER_TASK_STACK_SIZE,  \
    .task_core          = 1,                            \
    .task_prio          = MP3_DECODER_TASK_PRIO,        \
    .stack_in_ext       = true,                         \
}

// amr decoder
#define BOARD_AMR_DECODER_CONFIG() {                        \
        .out_rb_size        = AMR_DECODER_RINGBUFFER_SIZE,  \
        .task_stack         = AMR_DECODER_TASK_STACK_SIZE,  \
        .task_core          = 1,                            \
        .task_prio          = AMR_DECODER_TASK_PRIO,        \
        .stack_in_ext       = true,                         \
    }

// wav decoder
#define BOARD_WAV_DECODER_CONFIG() {                    \
    .out_rb_size        = WAV_DECODER_RINGBUFFER_SIZE,  \
    .task_stack         = WAV_DECODER_TASK_STACK,       \
    .task_core          = 1,                            \
    .task_prio          = WAV_DECODER_TASK_PRIO,        \
    .stack_in_ext       = true,                         \
}

// pcm decoder
#define BOARD_PCM_DECODER_CONFIG() {                    \
    .out_rb_size        = PCM_DECODER_RINGBUFFER_SIZE,  \
    .task_stack         = PCM_DECODER_TASK_STACK,       \
    .task_core          = 1,                            \
    .task_prio          = PCM_DECODER_TASK_PRIO,        \
    .stack_in_ext       = true,                         \
    .rate               = 8000,                         \
    .bits               = 16,                           \
    .channels           = 1,                            \
}

// i2s stream
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
    .task_core = 1,                                                             \
    .task_prio = I2S_STREAM_TASK_PRIO,                                          \
    .stack_in_ext = false,                                                      \
    .multi_out_num = 0,                                                         \
    .uninstall_drv = true,                                                      \
    .need_expand = false,                                                       \
    .expand_src_bits = I2S_BITS_PER_SAMPLE_16BIT,                               \
    .buffer_len = I2S_STREAM_BUF_SIZE,                                          \
}

/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>

typedef struct _mp_mic_config_t {
    mp_obj_base_t base;
    mp_obj_t pin_data_in;
    mp_obj_t pin_bck;
    mp_obj_t pin_mck;
    mp_obj_t pin_ws;
    mp_obj_t sample_rate;
    mp_obj_t stereo;
    mp_obj_t input_offset;
    mp_obj_t over_sampling;
    mp_obj_t magnification;
    mp_obj_t noise_filter_level;
    mp_obj_t use_adc;
    mp_obj_t dma_buf_len;
    mp_obj_t dma_buf_count;
    mp_obj_t task_priority;
    mp_obj_t task_pinned_core;
    mp_obj_t i2s_port;
} mp_mic_config_t;

extern const mp_obj_type_t mp_mic_config_t_type;

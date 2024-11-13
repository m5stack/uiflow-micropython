/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "mic_config_t.h"

/* *FORMAT-OFF* */

static mp_obj_t mic_config_t_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_mic_config_t *self = m_new_obj(mp_mic_config_t);
    self->base.type = &mp_mic_config_t_type;
    self->pin_data_in = mp_obj_new_int(-1);
    self->pin_bck = mp_obj_new_int(-1);
    self->pin_mck = mp_obj_new_int(-1);
    self->pin_ws = mp_obj_new_int(-1);
    self->sample_rate = mp_obj_new_int(16000);
    self->stereo = mp_obj_new_bool(false);
    self->input_offset = mp_obj_new_int(0);
    self->over_sampling = mp_obj_new_int(2);
    self->magnification = mp_obj_new_int(16);
    self->noise_filter_level = mp_obj_new_int(0);
    self->use_adc = mp_obj_new_bool(false);
    self->dma_buf_len = mp_obj_new_int(256);
    self->dma_buf_count = mp_obj_new_int(3);
    self->task_priority = mp_obj_new_int(2);
    self->task_pinned_core = mp_obj_new_int(-1);
    self->i2s_port = mp_obj_new_int(0);
    return MP_OBJ_FROM_PTR(self);
}

static void mic_config_t_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) {
    mp_mic_config_t *self = (mp_mic_config_t *)MP_OBJ_TO_PTR(self_in);
    if (dest[0] == MP_OBJ_NULL) {
        // Load
        if (attr == MP_QSTR_pin_data_in) {
            dest[0] = self->pin_data_in;
        } else if (attr == MP_QSTR_pin_bck) {
            dest[0] = self->pin_bck;
        } else if (attr == MP_QSTR_pin_mck) {
            dest[0] = self->pin_mck;
        } else if (attr == MP_QSTR_pin_ws) {
            dest[0] = self->pin_ws;
        } else if (attr == MP_QSTR_sample_rate) {
            dest[0] = self->sample_rate;
        } else if (attr == MP_QSTR_stereo) {
            dest[0] = self->stereo;
        } else if (attr == MP_QSTR_input_offset) {
            dest[0] = self->input_offset;
        } else if (attr == MP_QSTR_over_sampling) {
            dest[0] = self->over_sampling;
        } else if (attr == MP_QSTR_magnification) {
            dest[0] = self->magnification;
        } else if (attr == MP_QSTR_noise_filter_level) {
            dest[0] = self->noise_filter_level;
        } else if (attr == MP_QSTR_use_adc) {
            dest[0] = self->use_adc;
        } else if (attr == MP_QSTR_dma_buf_len) {
            dest[0] = self->dma_buf_len;
        } else if (attr == MP_QSTR_dma_buf_count) {
            dest[0] = self->dma_buf_count;
        } else if (attr == MP_QSTR_task_priority) {
            dest[0] = self->task_priority;
        } else if (attr == MP_QSTR_task_pinned_core) {
            dest[0] = self->task_pinned_core;
        } else if (attr == MP_QSTR_i2s_port) {
            dest[0] = self->i2s_port;
        }
    } else if (dest[1] != MP_OBJ_NULL) {
        // Store
        if (attr == MP_QSTR_pin_data_in) {
            self->pin_data_in = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_pin_bck) {
            self->pin_bck = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_pin_mck) {
            self->pin_mck = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_pin_ws) {
            self->pin_ws = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_sample_rate) {
            self->sample_rate = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_stereo) {
            self->stereo = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_input_offset) {
            self->input_offset = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_over_sampling) {
            self->over_sampling = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_magnification) {
            self->magnification = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_noise_filter_level) {
            self->noise_filter_level = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_use_adc) {
            self->use_adc = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_dma_buf_len) {
            self->dma_buf_len = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_dma_buf_count) {
            self->dma_buf_count = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_task_priority) {
            self->task_priority = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_task_pinned_core) {
            self->task_pinned_core = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_i2s_port) {
            self->i2s_port = dest[1];
            dest[0] = MP_OBJ_NULL;
        }
    }
}

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_mic_config_t_type,
    MP_QSTR_mic_config_t,
    MP_TYPE_FLAG_NONE,
    make_new, mic_config_t_make_new,
    attr, mic_config_t_attr
);
#else
const mp_obj_type_t mp_mic_config_t_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_mic_config_t,
    .make_new = mic_config_t_make_new,
    .attr = mic_config_t_attr,
};
#endif

/* *FORMAT-ON* */

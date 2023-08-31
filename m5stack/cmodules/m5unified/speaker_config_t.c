#include "speaker_config_t.h"

/* *FORMAT-OFF* */

STATIC mp_obj_t speaker_config_t_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_speaker_config_t *self = m_new_obj(mp_speaker_config_t);
    self->base.type = &mp_speaker_config_t_type;
    self->pin_data_out = mp_obj_new_int(-1);
    self->pin_bck = mp_obj_new_int(-1);
    self->pin_ws = mp_obj_new_int(-1);
    self->sample_rate = mp_obj_new_int(64000);
    self->stereo = mp_obj_new_bool(false);
    self->buzzer = mp_obj_new_bool(false);
    self->use_dac = mp_obj_new_int(2);
    self->dac_zero_level = mp_obj_new_int(0);
    self->magnification = mp_obj_new_int(16);
    self->dma_buf_len = mp_obj_new_bool(256);
    self->dma_buf_count = mp_obj_new_int(8);
    self->task_priority = mp_obj_new_int(2);
    self->task_pinned_core = mp_obj_new_int(255);
    self->i2s_port = mp_obj_new_int(0);
    return MP_OBJ_FROM_PTR(self);
}

STATIC void speaker_config_t_attr(mp_obj_t self_in, qstr attr, mp_obj_t *dest) {
    mp_speaker_config_t *self = (mp_speaker_config_t *)MP_OBJ_TO_PTR(self_in);
    if (dest[0] == MP_OBJ_NULL) {
        // Load
        if (attr == MP_QSTR_pin_data_out) {
            dest[0] = self->pin_data_out;
        } else if (attr == MP_QSTR_pin_bck) {
            dest[0] = self->pin_bck;
        } else if (attr == MP_QSTR_pin_ws) {
            dest[0] = self->pin_ws;
        } else if (attr == MP_QSTR_sample_rate) {
            dest[0] = self->sample_rate;
        } else if (attr == MP_QSTR_stereo) {
            dest[0] = self->stereo;
        } else if (attr == MP_QSTR_buzzer) {
            dest[0] = self->buzzer;
        } else if (attr == MP_QSTR_use_dac) {
            dest[0] = self->use_dac;
        } else if (attr == MP_QSTR_dac_zero_level) {
            dest[0] = self->dac_zero_level;
        } else if (attr == MP_QSTR_magnification) {
            dest[0] = self->magnification;
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
        if (attr == MP_QSTR_pin_data_out) {
            self->pin_data_out = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_pin_bck) {
            self->pin_bck = dest[1];
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
        } else if (attr == MP_QSTR_buzzer) {
            self->buzzer = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_use_dac) {
            self->use_dac = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_dac_zero_level) {
            self->dac_zero_level = dest[1];
            dest[0] = MP_OBJ_NULL;
        } else if (attr == MP_QSTR_magnification) {
            self->magnification = dest[1];
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
    mp_speaker_config_t_type,
    MP_QSTR_speaker_config_t,
    MP_TYPE_FLAG_NONE,
    make_new, speaker_config_t_make_new,
    attr, speaker_config_t_attr
);
#else
const mp_obj_type_t mp_speaker_config_t_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_speaker_config_t,
    .make_new = speaker_config_t_make_new,
    .attr = speaker_config_t_attr,
};
#endif

/* *FORMAT-ON* */

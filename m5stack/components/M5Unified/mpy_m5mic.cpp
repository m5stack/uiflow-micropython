#include <M5Unified.h>

extern "C"
{
#include "mpy_m5mic.h"
#include "mic_config_t.h"

namespace m5
{
    static inline Mic_Class *getMic(const mp_obj_t *args) {
        return (Mic_Class *)(((mic_obj_t *)MP_OBJ_TO_PTR(args[0]))->mic);
    }

    mp_obj_t mic_config(size_t n_args, const mp_obj_t *args, mp_map_t *kwargs) {
        Mic_Class *mic = getMic(&args[0]);
        mic_config_t cfg = mic->config();
        if (n_args == 1) {

            // Set config iterm
            if (kwargs->used != 0) {
                for (size_t i = 0; i < kwargs->alloc; i++) {
                    if (mp_map_slot_is_filled(kwargs, i)) {
                        switch (mp_obj_str_get_qstr(kwargs->table[i].key)) {
                            case MP_QSTR_pin_data_in:
                                cfg.pin_data_in = (int)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_pin_bck:
                                cfg.pin_bck = (int)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_pin_mck:
                                cfg.pin_mck = (int)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_pin_ws:
                                cfg.pin_ws = (int)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_sample_rate:
                                cfg.sample_rate = (uint32_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_stereo:
                                cfg.stereo = (bool)mp_obj_is_true(kwargs->table[i].value);
                            break;

                            case MP_QSTR_input_offset:
                                cfg.input_offset = (int)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_over_sampling:
                                cfg.over_sampling = (uint8_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_magnification:
                                cfg.magnification = (uint8_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_noise_filter_level:
                                cfg.noise_filter_level = (uint8_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_use_adc:
                                cfg.use_adc = (bool)mp_obj_is_true(kwargs->table[i].value);
                            break;

                            case MP_QSTR_dma_buf_len:
                                cfg.dma_buf_len = (size_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_dma_buf_count:
                                cfg.dma_buf_count = (size_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_task_priority:
                                cfg.task_priority = (uint8_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_task_pinned_core:
                                cfg.task_pinned_core = (uint8_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_i2s_port:
                                cfg.i2s_port = (i2s_port_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            default:
                                goto unknown;
                        }
                    }
                }
                mic->config(cfg);
                return mp_const_none;
            }

            // Get all config
            mp_mic_config_t *config = m_new_obj(mp_mic_config_t);
            config->base.type = &mp_mic_config_t_type;
            config->pin_data_in = mp_obj_new_int(cfg.pin_data_in);
            config->pin_bck = mp_obj_new_int(cfg.pin_bck);
            config->pin_mck = mp_obj_new_int(cfg.pin_mck);
            config->pin_ws = mp_obj_new_int(cfg.pin_ws);
            config->sample_rate = mp_obj_new_int(cfg.sample_rate);
            config->stereo = mp_obj_new_bool(cfg.stereo);
            config->input_offset = mp_obj_new_int(cfg.input_offset);
            config->over_sampling = mp_obj_new_int(cfg.over_sampling);
            config->magnification = mp_obj_new_int(cfg.magnification);
            config->noise_filter_level = mp_obj_new_int(cfg.noise_filter_level);
            config->use_adc = mp_obj_new_bool(cfg.use_adc);
            config->dma_buf_len = mp_obj_new_int(cfg.dma_buf_len);
            config->dma_buf_count = mp_obj_new_int(cfg.dma_buf_count);
            config->task_priority = mp_obj_new_int(cfg.task_priority);
            config->task_pinned_core = mp_obj_new_int(cfg.task_pinned_core);
            config->i2s_port = mp_obj_new_int(cfg.i2s_port);
            return MP_OBJ_FROM_PTR(config);
        } else if (n_args == 2) {
            if (mp_obj_is_str(args[1])) {
                // Get config iterm
                switch (mp_obj_str_get_qstr(args[1])) {
                    case MP_QSTR_pin_data_in:
                        return mp_obj_new_int(cfg.pin_data_in);
                    break;

                    case MP_QSTR_pin_bck:
                        return mp_obj_new_int(cfg.pin_bck);
                    break;

                    case MP_QSTR_pin_mck:
                        return mp_obj_new_int(cfg.pin_mck);
                    break;

                    case MP_QSTR_pin_ws:
                        return mp_obj_new_int(cfg.pin_ws);
                    break;

                    case MP_QSTR_sample_rate:
                        return mp_obj_new_int(cfg.sample_rate);
                    break;

                    case MP_QSTR_stereo:
                        return mp_obj_new_bool(cfg.stereo);
                    break;

                    case MP_QSTR_input_offset:
                        return mp_obj_new_int(cfg.input_offset);
                    break;

                    case MP_QSTR_over_sampling:
                        return mp_obj_new_int(cfg.over_sampling);
                    break;

                    case MP_QSTR_magnification:
                        return mp_obj_new_int(cfg.magnification);
                    break;

                    case MP_QSTR_noise_filter_level:
                        return mp_obj_new_int(cfg.noise_filter_level);
                    break;

                    case MP_QSTR_use_adc:
                        return mp_obj_new_bool(cfg.use_adc);
                    break;

                    case MP_QSTR_dma_buf_len:
                        return mp_obj_new_int(cfg.dma_buf_len);
                    break;

                    case MP_QSTR_dma_buf_count:
                        return mp_obj_new_int(cfg.dma_buf_count);
                    break;

                    case MP_QSTR_task_priority:
                        return mp_obj_new_int(cfg.task_priority);
                    break;

                    case MP_QSTR_task_pinned_core:
                        return mp_obj_new_int(cfg.task_pinned_core);
                    break;

                    case MP_QSTR_i2s_port:
                        return mp_obj_new_int(cfg.i2s_port);
                    break;

                    default:
                        goto unknown;
                }
            } else if (mp_obj_is_type(MP_OBJ_TO_PTR(args[1]), &mp_mic_config_t_type)) {
                // Set all config
                mp_mic_config_t *config = (mp_mic_config_t *)MP_OBJ_TO_PTR(args[1]);
                cfg.pin_data_in = (int)mp_obj_get_int(config->pin_data_in);
                cfg.pin_bck = (int)mp_obj_get_int(config->pin_bck);
                cfg.pin_mck = (int)mp_obj_get_int(config->pin_mck);
                cfg.pin_ws = (int)mp_obj_get_int(config->pin_ws);
                cfg.sample_rate = (uint32_t)mp_obj_get_int(config->sample_rate);
                cfg.stereo = (bool)mp_obj_is_true(config->stereo);
                cfg.input_offset = (int)mp_obj_get_int(config->input_offset);
                cfg.over_sampling = (uint8_t)mp_obj_get_int(config->over_sampling);
                cfg.magnification = (uint8_t)mp_obj_get_int(config->magnification);
                cfg.noise_filter_level = (uint8_t)mp_obj_get_int(config->noise_filter_level);
                cfg.use_adc = (bool)mp_obj_is_true(config->use_adc);
                cfg.dma_buf_len = (size_t)mp_obj_get_int(config->dma_buf_len);
                cfg.dma_buf_count = (size_t)mp_obj_get_int(config->dma_buf_count);
                cfg.task_priority = (uint8_t)mp_obj_get_int(config->task_priority);
                cfg.task_pinned_core = (uint8_t)mp_obj_get_int(config->task_pinned_core);
                cfg.i2s_port = (i2s_port_t)mp_obj_get_int(config->i2s_port);
                mic->config(cfg);
                return mp_const_none;
            }
        }
        return mp_const_none;

    unknown:
        mp_raise_ValueError(MP_ERROR_TEXT("unknown config param"));
    }

    mp_obj_t mic_begin(mp_obj_t self) {
        return mp_obj_new_bool(getMic(&self)->begin());
    }

    mp_obj_t mic_end(mp_obj_t self) {
        getMic(&self)->end();
        return mp_const_none;
    }

    mp_obj_t mic_isRunning(mp_obj_t self) {
        return mp_obj_new_bool(getMic(&self)->isRunning());
    }

    mp_obj_t mic_isEnabled(mp_obj_t self) {
        return mp_obj_new_bool(getMic(&self)->isEnabled());
    }

    mp_obj_t mic_isRecording(mp_obj_t self) {
        return mp_obj_new_int(getMic(&self)->isRecording());
    }

    mp_obj_t mic_setSampleRate(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_rate};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_rate, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 8000 } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getMic(&pos_args[0])->setSampleRate(args[ARG_rate].u_int);
        return mp_const_none;
    }

    mp_obj_t mic_record(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_buf, ARG_rate, ARG_stereo};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_buf,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = MP_OBJ_NULL }     },
            { MP_QSTR_rate,   MP_ARG_INT,                   {.u_int = 16000 }           },
            { MP_QSTR_stereo, MP_ARG_BOOL,                  {.u_bool = mp_const_false } },
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Power object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[ARG_buf].u_obj, &bufinfo, MP_BUFFER_WRITE);

        int16_t *rec_data = (int16_t *)bufinfo.buf;
        size_t array_len = bufinfo.len / 2;

        bool ret = getMic(&pos_args[0])->record(
            rec_data,
            array_len,
            args[ARG_rate].u_int,
            args[ARG_stereo].u_bool
            );
        return mp_obj_new_bool(ret);
    }

}
}

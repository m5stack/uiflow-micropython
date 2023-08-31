#include <M5Unified.h>

extern "C"
{
#include "mpy_m5spk.h"
#include "speaker_config_t.h"

namespace m5
{
    static inline Speaker_Class *getSpk(const mp_obj_t *args) {
        return (Speaker_Class *)(((spk_obj_t *)MP_OBJ_TO_PTR(args[0]))->spk);
    }

    mp_obj_t spk_config(size_t n_args, const mp_obj_t *args, mp_map_t *kwargs) {
        Speaker_Class *speaker = getSpk(&args[0]);
        speaker_config_t cfg = speaker->config();
        if (n_args == 1) {
            // Set config iterm
            if (kwargs->used != 0) {
                for (size_t i = 0; i < kwargs->alloc; i++) {
                    if (mp_map_slot_is_filled(kwargs, i)) {
                        switch (mp_obj_str_get_qstr(kwargs->table[i].key)) {
                            case MP_QSTR_pin_data_out:
                                cfg.pin_data_out = (int)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_pin_bck:
                                cfg.pin_bck = (int)mp_obj_get_int(kwargs->table[i].value);
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

                            case MP_QSTR_buzzer:
                                cfg.buzzer = (bool)mp_obj_is_true(kwargs->table[i].value);
                            break;

                            case MP_QSTR_use_dac:
                                cfg.use_dac = (bool)mp_obj_is_true(kwargs->table[i].value);
                            break;

                            case MP_QSTR_dac_zero_level:
                                cfg.dac_zero_level = (uint8_t)mp_obj_get_int(kwargs->table[i].value);
                            break;

                            case MP_QSTR_magnification:
                                cfg.magnification = (uint8_t)mp_obj_get_int(kwargs->table[i].value);
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
                speaker->config(cfg);
                return mp_const_none;
            }

            // Get all config iterm
            speaker_config_t cfg = speaker->config();
            mp_speaker_config_t *config = m_new_obj(mp_speaker_config_t);
            config->base.type = &mp_speaker_config_t_type;
            config->pin_data_out = mp_obj_new_int(cfg.pin_data_out);
            config->pin_bck = mp_obj_new_int(cfg.pin_bck);
            config->pin_ws = mp_obj_new_int(cfg.pin_ws);
            config->sample_rate = mp_obj_new_int(cfg.sample_rate);
            config->stereo = mp_obj_new_bool(cfg.stereo);
            config->buzzer = mp_obj_new_bool(cfg.buzzer);
            config->use_dac = mp_obj_new_bool(cfg.use_dac);
            config->dac_zero_level = mp_obj_new_int(cfg.dac_zero_level);
            config->magnification = mp_obj_new_int(cfg.magnification);
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
                    case MP_QSTR_pin_data_out:
                        return mp_obj_new_int(cfg.pin_data_out);
                    break;

                    case MP_QSTR_pin_bck:
                        return mp_obj_new_int(cfg.pin_bck);
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

                    case MP_QSTR_buzzer:
                        return mp_obj_new_bool(cfg.buzzer);
                    break;

                    case MP_QSTR_use_dac:
                        return mp_obj_new_bool(cfg.use_dac);
                    break;

                    case MP_QSTR_dac_zero_level:
                        return mp_obj_new_int(cfg.dac_zero_level);
                    break;

                    case MP_QSTR_magnification:
                        return mp_obj_new_int(cfg.magnification);
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
            } else if (mp_obj_is_type(MP_OBJ_TO_PTR(args[1]), &mp_speaker_config_t_type)) {
                // Set all config iterm
                mp_speaker_config_t *config = (mp_speaker_config_t *)MP_OBJ_TO_PTR(args[1]);
                cfg.pin_data_out = (int)mp_obj_get_int(config->pin_data_out);
                cfg.pin_bck = (int)mp_obj_get_int(config->pin_bck);
                cfg.pin_ws = (int)mp_obj_get_int(config->pin_ws);
                cfg.sample_rate = (uint32_t)mp_obj_get_int(config->sample_rate);
                cfg.stereo = (bool)mp_obj_is_true(config->stereo);
                cfg.buzzer = (bool)mp_obj_is_true(config->buzzer);
                cfg.use_dac = (bool)mp_obj_is_true(config->use_dac);
                cfg.dac_zero_level = (uint8_t)mp_obj_get_int(config->dac_zero_level);
                cfg.magnification = (uint8_t)mp_obj_get_int(config->magnification);
                cfg.dma_buf_len = (size_t)mp_obj_get_int(config->dma_buf_len);
                cfg.dma_buf_count = (size_t)mp_obj_get_int(config->dma_buf_count);
                cfg.task_priority = (uint8_t)mp_obj_get_int(config->task_priority);
                cfg.task_pinned_core = (uint8_t)mp_obj_get_int(config->task_pinned_core);
                cfg.i2s_port = (i2s_port_t)mp_obj_get_int(config->i2s_port);
                speaker->config(cfg);
                return mp_const_none;
            }
        }
        return mp_const_none;
    unknown:
        mp_raise_ValueError(MP_ERROR_TEXT("unknown config param"));
    }

    mp_obj_t spk_begin(mp_obj_t self) {
        return mp_obj_new_bool(getSpk(&self)->begin());
    }

    mp_obj_t spk_end(mp_obj_t self) {
        getSpk(&self)->end();
        return mp_const_none;
    }

    mp_obj_t spk_isRunning(mp_obj_t self) {
        return mp_obj_new_bool(getSpk(&self)->isRunning());
    }

    mp_obj_t spk_isEnabled(mp_obj_t self) {
        return mp_obj_new_bool(getSpk(&self)->isEnabled());
    }

    mp_obj_t spk_isPlaying(size_t n_args, const mp_obj_t *args) {
        Speaker_Class *speaker = getSpk(&args[0]);
        if (n_args == 1) {
            return mp_obj_new_bool(speaker->isPlaying());
        } else if (n_args == 2) {
            uint8_t channel = (uint8_t)mp_obj_get_int(args[1]);
            return mp_obj_new_int(speaker->isPlaying(channel));
        }
        return mp_const_none;
    }

    mp_obj_t spk_getPlayingChannels(mp_obj_t self) {
        return mp_obj_new_int(getSpk(&self)->getPlayingChannels());
    }

    mp_obj_t spk_setVolume(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_master_volume};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_master_volume, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0} }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->setVolume(args[ARG_master_volume].u_int);
        return mp_const_none;
    }

    mp_obj_t spk_getVolume(mp_obj_t self) {
        return mp_obj_new_int(getSpk(&self)->getVolume());
    }

    mp_obj_t spk_setVolumePercentage(mp_obj_t self_in, mp_obj_t percentage_in) {
        float percentage = mp_obj_get_float(percentage_in);
        if (percentage > 1.0) {
            percentage = 1.0;
        }
        if (percentage < 0.0) {
            percentage = 0.0;
        }

        getSpk(&self_in)->setVolume(percentage * 255);
        return mp_const_none;
    }

    mp_obj_t spk_getVolumePercentage(mp_obj_t self) {
        uint8_t volume = getSpk(&self)->getVolume();
        return mp_obj_new_float(volume / 255);
    }

    mp_obj_t spk_setAllChannelVolume(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_volume};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_volume, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0} }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->setAllChannelVolume(args[ARG_volume].u_int);
        return mp_const_none;
    }

    mp_obj_t spk_setChannelVolume(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_channel, ARG_volume};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_channel, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0} },
            { MP_QSTR_volume,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0} }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->setChannelVolume(
            args[ARG_channel].u_int,
            args[ARG_volume].u_int
            );
        return mp_const_none;
    }

    mp_obj_t spk_getChannelVolume(mp_obj_t self, mp_obj_t ch) {
        return mp_obj_new_int(getSpk(&self)->getChannelVolume(mp_obj_get_int(ch)));
    }

    mp_obj_t spk_stop(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_channel};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_channel, MP_ARG_INT, {.u_int = 0 } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        if (n_args == 1) {
            getSpk(&pos_args[0])->stop();
        } else if (n_args == 2) {
            getSpk(&pos_args[0])->stop(args[ARG_channel].u_int);
        }
        return mp_const_none;
    }

    mp_obj_t spk_tone(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_frequency, ARG_duration, ARG_channel, ARG_stop_current_sound};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_frequency,          MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0}              },
            { MP_QSTR_duration,           MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0}              },
            { MP_QSTR_channel,            MP_ARG_INT,                   {.u_int = 0}              },
            { MP_QSTR_stop_current_sound, MP_ARG_BOOL,                  {.u_bool = mp_const_true} },
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->tone(
            args[ARG_frequency].u_int,
            args[ARG_duration].u_int,
            args[ARG_channel].u_int,
            args[ARG_stop_current_sound].u_bool
            );
        return mp_const_none;
    }

    mp_obj_t spk_playRaw(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_raw, ARG_rate, ARG_stereo, ARG_repeat, ARG_channel, ARG_stop_current_sound};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_raw,                MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none  } },
            { MP_QSTR_rate,               MP_ARG_INT,                   {.u_int = 44100}           },
            { MP_QSTR_stereo,             MP_ARG_BOOL,                  {.u_bool = mp_const_false} },
            { MP_QSTR_repeat,             MP_ARG_INT,                   {.u_int = 1}               },
            { MP_QSTR_channel,            MP_ARG_INT,                   {.u_int = -1}              },
            { MP_QSTR_stop_current_sound, MP_ARG_BOOL,                  {.u_bool = mp_const_false} },
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[ARG_raw].u_obj, &bufinfo, MP_BUFFER_READ);

        const int16_t *raw_data = (const int16_t *)bufinfo.buf;
        size_t array_len = bufinfo.len / 2;
        // const uint8_t *raw_data = (const uint8_t *)bufinfo.buf;
        // size_t array_len = bufinfo.len;

        bool ret = getSpk(&pos_args[0])->playRaw(
            raw_data,
            array_len,
            args[ARG_rate].u_int,
            args[ARG_stereo].u_bool,
            args[ARG_repeat].u_int,
            args[ARG_channel].u_int,
            args[ARG_stop_current_sound].u_bool
            );
        return mp_obj_new_bool(ret);
    }

    mp_obj_t spk_playWav(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_wav_data, ARG_repeat, ARG_channel, ARG_stop_current_sound};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_wav_data,           MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none}  },
            { MP_QSTR_repeat,             MP_ARG_INT,                   {.u_int = 1}              },
            { MP_QSTR_ch,                 MP_ARG_INT,                   {.u_int = 0}              },
            { MP_QSTR_stop_current_sound, MP_ARG_BOOL,                  {.u_bool = mp_const_true} },
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[ARG_wav_data].u_obj, &bufinfo, MP_BUFFER_READ);

        getSpk(&pos_args[0])->playWav(
            (const uint8_t *)bufinfo.buf,
            bufinfo.len,
            args[ARG_repeat].u_int,
            args[ARG_channel].u_int,
            args[ARG_stop_current_sound].u_bool
            );
        return mp_const_none;
    }

}
}

#include <utility/Speaker_Class.hpp>

extern "C"
{
#include <string.h>
#include "cJSON.h"
#include "mpy_m5spk.h"

namespace m5
{
    static inline Speaker_Class *getSpk(const mp_obj_t *args) {
        return (Speaker_Class *)(((spk_obj_t *)MP_OBJ_TO_PTR(args[0]))->spk);
    }

    mp_obj_t spk_getVolume(mp_obj_t self) {
        return mp_obj_new_int(getSpk(&self)->getVolume());
    }

    mp_obj_t spk_getChannelVolume(mp_obj_t self, mp_obj_t ch) {
        return mp_obj_new_int(getSpk(&self)->getChannelVolume(mp_obj_get_int(ch)));
    }

    mp_obj_t spk_setVolume(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_vol};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_vol,     MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = 0 } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->setVolume(args[ARG_vol].u_int);
        return mp_const_none;
    }

    mp_obj_t spk_setChannelVolume(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_ch, ARG_vol};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_ch,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
            { MP_QSTR_vol, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->setChannelVolume(args[ARG_ch].u_int, args[ARG_vol].u_int);
        return mp_const_none;
    }

    mp_obj_t spk_setAllChannelVolume(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_vol};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_vol, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->setAllChannelVolume(args[ARG_vol].u_int);
        return mp_const_none;
    }

    mp_obj_t spk_tone(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_freq, ARG_msec, ARG_ch, ARG_stop};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_freq, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
            { MP_QSTR_msec, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
            { MP_QSTR_ch,   MP_ARG_INT                  , {.u_int = 0 } },
            { MP_QSTR_stop, MP_ARG_BOOL                 , {.u_bool = mp_const_true } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->tone(args[ARG_freq].u_int, args[ARG_msec].u_int
            , args[ARG_ch].u_int, args[ARG_stop].u_bool);
        return mp_const_none;
    }

    mp_obj_t spk_stop(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_ch};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_ch, MP_ARG_INT, {.u_int = 0 } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        getSpk(&pos_args[0])->stop(args[ARG_ch].u_int);
        return mp_const_none;
    }

    mp_obj_t spk_playWav(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_wav, ARG_repeat, ARG_ch, ARG_stop};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_wav,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
            { MP_QSTR_repeat, MP_ARG_INT                  , {.u_int = 1 } },
            { MP_QSTR_ch,     MP_ARG_INT                  , {.u_int = 0 } },
            { MP_QSTR_stop,   MP_ARG_BOOL                 , {.u_bool = mp_const_true } }
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[ARG_wav].u_obj, &bufinfo, MP_BUFFER_READ);

        getSpk(&pos_args[0])->playWav((const uint8_t *)bufinfo.buf, bufinfo.len
            , args[ARG_repeat].u_int, args[ARG_ch].u_int
            , args[ARG_stop].u_bool);
        return mp_const_none;
    }
/********************************Configuration*********************************/
    mp_obj_t spk_config(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_dout, ARG_bck, ARG_ws, ARG_sample_rate, ARG_stereo, ARG_buzzer,
              ARG_use_dac, ARG_dac_zero_level, ARG_magnification, ARG_dma_buf_len,
              ARG_dma_buf_count, ARG_task_priority, ARG_task_pinned_core, ARG_i2s_port};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_dout,             MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = -1 } },
            { MP_QSTR_bck,              MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = -1 } },
            { MP_QSTR_ws,               MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = -1 } },
            { MP_QSTR_sample_rate,      MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = 6400 } },
            { MP_QSTR_stereo,           MP_ARG_BOOL | MP_ARG_KW_ONLY, {.u_bool = mp_const_false } },
            { MP_QSTR_buzzer,           MP_ARG_BOOL | MP_ARG_KW_ONLY, {.u_bool = mp_const_false } },
            { MP_QSTR_use_dac,          MP_ARG_BOOL | MP_ARG_KW_ONLY, {.u_bool = mp_const_false } },
            { MP_QSTR_dac_zero_level,   MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = 0 } },
            { MP_QSTR_magnification,    MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = 16 } },
            { MP_QSTR_dma_buf_len,      MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = 256 } },
            { MP_QSTR_dma_buf_count,    MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = 8 } },
            { MP_QSTR_task_priority,    MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = 2 } },
            { MP_QSTR_task_pinned_core, MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = -1 } },
            { MP_QSTR_i2s_port,         MP_ARG_INT  | MP_ARG_KW_ONLY, {.u_int = 0 } },
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        // Read p ri v
        auto spk = getSpk(&pos_args[0]);
        auto cfg = spk->config();

        // Set config
        if (kw_args->used != 0) {
            for (size_t i = 0; i < kw_args->alloc; i++) {
                if (mp_map_slot_is_filled(kw_args, i)) {
                    switch (mp_obj_str_get_qstr(kw_args->table[i].key)) {
                        case MP_QSTR_dout: {
                            cfg.pin_data_out = args[ARG_dout].u_int;
                            break;
                        }
                        case MP_QSTR_bck: {
                            cfg.pin_bck = args[ARG_bck].u_int;
                            break;
                        }
                        case MP_QSTR_ws: {
                            cfg.pin_ws = args[ARG_ws].u_int;
                            break;
                        }
                        case MP_QSTR_sample_rate: {
                            cfg.sample_rate = args[ARG_sample_rate].u_int;
                            break;
                        }
                        case MP_QSTR_stereo: {
                            cfg.stereo = args[ARG_stereo].u_bool;
                            break;
                        }
                        case MP_QSTR_buzzer: {
                            cfg.buzzer = args[ARG_buzzer].u_bool;
                            if (cfg.buzzer) {
                                cfg.stereo = false;
                            }
                            break;
                        }
                        case MP_QSTR_use_dac: {
                            cfg.use_dac = args[ARG_use_dac].u_bool;
                            break;
                        }
                        case MP_QSTR_dac_zero_level: {
                            cfg.dac_zero_level = args[ARG_dac_zero_level].u_int;
                            break;
                        }
                        case MP_QSTR_magnification: {
                            cfg.magnification = args[ARG_magnification].u_int;
                            break;
                        }
                        case MP_QSTR_dma_buf_len: {
                            cfg.dma_buf_len = args[ARG_dma_buf_len].u_int;
                            break;
                        }
                        case MP_QSTR_dma_buf_count: {
                            cfg.dma_buf_count = args[ARG_dma_buf_count].u_int;
                            break;
                        }
                        case MP_QSTR_task_priority: {
                            cfg.task_priority = args[ARG_task_priority].u_int;
                            break;
                        }
                        case MP_QSTR_task_pinned_core: {
                            cfg.task_pinned_core = args[ARG_task_pinned_core].u_int;
                            break;
                        }
                        case MP_QSTR_i2s_port: {
                            cfg.i2s_port = (i2s_port_t)(args[ARG_i2s_port].u_int);
                            break;
                        }
                        default:
                            break;
                    }
                }
            }
            spk->stop();
            spk->end();
            spk->config(cfg);
            return mp_obj_new_bool(spk->begin());
        }

        // Get config
        char *string = NULL;
        cJSON *config = cJSON_CreateObject();
        cJSON_AddNumberToObject(config, "dout", cfg.pin_data_out);
        cJSON_AddNumberToObject(config, "bck", cfg.pin_bck);
        cJSON_AddNumberToObject(config, "ws", cfg.pin_ws);
        cJSON_AddNumberToObject(config, "sample_rate", cfg.sample_rate);
        cJSON_AddBoolToObject(config, "stereo", cfg.stereo);
        cJSON_AddBoolToObject(config, "buzzer", cfg.buzzer);
        cJSON_AddBoolToObject(config, "use_dac", cfg.use_dac);
        cJSON_AddNumberToObject(config, "dac_zero_level", cfg.dac_zero_level);
        cJSON_AddNumberToObject(config, "magnification", cfg.magnification);
        cJSON_AddNumberToObject(config, "dma_buf_len", cfg.dma_buf_len);
        cJSON_AddNumberToObject(config, "dma_buf_count", cfg.dma_buf_count);
        cJSON_AddNumberToObject(config, "task_priority", cfg.task_priority);
        cJSON_AddNumberToObject(config, "task_pinned_core", cfg.task_pinned_core);
        cJSON_AddNumberToObject(config, "i2s_port", cfg.i2s_port);

        string = cJSON_PrintUnformatted(config);
        cJSON_Delete(config);
        return mp_obj_new_str(string, strlen(string));
        ;
    }
}
}

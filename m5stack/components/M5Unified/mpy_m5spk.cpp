#include <utility/Speaker_Class.hpp>

extern "C"
{
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
            { MP_QSTR_ch,   MP_ARG_INT                  , {.u_int = -1 } },
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
            { MP_QSTR_ch, MP_ARG_INT, {.u_int = -1 } }
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
            { MP_QSTR_ch,     MP_ARG_INT                  , {.u_int = -1 } },
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
}
}

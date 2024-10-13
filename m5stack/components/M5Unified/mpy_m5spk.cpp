/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include <M5Unified.h>

extern "C"
{
#include "mpy_m5spk.h"
#include "speaker_config_t.h"
#include "extmod/vfs_fat.h"
#include "py/builtin.h"
#include "py/runtime.h"
#include "py/stream.h"

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
            { MP_QSTR_stop_current_sound, MP_ARG_BOOL,                  {.u_bool = true} },
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
            { MP_QSTR_stereo,             MP_ARG_BOOL,                  {.u_bool = false} },
            { MP_QSTR_repeat,             MP_ARG_INT,                   {.u_int = 1}               },
            { MP_QSTR_channel,            MP_ARG_INT,                   {.u_int = -1}              },
            { MP_QSTR_stop_current_sound, MP_ARG_BOOL,                  {.u_bool = false} },
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
            { MP_QSTR_stop_current_sound, MP_ARG_BOOL,                  {.u_bool = true} },
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

    mp_obj_t spk_playWavFile(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
        enum {ARG_path, ARG_repeat, ARG_channel, ARG_stop_current_sound};
        /* *FORMAT-OFF* */
        const mp_arg_t allowed_args[] = {
            { MP_QSTR_path,               MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none}  },
            { MP_QSTR_repeat,             MP_ARG_INT,                   {.u_int = 1}              },
            { MP_QSTR_ch,                 MP_ARG_INT,                   {.u_int = 0}              },
            { MP_QSTR_stop_current_sound, MP_ARG_BOOL,                  {.u_bool = true}          },
        };
        /* *FORMAT-ON* */
        mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
        // The first parameter is the Speaker object, parse from second parameter.
        mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

        struct __attribute__((packed)) wav_header_t
        {
            char RIFF[4];
            uint32_t chunk_size;
            char WAVEfmt[8];
            uint32_t fmt_chunk_size;
            uint16_t audiofmt;
            uint16_t channel;
            uint32_t sample_rate;
            uint32_t byte_per_sec;
            uint16_t block_size;
            uint16_t bit_per_sample;
        };

        struct __attribute__((packed)) sub_chunk_t
        {
            char identifier[4];
            uint32_t chunk_size;
            // uint8_t data[1];
        };

        auto spk = getSpk(&pos_args[0]);

        if (mp_obj_is_str(args[ARG_path].u_obj) && ((size_t)mp_obj_len(args[ARG_path].u_obj) < 128)) {
            char ftype[5] = {0};
            const char *file_path = mp_obj_str_get_str(args[ARG_path].u_obj);
            // mp_printf(&mp_plat_print, "file path: %s\r\n", file_path);

            for (size_t i = 0; i < 4; i++) {
                ftype[i] = tolower((char)file_path[i + strlen(file_path) - 4]);
            }
            ftype[4] = '\0';

            if (strcmp(ftype, ".wav") == 0) {
                mp_obj_t file_args[2];
                file_args[0] = args[ARG_path].u_obj;
                file_args[1] = mp_obj_new_str("rb", strlen("rb"));
                mp_obj_t wav_file = mp_vfs_open(2, file_args, (mp_map_t *)&mp_const_empty_map);
                if (wav_file == mp_const_none) {
                    mp_raise_OSError(MP_ENOENT);
                    // mp_raise_ValueError(MP_ERROR_TEXT("open file failed"));
                }

                wav_header_t header;
                int rlen = mp_stream_posix_read(wav_file, &header, sizeof(wav_header_t));
                if (rlen != sizeof(wav_header_t)) {
                    mp_stream_close(wav_file);
                    mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
                }

                /*
                // mp_printf(&mp_plat_print, "header.RIFF           : %.4s\r\n", header.RIFF);
                // mp_printf(&mp_plat_print, "header.chunk_size     : %d\r\n", header.chunk_size);
                // mp_printf(&mp_plat_print, "header.WAVEfmt        : %.8s\r\n", header.WAVEfmt);
                // mp_printf(&mp_plat_print, "header.fmt_chunk_size : %d\r\n", header.fmt_chunk_size);
                // mp_printf(&mp_plat_print, "header.audiofmt       : %d\r\n", header.audiofmt);
                // mp_printf(&mp_plat_print, "header.channel        : %d\r\n", header.channel);
                // mp_printf(&mp_plat_print, "header.sample_rate    : %d\r\n", header.sample_rate);
                // mp_printf(&mp_plat_print, "header.byte_per_sec   : %d\r\n", header.byte_per_sec);
                // mp_printf(&mp_plat_print, "header.block_size     : %d\r\n", header.block_size);
                // mp_printf(&mp_plat_print, "header.bit_per_sample : %d\r\n", header.bit_per_sample);
                */

                if (memcmp(header.RIFF, "RIFF", 4)
                    || memcmp(header.WAVEfmt, "WAVEfmt ", 8)
                    || header.audiofmt != 1
                    || header.bit_per_sample < 8
                    || header.bit_per_sample > 16
                    || header.channel == 0
                    || header.channel > 2) {
                    mp_stream_close(wav_file);
                    mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("file format is not supported"));
                }

                sub_chunk_t sub_chunk;
                while (true) {
                    if (mp_stream_posix_read(wav_file, &sub_chunk, sizeof(sub_chunk_t)) != sizeof(sub_chunk_t)) {
                        mp_stream_close(wav_file);
                        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
                    }
                    // mp_printf(&mp_plat_print, "sub_chunk.identifier  : %.4s\r\n", sub_chunk.identifier);
                    // mp_printf(&mp_plat_print, "sub_chunk.chunk_size  : %d\r\n", sub_chunk.chunk_size);

                    if (strncmp(sub_chunk.identifier, "data", 4) == 0) {
                        break;
                    }

                    if (mp_stream_posix_lseek(wav_file, sub_chunk.chunk_size, SEEK_CUR) == -1) {
                        mp_stream_close(wav_file);
                        mp_raise_OSError(MP_ESPIPE);
                    }
                }

                uint32_t data_len = sub_chunk.chunk_size;
                bool flg_16bit = (header.bit_per_sample >> 4);

                constexpr const size_t buf_num = 3;
                constexpr const size_t buf_size = 512;
                uint8_t wav_data[buf_num][buf_size];

                size_t idx = 0;
                while (data_len > 0) {
                    size_t len = (data_len > buf_size) ? buf_size : data_len;
                    // mp_printf(&mp_plat_print, "buf idx: %d len: %d data_len: %d\r\n", idx, len, data_len);
                    if (mp_stream_posix_read(wav_file, (uint8_t *)wav_data[idx], len) != len) {
                        mp_stream_close(wav_file);
                        mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("File is too short"));
                    }
                    data_len -= len;

                    if (flg_16bit) {
                        spk->playRaw((const int16_t *)wav_data[idx], len >> 1, header.sample_rate, header.channel > 1, 1, 0);
                    } else {
                        spk->playRaw((const uint8_t *)wav_data[idx], len, header.sample_rate, header.channel > 1, 1, 0);
                    }
                    idx = idx < (buf_num - 1) ? idx + 1 : 0;
                }
                mp_stream_close(wav_file);
            } else {
                mp_raise_ValueError(MP_ERROR_TEXT("file type is not supported"));
            }
        }
        return mp_const_none;
    }
}
}

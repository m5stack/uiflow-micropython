// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT

#include <string.h>
#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "uvc_camera.h"

typedef struct {
    mp_obj_base_t base;
    uint32_t generation;
} uvc_camera_obj_t;

static void camera_check(esp_err_t err) {
    if (err == ESP_ERR_NOT_FOUND) {
        mp_raise_OSError(MP_ENODEV);
    }
    if (err != ESP_OK) {
        mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("USB UVC Camera: %s"), esp_err_to_name(err));
    }
}

static void camera_check_active(mp_obj_t self_in) {
    uvc_camera_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (!uiflow_uvc_active(self->generation)) {
        mp_raise_OSError(MP_ENODEV);
    }
}

static unsigned camera_timeout(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args, unsigned default_ms) {
    const mp_arg_t allowed[] = {
        {MP_QSTR_timeout, MP_ARG_INT, {.u_int = default_ms}},
    };
    mp_arg_val_t args[1];
    mp_arg_parse_all(n_args, pos_args, kw_args, 1, allowed, args);
    if (args[0].u_int < 0 || args[0].u_int > 60000) {
        mp_raise_ValueError(MP_ERROR_TEXT("timeout must be 0..60000 ms"));
    }
    return args[0].u_int;
}

static mp_obj_t camera_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum { ARG_width, ARG_height, ARG_fps, ARG_frame_size, ARG_format };
    static const mp_arg_t allowed[] = {
        {MP_QSTR_width, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 640}},
        {MP_QSTR_height, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 480}},
        {MP_QSTR_fps, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_frame_size, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 0}},
        {MP_QSTR_format, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_rom_obj = MP_ROM_QSTR(MP_QSTR_mjpeg)}},
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed), allowed, args);
    if (args[ARG_width].u_int <= 0 || args[ARG_width].u_int > 4096 ||
        args[ARG_height].u_int <= 0 || args[ARG_height].u_int > 4096 ||
        args[ARG_fps].u_int < 0 || args[ARG_fps].u_int > 120 ||
        args[ARG_frame_size].u_int < 0 || args[ARG_frame_size].u_int > 4 * 1024 * 1024) {
        mp_raise_ValueError(MP_ERROR_TEXT("invalid resolution, fps or frame_size"));
    }
    const char *name = mp_obj_str_get_str(args[ARG_format].u_obj);
    enum uvc_host_stream_format format;
    if (strcmp(name, "mjpeg") == 0) {
        format = UVC_VS_FORMAT_MJPEG;
    } else if (strcmp(name, "yuy2") == 0) {
        format = UVC_VS_FORMAT_YUY2;
    } else {
        mp_raise_ValueError(MP_ERROR_TEXT("format must be mjpeg or yuy2"));
    }
    size_t raw_size = (size_t)args[ARG_width].u_int * args[ARG_height].u_int * 2;
    size_t frame_size = args[ARG_frame_size].u_int;
    if (frame_size == 0) {
        frame_size = format == UVC_VS_FORMAT_YUY2 ?
            (raw_size < 16 * 1024 ? 16 * 1024 : raw_size) : 512 * 1024;
    }
    if (frame_size < 16 * 1024 || frame_size > 4 * 1024 * 1024 ||
        (format == UVC_VS_FORMAT_YUY2 && ((args[ARG_width].u_int & 1) || frame_size < raw_size))) {
        mp_raise_ValueError(MP_ERROR_TEXT("frame_size too small or invalid YUY2 resolution"));
    }
    uvc_camera_obj_t *self = mp_obj_malloc(uvc_camera_obj_t, type);
    camera_check(uiflow_uvc_init(args[ARG_width].u_int, args[ARG_height].u_int,
        args[ARG_fps].u_int, frame_size, format));
    self->generation = uiflow_uvc_generation();
    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t camera_start(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    camera_check_active(pos_args[0]);
    unsigned timeout = camera_timeout(n_args - 1, pos_args + 1, kw_args, 5000);
    camera_check(uiflow_uvc_start(timeout));
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(camera_start_obj, 1, camera_start);

static mp_obj_t camera_stop(mp_obj_t self_in) {
    camera_check_active(self_in);
    camera_check(uiflow_uvc_stop());
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_stop_obj, camera_stop);

static mp_obj_t camera_deinit(mp_obj_t self_in) {
    uvc_camera_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (self->generation == uiflow_uvc_generation()) {
        camera_check(uiflow_uvc_deinit());
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_deinit_obj, camera_deinit);

static uvc_host_frame_t *camera_wait_frame(mp_obj_t self, unsigned timeout) {
    mp_uint_t start = mp_hal_ticks_ms();
    for (;;) {
        camera_check_active(self);
        uvc_host_frame_t *frame;
        camera_check(uiflow_uvc_frame_take(&frame));
        if (frame != NULL) {
            return frame;
        }
        if (mp_hal_ticks_ms() - start >= timeout) {
            return NULL;
        }
        mp_hal_delay_ms(1);
    }
}

static mp_obj_t camera_readinto(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    camera_check_active(pos_args[0]);
    unsigned timeout = camera_timeout(n_args - 2, pos_args + 2, kw_args, 1000);
    mp_buffer_info_t buf;
    mp_get_buffer_raise(pos_args[1], &buf, MP_BUFFER_WRITE);
    uvc_host_frame_t *frame = camera_wait_frame(pos_args[0], timeout);
    if (frame == NULL) {
        return MP_OBJ_NEW_SMALL_INT(0);
    }
    size_t length = frame->data_len;
    if (length <= buf.len) {
        memcpy(buf.buf, frame->data, length);
    }
    camera_check(uiflow_uvc_frame_release(frame));
    if (length > buf.len) {
        mp_raise_ValueError(MP_ERROR_TEXT("buffer too small for camera frame"));
    }
    return mp_obj_new_int_from_uint(length);
}
static MP_DEFINE_CONST_FUN_OBJ_KW(camera_readinto_obj, 2, camera_readinto);

static mp_obj_t camera_readinto_rgb565(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    camera_check_active(pos_args[0]);
    unsigned timeout = camera_timeout(n_args - 2, pos_args + 2, kw_args, 1000);
    mp_buffer_info_t buf;
    mp_get_buffer_raise(pos_args[1], &buf, MP_BUFFER_WRITE);
    uiflow_uvc_info_t info;
    uiflow_uvc_info(&info);
    if (info.format.format != UVC_VS_FORMAT_YUY2) {
        mp_raise_ValueError(MP_ERROR_TEXT("RGB565 conversion requires yuy2"));
    }
    if (buf.len < (size_t)info.format.h_res * info.format.v_res * 2) {
        mp_raise_ValueError(MP_ERROR_TEXT("buffer too small for RGB565 frame"));
    }
    uvc_host_frame_t *frame = camera_wait_frame(pos_args[0], timeout);
    if (frame == NULL) {
        return MP_OBJ_NEW_SMALL_INT(0);
    }
    size_t length = frame->data_len;
    esp_err_t err = uiflow_uvc_rgb565(frame, buf.buf, buf.len);
    camera_check(uiflow_uvc_frame_release(frame));
    camera_check(err);
    return mp_obj_new_int_from_uint(length);
}
static MP_DEFINE_CONST_FUN_OBJ_KW(camera_readinto_rgb565_obj, 2, camera_readinto_rgb565);

static mp_obj_t camera_read(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    camera_check_active(pos_args[0]);
    unsigned timeout = camera_timeout(n_args - 1, pos_args + 1, kw_args, 1000);
    uvc_host_frame_t *frame = camera_wait_frame(pos_args[0], timeout);
    if (frame == NULL) {
        return mp_const_none;
    }
    mp_obj_t result;
    nlr_buf_t nlr;
    if (nlr_push(&nlr) == 0) {
        result = mp_obj_new_bytes(frame->data, frame->data_len);
        nlr_pop();
    } else {
        // A GC allocation failure must not leave a driver frame retained.
        uiflow_uvc_frame_release(frame);
        nlr_jump(nlr.ret_val);
    }
    camera_check(uiflow_uvc_frame_release(frame));
    return result;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(camera_read_obj, 1, camera_read);

static void camera_put(mp_obj_t dict, qstr key, mp_obj_t value) {
    mp_obj_dict_store(dict, MP_OBJ_NEW_QSTR(key), value);
}

static mp_obj_t camera_format_name(enum uvc_host_stream_format format) {
    switch (format) {
        case UVC_VS_FORMAT_MJPEG:
            return MP_OBJ_NEW_QSTR(MP_QSTR_mjpeg);
        case UVC_VS_FORMAT_YUY2:
            return MP_OBJ_NEW_QSTR(MP_QSTR_yuy2);
        case UVC_VS_FORMAT_H264:
            return MP_OBJ_NEW_QSTR(MP_QSTR_h264);
        case UVC_VS_FORMAT_H265:
            return MP_OBJ_NEW_QSTR(MP_QSTR_h265);
        case UVC_VS_FORMAT_NV12:
            return MP_OBJ_NEW_QSTR(MP_QSTR_nv12);
        default:
            return MP_OBJ_NEW_QSTR(MP_QSTR_unknown);
    }
}

static mp_obj_t camera_formats(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    camera_check_active(pos_args[0]);
    unsigned timeout = camera_timeout(n_args - 1, pos_args + 1, kw_args, 5000);
    size_t count = 0;
    mp_uint_t start = mp_hal_ticks_ms();
    for (;;) {
        esp_err_t err = uiflow_uvc_formats(NULL, &count);
        if (err == ESP_OK) {
            break;
        }
        if (err != ESP_ERR_NOT_FOUND) {
            camera_check(err);
        }
        if (mp_hal_ticks_ms() - start >= timeout) {
            return mp_obj_new_list(0, NULL);
        }
        mp_hal_delay_ms(1);
    }
    if (count > 64) {
        mp_raise_ValueError(MP_ERROR_TEXT("too many camera formats"));
    }
    uvc_host_frame_info_t *formats = m_new(uvc_host_frame_info_t, count);
    size_t actual = count;
    esp_err_t err = uiflow_uvc_formats((uvc_host_frame_info_t(*)[])formats, &actual);
    if (err != ESP_OK) {
        m_del(uvc_host_frame_info_t, formats, count);
        camera_check(err);
    }
    mp_obj_t result = mp_obj_new_list(0, NULL);
    for (size_t i = 0; i < actual; ++i) {
        const uvc_host_frame_info_t *f = &formats[i];
        mp_obj_t item = mp_obj_new_dict(0);
        camera_put(item, MP_QSTR_format, camera_format_name(f->format));
        camera_put(item, MP_QSTR_width, mp_obj_new_int_from_uint(f->h_res));
        camera_put(item, MP_QSTR_height, mp_obj_new_int_from_uint(f->v_res));
        camera_put(item, MP_QSTR_default_fps, mp_obj_new_float(
            f->default_interval ? 10000000.0f / f->default_interval : 0));
        mp_obj_list_append(result, item);
    }
    m_del(uvc_host_frame_info_t, formats, count);
    return result;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(camera_formats_obj, 1, camera_formats);

static mp_obj_t camera_info(mp_obj_t self_in) {
    camera_check_active(self_in);
    uiflow_uvc_info_t info;
    uiflow_uvc_info(&info);
    mp_obj_t result = mp_obj_new_dict(0);
    camera_put(result, MP_QSTR_status, MP_OBJ_NEW_QSTR(info.streaming ?
        MP_QSTR_streaming : (info.connected ? MP_QSTR_ready : MP_QSTR_waiting)));
    camera_put(result, MP_QSTR_format, camera_format_name(info.format.format));
    camera_put(result, MP_QSTR_width, mp_obj_new_int_from_uint(info.format.h_res));
    camera_put(result, MP_QSTR_height, mp_obj_new_int_from_uint(info.format.v_res));
    camera_put(result, MP_QSTR_fps, mp_obj_new_float(info.format.fps));
    camera_put(result, MP_QSTR_received, mp_obj_new_int_from_uint(info.frames));
    camera_put(result, MP_QSTR_dropped, mp_obj_new_int_from_uint(info.dropped));
    camera_put(result, MP_QSTR_overflows, mp_obj_new_int_from_uint(info.overflows));
    camera_put(result, MP_QSTR_errors, mp_obj_new_int_from_uint(info.errors));
    camera_put(result, MP_QSTR_last_error, mp_obj_new_int(info.last_error));
    return result;
}
static MP_DEFINE_CONST_FUN_OBJ_1(camera_info_obj, camera_info);

static const mp_rom_map_elem_t camera_locals_table[] = {
    {MP_ROM_QSTR(MP_QSTR_formats), MP_ROM_PTR(&camera_formats_obj)},
    {MP_ROM_QSTR(MP_QSTR_start), MP_ROM_PTR(&camera_start_obj)},
    {MP_ROM_QSTR(MP_QSTR_stop), MP_ROM_PTR(&camera_stop_obj)},
    {MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&camera_read_obj)},
    {MP_ROM_QSTR(MP_QSTR_readinto), MP_ROM_PTR(&camera_readinto_obj)},
    {MP_ROM_QSTR(MP_QSTR_readinto_rgb565), MP_ROM_PTR(&camera_readinto_rgb565_obj)},
    {MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&camera_info_obj)},
    {MP_ROM_QSTR(MP_QSTR_deinit), MP_ROM_PTR(&camera_deinit_obj)},
};
static MP_DEFINE_CONST_DICT(camera_locals, camera_locals_table);

MP_DEFINE_CONST_OBJ_TYPE(
    uiflow_uvc_camera_type,
    MP_QSTR_UVCCamera,
    MP_TYPE_FLAG_NONE,
    make_new, camera_make_new,
    locals_dict, &camera_locals
    );

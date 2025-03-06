/*
 * SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include "py/nlr.h"
#include "py/obj.h"
#include "py/objlist.h"
#include "py/objstr.h"
#include "py/objtuple.h"
#include "py/objtype.h"
#include "py/runtime.h"
#include "py/mphal.h"

#include "esp_code_scanner.h"
#include "imlib.h"
#include "py_image.h"
#include "py_helper.h"



// =================================================================================================
// object: qrcode
#define py_qrcode_obj_size 2

typedef struct py_qrcode_obj {
    mp_obj_base_t base;
    mp_obj_t type_name, data;
} py_qrcode_obj_t;


static void py_qrcode_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    py_qrcode_obj_t *self = self_in;
    mp_printf(print,
        "qrcode type name: %s, payload: %s\n",
        mp_obj_str_get_str(self->type_name), mp_obj_str_get_str(self->data));
}

static mp_obj_t py_qrcode_subscr(mp_obj_t self_in, mp_obj_t index, mp_obj_t value) {
    if (value == MP_OBJ_SENTINEL) {
        py_qrcode_obj_t *self = self_in;
        if (MP_OBJ_IS_TYPE(index, &mp_type_slice)) {
            mp_bound_slice_t slice;
            if (!mp_seq_get_fast_slice_indexes(py_qrcode_obj_size, index, &slice)) {
                mp_raise_msg(&mp_type_OSError, MP_ERROR_TEXT("only slices with step=1 (aka None) are supported"));
            }
            mp_obj_tuple_t *result = mp_obj_new_tuple(slice.stop - slice.start, NULL);
            mp_seq_copy(result->items, &(self->type_name) + slice.start, result->len, mp_obj_t);
            return result;
        }
        switch (mp_get_index(self->base.type, py_qrcode_obj_size, index, false)) {
            case 0:
                return self->type_name;
            case 1:
                return self->data;
        }
    }

    return MP_OBJ_NULL;
}

mp_obj_t py_qrcode_type_name(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->type_name;
}
mp_obj_t py_qrcode_data(mp_obj_t self_in) {
    return ((py_qrcode_obj_t *)self_in)->data;
}

static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_type_name_obj, py_qrcode_type_name);
static MP_DEFINE_CONST_FUN_OBJ_1(py_qrcode_data_obj, py_qrcode_data);


static const mp_rom_map_elem_t py_qrcode_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_type_name), MP_ROM_PTR(&py_qrcode_type_name_obj) },
    { MP_ROM_QSTR(MP_QSTR_payload),   MP_ROM_PTR(&py_qrcode_data_obj)      },
};

static MP_DEFINE_CONST_DICT(py_qrcode_locals_dict, py_qrcode_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    py_qrcode_type,
    MP_QSTR_qrcode,
    MP_TYPE_FLAG_NONE,
    print, py_qrcode_print,
    subscr, py_qrcode_subscr,
    locals_dict, &py_qrcode_locals_dict);


// =================================================================================================
// method: find_qrcodes
static mp_obj_t py_find_qrcodes(mp_obj_t arg_img) {
    image_t *img = (image_t *)py_image_cobj(arg_img);

    // Decode Progress
    esp_image_scanner_t *esp_scan = esp_code_scanner_create();
    esp_code_scanner_config_t config = {ESP_CODE_SCANNER_MODE_FAST,
                                        ESP_CODE_SCANNER_IMAGE_RGB565,
                                        img->w,
                                        img->h};
    esp_code_scanner_set_config(esp_scan, config);

    int decoded_num = esp_code_scanner_scan_image(esp_scan, img->data);
    if (decoded_num) {
        esp_code_scanner_symbol_t result = esp_code_scanner_result(esp_scan);
        py_qrcode_obj_t *o = m_new_obj(py_qrcode_obj_t);
        o->base.type = &py_qrcode_type;
        o->type_name = mp_obj_new_str(result.type_name, strlen(result.type_name));
        o->data = mp_obj_new_str(result.data, strlen(result.data));
        esp_code_scanner_destroy(esp_scan);
        return o;
    } else {
        esp_code_scanner_destroy(esp_scan);
        return mp_const_none;
    }
}
static MP_DEFINE_CONST_FUN_OBJ_1(py_find_qrcodes_obj, py_find_qrcodes);


// =================================================================================================
// module: code_scanner
static const mp_rom_map_elem_t code_scanner_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__),     MP_ROM_QSTR(MP_QSTR_code_scanner) },
    { MP_ROM_QSTR(MP_QSTR_qrcode),       MP_ROM_PTR(&py_qrcode_type)       },
    { MP_ROM_QSTR(MP_QSTR_find_qrcodes), MP_ROM_PTR(&py_find_qrcodes_obj)  },
};
static MP_DEFINE_CONST_DICT(code_scanner_globals, code_scanner_globals_table);

const mp_obj_module_t module_code_scanner = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&code_scanner_globals,
};

MP_REGISTER_MODULE(MP_QSTR_code_scanner, module_code_scanner);

/*
 * SPDX-License-Identifier: MIT
 *
 * Copyright (C) 2013-2024 OpenMV, LLC.
 * Copyright (c) 2024 M5Stack Technology CO LTD
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * Python helper functions.
 */

#include "py/obj.h"
#include "py/runtime.h"
#include "py_helper.h"
#include "py_image.h"

#include "cmsis_iccarm.h"



image_t *py_helper_arg_to_image(const mp_obj_t arg, uint32_t flags) {
    image_t *image = NULL;
    image = py_image_cobj(arg);
    if (flags) {
        if ((flags & ARG_IMAGE_MUTABLE) && !image->is_mutable) {
            mp_raise_msg(&mp_type_ValueError, MP_ERROR_TEXT("Expected a mutable image"));
        } else if ((flags & ARG_IMAGE_UNCOMPRESSED) && image->is_compressed) {
            mp_raise_msg(&mp_type_ValueError, MP_ERROR_TEXT("Expected an uncompressed image"));
        } else if ((flags & ARG_IMAGE_GRAYSCALE) && image->pixfmt != OMV_PIXFORMAT_GRAYSCALE) {
            mp_raise_msg(&mp_type_ValueError, MP_ERROR_TEXT("Expected an uncompressed image"));
        }
    }
    return image;
}


uint py_helper_consume_array(size_t n_args, const mp_obj_t *args, uint arg_index, size_t len, const mp_obj_t **items)
{
    if (MP_OBJ_IS_TYPE(args[arg_index], &mp_type_tuple) || MP_OBJ_IS_TYPE(args[arg_index], &mp_type_list)) {
        mp_obj_get_array_fixed_n(args[arg_index], len, (mp_obj_t **) items);
        return arg_index + 1;
    } else {
        //PY_ASSERT_TRUE_MSG((n_args - arg_index) >= len, "Not enough positional arguments!");
        *items = args + arg_index;
        return arg_index + len;
    }
}
 
float py_helper_keyword_float(uint n_args, const mp_obj_t *args, uint arg_index,
                              mp_map_t *kw_args, mp_obj_t kw, float default_val) {
    mp_map_elem_t *kw_arg = mp_map_lookup(kw_args, kw, MP_MAP_LOOKUP);

    if (kw_arg) {
        default_val = mp_obj_get_float(kw_arg->value);
    } else if (n_args > arg_index) {
        default_val = mp_obj_get_float(args[arg_index]);
    }

    return default_val;
}

int py_helper_keyword_color(image_t *img, uint n_args, const mp_obj_t *args, uint arg_index,
                            mp_map_t *kw_args, int default_val) {
    mp_map_elem_t *kw_arg = kw_args ? mp_map_lookup(kw_args, MP_OBJ_NEW_QSTR(MP_QSTR_color), MP_MAP_LOOKUP) : NULL;

    if (kw_arg) {
        if (mp_obj_is_integer(kw_arg->value)) {
            //default_val = mp_obj_get_int(kw_arg->value);
            int tmp = mp_obj_get_int(kw_arg->value);
            int r, g, b;
            r = tmp >> 8 & 0x00F800;  
            g = tmp >> 5 & 0x0007E0;  
            b = tmp >> 3 & 0x00001F;  
            default_val = (r | g | b);
        } else {
            mp_obj_t *arg_color;
            mp_obj_get_array_fixed_n(kw_arg->value, 3, &arg_color);
            default_val = COLOR_R8_G8_B8_TO_RGB565(__USAT(mp_obj_get_int(arg_color[0]), 8),
                                                   __USAT(mp_obj_get_int(arg_color[1]), 8),
                                                   __USAT(mp_obj_get_int(arg_color[2]), 8));

            switch (img->pixfmt) {
                case OMV_PIXFORMAT_BINARY: {
                    default_val = COLOR_RGB565_TO_BINARY(default_val);
                    break;
                }
                case OMV_PIXFORMAT_GRAYSCALE: {
                    default_val = COLOR_RGB565_TO_GRAYSCALE(default_val);
                    break;
                }
                default: {
                    break;
                }
            }
        }
    } else if (n_args > arg_index) {
        if (mp_obj_is_integer(args[arg_index])) {
            default_val = mp_obj_get_int(args[arg_index]);
        } else {
            mp_obj_t *arg_color;
            mp_obj_get_array_fixed_n(args[arg_index], 3, &arg_color);
            default_val = COLOR_R8_G8_B8_TO_RGB565(__USAT(mp_obj_get_int(arg_color[0]), 8),
                                                   __USAT(mp_obj_get_int(arg_color[1]), 8),
                                                   __USAT(mp_obj_get_int(arg_color[2]), 8));
            switch (img->pixfmt) {
                case OMV_PIXFORMAT_BINARY: {
                    default_val = COLOR_RGB565_TO_BINARY(default_val);
                    break;
                }
                case OMV_PIXFORMAT_GRAYSCALE: {
                    default_val = COLOR_RGB565_TO_GRAYSCALE(default_val);
                    break;
                }
                default: {
                    break;
                }
            }
        }
    }

    default_val = (default_val << 8) | (default_val >> 8); // swap endian for esp32
    return default_val;
}

 
int py_helper_keyword_int(size_t n_args, const mp_obj_t *args, uint arg_index,
                          mp_map_t *kw_args, mp_obj_t kw, int default_val)
{
    mp_map_elem_t *kw_arg = mp_map_lookup(kw_args, kw, MP_MAP_LOOKUP);

    if (kw_arg) {
        default_val = mp_obj_get_int(kw_arg->value);
    } else if (n_args > arg_index) {
        default_val = mp_obj_get_int(args[arg_index]);
    }

    return default_val;
}
 


/*
 * This file is part of the OpenMV project.
 *
 * Copyright (c) 2013-2021 Ibrahim Abdelkader <iabdalkader@openmv.io>
 * Copyright (c) 2013-2021 Kwabena W. Agyeman <kwagyeman@openmv.io>
 *
 * This work is licensed under the MIT license, see the file LICENSE for details.
 *
 * Python helper functions.
 */
#ifndef __PY_HELPER_H__
#define __PY_HELPER_H__

#include "py/obj.h"
#include "imlib.h"


typedef enum py_helper_arg_image_flags {
    ARG_IMAGE_ANY          = (0 << 0),
    ARG_IMAGE_MUTABLE      = (1 << 0),
    ARG_IMAGE_UNCOMPRESSED = (1 << 1),
    ARG_IMAGE_GRAYSCALE    = (1 << 2),
    ARG_IMAGE_ALLOC        = (1 << 3)
} py_helper_arg_image_flags_t;

image_t *py_helper_arg_to_image(const mp_obj_t arg, uint32_t flags);

uint py_helper_consume_array(size_t n_args, const mp_obj_t *args, uint arg_index, size_t len, const mp_obj_t **items);
 
int py_helper_keyword_int(size_t n_args, const mp_obj_t *args, uint arg_index,
                          mp_map_t *kw_args, mp_obj_t kw, int default_val);

float py_helper_keyword_float(uint n_args, const mp_obj_t *args, uint arg_index,
                              mp_map_t *kw_args, mp_obj_t kw, float default_val);

int py_helper_keyword_color(image_t *img, uint n_args, const mp_obj_t *args, uint arg_index,
                            mp_map_t *kw_args, int default_val);


#endif // __PY_HELPER__


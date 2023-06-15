#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>

typedef struct _als_obj_t {
    mp_obj_base_t base;
    void *als;
} als_obj_t;

extern const mp_obj_type_t mp_als_type;

#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>

typedef struct _gfx_obj_t {
    mp_obj_base_t base;
    void* gfx;
} gfx_obj_t;

extern const mp_obj_type_t gfxdevice_type;
extern const mp_obj_type_t gfxcanvas_type;


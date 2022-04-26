#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>
#include <py/stream.h>
#include <py/builtin.h>

typedef struct _gfx_obj_t {
    mp_obj_base_t base;
    void *gfx;
} gfx_obj_t;

typedef struct _font_obj_t {
    mp_obj_base_t base;
    const void *font;
} font_obj_t;


extern const mp_obj_type_t gfxdevice_type;
extern const mp_obj_type_t gfxcanvas_type;

extern const font_obj_t gfx_font_0_obj;
extern const font_obj_t gfx_font_2_obj;
extern const font_obj_t gfx_font_4_obj;
extern const font_obj_t gfx_font_6_obj;
extern const font_obj_t gfx_font_7_obj;
extern const font_obj_t gfx_font_8_obj;
extern const font_obj_t gfx_font_DejaVu9_obj;
extern const font_obj_t gfx_font_DejaVu12_obj;
extern const font_obj_t gfx_font_DejaVu18_obj;
extern const font_obj_t gfx_font_DejaVu24_obj;

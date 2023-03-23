#include <M5GFX.h>
#include <M5Unified.h>

#include <ffi.h>
typedef union {
    ffi_sarg sint;
    ffi_arg uint;
    float flt;
    double dbl;
    void *ptr;
} ffi_value;

extern "C"
{
#include <py/obj.h>
#include "mpy_m5unified.h"
#include "mpy_m5gfx.h"
#include "esp_log.h"

#if MICROPY_PY_LVGL
#include "lvgl/lvgl.h"
#include "lvgl/src/hal/lv_hal_disp.h"
#include "./../../components/lv_bindings/driver/include/common.h"
#endif

#include "mpy_m5lfs2.txt"

static inline M5GFX *getGfx(const mp_obj_t *args) {
    return (M5GFX *)((((gfx_obj_t *)MP_OBJ_TO_PTR(args[0]))->gfx));
}

// -------- GFX common wrapper
mp_obj_t gfx_width(mp_obj_t self) {
    auto gfx = getGfx(&self);
    return mp_obj_new_int(gfx->width());
}

mp_obj_t gfx_height(mp_obj_t self) {
    auto gfx = getGfx(&self);
    return mp_obj_new_int(gfx->height());
}

mp_obj_t gfx_getRotation(mp_obj_t self) {
    auto gfx = getGfx(&self);
    return mp_obj_new_int(gfx->getRotation());
}

mp_obj_t gfx_getColorDepth(mp_obj_t self) {
    auto gfx = getGfx(&self);
    return mp_obj_new_int(gfx->getColorDepth());
}

mp_obj_t gfx_getCursor(mp_obj_t self) {
    auto gfx = getGfx(&self);
    mp_obj_t tuple[2] = { mp_obj_new_int(gfx->getCursorX())
                          , mp_obj_new_int(gfx->getCursorY())};
    return mp_obj_new_tuple(2, tuple);
}

mp_obj_t gfx_setRotation(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_r};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_r, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->setRotation(args[ARG_r].u_int);
    return mp_const_none;
}

mp_obj_t gfx_setColorDepth(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_bpp};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_bpp, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->setColorDepth(args[ARG_bpp].u_int);
    return mp_const_none;
}

mp_obj_t gfx_setFont(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_font};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_font, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->setFont((const m5gfx::IFont *)((font_obj_t *)args[ARG_font].u_obj)->font);
    return mp_const_none;
}

mp_obj_t gfx_setTextColor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_fgcolor, ARG_bgcolor};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_fgcolor, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_bgcolor, MP_ARG_INT                  , {.u_int = 0x000000 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->setTextColor((uint32_t)args[ARG_fgcolor].u_int, (uint32_t)args[ARG_bgcolor].u_int);
    return mp_const_none;
}

mp_obj_t gfx_setTextScroll(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_scroll};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_scroll, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = mp_const_false } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->setTextScroll((bool)args[ARG_scroll].u_bool);
    return mp_const_none;
}

mp_obj_t gfx_setTextSize(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_size};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_size, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_true } }  // 1.0
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->setTextSize(mp_obj_get_float(args[ARG_size].u_obj));
    return mp_const_none;
}

mp_obj_t gfx_setCursor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->setCursor(args[ARG_x].u_int, args[ARG_y].u_int);
    return mp_const_none;
}

mp_obj_t gfx_setBrightness(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_brightness};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_brightness, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 80 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->setBrightness(args[ARG_brightness].u_int);
    return mp_const_none;
}

mp_obj_t gfx_clear(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setBaseColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->clear();
    return mp_const_none;
}

mp_obj_t gfx_fillScreen(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->fillScreen();
    return mp_const_none;
}

mp_obj_t gfx_drawPixel(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawPixel(args[ARG_x].u_int, args[ARG_y].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawCircle(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_r, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawCircle(args[ARG_x].u_int, args[ARG_y].u_int, args[ARG_r].u_int);
    return mp_const_none;
}

mp_obj_t gfx_fillCircle(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_r, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->fillCircle(args[ARG_x].u_int, args[ARG_y].u_int, args[ARG_r].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawEllipse(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_rx, ARG_ry, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_rx,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_ry,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawEllipse(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_rx].u_int, args[ARG_ry].u_int);
    return mp_const_none;
}

mp_obj_t gfx_fillEllipse(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_rx, ARG_ry, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_rx,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_ry,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->fillEllipse(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_rx].u_int, args[ARG_ry].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawLine(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x0, ARG_y0, ARG_x1, ARG_y1, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x0,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y0,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_x1,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y1,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawLine(args[ARG_x0].u_int, args[ARG_y0].u_int
        , args[ARG_x1].u_int, args[ARG_y1].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawRect(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_w, ARG_h, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_w,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_h,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawRect(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_w].u_int, args[ARG_h].u_int);
    return mp_const_none;
}

mp_obj_t gfx_fillRect(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_w, ARG_h, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_w,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_h,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->fillRect(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_w].u_int, args[ARG_h].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawRoundRect(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_w, ARG_h, ARG_r, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_w,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_h,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawRoundRect(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_w].u_int, args[ARG_h].u_int
        , args[ARG_r].u_int);
    return mp_const_none;
}

mp_obj_t gfx_fillRoundRect(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_w, ARG_h, ARG_r, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_w,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_h,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->fillRoundRect(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_w].u_int, args[ARG_h].u_int
        , args[ARG_r].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawTriangle(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x0, ARG_y0, ARG_x1, ARG_y1, ARG_x2, ARG_y2, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x0,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y0,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_x1,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y1,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_x2,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y2,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawTriangle(args[ARG_x0].u_int, args[ARG_y0].u_int
        , args[ARG_x1].u_int, args[ARG_y1].u_int
        , args[ARG_x2].u_int, args[ARG_y2].u_int);
    return mp_const_none;
}

mp_obj_t gfx_fillTriangle(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x0, ARG_y0, ARG_x1, ARG_y1, ARG_x2, ARG_y2, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x0,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y0,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_x1,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y1,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_x2,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y2,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->fillTriangle(args[ARG_x0].u_int, args[ARG_y0].u_int
        , args[ARG_x1].u_int, args[ARG_y1].u_int
        , args[ARG_x2].u_int, args[ARG_y2].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawArc(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_r0, ARG_r1, ARG_angle0, ARG_angle1, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r0,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r1,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_angle0, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_angle1, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color,  MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawArc(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_r0].u_int, args[ARG_r1].u_int
        , args[ARG_angle0].u_int, args[ARG_angle1].u_int);
    return mp_const_none;
}

mp_obj_t gfx_fillArc(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_r0, ARG_r1, ARG_angle0, ARG_angle1, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r0,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r1,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_angle0, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_angle1, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color,  MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->fillArc(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_r0].u_int, args[ARG_r1].u_int
        , args[ARG_angle0].u_int, args[ARG_angle1].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawEllipseArc(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_r0x, ARG_r1x, ARG_r0y, ARG_r1y, ARG_angle0, ARG_angle1, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r0x,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r1x,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r0y,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r1y,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_angle0, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_angle1, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color,  MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->drawEllipseArc(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_r0x].u_int, args[ARG_r1x].u_int
        , args[ARG_r0y].u_int, args[ARG_r1y].u_int
        , args[ARG_angle0].u_int, args[ARG_angle1].u_int);
    return mp_const_none;
}

mp_obj_t gfx_fillEllipseArc(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y, ARG_r0x, ARG_r1x, ARG_r0y, ARG_r1y, ARG_angle0, ARG_angle1, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_y,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r0x,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r1x,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r0y,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_r1y,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_angle0, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_angle1, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_color,  MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (args[ARG_color].u_int != -1) {
        gfx->setColor((uint32_t)args[ARG_color].u_int);
    }
    gfx->fillEllipseArc(args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_r0x].u_int, args[ARG_r1x].u_int
        , args[ARG_r0y].u_int, args[ARG_r1y].u_int
        , args[ARG_angle0].u_int, args[ARG_angle1].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawQR(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text, ARG_x, ARG_y, ARG_w, ARG_version};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,       MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,       MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_w,       MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_version, MP_ARG_INT                  , {.u_int = 1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    gfx->qrcode(mp_obj_str_get_str(args[ARG_text].u_obj)
        , args[ARG_x].u_int, args[ARG_y].u_int
        , args[ARG_w].u_int, args[ARG_version].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawJpg(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_img, ARG_x, ARG_y, ARG_maxW, ARG_maxH, ARG_offX, ARG_offY, ARG_scaleX, ARG_scaleY};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_img,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,      MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_y,      MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_maxW,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_maxH,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_offX,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_offY,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_scaleX, MP_ARG_OBJ                  , {.u_obj = mp_const_true } },  // 1.0
        { MP_QSTR_scaleY, MP_ARG_OBJ                  , {.u_obj = mp_const_false } }, // 0.0
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (mp_obj_is_str(args[ARG_img].u_obj) && ((size_t)mp_obj_len(args[ARG_img].u_obj) < 128)) { // file
        LFS2Wrapper wrapper;
        gfx->drawJpgFile(&wrapper
            , mp_obj_str_get_str(args[ARG_img].u_obj)
            , args[ARG_x].u_int, args[ARG_y].u_int
            , args[ARG_maxW].u_int, args[ARG_maxH].u_int
            , args[ARG_offX].u_int, args[ARG_offY].u_int
            , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
    } else { // buffer
        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[ARG_img].u_obj, &bufinfo, MP_BUFFER_READ);
        gfx->drawJpg((const uint8_t *)bufinfo.buf
            , bufinfo.len
            , args[ARG_x].u_int, args[ARG_y].u_int
            , args[ARG_maxW].u_int, args[ARG_maxH].u_int
            , args[ARG_offX].u_int, args[ARG_offY].u_int
            , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
    }
    return mp_const_none;
}

mp_obj_t gfx_drawPng(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_img, ARG_x, ARG_y, ARG_maxW, ARG_maxH, ARG_offX, ARG_offY, ARG_scaleX, ARG_scaleY};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_img,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,      MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_y,      MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_maxW,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_maxH,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_offX,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_offY,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_scaleX, MP_ARG_OBJ                  , {.u_obj = mp_const_true } },  // 1.0
        { MP_QSTR_scaleY, MP_ARG_OBJ                  , {.u_obj = mp_const_false } }, // 0.0
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (mp_obj_is_str(args[ARG_img].u_obj) && ((size_t)mp_obj_len(args[ARG_img].u_obj) < 128)) { // file
        LFS2Wrapper wrapper;
        gfx->drawPngFile(&wrapper
            , mp_obj_str_get_str(args[ARG_img].u_obj)
            , args[ARG_x].u_int, args[ARG_y].u_int
            , args[ARG_maxW].u_int, args[ARG_maxH].u_int
            , args[ARG_offX].u_int, args[ARG_offY].u_int
            , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
    } else { // buffer
        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[ARG_img].u_obj, &bufinfo, MP_BUFFER_READ);
        gfx->drawPng((const uint8_t *)bufinfo.buf
            , bufinfo.len
            , args[ARG_x].u_int, args[ARG_y].u_int
            , args[ARG_maxW].u_int, args[ARG_maxH].u_int
            , args[ARG_offX].u_int, args[ARG_offY].u_int
            , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
    }
    return mp_const_none;
}

mp_obj_t gfx_drawBmp(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_img, ARG_x, ARG_y, ARG_maxW, ARG_maxH, ARG_offX, ARG_offY, ARG_scaleX, ARG_scaleY};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_img,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,      MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_y,      MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_maxW,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_maxH,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_offX,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_offY,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_scaleX, MP_ARG_OBJ                  , {.u_obj = mp_const_true } },  // 1.0
        { MP_QSTR_scaleY, MP_ARG_OBJ                  , {.u_obj = mp_const_false } }, // 0.0
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (mp_obj_is_str(args[ARG_img].u_obj) && ((size_t)mp_obj_len(args[ARG_img].u_obj) < 128)) { // file
        LFS2Wrapper wrapper;
        gfx->drawBmpFile(&wrapper
            , mp_obj_str_get_str(args[ARG_img].u_obj)
            , args[ARG_x].u_int, args[ARG_y].u_int
            , args[ARG_maxW].u_int, args[ARG_maxH].u_int
            , args[ARG_offX].u_int, args[ARG_offY].u_int
            , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
    } else { // buffer
        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[ARG_img].u_obj, &bufinfo, MP_BUFFER_READ);
        gfx->drawBmp((const uint8_t *)bufinfo.buf
            , bufinfo.len
            , args[ARG_x].u_int, args[ARG_y].u_int
            , args[ARG_maxW].u_int, args[ARG_maxH].u_int
            , args[ARG_offX].u_int, args[ARG_offY].u_int
            , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
    }
    return mp_const_none;
}

mp_obj_t gfx_drawImage(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_img, ARG_x, ARG_y, ARG_maxW, ARG_maxH, ARG_offX, ARG_offY, ARG_scaleX, ARG_scaleY};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_img,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,      MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_y,      MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_maxW,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_maxH,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_offX,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_offY,   MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_scaleX, MP_ARG_OBJ                  , {.u_obj = mp_const_true } },  // 1.0
        { MP_QSTR_scaleY, MP_ARG_OBJ                  , {.u_obj = mp_const_false } }, // 0.0
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    if (mp_obj_is_str(args[ARG_img].u_obj) && ((size_t)mp_obj_len(args[ARG_img].u_obj) < 128)) { // file
        char ftype[5] = {0};
        const char *file_path = mp_obj_str_get_str(args[ARG_img].u_obj);

        for (size_t i = 0; i < 4; i++)
        {
            ftype[i] = tolower((char)file_path[i + strlen(file_path) - 4]);
        }
        ftype[4] = '\0';

        LFS2Wrapper wrapper;
        if (strstr(ftype, "bmp") != NULL) {
            gfx->drawBmpFile(&wrapper
                , mp_obj_str_get_str(args[ARG_img].u_obj)
                , args[ARG_x].u_int, args[ARG_y].u_int
                , args[ARG_maxW].u_int, args[ARG_maxH].u_int
                , args[ARG_offX].u_int, args[ARG_offY].u_int
                , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
        } else if ((strstr(ftype, "jpg") != NULL) || (strstr(ftype, "jpeg") != NULL)) {
            gfx->drawJpgFile(&wrapper
                , mp_obj_str_get_str(args[ARG_img].u_obj)
                , args[ARG_x].u_int, args[ARG_y].u_int
                , args[ARG_maxW].u_int, args[ARG_maxH].u_int
                , args[ARG_offX].u_int, args[ARG_offY].u_int
                , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
        } else if (strstr(ftype, "png") != NULL) {
            gfx->drawPngFile(&wrapper
                , mp_obj_str_get_str(args[ARG_img].u_obj)
                , args[ARG_x].u_int, args[ARG_y].u_int
                , args[ARG_maxW].u_int, args[ARG_maxH].u_int
                , args[ARG_offX].u_int, args[ARG_offY].u_int
                , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
        }
    } else { // buffer
        mp_buffer_info_t bufinfo;
        mp_get_buffer_raise(args[ARG_img].u_obj, &bufinfo, MP_BUFFER_READ);
        uint8_t *type_ptr = (uint8_t *)bufinfo.buf;

        if ((type_ptr[0] == 0x42) && (type_ptr[1] == 0x4D)) {
            gfx->drawBmp((const uint8_t *)bufinfo.buf
                , bufinfo.len
                , args[ARG_x].u_int, args[ARG_y].u_int
                , args[ARG_maxW].u_int, args[ARG_maxH].u_int
                , args[ARG_offX].u_int, args[ARG_offY].u_int
                , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
        } else if ((type_ptr[0] == 0xFF) && (type_ptr[1] == 0xD8)) {
            gfx->drawJpg((const uint8_t *)bufinfo.buf
                , bufinfo.len
                , args[ARG_x].u_int, args[ARG_y].u_int
                , args[ARG_maxW].u_int, args[ARG_maxH].u_int
                , args[ARG_offX].u_int, args[ARG_offY].u_int
                , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
        } else if ((type_ptr[0] == 0x89) && (type_ptr[1] == 0x50)) {
            gfx->drawPng((const uint8_t *)bufinfo.buf
                , bufinfo.len
                , args[ARG_x].u_int, args[ARG_y].u_int
                , args[ARG_maxW].u_int, args[ARG_maxH].u_int
                , args[ARG_offX].u_int, args[ARG_offY].u_int
                , mp_obj_get_float(args[ARG_scaleX].u_obj), mp_obj_get_float(args[ARG_scaleY].u_obj));
        }
    }
    return mp_const_none;
}

mp_obj_t gfx_drawRawBuf(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_buf, ARG_x, ARG_y, ARG_w, ARG_h, ARG_len, ARG_swap};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_buf,  MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_w,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_h,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_len,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_swap, MP_ARG_BOOL                 , {.u_bool = false } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);

    // The raw buf
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(args[ARG_buf].u_obj, &bufinfo, MP_BUFFER_READ);

    gfx->startWrite();
    gfx->setAddrWindow(args[ARG_x].u_int, args[ARG_y].u_int, args[ARG_w].u_int, args[ARG_h].u_int);
    gfx->writePixels((const uint16_t *)bufinfo.buf, args[ARG_len].u_int, args[ARG_swap].u_bool);
    gfx->endWrite();

    return mp_const_none;
}

mp_obj_t gfx_drawString(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text, ARG_x, ARG_y, ARG_font};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_font, MP_ARG_OBJ                  , {.u_obj = mp_const_none } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);

    if (args[ARG_font].u_obj != mp_const_none) {
        gfx->setFont((const m5gfx::IFont *)((font_obj_t *)args[ARG_font].u_obj)->font);
    }
    gfx->drawString(mp_obj_str_get_str(args[ARG_text].u_obj), args[ARG_x].u_int, args[ARG_y].u_int);
    return mp_const_none;
}

mp_obj_t gfx_drawCenterString(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text, ARG_x, ARG_y, ARG_font};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,    MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_font, MP_ARG_OBJ                  , {.u_obj = mp_const_none } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);

    if (args[ARG_font].u_obj != mp_const_none) {
        gfx->setFont((const m5gfx::IFont *)((font_obj_t *)args[ARG_font].u_obj)->font);
    }
    gfx->drawCenterString(mp_obj_str_get_str(args[ARG_text].u_obj), args[ARG_x].u_int, args[ARG_y].u_int);
    return mp_const_none;
}

mp_obj_t gfx_print(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text, ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text,  MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_color, MP_ARG_INT                  , {.u_int = -1 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);

    if (args[ARG_color].u_int != -1) {
        gfx->setTextColor((uint32_t)args[ARG_color].u_int);
    }

    gfx->print(mp_obj_str_get_str(args[ARG_text].u_obj));
    return mp_const_none;
}

mp_obj_t gfx_printf(size_t n_args, const mp_obj_t *args) {
    auto types = (ffi_type **)alloca(n_args * sizeof(ffi_type *));
    auto values = (ffi_value *)alloca(n_args * sizeof(ffi_value));
    auto arg_values = (void **)alloca(n_args * sizeof(void *));

    size_t i;
    types[0] = &ffi_type_pointer;
    values[0].ptr = getGfx(args);
    arg_values[0] = &values[0];
    for (i = 1; i < n_args; i++) {
        if (mp_obj_get_int_maybe(args[i], (mp_int_t *)&values[i].sint)) {
            types[i] = &ffi_type_sint;
        } else if (mp_obj_is_float(args[i])) {
            types[i] = &ffi_type_double;
            values[i].dbl = mp_obj_get_float_to_d(args[i]);
        } else if (mp_obj_is_str(args[i])) {
            types[i] = &ffi_type_pointer;
            values[i].ptr = (void *)mp_obj_str_get_str(args[i]);
        } else {
            // ERROR
            mp_raise_TypeError(MP_ERROR_TEXT("not supported type is specified"));
        }
        arg_values[i] = &values[i];
    }

    ffi_cif cif;
    ffi_prep_cif_var(&cif, FFI_DEFAULT_ABI, 1, n_args, &ffi_type_sint, types);
    ffi_arg result;
    ffi_call(&cif, FFI_FN(&LovyanGFX::printf), &result, arg_values);

    return mp_const_none;
}

mp_obj_t gfx_newCanvas(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_w, ARG_h, ARG_bpp, ARG_psram};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_w,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_h,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_bpp,   MP_ARG_INT                  , {.u_int = -1 } },
        { MP_QSTR_psram, MP_ARG_BOOL                 , {.u_bool = mp_const_false } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    // The first parameter is the GFX object, parse from second parameter.
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    auto gfx = getGfx(&pos_args[0]);
    auto canvas = new M5Canvas(gfx);
    canvas->setPsram((bool)args[ARG_psram].u_bool);
    if (args[ARG_bpp].u_int != -1) {
        canvas->setColorDepth(args[ARG_bpp].u_int);
    }
    canvas->createSprite(args[ARG_w].u_int, args[ARG_h].u_int);
    gfx_obj_t *res = m_new_obj_with_finaliser(gfx_obj_t);
    res->base.type = &mp_gfxcanvas_type;
    res->gfx = canvas;
    return MP_OBJ_FROM_PTR(res);
}

// -------- GFX device wrapper
mp_obj_t gfx_startWrite(mp_obj_t self) {
    auto gfx = getGfx(&self);
    gfx->startWrite();
    return mp_const_none;
}

mp_obj_t gfx_endWrite(mp_obj_t self) {
    auto gfx = getGfx(&self);
    gfx->endWrite();
    return mp_const_none;
}

// -------- GFX canvas wrapper
mp_obj_t gfx_push(mp_obj_t self, mp_obj_t x, mp_obj_t y) {
    auto gfx = getGfx(&self);
    if (gfx) {
        ((M5Canvas *)gfx)->pushSprite(mp_obj_get_int(x), mp_obj_get_int(y));
    }
    return mp_const_none;
}

mp_obj_t gfx_delete(mp_obj_t self) {
    auto gfx = getGfx(&self);
    if (gfx) {
        ((M5Canvas *)gfx)->deleteSprite();
        delete(M5Canvas *) gfx;
        ((gfx_obj_t *)MP_OBJ_TO_PTR(self))->gfx = nullptr;
    }
    return mp_const_none;
}

#include "mpy_gfx_stream.c"

// --------------------------- builtin fonts ----------------------------
const font_obj_t gfx_font_0_obj = {{ &mp_type_object }, &m5gfx::fonts::Font0 };
const font_obj_t gfx_font_DejaVu9_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu9  };
const font_obj_t gfx_font_DejaVu12_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu12 };
const font_obj_t gfx_font_DejaVu18_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu18 };
const font_obj_t gfx_font_DejaVu24_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu24 };
const font_obj_t gfx_font_DejaVu40_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu40 };
const font_obj_t gfx_font_DejaVu56_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu56 };
const font_obj_t gfx_font_DejaVu72_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu72 };
const font_obj_t gfx_font_efontCN_24_obj = {{ &mp_type_object }, &m5gfx::fonts::efontCN_24 };
const font_obj_t gfx_font_efontJA_24_obj = {{ &mp_type_object }, &m5gfx::fonts::efontJA_24 };
const font_obj_t gfx_font_efontKR_24_obj = {{ &mp_type_object }, &m5gfx::fonts::efontKR_24 };
}

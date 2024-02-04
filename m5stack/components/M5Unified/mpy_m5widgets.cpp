#include <M5Unified.h>
#include "lgfx/utility/lgfx_tjpgd.h"

extern "C"
{
#include <py/obj.h>
#include "mpy_m5widgets.h"
#include "mpy_m5gfx.h"
#include "esp_log.h"

#include "mpy_m5lfs2.txt"

// -------- M5Widgets Common Attributes
static uint32_t _bg_color_g = 0x000000;

typedef struct _widgets_color_t {
    uint32_t bg_color;  // fill color
    uint32_t fg_color;  // text, outline...
} widgets_color_t;

typedef struct _widgets_pos_t {
    int16_t x0;
    int16_t y0;
    int16_t x1;
    int16_t y1;
    int16_t x2;
    int16_t y2;
} widgets_pos_t;

typedef struct _widgets_size_t {
    uint32_t w;
    uint32_t h;
    uint32_t r0;
    uint32_t r1;
    float text_size;
} widgets_size_t;

// -------- M5Widgets Common
static LGFX_Device *getGfx(const mp_obj_t *args) {
    return (LGFX_Device *)(((gfx_obj_t *)MP_OBJ_TO_PTR(args[0]))->gfx);
}

mp_obj_t m5widgets_fillScreen(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_color, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_color,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0x000000 } },
        { MP_QSTR_parent, MP_ARG_OBJ                  , {.u_obj =  mp_const_none} }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        auto gfx = (LGFX_Device *)&(M5.Display);
        gfx->fillScreen((uint32_t)args[ARG_color].u_int);
    } else {
        // Canvas, UserDisplay
        auto gfx = getGfx(&args[ARG_parent].u_obj);
        gfx->fillScreen((uint32_t)args[ARG_color].u_int);
    }
    _bg_color_g = (uint32_t)args[ARG_color].u_int;
    return mp_const_none;
}

mp_obj_t m5widgets_setRotation(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_r, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_r,         MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_parent,    MP_ARG_OBJ                  , {.u_obj =  mp_const_none} }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        auto gfx = (LGFX_Device *)&(M5.Display);
        gfx->setRotation((uint8_t)args[ARG_r].u_int);
    } else {
        // Canvas, UserDisplay
        auto gfx = getGfx(&args[ARG_parent].u_obj);
        gfx->setRotation((uint8_t)args[ARG_r].u_int);
    }
    return mp_const_none;
}

mp_obj_t m5widgets_setBrightness(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_brightness, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_brightness,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_parent,      MP_ARG_OBJ                  , {.u_obj =  mp_const_none} }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args, pos_args, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        auto gfx = (LGFX_Device *)&(M5.Display);
        gfx->setBrightness((uint8_t)args[ARG_brightness].u_int);
    } else {
        // Canvas, UserDisplay
        auto gfx = getGfx(&args[ARG_parent].u_obj);
        gfx->setBrightness((uint8_t)args[ARG_brightness].u_int);
    }
    return mp_const_none;
}

// -------- M5Widgets Label
typedef struct _widgets_label_obj_t {
    mp_obj_base_t base;
    LGFX_Device *gfx;
    const char *text;
    const m5gfx::IFont *font;
    widgets_color_t color;
    widgets_pos_t text_pos;
    widgets_size_t size;
}widgets_label_obj_t;

static void m5widgets_label_erase_helper(const widgets_label_obj_t *self) {
    self->gfx->fillRect(self->text_pos.x0, self->text_pos.y0,
        self->gfx->textWidth(self->text, self->font),
        self->gfx->fontHeight(self->font),
        _bg_color_g);
}

static void m5widgets_label_draw_helper(const widgets_label_obj_t *self) {
    self->gfx->setTextColor((uint32_t)self->color.fg_color, (uint32_t)self->color.bg_color);
    self->gfx->setTextSize(self->size.text_size);
    self->gfx->drawString(self->text, self->text_pos.x0, self->text_pos.y0, self->font);
}

mp_obj_t m5widgets_label_setText(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_label_obj_t *self = (widgets_label_obj_t *)pos_args[0];

    const char *new_text = mp_obj_str_get_str(args[ARG_text].u_obj);
    if (strcmp(self->text, new_text) == 0) {
        return mp_const_none;
    }
    auto stash_style = self->gfx->getTextStyle();
    m5widgets_label_erase_helper(self);
    self->text = new_text;
    m5widgets_label_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_label_setColor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text_c, ARG_bg_c};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text_c, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0xFFFFFF } },
        { MP_QSTR_bg_c,   MP_ARG_INT                  , {.u_int = -1 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_label_obj_t *self = (widgets_label_obj_t *)pos_args[0];
    auto stash_style = self->gfx->getTextStyle();
    m5widgets_label_erase_helper(self);
    self->color.fg_color = args[ARG_text_c].u_int;
    if (args[ARG_bg_c].u_int >= 0) {
        self->color.bg_color = args[ARG_bg_c].u_int;
    }
    m5widgets_label_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_label_setCursor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_label_obj_t *self = (widgets_label_obj_t *)pos_args[0];

    if ((self->text_pos.x0 == args[ARG_x].u_int) && (self->text_pos.y0 == args[ARG_y].u_int)) {
        return mp_const_none;
    }
    auto stash_style = self->gfx->getTextStyle();
    m5widgets_label_erase_helper(self);
    self->text_pos.x0 = args[ARG_x].u_int;
    self->text_pos.y0 = args[ARG_y].u_int;
    m5widgets_label_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_label_setSize(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text_sz};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text_sz, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_true } }  // 1.0
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_label_obj_t *self = (widgets_label_obj_t *)pos_args[0];
    auto stash_style = self->gfx->getTextStyle();
    m5widgets_label_erase_helper(self);
    self->size.text_size = mp_obj_get_float(args[ARG_text_sz].u_obj);
    m5widgets_label_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_label_setFont(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_font};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_font, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_label_obj_t *self = (widgets_label_obj_t *)pos_args[0];
    auto stash_style = self->gfx->getTextStyle();
    m5widgets_label_erase_helper(self);
    self->font = (const m5gfx::IFont *)((font_obj_t *)args[ARG_font].u_obj)->font;
    m5widgets_label_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_label_setVisible(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_visible};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_visible, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_label_obj_t *self = (widgets_label_obj_t *)pos_args[0];
    auto stash_style = self->gfx->getTextStyle();
    if (args[ARG_visible].u_bool) {
        m5widgets_label_draw_helper(self);
    } else {
        m5widgets_label_erase_helper(self);
    }
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_label_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum {ARG_text, ARG_x, ARG_y, ARG_text_sz, ARG_text_c, ARG_bg_c, ARG_font, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,       MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,       MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_text_sz, MP_ARG_OBJ                  , {.u_obj = mp_const_true } },  // 1.0
        { MP_QSTR_text_c,  MP_ARG_INT                  , {.u_int = 0xFFFFFF } },
        { MP_QSTR_bg_c,    MP_ARG_INT                  , {.u_int = 0x000000 } },
        { MP_QSTR_font,    MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
        { MP_QSTR_parent,  MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_label_obj_t *self = mp_obj_malloc(widgets_label_obj_t, &mp_widgets_label_type);

    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        self->gfx = (LGFX_Device *)&(M5.Display);
    } else {
        // Canvas, UserDisplay
        self->gfx = getGfx(&args[ARG_parent].u_obj);
    }

    self->text_pos.x0 = args[ARG_x].u_int;
    self->text_pos.y0 = args[ARG_y].u_int;
    self->size.text_size = mp_obj_get_float(args[ARG_text_sz].u_obj);
    self->color.fg_color = (uint32_t)args[ARG_text_c].u_int;
    self->color.bg_color = (uint32_t)args[ARG_bg_c].u_int;

    if (args[ARG_font].u_obj != mp_const_none) {
        self->font = (const m5gfx::IFont *)((font_obj_t *)args[ARG_font].u_obj)->font;
    } else {
        self->font = &m5gfx::fonts::DejaVu9;
    }

    if (args[ARG_text].u_obj == mp_const_none) {
        self->text = "Label";
    } else {
        self->text = mp_obj_str_get_str(args[ARG_text].u_obj);
    }

    auto stash_style = self->gfx->getTextStyle();
    m5widgets_label_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return MP_OBJ_FROM_PTR(self);
}

// -------- M5Widgets Title
typedef struct _widgets_title_obj_t {
    mp_obj_base_t base;
    LGFX_Device *gfx;
    const char *text;
    const m5gfx::IFont *font;
    widgets_pos_t text_pos;
    widgets_color_t color;
    widgets_size_t size;
}widgets_title_obj_t;

static void m5widgets_title_erase_helper(widgets_title_obj_t *self) {
    uint32_t stash_color = self->gfx->getRawColor();
    self->gfx->fillRect(0, 0, self->size.w, self->size.h, (uint32_t)self->color.bg_color);
    self->gfx->setRawColor(stash_color);
}

static void m5widgets_title_draw_helper(widgets_title_obj_t *self) {
    m5widgets_title_erase_helper(self);
    // text
    self->gfx->setTextColor((uint32_t)self->color.fg_color, (uint32_t)self->color.bg_color);
    self->gfx->setTextSize(self->size.text_size);
    self->gfx->drawString(self->text, self->text_pos.x0, self->text_pos.y0, self->font);
}

mp_obj_t m5widgets_title_setText(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_title_obj_t *self = (widgets_title_obj_t *)pos_args[0];

    const char *new_text = mp_obj_str_get_str(args[ARG_text].u_obj);
    if (strcmp(self->text, new_text) == 0) {
        return mp_const_none;
    }
    auto stash_style = self->gfx->getTextStyle();
    m5widgets_title_erase_helper(self);
    self->text = new_text;
    m5widgets_title_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_title_setColor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text_c, ARG_bg_c};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text_c,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0xFFFFFF } },
        { MP_QSTR_bg_c, MP_ARG_INT                     , {.u_int = -1 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_title_obj_t *self = (widgets_title_obj_t *)pos_args[0];

    auto stash_style = self->gfx->getTextStyle();
    m5widgets_title_erase_helper(self);
    self->color.fg_color = args[ARG_text_c].u_int;
    if (args[ARG_bg_c].u_int >= 0) {
        self->color.bg_color = args[ARG_bg_c].u_int;
    }
    m5widgets_title_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_title_setSize(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_h};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_h, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_title_obj_t *self = (widgets_title_obj_t *)pos_args[0];
    auto stash_style = self->gfx->getTextStyle();
    m5widgets_title_erase_helper(self);
    self->size.h = args[ARG_h].u_int;
    if (self->size.h < self->gfx->fontHeight(self->font)) {
        self->size.h = self->gfx->fontHeight(self->font) + 2;
    }
    self->size.text_size = (float)(self->size.h / self->gfx->fontHeight(self->font));
    m5widgets_title_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_title_setTextCursor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text_x};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text_x, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_title_obj_t *self = (widgets_title_obj_t *)pos_args[0];
    auto stash_style = self->gfx->getTextStyle();
    m5widgets_title_erase_helper(self);
    self->text_pos.x0 = args[ARG_text_x].u_int;
    m5widgets_title_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_title_setVisible(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_visible};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_visible, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_title_obj_t *self = (widgets_title_obj_t *)pos_args[0];
    auto stash_style = self->gfx->getTextStyle();
    if (args[ARG_visible].u_bool) {
        m5widgets_title_draw_helper(self);
    } else {
        m5widgets_title_erase_helper(self);
    }
    self->gfx->setTextStyle(stash_style);
    return mp_const_none;
}

mp_obj_t m5widgets_title_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum {ARG_text, ARG_text_x, ARG_text_c, ARG_bg_c, ARG_font, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text,   MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_text_x, MP_ARG_INT                  , {.u_int = 0 } },
        { MP_QSTR_text_c, MP_ARG_INT                  , {.u_int = 0xFFFFFF } },
        { MP_QSTR_bg_c,   MP_ARG_INT                  , {.u_int = 0xFF00FF } },
        { MP_QSTR_font,   MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
        { MP_QSTR_parent, MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    _widgets_title_obj_t *self = mp_obj_malloc(_widgets_title_obj_t, &mp_widgets_title_type);
    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        self->gfx = (LGFX_Device *)&(M5.Display);
    } else {
        // Canvas, UserDisplay
        self->gfx = getGfx(&args[ARG_parent].u_obj);
    }

    if (args[ARG_text].u_obj == mp_const_none) {
        self->text = "Title";
    } else {
        self->text = mp_obj_str_get_str(args[ARG_text].u_obj);
    }

    if (args[ARG_font].u_obj != mp_const_none) {
        self->font = (const m5gfx::IFont *)((font_obj_t *)args[ARG_font].u_obj)->font;
    } else {
        self->font = &m5gfx::fonts::DejaVu9;
    }

    self->size.w = self->gfx->width();
    self->size.h = self->gfx->fontHeight(self->font);
    self->text_pos.x0 = args[ARG_text_x].u_int;
    self->text_pos.y0 = 0;
    self->color.fg_color = args[ARG_text_c].u_int;
    self->color.bg_color = args[ARG_bg_c].u_int;
    self->size.text_size = 1.0;

    auto stash_style = self->gfx->getTextStyle();
    m5widgets_title_draw_helper(self);
    self->gfx->setTextStyle(stash_style);
    return MP_OBJ_FROM_PTR(self);
}

// -------- M5Widgets Image
typedef struct _widgets_image_obj_t {
    mp_obj_base_t base;
    LGFX_Device *gfx;
    const char *img;
    widgets_pos_t pos;
    widgets_size_t size;
}widgets_image_obj_t;

static void m5widgets_image_erase_helper(widgets_image_obj_t *self) {
    self->gfx->fillRect(self->pos.x0, self->pos.y0, self->size.w, self->size.h, _bg_color_g);
}

static bool m5widgets_image_bmp_helper(LFS2Wrapper *file, widgets_image_obj_t *self) {
    if (!file->open(self->img, LFS2_O_RDONLY)) {
        return false;
    }

    uint8_t buf[2] = {0};
    for (size_t i = 0; i < 2; i++) {
        buf[i] = file->read8();
    }
    if (buf[0] != 'B' && buf[1] != 'M') {
        return false;
    }
    m5widgets_image_erase_helper(self);
    file->seek(16, LFS2_SEEK_CUR);
    self->size.w = file->read32();
    self->size.h = file->read32();
    file->close();
    // printf("%s W:%d H:%d\r\n", self->img, self->size.w, self->size.h);
    return true;
}

static bool m5widgets_image_jpg_helper(LFS2Wrapper *file, widgets_image_obj_t *self) {
    if (!file->open(self->img, LFS2_O_RDONLY)) {
        return false;
    }
    m5widgets_image_erase_helper(self);

    uint8_t idx, result = 0;
    uint16_t value;
    while (!result) {
        if (!file->read(&idx, 1) || idx != 0xff || !file->read(&idx, 1)) {
            result = 3;
            break;
        }

        if (idx >= 0xE0 && idx <= 0xEF) {
            value = file->read16swap();
            file->seek((uint32_t)(value - 2), LFS2_SEEK_CUR);
            continue;
        }

        switch (idx)
        {
            case 0xD8:
                break;
            case 0xFE:
            case 0xDB:
            case 0xC4:
            case 0xDC:
            case 0xDD:
                value = file->read16swap();
                file->seek((uint32_t)(value - 2), LFS2_SEEK_CUR);
                break;
            case 0xC0:
                file->seek(0x03, LFS2_SEEK_CUR);
                self->size.h = (uint32_t)file->read16swap();
                self->size.w = (uint32_t)file->read16swap();
                result = 1;
                break;
            case 0xDA:
            case 0xD9:
            case 0x00:
                result = 2;
                break;
            default:
                value = file->read16swap();
                if (file->seek((uint32_t)(value - 2), LFS2_SEEK_CUR) != 0) {
                    result = 3;
                }
                break;
        }
    }
    file->close();
    // printf("%s W:%d H:%d result:%d\r\n", self->img, self->size.w, self->size.h, result);
    return result == 1? true: false;
}

static bool m5widgets_image_png_helper(LFS2Wrapper *file, widgets_image_obj_t *self) {
    if (!file->open(self->img, LFS2_O_RDONLY)) {
        return false;
    }

    uint16_t buf[2] = {0};
    for (size_t i = 0; i < 2; i++) {
        buf[i] = file->read16swap();
    }
    if ((buf[0] << 16 | buf[1]) != 0x89504E47) {
        return false;
    }
    m5widgets_image_erase_helper(self);
    file->seek(16);
    for (size_t i = 0; i < 2; i++) {
        buf[i] = file->read16swap();
    }
    self->size.w = buf[0] << 16 | buf[1];
    for (size_t i = 0; i < 2; i++) {
        buf[i] = file->read16swap();
    }
    self->size.h = buf[0] << 16 | buf[1];
    file->close();
    // printf("%s W:%d H:%d\r\n", self->img, self->size.w, self->size.h);
    return true;
}

static bool m5widgets_image_draw_helper(widgets_image_obj_t *self) {
    char ftype[5] = {0};
    for (size_t i = 0; i < 4; i++)
    {
        ftype[i] = tolower((char)self->img[i + strlen(self->img) - 4]);
    }
    ftype[4] = '\0';

    LFS2Wrapper wrapper;
    bool ret = true;
    if (strstr(ftype, "bmp") != NULL) {
        ret = m5widgets_image_bmp_helper(&wrapper, self);
        self->gfx->drawBmpFile(&wrapper, self->img, self->pos.x0, self->pos.y0, ~0u, ~0u, 0, 0, 1.0, 1.0);
    } else if ((strstr(ftype, "jpg") != NULL) || (strstr(ftype, "jpeg") != NULL)) {
        ret = m5widgets_image_jpg_helper(&wrapper, self);
        self->gfx->drawJpgFile(&wrapper, self->img, self->pos.x0, self->pos.y0, ~0u, ~0u, 0, 0, 1.0, 1.0);
    } else if (strstr(ftype, "png") != NULL) {
        ret = m5widgets_image_png_helper(&wrapper, self);
        self->gfx->drawPngFile(&wrapper, self->img, self->pos.x0, self->pos.y0, ~0u, ~0u, 0, 0, 1.0, 1.0);
    } else {
        printf("Image format was not bmp, jpg, png\r\n");
    }

    if (!ret) {
        printf("Get %s width and height failed\r\n", self->img);
    }
    return ret;
}

mp_obj_t m5widgets_image_setImage(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_img};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_img, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_image_obj_t *self = (widgets_image_obj_t *)pos_args[0];
    if (args[ARG_img].u_obj == mp_const_none) {
        return mp_const_none;
    } else {
        self->img = mp_obj_str_get_str(args[ARG_img].u_obj);
    }

    m5widgets_image_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_image_setCursor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_image_obj_t *self = (widgets_image_obj_t *)pos_args[0];
    m5widgets_image_erase_helper(self);

    self->pos.x0 = args[ARG_x].u_int;
    self->pos.y0 = args[ARG_y].u_int;
    m5widgets_image_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_image_setVisible(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_visible};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_visible, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_image_obj_t *self = (widgets_image_obj_t *)pos_args[0];
    if (args[ARG_visible].u_bool) {
        m5widgets_image_draw_helper(self);
    } else {
        m5widgets_image_erase_helper(self);
    }
    return mp_const_none;
}

mp_obj_t m5widgets_image_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum {ARG_img, ARG_x, ARG_y, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_img,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_parent, MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_image_obj_t *self = mp_obj_malloc(widgets_image_obj_t, &mp_widgets_image_type);
    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        self->gfx = (LGFX_Device *)&(M5.Display);
    } else {
        // Canvas, UserDisplay
        self->gfx = getGfx(&args[ARG_parent].u_obj);
    }

    self->pos.x0 = args[ARG_x].u_int;
    self->pos.y0 = args[ARG_y].u_int;
    self->size.w = 0;
    self->size.h = 0;

    if (args[ARG_img].u_obj == mp_const_none) {
        self->img = "res/img/default.png";
    } else {
        self->img = mp_obj_str_get_str(args[ARG_img].u_obj);
    }
    m5widgets_image_draw_helper(self);
    return MP_OBJ_FROM_PTR(self);
}

// -------- M5Widgets Line
typedef struct _widgets_line_obj_t {
    mp_obj_base_t base;
    LGFX_Device *gfx;
    widgets_pos_t pos;
    widgets_size_t size;
    widgets_color_t color;
}widgets_line_obj_t;

static void m5widgets_line_erase_helper(const widgets_line_obj_t *self) {
    self->gfx->drawLine(self->pos.x0, self->pos.y0, self->pos.x1, self->pos.y1, _bg_color_g);
}

static void m5widgets_line_draw_helper(const widgets_line_obj_t *self) {
    uint32_t stash_color = self->gfx->getRawColor();
    self->gfx->drawLine(self->pos.x0, self->pos.y0, self->pos.x1, self->pos.y1, self->color.fg_color);
    self->gfx->setRawColor(stash_color);
}

mp_obj_t m5widgets_line_setColor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_color};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_color, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_line_obj_t *self = (widgets_line_obj_t *)pos_args[0];

    self->color.fg_color = args[ARG_color].u_int;
    m5widgets_line_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_line_setPoints(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x0, ARG_y0, ARG_x1, ARG_y1};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x0, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y0, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_x1, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y1, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_line_obj_t *self = (widgets_line_obj_t *)pos_args[0];
    m5widgets_line_erase_helper(self);

    self->pos.x0 = args[ARG_x0].u_int;
    self->pos.y0 = args[ARG_y0].u_int;
    self->pos.x1 = args[ARG_x1].u_int;
    self->pos.y1 = args[ARG_y1].u_int;
    m5widgets_line_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_line_setVisible(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_visible};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_visible, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_line_obj_t *self = (widgets_line_obj_t *)pos_args[0];
    if (args[ARG_visible].u_bool) {
        m5widgets_line_draw_helper(self);
    } else {
        m5widgets_line_erase_helper(self);
    }
    return mp_const_none;
}

mp_obj_t m5widgets_line_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum {ARG_x0, ARG_y0, ARG_x1, ARG_y1, ARG_color, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x0,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y0,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_x1,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y1,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_color,  MP_ARG_INT                  , {.u_int = 0xFFFFFF } },
        { MP_QSTR_parent, MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_line_obj_t *self = mp_obj_malloc(widgets_line_obj_t, &mp_widgets_line_type);
    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        self->gfx = (LGFX_Device *)&(M5.Display);
    } else {
        // Canvas, UserDisplay
        self->gfx = getGfx(&args[ARG_parent].u_obj);
    }

    self->pos.x0 = args[ARG_x0].u_int;
    self->pos.y0 = args[ARG_y0].u_int;
    self->pos.x1 = args[ARG_x1].u_int;
    self->pos.y1 = args[ARG_y1].u_int;
    self->color.fg_color = args[ARG_color].u_int;
    m5widgets_line_draw_helper(self);
    return MP_OBJ_FROM_PTR(self);
}

// -------- M5Widgets Circle
typedef struct _widgets_circle_obj_t {
    mp_obj_base_t base;
    LGFX_Device *gfx;
    widgets_pos_t pos;
    widgets_size_t size;
    widgets_color_t color;
}widgets_circle_obj_t;

static void m5widgets_circle_erase_helper(const widgets_circle_obj_t *self) {
    self->gfx->fillCircle(self->pos.x0, self->pos.y0, self->size.r0, _bg_color_g);
}

static void m5widgets_circle_draw_helper(const widgets_circle_obj_t *self) {
    uint32_t stash_color = self->gfx->getRawColor();
    self->gfx->fillCircle(self->pos.x0, self->pos.y0, self->size.r0, self->color.bg_color);
    self->gfx->drawCircle(self->pos.x0, self->pos.y0, self->size.r0, self->color.fg_color);
    self->gfx->setRawColor(stash_color);
}

mp_obj_t m5widgets_circle_setRadius(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_r};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_r, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_circle_obj_t *self = (widgets_circle_obj_t *)pos_args[0];
    m5widgets_circle_erase_helper(self);

    self->size.r0 = args[ARG_r].u_int;
    m5widgets_circle_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_circle_setCursor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_circle_obj_t *self = (widgets_circle_obj_t *)pos_args[0];
    m5widgets_circle_erase_helper(self);

    self->pos.x0 = args[ARG_x].u_int;
    self->pos.y0 = args[ARG_y].u_int;
    m5widgets_circle_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_circle_setColor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_color, ARG_fill_c};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_color,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0xFFFFFF } },
        { MP_QSTR_fill_c, MP_ARG_INT                  , {.u_int = 0x000000 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_circle_obj_t *self = (widgets_circle_obj_t *)pos_args[0];
    self->color.fg_color = args[ARG_color].u_int;
    self->color.bg_color = args[ARG_fill_c].u_int;
    m5widgets_circle_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_circle_setVisible(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_visible};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_visible, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_circle_obj_t *self = (widgets_circle_obj_t *)pos_args[0];
    if (args[ARG_visible].u_bool) {
        m5widgets_circle_draw_helper(self);
    } else {
        m5widgets_circle_erase_helper(self);
    }
    return mp_const_none;
}

mp_obj_t m5widgets_circle_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum {ARG_x, ARG_y, ARG_r, ARG_color, ARG_fill_c, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_r,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_color,  MP_ARG_INT                  , {.u_int = 0xFFFFFF } },
        { MP_QSTR_fill_c, MP_ARG_INT                  , {.u_int = 0x000000 } },
        { MP_QSTR_parent, MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_circle_obj_t *self = mp_obj_malloc(widgets_circle_obj_t, &mp_widgets_circle_type);
    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        self->gfx = (LGFX_Device *)&(M5.Display);
    } else {
        // Canvas, UserDisplay
        self->gfx = getGfx(&args[ARG_parent].u_obj);
    }

    self->pos.x0 = args[ARG_x].u_int;
    self->pos.y0 = args[ARG_y].u_int;
    self->size.r0 = args[ARG_r].u_int;
    self->color.fg_color = args[ARG_color].u_int;
    self->color.bg_color = args[ARG_fill_c].u_int;
    m5widgets_circle_draw_helper(self);
    return MP_OBJ_FROM_PTR(self);
}

// -------- M5Widgets Rectangle
typedef struct _widgets_rectangle_obj_t {
    mp_obj_base_t base;
    LGFX_Device *gfx;
    widgets_pos_t pos;
    widgets_size_t size;
    widgets_color_t color;
}widgets_rectangle_obj_t;

static void m5widgets_rectangle_erase_helper(const widgets_rectangle_obj_t *self) {
    self->gfx->fillRect(self->pos.x0, self->pos.y0, self->size.w, self->size.h, _bg_color_g);
}

static void m5widgets_rectangle_draw_helper(const widgets_rectangle_obj_t *self) {
    uint32_t stash_color = self->gfx->getRawColor();
    self->gfx->fillRect(self->pos.x0, self->pos.y0, self->size.w, self->size.h, self->color.bg_color);
    self->gfx->drawRect(self->pos.x0, self->pos.y0, self->size.w, self->size.h, self->color.fg_color);
    self->gfx->setRawColor(stash_color);
}

mp_obj_t m5widgets_rectangle_setSize(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_w, ARG_h};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_w, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_h, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_rectangle_obj_t *self = (widgets_rectangle_obj_t *)pos_args[0];

    m5widgets_rectangle_erase_helper(self);

    self->size.w = args[ARG_w].u_int;
    self->size.h = args[ARG_h].u_int;

    m5widgets_rectangle_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_rectangle_setColor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_color, ARG_fill_c};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_color,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0xFFFFFF } },
        { MP_QSTR_fill_c, MP_ARG_INT                  , {.u_int = 0x000000 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_rectangle_obj_t *self = (widgets_rectangle_obj_t *)pos_args[0];
    m5widgets_rectangle_erase_helper(self);

    self->color.fg_color = args[ARG_color].u_int;
    self->color.bg_color = args[ARG_fill_c].u_int;
    m5widgets_rectangle_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_rectangle_setCursor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y, MP_ARG_INT                  , {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_rectangle_obj_t *self = (widgets_rectangle_obj_t *)pos_args[0];
    m5widgets_rectangle_erase_helper(self);

    self->pos.x0 = args[ARG_x].u_int;
    self->pos.y0 = args[ARG_y].u_int;
    m5widgets_rectangle_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_rectangle_setVisible(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_visible};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_visible, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_rectangle_obj_t *self = (widgets_rectangle_obj_t *)pos_args[0];
    if (args[ARG_visible].u_bool) {
        m5widgets_rectangle_draw_helper(self);
    } else {
        m5widgets_rectangle_erase_helper(self);
    }
    return mp_const_none;
}

mp_obj_t m5widgets_rectangle_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum {ARG_x, ARG_y, ARG_w, ARG_h, ARG_color, ARG_fill_c, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_w,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_h,      MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_color,  MP_ARG_INT                  , {.u_int = 0xFFFFFF } },
        { MP_QSTR_fill_c, MP_ARG_INT                  , {.u_int = 0x000000 } },
        { MP_QSTR_parent, MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_rectangle_obj_t *self = mp_obj_malloc(widgets_rectangle_obj_t, &mp_widgets_rectangle_type);
    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        self->gfx = (LGFX_Device *)&(M5.Display);
    } else {
        // Canvas, UserDisplay
        self->gfx = getGfx(&args[ARG_parent].u_obj);
    }

    self->pos.x0 = args[ARG_x].u_int;
    self->pos.y0 = args[ARG_y].u_int;
    self->size.w = args[ARG_w].u_int;
    self->size.h = args[ARG_h].u_int;
    self->color.fg_color = args[ARG_color].u_int;
    self->color.bg_color = args[ARG_fill_c].u_int;
    m5widgets_rectangle_draw_helper(self);
    return MP_OBJ_FROM_PTR(self);
}

// -------- M5Widgets Triangle
typedef struct _widgets_triangle_obj_t {
    mp_obj_base_t base;
    LGFX_Device *gfx;
    widgets_pos_t pos;
    widgets_size_t size;
    widgets_color_t color;
}widgets_triangle_obj_t;

static void m5widgets_triangle_erase_helper(const widgets_triangle_obj_t *self) {
    self->gfx->fillTriangle(self->pos.x0, self->pos.y0, self->pos.x1, self->pos.y1, self->pos.x2, self->pos.y2, _bg_color_g);
}

static void m5widgets_triangle_draw_helper(const widgets_triangle_obj_t *self) {
    uint32_t stash_color = self->gfx->getRawColor();
    self->gfx->fillTriangle(self->pos.x0, self->pos.y0, self->pos.x1, self->pos.y1, self->pos.x2, self->pos.y2, self->color.bg_color);
    self->gfx->drawTriangle(self->pos.x0, self->pos.y0, self->pos.x1, self->pos.y1, self->pos.x2, self->pos.y2, self->color.fg_color);
    self->gfx->setRawColor(stash_color);
}

mp_obj_t m5widgets_triangle_setColor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_color, ARG_fill_c};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_color,  MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0xFFFFFF } },
        { MP_QSTR_fill_c, MP_ARG_INT                  , {.u_int = 0x000000 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_triangle_obj_t *self = (widgets_triangle_obj_t *)pos_args[0];
    m5widgets_triangle_erase_helper(self);

    self->color.fg_color = args[ARG_color].u_int;
    self->color.bg_color = args[ARG_fill_c].u_int;
    m5widgets_triangle_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_triangle_setPoints(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x0, ARG_y0, ARG_x1, ARG_y1, ARG_x2, ARG_y2};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x0,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y0,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_x1,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y1,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_x2,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y2,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_triangle_obj_t *self = (widgets_triangle_obj_t *)pos_args[0];
    m5widgets_triangle_erase_helper(self);

    self->pos.x0 = args[ARG_x0].u_int;
    self->pos.y0 = args[ARG_y0].u_int;
    self->pos.x1 = args[ARG_x1].u_int;
    self->pos.y1 = args[ARG_y1].u_int;
    self->pos.x2 = args[ARG_x2].u_int;
    self->pos.y2 = args[ARG_y2].u_int;
    m5widgets_triangle_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_triangle_setVisible(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_visible};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_visible, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_triangle_obj_t *self = (widgets_triangle_obj_t *)pos_args[0];
    if (args[ARG_visible].u_bool) {
        m5widgets_triangle_draw_helper(self);
    } else {
        m5widgets_triangle_erase_helper(self);
    }
    return mp_const_none;
}

mp_obj_t m5widgets_triangle_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum {ARG_x0, ARG_y0, ARG_x1, ARG_y1, ARG_x2, ARG_y2, ARG_color, ARG_fill_c, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x0,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y0,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_x1,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y1,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_x2,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y2,     MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_color,  MP_ARG_INT                  , {.u_int = 0xFFFFFF } },
        { MP_QSTR_fill_c, MP_ARG_INT                  , {.u_int = 0x000000 } },
        { MP_QSTR_parent, MP_ARG_OBJ                  , {.u_obj =  mp_const_none} },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_triangle_obj_t *self = mp_obj_malloc(widgets_triangle_obj_t, &mp_widgets_triangle_type);
    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        self->gfx = (LGFX_Device *)&(M5.Display);
    } else {
        // Canvas, UserDisplay
        self->gfx = getGfx(&args[ARG_parent].u_obj);
    }

    self->pos.x0 = args[ARG_x0].u_int;
    self->pos.y0 = args[ARG_y0].u_int;
    self->pos.x1 = args[ARG_x1].u_int;
    self->pos.y1 = args[ARG_y1].u_int;
    self->pos.x2 = args[ARG_x2].u_int;
    self->pos.y2 = args[ARG_y2].u_int;
    self->color.fg_color = args[ARG_color].u_int;
    self->color.bg_color = args[ARG_fill_c].u_int;
    m5widgets_triangle_draw_helper(self);
    return MP_OBJ_FROM_PTR(self);
}

// -------- M5Widgets QRCode
typedef struct _widgets_qrcode_obj_t {
    mp_obj_base_t base;
    LGFX_Device *gfx;
    const char *text;
    widgets_pos_t pos;
    widgets_size_t size;
    uint8_t version;
}widgets_qrcode_obj_t;

static void m5widgets_qrcode_erase_helper(const widgets_qrcode_obj_t *self) {
    self->gfx->fillRect(self->pos.x0, self->pos.y0, self->size.w, self->size.w, _bg_color_g);
}

static void m5widgets_qrcode_draw_helper(const widgets_qrcode_obj_t *self) {
    uint32_t stash_color = self->gfx->getRawColor();
    self->gfx->qrcode(self->text, self->pos.x0, self->pos.y0, self->size.w, self->version);
    self->gfx->setRawColor(stash_color);
}

mp_obj_t m5widgets_qrcode_setText(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_text};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text, MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_qrcode_obj_t *self = (widgets_qrcode_obj_t *)pos_args[0];

    const char *new_text = mp_obj_str_get_str(args[ARG_text].u_obj);
    if (strcmp(self->text, new_text) == 0) {
        return mp_const_none;
    }
    m5widgets_qrcode_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_qrcode_setSize(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_w};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_w, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_qrcode_obj_t *self = (widgets_qrcode_obj_t *)pos_args[0];
    self->size.w = args[ARG_w].u_int;
    m5widgets_qrcode_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_qrcode_setVersion(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_version};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_version, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_qrcode_obj_t *self = (widgets_qrcode_obj_t *)pos_args[0];
    self->version = args[ARG_version].u_int;
    m5widgets_qrcode_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_qrcode_setCursor(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_x, ARG_y};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_x, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y, MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_qrcode_obj_t *self = (widgets_qrcode_obj_t *)pos_args[0];
    self->pos.x0 = args[ARG_x].u_int;
    self->pos.y0 = args[ARG_y].u_int;
    m5widgets_qrcode_draw_helper(self);
    return mp_const_none;
}

mp_obj_t m5widgets_qrcode_setVisible(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    enum {ARG_visible};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_visible, MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = true } }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_qrcode_obj_t *self = (widgets_qrcode_obj_t *)pos_args[0];
    if (args[ARG_visible].u_bool) {
        m5widgets_qrcode_draw_helper(self);
    } else {
        m5widgets_qrcode_erase_helper(self);
    }
    return mp_const_none;
}

mp_obj_t m5widgets_qrcode_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    enum {ARG_text, ARG_x, ARG_y, ARG_w, ARG_version, ARG_parent};
    /* *FORMAT-OFF* */
    const mp_arg_t allowed_args[] = {
        { MP_QSTR_text,    MP_ARG_OBJ | MP_ARG_REQUIRED, {.u_obj = mp_const_none } },
        { MP_QSTR_x,       MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_y,       MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_w,       MP_ARG_INT | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_version, MP_ARG_INT                  , {.u_int = 1 } },
        { MP_QSTR_parent,  MP_ARG_OBJ                  , {.u_obj =  mp_const_none} }
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    widgets_qrcode_obj_t *self = mp_obj_malloc(widgets_qrcode_obj_t, &mp_widgets_qrcode_type);
    if (args[ARG_parent].u_obj == mp_const_none) {
        // default Display
        self->gfx = (LGFX_Device *)&(M5.Display);
    } else {
        // Canvas, UserDisplay
        self->gfx = getGfx(&args[ARG_parent].u_obj);
    }

    if (args[ARG_text].u_obj == mp_const_none) {
        self->text = "QRCode";
    } else {
        self->text = mp_obj_str_get_str(args[ARG_text].u_obj);
    }

    self->pos.x0 = args[ARG_x].u_int;
    self->pos.y0 = args[ARG_y].u_int;
    self->size.w = args[ARG_w].u_int;
    self->version = args[ARG_version].u_int;
    m5widgets_qrcode_draw_helper(self);
    return MP_OBJ_FROM_PTR(self);
}
}

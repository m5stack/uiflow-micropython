#include "m5unified.h"

// -------- stream function
extern mp_uint_t gfx_read(mp_obj_t self_in, void *buf, mp_uint_t size, int *errcode);
extern mp_uint_t gfx_write(mp_obj_t self_in, const void *buf, mp_uint_t size, int *errcode);
extern mp_uint_t gfx_ioctl(mp_obj_t self, mp_uint_t request, uintptr_t arg, int *errcode);

// -------- user define panel
extern mp_obj_t user_panel_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args);

// -------- lvgl port funciton
#if MICROPY_PY_LVGL
extern void gfx_lvgl_flush(void *_disp_drv, const lv_area_t *area, lv_color_t *color_p);
extern void user_lvgl_flush(void *_disp_drv, const lv_area_t *area, lv_color_t *color_p);
extern bool gfx_lvgl_touch_read(lv_indev_drv_t *indev_drv, lv_indev_data_t *data);
DEFINE_PTR_OBJ(gfx_lvgl_flush);
DEFINE_PTR_OBJ(user_lvgl_flush);
DEFINE_PTR_OBJ(gfx_lvgl_touch_read);
#endif

// -------- GFX common wrapper
MAKE_METHOD_0(gfx, width);
MAKE_METHOD_0(gfx, height);
MAKE_METHOD_0(gfx, getRotation);
MAKE_METHOD_0(gfx, getColorDepth);
MAKE_METHOD_0(gfx, getCursor);
MAKE_METHOD_KW(gfx, setRotation, 1);
MAKE_METHOD_KW(gfx, setColorDepth, 1);
MAKE_METHOD_KW(gfx, setFont, 1);
MAKE_METHOD_KW(gfx, setTextColor, 1);
MAKE_METHOD_KW(gfx, setTextScroll, 1);
MAKE_METHOD_KW(gfx, setTextSize, 1);
MAKE_METHOD_KW(gfx, textWidth, 1);
MAKE_METHOD_KW(gfx, fontHeight, 1);
MAKE_METHOD_KW(gfx, setCursor, 1);
MAKE_METHOD_KW(gfx, setBrightness, 1);
MAKE_METHOD_KW(gfx, clear, 1);
MAKE_METHOD_KW(gfx, fillScreen, 1);
MAKE_METHOD_KW(gfx, drawPixel, 1);
MAKE_METHOD_KW(gfx, drawCircle, 1);
MAKE_METHOD_KW(gfx, fillCircle, 1);
MAKE_METHOD_KW(gfx, drawEllipse, 1);
MAKE_METHOD_KW(gfx, fillEllipse, 1);
MAKE_METHOD_KW(gfx, drawLine, 1);
MAKE_METHOD_KW(gfx, drawRect, 1);
MAKE_METHOD_KW(gfx, fillRect, 1);
MAKE_METHOD_KW(gfx, drawRoundRect, 1);
MAKE_METHOD_KW(gfx, fillRoundRect, 1);
MAKE_METHOD_KW(gfx, drawTriangle, 1);
MAKE_METHOD_KW(gfx, fillTriangle, 1);
MAKE_METHOD_KW(gfx, drawArc, 1);
MAKE_METHOD_KW(gfx, fillArc, 1);
MAKE_METHOD_KW(gfx, drawEllipseArc, 1);
MAKE_METHOD_KW(gfx, fillEllipseArc, 1);
MAKE_METHOD_KW(gfx, drawQR, 1);
MAKE_METHOD_KW(gfx, drawJpg, 1);
MAKE_METHOD_KW(gfx, drawPng, 1);
MAKE_METHOD_KW(gfx, drawBmp, 1);
MAKE_METHOD_KW(gfx, drawImage, 1);
MAKE_METHOD_KW(gfx, drawRawBuf, 1);
MAKE_METHOD_KW(gfx, drawString, 1);
MAKE_METHOD_KW(gfx, drawCenterString, 1);
MAKE_METHOD_KW(gfx, print, 1);
MAKE_METHOD_V(gfx, printf, 2, 32);
MAKE_METHOD_KW(gfx, newCanvas, 1);
#if MICROPY_PY_LVGL
MAKE_METHOD_0(gfx, lvgl_init);
MAKE_METHOD_0(gfx, lvgl_deinit);
#endif

#define TABLE_PARTS_GFX_BASE \
    MAKE_TABLE(gfx, height), \
    MAKE_TABLE(gfx, width), \
    MAKE_TABLE(gfx, getRotation), \
    MAKE_TABLE(gfx, getColorDepth), \
    MAKE_TABLE(gfx, getCursor), \
    MAKE_TABLE(gfx, setRotation), \
    MAKE_TABLE(gfx, setColorDepth), \
    MAKE_TABLE(gfx, setFont), \
    MAKE_TABLE(gfx, setTextColor), \
    MAKE_TABLE(gfx, setTextScroll), \
    MAKE_TABLE(gfx, setTextSize), \
    MAKE_TABLE(gfx, textWidth), \
    MAKE_TABLE(gfx, fontHeight), \
    MAKE_TABLE(gfx, setCursor), \
    MAKE_TABLE(gfx, setBrightness), \
    MAKE_TABLE(gfx, clear), \
    MAKE_TABLE(gfx, fillScreen), \
    MAKE_TABLE(gfx, drawPixel), \
    MAKE_TABLE(gfx, drawCircle), \
    MAKE_TABLE(gfx, fillCircle), \
    MAKE_TABLE(gfx, drawEllipse), \
    MAKE_TABLE(gfx, fillEllipse), \
    MAKE_TABLE(gfx, drawLine), \
    MAKE_TABLE(gfx, drawRect), \
    MAKE_TABLE(gfx, fillRect), \
    MAKE_TABLE(gfx, drawRoundRect), \
    MAKE_TABLE(gfx, fillRoundRect), \
    MAKE_TABLE(gfx, drawTriangle), \
    MAKE_TABLE(gfx, fillTriangle), \
    MAKE_TABLE(gfx, drawArc), \
    MAKE_TABLE(gfx, fillArc), \
    MAKE_TABLE(gfx, drawEllipseArc), \
    MAKE_TABLE(gfx, fillEllipseArc), \
    MAKE_TABLE(gfx, drawQR), \
    MAKE_TABLE(gfx, drawJpg), \
    MAKE_TABLE(gfx, drawPng), \
    MAKE_TABLE(gfx, drawBmp), \
    MAKE_TABLE(gfx, drawImage), \
    MAKE_TABLE(gfx, drawRawBuf), \
    MAKE_TABLE(gfx, drawString), \
    MAKE_TABLE(gfx, drawCenterString), \
    MAKE_TABLE(gfx, print), \
    MAKE_TABLE(gfx, printf), \
    MAKE_TABLE(gfx, newCanvas)

// -------- GFX device wrapper
MAKE_METHOD_0(gfx, startWrite);
MAKE_METHOD_0(gfx, endWrite);

STATIC const mp_rom_map_elem_t fonts_member_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_ASCII7),    MP_ROM_PTR(&gfx_font_0_obj) },
    { MP_ROM_QSTR(MP_QSTR_DejaVu9),   MP_ROM_PTR(&gfx_font_DejaVu9_obj) },
    { MP_ROM_QSTR(MP_QSTR_DejaVu12),  MP_ROM_PTR(&gfx_font_DejaVu12_obj) },
    { MP_ROM_QSTR(MP_QSTR_DejaVu18),  MP_ROM_PTR(&gfx_font_DejaVu18_obj) },
    { MP_ROM_QSTR(MP_QSTR_DejaVu24),  MP_ROM_PTR(&gfx_font_DejaVu24_obj) },
    { MP_ROM_QSTR(MP_QSTR_DejaVu40),  MP_ROM_PTR(&gfx_font_DejaVu40_obj) },
    { MP_ROM_QSTR(MP_QSTR_DejaVu56),  MP_ROM_PTR(&gfx_font_DejaVu56_obj) },
    { MP_ROM_QSTR(MP_QSTR_DejaVu72),  MP_ROM_PTR(&gfx_font_DejaVu72_obj) },
    { MP_ROM_QSTR(MP_QSTR_EFontCN24), MP_ROM_PTR(&gfx_font_efontCN_24_obj) },
    { MP_ROM_QSTR(MP_QSTR_EFontJA24), MP_ROM_PTR(&gfx_font_efontJA_24_obj) },
    { MP_ROM_QSTR(MP_QSTR_EFontKR24), MP_ROM_PTR(&gfx_font_efontKR_24_obj) },
    { MP_ROM_QSTR(MP_QSTR_Montserrat6), MP_ROM_PTR(&gfx_font_montserrat_6_obj)},
    // { MP_ROM_QSTR(MP_QSTR_Montserrat7), MP_ROM_PTR(&gfx_font_montserrat_7_obj)},
    { MP_ROM_QSTR(MP_QSTR_Montserrat8), MP_ROM_PTR(&gfx_font_montserrat_8_obj)},
    { MP_ROM_QSTR(MP_QSTR_Montserrat9), MP_ROM_PTR(&gfx_font_montserrat_9_obj)},
    // { MP_ROM_QSTR(MP_QSTR_Montserrat10), MP_ROM_PTR(&gfx_font_montserrat_10_obj)},
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(fonts_member, fonts_member_table);
const mp_obj_type_t mp_fonts_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Fonts,
    .locals_dict = (mp_obj_dict_t *)&fonts_member,
};

STATIC const mp_rom_map_elem_t color_pre_define_members_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_BLACK),       MP_ROM_INT(0x000000) },
    { MP_ROM_QSTR(MP_QSTR_NAVY),        MP_ROM_INT(0x000080) },
    { MP_ROM_QSTR(MP_QSTR_DARKGREEN),   MP_ROM_INT(0x008000) },
    { MP_ROM_QSTR(MP_QSTR_DARKCYAN),    MP_ROM_INT(0x008080) },
    { MP_ROM_QSTR(MP_QSTR_MAROON),      MP_ROM_INT(0x800000) },
    { MP_ROM_QSTR(MP_QSTR_PURPLE),      MP_ROM_INT(0x800080) },
    { MP_ROM_QSTR(MP_QSTR_OLIVE),       MP_ROM_INT(0x808000) },
    { MP_ROM_QSTR(MP_QSTR_LIGHTGREY),   MP_ROM_INT(0xC0C0C0) },
    { MP_ROM_QSTR(MP_QSTR_DARKGREY),    MP_ROM_INT(0x808080) },
    { MP_ROM_QSTR(MP_QSTR_BLUE),        MP_ROM_INT(0x0000FF) },
    { MP_ROM_QSTR(MP_QSTR_GREEN),       MP_ROM_INT(0x00FF00) },
    { MP_ROM_QSTR(MP_QSTR_CYAN),        MP_ROM_INT(0x00FFFF) },
    { MP_ROM_QSTR(MP_QSTR_RED),         MP_ROM_INT(0xFF0000) },
    { MP_ROM_QSTR(MP_QSTR_MAGENTA),     MP_ROM_INT(0xFF00FF) },
    { MP_ROM_QSTR(MP_QSTR_YELLOW),      MP_ROM_INT(0xFFFF00) },
    { MP_ROM_QSTR(MP_QSTR_WHITE),       MP_ROM_INT(0xFFFFFF) },
    { MP_ROM_QSTR(MP_QSTR_ORANGE),      MP_ROM_INT(0xFFA500) },
    { MP_ROM_QSTR(MP_QSTR_GREENYELLOW), MP_ROM_INT(0xADFF2F) },
    { MP_ROM_QSTR(MP_QSTR_PINK),        MP_ROM_INT(0xFFC0CB) }
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(color_pre_define_members, color_pre_define_members_table);
const mp_obj_type_t mp_color_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Color,
    .locals_dict = (mp_obj_dict_t *)&color_pre_define_members,
};

STATIC const mp_rom_map_elem_t gfxdevice_member_table[] = {
    TABLE_PARTS_GFX_BASE,
    MAKE_TABLE(gfx, startWrite),
    MAKE_TABLE(gfx, endWrite),
    // fonts
    { MP_ROM_QSTR(MP_QSTR_FONTS),           MP_OBJ_FROM_PTR(&mp_fonts_type) },
    // colors
    { MP_ROM_QSTR(MP_QSTR_COLOR),           MP_OBJ_FROM_PTR(&mp_color_type) },
    // stream function
    { MP_ROM_QSTR(MP_QSTR_read),            MP_ROM_PTR(&mp_stream_read_obj) },
    { MP_ROM_QSTR(MP_QSTR_write),           MP_ROM_PTR(&mp_stream_write_obj) },
    { MP_ROM_QSTR(MP_QSTR_close),           MP_ROM_PTR(&mp_stream_close_obj) },
    #if MICROPY_PY_LVGL
    // lvgl port function
    { MP_ROM_QSTR(MP_QSTR_lvgl_init),       MP_ROM_PTR(&gfx_lvgl_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_lvgl_deinit),     MP_ROM_PTR(&gfx_lvgl_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR_lvgl_flush),      MP_ROM_PTR(&PTR_OBJ(gfx_lvgl_flush)) },
    { MP_ROM_QSTR(MP_QSTR_lvgl_read),       MP_ROM_PTR(&PTR_OBJ(gfx_lvgl_touch_read)) },
    { MP_ROM_QSTR(MP_QSTR_user_lvgl_flush), MP_ROM_PTR(&PTR_OBJ(user_lvgl_flush)) },
    #endif
};
STATIC MP_DEFINE_CONST_DICT(gfxdevice_member, gfxdevice_member_table);

STATIC const mp_rom_map_elem_t user_panel_types_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_ILI9342),      MP_ROM_INT(SPI_LCD_ILI9342) },
    { MP_ROM_QSTR(MP_QSTR_ST7735),       MP_ROM_INT(SPI_LCD_ST7735) },
    { MP_ROM_QSTR(MP_QSTR_ST7735S),      MP_ROM_INT(SPI_LCD_ST7735S) },
    { MP_ROM_QSTR(MP_QSTR_ST7789),       MP_ROM_INT(SPI_LCD_ST7789) },
    { MP_ROM_QSTR(MP_QSTR_GC9A01),       MP_ROM_INT(SPI_LCD_GC9A01) },
    { MP_ROM_QSTR(MP_QSTR_GC9107),       MP_ROM_INT(SPI_LCD_GC9107) },
    { MP_ROM_QSTR(MP_QSTR_GDEW0154M09),  MP_ROM_INT(SPI_EINK_GDEW0154M09) },
    { MP_ROM_QSTR(MP_QSTR_IT8951),       MP_ROM_INT(SPI_EINK_IT8951) },
    { MP_ROM_QSTR(MP_QSTR_SSD1306),      MP_ROM_INT(I2C_OLED_SSD1306) },
    { MP_ROM_QSTR(MP_QSTR_SH110x),       MP_ROM_INT(I2C_OLED_SH110x) },
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(user_panel_types, user_panel_types_table);
const mp_obj_type_t mp_user_panel_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Panel,
    .locals_dict = (mp_obj_dict_t *)&user_panel_types,
};

STATIC const mp_rom_map_elem_t user_touch_types_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_FT5X06),      MP_ROM_INT(I2C_TP_FT5X06) },
    { MP_ROM_QSTR(MP_QSTR_GT911),       MP_ROM_INT(I2C_TP_GT911) },
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(user_touch_types, user_touch_types_table);
const mp_obj_type_t mp_user_touch_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Touch,
    .locals_dict = (mp_obj_dict_t *)&user_touch_types,
};

STATIC const mp_rom_map_elem_t gfxuserdevice_member_table[] = {
    TABLE_PARTS_GFX_BASE,
    MAKE_TABLE(gfx, startWrite),
    MAKE_TABLE(gfx, endWrite),
    // font
    { MP_ROM_QSTR(MP_QSTR_FONTS),           MP_ROM_PTR(&mp_fonts_type) },
    // color
    { MP_ROM_QSTR(MP_QSTR_COLOR),           MP_ROM_PTR(&mp_color_type) },
    // Panel
    { MP_ROM_QSTR(MP_QSTR_PANEL),           MP_ROM_PTR(&mp_user_panel_type) },
    // Touch
    { MP_ROM_QSTR(MP_QSTR_TOUCH),           MP_ROM_PTR(&mp_user_touch_type) },
    // stream function
    { MP_ROM_QSTR(MP_QSTR_read),            MP_ROM_PTR(&mp_stream_read_obj) },
    { MP_ROM_QSTR(MP_QSTR_write),           MP_ROM_PTR(&mp_stream_write_obj) },
    { MP_ROM_QSTR(MP_QSTR_close),           MP_ROM_PTR(&mp_stream_close_obj) },
    #if MICROPY_PY_LVGL
    // lvgl port function
    { MP_ROM_QSTR(MP_QSTR_lvgl_init),       MP_ROM_PTR(&gfx_lvgl_init_obj) },
    { MP_ROM_QSTR(MP_QSTR_lvgl_deinit),     MP_ROM_PTR(&gfx_lvgl_deinit_obj) },
    { MP_ROM_QSTR(MP_QSTR_lvgl_flush),      MP_ROM_PTR(&PTR_OBJ(gfx_lvgl_flush)) },
    { MP_ROM_QSTR(MP_QSTR_lvgl_read),       MP_ROM_PTR(&PTR_OBJ(gfx_lvgl_touch_read)) },
    { MP_ROM_QSTR(MP_QSTR_user_lvgl_flush), MP_ROM_PTR(&PTR_OBJ(user_lvgl_flush)) },
    #endif
};
STATIC MP_DEFINE_CONST_DICT(gfxuserdevice_member, gfxuserdevice_member_table);

// -------- GFX stream function
STATIC const mp_stream_p_t mp_gfx_stream_p = {
    .read = gfx_read,
    .write = gfx_write,
    .ioctl = gfx_ioctl,
};

// -------- GFX canvas wrapper
MAKE_METHOD_0(gfx, delete);
MAKE_METHOD_2(gfx, push);

// -------- GFX canvas function
STATIC const mp_rom_map_elem_t gfxcanvas_member_table[] = {
    TABLE_PARTS_GFX_BASE,
    MAKE_TABLE(gfx, delete),
    MAKE_TABLE(gfx, push),
};
STATIC MP_DEFINE_CONST_DICT(gfxcanvas_member, gfxcanvas_member_table);

// -------- GFX canvas panel class
const mp_obj_type_t mp_gfxcanvas_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Canvas,
    .flags = MP_TYPE_FLAG_IS_SUBCLASSED,
    .protocol = &mp_gfx_stream_p,
    .locals_dict = (mp_obj_dict_t *)&gfxcanvas_member,
};

// -------- GFX user panel class
const mp_obj_type_t m5_user_display = {
    .base = { &mp_type_type },
    .name = MP_QSTR_UserDisplay,
    .protocol = &mp_gfx_stream_p,
    .make_new = user_panel_make_new,
    .locals_dict = (mp_obj_dict_t *)&gfxuserdevice_member,
};

// -------- GFX panel class
const mp_obj_type_t mp_gfxdevice_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_Display,
    .protocol = &mp_gfx_stream_p,
    .locals_dict = (mp_obj_dict_t *)&gfxdevice_member,
};

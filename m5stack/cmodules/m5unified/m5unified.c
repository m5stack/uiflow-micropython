#include <mpy_m5unified.h>

/* *FORMAT-OFF* */
#define MAKE_METHOD_V(prefix, func, arg_min, arg_max) extern mp_obj_t prefix##_##func(size_t,const mp_obj_t*); STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN( prefix##_##func##_obj, arg_min, arg_max, prefix##_##func ); 
#define MAKE_METHOD_0(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t                  ); STATIC MP_DEFINE_CONST_FUN_OBJ_1( prefix##_##func##_obj, prefix##_##func );
#define MAKE_METHOD_1(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t,mp_obj_t         ); STATIC MP_DEFINE_CONST_FUN_OBJ_2( prefix##_##func##_obj, prefix##_##func );
#define MAKE_METHOD_2(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t,mp_obj_t,mp_obj_t); STATIC MP_DEFINE_CONST_FUN_OBJ_3( prefix##_##func##_obj, prefix##_##func );
#define MAKE_METHOD_KW(prefix, func, args) extern mp_obj_t prefix##_##func(size_t,const mp_obj_t*,mp_map_t*); STATIC MP_DEFINE_CONST_FUN_OBJ_KW( prefix##_##func##_obj, args, prefix##_##func ); 
/* *FORMAT-ON* */

#define MAKE_TABLE(prefix, func) \
    { MP_ROM_QSTR(MP_QSTR_##func), MP_ROM_PTR(&prefix##_##func##_obj) }

// stream function
extern mp_uint_t gfx_read(mp_obj_t self_in, void *buf, mp_uint_t size, int *errcode);
extern mp_uint_t gfx_write(mp_obj_t self_in, const void *buf, mp_uint_t size, int *errcode);
extern mp_uint_t gfx_ioctl(mp_obj_t self, mp_uint_t request, uintptr_t arg, int *errcode);

// -------- GFX common wrapper
MAKE_METHOD_0(gfx, width);
MAKE_METHOD_0(gfx, height);
MAKE_METHOD_0(gfx, getRotation);
MAKE_METHOD_0(gfx, getColorDepth);
MAKE_METHOD_0(gfx, getCursor);
MAKE_METHOD_1(gfx, setRotation);
MAKE_METHOD_1(gfx, setColorDepth);
MAKE_METHOD_1(gfx, setFont);
MAKE_METHOD_1(gfx, setTextColor);
MAKE_METHOD_1(gfx, setTextScroll);
MAKE_METHOD_2(gfx, setCursor);
MAKE_METHOD_V(gfx, print, 2, 3);
MAKE_METHOD_V(gfx, clear, 1, 2);
MAKE_METHOD_V(gfx, fillScreen, 1, 2);
MAKE_METHOD_V(gfx, drawPixel, 3, 4);
MAKE_METHOD_V(gfx, drawCircle, 4, 5);
MAKE_METHOD_V(gfx, fillCircle, 4, 5);
MAKE_METHOD_V(gfx, drawEllipse, 5, 6);
MAKE_METHOD_V(gfx, fillEllipse, 5, 6);
MAKE_METHOD_V(gfx, drawLine, 5, 6);
MAKE_METHOD_V(gfx, drawRect, 5, 6);
MAKE_METHOD_V(gfx, fillRect, 5, 6);
MAKE_METHOD_V(gfx, drawRoundRect, 6, 7);
MAKE_METHOD_V(gfx, fillRoundRect, 6, 7);
MAKE_METHOD_V(gfx, drawTriangle, 7, 8);
MAKE_METHOD_V(gfx, fillTriangle, 7, 8);
MAKE_METHOD_V(gfx, drawArc, 7, 8);
MAKE_METHOD_V(gfx, fillArc, 7, 8);
MAKE_METHOD_V(gfx, drawEllipseArc, 9, 10);
MAKE_METHOD_V(gfx, fillEllipseArc, 9, 10);
MAKE_METHOD_V(gfx, drawQR, 6, 6);
MAKE_METHOD_V(gfx, drawJpg, 4, 4);
MAKE_METHOD_V(gfx, drawPng, 4, 4);
MAKE_METHOD_V(gfx, drawBmp, 4, 4);
MAKE_METHOD_V(gfx, drawImage, 4, 4);
MAKE_METHOD_V(gfx, printf, 2, 32);
MAKE_METHOD_V(gfx, newCanvas, 3, 5);

#define TABLE_PARTS_GFX_BASE \
    MAKE_TABLE(gfx, clear), \
    MAKE_TABLE(gfx, drawArc), \
    MAKE_TABLE(gfx, drawCircle), \
    MAKE_TABLE(gfx, drawEllipse), \
    MAKE_TABLE(gfx, drawEllipseArc), \
    MAKE_TABLE(gfx, drawLine), \
    MAKE_TABLE(gfx, drawPixel), \
    MAKE_TABLE(gfx, drawRect), \
    MAKE_TABLE(gfx, drawRoundRect), \
    MAKE_TABLE(gfx, drawQR), \
    MAKE_TABLE(gfx, drawJpg), \
    MAKE_TABLE(gfx, drawPng), \
    MAKE_TABLE(gfx, drawBmp), \
    MAKE_TABLE(gfx, drawImage), \
    MAKE_TABLE(gfx, drawTriangle), \
    MAKE_TABLE(gfx, fillArc), \
    MAKE_TABLE(gfx, fillCircle), \
    MAKE_TABLE(gfx, fillEllipse), \
    MAKE_TABLE(gfx, fillEllipseArc), \
    MAKE_TABLE(gfx, fillRect), \
    MAKE_TABLE(gfx, fillRoundRect), \
    MAKE_TABLE(gfx, fillScreen), \
    MAKE_TABLE(gfx, fillTriangle), \
    MAKE_TABLE(gfx, getColorDepth), \
    MAKE_TABLE(gfx, getCursor), \
    MAKE_TABLE(gfx, getRotation), \
    MAKE_TABLE(gfx, height), \
    MAKE_TABLE(gfx, newCanvas), \
    MAKE_TABLE(gfx, print), \
    MAKE_TABLE(gfx, printf), \
    MAKE_TABLE(gfx, setColorDepth), \
    MAKE_TABLE(gfx, setCursor), \
    MAKE_TABLE(gfx, setFont), \
    MAKE_TABLE(gfx, setTextColor), \
    MAKE_TABLE(gfx, setTextScroll), \
    MAKE_TABLE(gfx, setRotation), \
    MAKE_TABLE(gfx, width), \
    { MP_ROM_QSTR(MP_QSTR_FONT0), MP_ROM_PTR(&gfx_font_0_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT2), MP_ROM_PTR(&gfx_font_2_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT4), MP_ROM_PTR(&gfx_font_4_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT6), MP_ROM_PTR(&gfx_font_6_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT7), MP_ROM_PTR(&gfx_font_7_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT8), MP_ROM_PTR(&gfx_font_8_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT_DejaVu9), MP_ROM_PTR(&gfx_font_DejaVu9_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT_DejaVu12), MP_ROM_PTR(&gfx_font_DejaVu12_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT_DejaVu18), MP_ROM_PTR(&gfx_font_DejaVu18_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_FONT_DejaVu24), MP_ROM_PTR(&gfx_font_DejaVu24_obj) }, \
    { MP_ROM_QSTR(MP_QSTR_BLACK), MP_ROM_INT(0x000000) }, \
    { MP_ROM_QSTR(MP_QSTR_NAVY), MP_ROM_INT(0x000080) }, \
    { MP_ROM_QSTR(MP_QSTR_DARKGREEN), MP_ROM_INT(0x008000) }, \
    { MP_ROM_QSTR(MP_QSTR_DARKCYAN), MP_ROM_INT(0x008080) }, \
    { MP_ROM_QSTR(MP_QSTR_MAROON), MP_ROM_INT(0x800000) }, \
    { MP_ROM_QSTR(MP_QSTR_PURPLE), MP_ROM_INT(0x800080) }, \
    { MP_ROM_QSTR(MP_QSTR_OLIVE), MP_ROM_INT(0x808000) }, \
    { MP_ROM_QSTR(MP_QSTR_LIGHTGREY), MP_ROM_INT(0xC0C0C0) }, \
    { MP_ROM_QSTR(MP_QSTR_DARKGREY), MP_ROM_INT(0x808080) }, \
    { MP_ROM_QSTR(MP_QSTR_BLUE), MP_ROM_INT(0x0000FF) }, \
    { MP_ROM_QSTR(MP_QSTR_GREEN), MP_ROM_INT(0x00FF00) }, \
    { MP_ROM_QSTR(MP_QSTR_CYAN), MP_ROM_INT(0x00FFFF) }, \
    { MP_ROM_QSTR(MP_QSTR_RED), MP_ROM_INT(0xFF0000) }, \
    { MP_ROM_QSTR(MP_QSTR_MAGENTA), MP_ROM_INT(0xFF00FF) }, \
    { MP_ROM_QSTR(MP_QSTR_YELLOW), MP_ROM_INT(0xFFFF00) }, \
    { MP_ROM_QSTR(MP_QSTR_WHITE), MP_ROM_INT(0xFFFFFF) }, \
    { MP_ROM_QSTR(MP_QSTR_ORANGE), MP_ROM_INT(0xFFA500) }, \
    { MP_ROM_QSTR(MP_QSTR_GREENYELLOW), MP_ROM_INT(0xADFF2F) }, \
    { MP_ROM_QSTR(MP_QSTR_PINK), MP_ROM_INT(0xFFC0CB) }

// -------- GFX device wrapper
MAKE_METHOD_0(gfx, startWrite);
MAKE_METHOD_0(gfx, endWrite);

STATIC const mp_rom_map_elem_t gfxdevice_member_table[] = {
    TABLE_PARTS_GFX_BASE,
    MAKE_TABLE(gfx, startWrite),
    MAKE_TABLE(gfx, endWrite),
    // stream function
    { MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&mp_stream_read_obj) },
    { MP_ROM_QSTR(MP_QSTR_write), MP_ROM_PTR(&mp_stream_write_obj) },
    { MP_ROM_QSTR(MP_QSTR_close), MP_ROM_PTR(&mp_stream_close_obj) },
};
STATIC MP_DEFINE_CONST_DICT(gfxdevice_member, gfxdevice_member_table);

// stream function
STATIC const mp_stream_p_t gfx_stream_p = {
    .read = gfx_read,
    .write = gfx_write,
    .ioctl = gfx_ioctl,
};

const mp_obj_type_t gfxdevice_type = {
    { &mp_type_type },
    .protocol = &gfx_stream_p,
    .locals_dict = (mp_obj_dict_t *)&gfxdevice_member,
};

// -------- GFX canvas wrapper
MAKE_METHOD_0(gfx, delete);
MAKE_METHOD_2(gfx, push);

STATIC const mp_rom_map_elem_t gfxcanvas_member_table[] = {
    TABLE_PARTS_GFX_BASE,
    MAKE_TABLE(gfx, delete),
    MAKE_TABLE(gfx, push),
};
STATIC MP_DEFINE_CONST_DICT(gfxcanvas_member, gfxcanvas_member_table);

const mp_obj_type_t gfxcanvas_type = {
    { &mp_type_type },
    .flags = MP_TYPE_FLAG_IS_SUBCLASSED,
    .protocol = &gfx_stream_p,
    .locals_dict = (mp_obj_dict_t *)&gfxcanvas_member,
};

// -------- Button wrapper
MAKE_METHOD_0(btn, isHolding);
MAKE_METHOD_0(btn, isPressed);
MAKE_METHOD_0(btn, isReleased);
MAKE_METHOD_0(btn, wasChangePressed);
MAKE_METHOD_0(btn, wasClicked);
MAKE_METHOD_0(btn, wasHold);
MAKE_METHOD_0(btn, wasPressed);
MAKE_METHOD_0(btn, wasReleased);
MAKE_METHOD_0(btn, lastChange);
MAKE_METHOD_1(btn, pressedFor);
MAKE_METHOD_1(btn, releasedFor);
MAKE_METHOD_1(btn, setDebounceThresh);
MAKE_METHOD_1(btn, setHoldThresh);

STATIC const mp_rom_map_elem_t btn_member_table[] = {
    MAKE_TABLE(btn, isHolding),
    MAKE_TABLE(btn, isPressed),
    MAKE_TABLE(btn, isReleased),
    MAKE_TABLE(btn, wasChangePressed),
    MAKE_TABLE(btn, wasClicked),
    MAKE_TABLE(btn, wasHold),
    MAKE_TABLE(btn, wasPressed),
    MAKE_TABLE(btn, wasReleased),
    MAKE_TABLE(btn, lastChange),
    MAKE_TABLE(btn, pressedFor),
    MAKE_TABLE(btn, releasedFor),
    MAKE_TABLE(btn, setDebounceThresh),
    MAKE_TABLE(btn, setHoldThresh),
};
STATIC MP_DEFINE_CONST_DICT(btn_member, btn_member_table);

const mp_obj_type_t btn_type = {
    { &mp_type_type },
    .locals_dict = (mp_obj_dict_t *)&btn_member,
};

// board type
STATIC const mp_rom_map_elem_t board_enum_locals_dict_table[] = {
    // with display boards
    { MP_ROM_QSTR(MP_QSTR_unknown), MP_ROM_INT(0) },
    { MP_ROM_QSTR(MP_QSTR_Non_Panel), MP_ROM_INT(1) },
    { MP_ROM_QSTR(MP_QSTR_M5Stack), MP_ROM_INT(2) },
    { MP_ROM_QSTR(MP_QSTR_M5StackCore2), MP_ROM_INT(3) },
    { MP_ROM_QSTR(MP_QSTR_M5StickC), MP_ROM_INT(4) },
    { MP_ROM_QSTR(MP_QSTR_M5StickCPlus), MP_ROM_INT(5) },
    { MP_ROM_QSTR(MP_QSTR_M5StackCoreInk), MP_ROM_INT(6) },
    { MP_ROM_QSTR(MP_QSTR_M5Paper), MP_ROM_INT(7) },
    { MP_ROM_QSTR(MP_QSTR_M5Tough), MP_ROM_INT(8) },
    { MP_ROM_QSTR(MP_QSTR_M5Station), MP_ROM_INT(9) },
    // non display boards
    { MP_ROM_QSTR(MP_QSTR_M5Atom), MP_ROM_INT(10) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomPsram), MP_ROM_INT(11) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomU), MP_ROM_INT(12) },
    { MP_ROM_QSTR(MP_QSTR_M5Camera), MP_ROM_INT(13) },
    { MP_ROM_QSTR(MP_QSTR_M5TimerCam), MP_ROM_INT(14) },
    { MP_ROM_QSTR(MP_QSTR_M5StampPico), MP_ROM_INT(15) },
    { MP_ROM_QSTR(MP_QSTR_M5StampC3), MP_ROM_INT(16) },
    { MP_ROM_QSTR(MP_QSTR_M5StampC3U), MP_ROM_INT(17) },
    // external displays
    { MP_ROM_QSTR(MP_QSTR_M5AtomDisplay), MP_ROM_INT(18) },
    { MP_ROM_QSTR(MP_QSTR_M5UnitLCD), MP_ROM_INT(19) },
    { MP_ROM_QSTR(MP_QSTR_M5UnitOLED), MP_ROM_INT(20) },
};
STATIC MP_DEFINE_CONST_DICT(board_enum_locals_dict, board_enum_locals_dict_table);

const mp_obj_type_t board_enum_type = {
    { &mp_type_type },
    .locals_dict = (mp_obj_dict_t *)&board_enum_locals_dict,
};

// -------- M5 wrapper
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_begin_obj, m5_begin);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_update_obj, m5_update);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_getBoard_obj, m5_getBoard);

STATIC const mp_rom_map_elem_t m5_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_m5) },
    { MP_ROM_QSTR(MP_QSTR_begin), MP_ROM_PTR(&m5_begin_obj) },
    { MP_ROM_QSTR(MP_QSTR_update), MP_ROM_PTR(&m5_update_obj) },
    { MP_ROM_QSTR(MP_QSTR_BOARD), MP_ROM_PTR(&board_enum_type) },
    { MP_ROM_QSTR(MP_QSTR_getBoard), MP_ROM_PTR(&m5_getBoard_obj) },
    { MP_ROM_QSTR(MP_QSTR_btnA), MP_OBJ_FROM_PTR(&m5_btnA) },
    { MP_ROM_QSTR(MP_QSTR_btnB), MP_OBJ_FROM_PTR(&m5_btnB) },
    { MP_ROM_QSTR(MP_QSTR_btnC), MP_OBJ_FROM_PTR(&m5_btnC) },
    { MP_ROM_QSTR(MP_QSTR_btnPWR), MP_OBJ_FROM_PTR(&m5_btnPWR) },
    { MP_ROM_QSTR(MP_QSTR_btnEXT), MP_OBJ_FROM_PTR(&m5_btnEXT) },
    { MP_ROM_QSTR(MP_QSTR_display), MP_OBJ_FROM_PTR(&m5_display) },
    { MP_ROM_QSTR(MP_QSTR_lcd), MP_OBJ_FROM_PTR(&m5_display) },
};
STATIC MP_DEFINE_CONST_DICT(mp_module_m5_globals, m5_globals_table);

// Define module object.
const mp_obj_module_t m5m5unified_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&mp_module_m5_globals,
};

MP_REGISTER_MODULE(MP_QSTR_m5, m5m5unified_user_cmodule, MODULE_M5UNIFIED_ENABLED);

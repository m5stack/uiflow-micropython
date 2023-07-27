#include "m5unified.h"

// board type
STATIC const mp_rom_map_elem_t m5_board_member_table[] = {
    /* *FORMAT-OFF* */
    // with display boards
    { MP_ROM_QSTR(MP_QSTR_unknown),         MP_ROM_INT(0) },
    { MP_ROM_QSTR(MP_QSTR_Non_Panel),       MP_ROM_INT(1) },
    { MP_ROM_QSTR(MP_QSTR_M5Stack),         MP_ROM_INT(2) },
    { MP_ROM_QSTR(MP_QSTR_M5StackCore2),    MP_ROM_INT(3) },
    { MP_ROM_QSTR(MP_QSTR_M5StickC),        MP_ROM_INT(4) },
    { MP_ROM_QSTR(MP_QSTR_M5StickCPlus),    MP_ROM_INT(5) },
    { MP_ROM_QSTR(MP_QSTR_M5StickCPlus2),   MP_ROM_INT(6) },
    { MP_ROM_QSTR(MP_QSTR_M5StackCoreInk),  MP_ROM_INT(7) },
    { MP_ROM_QSTR(MP_QSTR_M5Paper),         MP_ROM_INT(8) },
    { MP_ROM_QSTR(MP_QSTR_M5Tough),         MP_ROM_INT(9) },
    { MP_ROM_QSTR(MP_QSTR_M5Station),       MP_ROM_INT(10) },
    { MP_ROM_QSTR(MP_QSTR_M5StackCoreS3),   MP_ROM_INT(11) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomS3),        MP_ROM_INT(12) },
    // non display boards
    { MP_ROM_QSTR(MP_QSTR_M5Atom),          MP_ROM_INT(13) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomPsram),     MP_ROM_INT(14) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomU),         MP_ROM_INT(15) },
    { MP_ROM_QSTR(MP_QSTR_M5Camera),        MP_ROM_INT(16) },
    { MP_ROM_QSTR(MP_QSTR_M5TimerCam),      MP_ROM_INT(17) },
    { MP_ROM_QSTR(MP_QSTR_M5StampPico),     MP_ROM_INT(18) },
    { MP_ROM_QSTR(MP_QSTR_M5StampC3),       MP_ROM_INT(19) },
    { MP_ROM_QSTR(MP_QSTR_M5StampC3U),      MP_ROM_INT(20) },
    { MP_ROM_QSTR(MP_QSTR_M5StampS3),       MP_ROM_INT(21) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomS3Lite),    MP_ROM_INT(22) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomS3U),       MP_ROM_INT(23) },
    // external displays
    { MP_ROM_QSTR(MP_QSTR_M5ATOMDisplay),   MP_ROM_INT(24) },
    { MP_ROM_QSTR(MP_QSTR_M5UnitLCD),       MP_ROM_INT(25) },
    { MP_ROM_QSTR(MP_QSTR_M5UnitOLED),      MP_ROM_INT(26) },
    { MP_ROM_QSTR(MP_QSTR_M5UnitGLASS),     MP_ROM_INT(27) },
    { MP_ROM_QSTR(MP_QSTR_M5UnitRCA),       MP_ROM_INT(28) },
    { MP_ROM_QSTR(MP_QSTR_M5ModuleDisplay), MP_ROM_INT(29) },
    { MP_ROM_QSTR(MP_QSTR_M5RCAModule),     MP_ROM_INT(30) },
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(m5_board_member, m5_board_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    m5_board_type,
    MP_QSTR_BOARD,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&m5_board_member
    );
#else
const mp_obj_type_t m5_board_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_BOARD,
    .locals_dict = (mp_obj_dict_t *)&m5_board_member,
};
#endif

// -------- M5 wrapper
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_begin_obj, m5_begin);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_update_obj, m5_update);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_end_obj, m5_end);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_getBoard_obj, m5_getBoard);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_getDisplayCount_obj, m5_getDisplayCount);
MAKE_METHOD_0(m5, Displays);
MAKE_METHOD_0(m5, getDisplay);
MAKE_METHOD_0(m5, getDisplayIndex);
MAKE_METHOD_0(m5, setPrimaryDisplay);

STATIC const mp_rom_map_elem_t mp_module_m5_globals_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR___name__),          MP_ROM_QSTR(MP_QSTR_M5) },
    { MP_ROM_QSTR(MP_QSTR_BOARD),             MP_ROM_PTR(&m5_board_type) },
    { MP_ROM_QSTR(MP_QSTR_BtnA),              MP_OBJ_FROM_PTR(&m5_btnA) },
    { MP_ROM_QSTR(MP_QSTR_BtnB),              MP_OBJ_FROM_PTR(&m5_btnB) },
    { MP_ROM_QSTR(MP_QSTR_BtnC),              MP_OBJ_FROM_PTR(&m5_btnC) },
    { MP_ROM_QSTR(MP_QSTR_BtnPWR),            MP_OBJ_FROM_PTR(&m5_btnPWR) },
    { MP_ROM_QSTR(MP_QSTR_BtnEXT),            MP_OBJ_FROM_PTR(&m5_btnEXT) },
    { MP_ROM_QSTR(MP_QSTR_Lcd),               MP_OBJ_FROM_PTR(&m5_display) },
    { MP_ROM_QSTR(MP_QSTR_Display),           MP_OBJ_FROM_PTR(&m5_display) },
    { MP_ROM_QSTR(MP_QSTR_UserDisplay),       MP_OBJ_FROM_PTR(&m5_user_display) },
    { MP_ROM_QSTR(MP_QSTR_Touch),             MP_OBJ_FROM_PTR(&m5_touch) },
    { MP_ROM_QSTR(MP_QSTR_Speaker),           MP_OBJ_FROM_PTR(&m5_speaker) },
    { MP_ROM_QSTR(MP_QSTR_Power),             MP_OBJ_FROM_PTR(&m5_power) },
    { MP_ROM_QSTR(MP_QSTR_Imu),               MP_OBJ_FROM_PTR(&m5_imu) },
    { MP_ROM_QSTR(MP_QSTR_Als),               MP_OBJ_FROM_PTR(&m5_als) },
    { MP_ROM_QSTR(MP_QSTR_Widgets),           MP_OBJ_FROM_PTR(&m5_widgets) },

    { MP_ROM_QSTR(MP_QSTR_begin),             MP_ROM_PTR(&m5_begin_obj) },
    { MP_ROM_QSTR(MP_QSTR_update),            MP_ROM_PTR(&m5_update_obj) },
    { MP_ROM_QSTR(MP_QSTR_end),               MP_ROM_PTR(&m5_end_obj) },
    { MP_ROM_QSTR(MP_QSTR_getBoard),          MP_ROM_PTR(&m5_getBoard_obj) },
    { MP_ROM_QSTR(MP_QSTR_Displays),          MP_ROM_PTR(&m5_Displays_obj) },
    { MP_ROM_QSTR(MP_QSTR_getDisplay),        MP_ROM_PTR(&m5_getDisplay_obj) },
    { MP_ROM_QSTR(MP_QSTR_getDisplayIndex),   MP_ROM_PTR(&m5_getDisplayIndex_obj) },
    { MP_ROM_QSTR(MP_QSTR_getDisplayCount),   MP_ROM_PTR(&m5_getDisplayCount_obj) },
    { MP_ROM_QSTR(MP_QSTR_setPrimaryDisplay), MP_ROM_PTR(&m5_setPrimaryDisplay_obj) },
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(mp_module_m5_globals, mp_module_m5_globals_table);

// Define module object.
const mp_obj_module_t mp_module_m5 = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&mp_module_m5_globals,
};

MP_REGISTER_MODULE(MP_QSTR_M5, mp_module_m5);

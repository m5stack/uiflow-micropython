#include "m5unified.h"

// board type
STATIC const mp_rom_map_elem_t board_enum_locals_dict_table[] = {
    /* *FORMAT-OFF* */
    // with display boards
    { MP_ROM_QSTR(MP_QSTR_unknown),         MP_ROM_INT(0) },
    { MP_ROM_QSTR(MP_QSTR_Non_Panel),       MP_ROM_INT(1) },
    { MP_ROM_QSTR(MP_QSTR_M5Stack),         MP_ROM_INT(2) },
    { MP_ROM_QSTR(MP_QSTR_M5StackCore2),    MP_ROM_INT(3) },
    { MP_ROM_QSTR(MP_QSTR_M5StickC),        MP_ROM_INT(4) },
    { MP_ROM_QSTR(MP_QSTR_M5StickCPlus),    MP_ROM_INT(5) },
    { MP_ROM_QSTR(MP_QSTR_M5StackCoreInk),  MP_ROM_INT(6) },
    { MP_ROM_QSTR(MP_QSTR_M5Paper),         MP_ROM_INT(7) },
    { MP_ROM_QSTR(MP_QSTR_M5Tough),         MP_ROM_INT(8) },
    { MP_ROM_QSTR(MP_QSTR_M5Station),       MP_ROM_INT(9) },
    { MP_ROM_QSTR(MP_QSTR_M5StackCoreS3),   MP_ROM_INT(10) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomS3LCD),     MP_ROM_INT(11) },
    // non display boards
    { MP_ROM_QSTR(MP_QSTR_M5Atom),          MP_ROM_INT(12) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomPsram),     MP_ROM_INT(13) },
    { MP_ROM_QSTR(MP_QSTR_M5AtomU),         MP_ROM_INT(14) },
    { MP_ROM_QSTR(MP_QSTR_M5Camera),        MP_ROM_INT(15) },
    { MP_ROM_QSTR(MP_QSTR_M5TimerCam),      MP_ROM_INT(16) },
    { MP_ROM_QSTR(MP_QSTR_M5StampPico),     MP_ROM_INT(17) },
    { MP_ROM_QSTR(MP_QSTR_M5StampC3),       MP_ROM_INT(18) },
    { MP_ROM_QSTR(MP_QSTR_M5StampC3U),      MP_ROM_INT(19) },
    // external displays
    { MP_ROM_QSTR(MP_QSTR_M5ATOMDisplay),   MP_ROM_INT(20) },
    { MP_ROM_QSTR(MP_QSTR_M5UnitLCD),       MP_ROM_INT(21) },
    { MP_ROM_QSTR(MP_QSTR_M5UnitOLED),      MP_ROM_INT(22) },
    { MP_ROM_QSTR(MP_QSTR_M5ModuleDisplay), MP_ROM_INT(23) },
    { MP_ROM_QSTR(MP_QSTR_M5RCAModule),     MP_ROM_INT(24) },
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(board_enum_locals_dict, board_enum_locals_dict_table);

const mp_obj_type_t board_enum_type = {
    .base = { &mp_type_enumerate },
    .locals_dict = (mp_obj_dict_t *)&board_enum_locals_dict,
};

// -------- M5 wrapper
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_begin_obj, m5_begin);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_update_obj, m5_update);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_getBoard_obj, m5_getBoard);

STATIC const mp_rom_map_elem_t m5_globals_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR___name__),     MP_ROM_QSTR(MP_QSTR_M5) },
    { MP_ROM_QSTR(MP_QSTR_begin),        MP_ROM_PTR(&m5_begin_obj) },
    { MP_ROM_QSTR(MP_QSTR_update),       MP_ROM_PTR(&m5_update_obj) },
    { MP_ROM_QSTR(MP_QSTR_getBoard),     MP_ROM_PTR(&m5_getBoard_obj) },
    { MP_ROM_QSTR(MP_QSTR_BOARD),        MP_ROM_PTR(&board_enum_type) },
    { MP_ROM_QSTR(MP_QSTR_BtnA),         MP_OBJ_FROM_PTR(&m5_btnA) },
    { MP_ROM_QSTR(MP_QSTR_BtnB),         MP_OBJ_FROM_PTR(&m5_btnB) },
    { MP_ROM_QSTR(MP_QSTR_BtnC),         MP_OBJ_FROM_PTR(&m5_btnC) },
    { MP_ROM_QSTR(MP_QSTR_BtnPWR),       MP_OBJ_FROM_PTR(&m5_btnPWR) },
    { MP_ROM_QSTR(MP_QSTR_BtnEXT),       MP_OBJ_FROM_PTR(&m5_btnEXT) },
    { MP_ROM_QSTR(MP_QSTR_Lcd),          MP_OBJ_FROM_PTR(&m5_display) },
    { MP_ROM_QSTR(MP_QSTR_Display),      MP_OBJ_FROM_PTR(&m5_display) },
    { MP_ROM_QSTR(MP_QSTR_UserDisplay),  MP_OBJ_FROM_PTR(&mp_user_panel_type) },
    { MP_ROM_QSTR(MP_QSTR_Speaker),      MP_OBJ_FROM_PTR(&m5_speaker) },
    { MP_ROM_QSTR(MP_QSTR_Power),        MP_OBJ_FROM_PTR(&m5_power) },
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(mp_module_m5_globals, m5_globals_table);

// Define module object.
const mp_obj_module_t mp_m5unified_module = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&mp_module_m5_globals,
};

MP_REGISTER_MODULE(MP_QSTR_M5, mp_m5unified_module);

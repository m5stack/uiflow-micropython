#include <mpy_m5unified.h>

#define MAKE_METHOD_V(prefix, func, arg_min, arg_max) extern mp_obj_t prefix##_##func(size_t,const mp_obj_t*); STATIC MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN( prefix##_##func##_obj, arg_min, arg_max, prefix##_##func ); 
#define MAKE_METHOD_0(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t                  ); STATIC MP_DEFINE_CONST_FUN_OBJ_1( prefix##_##func##_obj, prefix##_##func );
#define MAKE_METHOD_1(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t,mp_obj_t         ); STATIC MP_DEFINE_CONST_FUN_OBJ_2( prefix##_##func##_obj, prefix##_##func );
#define MAKE_METHOD_2(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t,mp_obj_t,mp_obj_t); STATIC MP_DEFINE_CONST_FUN_OBJ_3( prefix##_##func##_obj, prefix##_##func );

#define MAKE_TABLE( prefix, func ) \
  { MP_ROM_QSTR(MP_QSTR_##func), MP_ROM_PTR(&prefix##_##func##_obj) }

//-------- GFX common wrapper
MAKE_METHOD_0( gfx, width             );
MAKE_METHOD_0( gfx, height            );
MAKE_METHOD_0( gfx, getRotation       );
MAKE_METHOD_0( gfx, getColorDepth     );
MAKE_METHOD_1( gfx, setRotation       );
MAKE_METHOD_1( gfx, setColorDepth     );
MAKE_METHOD_1( gfx, print             );
MAKE_METHOD_2( gfx, setCursor         );
MAKE_METHOD_V( gfx, fillScreen , 1, 2 );
MAKE_METHOD_V( gfx, drawPixel  , 3, 4 );
MAKE_METHOD_V( gfx, drawCircle , 4, 5 );
MAKE_METHOD_V( gfx, fillCircle , 4, 5 );
MAKE_METHOD_V( gfx, drawLine   , 5, 6 );
MAKE_METHOD_V( gfx, drawRect   , 5, 6 );
MAKE_METHOD_V( gfx, fillRect   , 5, 6 );
MAKE_METHOD_V( gfx, printf     , 2, 32);
MAKE_METHOD_V( gfx, newCanvas  , 3, 5 );

#define TABLE_PARTS_GFX_BASE \
  MAKE_TABLE( gfx, drawCircle   ), \
  MAKE_TABLE( gfx, drawLine     ), \
  MAKE_TABLE( gfx, drawPixel    ), \
  MAKE_TABLE( gfx, drawRect     ), \
  MAKE_TABLE( gfx, fillCircle   ), \
  MAKE_TABLE( gfx, fillRect     ), \
  MAKE_TABLE( gfx, fillScreen   ), \
  MAKE_TABLE( gfx, getColorDepth), \
  MAKE_TABLE( gfx, getRotation  ), \
  MAKE_TABLE( gfx, height       ), \
  MAKE_TABLE( gfx, newCanvas    ), \
  MAKE_TABLE( gfx, print        ), \
  MAKE_TABLE( gfx, printf       ), \
  MAKE_TABLE( gfx, setColorDepth), \
  MAKE_TABLE( gfx, setCursor    ), \
  MAKE_TABLE( gfx, setRotation  ), \
  MAKE_TABLE( gfx, width        ), \
  { MP_ROM_QSTR(MP_QSTR_BLACK      ), MP_ROM_INT( 0x000000 ) }, \
  { MP_ROM_QSTR(MP_QSTR_NAVY       ), MP_ROM_INT( 0x000080 ) }, \
  { MP_ROM_QSTR(MP_QSTR_DARKGREEN  ), MP_ROM_INT( 0x008000 ) }, \
  { MP_ROM_QSTR(MP_QSTR_DARKCYAN   ), MP_ROM_INT( 0x008080 ) }, \
  { MP_ROM_QSTR(MP_QSTR_MAROON     ), MP_ROM_INT( 0x800000 ) }, \
  { MP_ROM_QSTR(MP_QSTR_PURPLE     ), MP_ROM_INT( 0x800080 ) }, \
  { MP_ROM_QSTR(MP_QSTR_OLIVE      ), MP_ROM_INT( 0x808000 ) }, \
  { MP_ROM_QSTR(MP_QSTR_LIGHTGREY  ), MP_ROM_INT( 0xC0C0C0 ) }, \
  { MP_ROM_QSTR(MP_QSTR_DARKGREY   ), MP_ROM_INT( 0x808080 ) }, \
  { MP_ROM_QSTR(MP_QSTR_BLUE       ), MP_ROM_INT( 0x0000FF ) }, \
  { MP_ROM_QSTR(MP_QSTR_GREEN      ), MP_ROM_INT( 0x00FF00 ) }, \
  { MP_ROM_QSTR(MP_QSTR_CYAN       ), MP_ROM_INT( 0x00FFFF ) }, \
  { MP_ROM_QSTR(MP_QSTR_RED        ), MP_ROM_INT( 0xFF0000 ) }, \
  { MP_ROM_QSTR(MP_QSTR_MAGENTA    ), MP_ROM_INT( 0xFF00FF ) }, \
  { MP_ROM_QSTR(MP_QSTR_YELLOW     ), MP_ROM_INT( 0xFFFF00 ) }, \
  { MP_ROM_QSTR(MP_QSTR_WHITE      ), MP_ROM_INT( 0xFFFFFF ) }, \
  { MP_ROM_QSTR(MP_QSTR_ORANGE     ), MP_ROM_INT( 0xFFA500 ) }, \
  { MP_ROM_QSTR(MP_QSTR_GREENYELLOW), MP_ROM_INT( 0xADFF2F ) }, \
  { MP_ROM_QSTR(MP_QSTR_PINK       ), MP_ROM_INT( 0xFFC0CB ) }

//-------- GFX device wrapper
MAKE_METHOD_0( gfx, startWrite        );
MAKE_METHOD_0( gfx, endWrite          );

STATIC const mp_rom_map_elem_t gfxdevice_member_table[] = {
  TABLE_PARTS_GFX_BASE ,
  MAKE_TABLE( gfx, startWrite ),
  MAKE_TABLE( gfx, endWrite   ),
};
STATIC MP_DEFINE_CONST_DICT(gfxdevice_member, gfxdevice_member_table);
const mp_obj_type_t gfxdevice_type = {
  { &mp_type_type },
  .locals_dict = (mp_obj_dict_t *)&gfxdevice_member,
};

//-------- GFX canvas wrapper
MAKE_METHOD_0( gfx, delete            );
MAKE_METHOD_2( gfx, push              );

STATIC const mp_rom_map_elem_t gfxcanvas_member_table[] = {
  TABLE_PARTS_GFX_BASE ,
  MAKE_TABLE( gfx, delete),
  MAKE_TABLE( gfx, push),
};
STATIC MP_DEFINE_CONST_DICT(gfxcanvas_member, gfxcanvas_member_table);
const mp_obj_type_t gfxcanvas_type = {
  { &mp_type_type },
  .flags = MP_TYPE_FLAG_IS_SUBCLASSED,
  .locals_dict = (mp_obj_dict_t *)&gfxcanvas_member,
};

//-------- Button wrapper
MAKE_METHOD_0( btn, isHolding        );
MAKE_METHOD_0( btn, isPressed        );
MAKE_METHOD_0( btn, isReleased       );
MAKE_METHOD_0( btn, wasChangePressed );
MAKE_METHOD_0( btn, wasClicked       );
MAKE_METHOD_0( btn, wasHold          );
MAKE_METHOD_0( btn, wasPressed       );
MAKE_METHOD_0( btn, wasReleased      );
MAKE_METHOD_0( btn, lastChange       );
MAKE_METHOD_1( btn, pressedFor       );
MAKE_METHOD_1( btn, releasedFor      );
MAKE_METHOD_1( btn, setDebounceThresh);
MAKE_METHOD_1( btn, setHoldThresh    );

STATIC const mp_rom_map_elem_t btn_member_table[] = {
  MAKE_TABLE( btn, isHolding        ),
  MAKE_TABLE( btn, isPressed        ),
  MAKE_TABLE( btn, isReleased       ),
  MAKE_TABLE( btn, wasChangePressed ),
  MAKE_TABLE( btn, wasClicked       ),
  MAKE_TABLE( btn, wasHold          ),
  MAKE_TABLE( btn, wasPressed       ),
  MAKE_TABLE( btn, wasReleased      ),
  MAKE_TABLE( btn, lastChange       ),
  MAKE_TABLE( btn, pressedFor       ),
  MAKE_TABLE( btn, releasedFor      ),
  MAKE_TABLE( btn, setDebounceThresh),
  MAKE_TABLE( btn, setHoldThresh    ),
};

STATIC MP_DEFINE_CONST_DICT(btn_member, btn_member_table);
const mp_obj_type_t btn_type = {
  { &mp_type_type },
  .locals_dict = (mp_obj_dict_t *)&btn_member,
};


//-------- M5 wrapper

STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_begin_obj, m5_begin);
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5_update_obj, m5_update);

STATIC const mp_rom_map_elem_t m5_globals_table[] = {
  { MP_ROM_QSTR(MP_QSTR___name__  ), MP_ROM_QSTR(MP_QSTR_m5) },
  { MP_ROM_QSTR(MP_QSTR_begin     ), MP_ROM_PTR(&m5_begin_obj) },
  { MP_ROM_QSTR(MP_QSTR_update    ), MP_ROM_PTR(&m5_update_obj) },
  { MP_ROM_QSTR(MP_QSTR_btnA      ), MP_OBJ_FROM_PTR(&m5_btnA) },
  { MP_ROM_QSTR(MP_QSTR_btnB      ), MP_OBJ_FROM_PTR(&m5_btnB) },
  { MP_ROM_QSTR(MP_QSTR_btnC      ), MP_OBJ_FROM_PTR(&m5_btnC) },
  { MP_ROM_QSTR(MP_QSTR_btnPWR    ), MP_OBJ_FROM_PTR(&m5_btnPWR) },
  { MP_ROM_QSTR(MP_QSTR_btnEXT    ), MP_OBJ_FROM_PTR(&m5_btnEXT) },
  { MP_ROM_QSTR(MP_QSTR_display   ), MP_OBJ_FROM_PTR(&m5_display) },
  { MP_ROM_QSTR(MP_QSTR_lcd       ), MP_OBJ_FROM_PTR(&m5_display) },
};

STATIC MP_DEFINE_CONST_DICT(mp_module_m5_globals, m5_globals_table);

// Define module object.
const mp_obj_module_t m5m5unified_user_cmodule = {
  .base = { &mp_type_module },
  .globals = (mp_obj_dict_t *)&mp_module_m5_globals,
};


MP_REGISTER_MODULE(MP_QSTR_m5, m5m5unified_user_cmodule, MODULE_M5UNIFIED_ENABLED);

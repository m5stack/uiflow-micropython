/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include <mpy_m5unified.h>

#if MICROPY_PY_LVGL
#include "./../../cmodules/lv_binding_micropython/lvgl/lvgl.h"
// #include "./../../cmodules/lv_binding_micropython/lvgl/src/hal/lv_hal_disp.h"
#include "./../../cmodules/lv_binding_micropython/driver/include/common.h"
#endif

/* *FORMAT-OFF* */
#define MAKE_METHOD_V(prefix, func, arg_min, arg_max) extern mp_obj_t prefix##_##func(size_t,const mp_obj_t*); static MP_DEFINE_CONST_FUN_OBJ_VAR_BETWEEN( prefix##_##func##_obj, arg_min, arg_max, prefix##_##func ); 
#define MAKE_METHOD_0(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t                  ); static MP_DEFINE_CONST_FUN_OBJ_1( prefix##_##func##_obj, prefix##_##func );
#define MAKE_METHOD_1(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t,mp_obj_t         ); static MP_DEFINE_CONST_FUN_OBJ_2( prefix##_##func##_obj, prefix##_##func );
#define MAKE_METHOD_2(prefix, func) extern mp_obj_t prefix##_##func(mp_obj_t,mp_obj_t,mp_obj_t); static MP_DEFINE_CONST_FUN_OBJ_3( prefix##_##func##_obj, prefix##_##func );
#define MAKE_METHOD_KW(prefix, func, args) extern mp_obj_t prefix##_##func(size_t,const mp_obj_t*,mp_map_t*); static MP_DEFINE_CONST_FUN_OBJ_KW( prefix##_##func##_obj, args, prefix##_##func ); 
/* *FORMAT-ON* */

#define MAKE_TABLE(prefix, func) \
    { MP_ROM_QSTR(MP_QSTR_##func), MP_ROM_PTR(&prefix##_##func##_obj) }

extern const mp_obj_type_t mp_fonts_type;
extern const mp_obj_type_t mp_color_type;

extern const mp_obj_type_t mp_btn_type;
extern const mp_obj_type_t mp_imu_type;
extern const mp_obj_type_t mp_led_type;
extern const mp_obj_type_t mp_spk_type;
extern const mp_obj_type_t mp_power_type;
extern const mp_obj_type_t mp_gfxcanvas_type;
extern const mp_obj_type_t m5_user_display;
extern const mp_obj_type_t mp_gfxdevice_type;
extern const mp_obj_module_t m5_widgets;
extern const mp_obj_type_t mp_touch_type;
extern const mp_obj_type_t mp_als_type;

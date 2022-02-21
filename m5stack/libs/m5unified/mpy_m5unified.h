#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>
#include "mpy_m5gfx.h"
#include "mpy_m5btn.h"

extern mp_obj_t m5_begin(void);
extern mp_obj_t m5_update(void);
extern mp_obj_t m5_getBoard(void);

extern const gfx_obj_t m5_display;
extern const btn_obj_t m5_btnA;
extern const btn_obj_t m5_btnB;
extern const btn_obj_t m5_btnC;
extern const btn_obj_t m5_btnPWR;
extern const btn_obj_t m5_btnEXT;


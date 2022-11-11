#define M5ATOMDISPLAY_LOGICAL_WIDTH 640
#define M5ATOMDISPLAY_LOGICAL_HEIGHT 360
#include <M5Unified.h>
#include <M5AtomDisplay.h>
#include <M5UnitOLED.h>
#include <M5UnitLCD.h>

extern "C"
{
#include "mpy_m5unified.h"

/* *FORMAT-OFF* */
const btn_obj_t m5_btnA    = {{&btn_type},        &(M5.BtnA)    };
const btn_obj_t m5_btnB    = {{&btn_type},        &(M5.BtnB)    };
const btn_obj_t m5_btnC    = {{&btn_type},        &(M5.BtnC)    };
const btn_obj_t m5_btnPWR  = {{&btn_type},        &(M5.BtnPWR)  };
const btn_obj_t m5_btnEXT  = {{&btn_type},        &(M5.BtnEXT)  };
const spk_obj_t m5_speaker = {{&spk_type},        &(M5.Speaker) };
const gfx_obj_t m5_display = {{&gfxdevice_type},  &(M5.Display) };
const pwr_obj_t m5_power   = {{&power_type},      &(M5.Power)   };
/* *FORMAT-ON* */

#if MICROPY_PY_LVGL
#include "lvgl/lvgl.h"
#include "lvgl/src/hal/lv_hal_disp.h"
LovyanGFX *g_gfx = &(M5.Display);
#endif

mp_obj_t m5_begin(void) {
    M5.begin();
    return mp_const_none;
}

mp_obj_t m5_update(void) {
    M5.update();
    return mp_const_none;
}

mp_obj_t m5_getBoard(void) {
    return mp_obj_new_int(M5.getBoard());
}

#if MICROPY_PY_LVGL
bool gfx_lvgl_touch_read(lv_indev_drv_t * indev_drv, lv_indev_data_t *data)
{
    if (g_gfx == nullptr) {
        return false;
    }

    M5.update();
    
    if (!M5.Touch.getCount()) {
        data->point = (lv_point_t){ 0, 0 };
        data->state = LV_INDEV_STATE_RELEASED;
        return false;
    }

    auto tp = M5.Touch.getTouchPointRaw(1);
    data->point = (lv_point_t){ tp.x, tp.y };
    data->state = LV_INDEV_STATE_PRESSED;
    return true;
}
#endif
}

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
const btn_obj_t m5_btnA    = {{&mp_btn_type},        &(M5.BtnA)    };
const btn_obj_t m5_btnB    = {{&mp_btn_type},        &(M5.BtnB)    };
const btn_obj_t m5_btnC    = {{&mp_btn_type},        &(M5.BtnC)    };
const btn_obj_t m5_btnPWR  = {{&mp_btn_type},        &(M5.BtnPWR)  };
const btn_obj_t m5_btnEXT  = {{&mp_btn_type},        &(M5.BtnEXT)  };
const spk_obj_t m5_speaker = {{&mp_spk_type},        &(M5.Speaker) };
const gfx_obj_t m5_display = {{&mp_gfxdevice_type},  &(M5.Display) };
const pwr_obj_t m5_power   = {{&mp_power_type},      &(M5.Power)   };
/* *FORMAT-ON* */

mp_obj_t m5_begin(void) {
    M5.begin();
    // Set default font to DejaVu9, keep same style with UIFlow website UI design.
    M5.Display.setTextFont(&fonts::DejaVu9);
    return mp_const_none;
}

mp_obj_t m5_update(void) {
    M5.update();
    return mp_const_none;
}

mp_obj_t m5_getBoard(void) {
    return mp_obj_new_int(M5.getBoard());
}

#include "mpy_user_lcd.c"

#if MICROPY_PY_LVGL
#include "mpy_lvgl.c"
#endif
}

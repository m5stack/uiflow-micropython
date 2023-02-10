#define M5ATOMDISPLAY_LOGICAL_WIDTH 640
#define M5ATOMDISPLAY_LOGICAL_HEIGHT 360

// #define M5MODULERCA_LOGICAL_WIDTH 216
// #define M5MODULERCA_LOGICAL_HEIGHT 144
// #define M5MODULERCA_SIGNAL_TYPE signal_type_t::PAL

// #define M5MODULERCA_USE_PSRAM use_psram_t::psram_use      // all psram
// #define M5MODULERCA_USE_PSRAM use_psram_t::psram_half_use // half sram :half psram
// #define M5MODULERCA_USE_PSRAM use_psram_t::psram_no_use   // all sram

#include <esp_log.h>
#include <sdkconfig.h>
#include <M5AtomDisplay.h>
#include <M5ModuleDisplay.h>
#include <M5ModuleRCA.h>
#include <M5UnitOLED.h>
#include <M5UnitLCD.h>
#include <M5UnitRCA.h>
#include <M5Unified.h>

extern "C"
{
#include "mpy_m5unified.h"

/* *FORMAT-OFF* */
const btn_obj_t m5_btnA    = { {&mp_btn_type},       &(M5.BtnA)          };
const btn_obj_t m5_btnB    = { {&mp_btn_type},       &(M5.BtnB)          };
const btn_obj_t m5_btnC    = { {&mp_btn_type},       &(M5.BtnC)          };
const btn_obj_t m5_btnPWR  = { {&mp_btn_type},       &(M5.BtnPWR)        };
const btn_obj_t m5_btnEXT  = { {&mp_btn_type},       &(M5.BtnEXT)        };
const spk_obj_t m5_speaker = { {&mp_spk_type},       &(M5.Speaker)       };
const pwr_obj_t m5_power   = { {&mp_power_type},     &(M5.Power)         };
const pwr_obj_t m5_imu     = { {&mp_imu_type},       &(M5.Imu)           };
      gfx_obj_t m5_display = { {&mp_gfxdevice_type}, NULL                };
/* *FORMAT-ON* */

// TODO: pass configuration parameters
mp_obj_t m5_begin(void) {
    // config
    auto cfg = M5.config();
    cfg.clear_display = true;
    M5.begin(cfg);
    M5.Display.clear();
    m5_display.gfx = (void *)(&(M5.Display));
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

/********************************Multi Display*********************************/
mp_obj_t m5_getDisplayCount(void) {
    return mp_obj_new_int(M5.getDisplayCount());
}

mp_obj_t m5_Displays(mp_obj_t index) {
    m5_display.gfx = (void *)&(M5.Displays(mp_obj_get_int(index)));
    return MP_OBJ_FROM_PTR(&m5_display);
}

mp_obj_t m5_getDisplay(mp_obj_t index) {
    m5_display.gfx = (void *)&(M5.getDisplay(mp_obj_get_int(index)));
    return MP_OBJ_FROM_PTR(&m5_display);
}

mp_obj_t m5_getDisplayIndex(mp_obj_t board) {
    return mp_obj_new_int(M5.getDisplayIndex((lgfx::boards::board_t)mp_obj_get_int(board)));
}

mp_obj_t m5_setPrimaryDisplay(mp_obj_t index) {
    M5.setPrimaryDisplay(mp_obj_get_int(index));
    m5_display.gfx = (void *)(&(M5.Display));
    return mp_const_none;
}

mp_obj_t m5_setPrimaryDisplayType(mp_obj_t type) {
    M5.setPrimaryDisplayType((m5gfx::board_t)mp_obj_get_int(type));
    m5_display.gfx = (void *)(&(M5.Display));
    return mp_const_none;
}

#include "mpy_user_lcd.txt"

#if MICROPY_PY_LVGL
#include "mpy_lvgl.txt"
#endif
}

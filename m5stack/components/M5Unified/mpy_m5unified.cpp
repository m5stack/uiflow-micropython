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

#include <utility/Button_Class.hpp>

extern "C"
{
#include "mpy_m5unified.h"
#include "mphalport.h"

static void m5_btns_callbacks_init(void);
static void m5_btns_callbacks_check(void);

/* *FORMAT-OFF* */
const spk_obj_t m5_speaker = {&mp_spk_type,       &(M5.Speaker)};
const pwr_obj_t m5_power   = {&mp_power_type,     &(M5.Power)  };
const pwr_obj_t m5_imu     = {&mp_imu_type,       &(M5.Imu)    };
      btn_obj_t m5_btnA    = {&mp_btn_type,       &(M5.BtnA)   };
      btn_obj_t m5_btnB    = {&mp_btn_type,       &(M5.BtnB)   };
      btn_obj_t m5_btnC    = {&mp_btn_type,       &(M5.BtnC)   };
      btn_obj_t m5_btnPWR  = {&mp_btn_type,       &(M5.BtnPWR) };
      btn_obj_t m5_btnEXT  = {&mp_btn_type,       &(M5.BtnEXT) };
      gfx_obj_t m5_display = {&mp_gfxdevice_type, NULL         };

static btn_obj_t *m5_btn_list[5] = {&m5_btnA, &m5_btnB, &m5_btnC, &m5_btnPWR, &m5_btnEXT};
/* *FORMAT-ON* */

// TODO: pass configuration parameters
mp_obj_t m5_begin(void) {
    // disable all external display
    auto cfg = M5.config();
    cfg.external_display_value = 0;

    // initial
    M5.begin(cfg);

    M5.Display.clear();
    // default display
    m5_display.gfx = (void *)(&(M5.Display));
    // set default font to DejaVu9, keep same style with UIFlow website UI design.
    M5.Display.setTextFont(&fonts::DejaVu9);

    m5_btns_callbacks_init();
    return mp_const_none;
}

mp_obj_t m5_update(void) {
    M5.update();

    m5_btns_callbacks_check();
    return mp_const_none;
}

mp_obj_t m5_getBoard(void) {
    return mp_obj_new_int(M5.getBoard());
}
/********************************Configuration*********************************/


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

/****************************Button Callback handler***************************/
static void m5_btns_callbacks_init(void) {
    // clear all callback flag bit
    for (uint8_t i = 0; i < 5; i++) {
        m5_btn_list[i]->callbacks.flag = 0;
    }
}

static void m5_btns_callbacks_check(void) {
    // mp_hal_wake_main_task_from_isr();
    for (uint8_t i = 0; i < 5; i++) {
        if (m5_btn_list[i]->callbacks.flag) {
            if (m5_btn_list[i]->callbacks.flag_bit.wasClicked) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasClicked()) {
                    mp_sched_schedule(m5_btn_list[i]->callbacks.wasClicked_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasSingleClicked) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasSingleClicked()) {
                    mp_sched_schedule(m5_btn_list[i]->callbacks.wasSingleClicked_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasDoubleClicked) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasDoubleClicked()) {
                    mp_sched_schedule(m5_btn_list[i]->callbacks.wasDoubleClicked_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasHold) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasHold()) {
                    mp_sched_schedule(m5_btn_list[i]->callbacks.wasHold_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasPressed) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasPressed()) {
                    mp_sched_schedule(m5_btn_list[i]->callbacks.wasPressed_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasReleased) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasReleased()) {
                    mp_sched_schedule(m5_btn_list[i]->callbacks.wasReleased_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }
        }
    }
}

#include "mpy_user_lcd.txt"

#if MICROPY_PY_LVGL
#include "mpy_lvgl.txt"
#endif
}

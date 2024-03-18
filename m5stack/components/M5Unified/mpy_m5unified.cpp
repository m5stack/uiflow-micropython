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

static void m5_btns_callbacks_check(void);
static void m5_btns_callbacks_deinit(void);

/* *FORMAT-OFF* */
const spk_obj_t m5_speaker = {&mp_spk_type,       &(M5.Speaker)};
const pwr_obj_t m5_power   = {&mp_power_type,     &(M5.Power)  };
const pwr_obj_t m5_imu     = {&mp_imu_type,       &(M5.Imu)    };
      als_obj_t m5_als     = {&mp_als_type,       &(M5.Als)    };
      btn_obj_t m5_btnA    = {&mp_btn_type,       &(M5.BtnA),   {0}};
      btn_obj_t m5_btnB    = {&mp_btn_type,       &(M5.BtnB),   {0}};
      btn_obj_t m5_btnC    = {&mp_btn_type,       &(M5.BtnC),   {0}};
      btn_obj_t m5_btnPWR  = {&mp_btn_type,       &(M5.BtnPWR), {0}};
      btn_obj_t m5_btnEXT  = {&mp_btn_type,       &(M5.BtnEXT), {0}};
      gfx_obj_t m5_display = {&mp_gfxdevice_type, &(M5.Display)};
      touch_obj_t m5_touch = {&mp_touch_type,     &(M5.Touch)  };
const mic_obj_t m5_mic     = {&mp_mic_type,       &(M5.Mic)    };

static btn_obj_t *m5_btn_list[5] = {&m5_btnA, &m5_btnB, &m5_btnC, &m5_btnPWR, &m5_btnEXT};
/* *FORMAT-ON* */

static void m5_config_helper_module_display(mp_obj_t config_obj, m5::M5Unified::config_t &cfg) {
    if (!MP_OBJ_IS_TYPE(config_obj, &mp_type_dict)) {
        mp_raise_TypeError("module_display must be a dict");
    }

    mp_map_t *config_map = mp_obj_dict_get_map(config_obj);

    for (size_t i = 0; i < config_map->alloc; i++) {
        if (MP_MAP_SLOT_IS_FILLED(config_map, i)) {
            mp_obj_t key = config_map->table[i].key;
            mp_obj_t value = config_map->table[i].value;

            const char *key_str = mp_obj_str_get_str(key);

            if (strcmp(key_str, "enabled") == 0) {
                cfg.external_display.module_display = mp_obj_get_int(value);
            } else if (strcmp(key_str, "width") == 0) {
                cfg.module_display.logical_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "height") == 0) {
                cfg.module_display.logical_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "refresh_rate") == 0) {
                cfg.module_display.refresh_rate = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_width") == 0) {
                cfg.module_display.output_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_height") == 0) {
                cfg.module_display.output_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "scale_w") == 0) {
                cfg.module_display.scale_w = mp_obj_get_int(value);
            } else if (strcmp(key_str, "scale_h") == 0) {
                cfg.module_display.scale_h = mp_obj_get_int(value);
            } else if (strcmp(key_str, "pixel_clock") == 0) {
                cfg.module_display.pixel_clock = mp_obj_get_int(value);
            }
        }
    }
}

static void m5_config_helper_module_rca(mp_obj_t config_obj, m5::M5Unified::config_t &cfg) {
    if (!MP_OBJ_IS_TYPE(config_obj, &mp_type_dict)) {
        mp_raise_TypeError("module_rca must be a dict");
    }

    mp_map_t *config_map = mp_obj_dict_get_map(config_obj);

    for (size_t i = 0; i < config_map->alloc; i++) {
        if (MP_MAP_SLOT_IS_FILLED(config_map, i)) {
            mp_obj_t key = config_map->table[i].key;
            mp_obj_t value = config_map->table[i].value;

            const char *key_str = mp_obj_str_get_str(key);

            if (strcmp(key_str, "enabled") == 0) {
                cfg.external_display.module_rca = mp_obj_get_int(value);
            } else if (strcmp(key_str, "width") == 0) {
                cfg.module_rca.logical_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "height") == 0) {
                cfg.module_rca.logical_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_width") == 0) {
                cfg.module_rca.output_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_height") == 0) {
                cfg.module_rca.output_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "signal_type") == 0) {
                cfg.module_rca.signal_type = (M5ModuleRCA::signal_type_t)mp_obj_get_int(value);
            } else if (strcmp(key_str, "use_psram") == 0) {
                cfg.module_rca.use_psram = (M5ModuleRCA::use_psram_t)mp_obj_get_int(value);
            } else if (strcmp(key_str, "pin_dac") == 0) {
                cfg.module_rca.pin_dac = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_level") == 0) {
                cfg.module_rca.output_level = mp_obj_get_int(value);
            }
        }
    }
}

static void m5_config_helper(mp_obj_t config_obj, m5::M5Unified::config_t &cfg) {
    mp_map_t *config_map = mp_obj_dict_get_map(config_obj);

    for (size_t i = 0; i < config_map->alloc; i++) {
        if (MP_MAP_SLOT_IS_FILLED(config_map, i)) {
            mp_obj_t key = config_map->table[i].key;
            mp_obj_t value = config_map->table[i].value;

            const char *key_str = mp_obj_str_get_str(key);

            if (strcmp(key_str, "module_display") == 0) {
                m5_config_helper_module_display(value, cfg);
            } else if (strcmp(key_str, "module_rca") == 0) {
                m5_config_helper_module_rca(value, cfg);
            }
        }
    }
}

mp_obj_t m5_add_display(mp_obj_t dict) {
    if (!MP_OBJ_IS_TYPE(dict, &mp_type_dict)) {
        mp_raise_TypeError("parameter must be a dict");
    }

    auto cfg = M5.config();
    cfg.external_display_value = 0; // disable all external display
    m5_config_helper(dict, cfg);

    mp_printf(&mp_plat_print, "external_display_value: %02X\n", cfg.external_display_value);

    m5::board_t board = M5.getBoard();

    if (cfg.external_display.module_display) {
        if (board == m5::board_t::board_M5Stack || board == m5::board_t::board_M5StackCore2 || board == m5::board_t::board_M5Tough || board == m5::board_t::board_M5StackCoreS3) {
            M5ModuleDisplay dsp(cfg.module_display);
            if (dsp.init()) {
                M5.addDisplay(dsp);
                mp_printf(&mp_plat_print, "module_display added\n");
            }
        } else {
            mp_raise_NotImplementedError("module_display is not supported on this board");
        }
    }
    if (cfg.external_display.module_rca) {
        if (board == m5::board_t::board_M5Stack || board == m5::board_t::board_M5StackCore2 || board == m5::board_t::board_M5Tough) {
            M5ModuleRCA dsp(cfg.module_rca);
            if (dsp.init()) {
                M5.addDisplay(dsp);
                mp_printf(&mp_plat_print, "module_rca added\n");
            }
        } else {
            mp_raise_NotImplementedError("module_rca is not supported on this board");
        }
    }

    return mp_const_none;
}

// TODO: pass configuration parameters
mp_obj_t m5_begin(size_t n_args, const mp_obj_t *args) {
    mp_obj_t config_obj = mp_const_none;

    auto cfg = M5.config();
    cfg.external_display_value = 0; // disable all external display

    if (n_args > 0) {
        config_obj = args[0];
        if (!MP_OBJ_IS_TYPE(config_obj, &mp_type_dict)) {
            mp_raise_TypeError("parameter must be a dict");
        }
        m5_config_helper(config_obj, cfg);
    }

    // initial
    M5.begin(cfg);
    M5.In_I2C.release();

    M5.Display.clear();
    // default display
    m5_display.gfx = (void *)(&(M5.Display));
    // set default font to DejaVu9, keep same style with UIFlow website UI design.
    M5.Display.setTextFont(&fonts::DejaVu9);

    {
        for (uint8_t i = 0; i < 5; i++) {
            MP_STATE_PORT(wasClicked_cb)[i] = mp_const_none;
            MP_STATE_PORT(wasDoubleClicked_cb)[i] = mp_const_none;
            MP_STATE_PORT(wasHold_cb)[i] = mp_const_none;
            MP_STATE_PORT(wasPressed_cb)[i] = mp_const_none;
            MP_STATE_PORT(wasReleased_cb)[i] = mp_const_none;
        }
        m5_btnA.callbacks.wasClicked_cb = &MP_STATE_PORT(wasClicked_cb)[0];
        m5_btnA.callbacks.wasDoubleClicked_cb = &MP_STATE_PORT(wasDoubleClicked_cb)[0];
        m5_btnA.callbacks.wasHold_cb = &MP_STATE_PORT(wasHold_cb)[0];
        m5_btnA.callbacks.wasPressed_cb = &MP_STATE_PORT(wasPressed_cb)[0];
        m5_btnA.callbacks.wasReleased_cb = &MP_STATE_PORT(wasReleased_cb)[0];

        m5_btnB.callbacks.wasClicked_cb = &MP_STATE_PORT(wasClicked_cb)[1];
        m5_btnB.callbacks.wasDoubleClicked_cb = &MP_STATE_PORT(wasDoubleClicked_cb)[1];
        m5_btnB.callbacks.wasHold_cb = &MP_STATE_PORT(wasHold_cb)[1];
        m5_btnB.callbacks.wasPressed_cb = &MP_STATE_PORT(wasPressed_cb)[1];
        m5_btnB.callbacks.wasReleased_cb = &MP_STATE_PORT(wasReleased_cb)[1];

        m5_btnC.callbacks.wasClicked_cb = &MP_STATE_PORT(wasClicked_cb)[2];
        m5_btnC.callbacks.wasDoubleClicked_cb = &MP_STATE_PORT(wasDoubleClicked_cb)[2];
        m5_btnC.callbacks.wasHold_cb = &MP_STATE_PORT(wasHold_cb)[2];
        m5_btnC.callbacks.wasPressed_cb = &MP_STATE_PORT(wasPressed_cb)[2];
        m5_btnC.callbacks.wasReleased_cb = &MP_STATE_PORT(wasReleased_cb)[2];

        m5_btnPWR.callbacks.wasClicked_cb = &MP_STATE_PORT(wasClicked_cb)[3];
        m5_btnPWR.callbacks.wasDoubleClicked_cb = &MP_STATE_PORT(wasDoubleClicked_cb)[3];
        m5_btnPWR.callbacks.wasHold_cb = &MP_STATE_PORT(wasHold_cb)[3];
        m5_btnPWR.callbacks.wasPressed_cb = &MP_STATE_PORT(wasPressed_cb)[3];
        m5_btnPWR.callbacks.wasReleased_cb = &MP_STATE_PORT(wasReleased_cb)[3];

        m5_btnEXT.callbacks.wasClicked_cb = &MP_STATE_PORT(wasClicked_cb)[4];
        m5_btnEXT.callbacks.wasDoubleClicked_cb = &MP_STATE_PORT(wasDoubleClicked_cb)[4];
        m5_btnEXT.callbacks.wasHold_cb = &MP_STATE_PORT(wasHold_cb)[4];
        m5_btnEXT.callbacks.wasPressed_cb = &MP_STATE_PORT(wasPressed_cb)[4];
        m5_btnEXT.callbacks.wasReleased_cb = &MP_STATE_PORT(wasReleased_cb)[4];
    }
    return mp_const_none;
}

mp_obj_t m5_update(void) {
    M5.update();

    m5_btns_callbacks_check();
    return mp_const_none;
}

mp_obj_t m5_end(void) {
    m5_btns_callbacks_deinit();
    return mp_const_none;
}

mp_obj_t m5_getBoard(void) {
    return mp_obj_new_int(BOARD_ID);
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
static void m5_btns_callbacks_check(void) {
    // mp_hal_wake_main_task_from_isr();
    for (uint8_t i = 0; i < 5; i++) {
        if (m5_btn_list[i]->callbacks.flag) {
            if (m5_btn_list[i]->callbacks.flag_bit.wasClicked) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasClicked()) {
                    mp_sched_schedule(*m5_btn_list[i]->callbacks.wasClicked_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasDoubleClicked) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasDoubleClicked()) {
                    mp_sched_schedule(*m5_btn_list[i]->callbacks.wasDoubleClicked_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasHold) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasHold()) {
                    mp_sched_schedule(*m5_btn_list[i]->callbacks.wasHold_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasPressed) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasPressed()) {
                    mp_sched_schedule(*m5_btn_list[i]->callbacks.wasPressed_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }

            if (m5_btn_list[i]->callbacks.flag_bit.wasReleased) {
                if (((m5::Button_Class *)(m5_btn_list[i]->btn))->wasReleased()) {
                    mp_sched_schedule(*m5_btn_list[i]->callbacks.wasReleased_cb,
                        mp_obj_new_int(((m5::Button_Class *)(m5_btn_list[i]->btn))->getState()));
                }
            }
        }
    }
}

static void m5_btns_callbacks_deinit(void) {
    // clear all callback flag bit
    for (uint8_t i = 0; i < 5; i++) {
        m5_btn_list[i]->callbacks.flag = 0;
    }
}

#include "mpy_user_lcd.txt"

#if MICROPY_PY_LVGL
#include "mpy_lvgl.txt"
#endif

MP_REGISTER_ROOT_POINTER(mp_obj_t wasClicked_cb[5]);
MP_REGISTER_ROOT_POINTER(mp_obj_t wasDoubleClicked_cb[5]);
MP_REGISTER_ROOT_POINTER(mp_obj_t wasHold_cb[5]);
MP_REGISTER_ROOT_POINTER(mp_obj_t wasPressed_cb[5]);
MP_REGISTER_ROOT_POINTER(mp_obj_t wasReleased_cb[5]);
}

/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

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
#include <M5Unified.hpp>
#include <M5AtomDisplay.h>
#include <M5ModuleDisplay.h>
#if CONFIG_IDF_TARGET_ESP32
#include <M5ModuleRCA.h>
#include <M5UnitRCA.h>
#endif
// #include <M5UnitOLED.h>
#include "mpy_unitoled.hpp"

// #include <M5UnitMiniOLED.h>
#include "mpy_unitminioled.hpp"

#include <M5UnitLCD.h>
// #include "mpy_unitlcd.hpp"

#include <M5UnitGLASS.h>
// #include "mpy_unitglass.hpp"

// #include <M5UnitGLASS2.h>
#include "mpy_unitglass2.hpp"

#include <utility/Button_Class.hpp>

extern "C"
{
#include "mpy_m5unified.h"
#include "mphalport.h"

#define MICROPY_HW_ESP_NEW_I2C_DRIVER 1

// #include <driver/periph_ctrl.h>
#if MICROPY_HW_ESP_NEW_I2C_DRIVER
#include "driver/i2c_master.h"
#else
#include "driver/i2c.h"
#include "hal/i2c_ll.h"
#endif

// machine_i2c.c
typedef struct _machine_hw_i2c_obj_t {
    mp_obj_base_t base;
    i2c_master_bus_handle_t bus_handle;
    #if ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(5, 5, 0)
    i2c_master_dev_handle_t dev_handle;
    #endif
    uint8_t port : 8;
    gpio_num_t scl : 8;
    gpio_num_t sda : 8;
    uint32_t freq;
    uint32_t timeout_us;
} machine_hw_i2c_obj_t;

static void m5_btns_callbacks_check(void);
static void m5_btns_callbacks_deinit(void);
mp_obj_t m5_getDisplay(mp_obj_t index);

/* *FORMAT-OFF* */
const spk_obj_t m5_speaker = {&mp_spk_type,       &(M5.Speaker)};
const pwr_obj_t m5_power   = {&mp_power_type,     &(M5.Power)  };
const pwr_obj_t m5_imu     = {&mp_imu_type,       &(M5.Imu)    };
const pwr_obj_t m5_led     = {&mp_led_type,       &(M5.Led)    };
      als_obj_t m5_als     = {&mp_als_type,       &(M5.Als)    };
      btn_obj_t m5_btnA    = {&mp_btn_type,       &(M5.BtnA),   {0}};
      btn_obj_t m5_btnB    = {&mp_btn_type,       &(M5.BtnB),   {0}};
      btn_obj_t m5_btnC    = {&mp_btn_type,       &(M5.BtnC),   {0}};
      btn_obj_t m5_btnPWR  = {&mp_btn_type,       &(M5.BtnPWR), {0}};
      btn_obj_t m5_btnEXT  = {&mp_btn_type,       &(M5.BtnEXT), {0}};
      gfx_obj_t m5_display = {&mp_gfxdevice_type, &(M5.Display), NULL};
      touch_obj_t m5_touch = {&mp_touch_type,     &(M5.Touch)  };
const mic_obj_t m5_mic     = {&mp_mic_type,       &(M5.Mic)    };

static btn_obj_t *m5_btn_list[5] = {&m5_btnA, &m5_btnB, &m5_btnC, &m5_btnPWR, &m5_btnEXT};
/* *FORMAT-ON* */


static void m5_config_helper_module_display(mp_obj_t config_obj, M5ModuleDisplay::config_t &cfg) {
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
                // cfg.external_display.module_display = mp_obj_is_true(value);
            } else if (strcmp(key_str, "width") == 0) {
                // cfg.module_display.logical_width = mp_obj_get_int(value);
                cfg.logical_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "height") == 0) {
                // cfg.module_display.logical_height = mp_obj_get_int(value);
                cfg.logical_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "refresh_rate") == 0) {
                // cfg.module_display.refresh_rate = mp_obj_get_int(value);
                cfg.refresh_rate = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_width") == 0) {
                // cfg.module_display.output_width = mp_obj_get_int(value);
                cfg.output_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_height") == 0) {
                // cfg.module_display.output_height = mp_obj_get_int(value);
                cfg.output_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "scale_w") == 0) {
                // cfg.module_display.scale_w = mp_obj_get_int(value);
                cfg.scale_w = mp_obj_get_int(value);
            } else if (strcmp(key_str, "scale_h") == 0) {
                // cfg.module_display.scale_h = mp_obj_get_int(value);
                cfg.scale_h = mp_obj_get_int(value);
            } else if (strcmp(key_str, "pixel_clock") == 0) {
                // cfg.module_display.pixel_clock = mp_obj_get_int(value);
                cfg.pixel_clock = mp_obj_get_int(value);
            }
        }
    }
}

static void m5_config_helper_atom_display(mp_obj_t config_obj, M5AtomDisplay::config_t &cfg) {
    if (!MP_OBJ_IS_TYPE(config_obj, &mp_type_dict)) {
        mp_raise_TypeError("atom_display must be a dict");
    }

    // cfg.atom_display = M5AtomDisplay::config_t();
    mp_map_t *config_map = mp_obj_dict_get_map(config_obj);

    for (size_t i = 0; i < config_map->alloc; i++) {
        if (MP_MAP_SLOT_IS_FILLED(config_map, i)) {
            mp_obj_t key = config_map->table[i].key;
            mp_obj_t value = config_map->table[i].value;

            const char *key_str = mp_obj_str_get_str(key);

            if (strcmp(key_str, "enabled") == 0) {
                // cfg.external_display.atom_display = mp_obj_is_true(value);
            } else if (strcmp(key_str, "width") == 0) {
                // cfg.atom_display.logical_width = mp_obj_get_int(value);
                cfg.logical_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "height") == 0) {
                // cfg.atom_display.logical_height = mp_obj_get_int(value);
                cfg.logical_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "refresh_rate") == 0) {
                // cfg.atom_display.refresh_rate = mp_obj_get_int(value);
                cfg.refresh_rate = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_width") == 0) {
                // cfg.atom_display.output_width = mp_obj_get_int(value);
                cfg.output_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_height") == 0) {
                // cfg.atom_display.output_height = mp_obj_get_int(value);
                cfg.output_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "scale_w") == 0) {
                // cfg.atom_display.scale_w = mp_obj_get_int(value);
                cfg.scale_w = mp_obj_get_int(value);
            } else if (strcmp(key_str, "scale_h") == 0) {
                // cfg.atom_display.scale_h = mp_obj_get_int(value);
                cfg.scale_h = mp_obj_get_int(value);
            } else if (strcmp(key_str, "pixel_clock") == 0) {
                // cfg.atom_display.pixel_clock = mp_obj_get_int(value);
                cfg.pixel_clock = mp_obj_get_int(value);
            }
        }
    }
}

#if CONFIG_IDF_TARGET_ESP32
static void m5_config_helper_module_rca(mp_obj_t config_obj, M5ModuleRCA::config_t &cfg) {
    if (!MP_OBJ_IS_TYPE(config_obj, &mp_type_dict)) {
        mp_raise_TypeError("module_rca must be a dict");
    }

    // cfg.module_rca = M5ModuleRCA::config_t();
    mp_map_t *config_map = mp_obj_dict_get_map(config_obj);

    for (size_t i = 0; i < config_map->alloc; i++) {
        if (MP_MAP_SLOT_IS_FILLED(config_map, i)) {
            mp_obj_t key = config_map->table[i].key;
            mp_obj_t value = config_map->table[i].value;

            const char *key_str = mp_obj_str_get_str(key);

            if (strcmp(key_str, "enabled") == 0) {
                // cfg.external_display.module_rca = mp_obj_get_int(value);
            } else if (strcmp(key_str, "width") == 0) {
                // cfg.module_rca.logical_width = mp_obj_get_int(value);
                cfg.logical_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "height") == 0) {
                // cfg.module_rca.logical_height = mp_obj_get_int(value);
                cfg.logical_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_width") == 0) {
                // cfg.module_rca.output_width = mp_obj_get_int(value);
                cfg.output_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_height") == 0) {
                // cfg.module_rca.output_height = mp_obj_get_int(value);
                cfg.output_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "signal_type") == 0) {
                // cfg.module_rca.signal_type = (M5ModuleRCA::signal_type_t)mp_obj_get_int(value);
                cfg.signal_type = (M5ModuleRCA::signal_type_t)mp_obj_get_int(value);
            } else if (strcmp(key_str, "use_psram") == 0) {
                // cfg.module_rca.use_psram = (M5ModuleRCA::use_psram_t)mp_obj_get_int(value);
                cfg.use_psram = (M5ModuleRCA::use_psram_t)mp_obj_get_int(value);
            } else if (strcmp(key_str, "pin_dac") == 0) {
                // cfg.module_rca.pin_dac = mp_obj_get_int(value);
                cfg.pin_dac = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_level") == 0) {
                // cfg.module_rca.output_level = mp_obj_get_int(value);
                cfg.output_level = mp_obj_get_int(value);
            }
        }
    }
}


static void m5_config_helper_unit_rca(mp_obj_t config_obj, M5UnitRCA::config_t &cfg) {
    if (!MP_OBJ_IS_TYPE(config_obj, &mp_type_dict)) {
        mp_raise_TypeError("unit_rca must be a dict");
    }

    // cfg.unit_rca = M5UnitRCA::config_t();
    mp_map_t *config_map = mp_obj_dict_get_map(config_obj);

    for (size_t i = 0; i < config_map->alloc; i++) {
        if (MP_MAP_SLOT_IS_FILLED(config_map, i)) {
            mp_obj_t key = config_map->table[i].key;
            mp_obj_t value = config_map->table[i].value;

            const char *key_str = mp_obj_str_get_str(key);

            if (strcmp(key_str, "enabled") == 0) {
                // cfg.external_display.unit_rca = mp_obj_get_int(value);
            } else if (strcmp(key_str, "width") == 0) {
                // cfg.unit_rca.logical_width = mp_obj_get_int(value);
                cfg.logical_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "height") == 0) {
                // cfg.unit_rca.logical_height = mp_obj_get_int(value);
                cfg.logical_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_width") == 0) {
                // cfg.unit_rca.output_width = mp_obj_get_int(value);
                cfg.output_width = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_height") == 0) {
                // cfg.unit_rca.output_height = mp_obj_get_int(value);
                cfg.output_height = mp_obj_get_int(value);
            } else if (strcmp(key_str, "signal_type") == 0) {
                // cfg.unit_rca.signal_type = (M5UnitRCA::signal_type_t)mp_obj_get_int(value);
                cfg.signal_type = (M5UnitRCA::signal_type_t)mp_obj_get_int(value);
            } else if (strcmp(key_str, "use_psram") == 0) {
                // cfg.unit_rca.use_psram = (M5UnitRCA::use_psram_t)mp_obj_get_int(value);
                cfg.use_psram = (M5UnitRCA::use_psram_t)mp_obj_get_int(value);
            } else if (strcmp(key_str, "pin_dac") == 0) {
                // cfg.unit_rca.pin_dac = mp_obj_get_int(value);
                cfg.pin_dac = mp_obj_get_int(value);
            } else if (strcmp(key_str, "output_level") == 0) {
                // cfg.unit_rca.output_level = mp_obj_get_int(value);
                cfg.output_level = mp_obj_get_int(value);
            }
        }
    }
}
#endif

mp_obj_t m5_add_display(mp_obj_t i2c_bus_in, mp_obj_t addr_in, mp_obj_t dict) {
    if (!MP_OBJ_IS_TYPE(dict, &mp_type_dict)) {
        mp_raise_TypeError("parameter must be a dict");
    }

    machine_hw_i2c_obj_t *i2c_bus = (machine_hw_i2c_obj_t *)i2c_bus_in;
    uint8_t addr = mp_obj_get_int(addr_in);

    mp_map_t *config_map = mp_obj_dict_get_map(dict);

    // mp_printf(&mp_plat_print, "external_display_value: %02X\n", cfg.external_display_value);

    m5::board_t board = M5.getBoard();

    for (size_t i = 0; i < config_map->alloc; i++) {
        if (MP_MAP_SLOT_IS_FILLED(config_map, i)) {
            mp_obj_t key = config_map->table[i].key;
            mp_obj_t value = config_map->table[i].value;

            const char *key_str = mp_obj_str_get_str(key);

            if (strcmp(key_str, "module_display") == 0) {
                M5ModuleDisplay::config_t cfg;
                m5_config_helper_module_display(value, cfg);
                if (board == m5::board_t::board_M5Stack || board == m5::board_t::board_M5StackCore2 || board == m5::board_t::board_M5Tough || board == m5::board_t::board_M5StackCoreS3) {
                    M5ModuleDisplay dsp(cfg);
                    if (dsp.init()) {
                        M5.addDisplay(dsp);
                        mp_printf(&mp_plat_print, "module_display added\n");
                    }
                } else {
                    mp_raise_NotImplementedError("module_display is not supported on this board");
                }
            } else if (strcmp(key_str, "atom_display") == 0) {
                M5AtomDisplay::config_t cfg;
                m5_config_helper_atom_display(value, cfg);
                M5AtomDisplay dsp(cfg);
                if (dsp.init_without_reset()) {
                    M5.addDisplay(dsp);
                    mp_printf(&mp_plat_print, "atom_display added\n");
                } else {
                    mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("AtomDisplay init failed"));
                }
            }
            #if CONFIG_IDF_TARGET_ESP32
            else if (strcmp(key_str, "module_rca") == 0) {
                M5ModuleRCA::config_t cfg;
                m5_config_helper_module_rca(value, cfg);
                if (board == m5::board_t::board_M5Stack || board == m5::board_t::board_M5StackCore2 || board == m5::board_t::board_M5Tough) {
                    M5ModuleRCA dsp(cfg);
                    if (dsp.init()) {
                        M5.addDisplay(dsp);
                        mp_printf(&mp_plat_print, "module_rca added\n");
                    }
                } else {
                    mp_raise_NotImplementedError("module_rca is not supported on this board");
                }
            } else if (strcmp(key_str, "unit_rca") == 0) {
                M5UnitRCA::config_t cfg;
                m5_config_helper_unit_rca(value, cfg);
                M5UnitRCA dsp(cfg);
                if (dsp.init()) {
                    M5.addDisplay(dsp);
                    mp_printf(&mp_plat_print, "unit_rca added\n");
                } else {
                    mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("RCA Unit init failed"));
                }
            }
            #endif
            else if (strcmp(key_str, "unit_lcd") == 0) {
                M5UnitLCD::config_t cfg;
                cfg.i2c_addr = addr;
                cfg.i2c_freq = i2c_bus->freq;
                cfg.i2c_port = i2c_bus->port;
                cfg.pin_scl = i2c_bus->scl;
                cfg.pin_sda = i2c_bus->sda;

                M5UnitLCD dsp(cfg);
                if (dsp.init()) {
                    M5.addDisplay(dsp);
                    mp_printf(&mp_plat_print, "unit_lcd added\n");
                } else {
                    mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("LCD Unit init failed"));
                }
            } else if (strcmp(key_str, "unit_oled") == 0) {
                MPY_M5UnitOLED::config_t cfg;
                cfg.i2c_addr = addr;
                mp_load_method_maybe(i2c_bus_in, MP_QSTR_readfrom_into, cfg.readfrom_into_method);
                mp_load_method_maybe(i2c_bus_in, MP_QSTR_writeto, cfg.writeto_method);

                MPY_M5UnitOLED dsp(cfg);
                if (dsp.init()) {
                    M5.addDisplay(dsp);
                    mp_printf(&mp_plat_print, "unit_oled added\n");
                } else {
                    mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("OLED Unit init failed"));
                }
            } else if (strcmp(key_str, "unit_mini_oled") == 0) {
                MPY_M5UnitMiniOLED::config_t cfg;
                cfg.i2c_addr = addr;
                mp_load_method_maybe(i2c_bus_in, MP_QSTR_readfrom_into, cfg.readfrom_into_method);
                mp_load_method_maybe(i2c_bus_in, MP_QSTR_writeto, cfg.writeto_method);

                MPY_M5UnitMiniOLED dsp(cfg);
                if (dsp.init()) {
                    M5.addDisplay(dsp);
                    mp_printf(&mp_plat_print, "unit_mini_oled added\n");
                } else {
                    mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("MiniOLED Unit init failed"));
                }
            } else if (strcmp(key_str, "unit_glass") == 0) {
                #if defined(__M5GFX_M5UNITGLASS__)
                M5UnitGLASS::config_t cfg;
                cfg.i2c_addr = addr;
                cfg.i2c_freq = i2c_bus->freq;
                cfg.i2c_port = i2c_bus->port;
                cfg.pin_scl = i2c_bus->scl;
                cfg.pin_sda = i2c_bus->sda;

                M5UnitGLASS dsp(cfg);
                #else
                MPY_M5UnitGLASS::config_t cfg;
                cfg.i2c_addr = addr;
                mp_load_method_maybe(i2c_bus_in, MP_QSTR_readfrom_into, cfg.readfrom_into_method);
                mp_load_method_maybe(i2c_bus_in, MP_QSTR_writeto, cfg.writeto_method);

                MPY_M5UnitGLASS dsp(cfg);
                #endif
                if (dsp.init()) {
                    M5.addDisplay(dsp);
                    mp_printf(&mp_plat_print, "unit_glass added\n");
                } else {
                    mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("GLASS Unit init failed"));
                }
            } else if (strcmp(key_str, "unit_glass2") == 0) {
                MPY_M5UnitGLASS2::config_t cfg;
                cfg.i2c_addr = addr;
                mp_load_method_maybe(i2c_bus_in, MP_QSTR_readfrom_into, cfg.readfrom_into_method);
                mp_load_method_maybe(i2c_bus_in, MP_QSTR_writeto, cfg.writeto_method);

                MPY_M5UnitGLASS2 dsp(cfg);
                if (dsp.init()) {
                    M5.addDisplay(dsp);
                    mp_printf(&mp_plat_print, "unit_glass2 added\n");
                } else {
                    mp_raise_msg_varg(&mp_type_OSError, MP_ERROR_TEXT("GLASS2 Unit init failed"));
                }
            } else {
                mp_printf(&mp_plat_print, "%s is not a valid display.\n", key_str);
            }
        }
    }

    return m5_getDisplay(mp_obj_new_int(M5.getDisplayCount() - 1));
}


mp_obj_t m5_create_speaker(void) {
    auto spk = new m5::Speaker_Class();
    spk_obj_t *o = mp_obj_malloc_with_finaliser(spk_obj_t, &mp_spk_type);
    o->spk = spk;
    return MP_OBJ_FROM_PTR(o);
}


mp_obj_t m5_create_mic(void) {
    auto mic = new m5::Mic_Class();
    mic_obj_t *o = mp_obj_malloc_with_finaliser(mic_obj_t, &mp_mic_type);
    o->mic = mic;
    return MP_OBJ_FROM_PTR(o);
}


static void in_i2c_init(void) {
    gpio_num_t in_scl = (gpio_num_t)M5.getPin(m5::pin_name_t::in_i2c_scl);
    gpio_num_t in_sda = (gpio_num_t)M5.getPin(m5::pin_name_t::in_i2c_sda);
    gpio_num_t ex_scl = (gpio_num_t)M5.getPin(m5::pin_name_t::ex_i2c_scl);
    gpio_num_t ex_sda = (gpio_num_t)M5.getPin(m5::pin_name_t::ex_i2c_sda);
    i2c_port_t ex_port = I2C_NUM_0;
    #if SOC_I2C_NUM == 1 || defined(CONFIG_IDF_TARGET_ESP32C6)
    i2c_port_t in_port = I2C_NUM_0;
    #else
    i2c_port_t in_port = I2C_NUM_1;
    if (in_scl == ex_scl && in_sda == ex_sda) {
        in_port = ex_port;
    }
    #endif

    if (in_scl != GPIO_NUM_NC || in_sda != GPIO_NUM_NC) {
        ESP_LOGI("BOARD", "Internal I2C(%d) init", in_port);
        // if (in_port == I2C_NUM_0) {
        //     periph_module_enable(PERIPH_I2C0_MODULE);
        // } else {
        //     periph_module_enable(PERIPH_I2C1_MODULE);
        // }
        #if MICROPY_HW_ESP_NEW_I2C_DRIVER
        i2c_master_bus_handle_t bus_handle;
        if (i2c_master_get_bus_handle(in_port, &bus_handle) == ESP_ERR_INVALID_STATE) {
            i2c_master_bus_config_t i2c_bus_config;
            memset(&i2c_bus_config, 0, sizeof(i2c_bus_config));
            i2c_bus_config.clk_source = I2C_CLK_SRC_DEFAULT;
            i2c_bus_config.i2c_port = in_port;
            i2c_bus_config.scl_io_num = in_scl;
            i2c_bus_config.sda_io_num = in_sda;
            i2c_bus_config.glitch_ignore_cnt = 7;
            i2c_bus_config.flags.enable_internal_pullup = true;
            i2c_new_master_bus(&i2c_bus_config, &bus_handle);
        }
        #else
        i2c_config_t conf;
        memset(&conf, 0, sizeof(i2c_config_t));
        conf.mode = I2C_MODE_MASTER;
        conf.sda_io_num = in_sda;
        conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
        conf.scl_io_num = in_scl;
        conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
        conf.master.clk_speed = 100000;
        // .clk_flags = 0,          /*!< Optional, you can use I2C_SCLK_SRC_FLAG_* flags to choose i2c source clock here. */
        i2c_param_config(in_port, &conf);
        i2c_driver_install(in_port, I2C_MODE_MASTER, 0, 0, 0);
        #endif
    }
}

void rtc_sync(struct timeval *tv_in) {
    struct timeval tv;
    if (tv_in == nullptr) {
        gettimeofday(&tv, NULL);
    } else {
        tv = *tv_in;
    }
    struct tm now;
    localtime_r(&tv.tv_sec, &now);
    M5.Rtc.setDateTime(&now);
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
        // m5_config_helper(config_obj, cfg);
    }

    // initial
    M5.begin(cfg);
    M5.Power.setExtOutput(true); // enable external power by default
    M5.In_I2C.release();
    in_i2c_init();
    // if (M5.getBoard() != m5::board_t::board_M5StackCoreS3
    //     && M5.getBoard() != m5::board_t::board_M5StackCoreS3SE
    //     && M5.getBoard() != m5::board_t::board_M5StackCore2
    //     && M5.getBoard() != m5::board_t::board_M5Tough
    //     && M5.getBoard() != m5::board_t::board_M5AtomS3
    // ) {

    // }

    M5.Display.clear();
    // default display
    m5_display.gfx = (void *)(&(M5.Display));
    // set default font to DejaVu9, keep same style with UIFlow website UI design.
    M5.Display.setTextFont(&fonts::DejaVu9);

    // get local time and sync to RTC IC
    rtc_sync(nullptr);

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
    gfx_obj_t *o = mp_obj_malloc_with_finaliser(gfx_obj_t, &mp_gfxdevice_type);
    o->gfx = (void *)&(M5.Displays(mp_obj_get_int(index)));
    return MP_OBJ_FROM_PTR(o);
}

mp_obj_t m5_getDisplay(mp_obj_t index) {
    gfx_obj_t *o = mp_obj_malloc_with_finaliser(gfx_obj_t, &mp_gfxdevice_type);
    o->gfx = (void *)&(M5.getDisplay(mp_obj_get_int(index)));
    return MP_OBJ_FROM_PTR(o);
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

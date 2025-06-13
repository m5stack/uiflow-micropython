/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "m5unified.h"

#if MICROPY_PY_LVGL
// -------- lvgl port
#include "freertos/FreeRTOS.h"
#include "freertos/timers.h"
#include "esp_log.h"
#include "lvgl/demos/benchmark/lv_demo_benchmark.h"

static TimerHandle_t lvgl_timer = NULL;

mp_obj_t mp_lv_task_handler(mp_obj_t self_in) {
    lv_task_handler();
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(mp_lv_task_handler_obj, mp_lv_task_handler);

static void vTimerCallback(TimerHandle_t plvgl_timer) {
    lv_tick_inc(portTICK_PERIOD_MS * 10);
    mp_sched_schedule((mp_obj_t)&mp_lv_task_handler_obj, mp_const_none);
}

void lvgl_deinit() {
    lv_deinit();
    if (lvgl_timer) {
        xTimerDelete(lvgl_timer, portMAX_DELAY);
        lvgl_timer = NULL;
    }
}

#include "driver/ppa.h"
#if SOC_PPA_SUPPORTED
ppa_client_handle_t ppa_srm_handle = NULL;
#endif
mp_obj_t gfx_lvgl_init(mp_obj_t self) {
    if (lvgl_timer) {
        return mp_const_none;
    }

    #if SOC_PPA_SUPPORTED
    ppa_client_config_t ppa_srm_config = {
        .oper_type = PPA_OPERATION_SRM,
    };
    ppa_register_client(&ppa_srm_config, &ppa_srm_handle);
    #endif

    lv_init();
    lvgl_timer = xTimerCreate("lvgl_timer", 10, pdTRUE, NULL, vTimerCallback);

    if (lvgl_timer == NULL || xTimerStart(lvgl_timer, 0) != pdPASS) {
        ESP_LOGE("LVGL", "Failed creating or starting LVGL timer!");
    }
    return mp_const_none;
}

mp_obj_t gfx_lvgl_deinit(mp_obj_t self) {
    lvgl_deinit();
    return mp_const_none;
}

#if MICROPY_PY_LVGL_BENCHMARK
mp_obj_t gfx_lvgl_benchmark(mp_obj_t self) {
    lv_demo_benchmark();
    return mp_const_none;
}
#endif

#endif

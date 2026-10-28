/*
 * SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include <string.h>
#include <stdbool.h>
#include "py/nlr.h"
#include "py/obj.h"
#include "py/objtuple.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "driver/rmt_rx.h"
#include "driver/rmt_tx.h"
#include "driver/rmt_encoder.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_log.h"
#include "soc/soc_caps.h"

static const char *TAG = "rmt_ir";

// NEC timing spec (in microseconds)
#define NEC_LEADING_CODE_DURATION_0  9000  // Leading pulse
#define NEC_LEADING_CODE_DURATION_1  4500  // Leading space
#define NEC_PAYLOAD_ZERO_DURATION_0  560   // Logic 0 pulse
#define NEC_PAYLOAD_ZERO_DURATION_1  560   // Logic 0 space
#define NEC_PAYLOAD_ONE_DURATION_0   560   // Logic 1 pulse
#define NEC_PAYLOAD_ONE_DURATION_1   1690  // Logic 1 space
#define NEC_REPEAT_CODE_DURATION_0   9000  // Repeat pulse
#define NEC_REPEAT_CODE_DURATION_1   2250  // Repeat space

#define IR_NEC_DECODE_MARGIN         200   // Decode tolerance in microseconds

typedef rmt_symbol_word_t rmt_item32_t;

typedef struct _rmt_ir_obj_t {
    mp_obj_base_t base;
    int in_pin;
    int tx_pin;
} rmt_ir_obj_t;

extern const mp_obj_type_t mp_ir_nec8_type;

// These pointers outlive the constructor and are used by a native task.
// Plain C statics are not scanned by MicroPython's garbage collector.
MP_REGISTER_ROOT_POINTER(mp_obj_t rmt_ir_rx_callback);
MP_REGISTER_ROOT_POINTER(void *rmt_ir_rx_symbols);
#define ir_rx_callback MP_STATE_PORT(rmt_ir_rx_callback)
#define ir_rx_symbols MP_STATE_PORT(rmt_ir_rx_symbols)
static TaskHandle_t ir_rx_task_handle = NULL;
static QueueHandle_t ir_rx_done_queue = NULL;
static bool ir_rx_is_initialized = false;
static rmt_channel_handle_t ir_rx_channel = NULL;
static int ir_rx_initialized_pin = -1;
static size_t ir_rx_symbol_buf_num = 0;
static uint16_t ir_nec_address = 0;
static uint16_t ir_nec_command = 0;
static bool ir_is_repeat = false;
static bool ir_data_ready = false;

static bool ir_tx_is_initialized = false;
static rmt_channel_handle_t ir_tx_channel = NULL;
static rmt_encoder_handle_t ir_tx_encoder = NULL;
static int ir_tx_initialized_pin = -1;

static const rmt_receive_config_t ir_rx_receive_config = {
    .signal_range_min_ns = 1250,     // 1.25us
    .signal_range_max_ns = 12000000, // 12ms
};

static inline void nec_fill_item(rmt_item32_t *item, uint32_t high_us, uint32_t low_us) {
    item->duration0 = high_us;
    item->level0 = 1;
    item->duration1 = low_us;
    item->level1 = 0;
}

static int nec_build_frame(uint16_t address, uint16_t command, rmt_item32_t *items) {
    int idx = 0;
    nec_fill_item(&items[idx++], NEC_LEADING_CODE_DURATION_0, NEC_LEADING_CODE_DURATION_1);

    uint32_t data = ((uint32_t)command << 16) | address;
    for (int i = 0; i < 32; i++) {
        if (data & 0x1) {
            nec_fill_item(&items[idx++], NEC_PAYLOAD_ONE_DURATION_0, NEC_PAYLOAD_ONE_DURATION_1);
        } else {
            nec_fill_item(&items[idx++], NEC_PAYLOAD_ZERO_DURATION_0, NEC_PAYLOAD_ZERO_DURATION_1);
        }
        data >>= 1;
    }

    nec_fill_item(&items[idx++], NEC_PAYLOAD_ZERO_DURATION_0, 0);
    return idx;
}

static inline bool nec_check_in_range(uint32_t signal_duration, uint32_t spec_duration) {
    return (signal_duration < (spec_duration + IR_NEC_DECODE_MARGIN))
           && (signal_duration > (spec_duration - IR_NEC_DECODE_MARGIN));
}

static bool nec_parse_logic0(rmt_item32_t *item) {
    return nec_check_in_range(item->duration0, NEC_PAYLOAD_ZERO_DURATION_0) &&
           nec_check_in_range(item->duration1, NEC_PAYLOAD_ZERO_DURATION_1);
}

static bool nec_parse_logic1(rmt_item32_t *item) {
    return nec_check_in_range(item->duration0, NEC_PAYLOAD_ONE_DURATION_0) &&
           nec_check_in_range(item->duration1, NEC_PAYLOAD_ONE_DURATION_1);
}

static bool nec_parse_frame(rmt_item32_t *items) {
    rmt_item32_t *cur = items;

    uint16_t addr = 0;
    uint16_t cmd = 0;
    bool valid_leading_code = nec_check_in_range(cur->duration0, NEC_LEADING_CODE_DURATION_0) &&
        nec_check_in_range(cur->duration1, NEC_LEADING_CODE_DURATION_1);

    if (!valid_leading_code) {
        return false;
    }
    cur++;
    for (int i = 0; i < 16; i++) {
        if (nec_parse_logic1(cur)) {
            addr |= 1 << i;
        } else if (nec_parse_logic0(cur)) {
            addr &= ~(1 << i);
        } else {
            return false;
        }
        cur++;
    }
    for (int i = 0; i < 16; i++) {
        if (nec_parse_logic1(cur)) {
            cmd |= 1 << i;
        } else if (nec_parse_logic0(cur)) {
            cmd &= ~(1 << i);
        } else {
            return false;
        }
        cur++;
    }
    ir_nec_address = addr;
    ir_nec_command = cmd;

    return true;
}

static bool nec_parse_frame_repeat(rmt_item32_t *item) {
    return nec_check_in_range(item->duration0, NEC_REPEAT_CODE_DURATION_0)
           && nec_check_in_range(item->duration1, NEC_REPEAT_CODE_DURATION_1);
}

static void process_nec_frame(rmt_item32_t *items, size_t symbol_num) {
    ir_is_repeat = false;
    ir_data_ready = false;

    if (symbol_num == 34) {
        if (nec_parse_frame(items)) {
            ir_data_ready = true;
        }
    } else if (symbol_num == 2) {
        if (nec_parse_frame_repeat(items)) {
            ir_is_repeat = true;
            ir_data_ready = true;
        }
    }

    if (ir_data_ready && ir_rx_callback != MP_OBJ_NULL && ir_rx_callback != mp_const_none) {
        mp_sched_schedule(ir_rx_callback, mp_const_none);
    }
}

static bool ir_rx_done_callback(rmt_channel_handle_t channel, const rmt_rx_done_event_data_t *edata, void *user_data) {
    BaseType_t high_task_wakeup = pdFALSE;
    (void)channel;
    if (ir_rx_done_queue != NULL) {
        xQueueSendFromISR(ir_rx_done_queue, edata, &high_task_wakeup);
    }
    return high_task_wakeup == pdTRUE;
}

static void ir_rx_task(void *param) {
    (void)param;
    rmt_rx_done_event_data_t rx_data;
    while (ir_rx_is_initialized && ir_rx_done_queue != NULL) {
        if (xQueueReceive(ir_rx_done_queue, &rx_data, portMAX_DELAY) == pdTRUE) {
            if (!ir_rx_is_initialized) {
                continue;
            }
            process_nec_frame((rmt_item32_t *)rx_data.received_symbols, rx_data.num_symbols);
            (void)rmt_receive(ir_rx_channel, ir_rx_symbols,
                ir_rx_symbol_buf_num * sizeof(rmt_symbol_word_t), &ir_rx_receive_config);
        }
    }
    ir_rx_task_handle = NULL;
    vTaskDelete(NULL);
}

static void deinit_rx_if_needed(void) {
    if (!ir_rx_is_initialized) {
        return;
    }
    ir_rx_is_initialized = false;
    // Stop ISR producers before deleting the worker, queue and GC buffer.
    if (ir_rx_channel) {
        rmt_disable(ir_rx_channel);
    }
    if (ir_rx_task_handle) {
        vTaskDelete(ir_rx_task_handle);
        ir_rx_task_handle = NULL;
    }
    if (ir_rx_done_queue) {
        vQueueDelete(ir_rx_done_queue);
        ir_rx_done_queue = NULL;
    }
    if (ir_rx_channel) {
        rmt_del_channel(ir_rx_channel);
        ir_rx_channel = NULL;
    }
    if (ir_rx_symbols) {
        m_free(ir_rx_symbols);
        ir_rx_symbols = NULL;
    }
    ir_rx_symbol_buf_num = 0;
    ir_rx_initialized_pin = -1;
}

static void deinit_tx_if_needed(void) {
    if (!ir_tx_is_initialized) {
        return;
    }
    if (ir_tx_channel) {
        rmt_disable(ir_tx_channel);
        rmt_del_channel(ir_tx_channel);
        ir_tx_channel = NULL;
    }
    if (ir_tx_encoder) {
        rmt_del_encoder(ir_tx_encoder);
        ir_tx_encoder = NULL;
    }
    ir_tx_is_initialized = false;
    ir_tx_initialized_pin = -1;
}

// Called before a soft reset sweeps the Python heap. The RMT task must not
// keep using a receive buffer or callback from the previous VM instance.
void rmt_ir_deinit(void) {
    ir_rx_callback = mp_const_none;
    deinit_rx_if_needed();
    deinit_tx_if_needed();
    ir_data_ready = false;
}

static esp_err_t init_tx_if_needed(int tx_pin) {
    if (tx_pin < 0) {
        return ESP_OK;
    }
    if (ir_tx_is_initialized) {
        if (tx_pin != ir_tx_initialized_pin) {
            deinit_tx_if_needed();
        } else {
            return ESP_OK;
        }
    }

    rmt_tx_channel_config_t tx_chan_cfg = {};
    tx_chan_cfg.gpio_num = tx_pin;
    tx_chan_cfg.clk_src = RMT_CLK_SRC_DEFAULT;
    tx_chan_cfg.resolution_hz = 1000000;
    tx_chan_cfg.mem_block_symbols = 64;
    tx_chan_cfg.trans_queue_depth = 4;
    esp_err_t err = rmt_new_tx_channel(&tx_chan_cfg, &ir_tx_channel);
    if (err != ESP_OK) {
        return err;
    }

    rmt_carrier_config_t carrier_cfg = {
        .frequency_hz = 38000, // 38KHz 载波
        .duty_cycle = 0.33f,   // 33% 占空比
    };
    err = rmt_apply_carrier(ir_tx_channel, &carrier_cfg);
    if (err != ESP_OK) {
        deinit_tx_if_needed();
        return err;
    }

    rmt_copy_encoder_config_t copy_encoder_cfg = {};
    err = rmt_new_copy_encoder(&copy_encoder_cfg, &ir_tx_encoder);
    if (err != ESP_OK) {
        deinit_tx_if_needed();
        return err;
    }

    err = rmt_enable(ir_tx_channel);
    if (err != ESP_OK) {
        deinit_tx_if_needed();
        return err;
    }
    ir_tx_initialized_pin = tx_pin;
    ir_tx_is_initialized = true;
    return ESP_OK;
}

static esp_err_t init_rx_if_needed(int rx_pin) {
    if (rx_pin < 0) {
        return ESP_OK;
    }
    if (ir_rx_is_initialized) {
        if (rx_pin != ir_rx_initialized_pin) {
            deinit_rx_if_needed();
        } else {
            return ESP_OK;
        }
    }

    rmt_rx_channel_config_t rx_chan_cfg = {};
    rx_chan_cfg.gpio_num = rx_pin;
    rx_chan_cfg.clk_src = RMT_CLK_SRC_DEFAULT;
    rx_chan_cfg.resolution_hz = 1000000;
    rx_chan_cfg.mem_block_symbols = 64;
    esp_err_t err = rmt_new_rx_channel(&rx_chan_cfg, &ir_rx_channel);
    if (err != ESP_OK) {
        return err;
    }

    rmt_rx_event_callbacks_t cbs = {
        .on_recv_done = ir_rx_done_callback,
    };
    err = rmt_rx_register_event_callbacks(ir_rx_channel, &cbs, ir_rx_done_queue);
    if (err != ESP_OK) {
        deinit_rx_if_needed();
        return err;
    }

    err = rmt_enable(ir_rx_channel);
    if (err != ESP_OK) {
        deinit_rx_if_needed();
        return err;
    }

    gpio_set_direction(rx_pin, GPIO_MODE_INPUT);
    gpio_set_pull_mode(rx_pin, GPIO_PULLUP_ONLY);
    ir_rx_symbol_buf_num = 64;
    ir_rx_symbols = m_malloc(ir_rx_symbol_buf_num * sizeof(rmt_symbol_word_t));
    if (ir_rx_symbols == NULL) {
        deinit_rx_if_needed();
        return ESP_ERR_NO_MEM;
    }

    ir_rx_done_queue = xQueueCreate(1, sizeof(rmt_rx_done_event_data_t));
    if (ir_rx_done_queue == NULL) {
        deinit_rx_if_needed();
        return ESP_ERR_NO_MEM;
    }

    ir_rx_is_initialized = true;
    err = rmt_receive(ir_rx_channel, ir_rx_symbols, ir_rx_symbol_buf_num * sizeof(rmt_symbol_word_t), &ir_rx_receive_config);
    if (err != ESP_OK) {
        deinit_rx_if_needed();
        return err;
    }

    BaseType_t task_created = xTaskCreate(ir_rx_task, "ir_rx_task", 6 * 1024, NULL, 3, &ir_rx_task_handle);
    if (task_created != pdPASS) {
        deinit_rx_if_needed();
        return ESP_ERR_NO_MEM;
    }

    ir_rx_initialized_pin = rx_pin;
    return ESP_OK;
}

static mp_obj_t rmt_ir_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    (void)type;
    mp_arg_check_num(n_args, n_kw, 2, 3, false);

    int rx_pin = mp_obj_get_int(args[0]);
    int tx_pin = (n_args == 3) ? mp_obj_get_int(args[1]) : -1;
    mp_obj_t cb_obj = (n_args == 3) ? args[2] : args[1];

    if (cb_obj != mp_const_none && !mp_obj_is_callable(cb_obj)) {
        mp_raise_ValueError(MP_ERROR_TEXT("callback must be callable or None"));
    }

    esp_err_t err = init_rx_if_needed(rx_pin);
    if (err != ESP_OK) {
        mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("RX init failed: %d"), err);
    }

    err = init_tx_if_needed(tx_pin);
    if (err != ESP_OK) {
        mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("TX init failed: %d"), err);
    }

    rmt_ir_obj_t *self = mp_obj_malloc_with_finaliser(rmt_ir_obj_t, &mp_ir_nec8_type);
    self->in_pin = rx_pin;
    self->tx_pin = tx_pin;
    ir_rx_callback = cb_obj;
    return MP_OBJ_FROM_PTR(self);
}

/**
 * @brief Read the received data - return a tuple (address, command, is_repeat)
*/
static mp_obj_t ir_rx_read(mp_obj_t self_in) {
    if (!ir_data_ready) {
        return mp_const_none;
    }
    ir_data_ready = false;

    mp_obj_t items[3] = {
        mp_obj_new_int(ir_nec_address),
        mp_obj_new_int(ir_nec_command),
        mp_obj_new_bool(ir_is_repeat),
    };
    return mp_obj_new_tuple(3, items);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ir_rx_read_obj, ir_rx_read);

/**
 * @brief Get the address
 */
static mp_obj_t ir_rx_get_address(mp_obj_t self_in) {
    return mp_obj_new_int(ir_nec_address);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ir_rx_get_address_obj, ir_rx_get_address);

/**
 * @brief Get the command
 */
static mp_obj_t ir_rx_get_command(mp_obj_t self_in) {
    return mp_obj_new_int(ir_nec_command);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ir_rx_get_command_obj, ir_rx_get_command);

/**
 * @brief Check whether the received data is a repeat code
 */
static mp_obj_t ir_rx_is_repeat_code(mp_obj_t self_in) {
    return mp_obj_new_bool(ir_is_repeat);
}
static MP_DEFINE_CONST_FUN_OBJ_1(ir_rx_is_repeat_code_obj, ir_rx_is_repeat_code);

/**
 * @brief Send a NEC frame (address, command)
 */
static mp_obj_t ir_tx_send(mp_obj_t self_in, mp_obj_t address_in, mp_obj_t command_in) {
    rmt_ir_obj_t *self = MP_OBJ_TO_PTR(self_in);

    if (self->tx_pin < 0 || !ir_tx_is_initialized || ir_tx_channel == NULL || ir_tx_encoder == NULL) {
        mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("TX not initialized"));
    }

    uint16_t address = (uint16_t)mp_obj_get_int(address_in);
    uint16_t command = (uint16_t)mp_obj_get_int(command_in);

    rmt_symbol_word_t items[35];  // 34 items needed, keep one extra for safety
    int item_num = nec_build_frame(address, command, items);

    rmt_transmit_config_t tx_cfg = {
        .loop_count = 0,
    };

    esp_err_t err = rmt_transmit(ir_tx_channel, ir_tx_encoder, items,
        item_num * sizeof(rmt_symbol_word_t), &tx_cfg);
    if (err != ESP_OK) {
        mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("rmt_transmit failed: %d"), err);
    }

    err = rmt_tx_wait_all_done(ir_tx_channel, -1);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "rmt_tx_wait_all_done failed: err=%d", err);
        mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("rmt_tx_wait_all_done failed: %d"), err);
    }

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_3(ir_tx_send_obj, ir_tx_send);


// Type definition
static const mp_rom_map_elem_t ir_rx_locals_dict_table[] = {
    // RX methods
    {MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&ir_rx_read_obj)},
    {MP_ROM_QSTR(MP_QSTR_get_address), MP_ROM_PTR(&ir_rx_get_address_obj)},
    {MP_ROM_QSTR(MP_QSTR_get_command), MP_ROM_PTR(&ir_rx_get_command_obj)},
    {MP_ROM_QSTR(MP_QSTR_is_repeat), MP_ROM_PTR(&ir_rx_is_repeat_code_obj)},
    // TX methods
    {MP_ROM_QSTR(MP_QSTR_send), MP_ROM_PTR(&ir_tx_send_obj)},
};
MP_DEFINE_CONST_DICT(ir_rx_locals_dict, ir_rx_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(mp_ir_nec8_type,
    MP_QSTR_NEC_8,
    MP_TYPE_FLAG_NONE,
    make_new,
    rmt_ir_make_new,
    locals_dict,
    &ir_rx_locals_dict);

// Module definition
static const mp_rom_map_elem_t rmt_ir_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_rmt_ir)},
    {MP_ROM_QSTR(MP_QSTR_NEC_8), MP_ROM_PTR(&mp_ir_nec8_type)},
    {MP_ROM_QSTR(MP_QSTR_NEC), MP_ROM_PTR(&mp_ir_nec8_type)},  // Compatibility name
};
static MP_DEFINE_CONST_DICT(rmt_ir_globals, rmt_ir_globals_table);

const mp_obj_module_t module_rmt_ir = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&rmt_ir_globals,
};

MP_REGISTER_MODULE(MP_QSTR_rmt_ir, module_rmt_ir);

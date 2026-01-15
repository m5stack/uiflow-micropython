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
#include "driver/rmt.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/ringbuf.h"
#include "esp_log.h"

static const char *TAG = "rmt_ir";

// NEC timing spec (in microseconds)
#define NEC_LEADING_CODE_DURATION_0  9000
#define NEC_LEADING_CODE_DURATION_1  4500
#define NEC_PAYLOAD_ZERO_DURATION_0  560
#define NEC_PAYLOAD_ZERO_DURATION_1  560
#define NEC_PAYLOAD_ONE_DURATION_0   560
#define NEC_PAYLOAD_ONE_DURATION_1   1690
#define NEC_REPEAT_CODE_DURATION_0   9000
#define NEC_REPEAT_CODE_DURATION_1   2250

#define IR_NEC_DECODE_MARGIN         500    // Tolerance for parsing RMT symbols (wide for noisy signals)

#define RMT_CLK_DIV                  80     // 80MHz / 80 = 1MHz, 1 tick = 1us
#define RMT_IDLE_THRESHOLD           12000  // 12ms idle threshold



// class: rmt_ir.NEC_8
typedef struct _rmt_ir_obj_t {
    mp_obj_base_t base;
    int in_pin;
    int tx_pin;
    rmt_channel_t rx_channel;
    rmt_channel_t tx_channel;
} rmt_ir_obj_t;

extern const mp_obj_type_t mp_ir_nec8_type;

// RX global state
static mp_obj_t ir_rx_callback = mp_const_none;
static RingbufHandle_t ir_rx_rb = NULL;
static TaskHandle_t ir_rx_task_handle = NULL;
static bool ir_rx_is_initialized = false;
static rmt_channel_t ir_rx_channel = RMT_CHANNEL_4;   // Default RX channel
static int ir_rx_initialized_pin = -1;
static uint16_t ir_nec_address = 0;
static uint16_t ir_nec_command = 0;
static bool ir_is_repeat = false;
static bool ir_data_ready = false;

// TX global state
static bool ir_tx_is_initialized = false;
static rmt_channel_t ir_tx_channel = RMT_CHANNEL_3;  // Default TX channel
static int ir_tx_initialized_pin = -1;


// ==============================================================================
// TX NEC Encoder
// ==============================================================================
static inline void nec_fill_item(rmt_item32_t *item, uint32_t high_us, uint32_t low_us) {
    item->duration0 = high_us;
    item->level0 = 1;
    item->duration1 = low_us;
    item->level1 = 0;
}

static int nec_build_frame(uint16_t address, uint16_t command, rmt_item32_t *items) {
    int idx = 0;

    // Leading pulse
    nec_fill_item(&items[idx++], NEC_LEADING_CODE_DURATION_0, NEC_LEADING_CODE_DURATION_1);

    // 32 data bits, LSB first (address + command)
    uint32_t data = ((uint32_t)command << 16) | address;
    for (int i = 0; i < 32; i++) {
        if (data & 0x1) {
            nec_fill_item(&items[idx++], NEC_PAYLOAD_ONE_DURATION_0, NEC_PAYLOAD_ONE_DURATION_1);
        } else {
            nec_fill_item(&items[idx++], NEC_PAYLOAD_ZERO_DURATION_0, NEC_PAYLOAD_ZERO_DURATION_1);
        }
        data >>= 1;
    }

    // Stop bit
    nec_fill_item(&items[idx++], NEC_PAYLOAD_ZERO_DURATION_0, 0);

    return idx;  // item count
}

// ==============================================================================
// RX NEC Decoder
// ==============================================================================
/**
  * @brief Check whether a duration is within expected range
  */
static inline bool nec_check_in_range(uint32_t signal_duration, uint32_t spec_duration) {
    return (signal_duration < (spec_duration + IR_NEC_DECODE_MARGIN)) &&
           (signal_duration > (spec_duration - IR_NEC_DECODE_MARGIN));
}

/**
  * @brief Check whether a RMT symbol represents NEC logic zero
  */
static bool nec_parse_logic0(rmt_item32_t *item) {
    return nec_check_in_range(item->duration0, NEC_PAYLOAD_ZERO_DURATION_0) &&
           nec_check_in_range(item->duration1, NEC_PAYLOAD_ZERO_DURATION_1);
}

/**
  * @brief Check whether a RMT symbol represents NEC logic one
  */
static bool nec_parse_logic1(rmt_item32_t *item) {
    return nec_check_in_range(item->duration0, NEC_PAYLOAD_ONE_DURATION_0) &&
           nec_check_in_range(item->duration1, NEC_PAYLOAD_ONE_DURATION_1);
}

/**
  * @brief Decode RMT symbols into NEC address and command
  */
static bool nec_parse_frame(rmt_item32_t *items) {
    rmt_item32_t *cur = items;
    uint16_t address = 0;
    uint16_t command = 0;

    // Check leading code
    bool valid_leading_code = nec_check_in_range(cur->duration0, NEC_LEADING_CODE_DURATION_0) &&
        nec_check_in_range(cur->duration1, NEC_LEADING_CODE_DURATION_1);
    if (!valid_leading_code) {
        return false;
    }
    cur++;

    // Parse address (16 bits)
    for (int i = 0; i < 16; i++) {
        if (nec_parse_logic1(cur)) {
            address |= 1 << i;
        } else if (nec_parse_logic0(cur)) {
            address &= ~(1 << i);
        } else {
            return false;
        }
        cur++;
    }

    // Parse command (16 bits)
    for (int i = 0; i < 16; i++) {
        if (nec_parse_logic1(cur)) {
            command |= 1 << i;
        } else if (nec_parse_logic0(cur)) {
            command &= ~(1 << i);
        } else {
            return false;
        }
        cur++;
    }

    ir_nec_address = address;
    ir_nec_command = command;
    return true;
}

/**
  * @brief Check whether the RMT symbols represent NEC repeat code
  */
static bool nec_parse_frame_repeat(rmt_item32_t *item) {
    return nec_check_in_range(item->duration0, NEC_REPEAT_CODE_DURATION_0) &&
           nec_check_in_range(item->duration1, NEC_REPEAT_CODE_DURATION_1);
}

/**
  * @brief Process received NEC frame
  */
static void process_nec_frame(rmt_item32_t *items, size_t symbol_num) {
    ir_is_repeat = false;
    ir_data_ready = false;

    switch (symbol_num) {
        case 34:  // NEC normal frame
            if (nec_parse_frame(items)) {
                ir_data_ready = true;
            }
            break;
        case 2:  // NEC repeat frame
            if (nec_parse_frame_repeat(items)) {
                ir_is_repeat = true;
                ir_data_ready = true;
            }
            break;
    }

    // Schedule callback if data is ready
    if (ir_data_ready && ir_rx_callback != mp_const_none) {
        mp_sched_schedule(ir_rx_callback, mp_const_none);
    }
}

/**
  * @brief IR RX task - receives data from RMT ringbuffer
  */
static void ir_rx_task(void *param) {
    while (ir_rx_rb) {
        size_t rx_size = 0;
        rmt_item32_t *items = (rmt_item32_t *)xRingbufferReceive(ir_rx_rb, &rx_size, portMAX_DELAY);
        if (items) {
            size_t symbol_num = rx_size / sizeof(rmt_item32_t);
            process_nec_frame(items, symbol_num);
            vRingbufferReturnItem(ir_rx_rb, (void *)items);
        }
    }
    vTaskDelete(NULL);
}



/**
 * @brief Initialize TX if needed (TX is a global singleton)
 * @param tx_pin: TX pin number
 * @param tx_channel: pointer to store the TX channel
 * @return ESP_OK on success, error code on failure
 */
static esp_err_t init_tx_if_needed(int tx_pin, rmt_channel_t *tx_channel) {
    if (tx_pin < 0) {
        *tx_channel = RMT_CHANNEL_MAX;
        return ESP_OK;
    }

    if (ir_tx_is_initialized) {
        if (tx_pin != ir_tx_initialized_pin) {
            // Pin changed - need to reinitialize
            rmt_driver_uninstall(ir_tx_channel);
            ir_tx_is_initialized = false;
        } else {
            // Same pin - reuse existing
            *tx_channel = ir_tx_channel;
            return ESP_OK;
        }
    }

    // Initialize TX
    *tx_channel = ir_tx_channel;
    ir_tx_initialized_pin = tx_pin;

    rmt_config_t rmt_tx_config = {
        .rmt_mode = RMT_MODE_TX,
        .channel = *tx_channel,
        .gpio_num = tx_pin,
        .clk_div = RMT_CLK_DIV,
        .mem_block_num = 1,
        .tx_config = {
            .loop_en = false,
            .carrier_en = true,
            .carrier_freq_hz = 38000,
            .carrier_duty_percent = 33,
            .carrier_level = 1,
            .idle_output_en = true,
            .idle_level = 0,
        },
    };
    esp_err_t err = rmt_config(&rmt_tx_config);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "rmt_config TX failed: err=%d, pin=%d, channel=%d", err, tx_pin, *tx_channel);
        return err;
    }

    err = rmt_driver_install(*tx_channel, 0, 0);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "rmt_driver_install TX failed: err=%d, channel=%d", err, *tx_channel);
        return err;
    }

    ir_tx_is_initialized = true;

    return ESP_OK;
}

/**
 * @brief Create a new NEC_8 instance, support 2 or 3 arguments
 * @param args[0]: the RX pin
 * @param args[1]: the TX pin (if 3 args) or callback (if 2 args)
 * @param args[2]: the callback function (if 3 args)
 *
 * Note: RX and TX are global singletons - only one RX and one TX can be initialized
 */
static mp_obj_t rmt_ir_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 2, 3, false);

    // Parse arguments
    int rx_pin = mp_obj_get_int(args[0]);
    int tx_pin = (n_args == 3) ? mp_obj_get_int(args[1]) : -1;
    mp_obj_t cb_obj = (n_args == 3) ? args[2] : args[1];

    // Validate callback
    if (cb_obj != mp_const_none && !mp_obj_is_callable(cb_obj)) {
        mp_raise_ValueError(MP_ERROR_TEXT("callback must be callable or None"));
    }

    // Check RX initialization status
    if (ir_rx_is_initialized) {
        // RX already initialized
        if (rx_pin != ir_rx_initialized_pin) {
            // Pin changed - need to reinitialize
            // Stop and uninstall old RX
            rmt_rx_stop(ir_rx_channel);
            rmt_driver_uninstall(ir_rx_channel);
            if (ir_rx_task_handle) {
                vTaskDelete(ir_rx_task_handle);
                ir_rx_task_handle = NULL;
            }
            ir_rx_rb = NULL;
            ir_rx_is_initialized = false;
        }
    }

    // Create instance
    rmt_ir_obj_t *self = mp_obj_malloc_with_finaliser(rmt_ir_obj_t, &mp_ir_nec8_type);
    self->in_pin = rx_pin;
    self->tx_pin = tx_pin;
    self->rx_channel = ir_rx_channel;

    // Initialize RX (only when a valid pin is provided and not already initialized)
    if (rx_pin >= 0 && !ir_rx_is_initialized) {
        ir_rx_initialized_pin = rx_pin;

        rmt_config_t rmt_rx_config = {
            .rmt_mode = RMT_MODE_RX,
            .channel = self->rx_channel,
            .gpio_num = self->in_pin,
            .clk_div = RMT_CLK_DIV,
            .mem_block_num = 1,
            .rx_config = {
                .idle_threshold = RMT_IDLE_THRESHOLD,
                .filter_ticks_thresh = 100,
                .filter_en = true,
            },
        };

        esp_err_t err = rmt_config(&rmt_rx_config);
        if (err != ESP_OK) {
            ESP_LOGE(TAG, "rmt_config failed for RX: err=0x%x (%d), channel=%d, gpio=%d", err, err, self->rx_channel, self->in_pin);
            mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("rmt_config failed: %d"), err);
        }

        err = rmt_driver_install(self->rx_channel, 1000, 0);
        if (err != ESP_OK) {
            mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("rmt_driver_install failed: %d"), err);
        }

        // Enable GPIO pull-up for RX pin
        gpio_set_pull_mode(rx_pin, GPIO_PULLUP_ONLY);

        // Get RMT RX ringbuffer handle
        err = rmt_get_ringbuf_handle(self->rx_channel, &ir_rx_rb);
        if (err != ESP_OK || ir_rx_rb == NULL) {
            mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("rmt_get_ringbuf_handle failed: %d"), err);
        }

        // Start RX
        err = rmt_rx_start(self->rx_channel, true);
        if (err != ESP_OK) {
            mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("rmt_rx_start failed: %d"), err);
        }

        // Create RX task
        BaseType_t task_created = xTaskCreate(ir_rx_task, "ir_rx_task", 8192, NULL, 3, &ir_rx_task_handle);
        if (task_created != pdPASS) {
            mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("Failed to create RX task"));
        }

        ir_rx_is_initialized = true;
    }
    ir_rx_callback = cb_obj;

    esp_err_t err = init_tx_if_needed(tx_pin, &self->tx_channel);
    if (err == ESP_ERR_INVALID_STATE) {
        mp_raise_msg_varg(&mp_type_RuntimeError,
            MP_ERROR_TEXT("IR TX already initialized on pin %d, cannot use pin %d"),
            ir_tx_initialized_pin, tx_pin);
    } else if (err != ESP_OK) {
        mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("TX initialization failed: %d"), err);
    }

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

    if (self->tx_pin < 0 || self->tx_channel >= RMT_CHANNEL_MAX || !ir_tx_is_initialized) {
        mp_raise_msg(&mp_type_RuntimeError, MP_ERROR_TEXT("TX not initialized"));
    }

    uint16_t address = (uint16_t)mp_obj_get_int(address_in);
    uint16_t command = (uint16_t)mp_obj_get_int(command_in);

    rmt_item32_t items[35];  // 34 items needed, keep one extra for safety
    int item_num = nec_build_frame(address, command, items);

    esp_err_t err = rmt_write_items(self->tx_channel, items, item_num, true);
    if (err != ESP_OK) {
        mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("rmt_write_items failed: %d"), err);
    }

    err = rmt_wait_tx_done(self->tx_channel, portMAX_DELAY);
    if (err != ESP_OK) {
        ESP_LOGE(TAG, "rmt_wait_tx_done failed: err=%d, channel=%d", err, self->tx_channel);
        mp_raise_msg_varg(&mp_type_RuntimeError, MP_ERROR_TEXT("rmt_wait_tx_done failed: %d"), err);
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

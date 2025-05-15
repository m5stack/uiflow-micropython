/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include <string.h>
#include <stdio.h>
#include <stdbool.h>
#include "py/nlr.h"
#include "py/obj.h"
#include "py/objlist.h"
#include "py/objstr.h"
#include "py/objtuple.h"
#include "py/objtype.h"
#include "py/runtime.h"
#include "py/mphal.h"
#include "driver/rmt.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/queue.h"
#include "esp_check.h"

static const char *TAG = "py_rf433";

#define RMT_TX_CHANNEL RMT_CHANNEL_0
#define RMT_RX_CHANNEL RMT_CHANNEL_1

#define RMT_CLK_DIV   80 /*!< RMT counter clock divider */
#define RMT_1US_TICKS (80000000 / RMT_CLK_DIV / 1000000)
#define RMT_1MS_TICKS (RMT_1US_TICKS * 1000)

RingbufHandle_t rb = NULL;

// 自定义协议参数
#define SYNC_HIGH_US 9000
#define SYNC_LOW_US  4500

#define BIT_HIGH_US 500
#define BIT0_LOW_US 500
#define BIT1_LOW_US 1500

#define FRAME_HEADER 0xAA
#define FRAME_TAIL   0xA0

// =================================================================================================
// class: rf433.Tx
typedef struct _tx_obj_t {
    mp_obj_base_t base;
    int out;
} tx_obj_t;

extern const mp_obj_type_t mp_tx_type;

// 编码单个比特
static rmt_item32_t encode_bit(bool bit) {
    rmt_item32_t item;
    if (bit) {
        item.level0 = 1;
        item.duration0 = BIT_HIGH_US;  // 1 高电平持续时间
        item.level1 = 0;
        item.duration1 = BIT1_LOW_US;  // 1 低电平持续时间
    } else {
        item.level0 = 1;
        item.duration0 = BIT_HIGH_US;  // 0 高电平持续时间
        item.level1 = 0;
        item.duration1 = BIT0_LOW_US;  // 0 低电平持续时间
    }

    return item;
}

// 编码一个字节
static void encode_byte(rmt_item32_t *items, int *index, uint8_t byte) {
    for (int bit_idx = 7; bit_idx >= 0; bit_idx--) {
        items[(*index)++] = encode_bit((byte >> bit_idx) & 1);
    }
}

// 发送 RMT 数据
void send_data(const uint8_t *payload, size_t len) {
    // 计算 RMT 数据的最大数量（同步位 + 帧头 + 数据长度 + 数据 + 帧尾，每个字节占 8 个项）
    size_t item_max_count = 1 + (2 + len + 1) * 8;
    rmt_item32_t items[item_max_count];
    int item_idx = 0;

    // 添加同步位
    items[item_idx++] = (rmt_item32_t) {.duration0 = SYNC_HIGH_US, .level0 = 1, .duration1 = SYNC_LOW_US, .level1 = 0};

    // 添加帧头 0xAA
    encode_byte(items, &item_idx, FRAME_HEADER);

    // 数据 payload 长度
    encode_byte(items, &item_idx, len);

    // 添加 payload 数据
    for (size_t i = 0; i < len; i++) {
        encode_byte(items, &item_idx, payload[i]);
    }

    // 添加帧尾 0xA0
    encode_byte(items, &item_idx, FRAME_TAIL);

    // 发送 RMT 数据
    rmt_write_items(RMT_TX_CHANNEL, items, item_idx, true);
    rmt_wait_tx_done(RMT_TX_CHANNEL, portMAX_DELAY);
}

static bool tx_is_initialized;
static mp_obj_t tx_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    tx_obj_t *self = mp_obj_malloc_with_finaliser(tx_obj_t, &mp_tx_type);

    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_out_pin, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL}},
    };
    mp_arg_val_t args_vals[MP_ARRAY_SIZE(allowed_args)];
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    mp_arg_parse_all(n_args, args + 1, &kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args_vals);

    self->out = mp_obj_get_int(args_vals[0].u_obj);
    if (!tx_is_initialized) {  // TODO: deinit() 实现
        tx_is_initialized = true;
        rmt_config_t tx_cfg;
        tx_cfg.rmt_mode = RMT_MODE_TX;
        tx_cfg.channel = RMT_TX_CHANNEL;
        tx_cfg.gpio_num = self->out;
        tx_cfg.mem_block_num = 1;
        tx_cfg.tx_config.loop_en = false;
        tx_cfg.tx_config.carrier_en = false;
        tx_cfg.tx_config.idle_output_en = true;
        tx_cfg.tx_config.idle_level = (rmt_idle_level_t)0;
        tx_cfg.clk_div = 80;                   // RMT_CLK_DIV; // 时钟分频
        ESP_ERROR_CHECK(rmt_config(&tx_cfg));
        ESP_ERROR_CHECK(rmt_driver_install(tx_cfg.channel, 0, 0));
    }

    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t tx_send(size_t n_args, const mp_obj_t *pos_args, mp_map_t *kw_args) {
    const mp_arg_t allowed_args[] = {
        {MP_QSTR_data, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = mp_const_none}},
    };

    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all(n_args - 1, pos_args + 1, kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    mp_buffer_info_t data_buff;
    mp_get_buffer_raise(args[0].u_obj, &data_buff, MP_BUFFER_READ);

    send_data((const uint8_t *)data_buff.buf, data_buff.len);

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_KW(tx_send_obj, 1, tx_send);

static const mp_rom_map_elem_t tx_locals_dict_table[] = {
    // Methods
    {MP_ROM_QSTR(MP_QSTR_send), MP_ROM_PTR(&tx_send_obj)},
};
MP_DEFINE_CONST_DICT(tx_locals_dict, tx_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(mp_tx_type, MP_QSTR_Tx, MP_TYPE_FLAG_NONE, make_new, tx_make_new, locals_dict,
    &tx_locals_dict);

// =================================================================================================
// class: rf433.Rx
typedef struct _rx_obj_t {
    mp_obj_base_t base;
    int in;
} rx_obj_t;

extern const mp_obj_type_t mp_rx_type;

static mp_obj_t rx_callback = mp_const_none;
static uint8_t rx_buffer[256];
static size_t rx_len = 0;
static const size_t RX_MAX_LEN = 64;

static bool decode_bit(rmt_item32_t item) {
    int high_us = item.duration0;
    int low_us = item.duration1;
    // 根据 endode 参数修改
    return high_us > 350 && high_us < 650 && low_us > 1350 && low_us < 1650;
}

static void decode_data(rmt_item32_t *items, size_t num_items) {
    uint8_t byte = 0;
    int bit_count = 0;
    int rx_state = 0;
    size_t data_len = 0;
    size_t buf_index = 0;

    for (int i = 0; i < num_items; i++) {
        bool bit = decode_bit(items[i]);
        byte = (byte << 1) | bit;
        bit_count++;
        if (bit_count == 8) {
            if (rx_state == 0 && byte == FRAME_HEADER) {
                rx_state++;
            } else if (rx_state == 1) {
                rx_state++;
                data_len = byte;
            } else if (rx_state == 2) {
                if (buf_index < RX_MAX_LEN) {
                    rx_buffer[buf_index++] = byte;
                    if (buf_index == data_len + 1) {
                        break;
                    }
                }
            } else {
                rx_state = 0;
                buf_index = 0;
            }
            bit_count = 0;
            byte = 0;
        }
    }

    if (rx_buffer[data_len] == FRAME_TAIL) {
        rx_len = data_len;
        if (rx_callback != mp_const_none && rx_len > 0) {
            if (!mp_sched_schedule(rx_callback, mp_const_none)) {
                mp_printf(&mp_plat_print, "Task queue full, cannot schedule callback!\n");
            }
        }
    }
}

void app_rf433r_rx_decode(void *param) {
    RingbufHandle_t rb = NULL;
    rmt_get_ringbuf_handle(RMT_RX_CHANNEL, &rb);
    rmt_rx_start(RMT_RX_CHANNEL, true);

    while (rb) {
        size_t rx_size = 0;
        rmt_item32_t *items = (rmt_item32_t *)xRingbufferReceive(rb, &rx_size, portMAX_DELAY);
        if (items) {
            size_t num_items = rx_size / sizeof(rmt_item32_t);
            decode_data(items, num_items);
            vRingbufferReturnItem(rb, (void *)items);
        }
    }
}

static bool rx_is_initialized;
static mp_obj_t rx_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    rx_obj_t *self = mp_obj_malloc_with_finaliser(rx_obj_t, &mp_rx_type);

    static const mp_arg_t allowed_args[] = {
        {MP_QSTR_in_pin, MP_ARG_KW_ONLY | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL}},
    };
    mp_arg_val_t args_vals[MP_ARRAY_SIZE(allowed_args)];
    mp_map_t kw_args;
    mp_map_init_fixed_table(&kw_args, n_kw, args + n_args);
    mp_arg_parse_all(n_args, args + 1, &kw_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args_vals);

    self->in = mp_obj_get_int(args_vals[0].u_obj);
    if (!rx_is_initialized) {  // TODO: deinit() 实现
        rx_is_initialized = true;
        rmt_config_t rxconfig;
        rxconfig.rmt_mode = RMT_MODE_RX;
        rxconfig.channel = RMT_RX_CHANNEL;
        rxconfig.gpio_num = self->in;
        rxconfig.mem_block_num = 6;
        rxconfig.clk_div = RMT_CLK_DIV;
        rxconfig.rx_config.filter_en = true;
        rxconfig.rx_config.filter_ticks_thresh = 100 * RMT_1US_TICKS;
        rxconfig.rx_config.idle_threshold = 3 * RMT_1MS_TICKS;
        ESP_ERROR_CHECK(rmt_config(&rxconfig));
        ESP_ERROR_CHECK(rmt_driver_install(rxconfig.channel, 4096, 0));

        xTaskCreate(app_rf433r_rx_decode, "app_rf433r_rx_decode", 4096, NULL, 3, NULL);
    }

    return MP_OBJ_FROM_PTR(self);
}

static mp_obj_t rx_start_recv(mp_obj_t self_in) {
    if (rb == NULL) {
        rmt_get_ringbuf_handle(RMT_RX_CHANNEL, &rb);
        rmt_rx_start(RMT_RX_CHANNEL, true);
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(rx_start_recv_obj, rx_start_recv);

static mp_obj_t rx_stop_recv(mp_obj_t self_in) {
    rb = NULL;
    rmt_rx_stop(RMT_RX_CHANNEL);
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(rx_stop_recv_obj, rx_stop_recv);

static mp_obj_t rx_set_recv_callback(mp_obj_t self_in, mp_obj_t callback) {
    if (mp_obj_is_callable(callback)) {
        rx_callback = callback;
    } else {
        mp_raise_ValueError(MP_ERROR_TEXT("callback must be callable or None"));
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(rx_set_recv_callback_obj, rx_set_recv_callback);

static mp_obj_t rx_read(mp_obj_t self_in) {
    if (rx_len == 0) {
        return mp_const_none;
    }
    mp_obj_t data = mp_obj_new_bytes(rx_buffer, rx_len);
    rx_len = 0;
    return data;
}
static MP_DEFINE_CONST_FUN_OBJ_1(rx_read_obj, rx_read);

static const mp_rom_map_elem_t rx_locals_dict_table[] = {
    // Methods
    {MP_ROM_QSTR(MP_QSTR_start_recv), MP_ROM_PTR(&rx_start_recv_obj)},
    {MP_ROM_QSTR(MP_QSTR_stop_recv), MP_ROM_PTR(&rx_stop_recv_obj)},
    {MP_ROM_QSTR(MP_QSTR_read), MP_ROM_PTR(&rx_read_obj)},
    {MP_ROM_QSTR(MP_QSTR_set_recv_callback), MP_ROM_PTR(&rx_set_recv_callback_obj)},
};
MP_DEFINE_CONST_DICT(rx_locals_dict, rx_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(mp_rx_type, MP_QSTR_Rx, MP_TYPE_FLAG_NONE, make_new, rx_make_new, locals_dict,
    &rx_locals_dict);

// =================================================================================================
// module: rf433
static const mp_rom_map_elem_t rf433_globals_table[] = {
    {MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_rf433)},
    {MP_ROM_QSTR(MP_QSTR_Tx), MP_ROM_PTR(&mp_tx_type)},
    {MP_ROM_QSTR(MP_QSTR_Rx), MP_ROM_PTR(&mp_rx_type)},
};
static MP_DEFINE_CONST_DICT(rf433_globals, rf433_globals_table);

const mp_obj_module_t module_rf433 = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&rf433_globals,
};

MP_REGISTER_MODULE(MP_QSTR_rf433, module_rf433);

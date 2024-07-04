/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2019 Damien P. George
 * Copyright (c) 2024 M5Stack Technology CO LTD
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "py/runtime.h"
#include "py/mphal.h"
#include "py/mperrno.h"
#include "extmod/modmachine.h"
#include "driver/i2c.h"
#include "freertos/FreeRTOS.h"

#if ESP_IDF_VERSION >= ESP_IDF_VERSION_VAL(4, 4, 0)
#include "hal/i2c_ll.h"
#else
#include "soc/i2c_reg.h"
#define I2C_LL_MAX_TIMEOUT I2C_TIME_OUT_REG_V
#endif

#ifndef MICROPY_HW_I2C0_SCL
#define MICROPY_HW_I2C0_SCL (GPIO_NUM_18)
#define MICROPY_HW_I2C0_SDA (GPIO_NUM_19)
#endif

#ifndef MICROPY_HW_I2C1_SCL
#if CONFIG_IDF_TARGET_ESP32
#define MICROPY_HW_I2C1_SCL (GPIO_NUM_25)
#define MICROPY_HW_I2C1_SDA (GPIO_NUM_26)
#else
#define MICROPY_HW_I2C1_SCL (GPIO_NUM_9)
#define MICROPY_HW_I2C1_SDA (GPIO_NUM_8)
#endif
#endif

#if CONFIG_IDF_TARGET_ESP32C3 || CONFIG_IDF_TARGET_ESP32S3
#define I2C_SCLK_FREQ XTAL_CLK_FREQ
#elif CONFIG_IDF_TARGET_ESP32 || CONFIG_IDF_TARGET_ESP32S2
#define I2C_SCLK_FREQ I2C_APB_CLK_FREQ
#else
#error "unsupported I2C for ESP32 SoC variant"
#endif

#define I2C_DEFAULT_TIMEOUT_US (50000) // 50ms
#define DEVICE_NUMBER 12

typedef struct _i2c_port_obj_t {
    i2c_port_t port : 8;
    gpio_num_t scl : 8;
    gpio_num_t sda : 8;
    uint32_t freq;
} i2c_port_obj_t;

typedef struct _machine_hw_i2c_obj_t {
    mp_obj_base_t base;
    uint8_t pos;
    i2c_port_t port;
} machine_hw_i2c_obj_t;

STATIC machine_hw_i2c_obj_t machine_hw_i2c_obj[I2C_NUM_MAX];
STATIC const mp_obj_type_t machine_hw_i2c_type;
STATIC i2c_port_obj_t *i2c_device[DEVICE_NUMBER];
STATIC SemaphoreHandle_t i2c_mutex[I2C_NUM_MAX];
STATIC uint8_t i2c_port_used[2] = { DEVICE_NUMBER, DEVICE_NUMBER };

void machine_i2c_deinit_all(void) {
    if (i2c_port_used[0] != DEVICE_NUMBER) {
        i2c_driver_delete(I2C_NUM_0);
        i2c_port_used[0] = DEVICE_NUMBER;
    }

    if (i2c_port_used[1] != DEVICE_NUMBER) {
        i2c_driver_delete(I2C_NUM_1);
        i2c_port_used[1] = DEVICE_NUMBER;
    }

    for (uint8_t i = 0; i < DEVICE_NUMBER; i++) {
        if (i2c_device[i] != NULL) {
            free(i2c_device[i]);
            i2c_device[i] = NULL;
        }
    }
}

STATIC uint8_t malloc_bus(gpio_num_t scl, gpio_num_t sda, uint32_t freq, uint8_t port) {
    if (i2c_mutex[0] == NULL) {
        i2c_mutex[0] = xSemaphoreCreateMutex();
    }
    if (i2c_mutex[1] == NULL) {
        i2c_mutex[1] = xSemaphoreCreateMutex();
    }

    uint8_t pos = 0;
    for (pos = 0; pos < DEVICE_NUMBER; pos++) {
        if (i2c_device[pos] == NULL) {
            continue;
        }
        if (i2c_device[pos]->scl == scl && i2c_device[pos]->sda == sda) {
            if (i2c_device[pos]->freq == freq) {
                // printf("found existing i2c bus, pos = %d, port = %d\n", pos, i2c_device[pos]->port);
                return pos;
            } else {
                // printf("found existing i2c bus with different freq, pos = %d, port = %d\n", pos, i2c_device[pos]->port);
                for (uint8_t i = 0; i < DEVICE_NUMBER; i++) {
                    if (i2c_device[i] != NULL) {
                        continue;
                    }
                    i2c_device[i] = (i2c_port_obj_t *)malloc(sizeof(i2c_port_obj_t));
                    i2c_device[i]->sda = sda;
                    i2c_device[i]->scl = scl;
                    i2c_device[i]->freq = freq;
                    i2c_device[i]->port = i2c_device[pos]->port;
                    // printf("create new i2c bus, pos = %d, port = %d\n", i, i2c_device[i]->port);
                    return i;
                }
            }
        }
    }

    for (pos = 0; pos < DEVICE_NUMBER; pos++) {
        if (i2c_device[pos] == NULL) {
            i2c_device[pos] = (i2c_port_obj_t *)malloc(sizeof(i2c_port_obj_t));
            i2c_device[pos]->sda = sda;
            i2c_device[pos]->scl = scl;
            i2c_device[pos]->freq = freq;
            i2c_device[pos]->port = port;
            // printf("create new i2c bus, pos = %d, port = %d\n", pos, i2c_device[pos]->port);
            // if(pos == 0) {
            //     i2c_device[pos]->port = I2C_NUM_0;
            // } else {
            //     i2c_device[pos]->port = I2C_NUM_1;
            // }
            return pos;
        }
    }

    return DEVICE_NUMBER;
}

void apply_bus(uint8_t pos) {
    if (pos >= DEVICE_NUMBER) {
        return;
    }
    if (i2c_device[pos] == NULL) {
        mp_raise_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("i2c bus apply failed"));
    }

    i2c_port_obj_t *device = i2c_device[pos];

    if (i2c_port_used[device->port] == pos) {
        MP_THREAD_GIL_EXIT();
        xSemaphoreTake(i2c_mutex[device->port], portMAX_DELAY);
        MP_THREAD_GIL_ENTER();
        return;
    }

    if (i2c_port_used[device->port] != DEVICE_NUMBER) {
        i2c_driver_delete(device->port);
    }

    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = device->sda,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_io_num = device->scl,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = device->freq,
    };

    i2c_param_config(device->port, &conf);
    int timeout = I2C_SCLK_FREQ / 1000000 * I2C_DEFAULT_TIMEOUT_US;
    i2c_set_timeout(device->port, (timeout > I2C_LL_MAX_TIMEOUT) ? I2C_LL_MAX_TIMEOUT : timeout);
    i2c_driver_install(device->port, I2C_MODE_MASTER, 0, 0, 0);

    MP_THREAD_GIL_EXIT();
    xSemaphoreTake(i2c_mutex[device->port], portMAX_DELAY);
    MP_THREAD_GIL_ENTER();

    i2c_port_used[device->port] = pos;

    return;
}

void free_bus(uint8_t pos) {
    xSemaphoreGive(i2c_mutex[i2c_device[pos]->port]);
}


int machine_hw_i2c_transfer(mp_obj_base_t *self_in, uint16_t addr, size_t n, mp_machine_i2c_buf_t *bufs, unsigned int flags) {
    machine_hw_i2c_obj_t *self = MP_OBJ_TO_PTR(self_in);
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();

    int data_len = 0;

    if (flags & MP_MACHINE_I2C_FLAG_WRITE1) {
        i2c_master_start(cmd);
        i2c_master_write_byte(cmd, addr << 1, true);
        i2c_master_write(cmd, bufs->buf, bufs->len, true);
        data_len += bufs->len;
        --n;
        ++bufs;
    }

    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, addr << 1 | (flags & MP_MACHINE_I2C_FLAG_READ), true);

    // printf("I2C transfer: addr=%02X, n=%u", addr, n);
    // if (flags & MP_MACHINE_I2C_FLAG_READ) {
    //     printf(", read");
    // }
    // else if (flags & MP_MACHINE_I2C_FLAG_STOP) {
    //     printf(", stop");
    // }
    // else {
    //     printf(", write");
    // }
    // printf("\n");

    for (; n--; ++bufs) {
        if (flags & MP_MACHINE_I2C_FLAG_READ) {
            i2c_master_read(cmd, bufs->buf, bufs->len, n == 0 ? I2C_MASTER_LAST_NACK : I2C_MASTER_ACK);
        } else {
            if (bufs->len != 0) {
                i2c_master_write(cmd, bufs->buf, bufs->len, true);
            }
        }
        data_len += bufs->len;
    }

    if (flags & MP_MACHINE_I2C_FLAG_STOP) {
        i2c_master_stop(cmd);
    }
    // TODO proper timeout
    apply_bus(self->pos);

    esp_err_t err = i2c_master_cmd_begin(i2c_device[self->pos]->port, cmd, 100 * (1 + data_len) / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);

    xSemaphoreGive(i2c_mutex[i2c_device[self->pos]->port]);

    if (err == ESP_FAIL) {
        return -MP_ENODEV;
    } else if (err == ESP_ERR_TIMEOUT) {
        return -MP_ETIMEDOUT;
    } else if (err != ESP_OK) {
        return -abs(err);
    }

    return data_len;
}

/******************************************************************************/
// MicroPython bindings for machine API

STATIC void machine_hw_i2c_print(const mp_print_t *print, mp_obj_t self_in, mp_print_kind_t kind) {
    machine_hw_i2c_obj_t *self = MP_OBJ_TO_PTR(self_in);
    i2c_port_obj_t *device = i2c_device[self->pos];
    mp_printf(print, "I2C device: %u\r\n", self->pos);
    mp_printf(print, "I2C(%u, scl=%u, sda=%u, freq=%u)", device->port, device->scl, device->sda, device->freq);
}

mp_obj_t machine_hw_i2c_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *all_args) {
    // MP_MACHINE_I2C_CHECK_FOR_LEGACY_SOFTI2C_CONSTRUCTION(n_args, n_kw, all_args);

    // Parse args
    enum { ARG_id, ARG_scl, ARG_sda, ARG_freq, ARG_timeout };
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_id, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_scl, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_sda, MP_ARG_REQUIRED | MP_ARG_OBJ, {.u_obj = MP_OBJ_NULL} },
        { MP_QSTR_freq, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = 400000} },
        { MP_QSTR_timeout, MP_ARG_KW_ONLY | MP_ARG_INT, {.u_int = I2C_DEFAULT_TIMEOUT_US} },
    };
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    // Get I2C bus
    mp_int_t i2c_id = mp_obj_get_int(args[ARG_id].u_obj);
    if (!(I2C_NUM_0 <= i2c_id && i2c_id < I2C_NUM_MAX)) {
        mp_raise_msg_varg(&mp_type_ValueError, MP_ERROR_TEXT("I2C(%d) doesn't exist"), i2c_id);
    }

    // Get static peripheral object
    // Get static peripheral object
    machine_hw_i2c_obj_t *self = (machine_hw_i2c_obj_t *)&machine_hw_i2c_obj[i2c_id];

    bool first_init = false;
    if (self->base.type == NULL) {
        // Created for the first time, set default pins
        self->base.type = &machine_i2c_type;
        self->port = i2c_id;
        first_init = true;
    }

    // if (!first_init) {
    //     printf("Delete I2C device: %u\r\n", self->port);
    //     i2c_driver_delete(self->port);
    //     i2c_port_used[self->port] = DEVICE_NUMBER;
    //     if (i2c_device[self->pos] != NULL) {
    //         free(i2c_device[self->pos]);
    //         i2c_device[self->pos] = NULL;
    //     }
    // }

    int scl = mp_hal_get_pin_obj(args[ARG_scl].u_obj);
    int sda = mp_hal_get_pin_obj(args[ARG_sda].u_obj);
    self->pos = malloc_bus(scl, sda, args[ARG_freq].u_int, i2c_id);
    self->port = i2c_device[self->pos]->port;
    // printf("i2c_id: %d, scl: %d, sda: %d, freq: %d\n", self->port , scl, sda, args[ARG_freq].u_int);

    return MP_OBJ_FROM_PTR(self);
}

STATIC const mp_machine_i2c_p_t machine_hw_i2c_p = {
    .transfer_supports_write1 = true,
    .transfer = machine_hw_i2c_transfer,
};

MP_DEFINE_CONST_OBJ_TYPE(
    machine_i2c_type,
    MP_QSTR_I2C,
    MP_TYPE_FLAG_NONE,
    make_new, machine_hw_i2c_make_new,
    print, machine_hw_i2c_print,
    protocol, &machine_hw_i2c_p,
    locals_dict, &mp_machine_i2c_locals_dict
    );

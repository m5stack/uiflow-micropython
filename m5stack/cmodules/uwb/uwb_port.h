/*
 * SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

#include <stdbool.h>
#include <stdint.h>

#include "driver/gpio.h"

typedef struct {
    gpio_num_t irq;
    gpio_num_t wakeup;
    gpio_num_t reset;
    gpio_num_t mosi;
    gpio_num_t miso;
    gpio_num_t clock;
    gpio_num_t cs;
} uwb_port_config_t;

int uwb_port_init(const uwb_port_config_t *config);
void uwb_port_deinit(void);
void uwb_port_reset(void);
void uwb_port_wakeup(void);

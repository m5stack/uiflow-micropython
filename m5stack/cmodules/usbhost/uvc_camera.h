// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT
#pragma once
#include "usb/uvc_host.h"

typedef struct {
    uint32_t frames;
    uint32_t dropped;
    uint32_t overflows;
    uint32_t errors;
    esp_err_t last_error;
    bool connected;
    bool streaming;
    uvc_host_stream_format_t format;
} uiflow_uvc_info_t;

esp_err_t uiflow_uvc_init(unsigned width, unsigned height, unsigned fps, size_t frame_size,
    enum uvc_host_stream_format format);
esp_err_t uiflow_uvc_start(unsigned timeout_ms);
esp_err_t uiflow_uvc_stop(void);
esp_err_t uiflow_uvc_deinit(void);
bool uiflow_uvc_active(uint32_t generation);
uint32_t uiflow_uvc_generation(void);
esp_err_t uiflow_uvc_frame_take(uvc_host_frame_t **frame);
esp_err_t uiflow_uvc_frame_release(uvc_host_frame_t *frame);
esp_err_t uiflow_uvc_formats(uvc_host_frame_info_t (*formats)[], size_t *count);
void uiflow_uvc_info(uiflow_uvc_info_t *info);
esp_err_t uiflow_uvc_rgb565(const uvc_host_frame_t *frame, uint8_t *output, size_t size);

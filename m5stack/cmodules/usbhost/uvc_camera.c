// SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
// SPDX-License-Identifier: MIT

#include <stdatomic.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"
#include "esp_heap_caps.h"
#include "esp_log.h"
#include "usbhost_bus.h"
#include "uvc_camera.h"

#define UVC_QUEUED_FRAMES (2)

static bool camera_installed;
static QueueHandle_t camera_frames;
static uvc_host_stream_hdl_t camera_stream;
static uvc_host_stream_format_t camera_format;
static uvc_host_stream_format_t camera_requested_format;
static size_t camera_frame_size;
static uint32_t camera_generation;
static atomic_bool camera_accept_frames;
static atomic_bool camera_disconnected;
static atomic_uint camera_callbacks;
static atomic_uint camera_address;
static atomic_uint camera_received;
static atomic_uint camera_dropped;
static atomic_uint camera_overflows;
static atomic_uint camera_errors;
static atomic_int camera_last_error;

static void camera_driver_event(const uvc_host_driver_event_data_t *event, void *arg) {
    if (event->type == UVC_HOST_DRIVER_EVENT_DEVICE_CONNECTED &&
        event->device_connected.uvc_stream_index == 0) {
        atomic_store(&camera_address, event->device_connected.dev_addr);
    }
}

static void camera_stream_event(const uvc_host_stream_event_data_t *event, void *arg) {
    switch (event->type) {
        case UVC_HOST_DEVICE_DISCONNECTED:
            atomic_store(&camera_disconnected, true);
            atomic_store(&camera_accept_frames, false);
            atomic_store(&camera_address, 0);
            break;
        case UVC_HOST_TRANSFER_ERROR:
            atomic_fetch_add(&camera_errors, 1);
            atomic_store(&camera_last_error, event->transfer_error.error);
            break;
        case UVC_HOST_FRAME_BUFFER_OVERFLOW:
            atomic_fetch_add(&camera_overflows, 1);
            break;
        case UVC_HOST_FRAME_BUFFER_UNDERFLOW:
            atomic_fetch_add(&camera_dropped, 1);
            break;
        default:
            break;
    }
}

static bool camera_frame_received(const uvc_host_frame_t *frame, void *arg) {
    // The callback runs in the driver task and owns no Python objects.
    atomic_fetch_add(&camera_callbacks, 1);
    bool returned = true;
    if (atomic_load(&camera_accept_frames)) {
        bool invalid = frame->vs_format.format != camera_format.format || frame->data_len < 4 ||
            frame->data_len > frame->data_buffer_len || frame->data_len > camera_frame_size;
        if (camera_format.format == UVC_VS_FORMAT_YUY2) {
            invalid |= frame->vs_format.h_res != camera_format.h_res ||
                frame->vs_format.v_res != camera_format.v_res ||
                frame->data_len != (size_t)camera_format.h_res * camera_format.v_res * 2;
        }
        if (invalid) {
            atomic_fetch_add(&camera_errors, 1);
            atomic_store(&camera_last_error, ESP_ERR_INVALID_SIZE);
        } else {
            atomic_fetch_add(&camera_received, 1);
            if (xQueueSend(camera_frames, &frame, 0) == pdTRUE) {
                returned = false;
            } else {
                atomic_fetch_add(&camera_dropped, 1);
            }
        }
    }
    atomic_fetch_sub(&camera_callbacks, 1);
    return returned;
}

bool uiflow_uvc_active(uint32_t generation) {
    return camera_installed && generation == camera_generation;
}

uint32_t uiflow_uvc_generation(void) {
    return camera_generation;
}

static esp_err_t camera_drain(void) {
    uvc_host_frame_t *frame;
    while (camera_frames != NULL && xQueueReceive(camera_frames, &frame, 0) == pdTRUE) {
        esp_err_t err = uvc_host_frame_return(camera_stream, frame);
        if (err != ESP_OK) {
            // Preserve the outstanding frame so the application can retry cleanup.
            xQueueSend(camera_frames, &frame, 0);
            return err;
        }
    }
    return ESP_OK;
}

esp_err_t uiflow_uvc_stop(void) {
    atomic_store(&camera_accept_frames, false);
    if (camera_stream == NULL) {
        return ESP_OK;
    }
    esp_err_t stop_error = uvc_host_stream_stop(camera_stream);
    TickType_t started = xTaskGetTickCount();
    while (atomic_load(&camera_callbacks) != 0) {
        if (xTaskGetTickCount() - started >= pdMS_TO_TICKS(5000)) {
            return ESP_ERR_TIMEOUT;
        }
        vTaskDelay(pdMS_TO_TICKS(1));
    }
    esp_err_t err = camera_drain();
    if (err != ESP_OK) {
        return err;
    }
    // close() also handles an already stopped/disconnected stream. It must
    // succeed before the handle or frame queue can be discarded.
    err = uvc_host_stream_close(camera_stream);
    if (err != ESP_OK) {
        return err;
    }
    camera_stream = NULL;
    if (atomic_load(&camera_disconnected)) {
        return ESP_OK;
    }
    return stop_error;
}

esp_err_t uiflow_uvc_deinit(void) {
    esp_err_t err = uiflow_uvc_stop();
    if (err != ESP_OK) {
        return err;
    }
    if (uiflow_usb_bus_owner() == UIFLOW_USB_BUS_UVC) {
        esp_err_t power_error = uiflow_usb_bus_disconnect(UIFLOW_USB_BUS_UVC);
        if (camera_installed) {
            err = uvc_host_uninstall();
            if (err != ESP_OK) {
                return err;
            }
            camera_installed = false;
        }
        err = uiflow_usb_bus_release(UIFLOW_USB_BUS_UVC);
        if (err != ESP_OK) {
            return err;
        }
        if (power_error != ESP_OK) {
            return power_error;
        }
    }
    if (camera_frames != NULL) {
        vQueueDelete(camera_frames);
        camera_frames = NULL;
    }
    atomic_store(&camera_address, 0);
    return ESP_OK;
}

esp_err_t uiflow_uvc_init(unsigned width, unsigned height, unsigned fps, size_t frame_size,
    enum uvc_host_stream_format format) {
    if (camera_installed || camera_frames != NULL || uiflow_usb_bus_owner() != UIFLOW_USB_BUS_NONE) {
        return ESP_ERR_INVALID_STATE;
    }
    atomic_store(&camera_accept_frames, false);
    atomic_store(&camera_disconnected, false);
    atomic_store(&camera_address, 0);
    atomic_store(&camera_received, 0);
    atomic_store(&camera_dropped, 0);
    atomic_store(&camera_overflows, 0);
    atomic_store(&camera_errors, 0);
    atomic_store(&camera_last_error, ESP_OK);
    camera_format = (uvc_host_stream_format_t) {
        .h_res = width, .v_res = height, .fps = fps, .format = format,
    };
    camera_requested_format = camera_format;
    camera_frame_size = frame_size;
    esp_err_t err = uiflow_usb_bus_claim(UIFLOW_USB_BUS_UVC);
    if (err != ESP_OK) {
        goto fail;
    }
    camera_frames = xQueueCreate(UVC_QUEUED_FRAMES, sizeof(uvc_host_frame_t *));
    if (camera_frames == NULL) {
        err = ESP_ERR_NO_MEM;
        goto fail;
    }
    const uvc_host_driver_config_t config = {
        .driver_task_stack_size = 6144,
        .driver_task_priority = 5,
        .xCoreID = tskNO_AFFINITY,
        .create_background_task = true,
        .event_cb = camera_driver_event,
    };
    err = uvc_host_install(&config);
    if (err != ESP_OK) {
        goto fail;
    }
    camera_installed = true;
    err = uiflow_usb_bus_enable(UIFLOW_USB_BUS_UVC);
    if (err != ESP_OK) {
        goto fail;
    }
    ++camera_generation;
    return ESP_OK;
fail:
    if (uiflow_uvc_deinit() != ESP_OK) {
        ESP_LOGE("usbhost", "UVC initialization cleanup requires retry");
    }
    return err;
}

esp_err_t uiflow_uvc_start(unsigned timeout_ms) {
    if (!camera_installed || camera_stream != NULL) {
        return ESP_ERR_INVALID_STATE;
    }
    atomic_store(&camera_disconnected, false);
    const uvc_host_stream_config_t config = {
        .event_cb = camera_stream_event,
        .frame_cb = camera_frame_received,
        .vs_format = camera_requested_format,
        .advanced = {
            .number_of_frame_buffers = UVC_QUEUED_FRAMES + 1,
            .frame_size = camera_frame_size,
            .frame_heap_caps = MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT,
            .number_of_urbs = 4,
            .urb_size = 10 * 1024,
        },
    };
    esp_err_t err = uvc_host_stream_open(&config, pdMS_TO_TICKS(timeout_ms), &camera_stream);
    if (err != ESP_OK) {
        return err;
    }
    err = uvc_host_stream_format_get(camera_stream, &camera_format);
    if (err == ESP_OK && !atomic_load(&camera_disconnected)) {
        atomic_store(&camera_accept_frames, true);
        err = uvc_host_stream_start(camera_stream);
    } else if (err == ESP_OK) {
        err = ESP_ERR_NOT_FOUND;
    }
    if (err != ESP_OK) {
        uiflow_uvc_stop();
    }
    return err;
}

esp_err_t uiflow_uvc_frame_take(uvc_host_frame_t **frame) {
    *frame = NULL;
    if (atomic_load(&camera_disconnected)) {
        return ESP_ERR_NOT_FOUND;
    }
    if (camera_stream == NULL || !atomic_load(&camera_accept_frames)) {
        return ESP_ERR_INVALID_STATE;
    }
    esp_err_t err = uiflow_usb_bus_error();
    if (err != ESP_OK) {
        return err;
    }
    xQueueReceive(camera_frames, frame, 0);
    return ESP_OK;
}

esp_err_t uiflow_uvc_frame_release(uvc_host_frame_t *frame) {
    return uvc_host_frame_return(camera_stream, frame);
}

esp_err_t uiflow_uvc_formats(uvc_host_frame_info_t (*formats)[], size_t *count) {
    unsigned address = atomic_load(&camera_address);
    if (address == 0) {
        return ESP_ERR_NOT_FOUND;
    }
    return uvc_host_get_frame_list(address, 0, formats, count);
}

void uiflow_uvc_info(uiflow_uvc_info_t *info) {
    *info = (uiflow_uvc_info_t) {
        .frames = atomic_load(&camera_received),
        .dropped = atomic_load(&camera_dropped),
        .overflows = atomic_load(&camera_overflows),
        .errors = atomic_load(&camera_errors),
        .last_error = atomic_load(&camera_last_error),
        .connected = atomic_load(&camera_address) != 0 && !atomic_load(&camera_disconnected),
        .streaming = atomic_load(&camera_accept_frames),
        .format = camera_format,
    };
}

static uint8_t camera_clamp(int value) {
    return value < 0 ? 0 : (value > 255 ? 255 : value);
}

static void camera_pixel_rgb565(uint8_t *output, int y, int u, int v) {
    // BT.601 limited range. Store native little-endian RGB565 for drawRawBuf.
    int c = y - 16;
    unsigned r = camera_clamp((298 * c + 409 * v + 128) >> 8);
    unsigned g = camera_clamp((298 * c - 100 * u - 208 * v + 128) >> 8);
    unsigned b = camera_clamp((298 * c + 516 * u + 128) >> 8);
    uint16_t pixel = ((r & 0xf8) << 8) | ((g & 0xfc) << 3) | (b >> 3);
    output[0] = pixel;
    output[1] = pixel >> 8;
}

esp_err_t uiflow_uvc_rgb565(const uvc_host_frame_t *frame, uint8_t *output, size_t size) {
    if (frame->vs_format.format != UVC_VS_FORMAT_YUY2) {
        return ESP_ERR_INVALID_ARG;
    }
    size_t expected = (size_t)frame->vs_format.h_res * frame->vs_format.v_res * 2;
    if (!frame->vs_format.h_res || !frame->vs_format.v_res || (frame->vs_format.h_res & 1) ||
        frame->data_len != expected || expected > frame->data_buffer_len || size < expected) {
        return ESP_ERR_INVALID_SIZE;
    }
    const uint8_t *input = frame->data;
    for (size_t i = 0; i < expected; i += 4) {
        int u = input[i + 1] - 128;
        int v = input[i + 3] - 128;
        camera_pixel_rgb565(output + i, input[i], u, v);
        camera_pixel_rgb565(output + i + 2, input[i + 2], u, v);
    }
    return ESP_OK;
}

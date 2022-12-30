#ifndef __M5THINGS_H__
#define __M5THINGS_H__

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

extern TaskHandle_t m5thing_task_handle;
extern bool wifi_sta_connected;
extern int mp_interrupt_char;

extern int hmac_sha256(const uint8_t *, size_t, const uint8_t *, size_t data_len, uint8_t *);
extern char * base64_encode(const void *src, size_t len, size_t *out_len);
extern unsigned char * base64_decode(const char *src, size_t len, size_t *out_len);
extern char * base64_url_encode(const void *src, size_t len, size_t *out_len);
extern unsigned char * base64_url_decode(const char *src, size_t len, size_t *out_len);

void m5thing_task(void *pvParameter);

#endif

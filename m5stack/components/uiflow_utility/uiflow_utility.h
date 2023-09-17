#ifndef _UIFLOW_UTILITY_H_
#define _UIFLOW_UTILITY_H_

#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#include "esp_log.h"
#include "nvs_flash.h"
#include "nvs.h"

// NVS Read/Write Helpers
#define UIFLOW_NVS_NAMESPACE "uiflow"

bool nvs_read_str_helper(char *ns, char *key, char *value, size_t *_len);
bool nvs_write_str_helper(char *ns, char *key, char *value);
bool nvs_read_u8_helper(char *ns, char *key, uint8_t *value);
bool nvs_write_u8_helper(char *ns, char *key, uint8_t value);
bool nvs_read_u32_helper(char *ns, char *key, uint32_t *value);
bool nvs_write_u32_helper(char *ns, char *key, uint32_t value);

#endif // _UIFLOW_UTILITY_H_

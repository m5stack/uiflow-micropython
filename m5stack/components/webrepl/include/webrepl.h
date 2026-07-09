#ifndef __WEBREPL_H__
#define __WEBREPL_H__

#include <stdbool.h>
#include <stddef.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#ifdef __cplusplus
extern "C" {
#endif

extern TaskHandle_t webrepl_task_handle;
bool webrepl_should_start(void);
void webrepl_task(void *pvParameter);

#ifdef __cplusplus
}
#endif
#endif

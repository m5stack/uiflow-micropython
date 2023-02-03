#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>

typedef struct _imu_obj_t {
    mp_obj_base_t base;
    void *imu;
} imu_obj_t;

extern const mp_obj_type_t mp_imu_type;

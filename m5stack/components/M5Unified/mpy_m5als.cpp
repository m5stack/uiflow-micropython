/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include <utility/LTR553_Class.hpp>

extern "C"
{
#include "mpy_m5als.h"

namespace m5
{
    static inline LTR553_Class *getAls(const mp_obj_t& self) {
        return (LTR553_Class *)(((als_obj_t *)MP_OBJ_TO_PTR(self))->als);
    }

    mp_obj_t als_getLightSensorData(mp_obj_t self) {
        uint16_t value = getAls(self)->getLightSensorData();
        return mp_obj_new_int(value);
    }

    mp_obj_t als_getProximitySensorData(mp_obj_t self) {
        uint16_t value = getAls(self)->getProximitySensorData();
        return mp_obj_new_int(value);
    }

}
}

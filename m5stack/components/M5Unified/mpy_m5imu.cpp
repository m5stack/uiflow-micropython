#include <utility/IMU_Class.hpp>

extern "C"
{
#include "mpy_m5imu.h"

namespace m5
{
    static inline IMU_Class *getImu(const mp_obj_t& self) {
        return (IMU_Class *)(((imu_obj_t *)MP_OBJ_TO_PTR(self))->imu);
    }

    mp_obj_t imu_getAccel(mp_obj_t self) {
        float x = 0.0f,y = 0.0f,z = 0.0f;
        getImu(self)->getAccel(&x, &y, &z);
        mp_obj_t tuple[3] = { mp_obj_new_float(x)
                              , mp_obj_new_float(y)
                              , mp_obj_new_float(x)};
        return mp_obj_new_tuple(3, tuple);
    }
    mp_obj_t imu_getGyro(mp_obj_t self) {
        float x = 0.0f,y = 0.0f,z = 0.0f;
        getImu(self)->getGyro(&x, &y, &z);
        mp_obj_t tuple[3] = { mp_obj_new_float(x)
                              , mp_obj_new_float(y)
                              , mp_obj_new_float(x)};
        return mp_obj_new_tuple(3, tuple);
    }
    mp_obj_t imu_getType(mp_obj_t self) {
        return mp_obj_new_int(getImu(self)->getType());
    }
    mp_obj_t imu_isEnabled(mp_obj_t self) {
        return mp_obj_new_bool(getImu(self)->isEnabled());
    }
}
}

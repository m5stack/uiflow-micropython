/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "m5unified.h"

// IMU type
static const mp_rom_map_elem_t m5_imu_types_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_NULL),          MP_ROM_INT(0) },
    { MP_ROM_QSTR(MP_QSTR_UNKNOWN),       MP_ROM_INT(1) },
    { MP_ROM_QSTR(MP_QSTR_SH200Q),        MP_ROM_INT(2) },
    { MP_ROM_QSTR(MP_QSTR_MPU6050),       MP_ROM_INT(3) },
    { MP_ROM_QSTR(MP_QSTR_MPU6886),       MP_ROM_INT(4) },
    { MP_ROM_QSTR(MP_QSTR_MPU9250),       MP_ROM_INT(5) },
    { MP_ROM_QSTR(MP_QSTR_BMI270),        MP_ROM_INT(6) },
    /* *FORMAT-ON* */
};
static MP_DEFINE_CONST_DICT(m5_imu_types, m5_imu_types_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_m5_imu_type,
    MP_QSTR_IMU_Type,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&m5_imu_types
    );
#else
const mp_obj_type_t mp_m5_imu_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_IMU_Type,
    .locals_dict = (mp_obj_dict_t *)&m5_imu_types,
};
#endif

// -------- IMU wrapper
MAKE_METHOD_0(imu, getAccel);
MAKE_METHOD_0(imu, getGyro);
MAKE_METHOD_0(imu, getMag);
MAKE_METHOD_0(imu, isEnabled);
MAKE_METHOD_0(imu, getType);

static const mp_rom_map_elem_t imu_member_table[] = {
    { MP_ROM_QSTR(MP_QSTR_IMU_TYPE),       MP_ROM_PTR(&mp_m5_imu_type) },
    MAKE_TABLE(imu, getAccel),
    MAKE_TABLE(imu, getGyro),
    MAKE_TABLE(imu, getMag),
    MAKE_TABLE(imu, isEnabled),
    MAKE_TABLE(imu, getType),
};

static MP_DEFINE_CONST_DICT(imu_member, imu_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_imu_type,
    MP_QSTR_IMU,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&imu_member
    );
#else
const mp_obj_type_t mp_imu_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_IMU,
    .locals_dict = (mp_obj_dict_t *)&imu_member,
};
#endif

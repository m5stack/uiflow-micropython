#include "m5unified.h"

// IMU type
STATIC const mp_rom_map_elem_t m5_imu_types_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR_unknown),       MP_ROM_INT(0) },
    { MP_ROM_QSTR(MP_QSTR_SH200Q),        MP_ROM_INT(1) },
    { MP_ROM_QSTR(MP_QSTR_MPU6050),       MP_ROM_INT(2) },
    { MP_ROM_QSTR(MP_QSTR_MPU6886),       MP_ROM_INT(3) },
    { MP_ROM_QSTR(MP_QSTR_MPU9250),       MP_ROM_INT(4) },
    /* *FORMAT-ON* */
};
STATIC MP_DEFINE_CONST_DICT(m5_imu_types, m5_imu_types_table);

const mp_obj_type_t mp_m5_imu_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_IMU_Type,
    .locals_dict = (mp_obj_dict_t *)&m5_imu_types,
};

// -------- IMU wrapper
MAKE_METHOD_0(imu, getAccel);
MAKE_METHOD_0(imu, getGyro);
MAKE_METHOD_0(imu, isEnabled);
MAKE_METHOD_0(imu, getType);

STATIC const mp_rom_map_elem_t imu_member_table[] = {
    { MP_ROM_QSTR(MP_QSTR_IMU_TYPE),       MP_ROM_PTR(&mp_m5_imu_type) },
    MAKE_TABLE(imu, getAccel),
    MAKE_TABLE(imu, getGyro),
    MAKE_TABLE(imu, isEnabled),
    MAKE_TABLE(imu, getType),
};

STATIC MP_DEFINE_CONST_DICT(imu_member, imu_member_table);

const mp_obj_type_t mp_imu_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_IMU,
    .locals_dict = (mp_obj_dict_t *)&imu_member,
};

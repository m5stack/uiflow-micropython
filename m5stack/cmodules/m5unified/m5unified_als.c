#include "m5unified.h"

MAKE_METHOD_0(als, getLightSensorData);
MAKE_METHOD_0(als, getProximitySensorData);

STATIC const mp_rom_map_elem_t als_member_table[] = {
    MAKE_TABLE(als, getLightSensorData),
    MAKE_TABLE(als, getProximitySensorData),
};

STATIC MP_DEFINE_CONST_DICT(als_member, als_member_table);

#ifdef MP_OBJ_TYPE_GET_SLOT
MP_DEFINE_CONST_OBJ_TYPE(
    mp_als_type,
    MP_QSTR_ALS,
    MP_TYPE_FLAG_NONE,
    locals_dict, (mp_obj_dict_t *)&als_member
    );
#else
const mp_obj_type_t mp_als_type = {
    .base = { &mp_type_type },
    .name = MP_QSTR_ALS,
    .locals_dict = (mp_obj_dict_t *)&als_member,
};
#endif

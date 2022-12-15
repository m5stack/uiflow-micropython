#include "m5unified.h"

STATIC const mp_rom_map_elem_t widget_member_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__),     MP_ROM_QSTR(MP_QSTR_widget) },
};
STATIC MP_DEFINE_CONST_DICT(widget_member, widget_member_table);

const mp_obj_type_t mp_widget_type = {
    .base = { &mp_type_type },
    .flags = MP_TYPE_FLAG_IS_SUBCLASSED,
    .name = MP_QSTR_Widget,
    .locals_dict = (mp_obj_dict_t *)&widget_member,
};

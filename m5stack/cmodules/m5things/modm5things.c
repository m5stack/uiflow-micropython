#include "m5things.h"

#include "py/stackctrl.h"
#include "py/nlr.h"
#include "py/compile.h"
#include "py/runtime.h"
#include "py/persistentcode.h"
#include "py/repl.h"
#include "py/gc.h"
#include "py/mphal.h"
#include "py/ringbuf.h"
#include "shared/readline/readline.h"
#include "shared/runtime/pyexec.h"
#include "shared/runtime/interrupt_char.h"

extern volatile m5things_status_t m5things_cnct_status;

STATIC mp_obj_t m5things_status() {
    return mp_obj_new_int(m5things_cnct_status);
}
STATIC MP_DEFINE_CONST_FUN_OBJ_0(m5things_status_obj, m5things_status);

STATIC const mp_rom_map_elem_t m5things_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_M5Things) },

    // functions
    { MP_ROM_QSTR(MP_QSTR_status),  MP_ROM_PTR(&m5things_status_obj) },
};
STATIC MP_DEFINE_CONST_DICT(mp_module_m5things_globals, m5things_globals_table);

// Define module object.
const mp_obj_module_t m5things_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&mp_module_m5things_globals,
};

MP_REGISTER_MODULE(MP_QSTR_M5Things, m5things_user_cmodule);

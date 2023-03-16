#pragma once

#include <py/runtime.h>
#include <py/objstr.h>
#include <py/objmodule.h>


typedef enum {
    BTN_TYPE_WAS_CLICKED = 0,
    BTN_TYPE_WAS_SINGLECLICKED,
    BTN_TYPE_WAS_DOUBLECLICKED,
    BTN_TYPE_WAS_HOLD,
    BTN_TYPE_WAS_PRESSED,
    BTN_TYPE_WAS_RELEASED
} btn_cb_type_t;

typedef struct _btn_callback_t {
    union
    {
        struct
        {
            uint8_t wasClicked : 1;
            uint8_t wasSingleClicked : 1;
            uint8_t wasDoubleClicked : 1;
            uint8_t wasHold : 1;
            uint8_t wasPressed : 1;
            uint8_t wasReleased : 2;
        } flag_bit;
        uint8_t flag;
    };
    mp_obj_t wasClicked_cb;        // flag bit[1]
    mp_obj_t wasSingleClicked_cb;  // flag bit[2]
    mp_obj_t wasDoubleClicked_cb;  // flag bit[3]
    mp_obj_t wasHold_cb;           // flag bit[4]
    mp_obj_t wasPressed_cb;        // flag bit[5]
    mp_obj_t wasReleased_cb;       // flag bit[6]
} btn_callback_t;

typedef struct _btn_obj_t {
    mp_obj_base_t base;
    void *btn;
    btn_callback_t callbacks;
} btn_obj_t;

extern const mp_obj_type_t mp_btn_type;

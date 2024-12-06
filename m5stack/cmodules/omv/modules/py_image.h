#ifdef __cplusplus 
extern "C" { 
#endif

#pragma once 

#include "py/obj.h"
#include "imlib.h"


typedef struct _py_image_obj_t {
    mp_obj_base_t base;
    image_t _cobj;
} py_image_obj_t;

extern const mp_obj_type_t py_image_type;

mp_obj_t py_image(int width, int height, omv_pixformat_t pixfmt, uint32_t size, void* pixels);
mp_obj_t py_image_from_struct(image_t* img);
void* py_image_cobj(mp_obj_t img_obj);

 


#ifdef __cplusplus
}
#endif






#include <M5GFX.h>

#include <ffi.h>
typedef union {
  ffi_sarg sint;
  ffi_arg  uint;
  float    flt;
  double   dbl;
  void*    ptr;
} ffi_value;

extern "C"
{
  #include "mpy_m5gfx.h"

  static inline LovyanGFX* getGfx(const mp_obj_t* args)
  {
    return (LovyanGFX*)(((gfx_obj_t*)MP_OBJ_TO_PTR(args[0]))->gfx);
  }

//-------- GFX common wrapper

  mp_obj_t gfx_width(mp_obj_t self)
  {
    auto gfx = getGfx(&self);
    return mp_obj_new_int(gfx->width());
  }

  mp_obj_t gfx_height(mp_obj_t self)
  {
    auto gfx = getGfx(&self);
    return mp_obj_new_int(gfx->height());
  }

  mp_obj_t gfx_getRotation(mp_obj_t self)
  {
    auto gfx = getGfx(&self);
    return mp_obj_new_int(gfx->getRotation());
  }

  mp_obj_t gfx_getColorDepth(mp_obj_t self)
  {
    auto gfx = getGfx(&self);
    return mp_obj_new_int(gfx->getColorDepth());
  }

  mp_obj_t gfx_setRotation(mp_obj_t self, mp_obj_t r)
  {
    auto gfx = getGfx(&self);
    gfx->setRotation(mp_obj_get_int(r));
    return mp_const_none;
  }

  mp_obj_t gfx_setColorDepth(mp_obj_t self, mp_obj_t bpp)
  {
    auto gfx = getGfx(&self);
    gfx->setColorDepth(mp_obj_get_int(bpp));
    return mp_const_none;
  }

  mp_obj_t gfx_print(mp_obj_t self, mp_obj_t str)
  {
    auto gfx = getGfx(&self);
    gfx->print( mp_obj_str_get_str(str));
    return mp_const_none;
  }

  mp_obj_t gfx_setCursor(mp_obj_t self, mp_obj_t x, mp_obj_t y)
  {
    auto gfx = getGfx(&self);
    gfx->setCursor( mp_obj_get_int(x)
                  , mp_obj_get_int(y)
                  );
    return mp_const_none;
  }

  mp_obj_t gfx_fillScreen(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 2) { gfx->setColor((uint32_t)mp_obj_get_int(args[1])); }
    gfx->fillScreen();
    return mp_const_none;
  }

  mp_obj_t gfx_drawPixel(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 4) { gfx->setColor((uint32_t)mp_obj_get_int(args[3])); }
    gfx->drawPixel( mp_obj_get_int(args[1])
                  , mp_obj_get_int(args[2])
                  );
    return mp_const_none;
  }

  mp_obj_t gfx_drawCircle(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 5) { gfx->setColor((uint32_t)mp_obj_get_int(args[4])); }
    gfx->drawCircle( mp_obj_get_int(args[1])
                   , mp_obj_get_int(args[2])
                   , mp_obj_get_int(args[3])
                   );
    return mp_const_none;
  }

  mp_obj_t gfx_fillCircle(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 5) { gfx->setColor((uint32_t)mp_obj_get_int(args[4])); }
    gfx->fillCircle( mp_obj_get_int(args[1])
                   , mp_obj_get_int(args[2])
                   , mp_obj_get_int(args[3])
                   );
    return mp_const_none;
  }

  mp_obj_t gfx_drawLine(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 6) { gfx->setColor((uint32_t)mp_obj_get_int(args[5])); }
    gfx->drawLine( mp_obj_get_int(args[1])
                 , mp_obj_get_int(args[2])
                 , mp_obj_get_int(args[3])
                 , mp_obj_get_int(args[4])
                 );
    return mp_const_none;
  }

  mp_obj_t gfx_drawRect(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 6) { gfx->setColor((uint32_t)mp_obj_get_int(args[5])); }
    gfx->drawRect( mp_obj_get_int(args[1])
                 , mp_obj_get_int(args[2])
                 , mp_obj_get_int(args[3])
                 , mp_obj_get_int(args[4])
                 );
    return mp_const_none;
  }

  mp_obj_t gfx_fillRect(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 6) { gfx->setColor((uint32_t)mp_obj_get_int(args[5])); }
    gfx->fillRect( mp_obj_get_int(args[1])
                 , mp_obj_get_int(args[2])
                 , mp_obj_get_int(args[3])
                 , mp_obj_get_int(args[4])
                 );
    return mp_const_none;
  }

  mp_obj_t gfx_printf(size_t n_args, const mp_obj_t *args)
  {
    auto types  = (ffi_type**)alloca(n_args * sizeof(ffi_type *));
    auto values = (ffi_value*)alloca(n_args * sizeof(ffi_value));
    auto arg_values = (void**)alloca(n_args * sizeof(void *));

    size_t i;
    types[0] = &ffi_type_pointer;
    values[0].ptr = getGfx(args);
    arg_values[0] = &values[0];
    for (i = 1; i < n_args; i++) {
      if (mp_obj_get_int_maybe(args[i], (mp_int_t *)&values[i].sint)) {
        types[i] = &ffi_type_sint;
      } else if (mp_obj_is_float(args[i])) {
        types[i] = &ffi_type_double;
        values[i].dbl = mp_obj_get_float_to_d(args[i]);
      } else if (mp_obj_is_str(args[i])) {
        types[i] = &ffi_type_pointer;
        values[i].ptr = (void *)mp_obj_str_get_str(args[i]);
      } else {
        // ERROR
        mp_raise_TypeError(MP_ERROR_TEXT("not supported type is specified"));
      }
      arg_values[i] = &values[i];
    }

    ffi_cif cif;
    ffi_prep_cif_var(&cif, FFI_DEFAULT_ABI, 1, n_args, &ffi_type_sint, types);
    ffi_arg result;
    ffi_call(&cif, FFI_FN(&LovyanGFX::printf), &result, arg_values);

    return mp_const_none;
  }

  mp_obj_t gfx_push(mp_obj_t self, mp_obj_t x, mp_obj_t y)
  {
    auto gfx = getGfx(&self);
    if (gfx)
    {
      ((M5Canvas*)gfx)->pushSprite(mp_obj_get_int(x), mp_obj_get_int(y));
    }
    return mp_const_none;
  }

//-------- GFX device wrapper

  mp_obj_t gfx_startWrite(mp_obj_t self)
  {
    auto gfx = getGfx(&self);
    gfx->startWrite();
    return mp_const_none;
  }

  mp_obj_t gfx_endWrite(mp_obj_t self)
  {
    auto gfx = getGfx(&self);
    gfx->endWrite();
    return mp_const_none;
  }

//-------- GFX canvas wrapper

  mp_obj_t gfx_delete(mp_obj_t self)
  {
    auto gfx = getGfx(&self);
    if (gfx)
    {
      ((M5Canvas*)gfx)->deleteSprite();
      delete (M5Canvas*)gfx;
      ((gfx_obj_t*)MP_OBJ_TO_PTR(self))->gfx = nullptr;
    }
    return mp_const_none;
  }

  mp_obj_t gfx_newCanvas(  size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    auto canvas = new M5Canvas(gfx);
    if (n_args >= 5) { canvas->setPsram(mp_obj_get_int(args[4])); }
    if (n_args >= 4) { canvas->setColorDepth(mp_obj_get_int(args[3])); }
    if (n_args >= 3) { canvas->createSprite(mp_obj_get_int(args[1]), mp_obj_get_int(args[2])); }
    gfx_obj_t *res = m_new_obj_with_finaliser(gfx_obj_t);
    res->base.type = &gfxcanvas_type;
    res->gfx = canvas;
    return MP_OBJ_FROM_PTR(res);
  }


}

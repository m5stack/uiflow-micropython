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
  #include <py/obj.h>
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

  mp_obj_t gfx_print(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 3) { gfx->setTextColor((uint32_t)mp_obj_get_int(args[2])); }
    gfx->print( mp_obj_str_get_str(args[1]));
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

  mp_obj_t gfx_getCursor(mp_obj_t self)
  {
    auto gfx = getGfx(&self);
    mp_obj_t tuple[2] = { mp_obj_new_int(gfx->getCursorX())
                        , mp_obj_new_int(gfx->getCursorY())
                        };
    return mp_obj_new_tuple(2, tuple);
  }

  mp_obj_t gfx_setFont(mp_obj_t self, mp_obj_t font)
  {
    auto gfx = getGfx(&self);
    gfx->setFont((const m5gfx::IFont*) ((font_obj_t*)MP_OBJ_TO_PTR(font))->font);
    return mp_const_none;
  }

  mp_obj_t gfx_setTextColor(mp_obj_t self, mp_obj_t color)
  {
    auto gfx = getGfx(&self);
    gfx->setTextColor((uint32_t)mp_obj_get_int(color));
    return mp_const_none;
  }

  mp_obj_t gfx_setTextScroll(mp_obj_t self, mp_obj_t scroll)
  {
    auto gfx = getGfx(&self);
    gfx->setTextScroll((bool)mp_obj_get_int(scroll));
    return mp_const_none;
  }

  mp_obj_t gfx_clear(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 2) { gfx->setBaseColor((uint32_t)mp_obj_get_int(args[1])); }
    gfx->clear();
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

  mp_obj_t gfx_drawRoundRect(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 7) { gfx->setColor((uint32_t)mp_obj_get_int(args[6])); }
    gfx->drawRoundRect( mp_obj_get_int(args[1])
                      , mp_obj_get_int(args[2])
                      , mp_obj_get_int(args[3])
                      , mp_obj_get_int(args[4])
                      , mp_obj_get_int(args[5])
                      );
    return mp_const_none;
  }

  mp_obj_t gfx_fillRoundRect(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (n_args >= 7) { gfx->setColor((uint32_t)mp_obj_get_int(args[6])); }
    gfx->fillRoundRect( mp_obj_get_int(args[1])
                      , mp_obj_get_int(args[2])
                      , mp_obj_get_int(args[3])
                      , mp_obj_get_int(args[4])
                      , mp_obj_get_int(args[5])
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

  mp_obj_t gfx_drawBmp(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (mp_obj_is_str(args[1]) && ((size_t)mp_obj_len(args[1]) < 128)) // file
    {
      gfx->drawBmpFile( mp_obj_str_get_str(args[1])
                      , mp_obj_get_int(args[2])
                      , mp_obj_get_int(args[3]));
    }
    else // buffer
    {
      mp_buffer_info_t bufinfo;
      mp_get_buffer_raise(args[1], &bufinfo, MP_BUFFER_READ);
      gfx->drawBmp( (const uint8_t*)bufinfo.buf
                  , bufinfo.len
                  , mp_obj_get_int(args[2])
                  , mp_obj_get_int(args[3]));
    }
    return mp_const_none;
  }

  mp_obj_t gfx_drawJpg(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (mp_obj_is_str(args[1]) && ((size_t)mp_obj_len(args[1]) < 128)) // file
    {
      gfx->drawJpgFile( mp_obj_str_get_str(args[1])
                      , mp_obj_get_int(args[2])
                      , mp_obj_get_int(args[3]));
    }
    else // buffer
    {
      mp_buffer_info_t bufinfo;
      mp_get_buffer_raise(args[1], &bufinfo, MP_BUFFER_READ);
      gfx->drawJpg( (const uint8_t*)bufinfo.buf
                  , bufinfo.len
                  , mp_obj_get_int(args[2])
                  , mp_obj_get_int(args[3]));
    }
    return mp_const_none;
  }

  mp_obj_t gfx_drawPng(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (mp_obj_is_str(args[1]) && ((size_t)mp_obj_len(args[1]) < 128)) // file
    {
      gfx->drawPngFile( mp_obj_str_get_str(args[1])
                      , mp_obj_get_int(args[2])
                      , mp_obj_get_int(args[3]));
    }
    else // buffer
    {
      mp_buffer_info_t bufinfo;
      mp_get_buffer_raise(args[1], &bufinfo, MP_BUFFER_READ);
      gfx->drawPng( (const uint8_t*)bufinfo.buf
                  , bufinfo.len
                  , mp_obj_get_int(args[2])
                  , mp_obj_get_int(args[3]));
    }
    return mp_const_none;
  }

  mp_obj_t gfx_drawImage(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    if (mp_obj_is_str(args[1]) && ((size_t)mp_obj_len(args[1]) < 128)) // file
    {
      char ftype[5] = {0};
      const char *file_path = mp_obj_str_get_str(args[1]);

      for (size_t i = 0; i < 4; i++)
      {
        ftype[i] = tolower((char)file_path[i + strlen(file_path) - 4]);
      }
      ftype[4] = '\0';

      if (strstr(ftype, "bmp") != NULL)
      {
        gfx->drawBmpFile( file_path
                        , mp_obj_get_int(args[2])
                        , mp_obj_get_int(args[3]));
      }
      else if ((strstr(ftype, "jpg") != NULL) || (strstr(ftype, "jpeg") != NULL))
      {
        gfx->drawJpgFile( file_path
                        , mp_obj_get_int(args[2])
                        , mp_obj_get_int(args[3]));
      }
      else if (strstr(ftype, "png") != NULL)
      {
        gfx->drawPngFile( file_path
                        , mp_obj_get_int(args[2])
                        , mp_obj_get_int(args[3]));
      }
    }
    else // buffer
    {
      mp_buffer_info_t bufinfo;
      mp_get_buffer_raise(args[1], &bufinfo, MP_BUFFER_READ);
      uint8_t* type_ptr = (uint8_t *)bufinfo.buf;

      if ((type_ptr[0] == 0x42) && (type_ptr[1] == 0x4D))
      {
        gfx->drawBmp( (const uint8_t*)bufinfo.buf
                    , bufinfo.len
                    , mp_obj_get_int(args[2])
                    , mp_obj_get_int(args[3]));
      }
      else if ((type_ptr[0] == 0xFF) && (type_ptr[1] == 0xD8))
      {
        gfx->drawJpg( (const uint8_t*)bufinfo.buf
                    , bufinfo.len
                    , mp_obj_get_int(args[2])
                    , mp_obj_get_int(args[3]));
      }
      else if ((type_ptr[0] == 0x89) && (type_ptr[1] == 0x50))
      {
        gfx->drawPng( (const uint8_t*)bufinfo.buf
                    , bufinfo.len
                    , mp_obj_get_int(args[2])
                    , mp_obj_get_int(args[3]));
      }
    }
    return mp_const_none;
  }

  mp_obj_t gfx_drawQR(size_t n_args, const mp_obj_t *args)
  {
    auto gfx = getGfx(args);
    gfx->qrcode( mp_obj_str_get_str(args[1])
               , mp_obj_get_int(args[2])
               , mp_obj_get_int(args[3])
               , mp_obj_get_int(args[4])
               , mp_obj_get_int(args[5]));
    return mp_const_none;
  }

  mp_obj_t gfx_newCanvas(size_t n_args, const mp_obj_t *args)
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

  mp_obj_t gfx_push(mp_obj_t self, mp_obj_t x, mp_obj_t y)
  {
    auto gfx = getGfx(&self);
    if (gfx)
    {
      ((M5Canvas*)gfx)->pushSprite(mp_obj_get_int(x), mp_obj_get_int(y));
    }
    return mp_const_none;
  }

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

  const font_obj_t gfx_font_0_obj = {{ &mp_type_object }, &m5gfx::fonts::Font0 };
  const font_obj_t gfx_font_2_obj = {{ &mp_type_object }, &m5gfx::fonts::Font2 };
  const font_obj_t gfx_font_4_obj = {{ &mp_type_object }, &m5gfx::fonts::Font4 };
  const font_obj_t gfx_font_6_obj = {{ &mp_type_object }, &m5gfx::fonts::Font6 };
  const font_obj_t gfx_font_7_obj = {{ &mp_type_object }, &m5gfx::fonts::Font7 };
  const font_obj_t gfx_font_8_obj = {{ &mp_type_object }, &m5gfx::fonts::Font8 };
  const font_obj_t gfx_font_DejaVu9_obj  = {{ &mp_type_object }, &m5gfx::fonts::DejaVu9  };
  const font_obj_t gfx_font_DejaVu12_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu12 };
  const font_obj_t gfx_font_DejaVu18_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu18 };
  const font_obj_t gfx_font_DejaVu24_obj = {{ &mp_type_object }, &m5gfx::fonts::DejaVu24 };

}

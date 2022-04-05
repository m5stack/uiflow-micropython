#include <utility/Speaker_Class.hpp>

extern "C"
{
  #include "mpy_m5spk.h"

  namespace m5
  {
    static inline Speaker_Class* getSpk(const mp_obj_t* args)
    {
      return (Speaker_Class*)(((spk_obj_t*)MP_OBJ_TO_PTR(args[0]))->spk);
    }

    mp_obj_t spk_setVolume(mp_obj_t self, mp_obj_t vol)
    {
      getSpk(&self)->setVolume(mp_obj_get_int(vol));
      return mp_const_none;
    }

    mp_obj_t spk_getVolume(mp_obj_t self)
    {
      return mp_obj_new_int(getSpk(&self)->getVolume());
    }

    mp_obj_t spk_setAllChannelVolume(mp_obj_t self, mp_obj_t vol)
    {
      getSpk(&self)->setAllChannelVolume(mp_obj_get_int(vol));
      return mp_const_none;
    }

    mp_obj_t spk_setChannelVolume(mp_obj_t self, mp_obj_t ch, mp_obj_t vol)
    {
      getSpk(&self)->setChannelVolume(mp_obj_get_int(ch), mp_obj_get_int(vol));
      return mp_const_none;
    }

    mp_obj_t spk_getChannelVolume(mp_obj_t self, mp_obj_t ch)
    {
      return mp_obj_new_int(getSpk(&self)->getChannelVolume(mp_obj_get_int(ch)));
    }

    mp_obj_t spk_tone(size_t n_args, const mp_obj_t *args)
    {
      auto spk = getSpk(args);
      float freq = mp_obj_get_float(args[1]);
      int msec   = mp_obj_get_int(args[2]);
      int ch = -1;
      if (n_args >= 4) { ch = mp_obj_get_int(args[3]); }

      spk->tone(freq, msec, ch, true);

      return mp_const_none;
    }

    mp_obj_t spk_stop(size_t n_args, const mp_obj_t *args)
    {
      auto spk = getSpk(args);
      int ch = -1;
      if (n_args >= 2) { ch = mp_obj_get_int(args[1]); }

      spk->stop(ch);

      return mp_const_none;
    }
  }
}

#include <utility/Button_Class.hpp>

extern "C"
{
  #include "mpy_m5btn.h"

  namespace m5
  {
    static inline Button_Class* getBtn(const mp_obj_t& self)
    {
      return (Button_Class*)(((btn_obj_t*)MP_OBJ_TO_PTR(self))->btn);
    }

    mp_obj_t btn_isHolding          (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->isHolding()); }
    mp_obj_t btn_isPressed          (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->isPressed()); }
    mp_obj_t btn_isReleased         (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->isReleased()); }
    mp_obj_t btn_wasChangePressed   (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->wasChangePressed()); }
    mp_obj_t btn_wasClicked         (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->wasClicked()); }
    mp_obj_t btn_wasHold            (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->wasHold()); }
    mp_obj_t btn_wasPressed         (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->wasPressed()); }
    mp_obj_t btn_wasReleased        (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->wasReleased()); }
    mp_obj_t btn_wasSingleClicked   (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->wasSingleClicked()); }
    mp_obj_t btn_wasDoubleClicked   (mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->wasDoubleClicked()); }
    mp_obj_t btn_wasDeciedClickCount(mp_obj_t self) { return mp_obj_new_bool(getBtn(self)->wasDeciedClickCount()); }
    mp_obj_t btn_getClickCount      (mp_obj_t self) { return mp_obj_new_int( getBtn(self)->getClickCount()); }
    mp_obj_t btn_lastChange         (mp_obj_t self) { return mp_obj_new_int( getBtn(self)->lastChange()); }
    mp_obj_t btn_pressedFor         (mp_obj_t self, mp_obj_t msec) { return mp_obj_new_bool(getBtn(self)->pressedFor( mp_obj_get_int(msec))); }
    mp_obj_t btn_releasedFor        (mp_obj_t self, mp_obj_t msec) { return mp_obj_new_bool(getBtn(self)->releasedFor(mp_obj_get_int(msec))); }
    mp_obj_t btn_setDebounceThresh  (mp_obj_t self, mp_obj_t msec) { getBtn(self)->setDebounceThresh(mp_obj_get_int(msec)); return mp_const_none; }
    mp_obj_t btn_setHoldThresh      (mp_obj_t self, mp_obj_t msec) { getBtn(self)->setHoldThresh(    mp_obj_get_int(msec)); return mp_const_none; }
  }
}

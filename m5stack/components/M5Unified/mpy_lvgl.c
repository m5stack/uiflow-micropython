#if MICROPY_PY_LVGL
#include "lvgl/lvgl.h"
#include "lvgl/src/hal/lv_hal_disp.h"
LovyanGFX *g_gfx = &(M5.Display);

void gfx_lvgl_flush(struct _disp_drv_t * disp_drv, const lv_area_t * area, lv_color_t * color_p)
{
    if (g_gfx == nullptr) {
        return;
    }
    int w = (area->x2 - area->x1 + 1);
    int h = (area->y2 - area->y1 + 1);
    g_gfx->startWrite();
    g_gfx->setAddrWindow(area->x1, area->y1, w, h);
    g_gfx->writePixels((lgfx::rgb565_t *)&color_p->full, w * h);
    g_gfx->endWrite();
    lv_disp_flush_ready((lv_disp_drv_t*)disp_drv);
}

bool gfx_lvgl_touch_read(lv_indev_drv_t * indev_drv, lv_indev_data_t *data)
{
    if (g_gfx == nullptr) {
        return false;
    }

    M5.update();
    
    if (!M5.Touch.getCount()) {
        data->point = (lv_point_t){ 0, 0 };
        data->state = LV_INDEV_STATE_RELEASED;
        return false;
    }

    auto tp = M5.Touch.getTouchPointRaw(1);
    data->point = (lv_point_t){ tp.x, tp.y };
    data->state = LV_INDEV_STATE_PRESSED;
    return true;
}


void user_lvgl_flush(struct _disp_drv_t * disp_drv, const lv_area_t * area, lv_color_t * color_p)
{
    int w = (area->x2 - area->x1 + 1);
    int h = (area->y2 - area->y1 + 1);
    user_lcd.startWrite();
    user_lcd.setAddrWindow(area->x1, area->y1, w, h);
    user_lcd.writePixels((lgfx::rgb565_t *)&color_p->full, w * h);
    user_lcd.endWrite();
    lv_disp_flush_ready((lv_disp_drv_t*)disp_drv);
}
#endif 

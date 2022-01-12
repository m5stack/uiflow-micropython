/*----------------------------------------------------------------------------/
  Lovyan GFX - Graphics library for embedded devices.

Original Source:
 https://github.com/lovyan03/LovyanGFX/

Licence:
 [FreeBSD](https://github.com/lovyan03/LovyanGFX/blob/master/license.txt)

Author:
 [lovyan03](https://twitter.com/lovyan03)

Contributors:
 [ciniml](https://github.com/ciniml)
 [mongonta0716](https://github.com/mongonta0716)
 [tobozo](https://github.com/tobozo)
/----------------------------------------------------------------------------*/
#pragma once

#include "../../panel/Panel_Device.hpp"

#if defined ( STM32F4xx )
  #include "stm32f4xx.h"
  #include "stm32f4xx_hal.h"
  #include "stm32f4xx_hal_ltdc.h"
#elif defined ( STM32F7xx )
  #include "stm32f7xx.h"
  #include "stm32f7xx_hal.h"
  #include "stm32f7xx_hal_ltdc.h"
#elif defined ( STM32H7xx )
  #include "stm32h7xx.h"
  #include "stm32h7xx_hal.h"
  #include "stm32h7xx_hal_ltdc.h"
#elif defined ( STM32L4xx )
  #include "stm32l4xx.h"
  #include "stm32l4xx_hal.h"
  #include "stm32l4xx_hal_ltdc.h"
#endif

namespace lgfx
{
 inline namespace v1
 {
//----------------------------------------------------------------------------

  struct Panel_LTDC : public Panel_Device
  {
  public:
    bool init(bool use_reset) override;
    void beginTransaction(void) override;
    void endTransaction(void) override;

    color_depth_t setColorDepth(color_depth_t depth) override;
    void setRotation(uint_fast8_t r) override;
    void setInvert(bool invert) override;
    void setSleep(bool flg) override;
    void setPowerSave(bool flg) override;

    void waitDisplay(void) override {}
    bool displayBusy(void) override { return false; }

    void writePixels(pixelcopy_t* param, uint32_t len, bool use_dma) override;
    void writeBlock(uint32_t rawcolor, uint32_t len) override;

    void setWindow(uint_fast16_t xs, uint_fast16_t ys, uint_fast16_t xe, uint_fast16_t ye) override;
    void drawPixelPreclipped(uint_fast16_t x, uint_fast16_t y, uint32_t rawcolor) override;
    void writeFillRectPreclipped(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, uint32_t rawcolor) override;
    void writeImage(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, pixelcopy_t* param, bool use_dma) override;

    uint32_t readCommand(uint_fast8_t cmd, uint_fast8_t index, uint_fast8_t len) override;
    uint32_t readData(uint_fast8_t index, uint_fast8_t len) override;
    void readRect(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, void* dst, pixelcopy_t* param) override;

  protected:

    struct LTDCSettings {
      uint16_t width;
      uint16_t height;
      uint16_t horizontalSync;
      uint16_t horizontalFrontPorch;
      uint16_t horizontalBackPorch;
      uint16_t verticalSync;
      uint16_t verticalFrontPorch;
      uint16_t verticalBackPorch;
    };
    LTDCSettings settings;
    LTDC_HandleTypeDef  hLtdcHandler;
    uint16_t *buffer;

    void begin_transaction(void);
    void end_transaction(void);
  };

//----------------------------------------------------------------------------
 }
}

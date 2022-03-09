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
#if defined (STM32F2xx) || defined (STM32F4xx) || defined (STM32F7xx)

#include "Panel_LTDC.hpp"
#include "../common.hpp"
#include "../../misc/pixelcopy.hpp"

namespace lgfx
{
 inline namespace v1
 {
//----------------------------------------------------------------------------

  bool Panel_LTDC::init(bool use_reset)
  {
    if (!Panel_Device::init(use_reset))
    {
      return false;
    }

    hLtdcHandler.Init.HorizontalSync = (settings.horizontalSync - 1);
    hLtdcHandler.Init.VerticalSync = (settings.verticalSync - 1);
    hLtdcHandler.Init.AccumulatedHBP = (settings.horizontalSync + settings.horizontalBackPorch - 1);
    hLtdcHandler.Init.AccumulatedVBP = (settings.verticalSync + settings.verticalBackPorch - 1);
    hLtdcHandler.Init.AccumulatedActiveH = (settings.height + settings.verticalSync + settings.verticalBackPorch - 1);
    hLtdcHandler.Init.AccumulatedActiveW = (settings.width + settings.horizontalSync + settings.horizontalBackPorch - 1);
    hLtdcHandler.Init.TotalHeigh = (settings.height + settings.verticalSync + settings.verticalBackPorch + settings.verticalFrontPorch - 1);
    hLtdcHandler.Init.TotalWidth = (settings.width + settings.horizontalSync + settings.horizontalBackPorch + settings.horizontalFrontPorch - 1);

    /* LCD clock configuration */

    /* Initialize the LCD pixel width and pixel height */
    hLtdcHandler.LayerCfg->ImageWidth  = settings.width;
    hLtdcHandler.LayerCfg->ImageHeight = settings.height;

    /* Background value */
    hLtdcHandler.Init.Backcolor.Blue = 0;
    hLtdcHandler.Init.Backcolor.Green = 0;
    hLtdcHandler.Init.Backcolor.Red = 0;

    /* Polarity */
    hLtdcHandler.Init.HSPolarity = LTDC_HSPOLARITY_AL;
    hLtdcHandler.Init.VSPolarity = LTDC_VSPOLARITY_AL;
    hLtdcHandler.Init.DEPolarity = LTDC_DEPOLARITY_AL;
    hLtdcHandler.Init.PCPolarity = LTDC_PCPOLARITY_IPC;
    hLtdcHandler.Instance = LTDC;

    __HAL_RCC_LTDC_CLK_ENABLE();

    // init();
//////////////////////////////////////////
    {
      static RCC_PeriphCLKInitTypeDef  periph_clk_init_struct;
      periph_clk_init_struct.PeriphClockSelection = RCC_PERIPHCLK_LTDC;
      periph_clk_init_struct.PLLSAI.PLLSAIN = 192;
      periph_clk_init_struct.PLLSAI.PLLSAIR = 5;
      periph_clk_init_struct.PLLSAIDivR = RCC_PLLSAIDIVR_4;
      HAL_RCCEx_PeriphCLKConfig(&periph_clk_init_struct);


      GPIO_InitTypeDef gpio_init_structure;

      /* Enable GPIOs clock */
      __HAL_RCC_GPIOE_CLK_ENABLE();
      __HAL_RCC_GPIOG_CLK_ENABLE();
      __HAL_RCC_GPIOI_CLK_ENABLE();
      __HAL_RCC_GPIOJ_CLK_ENABLE();
      __HAL_RCC_GPIOK_CLK_ENABLE();

      /*** LTDC Pins configuration ***/
      /* GPIOE configuration */
      gpio_init_structure.Pin       = GPIO_PIN_4;
      gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
      gpio_init_structure.Pull      = GPIO_NOPULL;
      gpio_init_structure.Speed     = GPIO_SPEED_FAST;
      gpio_init_structure.Alternate = GPIO_AF14_LTDC;
      HAL_GPIO_Init(GPIOE, &gpio_init_structure);

      /* GPIOG configuration */
      gpio_init_structure.Pin       = GPIO_PIN_12;
      gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
      gpio_init_structure.Alternate = GPIO_AF9_LTDC;
      HAL_GPIO_Init(GPIOG, &gpio_init_structure);

      /* GPIOI LTDC alternate configuration */
      gpio_init_structure.Pin       = GPIO_PIN_9 | GPIO_PIN_10 | \
                                    GPIO_PIN_13 | GPIO_PIN_14 | GPIO_PIN_15;
      gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
      gpio_init_structure.Alternate = GPIO_AF14_LTDC;
      HAL_GPIO_Init(GPIOI, &gpio_init_structure);

      /* GPIOJ configuration */
      gpio_init_structure.Pin       = GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_3 | \
                                    GPIO_PIN_4 | GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7 | \
                                    GPIO_PIN_8 | GPIO_PIN_9 | GPIO_PIN_10 | GPIO_PIN_11 | \
                                    GPIO_PIN_13 | GPIO_PIN_14 | GPIO_PIN_15;
      gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
      gpio_init_structure.Alternate = GPIO_AF14_LTDC;
      HAL_GPIO_Init(GPIOJ, &gpio_init_structure);

      /* GPIOK configuration */
      gpio_init_structure.Pin       = GPIO_PIN_0 | GPIO_PIN_1 | GPIO_PIN_2 | GPIO_PIN_4 | \
                                    GPIO_PIN_5 | GPIO_PIN_6 | GPIO_PIN_7;
      gpio_init_structure.Mode      = GPIO_MODE_AF_PP;
      gpio_init_structure.Alternate = GPIO_AF14_LTDC;
      HAL_GPIO_Init(GPIOK, &gpio_init_structure);

      // Display enable
      pinMode(PI12, pin_mode_t::output);
      gpio_hi(PI12);

      // Backlight enable
      pinMode(PK3, pin_mode_t::output);
      gpio_hi(PK3);
    }

//////////////////////////////////////////

    HAL_LTDC_Init(&hLtdcHandler);

    LTDC_LayerCfgTypeDef  layer_cfg;

    /* Layer Init */
    layer_cfg.WindowX0 = 0;
    layer_cfg.WindowX1 = settings.width;
    layer_cfg.WindowY0 = 0;
    layer_cfg.WindowY1 = settings.height;
    layer_cfg.PixelFormat = LTDC_PIXEL_FORMAT_RGB565;
    layer_cfg.FBStartAdress = (uint32_t)buffer;
    layer_cfg.Alpha = 255;
    layer_cfg.Alpha0 = 0;
    layer_cfg.Backcolor.Blue = 0;
    layer_cfg.Backcolor.Green = 0;
    layer_cfg.Backcolor.Red = 0;
    layer_cfg.BlendingFactor1 = LTDC_BLENDING_FACTOR1_PAxCA;
    layer_cfg.BlendingFactor2 = LTDC_BLENDING_FACTOR2_PAxCA;
    layer_cfg.ImageWidth = settings.width;
    layer_cfg.ImageHeight = settings.height;

    HAL_LTDC_ConfigLayer(&hLtdcHandler, &layer_cfg, 0);


    return true;
  }

  void Panel_LTDC::beginTransaction(void)
  {
    begin_transaction();
  }
  void Panel_LTDC::begin_transaction(void)
  {
  }

  void Panel_LTDC::endTransaction(void)
  {
  }
  void Panel_LTDC::end_transaction(void)
  {
  }

  void Panel_LTDC::setInvert(bool invert)
  {
    _invert = invert;
  }

  void Panel_LTDC::setSleep(bool flg)
  {
    startWrite();
  }

  void Panel_LTDC::setPowerSave(bool flg)
  {
    startWrite();
  }

  color_depth_t Panel_LTDC::setColorDepth(color_depth_t depth)
  {
    _write_depth = rgb565_2Byte;
    _read_depth  = rgb565_2Byte;
    return rgb565_2Byte;
  }
  void Panel_LTDC::setRotation(uint_fast8_t r)
  {
    r &= 7;
    _rotation = r;
    // offset_rotationを加算 (0~3:回転方向、 4:上下反転フラグ);
    _internal_rotation = ((r + _cfg.offset_rotation) & 3) | ((r & 4) ^ (_cfg.offset_rotation & 4));

  }

  uint32_t Panel_LTDC::readCommand(uint_fast8_t cmd, uint_fast8_t index, uint_fast8_t len)
  {
    return 0;
  }

  uint32_t Panel_LTDC::readData(uint_fast8_t index, uint_fast8_t len)
  {
    return 0;
  }

  void Panel_LTDC::setWindow(uint_fast16_t xs, uint_fast16_t ys, uint_fast16_t xe, uint_fast16_t ye)
  {
  }

  void Panel_LTDC::drawPixelPreclipped(uint_fast16_t x, uint_fast16_t y, uint32_t rawcolor)
  {
  }

  void Panel_LTDC::writeFillRectPreclipped(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, uint32_t rawcolor)
  {
  }

  void Panel_LTDC::writeBlock(uint32_t rawcolor, uint32_t len)
  {
  }

  void Panel_LTDC::writePixels(pixelcopy_t* param, uint32_t len, bool use_dma)
  {
  }

  void Panel_LTDC::writeImage(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, pixelcopy_t* param, bool use_dma)
  {
  }

  void Panel_LTDC::readRect(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, void* dst, pixelcopy_t* param)
  {
  }

//----------------------------------------------------------------------------
 }
}

#endif

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

#include "Panel_LCD.hpp"

namespace lgfx
{
 inline namespace v1
 {
//----------------------------------------------------------------------------

  struct Panel_ILI9331 : public Panel_LCD
  {
    Panel_ILI9331(void)
    {
      _cfg.memory_width  = _cfg.panel_width  = 240;
      _cfg.memory_height = _cfg.panel_height = 320;
    }

    // void setBrightness(uint8_t brightness) override;
    void setInvert(bool invert) override;
    void setSleep(bool flg) override;
    void setPowerSave(bool flg) override;
    void writeCommand(uint32_t data, uint_fast8_t length) override;
    void setWindow(uint_fast16_t xs, uint_fast16_t ys, uint_fast16_t xe, uint_fast16_t ye) override;
    void drawPixelPreclipped(uint_fast16_t x, uint_fast16_t y, uint32_t rawcolor) override;
    void writeFillRectPreclipped(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, uint32_t rawcolor) override;
    color_depth_t setColorDepth(color_depth_t depth) override;

    void setRotation(uint_fast8_t r) override;

  protected:

    void update_madctl(void);
    void set_window(uint_fast16_t xs, uint_fast16_t ys, uint_fast16_t xe, uint_fast16_t ye, uint32_t cmd);

    static constexpr uint8_t CMD_RAMWR = 0x22;

    static constexpr uint8_t CMD_H_ADDR1 = 0x51;
    static constexpr uint8_t CMD_H_ADDR2 = 0x50;
    static constexpr uint8_t CMD_V_ADDR1 = 0x53;
    static constexpr uint8_t CMD_V_ADDR2 = 0x52;
    static constexpr uint8_t CMD_OUTPUT_CTRL = 0x01;
    static constexpr uint8_t CMD_ENTRY_MODE  = 0x03;
    static constexpr uint8_t CMD_POWER_CTRL1 = 0x10;
    static constexpr uint8_t CMD_POWER_CTRL2 = 0x11;
    static constexpr uint8_t CMD_POWER_CTRL3 = 0x12;
    static constexpr uint8_t CMD_POWER_CTRL4 = 0x13;
    static constexpr uint8_t CMD_POWER_CTRL5 = 0x14;
    static constexpr uint8_t CMD_DISPLAY_CTRL1 = 0x07;

    const uint8_t* getInitCommands(uint8_t listno) const override
    {
      static constexpr uint8_t list0[] =
      {
//*
		    0xE7, 2                  , 0x10, 0x14,
		    0x01, 2                  , 0x01, 0x00,
		    0x02, 2                  , 0x02, 0x00,
		    0x08, 2                  , 0x02, 0x02,
		    0x09, 2                  , 0x00, 0x00,
		    0x0A, 2                  , 0x00, 0x00,
		    0x0C, 2                  , 0x00, 0x00,
		    0x0D, 2                  , 0x00, 0x00,
		    0x0F, 2                  , 0x00, 0x00,
		    0x10, 2                  , 0x00, 0x00,
		    0x11, 2                  , 0x00, 0x07,
		    0x12, 2                  , 0x00, 0x00,
		    0x13, 2 + CMD_INIT_DELAY , 0x00, 0x00, 200,
0x10, 2                  , 0x16, 0xF0,
    // 0x10, 2                  , 0x16, 0x90,
		    0x11, 2 + CMD_INIT_DELAY , 0x02, 0x27, 50,

0x12, 2 + CMD_INIT_DELAY , 0x00, 0x0F, 50,
     // 0x12, 2 + CMD_INIT_DELAY , 0x00, 0x0C, 50,

		    0x29, 2                  , 0x00, 0x11,
		    0x2B, 2 + CMD_INIT_DELAY , 0x00, 0x0B, 50,
		    0x30, 2                  , 0x00, 0x00,
		    0x31, 2                  , 0x01, 0x06,
		    0x32, 2                  , 0x00, 0x00,
		    0x35, 2                  , 0x02, 0x04,
		    0x36, 2                  , 0x16, 0x0A,
		    0x37, 2                  , 0x07, 0x07,
		    0x38, 2                  , 0x01, 0x06,
		    0x39, 2                  , 0x07, 0x07,
		    0x3C, 2                  , 0x04, 0x02,
		    0x3D, 2                  , 0x0C, 0x0F,
		    0x60, 2                  , 0x27, 0x00,
		    0x61, 2                  , 0x00, 0x01,
		    0x6A, 2                  , 0x00, 0x00,
		    0x80, 2                  , 0x00, 0x00,
		    0x81, 2                  , 0x00, 0x00,
		    0x82, 2                  , 0x00, 0x00,
		    0x83, 2                  , 0x00, 0x00,
		    0x84, 2                  , 0x00, 0x00,
		    0x85, 2                  , 0x00, 0x00,
		    0x90, 2                  , 0x00, 0x10,
		    0x92, 2                  , 0x06, 0x00,
		    0x07, 2                  , 0x01, 0x33, // 262K color and display ON
/*/
        0x01, 2, 0x01, 0x00,    
        0x02, 2, 0x07, 0x00,    
        0x03, 2, 0x80, 0x20,    
        0x08, 2, 0x03, 0x02,    
        0x09, 2, 0x00, 0x00,   
        0x0A, 2, 0x00, 0x08,    
        //POWER CONTROL REGISTER INITIAL    
        0x10, 2, 0x07, 0x90,    
        0x11, 2, 0x00, 0x05,    
        0x12, 2, 0x00, 0x00,   
        0x13, 2, 0x00, 0x00,    
        //delayms(50, 
        //POWER SUPPPLY STARTUP 1 SETTING    
        0x10, 2, 0x12, 0xB0,    
        // delayms(50,  
        0x11, 2, 0x00, 0x07,    
        //delayms(50,  
        //POWER SUPPLY STARTUP 2 SETTING    
        0x12, 2, 0x00, 0x8C,    
        0x13, 2, 0x17, 0x00,    
        0x29, 2, 0x00, 0x22,    
        // delayms(50,   
        //GAMMA CLUSTER SETTING    
        0x30, 2, 0x00, 0x00,    
        0x31, 2, 0x05, 0x05,    
        0x32, 2, 0x02, 0x05,    
        0x35, 2, 0x02, 0x06,    
        0x36, 2, 0x04, 0x08,    
        0x37, 2, 0x00, 0x00,    
        0x38, 2, 0x05, 0x04,
        0x39, 2, 0x02, 0x06,    
        0x3C, 2, 0x02, 0x06,    
        0x3D, 2, 0x04, 0x08,    
        //-----FRAME RATE SETTING-------//    
        0x60, 2, 0xA7, 0x00,   
        0x61, 2, 0x00, 0x01,   
        0x90, 2, 0x00, 0x33, //RTNI setting
        //-------DISPLAY ON------//    
        0x07, 2, 0x01, 0x33,
//*/
        0xFF,0xFF, // end
      };
      switch (listno)
      {
      case 0: return list0;
      default: return nullptr;
      }
    }

    virtual void setColorDepth_impl(color_depth_t depth) { _write_depth = ((int)depth & color_depth_t::bit_mask) > 16 ? rgb888_3Byte : rgb565_2Byte; _read_depth = rgb888_3Byte; }
  };

//----------------------------------------------------------------------------
 }
}

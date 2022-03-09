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

#include "Panel_Device.hpp"

namespace lgfx
{
 inline namespace v1
 {
//----------------------------------------------------------------------------

  struct Panel_RA8875 : public Panel_Device
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

    void writeCommand(uint32_t, uint_fast8_t) override;
    void writeData(uint32_t, uint_fast8_t) override;

    void waitDisplay(void) override;
    bool displayBusy(void) override;

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

    bool _in_transaction = false;
    uint16_t _colstart = 0;
    uint16_t _rowstart = 0;
    uint32_t _latestcolor = 0;

    const uint8_t* getInitCommands(uint8_t listno) const override
    {
      static constexpr uint8_t list0[] =
      {
        0x88      , 1+CMD_INIT_DELAY, 0x0A, 1, // PLL ini
        0x89      , 1+CMD_INIT_DELAY, 0x02, 1,

        0x10      , 1, 0x0c, //SYSR   bit[4:3]=00 256 color  bit[2:1]=  00 8bit MPU interface    1x 64k color  1x 16bit 						 
        0x04      , 1+CMD_INIT_DELAY, 0x82, 1,    //PCLK
        //0x14      , 1, 0x3b, //HDWR//Horizontal Display Width Setting Bit[6:0]  //Horizontal display width(pixels) = (HDWR + 1)*8       0x27
        0x14      , 1, 0x63, //HDWR//Horizontal Display Width Setting Bit[6:0]  //Horizontal display width(pixels) = (HDWR + 1)*8       0x27
        0x15      , 1, 0x02, //HNDFCR//Horizontal Non-Display Period fine tune Bit[3:0]  //(HNDR + 1)*8 +HNDFCR
        0x16      , 1, 0x03, //HNDR//Horizontal Non-Display Period Bit[4:0] //Horizontal Non-Display Period (pixels) = (HNDR + 1)*8 
        0x17      , 1, 0x01, //HSTR//HSYNC Start Position[4:0]  //HSYNC Start Position(PCLK) = (HSTR + 1)*8 
        0x18      , 1, 0x03, //HPWR//HSYNC Polarity ,The period width of HSYNC.  //HSYNC Width [4:0]   HSYNC Pulse width(PCLK) = (HPWR + 1)*8 

//Vertical set
        0x19      , 1, 0xDF, //VDHR0 //Vertical Display Height Bit [7:0] //Vertical pixels = VDHR + 1	0xef
        0x1a      , 1, 0x01, //VDHR1 //Vertical Display Height Bit [8]  //Vertical pixels = VDHR + 1 	0x00
        0x1b      , 1, 0x0F, //VNDR0 //Vertical Non-Display Period Bit [7:0]  //Vertical Non-Display area = (VNDR + 1) 
        0x1c      , 1, 0x00, //VNDR1 //Vertical Non-Display Period Bit [8] //Vertical Non-Display area = (VNDR + 1) 
        0x1d      , 1, 0x0e, //VSTR0 //VSYNC Start Position[7:0]  //VSYNC Start Position(PCLK) = (VSTR + 1) 
        0x1e      , 1, 0x06, //VSTR1 //VSYNC Start Position[8]  //VSYNC Start Position(PCLK) = (VSTR + 1) 
        0x1f      , 1, 0x01, //VPWR //VSYNC Polarity ,VSYNC Pulse Width[6:0]  //VSYNC Pulse Width(PCLK) = (VPWR + 1) 

        0x8a      , 1, 0x80, //PWM setting
        0x8a      , 1, 0x81, //PWM setting //open PWM
        0x8b      , 1, 0x7F, //Backlight brightness setting //Brightness parameter 0xff-0x00

	      0x01      , 1, 0x80, //display on

        0xFF,0xFF, // end
      };
      switch (listno)
      {
      case 0: return list0;
      default: return nullptr;
      }
    }

    void begin_transaction(void);
    void end_transaction(void);
    uint32_t read_bits(uint_fast8_t bit_index, uint_fast8_t bit_len);

    void write_command(uint32_t data);
    void write_data(uint32_t data);
    void write_bytes(const uint8_t* data, uint32_t len, bool use_dma);
    void set_window(uint_fast16_t xs, uint_fast16_t ys, uint_fast16_t xe, uint_fast16_t ye);
    bool _wait_busy( uint32_t timeout = 1000);

    virtual void update_madctl(void);

    virtual void setColorDepth_impl(color_depth_t depth) { _write_depth = rgb888_3Byte; _read_depth = rgb888_3Byte; }
  };

//----------------------------------------------------------------------------
 }
}

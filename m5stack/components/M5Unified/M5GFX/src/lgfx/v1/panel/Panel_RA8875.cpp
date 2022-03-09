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
#include "Panel_RA8875.hpp"
#include "../Bus.hpp"
#include "../platforms/common.hpp"
#include "../misc/pixelcopy.hpp"

namespace lgfx
{
 inline namespace v1
 {
//----------------------------------------------------------------------------

  bool Panel_RA8875::init(bool use_reset)
  {
    if (!Panel_Device::init(use_reset))
    {
      return false;
    }

    startWrite(true);

    for (uint8_t i = 0; auto cmds = getInitCommands(i); i++)
    {
      command_list(cmds);
    }

    endWrite();

    return true;
  }

  void Panel_RA8875::beginTransaction(void)
  {
    begin_transaction();
  }
  void Panel_RA8875::begin_transaction(void)
  {
    if (_in_transaction) return;
    _in_transaction = true;
    _bus->beginTransaction();
    // cs_control(false);
  }

  void Panel_RA8875::endTransaction(void)
  {
    end_transaction();
  }
  void Panel_RA8875::end_transaction(void)
  {
    if (!_in_transaction) return;
    _in_transaction = false;

    _bus->endTransaction();
    cs_control(true);
  }

  void Panel_RA8875::setInvert(bool invert)
  {
  }

  void Panel_RA8875::setSleep(bool flg)
  {
  }

  void Panel_RA8875::setPowerSave(bool flg)
  {
  }

  color_depth_t Panel_RA8875::setColorDepth(color_depth_t depth)
  {
    depth = rgb888_3Byte;
    setColorDepth_impl(depth);

//    update_madctl();

    return _write_depth;
  }
  void Panel_RA8875::setRotation(uint_fast8_t r)
  {
    r &= 7;
    _rotation = r;
    // offset_rotationを加算 (0~3:回転方向、 4:上下反転フラグ);
    _internal_rotation = ((r + _cfg.offset_rotation) & 3) | ((r & 4) ^ (_cfg.offset_rotation & 4));

    auto ox = _cfg.offset_x;
    auto oy = _cfg.offset_y;
    auto pw = _cfg.panel_width;
    auto ph = _cfg.panel_height;
    auto mw = _cfg.memory_width;
    auto mh = _cfg.memory_height;
    if (_internal_rotation & 1)
    {
      std::swap(ox, oy);
      std::swap(pw, ph);
      std::swap(mw, mh);
    }
    _width  = pw;
    _height = ph;
    _colstart = (_internal_rotation & 2)
              ? mw - (pw + ox) : ox;

    _rowstart = ((1 << _internal_rotation) & 0b10010110) // case 1:2:4:7
              ? mh - (ph + oy) : oy;

    _xs = _xe = _ys = _ye = INT16_MAX;

    update_madctl();
  }

  void Panel_RA8875::update_madctl(void)
  {
    return;

  }

  void Panel_RA8875::waitDisplay(void)
  {
    _wait_busy();
  }

  bool Panel_RA8875::displayBusy(void)
  {
    if (_bus->busy()) return true;
    if (_cfg.pin_busy >= 0 && !lgfx::gpio_in(_cfg.pin_busy)) return true;
    return false;
  }

  bool Panel_RA8875::_wait_busy(uint32_t timeout)
  {
    _bus->wait();
    cs_control(true);
    if (_cfg.pin_busy >= 0 && !lgfx::gpio_in(_cfg.pin_busy))
    {
      auto time = millis();
      do
      {
        if (millis() - time > timeout)
        {
          return false;
        }
      } while (!lgfx::gpio_in(_cfg.pin_busy));
    }
    cs_control(false);
    return true;
  }

  void Panel_RA8875::write_command(uint32_t data)
  {
    data = (data << 8) + 0x80;
    _wait_busy();
    _bus->writeData(data, 16);
  }

  void Panel_RA8875::write_data(uint32_t data)
  {
    data <<= 8;
    _wait_busy();
    _bus->writeData(data, 16);
  }

  void Panel_RA8875::writeCommand(uint32_t cmd, uint_fast8_t)
  {
    write_command(cmd);
  }
  void Panel_RA8875::writeData(uint32_t data, uint_fast8_t)
  {
    write_data(data);
  }

  uint32_t Panel_RA8875::readCommand(uint_fast8_t cmd, uint_fast8_t index, uint_fast8_t len)
  {
    startWrite();
    write_command(cmd);
    index = (index << 3) + _cfg.dummy_read_bits;
    auto res = read_bits(index, len << 3);
    endWrite();
    if (_in_transaction) { cs_control(false); }
    return res;
  }

  uint32_t Panel_RA8875::readData(uint_fast8_t index, uint_fast8_t len)
  {
    startWrite();
    auto res = read_bits(index << 3, len << 3);
    endWrite();
    if (_in_transaction) { cs_control(false); }
    return res;
  }

  uint32_t Panel_RA8875::read_bits(uint_fast8_t bit_index, uint_fast8_t bit_len)
  {
    _bus->beginRead();
    if (bit_index) { _bus->readData(bit_index); } // dummy read
    auto res = _bus->readData(bit_len);
    cs_control(true);
    _bus->endRead();
    return res;
  }

  void Panel_RA8875::setWindow(uint_fast16_t xs, uint_fast16_t ys, uint_fast16_t xe, uint_fast16_t ye)
  {
    set_window(xs, ys, xe, ye);
  }

  void Panel_RA8875::drawPixelPreclipped(uint_fast16_t x, uint_fast16_t y, uint32_t rawcolor)
  {
    bool tr = _in_transaction;
    if (!tr) begin_transaction();

    writeFillRectPreclipped(x, y, 1, 1, rawcolor);

    if (!tr) end_transaction();
  }

  void Panel_RA8875::writeFillRectPreclipped(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, uint32_t rawcolor)
  {
    uint_fast8_t r = _internal_rotation;
    if (r)
    {
      if ((1u << r) & 0b10010110) { y = _height - (y + h); }
      if (r & 2)                  { x = _width  - (x + w); }
      if (r & 1) { std::swap(x, y);  std::swap(w, h); }
    }

    set_window(x, y, x + w - 1, y + h - 1);

    if (_latestcolor != rawcolor)
    {
      _latestcolor = rawcolor;
      write_command(0x60);
      write_data(rawcolor>>3);
      write_command(0x61);
      write_data(rawcolor>>10);
      write_command(0x62);
      write_data(rawcolor>>19);
    }

    write_command(0x8E); //Began to clear the screen (display window)
    write_data(0xC0);
  }

  void Panel_RA8875::writeBlock(uint32_t rawcolor, uint32_t len)
  {
return;
    _bus->writeDataRepeat(rawcolor, _write_bits, len);
    if (_cfg.dlen_16bit && (_write_bits & 15) && (len & 1))
    {
      _has_align_data = !_has_align_data;
    }
  }

  void Panel_RA8875::writePixels(pixelcopy_t* param, uint32_t len, bool use_dma)
  {
return;
    if (param->no_convert)
    {
      _bus->writeBytes(reinterpret_cast<const uint8_t*>(param->src_data), len * _write_bits >> 3, true, use_dma);
    }
    else
    {
      _bus->writePixels(param, len);
    }
    if (_cfg.dlen_16bit && (_write_bits & 15) && (len & 1))
    {
      _has_align_data = !_has_align_data;
    }
  }

  void Panel_RA8875::writeImage(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, pixelcopy_t* param, bool use_dma)
  {
return;
    auto bytes = param->dst_bits >> 3;
    auto src_x = param->src_x;

    if (param->transp == pixelcopy_t::NON_TRANSP)
    {
      if (param->no_convert)
      {
        auto wb = w * bytes;
        uint32_t i = (src_x + param->src_y * param->src_bitwidth) * bytes;
        auto src = &((const uint8_t*)param->src_data)[i];
        setWindow(x, y, x + w - 1, y + h - 1);
        if (param->src_bitwidth == w || h == 1)
        {
          write_bytes(src, wb * h, use_dma);
        }
        else
        {
          auto add = param->src_bitwidth * bytes;
          if (use_dma)
          {
            if (_cfg.dlen_16bit && ((wb * h) & 1))
            {
              _has_align_data = !_has_align_data;
            }
            do
            {
              _bus->addDMAQueue(src, wb);
              src += add;
            } while (--h);
            _bus->execDMAQueue();
          }
          else
          {
            do
            {
              write_bytes(src, wb, false);
              src += add;
            } while (--h);
          }
        }
      }
      else
      {
        if (!_bus->busy())
        {
          static constexpr uint32_t WRITEPIXELS_MAXLEN = 32767;

          setWindow(x, y, x + w - 1, y + h - 1);
          bool nogap = (param->src_bitwidth == w || h == 1);
          if (nogap && (w * h <= WRITEPIXELS_MAXLEN))
          { 
            writePixels(param, w * h, use_dma);
          }
          else
          {
            uint_fast16_t h_step = nogap ? WRITEPIXELS_MAXLEN / w : 1;
            uint_fast16_t h_len = (h_step > 1) ? ((h - 1) % h_step) + 1 : 1;
            writePixels(param, w * h_len, use_dma);
            if (h -= h_len)
            {
              param->src_y += h_len;
              do
              {
                param->src_x = src_x;
                writePixels(param, w * h_step, use_dma);
                param->src_y += h_step;
              } while (h -= h_step);
            }
          }
        }
        else
        {
          size_t wb = w * bytes;
          auto buf = _bus->getDMABuffer(wb);
          param->fp_copy(buf, 0, w, param);
          setWindow(x, y, x + w - 1, y + h - 1);
          write_bytes(buf, wb, true);
          _has_align_data = (_cfg.dlen_16bit && (_write_bits & 15) && (w & h & 1));
          while (--h)
          {
            param->src_x = src_x;
            param->src_y++;
            buf = _bus->getDMABuffer(wb);
            param->fp_copy(buf, 0, w, param);
            write_bytes(buf, wb, true);
          }
        }
      }
    }
    else
    {
      h += y;
      uint32_t wb = w * bytes;
      do
      {
        uint32_t i = 0;
        while (w != (i = param->fp_skip(i, w, param)))
        {
          auto buf = _bus->getDMABuffer(wb);
          int32_t len = param->fp_copy(buf, 0, w - i, param);
          setWindow(x + i, y, x + i + len - 1, y);
          write_bytes(buf, len * bytes, true);
          if (w == (i += len)) break;
        }
        param->src_x = src_x;
        param->src_y++;
      } while (++y != h);
    }
  }

  void Panel_RA8875::write_bytes(const uint8_t* data, uint32_t len, bool use_dma)
  {
    _bus->writeBytes(data, len, true, use_dma);
    if (_cfg.dlen_16bit && (_write_bits & 15) && (len & 1))
    {
      _has_align_data = !_has_align_data;
    }
  }

  void Panel_RA8875::readRect(uint_fast16_t x, uint_fast16_t y, uint_fast16_t w, uint_fast16_t h, void* dst, pixelcopy_t* param)
  {
  }

  void Panel_RA8875::set_window(uint_fast16_t xs, uint_fast16_t ys, uint_fast16_t xe, uint_fast16_t ye)
  {
    xs += _colstart;
    if (_xs != xs)
    {
      _xs = xs;
      write_command(0x30);
      write_data(xs);
      write_command(0x31);
      write_data(xs >> 8);
    }
    ys += _rowstart;
    if (_ys != ys)
    {
      _ys = ys;
      write_command(0x32);
      write_data(ys);
      write_command(0x33);
      write_data(ys >> 8);
    }
    xe += _colstart;
    if (_xe != xe)
    {
      _xe = xe;
      write_command(0x34);
      write_data(xe);
      write_command(0x35);
      write_data(xe >> 8);
    }
    ye += _rowstart;
    if (_ye != ye)
    {
      _ye = ye;
      write_command(0x36);
      write_data(ye);
      write_command(0x37);
      write_data(ye >> 8);
    }
  }

//----------------------------------------------------------------------------
 }
}

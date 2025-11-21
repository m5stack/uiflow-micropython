/*
* SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/
#pragma once

#include "lgfx/v1/platforms/esp32/Bus_I2C.hpp"
#include "lgfx/v1/misc/pixelcopy.hpp"

extern "C" {
#include "py/obj.h"
#include "py/runtime.h"
#include "esp_log.h"
}


class MPY_Bus_I2C: public lgfx::Bus_I2C
{

public:
    struct config_t {
        uint8_t i2c_addr = 0x3C;
        uint32_t prefix_cmd = 0x00;
        uint32_t prefix_data = 0x40;
        uint32_t prefix_len = 1;
        mp_obj_t readfrom_into_method[2];
        mp_obj_t writeto_method[2];
    };

    const config_t& config(void) const { return _cfg; }

    void config(const config_t& config) {
        _cfg = config;
    }

    bool init(void) override {
        _state = state_t::state_none;
        // return lgfx::i2c::init(_cfg.i2c_port, _cfg.pin_sda, _cfg.pin_scl).has_value();
        if (_txbuf == nullptr) {
            _txbuf = (uint8_t *)malloc(sizeof(uint8_t) * _txbuf_size);
        }
        return true;
    }

    void release(void) override {
        // lgfx::i2c::release(_cfg.i2c_port);
        _state = state_t::state_none;
        if (_txbuf) {
            free(_txbuf);
            _txbuf = nullptr;
        }
    }

    void beginTransaction(void) override {
#if 0
        // 既に開始直後の場合は終了;
        if (_state == state_t::state_write_none)
        {
            return;
        }

        if (_state != state_none)
        {
            lgfx::i2c::endTransaction(_cfg.i2c_port);
        }
        lgfx::i2c::beginTransaction(_cfg.i2c_port, _cfg.i2c_addr, _cfg.freq_write, false);
        _state = state_t::state_write_none;
#endif
    }

    void endTransaction(void) override {
        if (_state == state_t::state_none) {
            return ;
        }
        _state = state_t::state_none;
        // lgfx::i2c::endTransaction(_cfg.i2c_port);
    }

    void wait(void) override {
        return ;
    }

    bool busy(void) const override {
        return false;
    }

    void flush(void) override {
        return ;
    }

    bool writeCommand(uint32_t data, uint_fast8_t bit_length) override {
#if 0
        dc_control(false);
        return lgfx::i2c::writeBytes(_cfg.i2c_port, (uint8_t*)&data, (bit_length >> 3)).has_value();
#else
        if (_cfg.prefix_len) {
            memcpy(_txbuf, &_cfg.prefix_cmd, _cfg.prefix_len);
        }
        memcpy(&_txbuf[_cfg.prefix_len], &data, bit_length >> 3);
        return i2c_bus_write(_cfg.i2c_addr, _txbuf, _cfg.prefix_len + (bit_length >> 3));
#endif
    }

    void writeData(uint32_t data, uint_fast8_t bit_length) override {
#if 0
        // dc_control(true);
        // lgfx::i2c::writeBytes(_cfg.i2c_port, (uint8_t*)&data, (bit_length >> 3));
#else
        if (_cfg.prefix_len) {
            memcpy(_txbuf, &_cfg.prefix_data, _cfg.prefix_len);
        }
        memcpy(&_txbuf[_cfg.prefix_len], &data, bit_length >> 3);
        i2c_bus_write(_cfg.i2c_addr, _txbuf, _cfg.prefix_len + (bit_length >> 3));
#endif
    }

    void writeDataRepeat(uint32_t data, uint_fast8_t bit_length, uint32_t length) override {
        // ESP_LOGE("writeDataRepeat", "data=%x, bit_length=%d, length=%d", data, bit_length, length);
#if 0
        // dc_control(true);
        const uint8_t dst_bytes = bit_length >> 3;
        uint32_t buf0 = data | data << bit_length;
        uint32_t buf1;
        uint32_t buf2;
        // make 12Bytes data.
        if (dst_bytes != 3) {
            if (dst_bytes == 1) {
                buf0 |= buf0 << 16;
            }
            buf1 = buf0;
            buf2 = buf0;
        } else {
            buf1 = buf0 >>  8 | buf0 << 16;
            buf2 = buf0 >> 16 | buf0 <<  8;
        }
        uint32_t src[8] = { buf0, buf1, buf2, buf0, buf1, buf2, buf0, buf1 };
        auto buf = reinterpret_cast<uint8_t*>(src);
        if (_cfg.prefix_len) {
            memcpy(_txbuf, &_cfg.prefix_data, _cfg.prefix_len);
        }
        memcpy(&_txbuf[_cfg.prefix_len], src, 32);
        uint32_t limit = 32 / dst_bytes;
        uint32_t len;
        do {
            len = ((length - 1) % limit) + 1;
            // i2c::writeBytes(_cfg.i2c_port, buf, len * dst_bytes);
            i2c_bus_write(_cfg.i2c_addr, _txbuf, _cfg.prefix_len + len * dst_bytes);
        } while (length -= len);
#else
        // 一次性构建完整的重复数据并发送
        const uint8_t dst_bytes = bit_length >> 3;
        if (dst_bytes == 0) { return; }
        size_t total = _cfg.prefix_len + static_cast<size_t>(length) * dst_bytes;
        uint8_t* out = nullptr;
        bool need_free = false;
        if (total <= _txbuf_size && _txbuf) {
            out = _txbuf;
        } else {
            out = static_cast<uint8_t*>(malloc(total));
            if (!out) { return; }
            need_free = true;
        }
        // 写前缀
        if (_cfg.prefix_len) {
            memcpy(out, &_cfg.prefix_data, _cfg.prefix_len);
        }
        // 填充重复数据（按先前语义使用 memcpy(&data, ...)，保持端序一致）
        uint8_t* p = out + _cfg.prefix_len;
        for (uint32_t i = 0; i < length; ++i) {
            memcpy(p + i * dst_bytes, &data, dst_bytes);
        }
        i2c_bus_write(_cfg.i2c_addr, out, total);
        if (need_free) free(out);
#endif
    }

    void writePixels(lgfx::pixelcopy_t* param, uint32_t length) override {
        // ESP_LOGE("writeDataRepeat", "param=%p, bit_length=%d, length=%d", param, length);
#if 0
        // dc_control(true);
        const uint8_t dst_bytes = param->dst_bits >> 3;
        uint32_t limit = 32 / dst_bytes;
        uint32_t len;
        uint8_t buf[32];
        if (_cfg.prefix_len) {
            memcpy(_txbuf, &_cfg.prefix_data, _cfg.prefix_len);
        }
        do {
            len = ((length - 1) % limit) + 1;
            param->fp_copy(buf, 0, len, param);
            memcpy(&_txbuf[_cfg.prefix_len], buf, len * dst_bytes);
            // i2c::writeBytes(_cfg.i2c_port, buf, len * dst_bytes);
            i2c_bus_write(_cfg.i2c_addr, _txbuf, _cfg.prefix_len + len * dst_bytes);
        } while (length -= len);
#else
        // 一次性构建完整的数据并发送
        const uint8_t dst_bytes = param->dst_bits >> 3;
        if (dst_bytes == 0) { return; }
        size_t total = _cfg.prefix_len + static_cast<size_t>(length) * dst_bytes;
        uint8_t* out = nullptr;
        bool need_free = false;
        if (total <= _txbuf_size && _txbuf) {
            out = _txbuf;
        } else {
            out = static_cast<uint8_t*>(malloc(total));
            if (!out) { return; }
            need_free = true;
        }
        // 写前缀
        if (_cfg.prefix_len) {
            memcpy(out, &_cfg.prefix_data, _cfg.prefix_len);
        }
        // 填充像素数据
        uint8_t* p = out + _cfg.prefix_len;
        param->fp_copy(p, 0, length, param);
        i2c_bus_write(_cfg.i2c_addr, out, total);
        if (need_free) free(out);
#endif
    }

    void writeBytes(const uint8_t* data, uint32_t length, bool dc, bool use_dma) override {
#if 0
        dc_control(dc);
        // i2c::writeBytes(_cfg.i2c_port, data, length);
        i2c_bus_write(_cfg.i2c_addr, data, length);
#else
        if (_cfg.prefix_len) {
            if (_txbuf_size > (_cfg.prefix_len + length)) {
                memcpy(&_txbuf[0], (uint8_t*)(dc ? &_cfg.prefix_data : &_cfg.prefix_cmd), _cfg.prefix_len);
                memcpy(&_txbuf[_cfg.prefix_len], data, length);
                i2c_bus_write(_cfg.i2c_addr, _txbuf, _cfg.prefix_len + length);
            } else {
                uint8_t *buf = (uint8_t *)malloc(_cfg.prefix_len + length);
                memcpy(buf, (uint8_t*)(dc ? &_cfg.prefix_data : &_cfg.prefix_cmd), _cfg.prefix_len);
                memcpy(&buf[_cfg.prefix_len], data, length);
                i2c_bus_write(_cfg.i2c_addr, buf, _cfg.prefix_len + length);
                free(buf);
            }
        } else {
            i2c_bus_write(_cfg.i2c_addr, data, length);
        }
#endif
    }

    void beginRead(void) override {
#if 0
        if (_state == state_t::state_read)
        {
            return;
        }
        
        if (_state != state_t::state_none)
        {
            lgfx::i2c::restart(_cfg.i2c_port, _cfg.i2c_addr, _cfg.freq_read, true);
        }
        else
        {
            lgfx::i2c::beginTransaction(_cfg.i2c_port, _cfg.i2c_addr, _cfg.freq_read, true);
        }
        _state = state_t::state_read;
#endif
    }

    void endRead(void) override {
        endTransaction();
    }

    uint32_t readData(uint_fast8_t bit_length) override {
        // ESP_LOGE("readData", "bit_length=%d", bit_length);
        beginRead();
        uint32_t res;
#if 0
        // i2c::readBytes(_cfg.i2c_port, reinterpret_cast<uint8_t*>(&res), bit_length >> 3);
        // return res;
#else
        i2c_bus_read(_cfg.i2c_addr, reinterpret_cast<uint8_t*>(&res), bit_length >> 3);
        return res;
#endif
    }

    bool readBytes(uint8_t* dst, uint32_t length, bool use_dma) override {
        // ESP_LOGE("readBytes", "dst=%p, length=%d, use_dma=%d", dst, length, use_dma);
        return readBytes(dst, length, use_dma, false);
    }

    bool readBytes(uint8_t* dst, uint32_t length, bool use_dma, bool last_nack) override {
        // ESP_LOGE("readBytes", "length=%d, use_dma=%d, last_nack=%d", length, use_dma, last_nack);
#if 0
        beginRead();
        return i2c::readBytes(_cfg.i2c_port, dst, length, last_nack).has_value();
#else
        i2c_bus_read(_cfg.i2c_addr, dst, length);
        return true;
#endif
    }

    void readPixels(void* dst, lgfx::pixelcopy_t* param, uint32_t length) override {
        // ESP_LOGE("readPixels", "param=%p, bit_length=%d, length=%d", param, length);
#if 0
        beginRead();
        const auto bytes = param->src_bits >> 3;
        uint32_t regbuf[8];
        uint32_t limit = 32 / bytes;

        param->src_data = regbuf;
        int32_t dstindex = 0;
        do {
            uint32_t len = (limit > length) ? length : limit;
            length -= len;
            // i2c::readBytes(_cfg.i2c_port, (uint8_t*)regbuf, len * bytes);
            i2c_bus_read(_cfg.i2c_addr, (uint8_t*)regbuf, len * bytes);
            param->src_x = 0;
            dstindex = param->fp_copy(dst, dstindex, dstindex + len, param);
        } while (length);
#else
        // 一次性读取所有像素到连续缓冲区，然后一次性做像素转换拷贝
        beginRead();
        const uint8_t bytes = param->src_bits >> 3;
        if (bytes == 0 || length == 0) { return; }
        size_t total = static_cast<size_t>(length) * bytes;

        uint8_t* buf = nullptr;
        bool need_free = false;
        if (_txbuf && _txbuf_size >= total) {
            buf = _txbuf;          // 复用已分配缓冲
        } else {
            buf = static_cast<uint8_t*>(malloc(total));
            if (!buf) { return; }  // 内存不足，放弃
            need_free = true;
        }

        // 一次性读入
        i2c_bus_read(_cfg.i2c_addr, buf, total);

        // 设置 pixelcopy 源并一次性转换到目标
        param->src_data = buf;
        param->src_x = 0;
        (void)param->fp_copy(dst, 0, length, param);

        if (need_free) { free(buf); }
#endif
    }

protected:
    config_t _cfg;
    // 动态发送缓冲区及容量；init时分配，release释放。
    uint8_t* _txbuf = nullptr;
    size_t _txbuf_size = 256;

    enum state_t
    {
      state_none,
      state_write_none,
      state_write_cmd,
      state_write_data,
      state_read,
    };
    state_t _state = state_none;

    void dc_control(bool dc) {
        // 如果事务处于读取状态，则关闭事务；
        if (_state == state_t::state_read) {
            _state = state_t::state_none;
            // lgfx::i2c::endTransaction(_cfg.i2c_port);
        }

        // 如果传输尚未开始，则开始传输；
        if (_state == state_t::state_none) {
            _state = state_t::state_write_none;
            // lgfx::i2c::beginTransaction(_cfg.i2c_port, _cfg.i2c_addr, _cfg.freq_write, false);
        }

        // 如果没有 DC 前缀，则无需进一步处理；
        if (_cfg.prefix_len == 0) return;

        state_t st = dc ? state_t::state_write_data : state_t::state_write_cmd;
        // 如果已发送的 DC 前缀与请求匹配，则退出；
        if (_state == st) return;

        // 如果 DC 前缀已经发送，则事务将重新进行，因为发送的 DC 前缀与请求不匹配。
        int retry = 3;
        do {
            if (_state != state_t::state_write_none) {
                // lgfx::i2c::endTransaction(_cfg.i2c_port);
                // lgfx::i2c::beginTransaction(_cfg.i2c_port, _cfg.i2c_addr, _cfg.freq_write, false);
            }
            _state = st;
        // } while (lgfx::i2c::writeBytes(_cfg.i2c_port, (uint8_t*)(dc ? &_cfg.prefix_data : &_cfg.prefix_cmd), _cfg.prefix_len).has_error() && --retry);
        } while (i2c_bus_write(_cfg.i2c_addr, (uint8_t*)(dc ? &_cfg.prefix_data : &_cfg.prefix_cmd), _cfg.prefix_len) && --retry);
        if (!retry) { _state = state_none; }
    }

    bool i2c_bus_write(uint8_t addr, const uint8_t *in_data, uint32_t len) {
        mp_obj_t args[2];
        const char *buf;
        size_t l = 0;

        args[0] = mp_obj_new_int(addr);
        args[1] = mp_obj_new_bytes(in_data, len);

        // ESP_LOGE("i2c_bus_write", "addr: 0x%x, len: %d", addr, len);

        mp_obj_t ret = mp_call_method_self_n_kw(
            _cfg.writeto_method[0],
            _cfg.writeto_method[1],
            2,
            0,
            args
            );
        
        return mp_obj_get_int(ret) == len;
    }

    int8_t i2c_bus_read(uint8_t addr, uint8_t *out_data, uint32_t len, bool stop=true) {
        mp_obj_t args[3];
        const char *buf;
        size_t l = 0;

        args[0] = mp_obj_new_int(addr);
        args[1] = mp_obj_new_bytearray(len, out_data);
        args[2] = mp_obj_new_bool(stop);

        // ESP_LOGE("i2c_bus_read", "addr: 0x%x, len: %d", addr, len);

        mp_obj_t ret = mp_call_method_self_n_kw(
            _cfg.readfrom_into_method[0],
            _cfg.readfrom_into_method[1],
            3,
            0,
            args
            );

        return 0;
    }
};

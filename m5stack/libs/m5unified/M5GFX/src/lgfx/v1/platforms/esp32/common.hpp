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

#include "../../misc/DataWrapper.hpp"
#include "../../misc/enum.hpp"
#include "../../../utility/result.hpp"

#include <stdint.h>

#include <freertos/FreeRTOS.h>
#include <freertos/task.h>
#include <driver/gpio.h>
#include <sdkconfig.h>
#include <soc/soc.h>
#include <soc/spi_reg.h>

#if MICROPY_VFS_LFS2
extern "C"
{
#include "extmod/vfs.h"
#include "extmod/vfs_lfs.h"
#include "lib/littlefs/lfs2.h"
typedef struct _mp_obj_vfs_lfs2_t {
    mp_obj_base_t base;
    mp_vfs_blockdev_t blockdev;
    bool enable_mtime;
    vstr_t cur_dir;
    struct lfs2_config config;
    lfs2_t lfs;
} mp_obj_vfs_lfs2_t;

#endif

#if !defined ( REG_SPI_BASE )
//#define REG_SPI_BASE(i) (DR_REG_SPI0_BASE - (i) * 0x1000)
#define REG_SPI_BASE(i)     (DR_REG_SPI2_BASE)
#endif

namespace lgfx
{
 inline namespace v1
 {
//----------------------------------------------------------------------------

  __attribute__ ((unused)) static inline unsigned long millis(void) { return (unsigned long) (esp_timer_get_time() / 1000ULL); }
  __attribute__ ((unused)) static inline unsigned long micros(void) { return (unsigned long) (esp_timer_get_time()); }
  __attribute__ ((unused)) static inline void delayMicroseconds(uint32_t us) { ets_delay_us(us); }
  __attribute__ ((unused)) static inline void delay(uint32_t ms)
  {
    uint32_t time = micros();
    vTaskDelay( std::max<uint32_t>(2u, ms / portTICK_PERIOD_MS) - 1 );
    if (ms != 0 && ms < portTICK_PERIOD_MS*8)
    {
      ms *= 1000;
      time = micros() - time;
      if (time < ms)
      {
        ets_delay_us(ms - time);
      }
    }
  }

  static inline void* heap_alloc(      size_t length) { return heap_caps_malloc(length, MALLOC_CAP_8BIT);  }
  static inline void* heap_alloc_dma(  size_t length) { return heap_caps_malloc((length + 3) & ~3, MALLOC_CAP_DMA);  }
  static inline void* heap_alloc_psram(size_t length) { return heap_caps_malloc(length, MALLOC_CAP_SPIRAM | MALLOC_CAP_8BIT);  }
  static inline void heap_free(void* buf) { heap_caps_free(buf); }

  enum pin_mode_t
  { output
  , input
  , input_pullup
  , input_pulldown
  };

  void pinMode(int_fast16_t pin, pin_mode_t mode);
  inline void lgfxPinMode(int_fast16_t pin, pin_mode_t mode)
  {
    pinMode(pin, mode);
  }

#if defined ( CONFIG_IDF_TARGET_ESP32C3 )
  static inline volatile uint32_t* get_gpio_hi_reg(int_fast8_t pin) { return &GPIO.out_w1ts.val; }
  static inline volatile uint32_t* get_gpio_lo_reg(int_fast8_t pin) { return &GPIO.out_w1tc.val; }
  static inline bool gpio_in(int_fast8_t pin) { return GPIO.in.val & (1 << (pin & 31)); }
#else
  static inline volatile uint32_t* get_gpio_hi_reg(int_fast8_t pin) { return (pin & 32) ? &GPIO.out1_w1ts.val : &GPIO.out_w1ts; }
//static inline volatile uint32_t* get_gpio_hi_reg(int_fast8_t pin) { return (volatile uint32_t*)((pin & 32) ? 0x60004014 : 0x60004008) ; } // workaround Eratta
  static inline volatile uint32_t* get_gpio_lo_reg(int_fast8_t pin) { return (pin & 32) ? &GPIO.out1_w1tc.val : &GPIO.out_w1tc; }
//static inline volatile uint32_t* get_gpio_lo_reg(int_fast8_t pin) { return (volatile uint32_t*)((pin & 32) ? 0x60004018 : 0x6000400C) ; }
  static inline bool gpio_in(int_fast8_t pin) { return ((pin & 32) ? GPIO.in1.data : GPIO.in) & (1 << (pin & 31)); }
#endif
  static inline void gpio_hi(int_fast8_t pin) { if (pin >= 0) *get_gpio_hi_reg(pin) = 1 << (pin & 31); } // ESP_LOGI("LGFX", "gpio_hi: %d", pin); }
  static inline void gpio_lo(int_fast8_t pin) { if (pin >= 0) *get_gpio_lo_reg(pin) = 1 << (pin & 31); } // ESP_LOGI("LGFX", "gpio_lo: %d", pin); }

  uint32_t getApbFrequency(void);
  uint32_t FreqToClockDiv(uint32_t fapb, uint32_t hz);

  // esp_efuse_get_pkg_ver
  uint32_t get_pkg_ver(void);

//----------------------------------------------------------------------------

#if defined (ARDUINO)
 #if defined (FS_H)

  struct FileWrapper : public DataWrapper
  {
private:
#if defined (_SPIFFS_H_)
    bool _check_need_transaction(void) const { return _fs != &SPIFFS; }
#else
    bool _check_need_transaction(void) const { return true; }
#endif

public:
    FileWrapper() : DataWrapper()
    {
#if defined (_SD_H_)
      _fs = &SD;
#elif defined (_SPIFFS_H_)
      _fs = &SPIFFS;
#else
      _fs = nullptr;
#endif
      need_transaction = _check_need_transaction();
      _fp = nullptr;
    }

    fs::FS* _fs;
    fs::File *_fp;
    fs::File _file;

    FileWrapper(fs::FS& fs, fs::File* fp = nullptr) : DataWrapper(), _fs(&fs), _fp(fp) { need_transaction = _check_need_transaction(); }
    void setFS(fs::FS& fs) {
      _fs = &fs;
      need_transaction = _check_need_transaction();
    }

    bool open(fs::FS& fs, const char* path)
    {
      setFS(fs);
      return open(path);
    }
    bool open(const char* path) override
    {
      _file = _fs->open(path, "r");
      _fp = &_file;
      return _file;
    }
    int read(uint8_t *buf, uint32_t len) override { return _fp->read(buf, len); }
    void skip(int32_t offset) override { seek(offset, SeekCur); }
    bool seek(uint32_t offset) override { return seek(offset, SeekSet); }
    bool seek(uint32_t offset, SeekMode mode) { return _fp->seek(offset, mode); }
    void close(void) override { if (_fp) _fp->close(); }
    int32_t tell(void) override { return _fp->position(); }
  };
 #else
  // dummy
  struct FileWrapper : public DataWrapper
  {
    FileWrapper() : DataWrapper()
    {
      need_transaction = true;
    }
    void* _fp;

    template <typename T>
    void setFS(T& fs) {}

    bool open(const char* path, const char* mode) { return false; }
    int read(uint8_t *buf, uint32_t len) override { return false; }
    void skip(int32_t offset) override { }
    bool seek(uint32_t offset) override { return false; }
    bool seek(uint32_t offset, int origin) { return false; }
    void close() override { }
    int32_t tell(void) override { return 0; }
  };

 #endif
#else // ESP-IDF

  struct FileWrapper : public DataWrapper
  {
    FileWrapper() : DataWrapper()
    {
      need_transaction = true;
    }
#ifdef MICROPY_VFS_LFS2
    // Not formatted yet, only for micropython porting
    bool open(const char* path) override {
        const char* full_path;
        struct lfs2_info _finfo;
        mp_vfs_mount_t* _fm = mp_vfs_lookup_path(path, &full_path);
        if (_fm == MP_VFS_NONE || _fm == MP_VFS_ROOT) {
            if (_fm == MP_VFS_NONE) mp_printf(&mp_plat_print, "path not found");
            if (_fm == MP_VFS_ROOT)
                mp_printf(&mp_plat_print, "path is \"\" or \"/\"");
            return false;
        }
        _fp = &((mp_obj_vfs_lfs2_t*)MP_OBJ_TO_PTR(_fm->obj))->lfs;
        enum lfs2_error res = (lfs2_error)lfs2_stat(_fp, full_path, &_finfo);
        if (res != LFS2_ERR_OK) {
            mp_printf(&mp_plat_print, "%s\r\n", strerror(res));
            return false;
        }
        _file = (lfs2_file_t*)malloc(1 * sizeof(lfs2_file_t));
        memset(&_fcfg, 0, sizeof(lfs2_file_config));
        _fcfg.buffer = malloc(_fp->cfg->cache_size * sizeof(uint8_t));
        return ((lfs2_file_opencfg(_fp, _file, full_path,
                                   LFS2_O_RDWR | LFS2_O_CREAT,
                                   &_fcfg) == LFS2_ERR_OK)
                    ? true
                    : false);
    }
    int read(uint8_t* buf, uint32_t len) override {
        return lfs2_file_read(_fp, _file, (char*)buf, len);
    }
    void skip(int32_t offset) override {
        lfs2_file_seek(_fp, _file, offset, LFS2_SEEK_CUR);
    }
    bool seek(uint32_t offset) override {
        return lfs2_file_seek(_fp, _file, offset, LFS2_SEEK_SET);
    }
    bool seek(uint32_t offset, int origin) {
        return lfs2_file_seek(_fp, _file, offset, origin);
    }
    void close() override {
        if (_fp) lfs2_file_close(_fp, _file);
        if (_file) free(_file);
        if (_fcfg.buffer) free(_fcfg.buffer);
    }
    int32_t tell(void) override {
        return lfs2_file_tell(_fp, _file);
    }

   protected:
    lfs2_t* _fp        = nullptr;
    lfs2_file_t* _file = nullptr;
    struct lfs2_file_config _fcfg;
#else
    FILE* _fp;
    bool open(const char* path) override { return (_fp = fopen(path, "r")); }
    int read(uint8_t *buf, uint32_t len) override { return fread((char*)buf, 1, len, _fp); }
    void skip(int32_t offset) override { seek(offset, SEEK_CUR); }
    bool seek(uint32_t offset) override { return seek(offset, SEEK_SET); }
    bool seek(uint32_t offset, int origin) { return fseek(_fp, offset, origin); }
    void close() override { if (_fp) fclose(_fp); }
    int32_t tell(void) override { return ftell(_fp); }
#endif
  };

#endif

//----------------------------------------------------------------------------

  namespace spi
  {
    cpp::result<void, error_t> init(int spi_host, int spi_sclk, int spi_miso, int spi_mosi, int dma_channel);
    void beginTransaction(int spi_host);
  }

//----------------------------------------------------------------------------
 }
}
#ifdef MICROPY_VFS_LFS2
}
#endif

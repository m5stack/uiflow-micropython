#include "lgfx/v1/platforms/device.hpp"
#include "lgfx/v1/panel/Panel_ILI9342.hpp"
#include "lgfx/v1/panel/Panel_ST7735.hpp"
#include "lgfx/v1/panel/Panel_ST7789.hpp"
#include "lgfx/v1/panel/Panel_GC9A01.hpp"
#include "lgfx/v1/panel/Panel_GDEW0154M09.hpp"
#include "lgfx/v1/panel/Panel_IT8951.hpp"
#include "lgfx/v1/touch/Touch_FT5x06.hpp"
#include "lgfx/v1/touch/Touch_GT911.hpp"

class Customers_GFX : public lgfx::LGFX_Device {
    lgfx::Panel_Device* _panel_instance;
    lgfx::Bus_SPI _spi_bus_instance;

   public:
    Customers_GFX(void){

    };

    void setup(uint8_t lcd_type, uint8_t spi_host, int16_t width, int16_t height,
               int16_t offset_x = 0, int16_t offset_y = 0, bool invert = false,
               bool rgb_order = false, uint32_t freq_write = 40,
               uint32_t freq_read = 16, int16_t pin_sclk = -1,
               int16_t pin_mosi = -1, int16_t pin_miso = -1,
               int16_t pin_dc = -1, int16_t pin_cs = -1, int16_t pin_rst = -1,
               int16_t pin_busy = -1) {
        {
            auto cfg = _spi_bus_instance.config();

            cfg.spi_host    = (spi_host_device_t)spi_host;
            cfg.spi_mode    = 0;
            cfg.freq_write  = freq_write * 1000000;
            cfg.freq_read   = freq_read * 1000000;
            cfg.spi_3wire   = true;
            cfg.use_lock    = true;
            cfg.dma_channel = 3;  // AUTO
            cfg.pin_sclk    = pin_sclk;
            cfg.pin_mosi    = pin_mosi;
            cfg.pin_miso    = pin_miso;
            cfg.pin_dc      = pin_dc;

            _spi_bus_instance.config(cfg);
        }
        {
            // TODO:
            switch (lcd_type) {
                case 0: {
                    auto p          = new lgfx::Panel_ILI9342();
                    _panel_instance = p;
                } break;
                case 1: {
                    auto p          = new lgfx::Panel_GC9A01();
                    _panel_instance = p;
                } break;

                default: {
                    auto p          = new lgfx::Panel_ILI9342();
                    _panel_instance = p;
                } break;
            }

            auto cfg = _panel_instance->config();

            cfg.pin_cs   = pin_cs;
            cfg.pin_rst  = pin_rst;
            cfg.pin_busy = pin_busy;

            cfg.panel_width      = width;
            cfg.panel_height     = height;
            cfg.offset_x         = offset_x;
            cfg.offset_y         = offset_y;
            cfg.offset_rotation  = 0;
            cfg.dummy_read_pixel = 8;
            cfg.dummy_read_bits  = 1;
            cfg.readable         = true;
            cfg.invert           = invert;
            cfg.rgb_order        = false;
            cfg.dlen_16bit       = false;
            cfg.bus_shared       = true;

            _panel_instance->setBus(&_spi_bus_instance);
            _panel_instance->config(cfg);
            setPanel(_panel_instance);
        }
    }
};

Customers_GFX user_lcd;

mp_obj_t user_lcd_make_new(const mp_obj_type_t *type, size_t n_args,
                               size_t n_kw, const mp_obj_t *all_args) {
    enum {
        ARG_lcd_type, ARG_spi_host, ARG_width, ARG_height, ARG_offset_x,
        ARG_offset_y, ARG_invert, ARG_rgb_order, ARG_freq_write, ARG_freq_read,
        ARG_pin_sclk, ARG_pin_mosi, ARG_pin_miso, ARG_pin_dc, ARG_pin_cs,
        ARG_pin_rst, ARG_pin_busy};
    /* *FORMAT-OFF* */
    static const mp_arg_t allowed_args[] = {
        { MP_QSTR_lcd_type,   MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_spi_host,   MP_ARG_INT                   , {.u_int = 2 } },
        { MP_QSTR_width,      MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_height,     MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = 0 } },
        { MP_QSTR_offset_x,   MP_ARG_INT                   , {.u_int = 0 } },
        { MP_QSTR_offset_y,   MP_ARG_INT                   , {.u_int = 0 } },
        { MP_QSTR_invert,     MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = mp_const_false } },
        { MP_QSTR_rgb_order,  MP_ARG_BOOL | MP_ARG_REQUIRED, {.u_bool = mp_const_false } },
        { MP_QSTR_freq_write, MP_ARG_INT                   , {.u_int = 40 } },
        { MP_QSTR_freq_read,  MP_ARG_INT                   , {.u_int = 16 } },
        { MP_QSTR_pin_sclk,   MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_pin_mosi,   MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_pin_miso,   MP_ARG_INT                   , {.u_int = -1 } },
        { MP_QSTR_pin_dc,     MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_pin_cs,     MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_pin_rst,    MP_ARG_INT  | MP_ARG_REQUIRED, {.u_int = -1 } },
        { MP_QSTR_pin_busy,   MP_ARG_INT                   , {.u_int = -1 } },
    };
    /* *FORMAT-ON* */
    mp_arg_val_t args[MP_ARRAY_SIZE(allowed_args)];
    mp_arg_parse_all_kw_array(n_args, n_kw, all_args, MP_ARRAY_SIZE(allowed_args), allowed_args, args);

    user_lcd.setup(args[ARG_lcd_type].u_int, args[ARG_spi_host].u_int,
                       args[ARG_width].u_int, args[ARG_height].u_int,
                       args[ARG_offset_x].u_int, args[ARG_offset_y].u_bool,
                       args[ARG_invert].u_bool, args[ARG_rgb_order].u_int,
                       args[ARG_freq_write].u_int, args[ARG_freq_read].u_int,
                       args[ARG_pin_sclk].u_int, args[ARG_pin_mosi].u_int,
                       args[ARG_pin_miso].u_int, args[ARG_pin_dc].u_int,
                       args[ARG_pin_cs].u_int, args[ARG_pin_rst].u_int,
                       args[ARG_pin_busy].u_int);
    user_lcd.init();

    gfx_obj_t *self = mp_obj_malloc(gfx_obj_t, &user_lcd_type);
    self->gfx = &(user_lcd);

    return MP_OBJ_FROM_PTR(self);
}

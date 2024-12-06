#ifndef __FONT_H
#define __FONT_H


#include <stdint.h>

typedef struct {
    int w;
    int h;
    uint8_t data[16];
} glyph_t;

extern const glyph_t font[95];


extern const unsigned char font_ascii_8x16[95];  
extern const uint8_t font_unicode_16x16_start[] asm("_binary_font_unicode_16x16_bin_start");
extern const uint8_t font_unicode_16x16_end[] asm("_binary_font_unicode_16x16_bin_end");

#endif // __FONT_H  



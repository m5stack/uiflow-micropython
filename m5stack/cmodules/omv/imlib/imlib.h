#pragma once

#include "esp_err.h"
#include "esp_log.h"
#include <stdbool.h>
#include "fmath.h"


#ifdef __cplusplus
extern "C" {
#endif



#define IM_LOG2_2(x)             (((x) & 0x2ULL) ? (2) :             1)                                // NO ({ ... }) !
#define IM_LOG2_4(x)             (((x) & 0xCULL) ? (2 + IM_LOG2_2((x) >> 2)) :  IM_LOG2_2(x))          // NO ({ ... }) !
#define IM_LOG2_8(x)             (((x) & 0xF0ULL) ? (4 + IM_LOG2_4((x) >> 4)) :  IM_LOG2_4(x))         // NO ({ ... }) !
#define IM_LOG2_16(x)            (((x) & 0xFF00ULL) ? (8 + IM_LOG2_8((x) >> 8)) :  IM_LOG2_8(x))       // NO ({ ... }) !
#define IM_LOG2_32(x)            (((x) & 0xFFFF0000ULL) ? (16 + IM_LOG2_16((x) >> 16)) : IM_LOG2_16(x)) // NO ({ ... }) !
#define IM_LOG2(x)               (((x) & 0xFFFFFFFF00000000ULL) ? (32 + IM_LOG2_32((x) >> 32)) : IM_LOG2_32(x)) // NO ({ ... }) !

#define IM_IS_SIGNED(a)          (__builtin_types_compatible_p(__typeof__(a), signed) || \
                                  __builtin_types_compatible_p(__typeof__(a), signed long))
#define IM_IS_UNSIGNED(a)        (__builtin_types_compatible_p(__typeof__(a), unsigned) || \
                                  __builtin_types_compatible_p(__typeof__(a), unsigned long))
#define IM_SIGN_COMPARE(a, b)    ((IM_IS_SIGNED(a) && IM_IS_UNSIGNED(b)) || \
                                  (IM_IS_SIGNED(b) && IM_IS_UNSIGNED(a)))

#define IM_MAX(a, b)                                    \
    ({__typeof__ (a) _a = (a); __typeof__ (b) _b = (b); \
      __builtin_choose_expr(IM_SIGN_COMPARE(_a, _b), (void) 0, (_a > _b ? _a : _b)); })

#define IM_MIN(a, b)                                    \
    ({__typeof__ (a) _a = (a); __typeof__ (b) _b = (b); \
      __builtin_choose_expr(IM_SIGN_COMPARE(_a, _b), (void) 0, (_a < _b ? _a : _b)); })

#define IM_CLAMP(x, min, max)    IM_MAX(IM_MIN((x), (max)), (min))

#define IM_DIV(a, b)             ({ __typeof__ (a) _a = (a); __typeof__ (b) _b = (b); _b ? (_a / _b) : 0; })
#define IM_MOD(a, b)             ({ __typeof__ (a) _a = (a); __typeof__ (b) _b = (b); _b ? (_a % _b) : 0; })

#define INT8_T_BITS              (sizeof(int8_t) * 8)
#define INT8_T_MASK              (INT8_T_BITS - 1)
#define INT8_T_SHIFT             IM_LOG2(INT8_T_MASK)

#define INT16_T_BITS             (sizeof(int16_t) * 8)
#define INT16_T_MASK             (INT16_T_BITS - 1)
#define INT16_T_SHIFT            IM_LOG2(INT16_T_MASK)

#define INT32_T_BITS             (sizeof(int32_t) * 8)
#define INT32_T_MASK             (INT32_T_BITS - 1)
#define INT32_T_SHIFT            IM_LOG2(INT32_T_MASK)

#define INT64_T_BITS             (sizeof(int64_t) * 8)
#define INT64_T_MASK             (INT64_T_BITS - 1)
#define INT64_T_SHIFT            IM_LOG2(INT64_T_MASK)

#define UINT8_T_BITS             (sizeof(uint8_t) * 8)
#define UINT8_T_MASK             (UINT8_T_BITS - 1)
#define UINT8_T_SHIFT            IM_LOG2(UINT8_T_MASK)

#define UINT16_T_BITS            (sizeof(uint16_t) * 8)
#define UINT16_T_MASK            (UINT16_T_BITS - 1)
#define UINT16_T_SHIFT           IM_LOG2(UINT16_T_MASK)

#define UINT32_T_BITS            (sizeof(uint32_t) * 8)
#define UINT32_T_MASK            (UINT32_T_BITS - 1)
#define UINT32_T_SHIFT           IM_LOG2(UINT32_T_MASK)

#define UINT64_T_BITS            (sizeof(uint64_t) * 8)
#define UINT64_T_MASK            (UINT64_T_BITS - 1)
#define UINT64_T_SHIFT           IM_LOG2(UINT64_T_MASK)

#define IM_DEG2RAD(x)            (((x) * M_PI) / 180)
#define IM_RAD2DEG(x)            (((x) * 180) / M_PI)


//=======================================================================================
// Point  Stuff  
//=======================================================================================
typedef struct point {
    int16_t x;
    int16_t y;
} point_t;

void point_init(point_t *ptr, int x, int y);
void point_copy(point_t *dst, point_t *src);
bool point_equal_fast(point_t *ptr0, point_t *ptr1);
int point_quadrance(point_t *ptr0, point_t *ptr1);
void point_rotate(int x, int y, float r, int center_x, int center_y, int16_t *new_x, int16_t *new_y);
void point_min_area_rectangle(point_t *corners, point_t *new_corners, int corners_len);


//=======================================================================================
// Line Stuff  
//=======================================================================================
typedef struct line {
    int16_t x1;
    int16_t y1;
    int16_t x2;
    int16_t y2;
} line_t;

bool lb_clip_line(line_t *l, int x, int y, int w, int h);


//=======================================================================================
// Rectangle Stuff  
//=======================================================================================
typedef struct rectangle {
    int16_t x;
    int16_t y;
    int16_t w;
    int16_t h;
} rectangle_t;

typedef struct bounding_box_lnk_data {
    rectangle_t rect;
    float score;
    int label_index;
} bounding_box_lnk_data_t;


//=======================================================================================
// Color Stuff 
//=======================================================================================
typedef struct color_thresholds_list_lnk_data {
    uint8_t LMin, LMax; // or grayscale
    int8_t AMin, AMax;
    int8_t BMin, BMax;
}
color_thresholds_list_lnk_data_t;

#define COLOR_THRESHOLD_BINARY(pixel, threshold, invert)                          \
    ({                                                                            \
        __typeof__ (pixel) _pixel = (pixel);                                      \
        __typeof__ (threshold) _threshold = (threshold);                          \
        __typeof__ (invert) _invert = (invert);                                   \
        ((_threshold->LMin <= _pixel) && (_pixel <= _threshold->LMax)) ^ _invert; \
    })

#define COLOR_THRESHOLD_GRAYSCALE(pixel, threshold, invert)                       \
    ({                                                                            \
        __typeof__ (pixel) _pixel = (pixel);                                      \
        __typeof__ (threshold) _threshold = (threshold);                          \
        __typeof__ (invert) _invert = (invert);                                   \
        ((_threshold->LMin <= _pixel) && (_pixel <= _threshold->LMax)) ^ _invert; \
    })

#define COLOR_THRESHOLD_RGB565(pixel, threshold, invert)                  \
    ({                                                                    \
        __typeof__ (pixel) _pixel = (pixel);                              \
        __typeof__ (threshold) _threshold = (threshold);                  \
        __typeof__ (invert) _invert = (invert);                           \
        uint8_t _l = COLOR_RGB565_TO_L(_pixel);                           \
        int8_t _a = COLOR_RGB565_TO_A(_pixel);                            \
        int8_t _b = COLOR_RGB565_TO_B(_pixel);                            \
        ((_threshold->LMin <= _l) && (_l <= _threshold->LMax) &&          \
         (_threshold->AMin <= _a) && (_a <= _threshold->AMax) &&          \
         (_threshold->BMin <= _b) && (_b <= _threshold->BMax)) ^ _invert; \
    })

#define COLOR_BOUND_BINARY(pixel0, pixel1, threshold)    \
    ({                                                   \
        __typeof__ (pixel0) _pixel0 = (pixel0);          \
        __typeof__ (pixel1) _pixel1 = (pixel1);          \
        __typeof__ (threshold) _threshold = (threshold); \
        (abs(_pixel0 - _pixel1) <= _threshold);          \
    })

#define COLOR_BOUND_GRAYSCALE(pixel0, pixel1, threshold) \
    ({                                                   \
        __typeof__ (pixel0) _pixel0 = (pixel0);          \
        __typeof__ (pixel1) _pixel1 = (pixel1);          \
        __typeof__ (threshold) _threshold = (threshold); \
        (abs(_pixel0 - _pixel1) <= _threshold);          \
    })

#define COLOR_BOUND_RGB565(pixel0, pixel1, threshold)                                                         \
    ({                                                                                                        \
        __typeof__ (pixel0) _pixel0 = (pixel0);                                                               \
        __typeof__ (pixel1) _pixel1 = (pixel1);                                                               \
        __typeof__ (threshold) _threshold = (threshold);                                                      \
        (abs(COLOR_RGB565_TO_R5(_pixel0) - COLOR_RGB565_TO_R5(_pixel1)) <= COLOR_RGB565_TO_R5(_threshold)) && \
        (abs(COLOR_RGB565_TO_G6(_pixel0) - COLOR_RGB565_TO_G6(_pixel1)) <= COLOR_RGB565_TO_G6(_threshold)) && \
        (abs(COLOR_RGB565_TO_B5(_pixel0) - COLOR_RGB565_TO_B5(_pixel1)) <= COLOR_RGB565_TO_B5(_threshold));   \
    })

#define COLOR_BINARY_MIN                        0
#define COLOR_BINARY_MAX                        1
#define COLOR_GRAYSCALE_BINARY_MIN              0x00
#define COLOR_GRAYSCALE_BINARY_MAX              0xFF
#define COLOR_RGB565_BINARY_MIN                 0x0000
#define COLOR_RGB565_BINARY_MAX                 0xFFFF

#define COLOR_GRAYSCALE_MIN                     0
#define COLOR_GRAYSCALE_MAX                     255

#define COLOR_R5_MIN                            0
#define COLOR_R5_MAX                            31
#define COLOR_G6_MIN                            0
#define COLOR_G6_MAX                            63
#define COLOR_B5_MIN                            0
#define COLOR_B5_MAX                            31

#define COLOR_R8_MIN                            0
#define COLOR_R8_MAX                            255
#define COLOR_G8_MIN                            0
#define COLOR_G8_MAX                            255
#define COLOR_B8_MIN                            0
#define COLOR_B8_MAX                            255

#define COLOR_L_MIN                             0
#define COLOR_L_MAX                             100
#define COLOR_A_MIN                             -128
#define COLOR_A_MAX                             127
#define COLOR_B_MIN                             -128
#define COLOR_B_MAX                             127

#define COLOR_Y_MIN                             0
#define COLOR_Y_MAX                             255
#define COLOR_U_MIN                             -128
#define COLOR_U_MAX                             127
#define COLOR_V_MIN                             -128
#define COLOR_V_MAX                             127


//=======================================================================================
// RGB565 Stuff  
//=======================================================================================
#define COLOR_RGB565_TO_R5(pixel)               (((pixel) >> 11) & 0x1F)
#define COLOR_RGB565_TO_R8(pixel)             \
    ({                                        \
        __typeof__ (pixel) __pixel = (pixel); \
        __pixel = (__pixel >> 8) & 0xF8;      \
        __pixel | (__pixel >> 5);             \
    })

#define COLOR_RGB565_TO_G6(pixel)               (((pixel) >> 5) & 0x3F)
#define COLOR_RGB565_TO_G8(pixel)             \
    ({                                        \
        __typeof__ (pixel) __pixel = (pixel); \
        __pixel = (__pixel >> 3) & 0xFC;      \
        __pixel | (__pixel >> 6);             \
    })

#define COLOR_RGB565_TO_B5(pixel)               ((pixel) & 0x1F)
#define COLOR_RGB565_TO_B8(pixel)             \
    ({                                        \
        __typeof__ (pixel) __pixel = (pixel); \
        __pixel = (__pixel << 3) & 0xF8;      \
        __pixel | (__pixel >> 5);             \
    })

#define COLOR_R5_G6_B5_TO_RGB565(r5, g6, b5)    (((r5) << 11) | ((g6) << 5) | (b5))
#define COLOR_R8_G8_B8_TO_RGB565(r8, g8, b8)    ((((r8) & 0xF8) << 8) | (((g8) & 0xFC) << 3) | ((b8) >> 3))

#define COLOR_RGB888_TO_Y(r8, g8, b8)           ((((r8) * 38) + ((g8) * 75) + ((b8) * 15)) >> 7) // 0.299R + 0.587G + 0.114B
#define COLOR_RGB565_TO_Y(rgb565)                \
    ({                                           \
        __typeof__ (rgb565) __rgb565 = (rgb565); \
        int r = COLOR_RGB565_TO_R8(__rgb565);    \
        int g = COLOR_RGB565_TO_G8(__rgb565);    \
        int b = COLOR_RGB565_TO_B8(__rgb565);    \
        COLOR_RGB888_TO_Y(r, g, b);              \
    })

#define COLOR_Y_TO_RGB888(pixel)                ((pixel) * 0x010101)
#define COLOR_Y_TO_RGB565(pixel)                          \
    ({                                                    \
        __typeof__ (pixel) __pixel = (pixel);             \
        int __rb_pixel = (__pixel >> 3) & 0x1F;           \
        (__rb_pixel * 0x0801) + ((__pixel << 3) & 0x7E0); \
    })

#define COLOR_RGB888_TO_U(r8, g8, b8)           ((((r8) * -21) - ((g8) * 43) + ((b8) * 64)) >> 7) // -0.168736R - 0.331264G + 0.5B
#define COLOR_RGB565_TO_U(rgb565)                \
    ({                                           \
        __typeof__ (rgb565) __rgb565 = (rgb565); \
        int r = COLOR_RGB565_TO_R8(__rgb565);    \
        int g = COLOR_RGB565_TO_G8(__rgb565);    \
        int b = COLOR_RGB565_TO_B8(__rgb565);    \
        COLOR_RGB888_TO_U(r, g, b);              \
    })

#define COLOR_RGB888_TO_V(r8, g8, b8)           ((((r8) * 64) - ((g8) * 54) - ((b8) * 10)) >> 7) // 0.5R - 0.418688G - 0.081312B
#define COLOR_RGB565_TO_V(rgb565)                \
    ({                                           \
        __typeof__ (rgb565) __rgb565 = (rgb565); \
        int r = COLOR_RGB565_TO_R8(__rgb565);    \
        int g = COLOR_RGB565_TO_G8(__rgb565);    \
        int b = COLOR_RGB565_TO_B8(__rgb565);    \
        COLOR_RGB888_TO_V(r, g, b);              \
    })

extern const int8_t lab_table[196608 / 2];

#ifdef IMLIB_ENABLE_LAB_LUT
#define COLOR_RGB565_TO_L(pixel)                lab_table[((pixel >> 1) * 3) + 0]
#define COLOR_RGB565_TO_A(pixel)                lab_table[((pixel >> 1) * 3) + 1]
#define COLOR_RGB565_TO_B(pixel)                lab_table[((pixel >> 1) * 3) + 2]
#else
#define COLOR_RGB565_TO_L(pixel)                imlib_rgb565_to_l(pixel)
#define COLOR_RGB565_TO_A(pixel)                imlib_rgb565_to_a(pixel)
#define COLOR_RGB565_TO_B(pixel)                imlib_rgb565_to_b(pixel)
#endif

#define COLOR_LAB_TO_RGB565(l, a, b)            imlib_lab_to_rgb(l, a, b)
#define COLOR_YUV_TO_RGB565(y, u, v)            imlib_yuv_to_rgb((y) + 128, u, v)

#define COLOR_BINARY_TO_GRAYSCALE(pixel)        ((pixel) * COLOR_GRAYSCALE_MAX)
#define COLOR_BINARY_TO_RGB565(pixel)           COLOR_YUV_TO_RGB565(((pixel) ? 127 : -128), 0, 0)
#define COLOR_RGB565_TO_BINARY(pixel)           (COLOR_RGB565_TO_Y(pixel) > (((COLOR_Y_MAX - COLOR_Y_MIN) / 2) + COLOR_Y_MIN))
#define COLOR_RGB565_TO_GRAYSCALE(pixel)        COLOR_RGB565_TO_Y(pixel)
#define COLOR_GRAYSCALE_TO_BINARY(pixel)        ((pixel) > \
                                                 (((COLOR_GRAYSCALE_MAX - COLOR_GRAYSCALE_MIN) / 2) + COLOR_GRAYSCALE_MIN))
#define COLOR_GRAYSCALE_TO_RGB565(pixel)        COLOR_YUV_TO_RGB565(((pixel) - 128), 0, 0)

typedef enum {
    COLOR_PALETTE_RAINBOW,
    COLOR_PALETTE_IRONBOW,
    COLOR_PALETTE_DEPTH,
    COLOR_PALETTE_EVT_DARK,
    COLOR_PALETTE_EVT_LIGHT
} color_palette_t;

// Color palette LUTs
extern const uint16_t rainbow_table[256];
extern const uint16_t ironbow_table[256];
extern const uint16_t depth_table[256];
extern const uint16_t evt_dark_table[256];
extern const uint16_t evt_light_table[256];



//=======================================================================================
// Image Stuff 
//=======================================================================================

// Pixel format IDs.
typedef enum {
    OMV_PIXFORMAT_ID_BINARY = 1,
    OMV_PIXFORMAT_ID_GRAY   = 2,
    OMV_PIXFORMAT_ID_RGB565 = 3,
    OMV_PIXFORMAT_ID_BAYER  = 4,
    OMV_PIXFORMAT_ID_YUV422 = 5,
    OMV_PIXFORMAT_ID_JPEG   = 6,
    OMV_PIXFORMAT_ID_PNG    = 7,
    OMV_PIXFORMAT_ID_ARGB8  = 8,
    /* Note: Update OMV_PIXFORMAT_IS_VALID when adding new formats */
} omv_pixformat_id_t;

// Pixel sub-format IDs.
typedef enum {
    SUBFORMAT_ID_GRAY8  = 0,
    SUBFORMAT_ID_GRAY16 = 1,
    SUBFORMAT_ID_BGGR   = 0,     // !!! Note: Make sure bayer sub-formats don't  !!!
    SUBFORMAT_ID_GBRG   = 1,     // !!! overflow the sensor.hw_flags.bayer field !!!
    SUBFORMAT_ID_GRBG   = 2,
    SUBFORMAT_ID_RGGB   = 3,
    SUBFORMAT_ID_YUV422 = 0,
    SUBFORMAT_ID_YVU422 = 1,
    /* Note: Update OMV_PIXFORMAT_IS_VALID when adding new formats */
} subformat_id_t;

// Pixel format Byte Per Pixel.
typedef enum {
    OMV_PIXFORMAT_BPP_BINARY = 0,
    OMV_PIXFORMAT_BPP_GRAY8  = 1,
    OMV_PIXFORMAT_BPP_GRAY16 = 2,
    OMV_PIXFORMAT_BPP_RGB565 = 2,
    OMV_PIXFORMAT_BPP_BAYER  = 1,
    OMV_PIXFORMAT_BPP_YUV422 = 2,
    OMV_PIXFORMAT_BPP_ARGB8  = 4,
    /* Note: Update OMV_PIXFORMAT_IS_VALID when adding new formats */
} omv_pixformat_bpp_t;

// Pixel format flags.
#define OMV_PIXFORMAT_FLAGS_Y          (1 << 28) // YUV format.
#define OMV_PIXFORMAT_FLAGS_M          (1 << 27) // Mutable format.
#define OMV_PIXFORMAT_FLAGS_C          (1 << 26) // Colored format.
#define OMV_PIXFORMAT_FLAGS_J          (1 << 25) // Compressed format (JPEG/PNG).
#define OMV_PIXFORMAT_FLAGS_R          (1 << 24) // RAW/Bayer format.
#define OMV_PIXFORMAT_FLAGS_CY         (OMV_PIXFORMAT_FLAGS_C | OMV_PIXFORMAT_FLAGS_Y)
#define OMV_PIXFORMAT_FLAGS_CM         (OMV_PIXFORMAT_FLAGS_C | OMV_PIXFORMAT_FLAGS_M)
#define OMV_PIXFORMAT_FLAGS_CR         (OMV_PIXFORMAT_FLAGS_C | OMV_PIXFORMAT_FLAGS_R)
#define OMV_PIXFORMAT_FLAGS_CJ         (OMV_PIXFORMAT_FLAGS_C | OMV_PIXFORMAT_FLAGS_J)
#define IMLIB_IMAGE_MAX_SIZE(x)    ((x) & 0xFFFFFFFF)

// *INDENT-OFF*
// Each pixel format encodes flags, pixel format id and bpp as follows:
// 31......29  28  27  26  25  24  23..........16  15...........8  7.............0
// <RESERVED>  YF  MF  CF  JF  RF  <OMV_PIXFORMAT_ID>  <SUBFORMAT_ID>  <BYTES_PER_PIX>
// NOTE: Bit 31-30 must Not be used for omv_pixformat_t to be used as mp_int_t.
typedef enum {
  OMV_PIXFORMAT_INVALID    = (0x00000000U),
  OMV_PIXFORMAT_BINARY     = (OMV_PIXFORMAT_FLAGS_M  | (OMV_PIXFORMAT_ID_BINARY << 16) | (0                   << 8) | OMV_PIXFORMAT_BPP_BINARY ),
  OMV_PIXFORMAT_GRAYSCALE  = (OMV_PIXFORMAT_FLAGS_M  | (OMV_PIXFORMAT_ID_GRAY   << 16) | (SUBFORMAT_ID_GRAY8  << 8) | OMV_PIXFORMAT_BPP_GRAY8  ),
  OMV_PIXFORMAT_RGB565     = (OMV_PIXFORMAT_FLAGS_CM | (OMV_PIXFORMAT_ID_RGB565 << 16) | (0                   << 8) | OMV_PIXFORMAT_BPP_RGB565 ),
  OMV_PIXFORMAT_ARGB8      = (OMV_PIXFORMAT_FLAGS_CM | (OMV_PIXFORMAT_ID_ARGB8  << 16) | (0                   << 8) | OMV_PIXFORMAT_BPP_ARGB8  ),
  OMV_PIXFORMAT_BAYER      = (OMV_PIXFORMAT_FLAGS_CR | (OMV_PIXFORMAT_ID_BAYER  << 16) | (SUBFORMAT_ID_BGGR   << 8) | OMV_PIXFORMAT_BPP_BAYER  ),
  OMV_PIXFORMAT_BAYER_BGGR = (OMV_PIXFORMAT_FLAGS_CR | (OMV_PIXFORMAT_ID_BAYER  << 16) | (SUBFORMAT_ID_BGGR   << 8) | OMV_PIXFORMAT_BPP_BAYER  ),
  OMV_PIXFORMAT_BAYER_GBRG = (OMV_PIXFORMAT_FLAGS_CR | (OMV_PIXFORMAT_ID_BAYER  << 16) | (SUBFORMAT_ID_GBRG   << 8) | OMV_PIXFORMAT_BPP_BAYER  ),
  OMV_PIXFORMAT_BAYER_GRBG = (OMV_PIXFORMAT_FLAGS_CR | (OMV_PIXFORMAT_ID_BAYER  << 16) | (SUBFORMAT_ID_GRBG   << 8) | OMV_PIXFORMAT_BPP_BAYER  ),
  OMV_PIXFORMAT_BAYER_RGGB = (OMV_PIXFORMAT_FLAGS_CR | (OMV_PIXFORMAT_ID_BAYER  << 16) | (SUBFORMAT_ID_RGGB   << 8) | OMV_PIXFORMAT_BPP_BAYER  ),
  OMV_PIXFORMAT_YUV        = (OMV_PIXFORMAT_FLAGS_CY | (OMV_PIXFORMAT_ID_YUV422 << 16) | (SUBFORMAT_ID_YUV422 << 8) | OMV_PIXFORMAT_BPP_YUV422 ),
  OMV_PIXFORMAT_YUV422     = (OMV_PIXFORMAT_FLAGS_CY | (OMV_PIXFORMAT_ID_YUV422 << 16) | (SUBFORMAT_ID_YUV422 << 8) | OMV_PIXFORMAT_BPP_YUV422 ),
  OMV_PIXFORMAT_YVU422     = (OMV_PIXFORMAT_FLAGS_CY | (OMV_PIXFORMAT_ID_YUV422 << 16) | (SUBFORMAT_ID_YVU422 << 8) | OMV_PIXFORMAT_BPP_YUV422 ),
  OMV_PIXFORMAT_JPEG       = (OMV_PIXFORMAT_FLAGS_CJ | (OMV_PIXFORMAT_ID_JPEG   << 16) | (0                   << 8) | 0                    ),
  OMV_PIXFORMAT_PNG        = (OMV_PIXFORMAT_FLAGS_CJ | (OMV_PIXFORMAT_ID_PNG    << 16) | (0                   << 8) | 0                    ),
  OMV_PIXFORMAT_LAST       = (0xFFFFFFFFU),
} omv_pixformat_t;
// *INDENT-ON*


#define OMV_PIXFORMAT_MUTABLE_ANY \
        OMV_PIXFORMAT_BINARY:     \
    case OMV_PIXFORMAT_GRAYSCALE: \
    case OMV_PIXFORMAT_RGB565:    \
    case OMV_PIXFORMAT_ARGB8      \

#define OMV_PIXFORMAT_BAYER_ANY    \
    OMV_PIXFORMAT_BAYER_BGGR:      \
    case OMV_PIXFORMAT_BAYER_GBRG: \
    case OMV_PIXFORMAT_BAYER_GRBG: \
    case OMV_PIXFORMAT_BAYER_RGGB  \

#define OMV_PIXFORMAT_YUV_ANY \
    OMV_PIXFORMAT_YUV422:     \
    case OMV_PIXFORMAT_YVU422 \

#define OMV_PIXFORMAT_COMPRESSED_ANY \
    OMV_PIXFORMAT_JPEG:              \
    case OMV_PIXFORMAT_PNG           \

#define IMLIB_OMV_PIXFORMAT_IS_VALID(x) \
    ((x == OMV_PIXFORMAT_BINARY)        \
     || (x == OMV_PIXFORMAT_GRAYSCALE)  \
     || (x == OMV_PIXFORMAT_RGB565)     \
     || (x == OMV_PIXFORMAT_ARGB8)      \
     || (x == OMV_PIXFORMAT_BAYER_BGGR) \
     || (x == OMV_PIXFORMAT_BAYER_GBRG) \
     || (x == OMV_PIXFORMAT_BAYER_GRBG) \
     || (x == OMV_PIXFORMAT_BAYER_RGGB) \
     || (x == OMV_PIXFORMAT_YUV422)     \
     || (x == OMV_PIXFORMAT_YVU422)     \
     || (x == OMV_PIXFORMAT_JPEG)       \
     || (x == OMV_PIXFORMAT_PNG))       \


#define OMV_PIXFORMAT_STRUCT            \
struct {                            \
  union {                           \
    struct {                        \
        uint32_t bpp            :8; \
        uint32_t subfmt_id      :8; \
        uint32_t pixfmt_id      :8; \
        uint32_t is_bayer       :1; \
        uint32_t is_compressed  :1; \
        uint32_t is_color       :1; \
        uint32_t is_mutable     :1; \
        uint32_t is_yuv         :1; \
        uint32_t /*reserved*/   :3; \
    };                              \
    uint32_t pixfmt;                \
  };                                \
  uint32_t size; /* for compressed images */ \
}

typedef struct image {
    int32_t w;
    int32_t h;
    OMV_PIXFORMAT_STRUCT;
    union {
        uint8_t *pixels;
        uint8_t *data;
    };
} image_t;



#define IMAGE_BINARY_LINE_LEN(image)             (((image)->w + UINT32_T_MASK) >> UINT32_T_SHIFT)
#define IMAGE_BINARY_LINE_LEN_BYTES(image)       (IMAGE_BINARY_LINE_LEN(image) * sizeof(uint32_t))

#define IMAGE_GRAYSCALE_LINE_LEN(image)          ((image)->w)
#define IMAGE_GRAYSCALE_LINE_LEN_BYTES(image)    (IMAGE_GRAYSCALE_LINE_LEN(image) * sizeof(uint8_t))

#define IMAGE_RGB565_LINE_LEN(image)             ((image)->w)
#define IMAGE_RGB565_LINE_LEN_BYTES(image)       (IMAGE_RGB565_LINE_LEN(image) * sizeof(uint16_t))

#define IMAGE_GET_BINARY_PIXEL(image, x, y)                                                                              \
    ({                                                                                                                   \
        __typeof__ (image) _image = (image);                                                                             \
        __typeof__ (x) _x = (x);                                                                                         \
        __typeof__ (y) _y = (y);                                                                                         \
        (((uint32_t *) _image->data)[(((_image->w + UINT32_T_MASK) >> UINT32_T_SHIFT) * _y) + (_x >> UINT32_T_SHIFT)] >> \
         (_x & UINT32_T_MASK)) & 1;                                                                                      \
    })

#define IMAGE_PUT_BINARY_PIXEL(image, x, y, v)                                                                 \
    ({                                                                                                         \
        __typeof__ (image) _image = (image);                                                                   \
        __typeof__ (x) _x = (x);                                                                               \
        __typeof__ (y) _y = (y);                                                                               \
        __typeof__ (v) _v = (v);                                                                               \
        size_t _i = (((_image->w + UINT32_T_MASK) >> UINT32_T_SHIFT) * _y) + (_x >> UINT32_T_SHIFT);           \
        size_t _j = _x & UINT32_T_MASK;                                                                        \
        ((uint32_t *) _image->data)[_i] = (((uint32_t *) _image->data)[_i] & (~(1 << _j))) | ((_v & 1) << _j); \
    })

#define IMAGE_CLEAR_BINARY_PIXEL(image, x, y)                                                                          \
    ({                                                                                                                 \
        __typeof__ (image) _image = (image);                                                                           \
        __typeof__ (x) _x = (x);                                                                                       \
        __typeof__ (y) _y = (y);                                                                                       \
        ((uint32_t *) _image->data)[(((_image->w + UINT32_T_MASK) >>                                                   \
                                      UINT32_T_SHIFT) * _y) + (_x >> UINT32_T_SHIFT)] &= ~(1 << (_x & UINT32_T_MASK)); \
    })

#define IMAGE_SET_BINARY_PIXEL(image, x, y)                                                                                              \
    ({                                                                                                                                   \
        __typeof__ (image) _image = (image);                                                                                             \
        __typeof__ (x) _x = (x);                                                                                                         \
        __typeof__ (y) _y = (y);                                                                                                         \
        ((uint32_t *) _image->data)[(((_image->w + UINT32_T_MASK) >> UINT32_T_SHIFT) * _y) + (_x >> UINT32_T_SHIFT)] |= 1 <<             \
                                                                                                                        (_x &            \
                                                                                                                         UINT32_T_MASK); \
    })

#define IMAGE_GET_GRAYSCALE_PIXEL(image, x, y)             \
    ({                                                     \
        __typeof__ (image) _image = (image);               \
        __typeof__ (x) _x = (x);                           \
        __typeof__ (y) _y = (y);                           \
        ((uint8_t *) _image->data)[(_image->w * _y) + _x]; \
    })

#define IMAGE_PUT_GRAYSCALE_PIXEL(image, x, y, v)               \
    ({                                                          \
        __typeof__ (image) _image = (image);                    \
        __typeof__ (x) _x = (x);                                \
        __typeof__ (y) _y = (y);                                \
        __typeof__ (v) _v = (v);                                \
        ((uint8_t *) _image->data)[(_image->w * _y) + _x] = _v; \
    })

#define IMAGE_GET_RGB565_PIXEL(image, x, y)                 \
    ({                                                      \
        __typeof__ (image) _image = (image);                \
        __typeof__ (x) _x = (x);                            \
        __typeof__ (y) _y = (y);                            \
        ((uint16_t *) _image->data)[(_image->w * _y) + _x]; \
    })

#define IMAGE_PUT_RGB565_PIXEL(image, x, y, v)                   \
    ({                                                           \
        __typeof__ (image) _image = (image);                     \
        __typeof__ (x) _x = (x);                                 \
        __typeof__ (y) _y = (y);                                 \
        __typeof__ (v) _v = (v);                                 \
        ((uint16_t *) _image->data)[(_image->w * _y) + _x] = _v; \
    })

#define IMAGE_GET_YUV_PIXEL(image, x, y)                    \
    ({                                                      \
        __typeof__ (image) _image = (image);                \
        __typeof__ (x) _x = (x);                            \
        __typeof__ (y) _y = (y);                            \
        ((uint16_t *) _image->data)[(_image->w * _y) + _x]; \
    })

#define IMAGE_PUT_YUV_PIXEL(image, x, y, v)                      \
    ({                                                           \
        __typeof__ (image) _image = (image);                     \
        __typeof__ (x) _x = (x);                                 \
        __typeof__ (y) _y = (y);                                 \
        __typeof__ (v) _v = (v);                                 \
        ((uint16_t *) _image->data)[(_image->w * _y) + _x] = _v; \
    })

#define IMAGE_GET_BAYER_PIXEL(image, x, y)                 \
    ({                                                     \
        __typeof__ (image) _image = (image);               \
        __typeof__ (x) _x = (x);                           \
        __typeof__ (y) _y = (y);                           \
        ((uint8_t *) _image->data)[(_image->w * _y) + _x]; \
    })

#define IMAGE_PUT_BAYER_PIXEL(image, x, y, v)                   \
    ({                                                          \
        __typeof__ (image) _image = (image);                    \
        __typeof__ (x) _x = (x);                                \
        __typeof__ (y) _y = (y);                                \
        __typeof__ (v) _v = (v);                                \
        ((uint8_t *) _image->data)[(_image->w * _y) + _x] = _v; \
    })

// Fast Stuff //

#define IMAGE_COMPUTE_BINARY_PIXEL_ROW_PTR(image, y)                                          \
    ({                                                                                        \
        __typeof__ (image) _image = (image);                                                  \
        __typeof__ (y) _y = (y);                                                              \
        ((uint32_t *) _image->data) + (((_image->w + UINT32_T_MASK) >> UINT32_T_SHIFT) * _y); \
    })

#define IMAGE_GET_BINARY_PIXEL_FAST(row_ptr, x)                       \
    ({                                                                \
        __typeof__ (row_ptr) _row_ptr = (row_ptr);                    \
        __typeof__ (x) _x = (x);                                      \
        (_row_ptr[_x >> UINT32_T_SHIFT] >> (_x & UINT32_T_MASK)) & 1; \
    })

#define IMAGE_PUT_BINARY_PIXEL_FAST(row_ptr, x, v)                       \
    ({                                                                   \
        __typeof__ (row_ptr) _row_ptr = (row_ptr);                       \
        __typeof__ (x) _x = (x);                                         \
        __typeof__ (v) _v = (v);                                         \
        size_t _i = _x >> UINT32_T_SHIFT;                                \
        size_t _j = _x & UINT32_T_MASK;                                  \
        _row_ptr[_i] = (_row_ptr[_i] & (~(1 << _j))) | ((_v & 1) << _j); \
    })

#define IMAGE_CLEAR_BINARY_PIXEL_FAST(row_ptr, x)                       \
    ({                                                                  \
        __typeof__ (row_ptr) _row_ptr = (row_ptr);                      \
        __typeof__ (x) _x = (x);                                        \
        _row_ptr[_x >> UINT32_T_SHIFT] &= ~(1 << (_x & UINT32_T_MASK)); \
    })

#define IMAGE_SET_BINARY_PIXEL_FAST(row_ptr, x)                      \
    ({                                                               \
        __typeof__ (row_ptr) _row_ptr = (row_ptr);                   \
        __typeof__ (x) _x = (x);                                     \
        _row_ptr[_x >> UINT32_T_SHIFT] |= 1 << (_x & UINT32_T_MASK); \
    })

#define IMAGE_COMPUTE_GRAYSCALE_PIXEL_ROW_PTR(image, y) \
    ({                                                  \
        __typeof__ (image) _image = (image);            \
        __typeof__ (y) _y = (y);                        \
        ((uint8_t *) _image->data) + (_image->w * _y);  \
    })

#define IMAGE_GET_GRAYSCALE_PIXEL_FAST(row_ptr, x) \
    ({                                             \
        __typeof__ (row_ptr) _row_ptr = (row_ptr); \
        __typeof__ (x) _x = (x);                   \
        _row_ptr[_x];                              \
    })

#define IMAGE_PUT_GRAYSCALE_PIXEL_FAST(row_ptr, x, v) \
    ({                                                \
        __typeof__ (row_ptr) _row_ptr = (row_ptr);    \
        __typeof__ (x) _x = (x);                      \
        __typeof__ (v) _v = (v);                      \
        _row_ptr[_x] = _v;                            \
    })

#define IMAGE_COMPUTE_RGB565_PIXEL_ROW_PTR(image, y)    \
    ({                                                  \
        __typeof__ (image) _image = (image);            \
        __typeof__ (y) _y = (y);                        \
        ((uint16_t *) _image->data) + (_image->w * _y); \
    })

#define IMAGE_GET_RGB565_PIXEL_FAST(row_ptr, x)    \
    ({                                             \
        __typeof__ (row_ptr) _row_ptr = (row_ptr); \
        __typeof__ (x) _x = (x);                   \
        _row_ptr[_x];                              \
    })

#define IMAGE_PUT_RGB565_PIXEL_FAST(row_ptr, x, v) \
    ({                                             \
        __typeof__ (row_ptr) _row_ptr = (row_ptr); \
        __typeof__ (x) _x = (x);                   \
        __typeof__ (v) _v = (v);                   \
        _row_ptr[_x] = _v;                         \
    })

#define IMAGE_COMPUTE_BAYER_PIXEL_ROW_PTR(image, y)    \
    ({                                                 \
        __typeof__ (image) _image = (image);           \
        __typeof__ (y) _y = (y);                       \
        ((uint8_t *) _image->data) + (_image->w * _y); \
    })

#define IMAGE_COMPUTE_YUV_PIXEL_ROW_PTR(image, y)       \
    ({                                                  \
        __typeof__ (image) _image = (image);            \
        __typeof__ (y) _y = (y);                        \
        ((uint16_t *) _image->data) + (_image->w * _y); \
    })



typedef enum {
    OMV_FRAMESIZE_INVALID = 0,
    // C/SIF Resolutions
    OMV_FRAMESIZE_QQCIF,    // 88x72
    OMV_FRAMESIZE_QCIF,     // 176x144
    OMV_FRAMESIZE_CIF,      // 352x288
    OMV_FRAMESIZE_QQSIF,    // 88x60
    OMV_FRAMESIZE_QSIF,     // 176x120
    OMV_FRAMESIZE_SIF,      // 352x240
    // VGA Resolutions
    OMV_FRAMESIZE_QQQQVGA,  // 40x30
    OMV_FRAMESIZE_QQQVGA,   // 80x60
    OMV_FRAMESIZE_QQVGA,    // 160x120
    OMV_FRAMESIZE_QVGA,     // 320x240
    OMV_FRAMESIZE_VGA,      // 640x480
    OMV_FRAMESIZE_HQQQQVGA, // 30x20
    OMV_FRAMESIZE_HQQQVGA,  // 60x40
    OMV_FRAMESIZE_HQQVGA,   // 120x80
    OMV_FRAMESIZE_HQVGA,    // 240x160
    OMV_FRAMESIZE_HVGA,     // 480x320
    // FFT Resolutions
    OMV_FRAMESIZE_64X32,    // 64x32
    OMV_FRAMESIZE_64X64,    // 64x64
    OMV_FRAMESIZE_128X64,   // 128x64
    OMV_FRAMESIZE_128X128,  // 128x128
    // Himax Resolutions
    OMV_FRAMESIZE_160X160,  // 160x160
    OMV_FRAMESIZE_320X320,  // 320x320
    // Other
    OMV_FRAMESIZE_LCD,      // 128x160
    OMV_FRAMESIZE_QQVGA2,   // 128x160
    OMV_FRAMESIZE_WVGA,     // 720x480
    OMV_FRAMESIZE_WVGA2,    // 752x480
    OMV_FRAMESIZE_SVGA,     // 800x600
    OMV_FRAMESIZE_XGA,      // 1024x768
    OMV_FRAMESIZE_WXGA,     // 1280x768
    OMV_FRAMESIZE_SXGA,     // 1280x1024
    OMV_FRAMESIZE_SXGAM,    // 1280x960
    OMV_FRAMESIZE_UXGA,     // 1600x1200
    OMV_FRAMESIZE_HD,       // 1280x720
    OMV_FRAMESIZE_FHD,      // 1920x1080
    OMV_FRAMESIZE_QHD,      // 2560x1440
    OMV_FRAMESIZE_QXGA,     // 2048x1536
    OMV_FRAMESIZE_WQXGA,    // 2560x1600
    OMV_FRAMESIZE_WQXGA2,   // 2592x1944
} omv_framesize_t;


 
//=======================================================================================
// draw functions  
//=======================================================================================
int imlib_get_pixel(image_t *img, int x, int y);
int imlib_get_pixel_fast(image_t *img, const void *row_ptr, int x);
void imlib_set_pixel(image_t *img, int x, int y, int p);
void imlib_draw_line(image_t *img, int x0, int y0, int x1, int y1, int c, int thickness);
void imlib_draw_rectangle(image_t *img, int rx, int ry, int rw, int rh, int c, int thickness, bool fill);
void imlib_draw_circle(image_t *img, int cx, int cy, int r, int c, int thickness, bool fill);
void imlib_draw_ellipse(image_t *img, int cx, int cy, int rx, int ry, int rotation, int c, int thickness, bool fill);
void imlib_draw_string(image_t *img,
                       int x_off,
                       int y_off,
                       const char *str,
                       int c,
                       float scale,
                       int x_spacing,
                       int y_spacing,
                       bool mono_space,
                       int char_rotation,
                       bool char_hmirror,
                       bool char_vflip,
                       int string_rotation,
                       bool string_hmirror,
                       bool string_hflip);


#ifdef __cplusplus
}
#endif








/*
 * SPDX-License-Identifier: MIT
 *
 * Copyright (C) 2013-2024 OpenMV, LLC.
 * Copyright (c) 2024 M5Stack Technology CO LTD
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 *
 * Basic drawing functions.
 */
#include "imlib.h"
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include "utils.h"
#include "font.h"
#include "fmath.h"
 
 

void *imlib_compute_row_ptr(const image_t *img, int y) {
    switch (img->pixfmt) {
        case OMV_PIXFORMAT_BINARY: {
            return IMAGE_COMPUTE_BINARY_PIXEL_ROW_PTR(img, y);
        }
        case OMV_PIXFORMAT_GRAYSCALE: {
            return IMAGE_COMPUTE_GRAYSCALE_PIXEL_ROW_PTR(img, y);
        }
        case OMV_PIXFORMAT_RGB565: {
            return IMAGE_COMPUTE_RGB565_PIXEL_ROW_PTR(img, y);
        }
        default: {
            // This shouldn't happen, at least we return a valid memory block
            return img->data;
        }
    }
}

inline int imlib_get_pixel_fast(image_t *img, const void *row_ptr, int x) {
    switch (img->pixfmt) {
        case OMV_PIXFORMAT_BINARY: {
            return IMAGE_GET_BINARY_PIXEL_FAST((uint32_t *) row_ptr, x);
        }
        case OMV_PIXFORMAT_GRAYSCALE: {
            return IMAGE_GET_GRAYSCALE_PIXEL_FAST((uint8_t *) row_ptr, x);
        }
        case OMV_PIXFORMAT_RGB565: {
            return IMAGE_GET_RGB565_PIXEL_FAST((uint16_t *) row_ptr, x);
        }
        default: {
            return -1;
        }
    }
}


// Set pixel (handles boundary check and image type check).
void imlib_set_pixel(image_t *img, int x, int y, int p) {
    if ((0 <= x) && (x < img->w) && (0 <= y) && (y < img->h)) {
        switch (img->pixfmt) {
            case OMV_PIXFORMAT_BINARY: {
                IMAGE_PUT_BINARY_PIXEL(img, x, y, p);
                break;
            }
            case OMV_PIXFORMAT_GRAYSCALE: {
                IMAGE_PUT_GRAYSCALE_PIXEL(img, x, y, p);
                break;
            }
            case OMV_PIXFORMAT_RGB565: {
                IMAGE_PUT_RGB565_PIXEL(img, x, y, p);
                break;
            }
            default: {
                break;
            }
        }
    }
}

// https://stackoverflow.com/questions/1201200/fast-algorithm-for-drawing-filled-circles
static void point_fill(image_t *img, int cx, int cy, int r0, int r1, int c) {
    for (int y = r0; y <= r1; y++) {
        for (int x = r0; x <= r1; x++) {
            if (((x * x) + (y * y)) <= (r0 * r0)) {
                imlib_set_pixel(img, cx + x, cy + y, c);
            }
        }
    }
}

static void imlib_set_pixel_aa(image_t *img, int x, int y, int err, int c) {
    if (!((0 <= x) && (x < img->w) && (0 <= y) && (y < img->h))) {
        return;
    }

    switch (img->pixfmt) {
        case OMV_PIXFORMAT_BINARY: {
            uint32_t *ptr = IMAGE_COMPUTE_BINARY_PIXEL_ROW_PTR(img, y);
            int old_c = IMAGE_GET_BINARY_PIXEL_FAST(ptr, x) * 255;
            int new_c = (((old_c * err) + ((c ? 255 : 0) * (256 - err))) >> 8) > 127;
            IMAGE_PUT_BINARY_PIXEL_FAST(ptr, x, new_c);
            break;
        }
        case OMV_PIXFORMAT_GRAYSCALE: {
            uint8_t *ptr = IMAGE_COMPUTE_GRAYSCALE_PIXEL_ROW_PTR(img, y);
            int old_c = IMAGE_GET_GRAYSCALE_PIXEL_FAST(ptr, x);
            int new_c = ((old_c * err) + ((c & 0xff) * (256 - err))) >> 8;
            IMAGE_PUT_GRAYSCALE_PIXEL_FAST(ptr, x, new_c);
            break;
        }
        case OMV_PIXFORMAT_RGB565: {
            uint16_t *ptr = IMAGE_COMPUTE_RGB565_PIXEL_ROW_PTR(img, y);
            int old_c = IMAGE_GET_RGB565_PIXEL_FAST(ptr, x);
            int old_c_r5 = COLOR_RGB565_TO_R5(old_c);
            int old_c_g6 = COLOR_RGB565_TO_G6(old_c);
            int old_c_b5 = COLOR_RGB565_TO_B5(old_c);
            int c_r5 = COLOR_RGB565_TO_R5(c);
            int c_g6 = COLOR_RGB565_TO_G6(c);
            int c_b5 = COLOR_RGB565_TO_B5(c);
            int new_c_r5 = ((old_c_r5 * err) + (c_r5 * (256 - err))) >> 8;
            int new_c_g6 = ((old_c_g6 * err) + (c_g6 * (256 - err))) >> 8;
            int new_c_b5 = ((old_c_b5 * err) + (c_b5 * (256 - err))) >> 8;
            int new_c = COLOR_R5_G6_B5_TO_RGB565(new_c_r5, new_c_g6, new_c_b5);
            IMAGE_PUT_RGB565_PIXEL_FAST(ptr, x, new_c);
            break;
        }
        default: {
            break;
        }
    }
}

// https://gist.github.com/randvoorhies/807ce6e20840ab5314eb7c547899de68#file-bresenham-js-L381
static void imlib_draw_thin_line(image_t *img, int x0, int y0, int x1, int y1, int c) {
    const int dx = abs(x1 - x0);
    const int sx = x0 < x1 ? 1 : -1;
    const int dy = abs(y1 - y0);
    const int sy = y0 < y1 ? 1 : -1;
    int err = dx - dy;
    int e2, x2; // error value e_xy
    int ed = dx + dy == 0 ? 1 : fast_floorf(fast_sqrtf(dx * dx + dy * dy));

    for (;;) {
        // pixel loop
        imlib_set_pixel_aa(img, x0, y0, 256 * abs(err - dx + dy) / ed, c);
        e2 = err;
        x2 = x0;
        if (2 * e2 >= -dx) {
            // x step
            if (x0 == x1) {
                break;
            }
            if (e2 + dy < ed) {
                imlib_set_pixel_aa(img, x0, y0 + sy, 256 * (e2 + dy) / ed, c);
            }
            err -= dy;
            x0 += sx;
        }
        if (2 * e2 <= dy) {
            // y step
            if (y0 == y1) {
                break;
            }
            if (dx - e2 < ed) {
                imlib_set_pixel_aa(img, x2 + sx, y0, 256 * (dx - e2) / ed, c);
            }
            err += dx;
            y0 += sy;
        }
    }
}

// https://rosettacode.org/wiki/Bitmap/Bresenham%27s_line_algorithm#C
void imlib_draw_line(image_t* img, int x0, int y0, int x1, int y1, int color, int thickness) {
    if (thickness > 0) {
        int thickness0 = (thickness - 0) / 2;
        int thickness1 = (thickness - 1) / 2;
        int dx = abs(x1 - x0), sx = (x0 < x1) ? 1 : -1;
        int dy = abs(y1 - y0), sy = (y0 < y1) ? 1 : -1;
        int err = ((dx > dy) ? dx : -dy) / 2;

        for (;;) {
            point_fill(img, x0, y0, -thickness0, thickness1, color);
            if ((x0 == x1) && (y0 == y1)) break;
            int e2 = err;
            if (e2 > -dx) { err -= dy; x0 += sx; }
            if (e2 <  dy) { err += dx; y0 += sy; }
        }
    }    
}

static void xLine(image_t *img, int x1, int x2, int y, int c) {
    while (x1 <= x2) {
        imlib_set_pixel(img, x1++, y, c);
    }
}

static void yLine(image_t *img, int x, int y1, int y2, int c) {
    while (y1 <= y2) {
        imlib_set_pixel(img, x, y1++, c);
    }
}

void imlib_draw_rectangle(image_t *img, int rx, int ry, int rw, int rh, int c, int thickness, bool fill) {
    if (fill) {

        for (int y = ry, yy = ry + rh; y < yy; y++) {
            for (int x = rx, xx = rx + rw; x < xx; x++) {
                imlib_set_pixel(img, x, y, c);
            }
        }

    } else if (thickness > 0) {
        int thickness0 = (thickness - 0) / 2;
        int thickness1 = (thickness - 1) / 2;

        for (int i = rx - thickness0, j = rx + rw + thickness1, k = ry + rh - 1; i < j; i++) {
            yLine(img, i, ry - thickness0, ry + thickness1, c);
            yLine(img, i, k - thickness0, k + thickness1, c);
        }

        for (int i = ry - thickness0, j = ry + rh + thickness1, k = rx + rw - 1; i < j; i++) {
            xLine(img, rx - thickness0, rx + thickness1, i, c);
            xLine(img, k - thickness0, k + thickness1, i, c);
        }
    }
}

// https://stackoverflow.com/questions/27755514/circle-with-thickness-drawing-algorithm
void imlib_draw_circle(image_t* img, int cx, int cy, int radius, int color, int thickness, bool fill) {
    if (fill) {
        point_fill(img, cx, cy, -radius, radius, color);
    } else if (thickness > 0) {
        int thickness0 = (thickness - 0) / 2;
        int thickness1 = (thickness - 1) / 2;

        int xo = radius + thickness0;
        int xi = IM_MAX(radius - thickness1, 0);
        int xi_tmp = xi;
        int y = 0;
        int erro = 1 - xo;
        int erri = 1 - xi;

        while (xo >= y) {
            xLine(img, cx + xi, cx + xo, cy + y,  color);
            yLine(img, cx + y,  cy + xi, cy + xo, color);
            xLine(img, cx - xo, cx - xi, cy + y,  color);
            yLine(img, cx - y,  cy + xi, cy + xo, color);
            xLine(img, cx - xo, cx - xi, cy - y,  color);
            yLine(img, cx - y,  cy - xo, cy - xi, color);
            xLine(img, cx + xi, cx + xo, cy - y,  color);
            yLine(img, cx + y,  cy - xo, cy - xi, color);

            y++;

            if (erro < 0) {
                erro += 2 * y + 1;
            } else {
                xo--;
                erro += 2 * (y - xo + 1);
            }

            if (y > xi_tmp) {
                xi = y;
            } else {
                if (erri < 0) {
                    erri += 2 * y + 1;
                } else {
                    xi--;
                    erri += 2 * (y - xi + 1);
                }
            }
        }
    }   
}

// https://scratch.mit.edu/projects/50039326/
static void scratch_draw_pixel(image_t *img,
                               int x0,
                               int y0,
                               int dx,
                               int dy,
                               float shear_dx,
                               float shear_dy,
                               int r0,
                               int r1,
                               int c) {
    point_fill(img, x0 + dx, y0 + dy + fast_floorf((dx * shear_dy) / shear_dx), r0, r1, c);
}

// https://scratch.mit.edu/projects/50039326/
static void scratch_draw_line(image_t *img, int x0, int y0, int dx, int dy0, int dy1, float shear_dx, float shear_dy, int c) {
    int y = y0 + fast_floorf((dx * shear_dy) / shear_dx);
    yLine(img, x0 + dx, y + dy0, y + dy1, c);
}

// https://scratch.mit.edu/projects/50039326/
static void scratch_draw_sheared_ellipse(image_t *img,
                                         int x0,
                                         int y0,
                                         int width,
                                         int height,
                                         bool filled,
                                         float shear_dx,
                                         float shear_dy,
                                         int c,
                                         int thickness) {
    int thickness0 = (thickness - 0) / 2;
    int thickness1 = (thickness - 1) / 2;
    if (((thickness > 0) || filled) && (shear_dx != 0)) {
        int a_squared = width * width;
        int four_a_squared = a_squared * 4;
        int b_squared = height * height;
        int four_b_squared = b_squared * 4;

        int x = 0;
        int y = height;
        int sigma = (2 * b_squared) + (a_squared * (1 - (2 * height)));

        while ((b_squared * x) <= (a_squared * y)) {
            if (filled) {
                scratch_draw_line(img, x0, y0, x, -y, y, shear_dx, shear_dy, c);
                scratch_draw_line(img, x0, y0, -x, -y, y, shear_dx, shear_dy, c);
            } else {
                scratch_draw_pixel(img, x0, y0, x, y, shear_dx, shear_dy, -thickness0, thickness1, c);
                scratch_draw_pixel(img, x0, y0, -x, y, shear_dx, shear_dy, -thickness0, thickness1, c);
                scratch_draw_pixel(img, x0, y0, x, -y, shear_dx, shear_dy, -thickness0, thickness1, c);
                scratch_draw_pixel(img, x0, y0, -x, -y, shear_dx, shear_dy, -thickness0, thickness1, c);
            }

            if (sigma >= 0) {
                sigma += four_a_squared * (1 - y);
                y -= 1;
            }

            sigma += b_squared * ((4 * x) + 6);
            x += 1;
        }

        x = width;
        y = 0;
        sigma = (2 * a_squared) + (b_squared * (1 - (2 * width)));

        while ((a_squared * y) <= (b_squared * x)) {
            if (filled) {
                scratch_draw_line(img, x0, y0, x, -y, y, shear_dx, shear_dy, c);
                scratch_draw_line(img, x0, y0, -x, -y, y, shear_dx, shear_dy, c);
            } else {
                scratch_draw_pixel(img, x0, y0, x, y, shear_dx, shear_dy, -thickness0, thickness1, c);
                scratch_draw_pixel(img, x0, y0, -x, y, shear_dx, shear_dy, -thickness0, thickness1, c);
                scratch_draw_pixel(img, x0, y0, x, -y, shear_dx, shear_dy, -thickness0, thickness1, c);
                scratch_draw_pixel(img, x0, y0, -x, -y, shear_dx, shear_dy, -thickness0, thickness1, c);
            }

            if (sigma >= 0) {
                sigma += four_b_squared * (1 - x);
                x -= 1;
            }

            sigma += a_squared * ((4 * y) + 6);
            y += 1;
        }
    }
}

// https://scratch.mit.edu/projects/50039326/
static void scratch_draw_rotated_ellipse(image_t *img,
                                         int x,
                                         int y,
                                         int x_axis,
                                         int y_axis,
                                         int rotation,
                                         bool filled,
                                         int c,
                                         int thickness) {
    if ((x_axis > 0) && (y_axis > 0)) {
        if ((x_axis == y_axis) || (rotation == 0)) {
            scratch_draw_sheared_ellipse(img, x, y, x_axis / 2, y_axis / 2, filled, 1, 0, c, thickness);
        } else if (rotation == 90) {
            scratch_draw_sheared_ellipse(img, x, y, y_axis / 2, x_axis / 2, filled, 1, 0, c, thickness);
        } else {

            // Avoid rotations above 90.
            if (rotation > 90) {
                rotation -= 90;
                int temp = x_axis;
                x_axis = y_axis;
                y_axis = temp;
            }

            // Avoid rotations above 45.
            if (rotation > 45) {
                rotation -= 90;
                int temp = x_axis;
                x_axis = y_axis;
                y_axis = temp;
            }

            float theta = fast_atanf(IM_DIV(y_axis, x_axis) * (-tanf(IM_DEG2RAD(rotation))));
            float shear_dx = (x_axis * cosf(theta) * cosf(IM_DEG2RAD(rotation))) -
                             (y_axis * sinf(theta) * sinf(IM_DEG2RAD(rotation)));
            float shear_dy = (x_axis * cosf(theta) * sinf(IM_DEG2RAD(rotation))) +
                             (y_axis * sinf(theta) * cosf(IM_DEG2RAD(rotation)));
            float shear_x_axis = fast_fabsf(shear_dx);
            float shear_y_axis = IM_DIV((y_axis * x_axis), shear_x_axis);
            scratch_draw_sheared_ellipse(img,
                                         x,
                                         y,
                                         fast_floorf(shear_x_axis / 2),
                                         fast_floorf(shear_y_axis / 2),
                                         filled,
                                         shear_dx,
                                         shear_dy,
                                         c,
                                         thickness);
        }
    }
}

void imlib_draw_ellipse(image_t *img, int cx, int cy, int rx, int ry, int rotation, int c, int thickness, bool fill) {
    int r = rotation % 180;
    if (r < 0) {
        r += 180;
    }

    scratch_draw_rotated_ellipse(img, cx, cy, rx * 2, ry * 2, r, fill, c, thickness);
}

// char rotation == 0, 90, 180, 360, etc.
// string rotation == 0, 90, 180, 360, etc.
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
                       bool string_vflip) {
    char_rotation %= 360;
    if (char_rotation < 0) {
        char_rotation += 360;
    }
    char_rotation = (char_rotation / 90) * 90;

    string_rotation %= 360;
    if (string_rotation < 0) {
        string_rotation += 360;
    }
    string_rotation = (string_rotation / 90) * 90;

    bool char_swap_w_h = (char_rotation == 90) || (char_rotation == 270);
    bool char_upsidedown = (char_rotation == 180) || (char_rotation == 270);

    if (string_hmirror) {
        x_off -= fast_floorf(font[0].w * scale) - 1;
    }
    if (string_vflip) {
        y_off -= fast_floorf(font[0].h * scale) - 1;
    }

    int org_x_off = x_off;
    int org_y_off = y_off;
    const int anchor = x_off;

    for (char ch, last = '\0'; (ch = *str); str++, last = ch) {

        if ((last == '\r') && (ch == '\n')) {
            // handle "\r\n" strings
            continue;
        }

        if ((ch == '\n') || (ch == '\r')) {
            // handle '\n' or '\r' strings
            x_off = anchor;
            y_off += (string_vflip ? -1 : +1) * (fast_floorf((char_swap_w_h ? font[0].w : font[0].h) * scale) + y_spacing); // newline height == space height
            continue;
        }

        if ((ch < ' ') || (ch > '~')) {
            // handle unknown characters
            continue;
        }

        const glyph_t *g = &font[ch - ' '];

        if (!mono_space) {
            // Find the first pixel set and offset to that.
            bool exit = false;

            if (!char_swap_w_h) {
                for (int x = 0, xx = g->w; x < xx; x++) {
                    for (int y = 0, yy = g->h; y < yy; y++) {
                        if (g->data[(char_upsidedown ^ char_vflip) ? (g->h - 1 - y) : y] &
                            (1 << ((char_upsidedown ^ char_hmirror ^ string_hmirror) ? x : (g->w - 1 - x)))) {
                            x_off += (string_hmirror ? +1 : -1) * fast_floorf(x * scale);
                            exit = true;
                            break;
                        }
                    }

                    if (exit) {
                        break;
                    }
                }
            } else {
                for (int y = g->h - 1; y >= 0; y--) {
                    for (int x = 0, xx = g->w; x < xx; x++) {
                        if (g->data[(char_upsidedown ^ char_vflip) ? (g->h - 1 - y) : y] &
                            (1 << ((char_upsidedown ^ char_hmirror ^ string_hmirror) ? x : (g->w - 1 - x)))) {
                            x_off += (string_hmirror ? +1 : -1) * fast_floorf((g->h - 1 - y) * scale);
                            exit = true;
                            break;
                        }
                    }

                    if (exit) {
                        break;
                    }
                }
            }
        }

        for (int y = 0, yy = fast_floorf(g->h * scale); y < yy; y++) {
            for (int x = 0, xx = fast_floorf(g->w * scale); x < xx; x++) {
                if (g->data[fast_floorf(y / scale)] & (1 << (g->w - 1 - fast_floorf(x / scale)))) {
                    int16_t x_tmp = x_off + (char_hmirror ? (xx - x - 1) : x), y_tmp = y_off + (char_vflip ? (yy - y - 1) : y);
                    point_rotate(x_tmp, y_tmp, IM_DEG2RAD(char_rotation), x_off + (xx / 2), y_off + (yy / 2), &x_tmp, &y_tmp);
                    point_rotate(x_tmp, y_tmp, IM_DEG2RAD(string_rotation), org_x_off, org_y_off, &x_tmp, &y_tmp);
                    imlib_set_pixel(img, x_tmp, y_tmp, c);
                }
            }
        }

        if (mono_space) {
            x_off += (string_hmirror ? -1 : +1) * (fast_floorf((char_swap_w_h ? g->h : g->w) * scale) + x_spacing);
        } else {
            // Find the last pixel set and offset to that.
            bool exit = false;

            if (!char_swap_w_h) {
                for (int x = g->w - 1; x >= 0; x--) {
                    for (int y = g->h - 1; y >= 0; y--) {
                        if (g->data[(char_upsidedown ^ char_vflip) ? (g->h - 1 - y) : y] &
                            (1 << ((char_upsidedown ^ char_hmirror ^ string_hmirror) ? x : (g->w - 1 - x)))) {
                            x_off += (string_hmirror ? -1 : +1) * (fast_floorf((x + 2) * scale) + x_spacing);
                            exit = true;
                            break;
                        }
                    }

                    if (exit) {
                        break;
                    }
                }
            } else {
                for (int y = 0, yy = g->h; y < yy; y++) {
                    for (int x = g->w - 1; x >= 0; x--) {
                        if (g->data[(char_upsidedown ^ char_vflip) ? (g->h - 1 - y) : y] &
                            (1 << ((char_upsidedown ^ char_hmirror ^ string_hmirror) ? x : (g->w - 1 - x)))) {
                            x_off += (string_hmirror ? -1 : +1) * (fast_floorf(((g->h - 1 - y) + 2) * scale) + x_spacing);
                            exit = true;
                            break;
                        }
                    }

                    if (exit) {
                        break;
                    }
                }
            }

            if (!exit) {
                x_off += (string_hmirror ? -1 : +1) * fast_floorf(scale * 3);        // space char
            }
        }
    }
}




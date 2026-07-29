/**
 * @file      qmath.c
 *
 * @brief     Mathematical helper function implementation
 *
 * @author    Decawave Applications
 *
 * @copyright SPDX-FileCopyrightText: Copyright (c) 2024 Qorvo US, Inc.
 *            SPDX-License-Identifier: LicenseRef-QORVO-2
 *
 */
#include "qmath.h"
#include <stdbool.h>

#define LUT_SIZE                     33U
#define LUT_SIZE_POW_BASE_2          32U
#define LOG_PRECISION                5U
#define LOG2_10_SHIFTED_100TH        109UL
#define DIVIDE_BY_POW2_ROUNDED(x, y) (((uint64_t)(x) + (1ULL << ((uint64_t)(y) - 1ULL))) >> (uint64_t)(y))

/**
 * lut_power_base_2 is a lut that computes ((2 ^ x) multiplied by 4)
 *  - x belongs to [0:1[ with a step of 0.0315.
 *  - There is no need for negative values: any value can be written as
 *    the sum of negative or positive int and a positive fractional parts.
 */
static const uint8_t lut_power_base_2[LUT_SIZE_POW_BASE_2] =
{
    32U, 33U, 33U, 34U, 35U, 36U, 36U, 37U, 38U, 39U, 40U, 41U, 41U, 42U, 43U, 44U,
    45U, 46U, 47U, 48U, 49U, 50U, 52U, 53U, 54U, 55U, 56U, 57U, 59U, 60U, 61U, 63U
};

/**
 * lut_log2 is a lut that computes log2(x) shifted by LUT_LOG_SHIFT
 * with a step for x of 1/(2^LOG_PRECISION).
 */
static const uint16_t lut_log2[LUT_SIZE] =
{
    0U, 1455U, 2866U, 4236U, 5568U, 6863U, 8124U, 9352U, 10549U, 11716U, 12855U, 13968U, 15055U, 16117U, 17156U, 18173U, 19168U,
    20143U, 21098U, 22034U, 22952U, 23852U, 24736U, 25604U, 26455U, 27292U, 28114U, 28922U, 29717U, 30498U, 31267U, 32024U, 32768U
};

/**
 * log2_lut - Compute log2(x).
 * @x: x to convert in log2.
 *
 * Return: Return the log2(x) shifted by LUT_LOG_SHIFT.
 * 	   Results is shifted by LUT_LOG_SHIFT to gain
 * 	   precision and emulate the numbers after the decimal point.
 *
 * Algo here is to write x = y*2^z and to force y to be in the range of ]1,2].
 * Then we can write:
 *      log2(x)=log2(y*(2^z))
 *      log2(x)=log2(y) + log2(2^z)
 *      log2(x)=log2(y) + z
 *
 * To obtain y in the range of ]1,2] we can have it quickly because we know that
 * if we divide x with its msb we will find y.
 * Hence the use of __builtin_clz to find quickly the msb (named z in the algo).
 */

uint32_t log2_lut(uint32_t x)
{
    uint32_t log2_x = 0UL;
    uint64_t x_shifted = 0ULL;
    uint16_t index = 0U, y = 0U, z = 0U, left = 0U;

    if (x == 1UL)
    {
        /* log2(1) = 0.*/
        return 0U;
    }

    /* 31 xor clz(x) is equivalent but faster than 31 - clz(x).*/
    /* warning this is valid only because 31 is in binary 11111b.*/
    /* (31 is the size of uint32_t - 1 in bits) */
    z = 31U - (uint16_t)__builtin_clz(x);
    x_shifted = ((uint64_t)x << LUT_LOG_SHIFT);
    y = (uint16_t)DIVIDE_BY_POW2_ROUNDED(x_shifted, z);
    y -= (uint16_t)1U << LUT_LOG_SHIFT;
    index = y >> (LUT_LOG_SHIFT - LOG_PRECISION);
    left = y - (index << (LUT_LOG_SHIFT - LOG_PRECISION));
    log2_x = (uint32_t)lut_log2[index] + ((uint32_t)z << (uint32_t)LUT_LOG_SHIFT);
    /* A good approximation is to add half the delta to the next index.*/
    /* To be done according to the granularity of the lut table.*/
    if (left >= ((uint16_t)1U << (LUT_LOG_SHIFT - LOG_PRECISION - 2U)))
    {
        log2_x += (((uint32_t)lut_log2[index + 1U] - (uint32_t)lut_log2[index]) >> 1UL);
    }
    return log2_x;
}

/**
 * log10_10 - Compute 10*log10(x).
 * @x: x to convert in 10*log10(x).
 *
 * Return: 10*log(x) in 100th dB
 *
 * log10(x) = log2(x)/log2(10)
 * As function log2_lut returns log2(x) << LUT_LOG_SHIFT we compute log2(10) << LUT_LOG_SHIFT
 * Here log2(10) << LUT_LOG_SHIFT = 1088
 * As we want the result of 10*log10(x) in 100th dB we divide only by 1088/10 = 109
 */
uint16_t log10_10(uint32_t x)
{
    /* log10(0) is not valid hence return an error.*/
    if (x == 0UL)
    {
        return LOG_INVALID_VALUE;
    }

    return (uint16_t)((log2_lut(x) + (LOG2_10_SHIFTED_100TH >> 1UL)) / LOG2_10_SHIFTED_100TH);
}

uint32_t q8_pow_of_base2(int32_t exponent_q18)
{
    uint16_t int_part = 0U;
    uint16_t frac_part = 0U;
    uint32_t r1_q5, r2_q5;
    uint32_t exponent_q5;
    bool isNegative = false;

    exponent_q18 += 4096;

    if(exponent_q18 < 0)
    {
        isNegative = true;
        exponent_q18 *= -1;
    }

    exponent_q5 = (uint32_t)exponent_q18 >> 13UL;
    /* Transform exponent to sum of int and frac parts. */
    int_part = (uint16_t)(exponent_q5 >> 5UL);
    frac_part = (uint16_t)exponent_q5 & 0x1FU;

    if (isNegative)
    {
        r1_q5 = 32UL >> (uint32_t)int_part;
    }
    else
    {
        r1_q5 = 32UL << (uint32_t)int_part;
    }
    /* frac part */
    if (frac_part == 0UL)
    {
        r2_q5 = 32UL;
    }
    else
    {
        r2_q5 = (uint32_t)lut_power_base_2[frac_part];
    }

    return ((r1_q5 * r2_q5) >> 2UL);
}

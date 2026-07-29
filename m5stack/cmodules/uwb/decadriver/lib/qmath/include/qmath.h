/**
 * @file      qmath.h
 *
 * @brief     Mathematical helper function implementation
 *
 * @author    Decawave Applications
 *
 * @copyright SPDX-FileCopyrightText: Copyright (c) 2024 Qorvo US, Inc.
 *            SPDX-License-Identifier: LicenseRef-QORVO-2
 *
 */
#ifndef QMATH_H
#define QMATH_H

#include <stdint.h>

#define LUT_LOG_SHIFT     15U
#define LOG2_10_SHIFTED   10885U
#define LOG_INVALID_VALUE 0xFFFFU

/* Log2(10) 2 ^ 16 / 10. */
#define LOG2_10_DIV_10_Q16 21771

/**
 * log2_lut - Compute log2(x).
 * @x: x to convert in log2.
 *
 * Return: log2(x) shifted by LUT_LOG_SHIFT.
 */
uint32_t log2_lut(uint32_t x);

/**
 * log10_10 - Compute 10*log10(x).
 * @x: x to convert in 10*log10(x).
 *
 * Return: 10*log(x) in 100th dB.
 */
uint16_t log10_10(uint32_t x);

/**
 * q8_pow_of_base2 - Compute 2 ^ exponent_q18.
 * @exponent_q18: fixed point value.
 *
 * Return: 2 ^ exponent_q18.
 */
uint32_t q8_pow_of_base2(int32_t exponent_q18);

#endif /* QMATH_H */

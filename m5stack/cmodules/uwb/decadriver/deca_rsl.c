/**
 * @file:     deca_rsl.c
 * 
 * @brief     This file contains the receive signal strength computations
 *
 * @author    Decawave Applications
 *
 * @copyright SPDX-FileCopyrightText: Copyright (c) 2024 Qorvo US, Inc.
 *            SPDX-License-Identifier: LicenseRef-QORVO-2
 *
 */
#include <stdint.h>
#include <limits.h>
#include "deca_device_api.h"
#include "deca_rsl.h"
#include "qmath.h"

#define ALPHA_IP_PRF_16_Q8   29133    // Constant A for PRF of 16 MHz (Ipatov) 113.8.
#define ALPHA_IP_PRF_64_Q8   31155    // Constant A for PRF of 64 MHz (Ipatov) 121.7.

#define Q8_OFFSET 256UL
#define Q8_SHIFT 8UL

/**
 * rsl_calculate() - Estimate the signal power in dBm
 *
 * @power: power as integer.
 * @n: number of accumulate symbols or STS length.
 * @pow2: power of 2 to be multiplied to @power.
 *
 * Return: estimated signal power as a signed q8.8, with 0.1 dBm of precision,
 *         SHRT_MIN or error (-128.0).
 *
 * References:
 *  [1] DW3000 Family User Manual, sections 4.7.1, 4.7.2, version 1.1
 *  [2] DW3700 User Manual v0.4 sections 4.7.1, 4.7.2, version 0.4
 *
 *   10 * log10(power * 2^pow2 / n²) + 6 * D - A
 *
 * For the signal power in the first path
 *
 *   power = F1² + F2² + F3²
 *   pow2 = 0
 *
 *   F1, the First Path Amplitude (point 1) magnitude value (2 fractional bits).
 *   F2, the First Path Amplitude (point 2) magnitude value (2 fractional bits).
 *   F3, the First Path Amplitude (point 3) magnitude value (2 fractional bits).
 *
 * For the received signal
 *
 *   power = C, pow2 = 21  on the DW3 C0 [1]
 *   power = C, pow2 = 17  on the DW3 D0 and E0 [2]
 *
 *   C, the Channel Impulse Response Power value.
 *
 * Remaining parameters are common.
 *
 *   D, the DGC_DECISION, treated as an unsigned integer in range 0 to 7.
 *      0 when RX_TUNE_EN bit is not set in DGC_CFG (No DGC).
 *
 *   n, the number of preamble symbols accumulated, or accumulated STS length.
 *
 *   A, the constant.
 *      113.8 for a PRF of 16 MHz, or                   [1]
 *      121.7 for a PRF of 64 MHz Ipatov preamble or    [1]
 *      120.7 for a PRF of 64 MHz STS or                [1]
 */
static int16_t rsl_calculate(uint32_t c, uint32_t n, uint32_t pow2, uint8_t dgc_decision, uint8_t rx_pcode, bool is_sts)
{
    /* Algo to simplify the log computation:
     *      log10((power*2^pow2)/(n*n)) = log2((power*2^pow2)/(n*n))/log2(10)
     *      log10((power*2^pow2)/(n*n)) = (log(2^pow2) + log2(power) - log2(n*n))/log2(10)
     *      log10((power*2^pow2)/(n*n)) = (pow2 + log2(power) - 2*log2(n))/log2(10)
     * As function log2_lut returns log2(x) << LUT_LOG_SHIFT we compute log2(10) << LUT_LOG_SHIFT.
     * Here log2(10) << LUT_LOG_SHIFT = 108852.
     * As we want the result of 10*log10(x) in q8.8 format we multiply by 256 and
     * divide by 108852/10 = 10885.
     */
    if (c == 0UL || n == 0UL)
    {
        return (int16_t)SHRT_MIN;
    }
    uint32_t rsl_dbm_q8_u32 = (pow2 << LUT_LOG_SHIFT) + log2_lut(c) - (log2_lut(n) << 1UL);
    rsl_dbm_q8_u32 = (rsl_dbm_q8_u32 * Q8_OFFSET) / LOG2_10_SHIFTED;
    int32_t rsl_dbm_q8 = (int32_t)rsl_dbm_q8_u32;

    /* Computation of the offsets. */
    uint16_t dgc_desision_shifted = ((uint16_t)dgc_decision * 6U) << (uint16_t)Q8_SHIFT;
    int32_t dgc_decision_q8 = (int32_t)dgc_desision_shifted;
    int32_t alpha_q8;

    if (PCODE_PRF64_START <= rx_pcode)
    {
        alpha_q8 = ALPHA_IP_PRF_64_Q8;
        if (is_sts)
        {
            uint32_t q8_shifted_u32 = 1UL << Q8_SHIFT;
            alpha_q8 -= (int32_t)q8_shifted_u32;
        }
    }
    else
    {
        alpha_q8 = ALPHA_IP_PRF_16_Q8;
    }
    rsl_dbm_q8 = rsl_dbm_q8 + dgc_decision_q8 - alpha_q8;

    return (rsl_dbm_q8 < SHRT_MIN) ? (int16_t)SHRT_MIN : (int16_t)rsl_dbm_q8;
}

int16_t rsl_calculate_signal_power(
    int32_t channel_impulse_response,
    uint8_t quantization_factor,
	uint16_t preamble_accumulation_count,
    uint8_t dgc_decision,
    uint8_t rx_pcode,
    bool is_sts
) {
    return rsl_calculate((uint32_t)channel_impulse_response, preamble_accumulation_count, quantization_factor, dgc_decision, rx_pcode, is_sts);
}

int16_t rsl_calculate_first_path_power(
    uint32_t F1,
    uint32_t F2,
    uint32_t F3,
	uint16_t preamble_accumulation_count,
    uint8_t dgc_decision,
    uint8_t rx_pcode,
    bool is_sts
) {
    uint32_t channel_area;
    F1 /= 4UL; // The First Path Amplitude (point 1) magnitude value.
    F2 /= 4UL; // The First Path Amplitude (point 2) magnitude value.
    F3 /= 4UL; // The First Path Amplitude (point 3) magnitude value.
    channel_area = F1*F1 + F2*F2 + F3*F3;

    return rsl_calculate(channel_area, preamble_accumulation_count, 0, dgc_decision, rx_pcode, is_sts);
}

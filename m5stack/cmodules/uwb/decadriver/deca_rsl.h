/**
 * @file:     deca_rsl.h
 * 
 * @brief     This file contains the receive signal strength computations
 *
 * @author    Decawave Applications
 *
 * @copyright SPDX-FileCopyrightText: Copyright (c) 2024 Qorvo US, Inc.
 *            SPDX-License-Identifier: LicenseRef-QORVO-2
 *
 */
#ifndef DECA_RSL_H_
#define DECA_RSL_H_

#include <stdint.h>
#include <stdbool.h>

/*! ---------------------------------------------------------------------------------------------------
 * @brief Estimate signal power as described in DW3000 Datasheet using fixed point math
 * 
 * Also refered as RSSI. See rsl_calculate() for a detailed description.
 * 
 * input parameters
 * @param channel_impulse_response Channel Impulse Response Power value
 * @param quantization_factor power of two multiplied to C (21 or 17)
 * @param preamble_accumulation_count  Preamble Accumulation Count value
 * @param dgc_decision DGC_DECISION, treated as an unsigned integer in range 0 to 7
 * @param rx_pcode RX code, used to know which PRF is used
 * @param is_sts if RSL is calculated on a STS segment
 *
 * return: signal power encoded on a signed Q8.8 with 0.1 dBm precision,
 *         SHRT_MIN or error (-128.0).
 */
int16_t rsl_calculate_signal_power(
    int32_t channel_impulse_response,
    uint8_t quantization_factor,
	uint16_t preamble_accumulation_count,
    uint8_t dgc_decision,
    uint8_t rx_pcode,
    bool is_sts
);

/*! ---------------------------------------------------------------------------------------------------
 * @brief Estimate first path signal power as described in DW3000 Datasheet using fixed point math
 * 
 * See rsl_calculate() for a detailed description.
 * 
 * input parameters
 * @param F1 First Path Amplitude (point 1) magnitude value (2 fractional bits).
 * @param F2 First Path Amplitude (point 2) magnitude value (2 fractional bits).
 * @param F3 First Path Amplitude (point 3) magnitude value (2 fractional bits).
 * @param preamble_accumulation_count  Preamble Accumulation Count value
 * @param dgc_decision DGC_DECISION, treated as an unsigned integer in range 0 to 7
 * @param rx_pcode RX code, used to know which PRF is used
 * @param is_sts if RSL is calculated on a STS segment
 *
 * return: signal power encoded on a signed Q8.8 with 0.1 dBm precision,
 *         SHRT_MIN or error (-128.0).
 */
int16_t rsl_calculate_first_path_power(
    uint32_t F1,
    uint32_t F2,
    uint32_t F3,
	uint16_t preamble_accumulation_count,
    uint8_t dgc_decision,
    uint8_t rx_pcode,
    bool is_sts
);

#endif /* _DECA_RSL_H_ */

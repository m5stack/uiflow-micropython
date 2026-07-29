/**
 * @file      deca_private.h
 * 
 * @brief     QM33xxx UWB peripheral driver.
 *            This file is for driver-internal private objects.
 * 
 * @author    Decawave Applications
 *
 * @copyright SPDX-FileCopyrightText: Copyright (c) 2024 Qorvo US, Inc.
 *            SPDX-License-Identifier: LicenseRef-QORVO-2
 *
 */
#ifndef DECA_PRIVATE_H
#define DECA_PRIVATE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C"
{
#endif

void dwt_writetodevice(uint32_t regFileID, uint16_t index, uint16_t length, uint8_t *buffer);

void dwt_readfromdevice(uint32_t regFileID, uint16_t index, uint16_t length, uint8_t *buffer);

#ifdef __cplusplus
}
#endif

#endif // DECA_PRIVATE_H

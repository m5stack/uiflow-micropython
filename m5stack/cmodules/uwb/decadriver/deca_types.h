/**
 * @file      deca_types.h
 * 
 * @brief     Decawave general type definitions
 *
 * @author    Decawave Applications
 *
 * @copyright SPDX-FileCopyrightText: Copyright (c) 2024 Qorvo US, Inc.
 *            SPDX-License-Identifier: LicenseRef-QORVO-2
 *
 */
#ifndef DECA_TYPES_H
#define DECA_TYPES_H

#ifdef __cplusplus
extern "C"
{
#endif

#include <stddef.h>
#include <stdint.h>
#include <stdbool.h>

#ifdef STM32F429xx
#ifndef uint8_t
#ifndef DECA_UINT8_
#define DECA_UINT8_
    typedef unsigned char uint8_t;
#endif
#endif

#ifndef uint16_t
#ifndef DECA_UINT16_
#define DECA_UINT16_
    typedef unsigned short uint16_t;
#endif
#endif

#ifndef uint32_t
#ifndef DECA_UINT32_
#define DECA_UINT32_
    typedef unsigned long uint32_t;
#endif
#endif

#ifndef int8_t
#ifndef DECA_INT8_
#define DECA_INT8_
    typedef signed char int8_t;
#endif
#endif

#ifndef int16_t
#ifndef DECA_INT16_
#define DECA_INT16_
    typedef signed short int16_t;
#endif
#endif

#ifndef int32_t
#ifndef DECA_INT32_
#define DECA_INT32_
    typedef signed long int32_t;
#endif
#endif

#ifndef uint64_t
#ifndef DECA_UINT64_
#define DECA_UINT64_
    typedef unsigned long long uint64_t;
#endif
#endif

#ifndef int64_t
#ifndef DECA_INT64_
#define DECA_INT64_
    typedef signed long long int64_t;
#endif
#endif
#endif // STM32F429xx

#ifndef DECA_NULL
#define DECA_NULL ((void *)0UL)
#endif

#ifdef __cplusplus
}
#endif

#endif /* DECA_TYPES_H */

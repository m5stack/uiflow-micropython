/**************************************************************************//**
 * @file     cmsis_iccarm.h
 * @brief    CMSIS compiler ICCARM (IAR Compiler for Arm) header file
 * @version  V5.3.0
 * @date     14. April 2021
 ******************************************************************************/

//------------------------------------------------------------------------------
//
// Copyright (c) 2017-2021 IAR Systems
// Copyright (c) 2017-2021 Arm Limited. All rights reserved.
//
// SPDX-License-Identifier: Apache-2.0
//
// Licensed under the Apache License, Version 2.0 (the "License")
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
//------------------------------------------------------------------------------
#include <stdint.h>

#ifndef __CMSIS_ICCARM_H__
#define __CMSIS_ICCARM_H__

static inline uint32_t __USAT(int32_t val, uint32_t sat)
{
  if (sat <= 31U)
  {
    const uint32_t max = ((1U << sat) - 1U);
    if (val > (int32_t)max)
    {
      return max;
    }
    else if (val < 0)
    {
      return 0U;
    }
  }
  return (uint32_t)val;
}

#endif /* __CMSIS_ICCARM_H__ */

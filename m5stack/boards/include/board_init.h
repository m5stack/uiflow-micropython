/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "sdkconfig.h"
#include "audio_hal.h"
#include "board_def.h"

#if CONFIG_CORES3
#include "../M5STACK_CoreS3/audioconfigboard.h"
#endif

void * board_codec_init(void);
int board_codec_volume_set(void *hd, int vol);
int board_codec_volume_get(void *hd, int *vol);
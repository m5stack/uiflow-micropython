/*
* SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
*
* SPDX-License-Identifier: MIT
*/

#include "sdkconfig.h"
#include "audio_hal.h"

#if CONFIG_ESP32_S3_BOX_3_BOARD
#include "../ESPRESSIF_ESP32_S3_BOX_3/audioconfigboard.h"
#endif

/**
 * @brief                  Board i2s pin definition
 */
typedef struct {
    int mck_io_num;         /*!< MCK pin, output */
    int bck_io_num;         /*!< BCK pin, input in slave role, output in master role */
    int ws_io_num;          /*!< WS pin, input in slave role, output in master role */
    int data_out_num;       /*!< DATA pin, output */
    int data_in_num;        /*!< DATA pin, input */
} board_i2s_pin_t;

void * board_codec_init(void);
int board_codec_volume_set(void *hd, int vol);
int board_codec_volume_get(void *hd, int *vol);

/**
 * @file      dw3720_deca_vals.h
 * 
 * @brief     DW3720 Register Definitions
 *            This file supports assembler and C development for DW3720 enabled devices
 *
 * @author    Decawave Applications
 *
 * @copyright SPDX-FileCopyrightText: Copyright (c) 2024 Qorvo US, Inc.
 *            SPDX-License-Identifier: LicenseRef-QORVO-2
 *
 */
#ifndef DECA_VALS_DW3720_H
#define DECA_VALS_DW3720_H

#ifdef __cplusplus
extern "C"
{
#endif

#define RX_BUFFER_0_ID 0x120000UL /* Default Receive Data Buffer (and the 1st of the double buffer set) */
#define RX_BUFFER_1_ID 0x130000UL /* 2nd Receive Data Buffer (when operating in double buffer mode) */

#define RF_TXCTRL_CH5    0x1C081134UL /* */
#define RF_TXCTRL_CH9    0x1C020034UL /* */
#define RF_TXCTRL_LO_B2  0x0EU /* */
#define RF_PLL_CFG_CH5   0x1F3CU
#define RF_PLL_CFG_CH9   0x0F3CU
#define RF_PLL_CFG_LD    0x81U
#define LDO_RLOAD_VAL_B1 0x14U
#define TX_CTRL_LO_DEF   0x040E0763UL

#define RF_EN_CH5        0x0402C000UL
#define RF_EN_CH9        0x0405C000UL

#define AUTO_PLL_CAL_STEPS 20
#define LDO_TUNE_HI_VDDDIG_TRIM_MASK    0x00F00000UL
#define LDO_TUNE_HI_VDDDIG_COARSE_MASK  0x30000000UL

#define LDO_TUNE_HI_VDDDIG_TRIM_OFFSET 20UL
#define LDO_TUNE_HI_VDDDIG_COARSE_OFFSET 28UL

typedef enum {
    VDDDIG_86mV = 0,
    VDDDIG_88mV = 1,
    VDDDIG_93mV = 2
} dwt_vdddig_mv_t;

    /*
    Lookup table default values for channel 5
    */
    typedef enum
    {
        E0_CH5_DGC_LUT_0 = 0x3803e,
        E0_CH5_DGC_LUT_1 = 0x3876e,
        E0_CH5_DGC_LUT_2 = 0x397fe,
        E0_CH5_DGC_LUT_3 = 0x38efe,
        E0_CH5_DGC_LUT_4 = 0x39c7e,
        E0_CH5_DGC_LUT_5 = 0x39dfe,
        E0_CH5_DGC_LUT_6 = 0x39ff6
    } dwt_configmrxlut_ch5_e0_e;

    typedef enum
    {
        E0_CH9_DGC_LUT_0 = 0x5407e,
        E0_CH9_DGC_LUT_1 = 0x547be,
        E0_CH9_DGC_LUT_2 = 0x54d36,
        E0_CH9_DGC_LUT_3 = 0x55e36,
        E0_CH9_DGC_LUT_4 = 0x55f36,
        E0_CH9_DGC_LUT_5 = 0x55df6,
        E0_CH9_DGC_LUT_6 = 0x55ffe
    } dwt_configmrxlut_ch9_e0_e;

#define DWT_DGC_CFG       0x32U
#define DWT_DGC_CFG0      0x00000240UL
#define DWT_DGC_CFG1      0x1A491248UL
#define DWT_DGC_CFG2      0x2DB248DBUL
#define PD_THRESH_NO_DATA 0xAF5F35CCUL /* PD threshold for no data STS mode*/
#define PD_THRESH_DEFAULT 0xAF5F584CUL

#define IP_CONFIG_LO_SCP  0x0306UL
#define IP_CONFIG_HI_SCP  0x00000000UL
#define STS_CONFIG_LO_SCP 0x000C5A0AUL
#define STS_CONFIG_HI_SCP 0x9DUL
#define STS_CONFIG_HI_RES 0x94U /* Sets STSQUAL_THRESH_64 = 0.6125 .. (60%) */

#define DWT_AUTO_CLKS (0x200U | 0x200000U | 0x100000U) // this is the default value of CLK_CTRL register

#define ACC_BUFFER_MAX_LEN (12288U + 1U) /* +1 is needed for "dummy" read */

#define REG_DIRECT_OFFSET_MAX_LEN 127U
#define EXT_FRAME_LEN             1023U
#define INDIRECT_POINTER_A_ID     0x1D0000UL /* pointer to access indirect access buffer A */
#define INDIRECT_POINTER_B_ID     0x1E0000UL /* pointer to access indirect access buffer B */

#define ACC_MEM_ID 0x150000UL

#define IPATOV_CIR_NB_SAMPLES   1024
#define STS1_CIR_NB_SAMPLES     DWT_CIR_LEN_STS
#define STS2_CIR_NB_SAMPLES     DWT_CIR_LEN_STS

#define TX_BUFFER_ID            0x140000UL /* Transmit Data Buffer */
#define SCRATCH_RAM_ID          0x160000UL
#define AES_KEY_RAM_MEM_ADDRESS 0x170000UL /* Address of the AES keys in RAM */

#define CIA_I_RX_TIME_LEN  5U
#define CIA_C_RX_TIME_LEN  5U
#define CIA_TDOA_LEN       6U /* TDOA value is 41 bits long. You will need to read 6 bytes and mask with 0x01FFFFFFFFFF */
#define CIA_I_STAT_OFFSET  3UL /* RX status info for Ipatov sequence */
#define CIA_C_STAT_OFFSET  2UL /* RX status info for STS sequence */
#define CIA_DIAGNOSTIC_OFF (0x1U << 4U) /* bit4 in CIA_CONF + 1 */

#define DB_MAX_DIAG_SIZE 232U /* size of diagnostic data (in bytes) when DW_CIA_DIAG_LOG_MAX is set */
#define DB_MID_DIAG_SIZE 56U /* size of diagnostic data (in bytes) when DW_CIA_DIAG_LOG_MID is set */
#define DB_MIN_DIAG_SIZE 32U /* size of diagnostic data (in bytes) when DW_CIA_DIAG_LOG_MIN is set */

#define STS_ACC_CP_QUAL_SIGNTST 0x0800U /* sign test */
#define STS_ACC_CP_QUAL_SIGNEXT 0xF000U /* 12 bit to 16 bit sign extension */
#define STS_IV_LENGTH           16 /* CP initial value is 16 bytes or 128 bits*/

#define STS_KEY_LENGTH 16 /* CP AES key is 16 bytes or 128 bits*/

#define PMSC_TXFINESEQ_ENABLE  0x4D28874UL
#define PMSC_TXFINESEQ_DISABLE 0x0D20874UL

#define TXRXSWITCH_TX   0x01011100UL
#define TXRXSWITCH_AUTO 0x1C000000UL

#define ERR_RX_CAL_FAIL 0x1FFFFFFFUL

#define DWT_TX_BUFF_OFFSET_ADJUST 128UL // TX buffer offset adjustment when txBufferOffset > 127

#define LOGGER_MEM_ID 0x180000

#define PANADR_PAN_ID_BYTE_OFFSET 2U
#define PMSC_CTRL0_PLL2_SEQ_EN    0x01000000UL /* Enable PLL2 on/off sequencing by SNIFF mode */
#define RX_FINFO_STD_RXFLEN_MASK  0x007FU /* Receive Frame Length (0 to 127) */
#define RX_TIME_RX_STAMP_LEN      5U /* read only 5 bytes (the adjusted timestamp (40:0)) */
#define TX_TIME_TX_STAMP_LEN      5U /* 40-bits = 5 bytes */
#define SCRATCH_BUFFER_MAX_LEN    127 /* AES scratch memory */
#define STD_FRAME_LEN             127

#define TX_POWER_COARSE_GAIN_MASK 0x00000003UL
#define TX_POWER_FINE_GAIN_MASK 0x0000003FUL

/* All TX events mask. */
#define SYS_STATUS_ALL_TX ((uint8_t)DWT_INT_AAT_BIT_MASK | (uint8_t)DWT_INT_TXFRB_BIT_MASK | (uint8_t)DWT_INT_TXPRS_BIT_MASK | \
                           (uint8_t)DWT_INT_TXPHS_BIT_MASK | (uint8_t)DWT_INT_TXFRS_BIT_MASK)

#define SYS_STATUS_RXOK (DWT_INT_RXFCG_BIT_MASK | DWT_INT_CIA_DONE_BIT_MASK)

// SYS_STATE_LO register errors
#define DW_SYS_STATE_IDLE 0x3U // TSE is in IDLE (IDLE_PLL)

#define MAX_OFFSET_ALLOWED (0xFFF)
#define MIN_INDERECT_ADDR  (0x1000)

#define LDO_BIAS_KICK_E0 (0x600) // NOTE: (Writing to bit 10 for BIAS and 9 for LDO)

// DW3720 OTP operating parameter set selection
#define DWT_OPSET_LONG  (0x0UL << 12UL)
#define DWT_OPSET_SCP   (0x1UL << 12UL)
#define DWT_OPSET_SHORT (0x2UL << 12UL)

//! CIA version register
#define CIA_VERSION_REG    0x191F48UL //

#define SEMAPHORE_REG_ADDR      0x1A0000 // Address of the Semaphore register
#define SEMAPHORE_INT_ADDR      0x1A0001 // Address of the Semaphore interrupt
#define SEMA_SP1_GRANT          0x01U // Host on SPI1 has permission to access DW registers
#define SEMA_SP2_GRANT          0x02U // Host on SPI2 has permission to access DW registers
#define SEMA_SPI1_SLEEP_MASK    0x20U // Host on SPI1 has disabled sleeping functionality
#define SEMA_SPI2_SLEEP_MASK    0x40U // Host on SPI2 has disabled sleeping functionality
#define SEMA_SLEEP_MASK         (SEMA_SPI1_SLEEP_MASK | SEMA_SPI2_SLEEP_MASK)
#define SEMA_SOFT_RESET_NO_SEMA 0x08U /*Reset without the Semaphore register*/
#define SEMA_SOFT_RESET         0x10U /*Reset including the Semaphore register*/

#define BUF0_RX_FINFO     0x180000UL // part of min set
#define BUF0_RX_TIME      0x180004UL // part of min set (RX time ~ RX_TIME_0)
#define BUF0_RX_TIME1     0x180008UL // part of min set
#define BUF0_CIA_DIAG_0   0x18000CUL // part of min set
#define BUF0_TDOA         0x180010UL // part of min set
#define BUF0_PDOA         0x180014UL // part of min set
#define BUF0_RES1         0x180018UL // part of min set (---)
#define BUF0_IP_DIAG_12   0x18001CUL // part of min set
#define BUF0_IP_TS        0x180020UL // part of mid set
#define BUF0_RES2         0x180024UL // part of mid set
#define BUF0_STS_TS       0x180028UL // part of mid set
#define BUF0_STS_STAT     0x18002CUL // part of mid set
#define BUF0_STS1_TS      0x180030UL // part of mid set
#define BUF0_STS1_STAT    0x180034UL // part of mid set
#define BUF0_CIA_DIAG_1   0x180038UL // part of max set
#define BUF0_IP_DIAG_0    0x18003CUL // part of max set
#define BUF0_IP_DIAG_1    0x180040UL // part of max set
#define BUF0_IP_DIAG_2    0x180044UL //...
#define BUF0_IP_DIAG_3    0x180048UL
#define BUF0_IP_DIAG_4    0x18004CUL
#define BUF0_IP_DIAG_5    0x180050UL
#define BUF0_IP_DIAG_6    0x180054UL
#define BUF0_IP_DIAG_7    0x180058UL
#define BUF0_IP_DIAG_8    0x18005CUL
#define BUF0_IP_DIAG_9    0x180060UL
#define BUF0_IP_DIAG_10   0x180064UL
#define BUF0_IP_DIAG_11   0x180068UL
#define BUF0_STS_DIAG_0   0x18006CUL
#define BUF0_STS_DIAG_1   0x180070UL
#define BUF0_STS_DIAG_2   0x180074UL
#define BUF0_STS_DIAG_3   0x180078UL
#define BUF0_STS_DIAG_4   0x18007CUL
#define BUF0_STS_DIAG_5   0x180080UL
#define BUF0_STS_DIAG_6   0x180084UL
#define BUF0_STS_DIAG_7   0x180088UL
#define BUF0_STS_DIAG_8   0x18008CUL
#define BUF0_STS_DIAG_9   0x180090UL
#define BUF0_STS_DIAG_10  0x180094UL
#define BUF0_STS_DIAG_11  0x180098UL
#define BUF0_STS_DIAG_12  0x18009CUL
#define BUF0_STS_DIAG_13  0x1800A0UL
#define BUF0_STS_DIAG_14  0x1800A4UL
#define BUF0_STS_DIAG_15  0x1800A8UL
#define BUF0_STS_DIAG_16  0x1800ACUL
#define BUF0_STS_DIAG_17  0x1800B0UL
#define BUF0_STS1_DIAG_0  0x1800B4UL
#define BUF0_STS1_DIAG_1  0x1800B8UL
#define BUF0_STS1_DIAG_2  0x1800BCUL
#define BUF0_STS1_DIAG_3  0x1800C0UL
#define BUF0_STS1_DIAG_4  0x1800C4UL
#define BUF0_STS1_DIAG_5  0x1800C8UL
#define BUF0_STS1_DIAG_6  0x1800CCUL
#define BUF0_STS1_DIAG_7  0x1800D0UL
#define BUF0_STS1_DIAG_8  0x1800D4UL
#define BUF0_STS1_DIAG_9  0x1800D8UL
#define BUF0_STS1_DIAG_10 0x1800DCUL
#define BUF0_STS1_DIAG_11 0x1800E0UL
#define BUF0_STS1_DIAG_12 0x1800E4UL

#define BUF1_RX_FINFO     0x1800E8UL // part of min set
#define BUF1_RX_TIME      0x1800ECUL // part of min set (RX time ~ RX_TIME_O)
#define BUF1_RX_TIME1     0x1800F0UL // part of min set
#define BUF1_CIA_DIAG_0   0x1800F4UL // part of min set
#define BUF1_TDOA         0x1800F8UL // part of min set
#define BUF1_PDOA         0x1800FCUL // part of min set
#define BUF1_RES1         0x180100UL // part of min set (---)
#define BUF1_IP_DIAG_12   0x180104UL // part of min set
#define BUF1_IP_TS        0x180108UL // part of mid set
#define BUF1_RES2         0x18010CUL // part of mid set
#define BUF1_STS_TS       0x180110UL // part of mid set
#define BUF1_RES3         0x180114UL // part of mid set
#define BUF1_STS1_TS      0x180118UL // part of mid set
#define BUF1_RES4         0x18011CUL // part of mid set
#define BUF1_CIA_DIAG_1   0x180120UL // part of max set
#define BUF1_IP_DIAG_0    0x180124UL // part of max set
#define BUF1_IP_DIAG_1    0x180128UL // part of max set
#define BUF1_IP_DIAG_2    0x18012CUL //...
#define BUF1_IP_DIAG_3    0x180130UL
#define BUF1_IP_DIAG_4    0x180134UL
#define BUF1_IP_DIAG_5    0x180138UL
#define BUF1_IP_DIAG_6    0x18013CUL
#define BUF1_IP_DIAG_7    0x180140UL
#define BUF1_IP_DIAG_8    0x180144UL
#define BUF1_IP_DIAG_9    0x180148UL
#define BUF1_IP_DIAG_10   0x18014CUL
#define BUF1_IP_DIAG_11   0x180150UL
#define BUF1_STS_DIAG_0   0x180154UL
#define BUF1_STS_DIAG_1   0x180158UL
#define BUF1_STS_DIAG_2   0x18015CUL
#define BUF1_STS_DIAG_3   0x180160UL
#define BUF1_STS_DIAG_4   0x180164UL
#define BUF1_STS_DIAG_5   0x180168UL
#define BUF1_STS_DIAG_6   0x18016CUL
#define BUF1_STS_DIAG_7   0x180170UL
#define BUF1_STS_DIAG_8   0x180174UL
#define BUF1_STS_DIAG_9   0x180178UL
#define BUF1_STS_DIAG_10  0x18017CUL
#define BUF1_STS_DIAG_11  0x180180UL
#define BUF1_STS_DIAG_12  0x180184UL
#define BUF1_STS_DIAG_13  0x180188UL
#define BUF1_STS_DIAG_14  0x18018CUL
#define BUF1_STS_DIAG_15  0x180190UL
#define BUF1_STS_DIAG_16  0x180194UL
#define BUF1_STS_DIAG_17  0x180198UL
#define BUF1_STS1_DIAG_0  0x18019CUL
#define BUF1_STS1_DIAG_1  0x1801A0UL
#define BUF1_STS1_DIAG_2  0x1801A4UL
#define BUF1_STS1_DIAG_3  0x1801A8UL
#define BUF1_STS1_DIAG_4  0x1801ACUL
#define BUF1_STS1_DIAG_5  0x1801B0UL
#define BUF1_STS1_DIAG_6  0x1801B4UL
#define BUF1_STS1_DIAG_7  0x1801B8UL
#define BUF1_STS1_DIAG_8  0x1801BCUL
#define BUF1_STS1_DIAG_9  0x1801C0UL
#define BUF1_STS1_DIAG_10 0x1801C4UL
#define BUF1_STS1_DIAG_11 0x1801C8UL
#define BUF1_STS1_DIAG_12 0x1801CCUL

//! fast commands
#define CMD_ENTER_SLEEP       0x1A //!< Enters sleep/deep sleep according to ANA_CFG - DEEPSLEEP_EN
#define CMD_SEMA_RESET_NO_SEM 0x19 //!< Global digital reset without reset of the semaphore
#define CMD_SEMA_RESET        0x18 //!< Global digital reset including of the semaphore
#define CMD_SEMA_FORCE        0x16 //!< Only SPI 2 can issue this command. Force access regardless of current semaphore value.
#define CMD_SEMA_REL          0x15 //!< Release the semaphore if it is currently reserved by this master.
#define CMD_SEMA_REQ          0x14 //!< Write to the Semaphore and try to reserve access (if it hasn't already been reserved by the other master)
#define CMD_DB_TOGGLE         0x13 //!< Toggle double buffer pointer
#define CMD_CLR_IRQS          0x12 //!< Clear all events/clear interrupt
#define CMD_CCA_TX_W4R        0x11 //!< Check if channel clear prior to TX, enable RX when TX done
#define CMD_DTX_REF_W4R       0x10 //!< Start delayed TX (as DTX_REF below), enable RX when TX done
#define CMD_DTX_RS_W4R        0xF //!< Start delayed TX (as DTX_RS below), enable RX when TX done
#define CMD_DTX_TS_W4R        0xE //!< Start delayed TX (as DTX_TS below), enable RX when TX done
#define CMD_DTX_W4R           0xD //!< Start delayed TX (as DTX below), enable RX when TX done
#define CMD_TX_W4R            0xC //!< Start TX (as below), enable RX when TX done
#define CMD_CCA_TX            0xB //!< Check if channel clear prior to TX
#define CMD_DRX_REF           0xA //!< Enable RX @ time = DREF_TIME + DX_TIME
#define CMD_DTX_REF           0x9 //!< Start delayed TX (RMARKER will be @ time = DREF_TIME + DX_TIME)
#define CMD_DRX_RS            0x8 //!< Enable RX @ time = RX_TIME + DX_TIME
#define CMD_DTX_RS            0x7 //!< Start delayed TX (RMARKER will be @ time = RX_TIME + DX_TIME)
#define CMD_DRX_TS            0x6 //!< Enable RX @ time = TX_TIME + DX_TIME
#define CMD_DTX_TS            0x5 //!< Start delayed TX (RMARKER will be @ time = TX_TIME + DX_TIME)
#define CMD_DRX               0x4 //!< Enable RX @ time specified in DX_TIME register
#define CMD_DTX               0x3 //!< Start delayed TX (RMARKER will be @ time set in DX_TIME register)
#define CMD_RX                0x2 //!< Enable RX
#define CMD_TX                0x1 //!< Start TX
#define CMD_TXRXOFF           0x0 //!< Turn off TX or RX, clear any TX/RX events and put DW3720 into IDLE

#define ENABLE_ALL_GPIOS_MASK  0x1200492

// TxPower Adjustment
#define LUT_COMP_SIZE 64U               // Size of Tx power compensation look-up table
#define TXPOWER_ADJUSTMENT_MARGIN 5U    // Margin for tx power adjustment in 0.1dB steps. Trying to achieve 0.5dB output TxPower accuracy with DW3720
#define COARSE_0_TO_1   32              // TxPower difference between coarse gain 0 and coarse gain 1 in 0.1dB Step. Same for CH5 and CH9
#define COARSE_1_TO_2   13              // TxPower difference between coarse gain 1 and coarse gain 2 in 0.1dB Step. Same for CH5 and CH9
#define COARSE_2_TO_3   5               // TxPower difference between coarse gain 2 and coarse gain 3 in 0.1dB Step. Same for CH5 and CH9
#define NUM_COARSE_GAIN  3              // Number of coarse gains
#define MAX_BOOST_CH5  354U              // Maximum boost for channel 5
#define MAX_BOOST_CH9  305U              // Maximum boost for channel 9

#define RF_PLL_COMMON    0xE104

#ifdef __cplusplus
}
#endif

#endif /* DECA_VALS_DW3720_H */

/**
 * @file:     deca_compat.c
 * 
 * @brief     This file contains the code for the backward-compatibility with existing Decawave application examples
 *
 * @author    Decawave Applications
 *
 * @copyright SPDX-FileCopyrightText: Copyright (c) 2024 Qorvo US, Inc.
 *            SPDX-License-Identifier: LicenseRef-QORVO-2
 * 
 * Requirements to the application:
 * Call the dwt_probe() at the start of the application to select the correct driver.
 *
 */
#include "deca_device_api.h"
#include "deca_interface.h"
#include "deca_version.h"
#include "deca_private.h"
#include "deca_ull.h"

#ifdef ESP_PLATFORM
#include <sdkconfig.h>
#endif

#if CONFIG_DW3000_CHIP_DW3720
#include "dw3720/dw3720_deca_regs.h"
#include "dw3720/dw3720_deca_vals.h"
#elif CONFIG_DW3000_CHIP_DW3000
#include "dw3000/dw3000_deca_regs.h"
#include "dw3000/dw3000_deca_vals.h"
#endif

// Common to all Decawave chips ID address
#define DW3XXX_DEVICE_ID (0x0)

#ifdef DWT_ENABLE_CRC
// Static CRC-8 ATM implementation.
// clang-format off
static const uint8_t crcTable[256] = {
        0x00U, 0x07U, 0x0EU, 0x09U, 0x1CU, 0x1BU, 0x12U, 0x15U, 0x38U, 0x3FU, 0x36U, 0x31U, 0x24U, 0x23U, 0x2AU, 0x2DU,
        0x70U, 0x77U, 0x7EU, 0x79U, 0x6CU, 0x6BU, 0x62U, 0x65U, 0x48U, 0x4FU, 0x46U, 0x41U, 0x54U, 0x53U, 0x5AU, 0x5DU,
        0xE0U, 0xE7U, 0xEEU, 0xE9U, 0xFCU, 0xFBU, 0xF2U, 0xF5U, 0xD8U, 0xDFU, 0xD6U, 0xD1U, 0xC4U, 0xC3U, 0xCAU, 0xCDU,
        0x90U, 0x97U, 0x9EU, 0x99U, 0x8CU, 0x8BU, 0x82U, 0x85U, 0xA8U, 0xAFU, 0xA6U, 0xA1U, 0xB4U, 0xB3U, 0xBAU, 0xBDU,
        0xC7U, 0xC0U, 0xC9U, 0xCEU, 0xDBU, 0xDCU, 0xD5U, 0xD2U, 0xFFU, 0xF8U, 0xF1U, 0xF6U, 0xE3U, 0xE4U, 0xEDU, 0xEAU,
        0xB7U, 0xB0U, 0xB9U, 0xBEU, 0xABU, 0xACU, 0xA5U, 0xA2U, 0x8FU, 0x88U, 0x81U, 0x86U, 0x93U, 0x94U, 0x9DU, 0x9AU,
        0x27U, 0x20U, 0x29U, 0x2EU, 0x3BU, 0x3CU, 0x35U, 0x32U, 0x1FU, 0x18U, 0x11U, 0x16U, 0x03U, 0x04U, 0x0DU, 0x0AU,
        0x57U, 0x50U, 0x59U, 0x5EU, 0x4BU, 0x4CU, 0x45U, 0x42U, 0x6FU, 0x68U, 0x61U, 0x66U, 0x73U, 0x74U, 0x7DU, 0x7AU,
        0x89U, 0x8EU, 0x87U, 0x80U, 0x95U, 0x92U, 0x9BU, 0x9CU, 0xB1U, 0xB6U, 0xBFU, 0xB8U, 0xADU, 0xAAU, 0xA3U, 0xA4U,
        0xF9U, 0xFEU, 0xF7U, 0xF0U, 0xE5U, 0xE2U, 0xEBU, 0xECU, 0xC1U, 0xC6U, 0xCFU, 0xC8U, 0xDDU, 0xDAU, 0xD3U, 0xD4U,
        0x69U, 0x6EU, 0x67U, 0x60U, 0x75U, 0x72U, 0x7BU, 0x7CU, 0x51U, 0x56U, 0x5FU, 0x58U, 0x4DU, 0x4AU, 0x43U, 0x44U,
        0x19U, 0x1EU, 0x17U, 0x10U, 0x05U, 0x02U, 0x0BU, 0x0CU, 0x21U, 0x26U, 0x2FU, 0x28U, 0x3DU, 0x3AU, 0x33U, 0x34U,
        0x4EU, 0x49U, 0x40U, 0x47U, 0x52U, 0x55U, 0x5CU, 0x5BU, 0x76U, 0x71U, 0x78U, 0x7FU, 0x6AU, 0x6DU, 0x64U, 0x63U,
        0x3EU, 0x39U, 0x30U, 0x37U, 0x22U, 0x25U, 0x2CU, 0x2BU, 0x06U, 0x01U, 0x08U, 0x0FU, 0x1AU, 0x1DU, 0x14U, 0x13U,
        0xAEU, 0xA9U, 0xA0U, 0xA7U, 0xB2U, 0xB5U, 0xBCU, 0xBBU, 0x96U, 0x91U, 0x98U, 0x9FU, 0x8AU, 0x8DU, 0x84U, 0x83U,
        0xDEU, 0xD9U, 0xD0U, 0xD7U, 0xC2U, 0xC5U, 0xCCU, 0xCBU, 0xE6U, 0xE1U, 0xE8U, 0xEFU, 0xFAU, 0xFDU, 0xF4U, 0xF3U
};
// clang-format on
#endif // DWT_ENABLE_CRC

/* Use statically allocated struct: to make driver compatible with legacy implementations: 1chip<->1driver */
static struct dwchip_s static_dw = { 0 };

static struct dwchip_s *dw; //pointer to the local driver structure

#ifdef WIN32
extern const struct dwt_driver_s dw3000_driver;
extern const struct dwt_driver_s dw3720_driver;
static const struct dwt_driver_s* tmp_ptr[] = { &dw3000_driver, &dw3720_driver };
#endif // WIN32

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function selects the correct DecaDriver from the list
 *
 * input parameters
 * @parameter dwt_probe_s *probe_interf
 *
 * output parameters
 *
 * returns ret - DWT_ERROR if no driver found or invalid probe_interface. DWT_SUCCESS if driver is found.
 */
int32_t dwt_probe(struct dwt_probe_s *probe_interf)
{
    dwt_error_e ret = DWT_ERROR;
    uint32_t devId;
    uint8_t buf[sizeof(uint32_t)];
    uint8_t addr;

    if(probe_interf != NULL)
    {
        if(probe_interf->dw == NULL)
        {
            dw = &static_dw;
        }
        else
        {
            dw = (struct dwchip_s*)probe_interf->dw;
        }
        dw->SPI = (struct dwt_spi_s*)probe_interf->spi;
        dw->wakeup_device_with_io = probe_interf->wakeup_device_with_io;

        dw->wakeup_device_with_io();

        // Device ID address is common in between all DW chips
        addr = (uint8_t)DW3XXX_DEVICE_ID;

        (void)dw->SPI->readfromspi(sizeof(uint8_t), &addr, sizeof(buf), buf);
        devId = (((uint32_t)buf[3] << 24UL) | ((uint32_t)buf[2] << 16UL) | ((uint32_t)buf[1] << 8UL) | (uint32_t)buf[0]);

#ifdef WIN32
        // Find which DW device the host is connected to and assign correct low-level driver structure
        for(uint8_t i = 0U; i < 2U; i++)
        {
            if ((devId & tmp_ptr[i]->devmatch) == (tmp_ptr[i]->devid & tmp_ptr[i]->devmatch))
            {
                dw->dwt_driver = tmp_ptr[i];
                ret = DWT_SUCCESS;
                break;
            }
        }

#else
        struct dwt_driver_s **driver_list = probe_interf->driver_list;
        for (uint8_t i = 0U; i < probe_interf->dw_driver_num; i++)
        {
            if ((devId & driver_list[i]->devmatch) == (driver_list[i]->devid & driver_list[i]->devmatch))
            {
                dw->dwt_driver = driver_list[i];
                ret = DWT_SUCCESS;
                break;
            }
        }
#endif
    }

    return (int32_t)ret;
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will update dw pointer used by interrupt
 *
 * input parameters
 * @param new_dw - dw instatiated by MCPS layer
 *
 * return parameters
 * old_dw pointer. This pointer can be restored when deleting MCPS instance
 *
 */
struct dwchip_s *dwt_update_dw(struct dwchip_s *new_dw)
{
    struct dwchip_s *old_dw = dw;
    dw = new_dw;
    return old_dw;
}

/* Wrappers for the backward compatibility: the same fn() names for all chips, assuming only 1 chip present in the "compatible" implementation */

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function returns the version of the API
 *
 * input parameters
 *
 * output parameters
 *
 * returns version (DW3xxx_DRIVER_VERSION)
 */
int32_t dwt_apiversion(void)
{
    return (int32_t)dw->dwt_driver->vernum;
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function returns the driver version of the API
 *
 * input parameters
 *
 * output parameters
 *
 * returns version string
 */
const char *dwt_version_string(void)
{
    return DRIVER_VERSION_STR;
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to return the read V measured @ 3.0 V value recorded in OTP address 0x8 (VBAT_ADDRESS)
 *
 * NOTE: dwt_initialise() must be called prior to this function so that it can return a relevant value.
 *
 * input parameters
 *
 * output parameters
 *
 * returns the 8 bit V bat value as programmed in the factory
 */
uint8_t dwt_geticrefvolt(void)
{
    return ull_geticrefvolt(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to return the read T measured @ 22 C value recorded in OTP address 0x9 (VTEMP_ADDRESS)
 *
 * NOTE: dwt_initialise() must be called prior to this function so that it can return a relevant value.
 *
 * input parameters
 *
 * output parameters
 *
 * returns the 8 bit V temp value as programmed in the factory
 */
uint8_t dwt_geticreftemp(void)
{
    return ull_geticreftemp(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to return the read part ID of the device
 *
 * NOTE: dwt_initialise() must be called prior to this function so that it can return a relevant value.
 *
 * input parameters
 *
 * output parameters
 *
 * returns the 32 bit part ID value as programmed in the factory
 */
uint32_t dwt_getpartid(void)
{
    return ull_getpartid(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to return the read lot ID of the device
 *
 * NOTE: dwt_initialise() must be called prior to this function so that it can return a relevant value.
 *
 * input parameters
 *
 * output parameters
 *
 * returns the 64 bit lot ID value as programmed in the factory
 */
uint64_t dwt_getlotid(void)
{
    return ull_getlotid(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to return the read device type and revision information of the DW UWB chip
 *
 * input parameters
 *
 * output parameters
 *
 * returns the silicon DevID
 */
uint32_t dwt_readdevid(void)
{
    return dwt_read32bitoffsetreg(dw, DW3XXX_DEVICE_ID, 0U);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to return the read OTP revision
 *
 * NOTE: dwt_initialise() must be called prior to this function so that it can return a relevant value.
 *
 * input parameters
 *
 * output parameters
 *
 * returns the read OTP revision value
 */
uint8_t dwt_otprevision(void)
{
    return ull_otprevision(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function overrides the temperature to be used for PLL calibration of the device.
 *        If set to -127, the next time dwt_initialise is called the onchip temperature sensor
 *        will be used to set it.
 * input parameters
 * @param temperature - expected operating temperature in celcius
 *
 * output parameters none
 *
 * no return value
 * 
 * DW3720 ONLY
 */
void dwt_settemperature(int8_t temperature)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_setpllcaltemperature(dw, temperature);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function reads the temperature in celcius that will be used for PLL calibrations
 *
 * input parameters
 *
 * output parameters none
 *
 * returns the temperature in celcius that will be used by PLL calibrations
 * 
 * DW3720 ONLY
 */
int8_t dwt_getpllcalibrationtemperature(void)
{
#if CONFIG_DW3000_CHIP_DW3720
    return ull_getpllcaltemperature(dw);
#endif
    return -1;
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function enables/disables the fine grain TX sequencing (enabled by default).
 *
 * input parameters
 * @param enable - 1 to enable fine grain TX sequencing, 0 to disable it.
 *
 * output parameters none
 *
 * no return value
 */
void dwt_setfinegraintxseq(int32_t enable)
{
    ull_setfinegraintxseq(dw, enable);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to enable GPIO for external LNA or PA functionality - HW dependent, consult the DW3000 User Manual.
 *        This can also be used for debug as enabling TX and RX GPIOs is quite handy to monitor DW3000's activity.
 *
 * NOTE: Enabling PA functionality requires that fine grain TX sequencing is deactivated. This can be done using
 *       dwt_setfinegraintxseq().
 *
 * input parameters
 * @param lna_pa - bit field: bit 0 if set will enable LNA functionality,
 *                          : bit 1 if set will enable PA functionality,
 *                          : to disable LNA/PA set the bits to 0 (
 * output parameters
 *
 * no return value
 */
void dwt_setlnapamode(int32_t lna_pa)
{
    ull_setlnapamode(dw, lna_pa);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to configure GPIO function
 *
 *
 * input parameters
 * @param gpio_mask - the mask of the GPIOs to change the mode of. Typically built from dwt_gpio_mask_e values.
 * @param gpio_modes - the GPIO modes to set. Typically built from dwt_gpio_pin_e values.
 *
 * output parameters
 *
 * no return value
 */
void dwt_setgpiomode(uint32_t gpio_mask, uint32_t gpio_modes)
{
    ull_setgpiomode(dw, gpio_mask, gpio_modes);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to configure the GPIOs as inputs or outputs, default is input == 1
 *
 * input parameters
 * @param in_out - if corresponding GPIO bit is set to 1 then it is input, otherwise it is output
 *               - GPIO 0 = bit 0, GPIO 1 = bit 1 etc...
 *
 * output parameters
 *
 * no return value
 */
void dwt_setgpiodir(uint16_t in_out)
{
    ull_setgpiodir(dw, in_out);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to set output value on GPIOs that have been configured for output via dwt_setgpiodir() API
 *
 * input parameters
 * @param gpio - should be one or multiple of dwt_gpio_mask_e values
 * @param value - Logic value for GPIO/GPIOs if multiple set at same time.
 *
 * output parameters
 *
 * no return value
 */
void dwt_setgpiovalue(uint16_t gpio, int32_t value)
{
    ull_setgpiovalue(dw, gpio, value);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the raw value of the GPIO pins.
 *        It is presumed that functions such as dwt_setgpiomode(), dwt_setgpiovalue() and dwt_setgpiodir() are called before this function.
 *
 * input parameters
 *
 * returns a uint16_t value that holds the value read on the GPIO pins.
 */
uint16_t dwt_readgpiovalue(void)
{
    return ull_readgpiovalue(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function initialises the DW3xxx transceiver:
 * It performs the initially required device configurations and initializes
 * a static data belonging to the low-level driver.
 *
 * NOTES:
 * 1.this function needs to be run before dwt_configuresleep, also the SPI frequency has to be < 7MHz
 * 2.it also reads and applies LDO and BIAS tune and crystal trim values from OTP memory
 * 3.it is assumed this function is called after a reset or on power up of the DW3xxx transceiver
 *
 * input parameters
 * @param mode - mask which defines which OTP values to read.
 *
 * output parameters
 *
 * returns DWT_SUCCESS for success, or DWT_ERROR for error
 */
int32_t dwt_initialise(int32_t mode)
{
    return dw->dwt_driver->dwt_ops->initialize(dw, mode);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function can place DW3000 into IDLE/IDLE_PLL or IDLE_RC mode when it is not actively in TX or RX.
 *
 * input parameters
 * @param state - DWT_DW_IDLE (1) to put DW3000 into IDLE/IDLE_PLL state; DWT_DW_INIT (0) to put DW3000 into INIT_RC state;
 *                DWT_DW_IDLE_RC (2) to put DW3000 into IDLE_RC state.
 *
 * output parameters none
 *
 * returns DWT_SUCCESS for success, or DWT_ERROR for error
 */
int dwt_setdwstate(int state)
{
    return ull_setdwstate(dw, state);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to enable GPIO clocks. The clocks are needed to ensure correct GPIO operation
 *
 * input parameters
 *
 * output parameters
 *
 * no return value
 */
void dwt_enablegpioclocks(void)
{
    ull_enablegpioclocks(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function needs to be called after device is woken up from DEEPSLEEP/SLEEP state, to restore the
 * configuration which has not been automatically restored from AON
 *
 * input parameters
 * @param full_restore - If set to 0, the function will skip DGC update, PGC and ADC offset calibration.
 *                     - If set to any other value, the function will perform the complete update.
 *
 * return DWT_SUCCESS
 */
void dwt_restoreconfig(int32_t full_restore)
{
    ull_restoreconfig(dw, full_restore);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function configures STS mode: e.g. DWT_STS_MODE_OFF, DWT_STS_MODE_1 etc
 * The dwt_configure should be called prior to this to configure other parameters
 *
 * input parameters
 * @param stsMode    -   e.g. DWT_STS_MODE_OFF, DWT_STS_MODE_1 etc.
 *
 * return DWT_SUCCESS
 */
void dwt_configurestsmode(uint8_t stsMode)
{
    ull_configurestsmode(dw, stsMode);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function provides the main API for the configuration of the
 * DW3000 and this low-level driver.  The input is a pointer to the data structure
 * of type dwt_config_t that holds all the configurable items.
 * The dwt_config_t structure shows which ones are supported
 *
 * input parameters
 * @param config    -   pointer to the configuration structure, which contains the device configuration data.
 *
 * output parameters
 *
 * return DWT_SUCCESS or DWT_ERROR (e.g. when PLL CAL fails / PLL fails to lock)
 */
int32_t dwt_configure(dwt_config_t *config)
{
    return dw->dwt_driver->dwt_ops->configure(dw, config);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function provides the API for the configuration of the TX power
 * The input is the desired tx power to configure.
 *
 * input parameters
 * @param power     -   tx power to configure 32 bits.
 *
 * output parameters
 *
 * no return value
 */
void dwt_settxpower(uint32_t power)
{
    ull_settxpower(dw, power);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function provides the API for the configuration of the TX spectrum
 * including the power and pulse generator delay. The input is a pointer to the data structure
 * of type dwt_txconfig_t that holds all the configurable items.
 *
 * input parameters
 * @param config    -   pointer to the txrf configuration structure, which contains the tx rf config data
 *
 * output parameters
 *
 * no return value
 */
void dwt_configuretxrf(dwt_txconfig_t *config)
{
    dw->dwt_driver->dwt_ops->configure_tx_rf(dw, config);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function re-loads the STS AES initial value
 *
 * input parameters
 *
 * output parameters
 *
 * no return value
 */
void dwt_configurestsloadiv(void)
{
    ull_configurestsloadiv(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function sets the default values of the lookup tables depending on the channel selected.
 *
 * input parameters
 * @param[in] channel - Channel that the device will be transmitting/receiving on.
 *
 * no return value
 */
void dwt_configmrxlut(int32_t channel)
{
    ull_configmrxlut(dw, channel);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function configures the STS AES 128 bit key value.
 * the default value is [31:00]c9a375fa,
 *                      [63:32]8df43a20,
 *                      [95:64]b5e5a4ed,
 *                     [127:96]0738123b
 *
 * input parameters
 * @param pStsKey - the pointer to the structure of dwt_sts_cp_key_t type, which holds the AES128 key value to generate STS
 *
 * output parameters
 *
 * no return value
 */
void dwt_configurestskey(dwt_sts_cp_key_t *pStsKey)
{
    ull_configurestskey(dw, pStsKey);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function configures the STS AES 128 bit initial value, the default value is 1, i.e. DW3000 reset value is 1.
 *
 * input parameters
 * @param pStsIv - the pointer to the structure of dwt_sts_cp_iv_t type, which holds the IV value to generate STS
 *
 * output parameters
 *
 * no return value
 */
void dwt_configurestsiv(dwt_sts_cp_iv_t *pStsIv)
{
    ull_configurestsiv(dw, pStsIv);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function writes the antenna delay (in time units) to RX registers
 *
 * input parameters:
 * @param rxDelay - this is the total (RX) antenna delay value, which
 *                          will be programmed into the RX register
 *
 * output parameters
 *
 * no return value
 */
void dwt_setrxantennadelay(uint16_t antennaDly)
{
    ull_setrxantennadelay(dw, antennaDly);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function reads the antenna delay (in time units) from the RX antenna delay register
 *
 * input parameters:
 * @param dw - DW3xxx chip descriptor handler.
 *
 * output parameters
 *
 * returns 16-bit RX antenna delay value which is currently programmed in CIA_CONF_ID register
 */
uint16_t dwt_getrxantennadelay(void)
{
    return ull_getrxantennadelay(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function writes the antenna delay (in time units) to TX registers
 *
 * input parameters:
 * @param txDelay - this is the total (TX) antenna delay value, which
 *                          will be programmed into the TX delay register
 *
 * output parameters
 *
 * no return value
 */
void dwt_settxantennadelay(uint16_t antennaDly)
{
    ull_settxantennadelay(dw, antennaDly);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function reads the antenna delay (in time units) from the TX antenna delay register
 *
 * input parameters:
 * @param dw - DW3xxx chip descriptor handler.
 *
 * output parameters
 *
 * returns 16-bit TX antenna delay value which is currently programmed in TX_ANTD_ID register
 */
uint16_t dwt_gettxantennadelay(void)
{
    return ull_gettxantennadelay(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function writes the supplied TX data into the DW3000's
 * TX buffer.  The input parameters are the data length in bytes and a pointer
 * to those data bytes.
 *
 * input parameters
 * @param txDataLength   - This is the total length of data (in bytes) to write to the tx buffer.
 *                         Note: the size of tx buffer is 1024 bytes.
 *                         The standard PHR mode allows to transmit frames of up to 127 bytes (including 2 byte CRC)
 *                         The extended PHR mode allows to transmit frames of up to 1023 bytes (including 2 byte CRC)
 *                         if > 127 is programmed, DWT_PHRMODE_EXT needs to be set in the phrMode configuration
 *                         see dwt_configure function
 * @param txDataBytes    - Pointer to the user's buffer containing the data to send.
 * @param txBufferOffset - This specifies an offset in the DW IC's TX Buffer at which to start writing data.
 *
 * output parameters
 *
 * returns DWT_SUCCESS for success, or DWT_ERROR for error
 */
int32_t dwt_writetxdata(uint16_t txDataLength, uint8_t *txDataBytes, uint16_t txBufferOffset)
{
    return dw->dwt_driver->dwt_ops->write_tx_data(dw, txDataLength, txDataBytes, txBufferOffset);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function configures the TX frame control register before the transmission of a frame
 *
 * input parameters:
 * @param txFrameLength - this is the length of TX message (including the 2 byte CRC) - max is 1023
 *                              NOTE: standard PHR mode allows up to 127 bytes
 *                              if > 127 is programmed, DWT_PHRMODE_EXT needs to be set in the phrMode configuration
 *                              see dwt_configure function
 * @param txBufferOffset - the offset in the tx buffer to start writing the data
 * @param ranging - 1 if this is a ranging frame, else 0
 *
 * output parameters
 *
 * no return value
 */
void dwt_writetxfctrl(uint16_t txFrameLength, uint16_t txBufferOffset, uint8_t ranging)
{
    dw->dwt_driver->dwt_ops->write_tx_fctrl(dw, txFrameLength, txBufferOffset, ranging);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function is used to configure frame preamble length, the frame premable length can be
 * configured in steps of 8, from 16 to 2048 symbols. If a non-zero value is configured, then the TXPSR_PE setting is ignored.
 *
 * input parameters:
 * @param preambleLength - sets the length of the preamble, value of 0 disables this setting and the length of the
 *                         frame will be dependent on the TXPSR_PE setting as configured by dwt_configure function
 * 
 * @note preambleLength is uint16_t only to keep compatibility with QM35xxx devices but cannot be > 0xFF.
 * 
 * Valid range for the preamble length code is [1..0xFF] which corresponds to [16..2048] symbols.
 * You can use convenience constants DWT_PLEN_32..DWT_PLEN_2048 defined for some
 * common preamble lengths. Note that setting preamble length smaller than 32 symbols
 * should be used for testing only and will likely result in poor performance.
 * 
 * output parameters
 *
 * no return value
 */
void dwt_setplenfine(uint16_t preambleLength)
{
    // Make sure preambleLength <= 0xFF
    preambleLength = preambleLength > 0xFFU ? 0xFFU : preambleLength;
    uint8_t preambleLength8Bits = (uint8_t)preambleLength;
    ull_setplenfine(dw, preambleLength8Bits);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This call initiates the transmission, input parameter indicates which TX mode is used see below
 *
 * input parameters:
 * @param mode - if mode = DWT_START_TX_IMMEDIATE - immediate TX (no response expected)
 *               if mode = DWT_START_TX_DELAYED   - delayed TX (no response expected) at specified time (time in DX_TIME register)
 *               if mode = DWT_START_TX_DLY_REF   - delayed TX (no response expected) at specified time
 *                                                  (time in DREF_TIME register + any time in DX_TIME register)
 *               if mode = DWT_START_TX_DLY_RS    - delayed TX (no response expected) at specified time
 *                                                  (time in RX_TIME_0 register + any time in DX_TIME register)
 *               if mode = DWT_START_TX_DLY_TS    - delayed TX (no response expected) at specified time
 *                                                  (time in TX_TIME_LO register + any time in DX_TIME register)
 *               if mode = DWT_START_TX_IMMEDIATE | DWT_RESPONSE_EXPECTED - immediate TX (response expected,
 *                                                                          so the receiver will be automatically
 *                                                                          turned on after TX is done)
 *               if mode = DWT_START_TX_DELAYED | DWT_RESPONSE_EXPECTED - delayed TX (response expected,
 *                                                                        so the receiver will be automatically
 *                                                                        turned on after TX is done)
 *               if mode = DWT_START_TX_CCA        - Send the frame if no preamble detected within PTO time
 *               if mode = DWT_START_TX_CCA  | DWT_RESPONSE_EXPECTED - Send the frame if no preamble detected
 *                                                                     within PTO time and then enable RX output parameters
 *
 * returns DWT_SUCCESS for success, or DWT_ERROR for error (e.g. a delayed transmission will be cancelled if the delayed time has passed)
 */
int32_t dwt_starttx(uint8_t mode)
{
    return ull_starttx(dw, mode);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function configures the reference time used for relative timing of delayed sending and reception.
 * The value is at a 8ns resolution.
 *
 * input parameters
 * @param reftime - the reference time (which together with DX_TIME or TX timestamp or RX timestamp time is used to define a
 * transmission time or delayed RX on time)
 *
 * output parameters none
 *
 * no return value
 */
void dwt_setreferencetrxtime(uint32_t reftime)
{
    ull_setreferencetrxtime(dw, reftime);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API function configures the delayed transmit time or the delayed RX on time
 *
 * input parameters
 * @param starttime - the TX/RX start time (the 32 bits should be the high 32 bits of the system time at which to send the message,
 * or at which to turn on the receiver)
 *
 * output parameters none
 *
 * no return value
 */
void dwt_setdelayedtrxtime(uint32_t starttime)
{
    ull_setdelayedtrxtime(dw, starttime);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the DGC_DECISION index when RX_TUNING is enabled, this value is used to adjust the
 *        RX level and FP level estimation
 *
 * input parameters
 *
 * output parameters - the index value to be used in RX level and FP level formulas
 *
 * no return value
 */
uint8_t dwt_get_dgcdecision(void)
{
    return ull_get_dgcdecision(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the TX timestamp (adjusted with the programmed antenna delay)
 *
 * input parameters
 * @param timestamp - a pointer to a 5-byte buffer which will store the read TX timestamp time
 *
 * output parameters - the timestamp buffer will contain the value after the function call
 *
 * no return value
 */
void dwt_readtxtimestamp(uint8_t *timestamp)
{
    ull_readtxtimestamp(dw, timestamp);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the high 32-bits of the TX timestamp (adjusted with the programmed antenna delay)
 *
 * input parameters
 *
 * output parameters
 *
 * returns high 32-bits of TX timestamp
 */
uint32_t dwt_readtxtimestamphi32(void)
{
    return ull_readtxtimestamphi32(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the low 32-bits of the TX timestamp (adjusted with the programmed antenna delay)
 *
 * input parameters
 *
 * output parameters
 *
 * returns low 32-bits of TX timestamp
 */
uint32_t dwt_readtxtimestamplo32(void)
{
    return ull_readtxtimestamplo32(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the PDOA result, it is the phase difference between either the Ipatov and STS POA, or
 * the two STS POAs, depending on the PDOA mode of operation. (POA - Phase Of Arrival)
 *
 * NOTE: To convert to degrees: float pdoa_deg = ((float)pdoa / (1 << 11)) * 180 / M_PI
 *
 * input parameters
 *
 * output parameters - the PDOA result (signed in [1:-11] radian units)
 *
 * no return value
 */
int16_t dwt_readpdoa(void)
{
    return ull_readpdoa(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function is used to read the TDOA (Time Difference On Arrival). The TDOA value that is read from the
 * register is 41-bits in length. However, 6 bytes (or 48 bits) are read from the register. The remaining 7 bits at
 * the 'top' of the 6 bytes that are not part of the TDOA value should be set to zero and should not interfere with
 * rest of the 41-bit value. However, there is no harm in masking the returned value.
 *
 * input parameters
 *
 * output parameters
 * @param tdoa: time difference on arrival - buffer of 6 bytes that will be filled with TDOA value by calling this function
 *
 * no return value
 */
void dwt_readtdoa(uint8_t *tdoa)
{
    ull_readtdoa(dw, tdoa);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function is used to read the TDOA (Time Difference On Arrival) and the PDOA result (Phase Difference Of Arrival).
 * The device can measure 3 TDOA/PDOA results based on the configuration of the PDOA table.
 *
 * The TDOA value that is read from the register is 16-bits in length. It is a signed number, in device time units.
 *
 * The PDOA value that is read from the register is 15-bits in length. It is a signed number s[1:-11] (radians).
 * NOTE: To convert to degrees: float pdoa_deg = ((float)pdoa / (1 << 11)) * 180 / M_PI
 *
 * input parameters
 *
 * output parameters
 * @param *result - pointer to dwt_pdoa_tdoa_res_t structure which into which PDOA, TDOA and FP_OK will be read
 * @param index   - specifies which of 3 possible results are to be read (0, 1, 2)
 *
 * no return value
 */
void dwt_read_tdoa_pdoa(dwt_pdoa_tdoa_res_t *result, int32_t index)
{
    (void) index;
    uint8_t rd_tdoa[6];
    uint16_t tdoa_shifted;
    dwt_readtdoa(rd_tdoa);
    tdoa_shifted = ((uint16_t)rd_tdoa[0] + ((uint16_t)rd_tdoa[1] << 8U));
    result->tdoa = (int16_t)tdoa_shifted;
    result->pdoa = dwt_readpdoa();
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the RX timestamp (adjusted time of arrival)
 *
 * input parameters
 * @param timestamp - a pointer to a 5-byte buffer which will store the read RX timestamp time
 * @param segment - which IP/STS segment this RX time relates to (see dwt_ip_sts_segment_e) - not used
 *
 * output parameters - the timestamp buffer will contain the value after the function call
 *
 * no return value
 */
void dwt_readrxtimestamp(uint8_t *timestamp, dwt_ip_sts_segment_e segment)
{
    (void) segment; // not used
    dw->dwt_driver->dwt_ops->read_rx_timestamp(dw, timestamp);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the RX timestamp (unadjusted time of arrival)
 *
 * input parameters
 * @param timestamp - a pointer to a 5-byte buffer which will store the read RX timestamp time
 *
 * output parameters - the timestamp buffer will contain the value after the function call
 *
 * no return value
 */
void dwt_readrxtimestampunadj(uint8_t *timestamp)
{
    ull_readrxtimestampunadj(dw, timestamp);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the RX timestamp (adjusted time of arrival) w.r.t. Ipatov CIR
 *
 * input parameters
 * @param timestamp - a pointer to a 5-byte buffer which will store the read RX timestamp time
 *
 * output parameters - the timestamp buffer will contain the value after the function call
 *
 * no return value
 */
void dwt_readrxtimestamp_ipatov(uint8_t *timestamp)
{
    ull_readrxtimestamp_ipatov(dw, timestamp);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the RX timestamp (adjusted time of arrival) w.r.t. STS CIR
 *
 * input parameters
 * @param timestamp - a pointer to a 5-byte buffer which will store the read RX timestamp time
 *
 * output parameters - the timestamp buffer will contain the value after the function call
 *
 * no return value
 */
void dwt_readrxtimestamp_sts(uint8_t *timestamp)
{
    ull_readrxtimestamp_sts(dw, timestamp);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the high 32-bits of the RX timestamp (adjusted with the programmed antenna delay)
 *
 * NOTE: This should not be used when RX double buffer mode is enabled. Following APIs to read RX timestamp should be
 * used:  dwt_readrxtimestamp_ipatov or dwt_readrxtimestamp_sts or dwt_readrxtimestamp
 *
 * input parameters
 *
 * output parameters
 *
 * returns high 32-bits of RX timestamp
 */
uint32_t dwt_readrxtimestamphi32(void)
{
    return ull_readrxtimestamphi32(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the low 32-bits of the RX timestamp (adjusted with the programmed antenna delay)
 *
 * NOTE: This should not be used when RX double buffer mode is enabled. Following APIs to read RX timestamp should be
 * used:  dwt_readrxtimestamp_ipatov or dwt_readrxtimestamp_sts or dwt_readrxtimestamp
 *
 * input parameters
 * @param segment - which IP/STS segment this RX time relates to (see dwt_ip_sts_segment_e) - not used
 *                  segment should be set as DWT_COMPAT_NONE
 * output parameters
 *
 * returns low 32-bits of RX timestamp
 */
uint32_t dwt_readrxtimestamplo32(dwt_ip_sts_segment_e segment)
{
    (void) segment; //not used
    return ull_readrxtimestamplo32(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the high 32-bits of the system time
 *
 * input parameters
 *
 * output parameters
 *
 * returns high 32-bits of system time timestamp
 */
uint32_t dwt_readsystimestamphi32(void)
{
    return ull_readsystimehi32(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the system time
 *
 * input parameters
 * @param timestamp - a pointer to a 4-byte buffer which will store the read system time
 *
 * output parameters
 * @param timestamp - the timestamp buffer will contain the value after the function call
 *
 * no return value
 */
void dwt_readsystime(uint8_t *timestamp)
{
    ull_readsystime(dw, timestamp);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to turn off the transceiver
 *
 * input parameters
 *
 * output parameters
 *
 * no return value
 */
void dwt_forcetrxoff(void)
{
    ull_forcetrxoff(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This call turns on the receiver, can be immediate or delayed (depending on the mode parameter). In the case of a
 * "late" error the receiver will only be turned on if the DWT_IDLE_ON_DLY_ERR is not set.
 * The receiver will stay turned on, listening to any messages until
 * it either receives a good frame, an error (CRC, PHY header, Reed Solomon) or  it times out (SFD, Preamble or Frame).
 *
 * input parameters
 * @param mode - this can be one of the following allowed values:
 *
 * DWT_START_RX_IMMEDIATE      0x00    Enable the receiver immediately
 * DWT_START_RX_DELAYED        0x01    Set up delayed RX, if "late" error triggers, then the RX will be enabled immediately
 * DWT_IDLE_ON_DLY_ERR         0x02    If delayed RX failed due to "late" error then if this
                                       flag is set the RX will not be re-enabled immediately, and device will be in IDLE when function exits
 * DWT_START_RX_DLY_REF        0x04    Enable the receiver at specified time (time in DREF_TIME register + any time in DX_TIME register)
 * DWT_START_RX_DLY_RS         0x08    Enable the receiver at specified time (time in RX_TIME_0 register + any time in DX_TIME register)
 * DWT_START_RX_DLY_TS         0x10    Enable the receiver at specified time (time in TX_TIME_LO register + any time in DX_TIME register)

 * e.g.
 * (DWT_START_RX_DELAYED | DWT_IDLE_ON_DLY_ERR) 0x03 used to disable re-enabling of receiver if delayed RX failed due to "late" error
 *
 * returns DWT_SUCCESS for success, or DWT_ERROR for error (e.g. a delayed receive enable will be too far in the future if delayed time has passed)
 */
int32_t dwt_rxenable(int32_t mode)
{
    return dw->dwt_driver->dwt_ops->rx_enable(dw, mode);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief enable/disable and configure SNIFF mode.
 *
 * SNIFF mode is a low-power reception mode where the receiver is sequenced on and off instead of being on all the time.
 * The time spent in each state (on/off) is specified through the parameters below.
 * See DW3000 User Manual section 4.5 "Low-Power SNIFF mode" for more details.
 *
 * input parameters:
 * @param enable - 1 to enable SNIFF mode, 0 to disable. When 0, all other parameters are not taken into account.
 * @param timeOn - duration of receiver ON phase, expressed in multiples of PAC size. The counter automatically adds 1 PAC
 *                 size to the value set. Min value that can be set is 1 (i.e. an ON time of 2 PAC size), max value is 15.
 * @param timeOff - duration of receiver OFF phase, expressed in multiples of 128/125 us (~1 us). Max value is 255.
 *
 * output parameters
 *
 * no return value
 */
void dwt_setsniffmode(int32_t enable, uint8_t timeOn, uint8_t timeOff)
{
    ull_setsniffmode(dw, enable, timeOn, timeOff);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This call enables the double receive buffer mode
 *
 * input parameters
 * @param dbl_buff_state - enum variable for enabling/disabling double buffering mode
 * @param dbl_buff_mode - enum variable for Receiver Auto-Re-enable
 *
 * output parameters
 *
 * no return value
 */
void dwt_setdblrxbuffmode(dwt_dbl_buff_state_e dbl_buff_state, dwt_dbl_buff_mode_e dbl_buff_mode)
{
    ull_setdblrxbuffmode(dw, dbl_buff_state, dbl_buff_mode);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This call signal to the chip that the specific RX buff is free for fill
 *
 * input parameters
 * @param None
 *
 * output parameters
 *
 * no return value
 */
void dwt_signal_rx_buff_free(void)
{
    ull_signal_rx_buff_free(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This call enables RX timeout (SY_STAT_RFTO event)
 *
 * input parameters
 * @param time - how long the receiver remains on from the RX enable command
 *               The time parameter used here is in 1.0256 us (512/499.2MHz) units
 *               If set to 0 the timeout is disabled.
 *
 * output parameters
 *
 * no return value
 */
void dwt_setrxtimeout(uint32_t rx_time)
{
    ull_setrxtimeout(dw, rx_time);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This call enables preamble timeout (SY_STAT_RXPTO event)
 *
 * input parameters
 * @param  timeout - Preamble detection timeout, expressed in multiples of PAC size. The counter automatically adds 1 PAC
 *                   size to the value set.
 *                   Value 0 will disable the preamble timeout.
 *                   Value X >= 1 that can be set a timeout equal to (X + 1) * PAC
 *
 * output parameters
 *
 * no return value
 */
void dwt_setpreambledetecttimeout(uint16_t timeout)
{
    ull_setpreambledetecttimeout(dw, timeout);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief calibrates the local oscillator as its frequency can vary between 15 and 34kHz depending on temp and voltage
 *
 * NOTE: this function needs to be run before dwt_configuresleepcnt, so that we know what the counter units are
 *
 * input parameters
 *
 * output parameters
 *
 * returns the number of XTAL cycles per low-power oscillator cycle. LP OSC frequency = 38.4 MHz/return value
 */
uint16_t dwt_calibratesleepcnt(void)
{
    return ull_calibratesleepcnt(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief sets the sleep counter to new value, this function programs the high 16-bits of the 28-bit counter
 *
 * NOTE: this function needs to be run before dwt_configuresleep, also the SPI frequency has to be < 3MHz
 *
 * input parameters
 * @param sleepcnt - this it value of the sleep counter to program
 *
 * output parameters
 *
 * no return value
 */
void dwt_configuresleepcnt(uint16_t sleepcnt)
{
    ull_configuresleepcnt(dw, sleepcnt);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief configures the device for both DEEP_SLEEP and SLEEP modes, and on-wake mode
 * i.e. before entering the sleep, the device should be programmed for TX or RX, then upon "waking up" the TX/RX settings
 * will be preserved and the device can immediately perform the desired action TX/RX
 *
 * NOTE: e.g. Tag operation - after deep sleep, the device needs to just load the TX buffer and send the frame
 *
 *      mode:
 *      DWT_PGFCAL       0x0800 - Re-enable receiver on wake-up.
 *      DWT_GOTORX       0x0200
 *      DWT_GOTOIDLE     0x0100
 *      DWT_SEL_OPS      0x0040 | 0x0080
 *      DWT_LOADOPS      0x0020
 *      DWT_LOADLDO      0x0010
 *      DWT_LOADDGC      0x0008
 *      DWT_LOADBIAS     0x0004
 *      DWT_RUNSAR       0x0002
 *      DWT_CONFIG       0x0001 - download the AON array into the HIF (configuration download)
 *
 *      wake: wake up parameters
 *      DWT_SLP_CNT_RPT  0x40 - sleep counter loop after expiration
 *      DWT_PRESRVE_SLP  0x20 - allows for SLEEP_EN bit to be "preserved", although it will self-clear on wake up
 *      DWT_WAKE_WK      0x10 - wake up on WAKEUP PIN
 *      DWT_WAKE_CS      0x8 - wake up on chip select
 *      DWT_BR_DET       0x4 - enable brownout detector during sleep/deep sleep
 *      DWT_SLEEP        0x2 - enable sleep
 *      DWT_SLP_EN       0x1 - enable sleep/deep sleep functionality
 *
 * input parameters
 * @param mode - config on-wake parameters
 * @param wake - config wake up parameters
 *
 * output parameters
 *
 * no return value
 */
void dwt_configuresleep(uint16_t mode, uint8_t wake)
{
    ull_configuresleep(dw, mode, wake);
}

/*! ------------------------------------------------------------------------------------------------------------------
 *
 * @brief this function clears the AON configuration in DW3000
 *
 * input parameters:
 *
 * output parameters
 *
 * no return value
 */
void dwt_clearaonconfig(void)
{
    ull_clearaonconfig(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function puts the device into deep sleep or sleep. dwt_configuresleep() should be called first
 * to configure the sleep and on-wake/wake-up parameters
 *
 * input parameters
 * @param idle_rc - if this is set to DWT_DW_IDLE_RC, the auto INIT2IDLE bit will be cleared prior to going to sleep
 *                  thus after wakeup device will stay in IDLE_RC state
 *
 * output parameters
 *
 * no return value
 */
void dwt_entersleep(int32_t idle_rc)
{
    ull_entersleep(dw, idle_rc);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief sets or clears the auto TX to sleep bit. This means that after a frame
 * transmission the device will enter sleep or deep sleep mode. The dwt_configuresleep() function
 * needs to be called before this to configure the on-wake settings.
 *
 * NOTE: the IRQ line has to be low/inactive (i.e. no pending events)
 *
 * input parameters
 * @param enable - 1 to configure the device to enter sleep or deep sleep after TX, 0 - disables the configuration
 *
 * no return value
 */
void dwt_entersleepaftertx(int32_t enable)
{
    ull_entersleepaftertx(dw, enable);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief Sets or clears the auto TX and/or RX to sleep bits.
 *
 * This makes the device automatically enter deep sleep or sleep mode after a frame transmission and/or reception.
 * dwt_configuresleep() needs to be called before this to configure the sleep and on-wake/wake-up parameters.
 *
 * NOTE: the IRQ line has to be low/inactive (i.e. no pending events)
 *
 * input parameters
 * @param event_mask: bitmask to go to sleep after:
 *  - DWT_TX_COMPLETE to configure the device to enter sleep or deep sleep after TX
 *  - DWT_RX_COMPLETE to configure the device to enter sleep or deep sleep after RX
 *
 * output parameters
 *
 * no return value
 */
void dwt_entersleepafter(int32_t event_mask)
{
    ull_entersleepafter(dw, event_mask);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function is used to register the different callbacks called when one of the corresponding event occurs.
 *
 * NOTE: Callbacks can be undefined (set to NULL). In this case, dwt_isr() will process the event as usual but the 'null'
 * callback will not be called.
 *
 * input parameters
 * @param callbacks - reference to struct containing references for needed callback.
 *
 * output parameters
 *
 * no return value
 */
void dwt_setcallbacks(dwt_callbacks_s *callbacks)
{
    dw->callbacks = *callbacks;
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function checks if the IRQ line is active - this is used instead of interrupt handler
 *
 * input parameters
 *
 * output parameters
 *
 * return value is 1 if the IRQS bit is set and 0 otherwise
 */
uint8_t dwt_checkirq(void)
{
    return ull_checkirq(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function checks if the DW3000 is in IDLE_RC state
 *
 * It is recommended that host waits for SPI_RDY event, which will also generate interrupt once device is ready after reset/power on.
 * If the host cannot use interrupt as a way to check device is ready for SPI comms, then we recommend the host waits for 2 ms and reads this function,
 * which checks if the device is in IDLE_RC state by reading the SYS_STATUS register and checking for the IDLE_RC event to be set.
 * If host initiates SPI transaction with the device prior to it being ready, the SPI transaction may be incorrectly decoded by the device and
 * the device may be misconfigured. Reading registers over SPI prior to device being ready may return garbage on the MISO, which may confuse the host application.
 *
 * input parameters
 *
 * output parameters
 *
 * return value is 1 if the IDLE_RC bit is set and 0 otherwise
 */
uint8_t dwt_checkidlerc(void)
{
    return ull_checkidlerc(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is the DW3000's general Interrupt Service Routine. It will process/report the following events:
 *          - RXFCG (through cbRxOk callback)
 *          - TXFRS (through cbTxDone callback)
 *          - RXRFTO/RXPTO (through cbRxTo callback)
 *          - RXPHE/RXFCE/RXRFSL/RXSFDTO/AFFREJ/LDEERR (through cbRxErr callback)
 *        For all events, corresponding interrupts are cleared and necessary resets are performed. In addition, in the RXFCG case,
 *        received frame information and frame control are read before calling the callback. If double buffering is activated, it
 *        will also toggle between reception buffers once the reception callback processing has ended.
 *
 *        /!\ This version of the ISR supports double buffering but does not support automatic RX re-enabling!
 *
 * NOTE:  In PC based system using (Cheetah or ARM) USB to SPI converter there can be no interrupts, however we still need something
 *        to take the place of it and operate in a polled way. In an embedded system this function should be configured to be triggered
 *        on any of the interrupts described above.

 * input parameters
 *
 * output parameters
 *
 * no return value
 */
void dwt_isr(void)
{
    dw->dwt_driver->dwt_ops->isr(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function enables the specified events to trigger an interrupt.
 * The following events can be found in SYS_ENABLE_LO and SYS_ENABLE_HI registers.
 *
 *
 * input parameters:
 * @param bitmask_lo - sets the events in SYS_ENABLE_LO_ID register which will generate interrupt
 * @param bitmask_hi - sets the events in SYS_ENABLE_HI_ID register which will generate interrupt
 * @param operation  - if set to DWT_ENABLE_INT additional interrupts as selected in the bitmask are enabled
 *                   - if set to DWT_ENABLE_INT_ONLY the interrupts in the bitmask are forced to selected state -
 *                      i.e. the mask is written to the register directly.
 *                   - otherwise (if set to DWT_DISABLE_INT) clear the interrupts as selected in the bitmask
 * output parameters
 *
 * no return value
 */
void dwt_setinterrupt(uint32_t bitmask_lo, uint32_t bitmask_hi, dwt_INT_options_e INT_options)
{
    dw->dwt_driver->dwt_ops->set_interrupt(dw, bitmask_lo, bitmask_hi, INT_options);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to set the PAN ID
 *
 * input parameters
 * @param panID - this is the PAN ID
 *
 * output parameters
 *
 * no return value
 */
void dwt_setpanid(uint16_t panID)
{
    ull_setpanid(dw, panID);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to set 16-bit (short) address
 *
 * input parameters
 * @param shortAddress - this sets the 16 bit short address
 *
 * output parameters
 *
 * no return value
 */
void dwt_setaddress16(uint16_t shortAddress)
{
    ull_setaddress16(dw, shortAddress);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to set the EUI 64-bit (long) address
 *
 * input parameters
 * @param eui64 - this is the pointer to a buffer that contains the 64bit address
 *
 * output parameters
 *
 * no return value
 */
void dwt_seteui(uint8_t *eui64)
{
    ull_seteui(dw, eui64);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to get the EUI 64-bit from the DW3000
 *
 * input parameters
 * @param eui64 - this is the pointer to a buffer that will contain the read 64-bit EUI value
 *
 * output parameters
 *
 * no return value
 */
void dwt_geteui(uint8_t *eui64)
{
    ull_geteui(dw, eui64);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read from AON memory
 *
 * input parameters
 * @param aon_address - this is the address of the memory location to read
 *
 * output parameters - None
 *
 * returns 8-bits read from given AON memory address
 */
uint8_t dwt_aon_read(uint16_t aon_address)
{
    return ull_aon_read(dw, aon_address);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to write to AON memory
 *
 * @param aon_address - this is the address of the memory location to write
 * @param aon_write_data - this is the data to write
 *
 * output parameters - None
 *
 * no return value
 *
 */
void dwt_aon_write(uint16_t aon_address, uint8_t aon_write_data)
{
   return ull_aon_write(dw, aon_address, aon_write_data);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to enable the frame filtering - (the default option is to
 * accept any data and ACK frames with correct destination address
 *
 * input parameters
 * @param enabletype (bitmask) - enables/disables the frame filtering and configures 802.15.4 type
 *       DWT_FF_ENABLE_802_15_4      0x2             - use 802.15.4 filtering rules
 *       DWT_FF_DISABLE              0x0             - disable FF
 * @param filtermode (bitmask) - configures the frame filtering options according to
 *       DWT_FF_BEACON_EN            0x001           - beacon frames allowed
 *       DWT_FF_DATA_EN              0x002           - data frames allowed
 *       DWT_FF_ACK_EN               0x004           - ack frames allowed
 *       DWT_FF_MAC_EN               0x008           - mac control frames allowed
 *       DWT_FF_RSVD_EN              0x010           - reserved frame types allowed
 *       DWT_FF_MULTI_EN             0x020           - multipurpose frames allowed
 *       DWT_FF_FRAG_EN              0x040           - fragmented frame types allowed
 *       DWT_FF_EXTEND_EN            0x080           - extended frame types allowed
 *       DWT_FF_COORD_EN             0x100           - behave as coordinator (can receive frames with no dest address (PAN ID has to match))
 *       DWT_FF_IMPBRCAST_EN         0x200           - allow MAC implicit broadcast
 *
 * output parameters
 *
 * no return value
 */
void dwt_configureframefilter(uint16_t enabletype, uint16_t filtermode)
{
    ull_configureframefilter(dw, enabletype, filtermode);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief  this function is used to calculate 8-bit CRC, it uses 100000111 polynomial (i.e. P(x) = x^8+ x^2+ x^1+ x^0)
 *
 * input parameters:
 * @param byteArray     - data to calculate CRC for
 * @param flen          - length of byteArray
 * @param crcInit       - initialisation value for CRC calculation
 *
 * output parameters
 *
 * returns 8-bit calculate CRC value
 */
uint8_t dwt_generatecrc8(const uint8_t *byteArray, uint32_t flen, uint8_t crcInit)
{
#ifdef DWT_ENABLE_CRC
    uint8_t data;

    /* Divide the message by the polynomial, a byte at a time. */
    for (uint32_t byte = 0UL; byte < flen; ++byte)
    {
        data = byteArray[byte] ^ crcInit;
        crcInit = crcTable[data]; // ^ (crcRemainderInit << 8);
    }
#endif
    /* The final remainder is the CRC. */
    return (crcInit);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to enable SPI CRC check in DW3000
 *
 * input parameters
 * @param crc_mode - if set to DWT_SPI_CRC_MODE_WR then SPI CRC checking will be performed in DW3000 on each SPI write
 *                   last byte of the SPI write transaction needs to be the 8-bit CRC, if it does not match
 *                   the one calculated by DW3000 SPI CRC ERROR event will be set in the status register (SYS_STATUS_SPICRC)
 *
 * @param spireaderr_cb - this needs to contain the callback function pointer which will be called when SPI read error
 *                        is detected (when the DW3000 generated CRC does not match the one calculated by  dwt_generatecrc8
 *                        following the SPI read transaction)
 *
 * output parameters
 *
 * no return value
 */
void dwt_enablespicrccheck(dwt_spi_crc_mode_e crc_mode, dwt_spierrcb_t spireaderr_cb)
{
    ull_enablespicrccheck(dw, crc_mode, spireaderr_cb);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This call enables the auto-ACK feature. If the responseDelayTime (parameter) is 0, the ACK will be sent a.s.a.p.
 * otherwise it will be sent with a programmed delay (in symbols), max is 255.
 * NOTE: needs to have frame filtering enabled as well
 *
 * input parameters
 * @param responseDelayTime - if non-zero the ACK is sent after this delay, max is 255.
 * @param enable - enables or disables the auto-ACK feature
 *
 * output parameters
 *
 * no return value
 */
void dwt_enableautoack(uint8_t responseDelayTime, int32_t enable)
{
    ull_enableautoack(dw, responseDelayTime, enable);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This sets the receiver turn on delay time after a transmission of a frame
 *
 * input parameters
 * @param rxDelayTime - (20 bits) - the delay is in UWB microseconds
 *
 * output parameters
 *
 * no return value
 */
void dwt_setrxaftertxdelay(uint32_t rxDelayTime)
{
    ull_setrxaftertxdelay(dw, rxDelayTime);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function resets the DW3000
 *
 * NOTE: SPI rate must be <= 7MHz before a call to this function as the device will use FOSC/4 as part of internal reset
 *
 * input parameters:
 * @param reset_semaphore - if set to 1 the semaphore will be also reset. (only valid for DW3720 device)
 *
 * output parameters
 *
 * no return value
 */
void dwt_softreset(int32_t reset_semaphore)
{
    ull_softreset(dw, reset_semaphore);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the data from the RX buffer, from an offset location give by offset parameter
 *
 * input parameters
 * @param buffer - the buffer into which the data will be read
 * @param length - the length of data to read (in bytes)
 * @param rxBufferOffset - the offset in the rx buffer from which to read the data
 *
 * output parameters
 *
 * no return value
 */
void dwt_readrxdata(uint8_t *buffer, uint16_t length, uint16_t rxBufferOffset)
{
    dw->dwt_driver->dwt_ops->read_rx_data(dw, buffer, length, rxBufferOffset);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to write the data from the RX scratch buffer, from an offset location given by offset parameter.
 *
 * input parameters
 * @param buffer - the buffer which to write to the device
 * @param length - the length of data to read (in bytes)
 * @param bufferOffset - the offset in the scratch buffer to which to write the data
 *
 * output parameters
 *
 * no return value
 */
void dwt_write_rx_scratch_data(uint8_t *buffer, uint16_t length, uint16_t bufferOffset)
{
    //!!Check later if needs range protection.
    ull_write_rx_scratch_data(dw, buffer, length, bufferOffset);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the data from the RX scratch buffer, from an offset location given by offset parameter.
 *
 * input parameters
 * @param buffer - the buffer into which the data will be read
 * @param length - the length of data to read (in bytes)
 * @param rxBufferOffset - the offset in the rx buffer from which to read the data
 *
 * The Scratch buffer is an special 127-bytes buffer which can be used as an intermediate holder during AES operations.
 *
 * output parameters
 *
 * no return value
 */
void dwt_read_rx_scratch_data(uint8_t *buffer, uint16_t length, uint16_t bufferOffset)
{
    //!!Check later if needs range protection.
    ull_read_rx_scratch_data(dw, buffer, length, bufferOffset);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the 18 bit data from the Accumulator buffer, from an offset location give by offset parameter
 *        for 18 bit complex samples, each sample is 6 bytes (3 real and 3 imaginary)
 *
 *
 * NOTE: Because of an internal memory access delay when reading the accumulator the first octet output is a dummy octet
 *       that should be discarded. This is true no matter what sub-index the read begins at.
 *
 * input parameters
 * @param buffer - the buffer into which the data will be read
 * @param length - the length of data to read (in bytes)
 * @param accOffset - the offset in the acc buffer from which to read the data, this is a complex sample index
 *                    e.g. to read 10 samples starting at sample 100
 *                    buffer would need to be >= 10*6 + 1, length is 61 (1 is for dummy), accOffset is 100
 *
 * output parameters
 *
 * no return value
 *
 * @deprecated This function is now deprecated for new development. Plase use @ref dwt_readcir or @ref dwt_readcir_48b
 */
void dwt_readaccdata(uint8_t *buffer, uint16_t len, uint16_t accOffset)
{
    dw->dwt_driver->dwt_ops->read_acc_data(dw, buffer, len, accOffset);
}

/*!
 * This is used to read complex samples from the CIR/Accumulator buffer specifying the read mode.
 *
 * - Full sample mode: DWT_CIR_READ_FULL:
 * 48 bit complex samples with 24-bit real and 24-bit imaginary (18bits dynamic)
 * - Reduced sample mode: (DWT_CIR_READ_LO, DWT_CIR_READ_MID, DWT_CIR_READ_HI)
 * 32-bit complex samples with 16-bit real and 16-bit imaginary.
 *
 * Note that multiple CIRs cannot be read in one go, as the accumulator memory is not contiguous.
 *
 * Accumulator sizes depend on the accumulator and on the PRF setting, see the following constants
 *     DWT_CIR_LEN_STS
 *     DWT_CIR_LEN_IP_PRF16
 *     DWT_CIR_LEN_IP_PRF64
 *
 * input parameters
 * @param buffer[out] - the buffer into which the data will be read. The buffer should be big enough to accommodate
 *                 num_samples of size 64 bit (2 words) for DWT_CIR_READ_FULL, or 32 bit (1 word) for the "faster"
 *                 reading modes.
 * @param cir_idx[in]      - accumulator index. It is used to defines the CIR accumulator address offset to read from (dwt_acc_idx_e)
 * @param sample_offs[in]   - the sample index offset within the selected accumulator to start reading from
 * @param num_samples[in]   - the number of complex samples to read
 * @param mode[in]          - CIR read mode, see documentation for dwt_cir_read_mode_e
 *
 * @return None
 */
void dwt_readcir(uint32_t *buffer, dwt_acc_idx_e cir_idx, uint16_t sample_offs,
                    uint16_t num_samples, dwt_cir_read_mode_e mode)
{
    dw->dwt_driver->dwt_ops->read_cir( dw , buffer, cir_idx, sample_offs , num_samples , mode );
}

void dwt_readcir_48b(uint8_t *buffer, dwt_acc_idx_e acc_idx, uint16_t sample_offs, uint16_t num_samples){
    // In the QM33 devices the DWT_CIR_READ_FULL is already 48-bit. This function is added only for compatibility with QM35 devices
    dw->dwt_driver->dwt_ops->read_cir( dw , (uint32_t*)(void*)buffer, acc_idx, sample_offs , num_samples , DWT_CIR_READ_FULL );
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the crystal offset (relating to the frequency offset of the far DW3000 device compared to this one)
 *        Note: the returned signed 16-bit number should be divided by 16 to get ppm offset.
 *
 * input parameters - NONE
 *
 * return value - the (int12) signed offset value. (s[-15:-26])
 *                A positive value means the local (RX) clock is running slower than that of the remote (TX) device.
 */
int16_t dwt_readclockoffset(void)
{
    return ull_readclockoffset(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the RX carrier integrator value (relating to the frequency offset of the TX node)
 *
 * input parameters - NONE
 *
 * return value - the (int32_t) signed carrier integrator value.
 *                A positive value means the local (RX) clock is running slower than that of the remote (TX) device.
 */
int32_t dwt_readcarrierintegrator(void)
{
    return ull_readcarrierintegrator(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function enables CIA diagnostic data. When turned on the following registers will be logged:
 * IP_TOA_LO, IP_TOA_HI, STS_TOA_LO, STS_TOA_HI, STS1_TOA_LO, STS1_TOA_HI, CIA_TDOA_0, CIA_TDOA_1_PDOA, CIA_DIAG_0, CIA_DIAG_1
 *
 * input parameters
 * @param enable_mask :     DW_CIA_DIAG_LOG_MAX (0x8)   - CIA to copy to swinging set a maximum set of diagnostic registers in Double Buffer mode
 *                          DW_CIA_DIAG_LOG_MID (0x4)   - CIA to copy to swinging set a medium set of diagnostic registers in Double Buffer mode
 *                          DW_CIA_DIAG_LOG_MIN (0x2)   - CIA to copy to swinging set a minimal set of diagnostic registers in Double Buffer mode
 *                          DW_CIA_DIAG_LOG_ALL (0x1)   - CIA to log all diagnostic registers
 *                          DW_CIA_DIAG_LOG_OFF (0x0)   - CIA to log reduced set of diagnostic registers
 *
 * output parameters
 *
 * no return value
 */
void dwt_configciadiag(uint8_t enable_mask)
{
    ull_configciadiag(dw, enable_mask);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function reads the STS signal quality index
 *
 * input parameters
 * @param rxStsQualityIndex - the (int16_t) signed STS quality index value.
 * @param stsSegment        - not used
 *
 * output parameters
 * return value - >=0 for good and < 0 if bad STS quality.
 *
 * Note: For the 64 MHz PRF if value is >= 90% of the STS length then we can assume good STS reception.
 *       Otherwise the STS timestamp may not be accurate.
 */
int32_t dwt_readstsquality(int16_t *rxStsQualityIndex, int32_t stsSegment)
{
    return ull_readstsquality(dw, rxStsQualityIndex);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function reads the STS status
 *
 * input parameters
 * @param stsstatus - the (uint8_t) STS status value.
 * @param sts_num   - 0 for 1st STS, 1 for 2nd STS (2nd only valid when PDOA Mode 3 is used)
 *
 * output parameters
 * return value 0 for good/valid STS < 0 if bad STS quality.
 */
int32_t dwt_readstsstatus(uint16_t *stsStatus, int32_t sts_num)
{
    return ull_readstsstatus(dw, stsStatus, sts_num);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function reads the RX signal quality diagnostic data
 *
 * input parameters
 * @param diagnostics - diagnostic structure pointer, this will contain the diagnostic data read from the DW3000
 *
 * output parameters
 *
 * no return value
 */
void dwt_readdiagnostics(dwt_rxdiag_t *diagnostics)
{
    ull_readdiagnostics(dw, diagnostics);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to enable/disable the event counter in the IC
 *
 * input parameters
 * @param - enable - 1 enables (and reset), 0 disables the event counters
 * output parameters
 *
 * no return value
 */
void dwt_configeventcounters(int32_t enable)
{
    ull_configeventcounters(dw, enable);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the event counters in the IC
 *
 * input parameters
 * @param counters - pointer to the dwt_deviceentcnts_t structure which will hold the read data
 *
 * output parameters
 *
 * no return value
 */
void dwt_readeventcounters(dwt_deviceentcnts_t *counters)
{
    ull_readeventcounters(dw, counters);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the OTP data from given address into provided array
 *
 * input parameters
 * @param address - this is the OTP address to read from
 * @param array - this is the pointer to the array into which to read the data
 * @param length - this is the number of 32 bit words to read (array needs to be at least this length)
 *
 * output parameters
 *
 * no return value
 */
void dwt_otpread(uint16_t address, uint32_t* array, uint8_t length)
{
    ull_otpread(dw, address, array, length);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to program 32-bit value into the DW3000 OTP memory.
 *
 * input parameters
 * @param value - this is the 32-bit value to be programmed into OTP
 * @param address - this is the 16-bit OTP address into which the 32-bit value is programmed
 *
 * output parameters
 *
 * returns DWT_SUCCESS for success, or DWT_ERROR for error
 */
int32_t dwt_otpwriteandverify(uint32_t value, uint16_t address)
{
    return ull_otpwriteandverify(dw, value, address);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to program 32-bit value into the DW3xxx OTP memory, it will not validate the word was written correctly
 *
 * input parameters
 * @param value - this is the 32-bit value to be programmed into OTP
 * @param address - this is the 16-bit OTP address into which the 32-bit value is programmed
 *
 * output parameters
 *
 * returns DWT_SUCCESS
 */
int32_t dwt_otpwrite(uint32_t value, uint16_t address)
{
    return ull_otpwrite(dw, value, address);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to set up Tx/Rx GPIOs which could be used to control LEDs
 * Note: not completely IC dependent, also needs board with LEDS fitted on right I/O lines
 *       this function enables GPIOs 2 and 3 which are connected to LED3 and LED4 on EVB1000
 *
 * input parameters
 * @param mode - this is a bit field interpreted as follows:
 *          - bit 0: 1 to enable LEDs, 0 to disable them
 *          - bit 1: 1 to make LEDs blink once on init. Only valid if bit 0 is set (enable LEDs)
 *          - bit 2 to 7: reserved
 *
 * output parameters none
 *
 * no return value
 */
void dwt_setleds(uint8_t mode)
{
    ull_setleds(dw, mode);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to adjust the crystal frequency
 *
 * input parameters:
 * @param   value - crystal trim value (in range 0x0 to 0x3F) 64 steps (~1.65ppm per step)
 *
 * output parameters
 *
 * no return value
 */
void dwt_setxtaltrim(uint8_t value)
{
    ull_setxtaltrim(dw, value);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function returns the value of XTAL trim that has been applied during initialisation (dwt_init). This can
 *        be either the value read in OTP memory or a default value.
 *
 * NOTE: The value returned by this function is the initial value only! It is not updated on dwt_setxtaltrim calls.
 *
 * input parameters
 *
 * output parameters
 *
 * returns the XTAL trim value set upon initialisation
 */
uint8_t dwt_getxtaltrim(void)
{
    return ull_getxtaltrim(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function disables repeated frames from being generated.
 *
 * input parameters:
 * None
 *
 * output parameters:
 * None
 *
 * No return value
 */
void dwt_stop_repeated_frames(void)
{
    ull_stop_repeated_frames(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function enables repeated frames to be generated given a frame repetition rate.
 *
 * input parameters:
 * @param framerepetitionrate - Value specifying the rate at which frames will be repeated.
 *                            If the value is less than the frame duration, the frames are sent
 *                            back-to-back.
 *
 * output parameters:
 * None
 *
 * No return value
 */
void dwt_repeated_frames(uint32_t framerepetitionrate)
{
    ull_repeated_frames(dw, framerepetitionrate);
}


/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function enables preamble test mode which sends a preamble pattern for duration specified by delay parameter.
 *        Once the delay expires, the device goes back to normal mode.
 *
 * input parameters
 * @param delay         - this is the duration of the preamble transmission in us
 * @param test_txpower  - this is the TX power to be applied while transmitting preamble
 * output parameters
 *
 * no return value
 */
void dwt_send_test_preamble(uint16_t delay, uint32_t test_txpower)
{
    ull_send_test_preamble(dw, delay, test_txpower);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will enable a repeated continuous waveform on the device
 *
 * input parameters:
 * @param cw_enable: CW mode enable
 * @param cw_mode_config: CW configuration mode.
 *
 * output parameters:
 *
 */
void dwt_repeated_cw(int32_t cw_enable, int32_t cw_mode_config)
{
    ull_repeated_cw(dw, cw_enable, cw_mode_config);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function sets the DW3000 to transmit cw signal at specific channel frequency
 *
 * input parameters
 *
 * output parameters
 *
 * no return value
 */
void dwt_configcwmode(void)
{
    ull_configcwmode(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function sets the DW3000 to continuous tx frame mode for regulatory approvals testing.
 *
 * input parameters:
 * @param framerepetitionrate - This is a 32-bit value that is used to set the interval between transmissions.
 *  The minimum value is 2. The units are approximately 4 ns. (or more precisely 512/(499.2e6*256) seconds)).
 *
 * output parameters
 *
 * no return value
 */
void dwt_configcontinuousframemode(uint32_t framerepetitionrate)
{
    ull_configcontinuousframemode(dw, framerepetitionrate);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function stops the continuous tx frame mode.
 *
 * input parameters:
 *
 * output parameters
 *
 * no return value
 */
void dwt_disablecontinuousframemode(void)
{
    ull_disablecontinuousframemode(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function stops the continuous wave mode of the DW3xxx.
 *
 * input parameters:
 * @param dw - DW3xxx chip descriptor handler.
 *
 * output parameters
 *
 * no return value
 */
void dwt_disablecontinuouswavemode(void)
{
    ull_disablecontinuouswavemode(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function reads the raw battery voltage and temperature values of the DW IC.
 * The values read here will be the current values sampled by DW IC AtoD converters.
 *
 *
 * input parameters:
 *
 * output parameters
 *
 * returns  (temp_raw<<8)|(vbat_raw)
 */
uint16_t dwt_readtempvbat(void)
{
    return ull_readtempvbat(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief  this function takes in a raw temperature value and applies the conversion factor
 * to give true temperature. The dwt_initialise needs to be called before call to this to
 * ensure pdw3000local->tempP contains the SAR_LTEMP value from OTP.
 *
 * input parameters:
 * @param raw_temp - this is the 8-bit raw temperature value as read by dwt_readtempvbat
 *
 * output parameters:
 *
 * returns: temperature sensor value
 */
float dwt_convertrawtemperature(uint8_t raw_temp)
{
    return ull_convertrawtemperature(dw, raw_temp);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function takes in a raw voltage value and applies the conversion factor
 * to give true voltage. The dwt_initialise needs to be called before call to this to
 * ensure pdw3000local->vBatP contains the SAR_LVBAT value from OTP
 *
 * input parameters:
 * @param raw_voltage - this is the 8-bit raw voltage value as read by dwt_readtempvbat
 *
 * output parameters:
 *
 * returns: voltage sensor value
 */
float dwt_convertrawvoltage(uint8_t raw_voltage)
{
    return ull_convertrawvoltage(dw, raw_voltage);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function reads the temperature of the DW3000 that was sampled
 * on waking from Sleep/Deepsleep. They are not current values, but read on last
 * wakeup if DWT_TANDV bit is set in mode parameter of dwt_configuresleep
 *
 * input parameters:
 *
 * output parameters:
 *
 * returns: 8-bit raw temperature sensor value
 */
uint8_t dwt_readwakeuptemp(void)
{
    return ull_readwakeuptemp(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function reads the battery voltage of the DW3000 that was sampled
 * on waking from Sleep/Deepsleep. They are not current values, but read on last
 * wakeup if DWT_TANDV bit is set in mode parameter of dwt_configuresleep
 *
 * input parameters:
 *
 * output parameters:
 *
 * returns: 8-bit raw battery voltage sensor value
 */
uint8_t dwt_readwakeupvbat(void)
{
    return ull_readwakeupvbat(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief Returns the PG delay value of the TX
 *
 * input parameters
 *
 * output parameters
 *
 * returns uint8_t
 */
uint8_t dwt_readpgdelay(void)
{
    return ull_readpgdelay(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function determines the adjusted bandwidth setting (PG_DELAY bitfield setting)
 * of the DW3000. The adjustemnt is a result of DW3000 internal PG cal routine, given a target count value it will try to
 * find the PG delay which gives the closest count value.
 * Manual sequencing of TX blocks and TX clocks need to be enabled for either channel 5 or 9.
 * This function presumes that the PLL is already in the IDLE state. Please configure the PLL to IDLE
 * state before calling this function, by calling dwt_configure.
 *
 * input parameters:
 * @param target_count - uint16_t - the PG count target to reach in order to correct the bandwidth
 *
 * output parameters:
 * returns: (uint8_t) The setting that was written to the PG_DELAY register (when calibration completed)
 */
uint8_t dwt_calcbandwidthadj(uint16_t target_count)
{
    return ull_calcbandwidthadj(dw, target_count);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this function calculates the value in the pulse generator counter register (PGC_STATUS) for a given PG_DELAY
 * This is used to take a reference measurement, and the value recorded as the reference is used to adjust the
 * bandwidth of the device when the temperature changes. This function presumes that the PLL is already in the IDLE
 * state.
 *
 * input parameters:
 * @param pgdly - uint8_t - the PG_DELAY (max value 63) to set (to control bandwidth), and to find the corresponding count value for
 *
 * output parameters:
 * returns (uint16_t) - The count value calculated from the provided PG_DELAY value (from PGC_STATUS) - used as reference
 * for later bandwidth adjustments
 */
uint16_t dwt_calcpgcount(uint8_t pgdly)
{
    return ull_calcpgcount(dw, pgdly);
}

/********************************************************************************************************************/
/*                                                AES BLOCK                                                         */
/********************************************************************************************************************/

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief   This function provides the API for the configuration of the AES key before first usage.
 *
 * input parameters
 * @param   key - pointer to the key which will be programmed to the Key register
 *          Note, key register supports only 128-bit keys.
 *
 * output parameters
 *
 * no return value
 */
void dwt_set_keyreg_128(dwt_aes_key_t *key)
{
    ull_set_keyreg_128(dw, key);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief   This function provides the API for the configuration of the AES block before its first usage.
 *
 * input parameters
 * @param   pCfg - pointer to the configuration structure, which contains the AES configuration data.
 *
 * output parameters
 *
 * no return value
 */
void dwt_configure_aes(dwt_aes_config_t *pCfg)
{
    ull_configure_aes(dw, pCfg);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief   This gets mic size in bytes and convert it to value to write in AES_CFG
 * @param   mic_size_in_bytes - mic size in bytes.
 *
 * @Return  dwt_mic_size_e - reg value number
 */
dwt_mic_size_e dwt_mic_size_from_bytes(uint8_t mic_size_in_bytes)
{
    return ull_mic_size_from_bytes(dw, mic_size_in_bytes);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief   This function provides the API for the job of encrypt/decrypt the data block
 *
 *          128 bit key shall be pre-loaded with dwt_set_aes_key()
 *          dwt_configure_aes
 *
 *          supports AES_KEY_Src_Register mode only
 *          packet sizes < 127
 *          note, the "nonce" shall be unique for every transaction
 *
 * input parameters
 * @param job - pointer to AES job, contains data info and encryption info.
 * @param core_type - Core type
 *
 * @return  AES_STS_ID status bits
 */
int8_t dwt_do_aes(dwt_aes_job_t *job, dwt_aes_core_type_e core_type)
{
    return ull_do_aes(dw, job, core_type);
}

/****************************************************************************************************************************************************
 *
 * Declaration of platform-dependent lower level functions.
 *
 ****************************************************************************************************************************************************/

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief  This function wakeup device by an IO pin
 *
 * @param None
 *
 * output parameters
 *
 * no return value
 */
void dwt_wakeup_ic(void)
{
    dw->wakeup_device_with_io();
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief this reads the device ID and checks if it is the right one
 *
 * input parameters
 * None
 *
 * output parameters
 *
 * returns DWT_SUCCESS for success, or DWT_ERROR for error
 */
int32_t dwt_check_dev_id(void)
{
    return ull_check_dev_id(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 *
 * @brief This function runs the PGF calibration. This is needed prior to reception.
 * Note: If the RX calibration routine fails the device receiver performance will be severely affected, the application should reset and try again
 *
 * input parameters
 * @param ldoen    -   if set to 1 the function will enable LDOs prior to calibration and disable afterwards.
 *
 * return result of PGF calibration (DWT_ERROR/-1 = error)
 */
int32_t dwt_run_pgfcal(void)
{
    return ull_run_pgfcal(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function runs the PGF calibration. This is needed prior to reception.
 *
 * input parameters
 * @param ldoen    -   if set to 1 the function will enable LDOs prior to calibration and disable afterwards.
 *
 * return result of PGF calibration (0 = error)
 */
int32_t dwt_pgf_cal(int32_t ldoen)
{
    return ull_pgf_cal(dw, ldoen);
}

/*! ------------------------------------------------------------------------------------------------------------------
* @brief Read the current value of the PLL status register (32 bits)
*
* The status bits are defined as follows:
*
* - PLL_STATUS_LD_CODE_BIT_MASK          0x1f00U - Counter-based lock-detect status indicator
* - PLL_STATUS_XTAL_AMP_SETTLED_BIT_MASK 0x40U   - Status flag from the XTAL indicating that the amplitude has settled
* - PLL_STATUS_VCO_TUNE_UPDATE_BIT_MASK  0x20U   - Flag to indicate that the COARSE_TUNE codes have been updated by cal and are ready to read
* - PLL_STATUS_PLL_OVRFLOW_BIT_MASK      0x10U   - PLL calibration flag indicating all VCO_TUNE values have been cycled through
* - PLL_STATUS_PLL_HI_FLAG_BIT_MASK      0x8U    - VCO voltage too high indicator (active-high)
* - PLL_STATUS_PLL_LO_FLAG_N_BIT_MASK    0x4U    - VCO voltage too low indicator (active-low)
* - PLL_STATUS_PLL_LOCK_FLAG_BIT_MASK    0x2U    - PLL lock flag
* - PLL_STATUS_CPC_CAL_DONE_BIT_MASK     0x1U    - PLL cal done and PLL locked
*
*
* returns A uint32_t value containing the value of the PLL status register (only bits [14:0] are valid)
*/
uint32_t dwt_readpllstatus(void){
    return ull_readpllstatus(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief
 * This function will re-calibrate and re-lock the PLL. If the cal/lock is successful DWT_SUCCESS
 * will be returned otherwise DWT_ERROR will be returned
 *
 * input parameters:None
 *
 * output parameters:
 * returns DWT_SUCCESS for success or DWT_ERROR for error.
 */
int32_t dwt_pll_cal(void)
{
    return ull_pll_cal(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function is used to control what rf port to use for TX/RX.
 *
 * input params :
 * @param port_control - enum value for enabling or disabling manual control and primary antenna.
 *
 * No return value
 */
void dwt_configure_rf_port(dwt_rf_port_ctrl_e port_control)
{
    ull_configure_rf_port(dw, port_control);
}

/*! ------------------------------------------------------------------------------------------------------------------
 *
 * @brief   This function is used to write a 16 bit address to a desired Low-Energy device (LE) address. For frame pending to function when
 * the correct bits are set in the frame filtering configuration via the dwt_configureframefilter. See dwt_configureframefilter for more details.
 *
 * @param addr - the address value to be written to the selected LE register
 * @param leIndex - Low-Energy device (LE) address to write to
 *
 * no return value
 */
void dwt_configure_le_address(uint16_t addr, int32_t leIndex)
{
    ull_configure_le_address(dw, addr, leIndex);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function configures SFD type only: e.g. IEEE 4a - 8, DW-8, DW-16, or IEEE 4z -8 (binary)
 * The dwt_configure should be called prior to this to configure other parameters
 *
 * input parameters
 * @param sfdType    -   e.g. DWT_SFD_IEEE_4A, DWT_SFD_DW_8, DWT_SFD_DW_16, DWT_SFD_IEEE_4Z
 *
 * return none
 */
void dwt_configuresfdtype(uint8_t sfdType)
{
    ull_configuresfdtype(dw, sfdType);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief  this function allows read from the DW3xxx device 32-bit register
 *
 * input parameters:
 * @param address - ID of the DW3xxx register
 *
 * return - value of the 32-bit register
 *
 */
uint32_t dwt_read_reg(uint32_t address)
{
    return dwt_read32bitoffsetreg(dw, address, 0);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief  this function allows write to the DW3xxx device 32-bit register
 *
 * input parameters:
 * @param address - ID of the DW3xxx register
 *        data    - value to write
 *
 */
void dwt_write_reg(uint32_t address, uint32_t data)
{
    dwt_write32bitoffsetreg(dw, address, 0, data);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function writes a value to the system status register (lower).
 *
 * input parameters
 * @param mask - mask value to send to the system status register (lower 32-bits).
 *               e.g. "SYS_STATUS_TXFRS_BIT_MASK" to clear the TX frame sent event.
 *
 * return none
 */
void dwt_writesysstatuslo(uint32_t mask)
{
    ull_writesysstatuslo(dw, mask);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function writes a value to the system status register (higher).
 *
 * input parameters
 * @param mask - mask value to send to the system status register (higher bits).
 *               NOTE: Be aware that the size of this register varies per device.
 *               DW3000 devices only require a 16-bit mask value typecast to 32-bit.
 *               DW3720 devices require a 32-bit mask value.
 *
 * return none
 */
void dwt_writesysstatushi(uint32_t mask)
{
    ull_writesysstatushi(dw, mask);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function reads the current value of the system status register (lower 32 bits)
 *
 * input parameters
 *
 * return A uint32_t value containing the value of the system status register (lower 32 bits)
 */
uint32_t dwt_readsysstatuslo(void)
{
    return ull_readsysstatuslo(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function reads the current value of the system status register (higher bits)
 *
 * input parameters
 *
 * return A uint32_t value containing the value of the system status register (higher bits)
 *        NOTE: Be aware that the size of this register varies per device.
 *        DW3000 devices will return a 16-bit value of the register that is typecast to a 32-bit value.
 *        DW3720 devices will return a 'true' 32-bit value of the register.
 */
uint32_t dwt_readsysstatushi(void)
{
    return ull_readsysstatushi(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function writes a value to the Receiver Double Buffer status register.
 *
 * input parameters
 * @param mask - mask value to send to the register.
 *               e.g. "RDB_STATUS_CLEAR_BUFF0_EVENTS" to clear the clear buffer 0 events.
 *
 * return none
 */
void dwt_writerdbstatus(uint8_t mask)
{
    ull_writerdbstatus(dw, mask);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function reads the current value of the Receiver Double Buffer status register.
 *
 * input parameters
 *
 * @return A uint8_t value containing the value of the Receiver Double Buffer status register.
 */
uint8_t dwt_readrdbstatus(void)
{
    return ull_readrdbstatus(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will read the frame length of the last received frame.
 *        This function presumes that a good frame or packet has been received.
 *
 * input parameters
 * @param rng_bit - this is an output, the parameter will have DWT_CB_DATA_RX_FLAG_RNG set if RNG bit is set in FINFO
 *
 * return frame_len - A uint16_t with the number of octets in the received frame.
 */
uint16_t dwt_getframelength(uint8_t *rng)
{
    return ull_getframelength(dw, rng);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the value stored in CIA_ADJUST_ID register
 *
 * input parameters
 *
 * output parameters
 *
 * returns value stored in CIA_ADJUST_ID register
 */
uint32_t dwt_readpdoaoffset(void)
{
    return dwt_read32bitoffsetreg(dw, CIA_ADJUST_ID, 0);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will set the value to the CIA_ADJUST_ID register.
 *
 * input parameters
 * @param offset - the offset value to be written into the CIA_ADJUST_ID register.
 *
 * return None.
 */
void dwt_setpdoaoffset(uint16_t offset)
{
    ull_setpdoaoffset(dw, offset);
}
/* BEGIN: CHIP_SPECIFIC_SECTION D0 */

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function enables the specified double RX buffer to trigger an interrupt.
 * The following events can be found in RDB_STAT_EN_ID registers.
 *
 * input parameters:
 * @param bitmask    - sets the events in RDB_STAT_EN_ID register which will generate interrupt
 * @param operation  - if set to DWT_ENABLE_INT additional interrupts as selected in the bitmask are enabled
 *                   - if set to DWT_ENABLE_INT_ONLY the interrupts in the bitmask are forced to selected state -
 *                      i.e. the mask is written to the register directly.
 *                   - otherwise (if set to DWT_DISABLE_INT) clear the interrupts as selected in the bitmask
 * output parameters
 *
 * no return value
 */
void dwt_setinterrupt_db(uint8_t bitmask, dwt_INT_options_e INT_options)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_setinterrupt_db(dw, bitmask, INT_options);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 *
 * @brief Request access to the device registers, using the dual SPI semaphore request command. If the semaphore is available,
 * the semaphore will be given.
 * NOTE: dwt_ds_sema_status() should be used to get semaphore status value.
 *
 * input parameters
 * @param
 *
 * @return None
 */
void dwt_ds_sema_request(void)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_ds_sema_request(dw);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 *
 * @brief Release the semaphore that was taken by this host
 *
 * input parameters
 *
 * output parameters
 *
 * return None
 */
void dwt_ds_sema_release(void)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_ds_sema_release(dw);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This can be used by host on the SPI2 to force taking of the semaphore. Take semaphore even if it is not available.
 *        This does not apply to host on SPI1, only host on SPI2 can force taking of the semaphore.
 *
 * input parameters
 *
 * output parameters
 *
 * return None
 */
void dwt_ds_sema_force(void)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_ds_sema_force(dw);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief Reports the semaphore status low byte.
 *
 * input parameters
 *
 * output parameters
 *
 * @return semaphore value
 */
uint8_t dwt_ds_sema_status(void)
{
#if CONFIG_DW3000_CHIP_DW3720
    return ull_ds_sema_status(dw);
#else
    return 0;
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief Reports the semaphore status high byte.
 *
 * input parameters
 *
 * output parameters
 *
 * @return semaphore value
 */
uint8_t dwt_ds_sema_status_hi(void)
{
#if CONFIG_DW3000_CHIP_DW3720
    return ull_ds_sema_status_hi(dw);
#else
    return 0;
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief With this API each host can prevent the device going into Sleep/Deepsleep state.
 * By default it is possible for either host to place the device into Sleep/Deepsleep. This may not be desirable,
 * thus a host once it is granted access can set a SLEEP_DISABLE bit in the register
 * to prevent the other host from putting the device to sleep once it gives up its access.
 *
 * @param host_sleep_en - HOST_EN_SLEEP: clears the bit - allowing the the device to go to sleep.
 *                        HOST_DIS_SLEEP: sets the bit to prevent the device from going to sleep
 *
 * return None
 */
void dwt_ds_en_sleep(dwt_host_sleep_en_e host_sleep_en)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_ds_en_sleep(dw, host_sleep_en);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
*
* @brief With this API the host on either SPI1 or SPI2 can enable/disable whether the interrupt is raised upon
* SPI1MAVAIL or SPI2MAVAIL event.
*
* @param dwt_spi_host_e spi_num - should be set to either DWT_HOST_SPI1 or DWT_HOST_SPI2
* @param dwt_INT_options_e int_set    - should be set to either DWT_ENABLE_INT or DWT_DISABLE_INT
*
* return DWT_SUCCESS or DWT_ERROR (if input parameters not consistent)
*/
int32_t dwt_ds_setinterrupt_SPIxavailable(dwt_spi_host_e spi_num, dwt_INT_options_e int_set)
{
#if CONFIG_DW3000_CHIP_DW3720
    return ull_ds_setinterrupt_SPIxavailable(dw, spi_num, int_set);
#else
    return 0;
#endif
}
/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function enables or disables the equaliser block within in the CIA. The equaliser should be used when
 * receiving from devices which transmit using a Symmetric Root Raised Cosine pulse shape. The equaliser will adjust
 * the CIR to give improved receive timestamp results. Normally, this is left disabled (the default value), which
 * gives the best receive timestamp performance when interworking with devices (like this IC) that use the
 * IEEE 802.15.4z recommended minimum precursor pulse shape.
 *
 * @param en - DWT_EQ_ENABLED or DWT_EQ_DISABLED, enables/disables the equaliser block
 */
void dwt_enable_disable_eq(uint8_t en)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_enable_disable_eq(dw, en);
#endif
}

/* END: CHIP_SPECIFIC_SECTION D0 */

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will reset the timers block. It will reset both timers. It can be used to stop a timer running
 * in repeat mode.
 *
 * input parameters
 *
 * return none
 *
 */
void dwt_timers_reset(void)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_timers_reset(dw);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will read the timers' event counts. When reading from this register the values will be reset/cleared,
 * thus the host needs to read both timers' event counts the events relating to TIMER0 are in bits [7:0] and events
 * relating to TIMER1 in bits [15:8].
 *
 * input parameters
 *
 * return event counts from both timers: TIMER0 events in bits [7:0], TIMER1 events in bits [15:8]
 *
 */
uint16_t dwt_timers_read_and_clear_events(void)
{
#if CONFIG_DW3000_CHIP_DW3720
    return ull_timers_read_and_clear_events(dw);
#else
    return 0;
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function configures selected timer (TIMER0 or TIMER1) as per configuration structure
 *
 * input parameters
 * @param tim_cfg       - pointer to timer configuration structure
 *
 * return none
 *
 */
void dwt_configure_timer(dwt_timer_cfg_t *tim_cfg)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_configure_timer(dw, tim_cfg);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function configures the GPIOs (4 and 5) for COEX_OUT
 *
 * input parameters
 * @param timer_coexout - configure if timer controls the COEX_OUT
 * @param coex_swap     - configures if the COEX_OUT is on GPIO4 or GPIO5, when set to 1 the GPIO4 will be COEX_OUT
 *
 * return none
 *
 */
void dwt_configure_wificoex_gpio(uint8_t timer_coexout, uint8_t coex_swap)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_configure_wificoex_gpio(dw, timer_coexout, coex_swap);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function drive the antenna configuration GPIO6/7
 *
 * input parameters
 * @param antenna_config - configure GPIO 6 and or 7 to use for Antenna selection with expected value.
 *      bitfield configuration:
 *      Bit 0: Use GPIO 6
 *      Bit 1: Value to apply (0/1)
 *      Bit 2: Use GPIO 7
 *      Bit 3: Value to apply (0/1)
 *
 * return none
 *
 */
void dwt_configure_and_set_antenna_selection_gpio(uint8_t antenna_config)
{
    ull_configure_and_set_antenna_selection_gpio(dw, antenna_config);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function sets timer expiration period, it is a 22-bit number
 *
 * input parameters
 * @param timer_name - specify which timer period to set: TIMER0 or TIMER1
 * @param expiration - expiry count - e.g. if units are XTAL/64 (1.66 us) then setting 1024 ~= 1.7 ms period
 *
 * return none
 *
 */
void dwt_set_timer_expiration(dwt_timers_e timer_name, uint32_t expiration)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_set_timer_expiration(dw, timer_name, expiration);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function enables the timer. In order to enable, the timer enable bit [0] for TIMER0 or [1] for TIMER1
 * needs to transition from 0->1.
 *
 * input parameters
 * @param timer_name - specifies which timer to enable
 *
 * return none
 *
 */
void dwt_timer_enable(dwt_timers_e timer_name)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_timer_enable(dw, timer_name);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function can set GPIO output to high (1) or low (0) which can then be used to signal e.g. WiFi chip to
 * turn off or on. This can be used in devices with multiple radios to minimise co-existence interference.
 *
 * input parameters
 * @param enable       - specifies if to enable or disable WiFi co-ex functionality on GPIO5 (or GPIO4)
 *                       depending if coex_io_swap param is set to 1 or 0
 * @param coex_io_swap -  when set to 0, GPIO5 is used as co-ex out, otherwise GPIO4 is used
 *
 * return event counts from both timers: TIMER0 events in bits [7:0], TIMER1 events in bits [15:8]
 *
 */
void dwt_wifi_coex_set(dwt_wifi_coex_e enable, int32_t coex_io_swap)
{
    ull_wifi_coex_set(dw, enable, coex_io_swap);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will reset the internal system time counter. The counter will be momentarily reset to 0,
 * and then will continue counting as normal. The system time/counter is only available when device is in
 * IDLE or TX/RX states.
 *
 * input parameters
 *
 * return
 * none
 *
 */
void dwt_reset_system_counter(void)
{
    ull_reset_system_counter(dw);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function is used to configure the device for OSTR mode (One Shot Timebase Reset mode), this will
 * prime the device to reset the internal system time counter on SYNC pulse / SYNC pin toggle.
 * For more information on this operation please consult the device User Manual.
 *
 * input parameters
 * @param  enable       - Set to 1 to enable OSTR mode and 0 to disable
 * @param  wait_time    - When a counter running on the 38.4 MHz external clock and initiated on the rising edge
 *                        of the SYNC signal equals the WAIT programmed value, the DW3xxx timebase counter will be reset.
 *
 * NOTE: At the time the SYNC signal is asserted, the clock PLL dividers generating the DW3xxx 125 MHz system clock are reset,
 * to ensure that a deterministic phase relationship exists between the system clock and the asynchronous 38.4 MHz external clock.
 * For this reason, the WAIT value programmed will dictate the phase relationship and should be chosen to give the
 * desired phase relationship, as given by WAIT modulo 4. A WAIT value of 33 decimal is recommended,
 * but if a different value is chosen it should be chosen so that WAIT modulo 4 is equal to 1, i.e. 29, 37, and so on.
 *
 * return
 * none
 *
 */
void dwt_config_ostr_mode(uint8_t enable, uint16_t wait_time)
{
    ull_config_ostr_mode(dw, enable, wait_time);
}
/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API enables "Fixed STS" function. The fixed STS function means that the same STS will be sent in each packet.
 * And also in the receiver, when the receiver is enabled the STS will be reset. Thus transmitter and the receiver will be in sync.
 *
 * input parameters
 * @param set - Set to 1 to set FIXED STS and 0 to disable
 *
 * return
 * none
 *
 */
 void dwt_set_fixedsts(uint8_t set)
 {
#if CONFIG_DW3000_CHIP_DW3720
    ull_set_fixedsts(dw, set);
#endif
 }

 /*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the value stored in CTR_DBG_ID register, these are the low 32-bits of the STS IV counter.
 *
 * input parameters
 *
 * output parameters
 *
 * returns value stored in CTR_DBG_ID register
 */
 uint32_t dwt_readctrdbg(void)
 {
     return dwt_read32bitoffsetreg(dw, CTR_DBG_ID, 0);
 }

 /*! ------------------------------------------------------------------------------------------------------------------
 * @brief This is used to read the value stored in DGC_DBG_ID register.
 *
 * input parameters
 *
 * output parameters
 *
 * returns value stored in DGC_DBG_ID register
 */
 uint32_t dwt_readdgcdbg(void)
 {
     return dwt_read32bitoffsetreg(dw, DGC_DBG_ID, 0);
 }

 /*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function read CIA version in this device.
 *
 * input parameters
 * @param dw - DW3xxx chip descriptor handler.
 *
 * return
 * none
 *
 */
 uint32_t dwt_readCIAversion(void)
 {
     return ull_readCIAversion(dw);
 }

/*! ------------------------------------------------------------------------------------------------------------------
* @brief This is used to return base address of ACC_MEM_ID register (CIR base address)
*
* input parameters
*
* output parameters
*
* returns address of ACC_MEM_ID register
*/
 uint32_t dwt_getcirregaddress(void)
 {
     return ACC_MEM_ID;
 }

 /*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API enables returns a list of register name/value pairs, to enable debug output / logging in external applications
 * e.g. DecaRanging
 *
 * input parameters
 * @param regs - Pointer to registers structure register_name_add_t, will be returned
 *
 * return
 * none
 *
 */
 register_name_add_t* dwt_get_reg_names(void)
 {
    // NOT IMPLEMENTED
    return NULL;
 }

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API sets the Alternative Pulse Shape according to ARIB.
 *
 * input parameters
 * @param set_alternate - Set to 1 to enable the alternate pulse shape and 0 to restore default shape.
 *
 * return
 * none
 *
 */
void dwt_set_alternative_pulse_shape(uint8_t set_alternate)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_set_alternate_pulse_shape(dw, set_alternate);
#endif
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will read the Diagnostics Registers - IPATOV, STS1, STS2 from the device, which can help in
 *        determining if packet has been received in LOS (line-of-sight) or NLOS (non-line-of-sight) condition.
 *        To help determine/estimate NLOS condition either Ipatov, STS1 or STS2 can be used, (or all three).
 *
 * NOTE:  CIA Diagnostics need to be enabled to "DW_CIA_DIAG_LOG_ALL" else the diagnostic registers read will be 0.
 * input parameters:
 * @param dw        - DW3xxx chip descriptor handler.
 *
 * @param all_diag  - this is the pointer to the Structure into which to read the data.
 *
 * @return a uint8_t value indicating if DWT_SUCCESS if right enum is used else DWT_ERROR.
 */
uint8_t dwt_nlos_alldiag(dwt_nlos_alldiag_t *all_diag)
{
    return ull_nlos_alldiag(dw, all_diag);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will read the IPATOV Diagnostic Registers to get the First Path and Peak Path Index value.
 *        This function is used when signal power is low to determine the signal type (LOS or NLOS). Hence only
 *        Ipatov diagnostic registers are used to determine the signal type.
 *
 * input parameters:
 * @param dw        - DW3xxx chip descriptor handler.
 *
 * @param index - this is the pointer to the Structure into which to read the data.
 *
 */
void dwt_nlos_ipdiag(dwt_nlos_ipdiag_t *index)
{
    ull_nlos_ipdiag(dw, index);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function calculates the adjusted TxPower setting by applying a boost over a reference TxPower setting.
 * The reference TxPower setting should correspond to a 1ms frame (or 0dB) boost.
 * The boost to be applied should be provided in unit of 0.1dB boost.
 * For example, for a 125us frame, a theoretical boost of 9dB can be applied. A boost of 90 should be provided as input
 * parameter and will be applied over the reference TxPower setting for a 1ms frame.
 *
 * input parameters
 * @param boost - the boost to apply in 0.1dB units.
 * DW3XXX maximum boost is 354 in channel 5, 305 in channel 9. If the input value is greater than the maximum boost,
 * then it will be discarded and maximum boost will be targeted.
 * @param ref_tx_power - the tx_power_setting corresponding to a frame of 1ms (0dB boost)
 * @param channel - the current RF channel used for transmission of UWB frames
 * @param adj_tx_power - if successful, the adjusted tx power setting will be returned through this pointer
 * @param applied_boost - if successful, the exact amount of boost applied will be returned through this pointer
 *
 * return
 * int: DWT_SUCCESS: if an adjusted tx power setting could be calculated. In this case, the actual amount of boost that was
 * applied and the adjusted tx power setting will be respectively returned through the parameters adj_tx_power and boost
 *      DWT_ERROR: if the API could not calculate a valid adjusted TxPower setting
 *
 */
int32_t dwt_adjust_tx_power(uint16_t boost, uint32_t ref_tx_power, uint8_t channel, uint32_t* adj_tx_power, uint16_t* applied_boost)
{
    return ull_adjust_tx_power(boost, ref_tx_power, channel, adj_tx_power, applied_boost);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This API is used to calculate a transmit power configuration in a linear manner (step of 0.25 dB)
 *
 * input parameters
 * @param channel   The channel for which the linear tx power setting must be calculated
 * @param p_indexes Pointer to an object containing two members:
 *                   - in : The inputs indexes for which tx power configuration must be calculated.
 *                          This is an array of size 4 allowing to set individual indexes for each section of a frame.
 *
 *                          DWT_DATA_INDEX = 0
 *                          DWT_PHR_INDEX = 1
 *                          DWT_SHR_INDEX = 2
 *                          DWT_STS_INDEX = 3
 *
 *                          Index step is 0.25 dB. Power will decrease linearly by 0.25dB step with the index:
 *                          0 corresponds to maximum output power
 *                          Output power = Power(0) - 0.25dB * Index
 *
 *                          Effective maximum index value depens on DW3000 part and channel configuration. If the required index is higher than
 *                          the maximum supported value, then the API will apply the maximum index.
 *
 *                  - out: output tx power indexes corresponding to the indexes that were actually applied.
 *                         These may differ from the input indexes in the two cases below:
 *                             1. The input indexes correspond to different PLLCFG for different section of frame. This is not
 *                              supported by the IC. In such condition, all indexes will belong to the same tx configuration state. The state
 *                              to be used is the one corresponding to the highest required power (lower index)
 *
 *                              2. The input index are greater than the maximum value supported for the (channel, SOC) current
 *                              configuration. In which case, the maximum index supported is returned.
 * output parameters
 * @param p_res Pointer to an object containing the output configuration corresponding to input index.
 *              The object contain two members:
 *              - tx_frame_cfg: the power configuration to use during frame transmission
 *
 *              A configuration is a combination of two parameters:
 *              - uint32_t tx_power_setting : Tx power setting to be written to register TX_POWER_ID
 *              - uint32_t pll_cfg : PLL common configuration to be written to register PLL_COMMON_ID
 *
 * return
 * DWT_SUCCESS: if an adjusted tx power setting could be calculated. In this case, the configuration to be applied is return through
 * p_res parameter.
 * DWT_ERROR: if the API could not calculate a valid configuration.
 *
 */
int32_t dwt_calculate_linear_tx_setting(int32_t channel, power_indexes_t *p_indexes, tx_adj_res_t *p_res)
{
    return ull_calculate_linear_tx_setting(dw, channel, p_indexes, p_res);
}

int dwt_convert_tx_power_to_index(int channel, uint8_t tx_power, uint8_t *tx_power_idx)
{
	return ull_convert_tx_power_to_index(channel, tx_power, tx_power_idx);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will set the pll common config value. This allow to set the PLL setting
 * returned by the linear tx power control API, allowingto reduce LO leakage.
 *
 * input parameters
 * @param pll_common - the pll_configuration value to be written into the PLL_COMMON_ID register.
 *
 * return None.
 */
void dwt_set_pll_config(uint32_t pll_common)
{
    ull_set_pll_config(dw, pll_common);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will configure the channel number.
 *
 * input parameters
 * @param ch - Channel number (5 or 9)
 *
 * returns DWT_SUCCESS if successful, otherwise returns < 0 if failed.
 */
int32_t dwt_setchannel(dwt_pll_ch_type_e ch)
{
    return dw->dwt_driver->dwt_mcps_ops->set_channel(dw, ch);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will set the STS length. The STS length is specified in blocks. A block is 8 us duration,
 *        0 value specifies 8 us duration, the max value is 255 == 2048 us.
 *
 *        NOTE: dwt_configure() must be called prior to this to configure the PRF
 *        To set the PRF dwt_settxcode() is used.
 *
 *
 * input parameters
 * @param stsblocks  -  number of STS 8us blocks (0 == 8us, 1 == 16us, etc)
 *
 * return none
 */
void dwt_setstslength(uint8_t stsblocks)
{
    ull_setstslength(dw, stsblocks);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will configure the PHR mode and rate.
 *
 * input parameters
 * @param phrMode - PHR mode {0x0 - standard DWT_PHRMODE_STD, 0x1 - extended frames DWT_PHRMODE_EXT}
 * @param phrRate - PHR rate {0x0 - standard DWT_PHRRATE_STD, 0x1 - at datarate DWT_PHRRATE_DTA}
 *
 * returns DWT_SUCCESS if successful, otherwise returns < 0 if failed.
 */
int32_t dwt_setphr(dwt_phr_mode_e phrMode, dwt_phr_rate_e phrRate)
{
    ull_setphr(dw, phrMode, phrRate);
    return (int32_t)DWT_SUCCESS;
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will configure the data rate.
 *
 * input parameters
 * @param bitRate - Data rate see dwt_uwb_bit_rate_e, depends on PRF
 *
 * returns DWT_SUCCESS if successful, otherwise returns < 0 if failed.
 */
int32_t dwt_setdatarate(dwt_uwb_bit_rate_e bitRate)
{
    ull_setdatarate(dw, bitRate);
    return (int32_t)DWT_SUCCESS;
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will configure the Acquisition Chunk Size.
 *
 * input parameters
 * @param rxPac - Acquisition Chunk Size (Relates to RX preamble length)
 *
 * returns DWT_SUCCESS if successful, otherwise returns < 0 if failed.
 */
int32_t dwt_setrxpac(dwt_pac_size_e rxPAC)
{
    ull_setrxpac(dw, rxPAC);
    return (int32_t)DWT_SUCCESS;
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function will configure the SFD timeout value.
 *
 * input parameters
 * @param sfdTO - SFD timeout value (in symbols)
 *
 * returns DWT_SUCCESS if successful, otherwise returns < 0 if failed.
 */
int32_t dwt_setsfdtimeout(uint16_t sfdTO)
{
    ull_setsfdtimeout(dw, sfdTO);
    return (int32_t)DWT_SUCCESS;
}

/** @brief Synopsys have released an errata against the OTP power macro, in relation to low power
 *        SLEEP/RETENTION modes where the VDD and VCC are removed.
 *
 *        This function disables integrated power supply (IPS) and needs to be called prior to
 *        the SoC going to sleep or when an OTP low power mode is required.
 *
 *        On exit from low-power mode this is called to restore/enable the OTP IPS for normal OTP use (RD/WR).
 *
 * @param mode: if set to 1 this will configure OTP for low-power
 *
 * @return  none
 */
void disable_OTP_IPS(int32_t mode)
{
    ull_dis_otp_ips(dw, mode);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function runs the PLL calibration.
 *
 * input parameters:
 * @param int32_t  chan (5 = channel 5, 9 = channel 9)
 * @param uint32_t coarse_code
 * @param uint16_t sleep
 * @param uint8_t  steps
 *
 * output parameters
 *
 * return number of steps taken to lock the PLL or DWT_ERROR
 */
uint8_t dwt_pll_chx_auto_cal(int32_t chan, uint32_t coarse_code, uint16_t sleep, uint8_t steps, int8_t temperature)
{
    return ull_pll_chx_auto_cal(dw, chan, coarse_code, sleep, steps, temperature);
}

/*! ------------------------------------------------------------------------------------------------------------------
 * @brief This function sets the crystal trim based on temperature, and crystal temperature
 *        characteristics, if you pass in a temperature of TEMP_INIT (-127), the functions will also read
 *        onchip temperature sensors to determine the temperature, the crystal temperature
 *        could be different.
 *        If a crystal temperature of TEMP_INIT (-127) is passed, the function will assume 25C. 
 *        If a crystal trim of 0 is passed, the function will use the calibration value from OTP.
 *
 *        This is to compensate for crystal temperature versus frequency curve e.g.
 *
 *  Freq Hi
 *         *                               /
 *         *       __-__                  /
 *         *     /       \               /
 *         *   /           \            /
 *         *  /             \          /
 *         * /               \       /
 *         *                   -___-
 *         *
 *  Freq Lo  -40 -20   0  20  40  60  80 100 120
 *
 *
 * input parameters:
 * @param[in] dwt_xtal_trim_t params -- the based-on parameters to set the crystal trim. 
 * @param[in] uin8_t xtaltrim -- newly programmed crystal trim value
 *
 * output parameters
 *
 * return DWT_SUCCESS on succes, and DWT_ERROR on invalid parameters.
 */
int32_t dwt_xtal_temperature_compensation(
    dwt_xtal_trim_t *params,
    uint8_t *xtaltrim
    )
{
#if CONFIG_DW3000_CHIP_DW3720
    return ull_xtal_temperature_compensation(dw, params, xtaltrim);
#else
    return DWT_ERROR;
#endif
}

/** @brief This function captures the ADC samples on receiving a signal
 *
 * @param capture_adc - this is the pointer to the Structure into which to read the data.
 *
 * @return  none
 */
void dwt_capture_adc_samples(dwt_capture_adc_t *capture_adc)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_capture_adc_samples(dw, capture_adc);
#endif
}

/** @brief This function reads the captured ADC samples, needs to be called after dwt_capture_adc_samples()
 *        The test block will write to 255 (0xff) locations in the CIR memory (Ipatov).
 *        Each clock cycle produces 36 ADC bits so 8 clocks will fill a memory word.
 *        The ADC capture memory pointer increments twice each write, until the 255 limit is reached - the pointer will be at 0x1fe.
 *        If wrapped mode is used the poiner will wrap around after reaching the 255 limit.
 *        There are 36*8*255=73440 ADC bits logged (18-bit I and 18 bit Q ... but that is actually 16-bit I and 16-bit Q ... as the top two bits are 0).
 *        16-bit I and 16-bit Q are saved into 2 24 bit words: [0] = 0x00NNPP, [1] = 0x00NNPP,
 *        [0]: NN = I-, PP = I+, [1]: NN = Q-, PP = Q+,
 *        (18360 I samples and 18360 Q samples).
 *
 * @param capture_adc - this is the pointer to the dwt_capture_adc_t structure into which to read the data.
 *
 * @return  none
 */
void dwt_read_adc_samples(dwt_capture_adc_t *capture_adc)
{
#if CONFIG_DW3000_CHIP_DW3720
    ull_read_adc_samples(dw, capture_adc);
#endif
}

/** @brief This is used to enable/disable the FCS generation in transmitter and checking in receiver
 *
 * input parameters
 * @param - enable - dwt_fcs_mode_e - this is used to enable/disable FCS generation in TX and check in RX
 * output parameters
 *
 * no return value
 */
void dwt_configtxrxfcs(dwt_fcs_mode_e enable)
{
    ull_configtxrxfcs(dw, enable);
}

/*! ---------------------------------------------------------------------------------------------------
 * @brief This API will return the RSSI  - UWB channel power
 *        This API must be called only after initializing and configuring the driver
 *        and receving some Rx data packets.
 *
 * input parameters
 * @param diag diagnostics for a particular accumulator
 * @param acc_idx - Accumulator (see dwt_acc_idx_e)
 *
 * output parameters
 * @param signal_strength strength in q8.8 format (int16_t).
 *
 * return: returns DWT_SUCCESS on success and DWT_ERROR on invalid parameters.
 */
int dwt_calculate_rssi(const dwt_cirdiags_t *diag, dwt_acc_idx_e acc_idx, int16_t *signal_strength)
{
    return ull_calculate_rssi(dw, diag, acc_idx, signal_strength);
}

/*! ---------------------------------------------------------------------------------------------------
 * @brief This API will return the First path signal power
 *        This API must be called only after initializing and configuring the driver
 *        and receving some Rx data packets.
 *
 * input parameters
 * @param CIR diagnostics for a particular accumulator
 * @param acc_idx - Accumulator (see dwt_acc_idx_e)
 *
 * output parameters
 * @param Signal strength in q8.8 format (int16_t).
 *
 * return: returns DWT_SUCCESS on success and DWT_ERROR on input parameters.
 */
int dwt_calculate_first_path_power(const dwt_cirdiags_t *diag, dwt_acc_idx_e acc_idx, int16_t *signal_strength)
{
    return ull_calculate_first_path_power(dw, diag, acc_idx, signal_strength);
}

    /*! ---------------------------------------------------------------------------------------------------
    * @brief This function reads the CIA diagnostics for an individual accumulator.
    *
    * input parameters
    * @param  acc_idx   Accumulator index
    *
    * output parameters
    * @param cirdiags  CIA diagnostics structure
    *
    * return DWT_SUCCESS or DWT_ERROR if the passed parameters were wrong.
    */
int dwt_readdiagnostics_acc(dwt_cirdiags_t *cir_diag, dwt_acc_idx_e acc_idx)
{
    return ull_readdiagnostics_acc(dw, cir_diag, acc_idx);
}

/*!
 * This function is used to write to the DW3xxx device registers
 *
 * input parameters:
 * @param regFileID     - ID of register file or buffer being accessed
 * @param index         - byte index into register file or buffer being accessed
 * @param length        - number of bytes being written
 * @param buffer        - pointer to buffer containing the 'length' bytes to be written
 *
 * output parameters
 *
 * no return value
 */
void dwt_writetodevice(uint32_t regFileID, uint16_t index, uint16_t length, uint8_t *buffer)
{
    dw->dwt_driver->dwt_mcps_ops->write_to_device(dw, regFileID, index, length, buffer);
}

/*!
 * This function is used to read from the DW3xxx device registers
 *
 * input parameters:
 * @param regFileID     - ID of register file or buffer being accessed
 * @param index         - byte index into register file or buffer being accessed
 * @param length        - number of bytes being read
 * @param buffer        - pointer to buffer in which to return the read data.
 *
 * output parameters
 *
 * no return value
 */
void dwt_readfromdevice(uint32_t regFileID, uint16_t index, uint16_t length, uint8_t *buffer)
{
    dw->dwt_driver->dwt_mcps_ops->read_from_device(dw, regFileID, index, length, buffer);
}

/*! ------------------------------------------------------------------------------------------------------------------
* @brief This function will configure the PDOA mode.
*
* input parameters
* @param pdoaMode - PDOA mode
*
* NOTE: to modify preamble length or STS length call dwt_configure first.
*
* returns DWT_SUCCESS if successful, otherwise returns < 0 if failed.
*/
int dwt_setpdoamode(dwt_pdoa_mode_e pdoaMode)
{
    return ull_setpdoamode(dw, pdoaMode);
}

/*! ------------------------------------------------------------------------------------------------------------------
* @brief This function sets the ISR configuration flags.
*
* input parameters
* @param flags  - ISR configuration flags (see dwt_isr_flags_e)
*
* output parameters
*
* no return value
*/
void dwt_configureisr(dwt_isr_flags_e flags)
{
    dw->isrFlags = flags;
}
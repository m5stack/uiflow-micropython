/**
 * @file max30100.h
 *
 * @author
 * Angelo Elias Dalzotto (150633@upf.br)
 * GEPID - Grupo de Pesquisa em Cultura Digital (http://gepid.upf.br/)
 * Universidade de Passo Fundo (http://www.upf.br/)
 *
 * @copyright
 * Copyright (c) 2017 Raivis Strogonovs (https://morf.lv)
 *
 * @brief This library was created to interface the MAX30100 pulse and oxymeter
 * sensor with ESP32 using the IDF-SDK. It includes functions to initialize with
 * the programmer's desired parameters and to update the readings, detecting pulse
 * and having the pulse saturation O2. It is based on Strogonovs Arduino library.
*/
#ifndef MAX30100_H
#define MAX30100_H

#include <math.h>
#include <stdint.h>
#include <stdbool.h>
#include "esp_err.h"

/**
 * Default parameters for initialization.
 */
#define MAX30100_DEFAULT_OPERATING_MODE         MAX30100_MODE_SPO2_HR
#define MAX30100_DEFAULT_IR_LED_CURRENT         MAX30100_LED_CURRENT_50MA
#define MAX30100_DEFAULT_START_RED_LED_CURRENT  MAX30100_LED_CURRENT_27_1MA
#define MAX30100_DEFAULT_SAMPLING_RATE          MAX30100_SAMPLING_RATE_100HZ
#define MAX30100_DEFAULT_LED_PULSE_WIDTH        MAX30100_PULSE_WIDTH_1600US_ADC_16
#define MAX30100_DEFAULT_ACCEPTABLE_INTENSITY_DIFF      65000
#define MAX30100_DEFAULT_RED_LED_CURRENT_ADJUSTMENT_MS    500
#define MAX30100_DEFAULT_RESET_SPO2_EVERY_N_PULSES          4
#define MAX30100_DEFAULT_ALPHA                              0.95
#define MAX30100_DEFAULT_MEAN_FILTER_SIZE                  15
#define MAX30100_DEFAULT_PULSE_MIN_THRESHOLD              100
#define MAX30100_DEFAULT_PULSE_MAX_THRESHOLD             2000
#define MAX30100_DEFAULT_PULSE_BPM_SAMPLE_SIZE             10

/**
 * Operation Mode Enum.
 * Heart rate only or Oxigen saturation + Heart rate.
 */
typedef enum _max30100_mode_t {
    MAX30100_MODE_HR_ONLY                 = 0x02,
    MAX30100_MODE_SPO2_HR                 = 0x03
} max30100_mode_t;

/**
 * Sampling rate enum.
 * Internal sampling rates from 50Hz up to 1KHz.
 */
typedef enum SamplingRate {
    MAX30100_SAMPLING_RATE_50HZ           = 0x00,
    MAX30100_SAMPLING_RATE_100HZ          = 0x01,
    MAX30100_SAMPLING_RATE_167HZ          = 0x02,
    MAX30100_SAMPLING_RATE_200HZ          = 0x03,
    MAX30100_SAMPLING_RATE_400HZ          = 0x04,
    MAX30100_SAMPLING_RATE_600HZ          = 0x05,
    MAX30100_SAMPLING_RATE_800HZ          = 0x06,
    MAX30100_SAMPLING_RATE_1000HZ         = 0x07
} max30100_sampling_rate_t;

/**
 * Led pulse width enum.
 * Sets from 200us to 1600us.
 */
typedef enum LEDPulseWidth {
    MAX30100_PULSE_WIDTH_200US_ADC_13     = 0x00,
    MAX30100_PULSE_WIDTH_400US_ADC_14     = 0x01,
    MAX30100_PULSE_WIDTH_800US_ADC_15     = 0x02,
    MAX30100_PULSE_WIDTH_1600US_ADC_16    = 0x03,
} max30100_pulse_width_t;

/**
 * Led current enum.
 * Sets the current for any of the leds. From 0mA to 50mA.
 */
typedef enum LEDCurrent {
    MAX30100_LED_CURRENT_0MA              = 0x00,
    MAX30100_LED_CURRENT_4_4MA            = 0x01,
    MAX30100_LED_CURRENT_7_6MA            = 0x02,
    MAX30100_LED_CURRENT_11MA             = 0x03,
    MAX30100_LED_CURRENT_14_2MA           = 0x04,
    MAX30100_LED_CURRENT_17_4MA           = 0x05,
    MAX30100_LED_CURRENT_20_8MA           = 0x06,
    MAX30100_LED_CURRENT_24MA             = 0x07,
    MAX30100_LED_CURRENT_27_1MA           = 0x08,
    MAX30100_LED_CURRENT_30_6MA           = 0x09,
    MAX30100_LED_CURRENT_33_8MA           = 0x0A,
    MAX30100_LED_CURRENT_37MA             = 0x0B,
    MAX30100_LED_CURRENT_40_2MA           = 0x0C,
    MAX30100_LED_CURRENT_43_6MA           = 0x0D,
    MAX30100_LED_CURRENT_46_8MA           = 0x0E,
    MAX30100_LED_CURRENT_50MA             = 0x0F
} max30100_current_t;

/**
 * FIFO configuration structure.
 * Do NOT declare.
 */
typedef struct _max30100_fifo_t {
    uint16_t raw_ir;
    uint16_t raw_red;
} max30100_fifo_t;

/**
 * DC filter structure.
 * Do NOT declare.
 */
typedef struct _max30100_dc_filter_t {
    float w;
    float result;
} max30100_dc_filter_t;

/**
 * Butterworth filter structure.
 * Do NOT declare.
 */
typedef struct _max30100_butterworth_filter_t
{
    float v[2];
    float result;
} max30100_butterworth_filter_t;

/**
 * Mean diff filter structure.
 * Do NOT declare.
 */
typedef struct _max30100_mean_diff_filter_t
{
    float *values;
    uint8_t index;
    float sum;
    uint8_t count;
} max30100_mean_diff_filter_t;

/**
 * @brief Function pointer type for low-level I2C register read.
 *
 * This callback should read a single byte from the MAX30100
 * register given by 'reg', writing the result byte to *out_data. The
 * 'intf_ptr' is the opaque interface/context pointer supplied in the
 * configuration structure (e.g. pointer to an I2C bus object, mutex, or
 * driver abstraction).
 *
 * Return value semantics:
 *   0  -> success
 *  <0  -> failure (implementation-defined error code)
 */
typedef int8_t (*max30100_i2c_read_fn)(uint8_t addr, uint8_t reg, uint8_t *out_data, uint32_t len, void *intf_ptr);

/**
 * @brief Function pointer type for low-level I2C register write.
 *
 * This callback should write a single byte 'in_data' to the MAX30100
 * register given by 'reg'. The 'intf_ptr' is the opaque interface/context
 * pointer supplied in the configuration structure (e.g. pointer to an I2C
 * bus object, mutex, or driver abstraction).
 *
 * Return value semantics:
 *   0  -> success
 *  <0  -> failure (implementation-defined error code)
 */
typedef int8_t (*max30100_i2c_write_fn)(uint8_t addr, uint8_t reg, const uint8_t *in_data, uint32_t len, void *intf_ptr);

/**
 * Data structure.
 * You need this to keep track of the values.
 */
typedef struct _max30100_data_t {
    bool pulse_detected;
    float heart_bpm;

    float ir_cardiogram;

    float ir_dc_value;
    float red_dc_value;

    uint16_t ir_raw;
    uint16_t red_raw;

    float spO2;

    uint32_t last_beat_threshold;

    float dc_filtered_red;
    float dc_filtered_ir;
} max30100_data_t;

/**
 * The sensor "object" structure.
 * Use it to maintain all the configuration information.
 * Don't change it directly, use the functions to do so.
 */
typedef struct _max30100_config_t {

    uint8_t i2c_addr;

    bool debug;
    // interface pointer for I2C read/write functions
    void *intf_ptr;
    // function pointer for reading a register via the configured I2C interface
    max30100_i2c_read_fn i2c_bus_read;
    max30100_i2c_write_fn i2c_bus_write;

    uint8_t red_current;
    uint32_t last_red_current_check;

    uint8_t current_pulse_detector_state;
    float current_bpm;
    float *values_bpm;
    float values_bpm_sum;
    uint8_t values_bpm_count;
    uint8_t bpm_index;
    uint32_t last_beat_threshold;

    uint32_t acceptable_intense_diff;
    uint32_t red_current_adj_ms;
    uint8_t reset_spo2_pulse_n;
    float dc_alpha;
    uint16_t pulse_min_threshold;
    uint16_t pulse_max_threshold;

    uint8_t mean_filter_size;
    uint8_t pulse_bpm_sample_size;

    max30100_fifo_t prev_fifo;

    max30100_dc_filter_t dc_filter_ir;
    max30100_dc_filter_t dc_filter_red;
    max30100_butterworth_filter_t lpb_filter_ir;
    max30100_mean_diff_filter_t mean_diff_ir;

    float ir_ac_sq_sum;
    float red_ac_sq_sum;
    uint16_t samples_recorded;
    uint16_t pulses_detected;
    float current_spO2;

    max30100_current_t ir_current;

} max30100_config_t;

/**
 * @brief Initialize the sensor with the desired I2C and given parameters.
 * You can also set the debug mode.
 *
 * @details This functions include some parameters inside that initialize
 * with default values. You can change them later with max30100_set_* functions.
 *
 * @param this is the address of the configuration structure.
 * @param i2c_num is the I2C port of the ESP32 with the MAX30100 is attached to.
 * @param mode is the working mode of the sensor (HR only or HR+SPO2)
 * @param sampling_rate is the frequency which samples are taken internally.
 * @param pulse_width is the led pulse width.
 * @param ir_current is the current to the IR Led.
 * @param start_red_current is the starting value to Red Led current.
 * @param mean_filter_size is the sampling vector size to the filter.
 * @param pulse_bpm_sample_size is the heart rate sampling vector size.
 * @param high_res_mode is to set if high resolution mode or not.
 * @param debug is to set if registers output will be done to serial monitoring.
 *
 * @returns status of execution.
 */
esp_err_t max30100_init(max30100_config_t *this, uint8_t i2c_addr,
    max30100_mode_t mode, max30100_sampling_rate_t sampling_rate,
    max30100_pulse_width_t pulse_width, max30100_current_t ir_current,
    max30100_current_t start_red_current, uint8_t mean_filter_size,
    uint8_t pulse_bpm_sample_size, bool high_res_mode, bool debug);

/**
 * @brief Reads from MAX30100 internal registers and updates internal structures.
 * The results are written to a data structure.
 *
 * @details This functions must be called on a optimal rate of 100Hz.
 *
 * @param this is the address of the configuration structure.
 * @param data is the address of the data structure to save the results.
 *
 * @returns status of execution.
 */
esp_err_t max30100_update(max30100_config_t *this, max30100_data_t *data);

/**
 * @brief Reads the internal temperature of the MAX30100.
 *
 * @param this is the address of the configuration structure.
 * @param temperature is the address of the variable to save the temperature.
 *
 * @returns status of execution.
 */
esp_err_t max30100_read_temperature(max30100_config_t *this, float *temperature);

/**
 * @brief Prints the registers for debugging purposes.
 *
 * @param this is the address of the configuration structure.
 *
 * @returns status of execution.
 */
esp_err_t max30100_print_registers(max30100_config_t *this);

/**
 * @brief Sets the operation mode. HR Only or HR+SPO2.
 *
 * @details This is automatically called by the initializer function.
 *
 * @param this is the address of the configuration structure.
 * @param mode is the mode of operation desired.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_mode(max30100_config_t *this, max30100_mode_t mode);

/**
 * @brief Sets the resolution. High or standard.
 *
 * @details This is automatically called by the initializer function.
 *
 * @param this is the address of the configuration structure.
 * @param enable is if high resolution will be enabled.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_high_res(max30100_config_t *this, bool enabled);

/**
 * @brief Sets the led currents.
 *
 * @details This is automatically called by the initializer function
 * or automatically when needed by the library.
 *
 * @param this is the address of the configuration structure.
 * @param red_current is the current value of the Red Led.
 * @param ir_current is the current value of the IR Led.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_led_current(max30100_config_t *this,
    max30100_current_t red_current,
    max30100_current_t ir_current);

/**
 * @brief Sets the pulse width.
 *
 * @details This is automatically called by the initializer function.
 *
 * @param this is the address of the configuration structure.
 * @param pw is the pulse width desired.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_pulse_width(max30100_config_t *this, max30100_pulse_width_t pw);

/**
 * @brief Set the internal sampling rate.
 *
 * @details This is automatically called by the initializer function.
 *
 * @param this is the address of the configuration structure.
 * @param rate is the sampling rate desired.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_sampling_rate(max30100_config_t *this,
    max30100_sampling_rate_t rate);

/**
 * @brief Sets the acceptable intense diff.
 *
 * @details This is set to a default (recommended) value in the initializer.
 * The only way to change is by calling this function.
 *
 * @param this is the address of the configuration structure.
 * @param acceptable_intense_diff is the value of the diff accepted.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_acceptable_intense_diff(max30100_config_t *this,
    uint32_t acceptable_intense_diff);

/**
 * @brief Sets the rate which the red led current can be adjusted.
 *
 * @details This is set to a default (recommended) value in the initializer.
 * The only way to change is by calling this function.
 *
 * @param this is the address of the configuration structure.
 * @param red_current_adj_ms is the value in milliseconds to be set.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_red_current_adj_ms(max30100_config_t *this,
    uint32_t red_current_adj_ms);

/**
 * @brief Sets the number of pulses which the spo2 values are reset.
 *
 * @details This is set to a default (recommended) value in the initializer.
 * The only way to change is by calling this function.
 *
 * @param this is the address of the configuration structure.
 * @param reset_spo2_pulse_n is the number of pulses.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_reset_spo2_pulse_n(max30100_config_t *this,
    uint8_t reset_spo2_pulse_n);

/**
 * @brief Setts the DC filter alpha value.
 *
 * @details This is set to a default (recommended) value in the initializer.
 * The only way to change is by calling this function.
 *
 * @param this is the address of the configuration structure.
 * @param dc_alpha is the alpha value of the filter.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_dc_alpha(max30100_config_t *this, float dc_alpha);

/**
 * @brief Sets the minimum threshold to bpm.
 *
 * @details This is set to a default value in the initializer.
 * The only way to change is by calling this function.
 * You can't just throw these two values at random.
 * Check Check table 8 in datasheet on page 19.
 * You can set 300 for finger or 20 for wrist (with a lot of noise).
 *
 * @param this is the address of the configuration structure.
 * @param pulse_min_threshold is the value.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_pulse_min_threshold(max30100_config_t *this,
    uint16_t pulse_min_threshold);

/**
 * @brief Sets the maximum threshold to bpm.
 *
 * @details This is set to a default value in the initializer.
 * The only way to change is by calling this function.
 * You can't just throw these two values at random.
 * Check Check table 8 in datasheet on page 19.
 *
 * @param this is the address of the configuration structure.
 * @param pulse_max_threshold is the value.
 *
 * @returns status of execution.
 */
esp_err_t max30100_set_pulse_max_threshold(max30100_config_t *this,
    uint16_t pulse_max_threshold);

#endif

/**
 * MIT License
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:

 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.

 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
*/

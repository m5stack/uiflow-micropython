#ifndef MAX30102_H
#define MAX30102_H

#include <math.h>
#include "driver/i2c.h"
#include "freertos/task.h"
#include "esp_err.h"

/**
 * Default parameters for initialization.
 */
#define MAX30102_DEFAULT_OPERATING_MODE         MAX30102_MODE_SPO2_HR
#define MAX30102_DEFAULT_IR_LED_CURRENT         MAX30102_LED_CURRENT_6_2MA
#define MAX30102_DEFAULT_START_RED_LED_CURRENT  MAX30102_LED_CURRENT_6_2MA
#define MAX30102_DEFAULT_SAMPLING_RATE          MAX30102_SAMPLING_RATE_400HZ
#define MAX30102_DEFAULT_LED_PULSE_WIDTH        MAX30102_PULSE_WIDTH_411US_ADC_18
#define MAX30102_DEFAULT_ACCEPTABLE_INTENSITY_DIFF      65000
#define MAX30102_DEFAULT_RED_LED_CURRENT_ADJUSTMENT_MS    500
#define MAX30102_DEFAULT_RESET_SPO2_EVERY_N_PULSES          4
#define MAX30102_DEFAULT_ALPHA                              0.95
#define MAX30102_DEFAULT_MEAN_FILTER_SIZE                  15
#define MAX30102_DEFAULT_PULSE_MIN_THRESHOLD               10
#define MAX30102_DEFAULT_PULSE_MAX_THRESHOLD             2000
#define MAX30102_DEFAULT_PULSE_BPM_SAMPLE_SIZE             10

/**
 * Operation Mode Enum.
 * Heart rate only or Oxigen saturation + Heart rate.
 */
typedef enum _max30102_mode_t {
    MAX30102_MODE_HR_ONLY                 = 0x02,
    MAX30102_MODE_SPO2_HR                 = 0x03
} max30102_mode_t;

/**
 * Sampling rate enum.
 * Internal sampling rates from 50Hz up to 3.2KHz.
 */
typedef enum SamplingRate {
    MAX30102_SAMPLING_RATE_50HZ           = 0x00,
    MAX30102_SAMPLING_RATE_100HZ          = 0x01,
    MAX30102_SAMPLING_RATE_200HZ          = 0x02,
    MAX30102_SAMPLING_RATE_400HZ          = 0x03,
    MAX30102_SAMPLING_RATE_800HZ          = 0x04,
    MAX30102_SAMPLING_RATE_1000HZ         = 0x05,
    MAX30102_SAMPLING_RATE_1600HZ         = 0x06,
    MAX30102_SAMPLING_RATE_3200HZ         = 0x07
} max30102_sampling_rate_t;

/**
 * Led pulse width enum.
 * Sets from 69us to 411us.
 */
typedef enum LEDPulseWidth {
    MAX30102_PULSE_WIDTH_69US_ADC_15     = 0x00,
    MAX30102_PULSE_WIDTH_118US_ADC_16    = 0x01,
    MAX30102_PULSE_WIDTH_215US_ADC_17    = 0x02,
    MAX30102_PULSE_WIDTH_411US_ADC_18    = 0x03,
} max30102_pulse_width_t;

/**
 * Led current enum.
 * Sets the current for any of the leds. From 0mA to 50mA.
 */
typedef enum LEDCurrent {
    MAX30102_LED_CURRENT_0MA              = 0x00,
    MAX30102_LED_CURRENT_0_2MA            = 0x01,
    MAX30102_LED_CURRENT_3MA              = 0x0F,
    MAX30102_LED_CURRENT_6_2MA            = 0x1F,
    MAX30102_LED_CURRENT_9_4MA            = 0x2F,
    MAX30102_LED_CURRENT_12_6MA           = 0x3F,
    MAX30102_LED_CURRENT_15_8MA           = 0x4F,
    MAX30102_LED_CURRENT_19MA             = 0x5F,
    MAX30102_LED_CURRENT_22_2MA           = 0x6F,
    MAX30102_LED_CURRENT_25_4MA           = 0x7F,
    MAX30102_LED_CURRENT_28_6MA           = 0x8F,
    MAX30102_LED_CURRENT_31_8MA           = 0x9F,
    MAX30102_LED_CURRENT_35MA             = 0xAF,
    MAX30102_LED_CURRENT_38_2MA           = 0xBF,
    MAX30102_LED_CURRENT_41_4MA           = 0xCF,
    MAX30102_LED_CURRENT_44_6MA           = 0xDF,
    MAX30102_LED_CURRENT_47_8MA           = 0xEF,
    MAX30102_LED_CURRENT_51MA             = 0xFF
} max30102_current_t;

/**
 * ADC range: 2048, 4096, 8192, 16384.
 * Sets: 7.81pA. 15.63pA, 31.25pA, 62.5pA per LSB..
 */
typedef enum ADCRange {
    MAX30102_ADC_RANGE_2048     = 0x00,
    MAX30102_ADC_RANGE_4096     = 0x20,
    MAX30102_ADC_RANGE_8192     = 0x40,
    MAX30102_ADC_RANGE_16384    = 0x60,
} max30102_adc_range_t;

/**
 * FIFO sample avg: set the number of samples to be averaged by the chip.
 * Options: MAX30105_SAMPLE_AVG_1, 2, 4, 8, 16, 32
 */
typedef enum SampleAvg {
    MAX30102_SAMPLE_AVG_1       = 0x00,
    MAX30102_SAMPLE_AVG_2       = 0x20,
    MAX30102_SAMPLE_AVG_4       = 0x40,
    MAX30102_SAMPLE_AVG_8       = 0x60,
    MAX30102_SAMPLE_AVG_16      = 0x80,
    MAX30102_SAMPLE_AVG_32      = 0xA0,
} max30102_sample_avg_t;

/**
 * Mode configuration commands.
 */
typedef enum ModeConfig {
    MAX30102_WAKEUP             = 0x00,
    MAX30102_RESET              = 0x40,
    MAX30102_SHUTDOWN           = 0x80,
} max30102_mode_config_t;

/**
 * Multi-LED Mode enable slot.
 */
typedef enum MultiLedMode {
    MAX30102_SLOT_NONE             = 0x00,
    MAX30102_SLOT_RED_LED          = 0x01,
    MAX30102_SLOT_IR_LED           = 0x02,
} max30102_multi_led_mode_t;

/**
 * FIFO configuration structure.
 * Do NOT declare.
 */
typedef struct _max30102_fifo_t {
    uint32_t raw_red;
    uint32_t raw_ir;
} max30102_fifo_t;

/**
 * DC filter structure.
 * Do NOT declare.
 */
typedef struct _max30102_dc_filter_t {
    float w;
    float result;
} max30102_dc_filter_t;

/**
 * Butterworth filter structure.
 * Do NOT declare.
 */
typedef struct _max30102_butterworth_filter_t
{
    float v[2];
    float result;
} max30102_butterworth_filter_t;

/**
 * Mean diff filter structure.
 * Do NOT declare.
 */
typedef struct _max30102_mean_diff_filter_t
{
    float *values;
    uint8_t index;
    float sum;
    uint8_t count;
} max30102_mean_diff_filter_t;

/**
 * Data structure.
 * You need this to keep track of the values.
 */
typedef struct _max30102_data_t {
    bool pulse_detected;
    float heart_bpm;

    float ir_cardiogram;

    float ir_dc_value;
    float red_dc_value;

    uint32_t ir_raw;
    uint32_t red_raw;

    float spO2;

    uint32_t last_beat_threshold;

    float dc_filtered_red;
    float dc_filtered_ir;
} max30102_data_t;

/**
 * The sensor "object" structure.
 * Use it to maintain all the configuration information.
 * Don't change it directly, use the functions to do so.
 */
typedef struct _max30102_config_t {

    i2c_port_t i2c_num;
    uint8_t i2c_addr;
    uint8_t device_pos;

    bool debug;

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

    max30102_fifo_t prev_fifo;

    max30102_dc_filter_t dc_filter_ir;
    max30102_dc_filter_t dc_filter_red;
    max30102_butterworth_filter_t lpb_filter_ir;
    max30102_mean_diff_filter_t mean_diff_ir;

    float ir_ac_sq_sum;
    float red_ac_sq_sum;
    uint16_t samples_recorded;
    uint16_t pulses_detected;
    float current_spO2;

    max30102_current_t ir_current;

} max30102_config_t;

/**
 * @brief Initialize the sensor with the desired I2C and given parameters.
 * You can also set the debug mode.
 *
 * @details This functions include some parameters inside that initialize
 * with default values. You can change them later with max30102_set_* functions.
 *
 * @param this is the address of the configuration structure.
 * @param i2c_num is the I2C port of the ESP32 with the MAX30102 is attached to.
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
esp_err_t max30102_init(max30102_config_t *this, i2c_port_t i2c_num,
    max30102_mode_t mode, max30102_sampling_rate_t sampling_rate,
    max30102_pulse_width_t pulse_width, max30102_current_t ir_current,
    max30102_current_t start_red_current, max30102_adc_range_t adc_range,
    uint8_t mean_filter_size, uint8_t pulse_bpm_sample_size, bool debug);

/**
 * @brief When the RESET bit is set to one, all configuration, threshold.
 * a power-on reset. The RESET bit is cleared automatically back to zero
 *
 * @param this is the address of the configuration structure.
 *
 * @returns status of execution.
 */
esp_err_t max30102_soft_reset(max30102_config_t *this);

/**
 * @brief Reads from MAX30102 internal registers and updates internal structures.
 * The results are written to a data structure.
 *
 * @details This functions must be called on a optimal rate of 100Hz.
 *
 * @param this is the address of the configuration structure.
 * @param data is the address of the data structure to save the results.
 *
 * @returns status of execution.
 */
esp_err_t max30102_update(max30102_config_t *this, max30102_data_t *data);

/**
 * @brief Reads the internal temperature of the MAX30102.
 *
 * @param this is the address of the configuration structure.
 * @param temperature is the address of the variable to save the temperature.
 *
 * @returns status of execution.
 */
esp_err_t max30102_read_temperature(max30102_config_t *this, float *temperature);

/**
 * @brief Prints the registers for debugging purposes.
 *
 * @param this is the address of the configuration structure.
 *
 * @returns status of execution.
 */
esp_err_t max30102_print_registers(max30102_config_t *this);

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
esp_err_t max30102_set_mode(max30102_config_t *this, max30102_mode_t mode);

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
esp_err_t max30102_set_adc_range(max30102_config_t *this, max30102_adc_range_t range);

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
esp_err_t max30102_set_led_current(max30102_config_t *this,
    max30102_current_t red_current,
    max30102_current_t ir_current);

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
esp_err_t max30102_set_pulse_width(max30102_config_t *this, max30102_pulse_width_t pw);

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
esp_err_t max30102_set_sampling_rate(max30102_config_t *this,
    max30102_sampling_rate_t rate);

/**
 * @brief Given a slot number assign a thing to it.
 *
 * @details Devices are SLOT_RED_LED or SLOT_RED_PILOT (proximity)
 *          Assigning a SLOT_RED_LED will pulse LED
 *
 * @param this is the address of the configuration structure.
 * @param slotnumber.
 * @param device.
 *
 * @returns status of execution.
 */
esp_err_t max30102_enable_slot(max30102_config_t *this,  uint8_t slotNumber, max30102_multi_led_mode_t device);

/**
 * @brief FIFO averaged samples number Configuration.
 *
 * @details FIFO sample avg: set the number of samples to be averaged by the chip.
 * Options: MAX30105_SAMPLE_AVG_1, 2, 4, 8, 16, 32
 *
 * @param this is the address of the configuration structure.
 * @param num_samples is the value of the FIFO data queue configuration.
 *
 * @returns status of execution.
 */
esp_err_t max30102_set_fifo_average(max30102_config_t *this,
    max30102_sample_avg_t avg);

/**
 * @brief Sets the fifo_rollover. enable or disable.
 *
 * @details enable to allow FIFO tro wrap/roll over function.
 *
 * @param this is the address of the configuration structure.
 * @param enable.
 *
 * @returns status of execution.
 */
esp_err_t max30102_enable_fifo_rollover(max30102_config_t *this, bool enabled);

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
esp_err_t max30102_set_acceptable_intense_diff(max30102_config_t *this,
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
esp_err_t max30102_set_red_current_adj_ms(max30102_config_t *this,
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
esp_err_t max30102_set_reset_spo2_pulse_n(max30102_config_t *this,
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
esp_err_t max30102_set_dc_alpha(max30102_config_t *this, float dc_alpha);

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
esp_err_t max30102_set_pulse_min_threshold(max30102_config_t *this,
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
esp_err_t max30102_set_pulse_max_threshold(max30102_config_t *this,
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

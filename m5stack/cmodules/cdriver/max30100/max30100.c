/**
 * @file max30100.c
 *
 * @author
 * Angelo Elias Dalzotto (150633@upf.br)
 * GEPID - Grupo de Pesquisa em Cultura Digital (http://gepid.upf.br/)
 * Universidade de Passo Fundo (http://www.upf.br/)
 *
 * @copyright
 * Copyright (c) 2017 Raivis Strogonovs (https://morf.lv)
 *
 * @brief This is the source code for all the functions included in the
 * MAX30100 ESP32 Library.
*/

#include <stdio.h>
#include "./include/max30100/max30100.h"
#include "./include/max30100/registers.h"
#include <string.h>

#include "py/runtime.h"
static void apply_bus(uint8_t pos) {

}
static void free_bus(uint8_t pos) {

}

esp_err_t max30100_init(max30100_config_t *this,
    i2c_port_t i2c_num,
    max30100_mode_t mode,
    max30100_sampling_rate_t sampling_rate,
    max30100_pulse_width_t pulse_width,
    max30100_current_t ir_current,
    max30100_current_t start_red_current,
    uint8_t mean_filter_size,
    uint8_t pulse_bpm_sample_size,
    bool high_res_mode,
    bool debug) {
    this->i2c_num = i2c_num;

    this->acceptable_intense_diff = MAX30100_DEFAULT_ACCEPTABLE_INTENSITY_DIFF;
    this->red_current_adj_ms = MAX30100_DEFAULT_RED_LED_CURRENT_ADJUSTMENT_MS;
    this->reset_spo2_pulse_n = MAX30100_DEFAULT_RESET_SPO2_EVERY_N_PULSES;
    this->dc_alpha = MAX30100_DEFAULT_ALPHA;
    this->pulse_min_threshold = MAX30100_DEFAULT_PULSE_MIN_THRESHOLD;
    this->pulse_max_threshold = MAX30100_DEFAULT_PULSE_MAX_THRESHOLD;

    this->mean_filter_size = mean_filter_size;
    this->pulse_bpm_sample_size = pulse_bpm_sample_size;

    this->debug = debug;
    this->current_pulse_detector_state = MAX30100_PULSE_IDLE;

    this->mean_diff_ir.values = NULL;
    this->values_bpm = NULL;
    this->mean_diff_ir.values = malloc(sizeof(float) * mean_filter_size);
    this->values_bpm = malloc(sizeof(float) * pulse_bpm_sample_size);

    if (!(this->values_bpm) || !(this->mean_diff_ir.values)) {
        return ESP_ERR_INVALID_RESPONSE;
    }

    esp_err_t ret = max30100_set_mode(this, mode);
    if (ret != ESP_OK) {
        return ret;
    }

    ret = max30100_set_sampling_rate(this, sampling_rate);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_set_pulse_width(this, pulse_width);
    if (ret != ESP_OK) {
        return ret;
    }

    this->red_current = (uint8_t)start_red_current;
    this->last_red_current_check = 0;

    this->ir_current = ir_current;
    ret = max30100_set_led_current(this, this->red_current, ir_current);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_set_high_res(this, high_res_mode);
    if (ret != ESP_OK) {
        return ret;
    }

    this->dc_filter_ir.w = 0;
    this->dc_filter_ir.result = 0;

    this->dc_filter_red.w = 0;
    this->dc_filter_red.result = 0;


    this->lpb_filter_ir.v[0] = 0;
    this->lpb_filter_ir.v[1] = 0;
    this->lpb_filter_ir.result = 0;

    memset(this->mean_diff_ir.values, 0, sizeof(float) * mean_filter_size);
    this->mean_diff_ir.index = 0;
    this->mean_diff_ir.sum = 0;
    this->mean_diff_ir.count = 0;


    memset(this->values_bpm, 0, sizeof(float) * pulse_bpm_sample_size);
    this->values_bpm_sum = 0;
    this->values_bpm_count = 0;
    this->bpm_index = 0;


    this->ir_ac_sq_sum = 0;
    this->red_ac_sq_sum = 0;
    this->samples_recorded = 0;
    this->pulses_detected = 0;
    this->current_spO2 = 0;

    this->last_beat_threshold = 0;
    return ESP_OK;
}

esp_err_t max30100_update(max30100_config_t *this, max30100_data_t *data) {
    data->pulse_detected = false;
    data->heart_bpm = 0.0;
    data->ir_cardiogram = 0.0;
    data->ir_dc_value = 0.0;
    data->red_dc_value = 0.0;
    data->spO2 = this->current_spO2;
    data->last_beat_threshold = 0;
    data->dc_filtered_ir = 0.0;
    data->dc_filtered_red = 0.0;

    max30100_fifo_t raw_data;
    esp_err_t ret = max30100_read_fifo(this, &raw_data);
    if (ret != ESP_OK) {
        return ret;
    }
    data->ir_raw = raw_data.raw_ir;
    data->red_raw = raw_data.raw_red;
    this->dc_filter_ir = max30100_dc_removal((float)raw_data.raw_ir,
        this->dc_filter_ir.w,
        this->dc_alpha);
    this->dc_filter_red = max30100_dc_removal((float)raw_data.raw_red,
        this->dc_filter_red.w,
        this->dc_alpha);

    float mean_diff_res_ir = max30100_mean_diff(this,
        this->dc_filter_ir.result);

    max30100_lpb_filter(this, mean_diff_res_ir /*-dcFilterIR.result*/);

    this->ir_ac_sq_sum += this->dc_filter_ir.result * this->dc_filter_ir.result;
    this->red_ac_sq_sum += this->dc_filter_red.result * this->dc_filter_red.result;
    this->samples_recorded++;

    if (max30100_detect_pulse(this, this->lpb_filter_ir.result) && this->samples_recorded) {
        data->pulse_detected = true;
        this->pulses_detected++;

        float ratio_rms = log(sqrt(this->red_ac_sq_sum /
            (float)this->samples_recorded)) /
            log(sqrt(this->ir_ac_sq_sum /
            (float)this->samples_recorded));

        if (this->debug) {
            printf("RMS Ratio: %f\n", ratio_rms);
        }

        // This is my adjusted standard model, so it shows 0.89 as 94% saturation.
        // It is probably far from correct, requires proper empircal calibration.
        this->current_spO2 = 110.0 - 18.0 * ratio_rms;
        data->spO2 = this->current_spO2;

        if (!(this->pulses_detected % this->reset_spo2_pulse_n)) {
            this->ir_ac_sq_sum = 0;
            this->red_ac_sq_sum = 0;
            this->samples_recorded = 0;
        }
    }

    ret = max30100_balance_intensities(this,
        this->dc_filter_red.w,
        this->dc_filter_ir.w);
    if (ret != ESP_OK) {
        return ret;
    }


    data->heart_bpm = this->current_bpm;
    data->ir_cardiogram = this->lpb_filter_ir.result;
    data->ir_dc_value = this->dc_filter_ir.w;
    data->red_dc_value = this->dc_filter_red.w;
    data->last_beat_threshold = this->last_beat_threshold;
    data->dc_filtered_ir = this->dc_filter_ir.result;
    data->dc_filtered_red = this->dc_filter_red.result;

    return ESP_OK;
}

bool max30100_detect_pulse(max30100_config_t *this, float sensor_value) {
    static float prev_sensor_value = 0;
    static uint8_t values_went_down = 0;
    static uint32_t current_beat = 0;
    static uint32_t last_beat = 0;

    if (sensor_value > this->pulse_max_threshold) {
        this->current_pulse_detector_state = MAX30100_PULSE_IDLE;
        prev_sensor_value = 0;
        last_beat = 0;
        current_beat = 0;
        values_went_down = 0;
        this->last_beat_threshold = 0;
        return false;
    }

    switch (this->current_pulse_detector_state) {
        case MAX30100_PULSE_IDLE:
            if (sensor_value >= this->pulse_min_threshold) {
                this->current_pulse_detector_state = MAX30100_PULSE_TRACE_UP;
                values_went_down = 0;
            }
            break;
        case MAX30100_PULSE_TRACE_UP:
            if (sensor_value > prev_sensor_value) {
                current_beat = (uint32_t)(xTaskGetTickCount() * portTICK_PERIOD_MS);
                this->last_beat_threshold = sensor_value;
            } else {
                if (this->debug) {
                    printf("Peak reached: %f %f\n",
                        sensor_value,
                        prev_sensor_value);
                }

                uint32_t beat_duration = current_beat - last_beat;
                last_beat = current_beat;

                float raw_bpm = 0;
                if (beat_duration) {
                    raw_bpm = 60000.0 / (float)beat_duration;
                }

                if (this->debug) {
                    printf("Beat duration: %u\n", beat_duration);
                    printf("Raw BPM: %f\n", raw_bpm);
                }

                this->current_pulse_detector_state = MAX30100_PULSE_TRACE_DOWN;

                // Reset filter after a while without pulses
                if (beat_duration > 2500) { // 2.5 seconds
                    memset(this->values_bpm, 0, sizeof(float) * this->pulse_bpm_sample_size);
                    this->values_bpm_sum = 0;
                    this->values_bpm_count = 0;
                    this->bpm_index = 0;

                    if (this->debug) {
                        printf("Moving avg. reseted\n");
                    }
                }

                // Test if out of bounds
                if (raw_bpm < 50 || raw_bpm > 220) {
                    if (this->debug) {
                        printf("BPM out of bounds. Not adding to Moving Avg.\n");
                    }

                    return false;
                }

                // Optimized filter
                this->values_bpm_sum -= this->values_bpm[this->bpm_index];
                this->values_bpm[this->bpm_index] = raw_bpm;
                this->values_bpm_sum += this->values_bpm[this->bpm_index++];

                this->bpm_index %= this->pulse_bpm_sample_size;

                if (this->values_bpm_count < this->pulse_bpm_sample_size) {
                    this->values_bpm_count++;
                }

                this->current_bpm = this->values_bpm_sum / this->values_bpm_count;

                if (this->debug) {
                    printf("CurrentMoving Avg: ");

                    for (int i = 0; i < this->values_bpm_count; i++) {
                        printf("%f ", this->values_bpm[i]);
                    }

                    printf(" \n");
                    printf("AVg. BPM: %f\n", this->current_bpm);
                }

                return true;
            }
            break;
        case MAX30100_PULSE_TRACE_DOWN:
            if (sensor_value < prev_sensor_value) {
                values_went_down++;
            }

            if (sensor_value < this->pulse_min_threshold) {
                this->current_pulse_detector_state = MAX30100_PULSE_IDLE;
            }

            break;
    }

    prev_sensor_value = sensor_value;
    return false;
}

esp_err_t max30100_balance_intensities(max30100_config_t *this,
    float red_dc,
    float ir_dc) {
    if ((uint32_t)(xTaskGetTickCount() * portTICK_PERIOD_MS) -
        this->last_red_current_check >= this->red_current_adj_ms) {
        // printf("%f\n", red_dc - ir_dc);
        if (ir_dc - red_dc > this->acceptable_intense_diff &&
            this->red_current < MAX30100_LED_CURRENT_50MA) {
            this->red_current++;
            esp_err_t ret = max30100_set_led_current(this,
                this->red_current,
                this->ir_current);
            if (ret != ESP_OK) {
                return ret;
            }
            if (this->debug) {
                printf("RED LED Current +\n");
            }

        } else if (red_dc - ir_dc > this->acceptable_intense_diff &&
                   this->red_current > 0) {
            this->red_current--;
            esp_err_t ret = max30100_set_led_current(this,
                this->red_current,
                this->ir_current);
            if (ret != ESP_OK) {
                return ret;
            }
            if (this->debug) {
                printf("RED LED Current -\n");
            }
        }

        this->last_red_current_check = (uint32_t)(xTaskGetTickCount() *
            portTICK_PERIOD_MS);

    }
    return ESP_OK;
}



// Writes val to address register on device
esp_err_t max30100_write_register(max30100_config_t *this,
    uint8_t address,
    uint8_t val) {
    apply_bus(this->device_pos);
    // start transmission to device
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (this->i2c_addr << 1) | I2C_MASTER_WRITE, true);

    i2c_master_write_byte(cmd, address, true); // send register address
    i2c_master_write_byte(cmd, val, true); // send value to write

    // end transmission
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(this->i2c_num,
        cmd,
        1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);
    free_bus(this->device_pos);
    if (ret != ESP_OK) {
        mp_raise_ValueError(MP_ERROR_TEXT("max30100 I2C bus error"));
    }
    return ret;
}

esp_err_t max30100_read_register(max30100_config_t *this,
    uint8_t address,
    uint8_t *reg) {
    apply_bus(this->device_pos);
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (this->i2c_addr << 1) | I2C_MASTER_WRITE, true);
    i2c_master_write_byte(cmd, address, true);

    // i2c_master_stop(cmd);
    i2c_master_start(cmd);

    i2c_master_write_byte(cmd, (this->i2c_addr << 1) | I2C_MASTER_READ, true);
    i2c_master_read_byte(cmd, reg, 1); // 1 is NACK

    // end transmission
    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(this->i2c_num,
        cmd,
        1000 / portTICK_PERIOD_MS);

    i2c_cmd_link_delete(cmd);
    free_bus(this->device_pos);
    if (ret != ESP_OK) {
        mp_raise_ValueError(MP_ERROR_TEXT("max30100 I2C bus error"));
    }
    return ret;
}

// Reads num bytes starting from address register on device in to _buff array
esp_err_t max30100_read_from(max30100_config_t *this,
    uint8_t address,
    uint8_t *reg,
    uint8_t size) {
    if (!size) {
        return ESP_OK;
    }
    apply_bus(this->device_pos);
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (this->i2c_addr << 1) | I2C_MASTER_WRITE, 1);
    i2c_master_write_byte(cmd, address, true);

    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (this->i2c_addr << 1) | I2C_MASTER_READ, true);

    if (size > 1) {
        i2c_master_read(cmd, reg, size - 1, 0); // 0 is ACK

    }
    i2c_master_read_byte(cmd, reg + size - 1, 1); // 1 is NACK

    i2c_master_stop(cmd);
    esp_err_t ret = i2c_master_cmd_begin(this->i2c_num,
        cmd,
        1000 / portTICK_PERIOD_MS);
    i2c_cmd_link_delete(cmd);
    free_bus(this->device_pos);
    if (ret != ESP_OK) {
        mp_raise_ValueError(MP_ERROR_TEXT("max30100 I2C bus error"));
    }
    return ret;
}

esp_err_t max30100_set_mode(max30100_config_t *this, max30100_mode_t mode) {
    uint8_t current_mode_reg;
    // Tratar erros
    esp_err_t ret = max30100_read_register(this,
        MAX30100_MODE_CONF,
        &current_mode_reg);
    if (ret != ESP_OK) {
        return ret;
    }
    return max30100_write_register(this,
        MAX30100_MODE_CONF,
        (current_mode_reg & 0xF8) | mode);
}

esp_err_t max30100_set_high_res(max30100_config_t *this, bool enabled) {
    uint8_t previous;

    // Tratar erros
    esp_err_t ret = max30100_read_register(this, MAX30100_SPO2_CONF, &previous);
    if (ret != ESP_OK) {
        return ret;
    }
    if (enabled) {
        return max30100_write_register(this,
            MAX30100_SPO2_CONF,
            previous | MAX30100_SPO2_HI_RES_EN);
    } else {
        return max30100_write_register(this,
            MAX30100_SPO2_CONF,
            previous & ~MAX30100_SPO2_HI_RES_EN);
    }
}

esp_err_t max30100_set_sampling_rate(max30100_config_t *this,
    max30100_sampling_rate_t rate) {
    uint8_t current_spO2_reg;

    // Tratar erros
    esp_err_t ret = max30100_read_register(this,
        MAX30100_SPO2_CONF,
        &current_spO2_reg);
    if (ret != ESP_OK) {
        return ret;
    }
    return max30100_write_register(this,
        MAX30100_SPO2_CONF,
        (current_spO2_reg & 0xE3) | (rate << 2));
}

esp_err_t max30100_set_pulse_width(max30100_config_t *this,
    max30100_pulse_width_t pw) {
    uint8_t current_spO2_reg;

    // Tratar erros
    esp_err_t ret = max30100_read_register(this,
        MAX30100_SPO2_CONF,
        &current_spO2_reg);
    if (ret != ESP_OK) {
        return ret;
    }
    return max30100_write_register(this,
        MAX30100_SPO2_CONF,
        (current_spO2_reg & 0xFC) | pw);
}

esp_err_t max30100_set_led_current(max30100_config_t *this,
    max30100_current_t red_current,
    max30100_current_t ir_current) {
    // Tratar erros
    return max30100_write_register(this,
        MAX30100_LED_CONF,
        (red_current << 4) | ir_current);
}

esp_err_t max30100_set_acceptable_intense_difff(max30100_config_t *this,
    uint32_t acceptable_intense_diff) {
    // Add possible error check
    this->acceptable_intense_diff = acceptable_intense_diff;
    return ESP_OK;
}
esp_err_t max30100_set_red_current_adj_ms(max30100_config_t *this, uint32_t red_current_adj_ms) {
    // Add possible error check
    this->red_current_adj_ms = red_current_adj_ms;
    return ESP_OK;
}

esp_err_t max30100_set_reset_spo2_pulse_n(max30100_config_t *this, uint8_t reset_spo2_pulse_n) {
    // Add possible error check
    this->reset_spo2_pulse_n = reset_spo2_pulse_n;
    return ESP_OK;
}

esp_err_t max30100_set_dc_alpha(max30100_config_t *this, float dc_alpha) {
    // Add possible error check
    this->dc_alpha = dc_alpha;
    return ESP_OK;
}

esp_err_t max30100_set_pulse_min_threshold(max30100_config_t *this, uint16_t pulse_min_threshold) {
    // Add possible error check
    this->pulse_min_threshold = pulse_min_threshold;
    return ESP_OK;
}

esp_err_t max30100_set_pulse_max_threshold(max30100_config_t *this, uint16_t pulse_max_threshold) {
    // Add possible error check
    this->pulse_max_threshold = pulse_max_threshold;
    return ESP_OK;
}

esp_err_t max330100_read_temperature(max30100_config_t *this, float *temperature) {
    uint8_t current_mode_reg;
    // Tratar erros
    esp_err_t ret = max30100_read_register(this,
        MAX30100_MODE_CONF,
        &current_mode_reg);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_write_register(this,
        MAX30100_MODE_CONF,
        current_mode_reg | MAX30100_MODE_TEMP_EN);
    if (ret != ESP_OK) {
        return ret;
    }
    // This can be changed to a while loop, (with interrupt flag!)
    // there is an interrupt flag for when temperature has been read.
    vTaskDelay(100 / portTICK_PERIOD_MS);

    int8_t temp;
    // Tratar erros
    ret = max30100_read_register(this, MAX30100_TEMP_INT, (uint8_t *)&temp);
    if (ret != ESP_OK) {
        return ret;
    }

    float temp_fraction;
    ret = max30100_read_register(this,
        MAX30100_TEMP_FRACTION,
        (uint8_t *)&temp_fraction);
    if (ret != ESP_OK) {
        return ret;
    }
    temp_fraction *= 0.0625;
    *temperature = (float)temp + temp_fraction;
    return ESP_OK;
}

esp_err_t max30100_read_fifo(max30100_config_t *this, max30100_fifo_t *fifo) {
    uint8_t buffer[4];
    // Testar erros
    esp_err_t ret = max30100_read_from(this, MAX30100_FIFO_DATA, buffer, 4);
    if (ret != ESP_OK) {
        return ret;
    }
    fifo->raw_ir = ((uint16_t)buffer[0] << 8) | buffer[1];
    fifo->raw_red = ((uint16_t)buffer[2] << 8) | buffer[3];

    return ESP_OK;
}

max30100_dc_filter_t max30100_dc_removal(float x,
    float prev_w,
    float alpha) {
    max30100_dc_filter_t filtered = {};
    filtered.w = x + alpha * prev_w;
    filtered.result = filtered.w - prev_w;

    return filtered;
}

void max30100_lpb_filter(max30100_config_t *this, float x) {
    this->lpb_filter_ir.v[0] = this->lpb_filter_ir.v[1];

    // Fs = 100Hz and Fc = 10Hz
    this->lpb_filter_ir.v[1] = (2.452372752527856026e-1 * x) +
        (0.50952544949442879485 * this->lpb_filter_ir.v[0]);

    // Fs = 100Hz and Fc = 4Hz
    // this->lpb_filter_ir.v[1] = (1.367287359973195227e-1 * x)
    //                   + (0.72654252800536101020 * this->lpb_filter_ir.v[0]);
    // Very precise butterworth filter

    this->lpb_filter_ir.result = this->lpb_filter_ir.v[0] +
        this->lpb_filter_ir.v[1];
}

float max30100_mean_diff(max30100_config_t *this, float M) {
    float avg = 0;

    this->mean_diff_ir.sum -= this->mean_diff_ir.values[this->mean_diff_ir.index];
    this->mean_diff_ir.values[this->mean_diff_ir.index] = M;
    this->mean_diff_ir.sum += this->mean_diff_ir.values[this->mean_diff_ir.index++];

    this->mean_diff_ir.index = this->mean_diff_ir.index % this->mean_filter_size;

    if (this->mean_diff_ir.count < this->mean_filter_size) {
        this->mean_diff_ir.count++;
    }

    avg = this->mean_diff_ir.sum / this->mean_diff_ir.count;
    return avg - M;
}

esp_err_t max30100_print_registers(max30100_config_t *this) {
    uint8_t int_status, int_enable, fifo_write, fifo_ovf_cnt, fifo_read;
    uint8_t fifo_data, mode_conf, sp02_conf, led_conf, temp_int, temp_frac;
    uint8_t rev_id, part_id;
    esp_err_t ret;

    ret = max30100_read_register(this, MAX30100_INT_STATUS, &int_status);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_INT_ENABLE, &int_enable);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_FIFO_WRITE, &fifo_write);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this,
        MAX30100_FIFO_OVERFLOW_COUNTER,
        &fifo_ovf_cnt);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_FIFO_READ, &fifo_read);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_FIFO_DATA, &fifo_data);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_MODE_CONF, &mode_conf);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_SPO2_CONF, &sp02_conf);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_LED_CONF, &led_conf);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_TEMP_INT, &temp_int);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_TEMP_FRACTION, &temp_frac);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_REV_ID, &rev_id);
    if (ret != ESP_OK) {
        return ret;
    }
    ret = max30100_read_register(this, MAX30100_PART_ID, &part_id);
    if (ret != ESP_OK) {
        return ret;
    }

    printf("%x\n", int_status);
    printf("%x\n", int_enable);
    printf("%x\n", fifo_write);
    printf("%x\n", fifo_ovf_cnt);
    printf("%x\n", fifo_read);
    printf("%x\n", fifo_data);
    printf("%x\n", mode_conf);
    printf("%x\n", sp02_conf);
    printf("%x\n", led_conf);
    printf("%x\n", temp_int);
    printf("%x\n", temp_frac);
    printf("%x\n", rev_id);
    printf("%x\n", part_id);

    return ESP_OK;
}

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

/*
 * SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */
#include "uwb_port.h"

#include <string.h>

#include "deca_device_api.h"
#include "deca_interface.h"
#include "driver/spi_master.h"
#include "driver/uart.h"
#include "esp_err.h"
#include "esp_private/periph_ctrl.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "rom/ets_sys.h"
#include "soc/periph_defs.h"

#define UWB_SPI_HOST SPI2_HOST
#define UWB_SPI_SLOW_HZ 2000000
#define UWB_SPI_FAST_HZ 2000000
#define UWB_MAX_TRANSFER 256

static uwb_port_config_t port_config;
static spi_device_handle_t spi_device;
static bool bus_initialized;
static portMUX_TYPE driver_mutex = portMUX_INITIALIZER_UNLOCKED;

static int spi_set_speed(int speed_hz) {
    if (spi_device != NULL) {
        spi_bus_remove_device(spi_device);
        spi_device = NULL;
    }
    spi_device_interface_config_t device_config = {
        .clock_speed_hz = speed_hz,
        .mode = 0,
        .spics_io_num = port_config.cs,
        .queue_size = 1,
        .cs_ena_pretrans = 8,
        .cs_ena_posttrans = 8,
    };
    return spi_bus_add_device(UWB_SPI_HOST, &device_config, &spi_device);
}

int32_t uwb_spi_read(uint16_t header_len, uint8_t *header, uint16_t data_len, uint8_t *data) {
    uint32_t total = (uint32_t)header_len + data_len;
    if (spi_device == NULL || total > UWB_MAX_TRANSFER) {
        return DWT_ERROR;
    }
    uint8_t tx[UWB_MAX_TRANSFER] = {0};
    uint8_t rx[UWB_MAX_TRANSFER] = {0};
    memcpy(tx, header, header_len);
    spi_transaction_t transaction = {
        .length = total * 8,
        .rxlength = total * 8,
        .tx_buffer = tx,
        .rx_buffer = rx,
    };
    if (spi_device_polling_transmit(spi_device, &transaction) != ESP_OK) {
        return DWT_ERROR;
    }
    memcpy(data, rx + header_len, data_len);
    return DWT_SUCCESS;
}

int32_t uwb_spi_write(uint16_t header_len, const uint8_t *header, uint16_t data_len, const uint8_t *data) {
    uint32_t total = (uint32_t)header_len + data_len;
    if (spi_device == NULL || total > UWB_MAX_TRANSFER) {
        return DWT_ERROR;
    }
    uint8_t tx[UWB_MAX_TRANSFER];
    memcpy(tx, header, header_len);
    memcpy(tx + header_len, data, data_len);
    spi_transaction_t transaction = {.length = total * 8, .tx_buffer = tx};
    return spi_device_polling_transmit(spi_device, &transaction) == ESP_OK ? DWT_SUCCESS : DWT_ERROR;
}

int32_t uwb_spi_write_crc(uint16_t header_len, const uint8_t *header, uint16_t data_len,
    const uint8_t *data, uint8_t crc) {
    uint32_t total = (uint32_t)header_len + data_len + 1;
    if (spi_device == NULL || total > UWB_MAX_TRANSFER) {
        return DWT_ERROR;
    }
    uint8_t tx[UWB_MAX_TRANSFER];
    memcpy(tx, header, header_len);
    memcpy(tx + header_len, data, data_len);
    tx[total - 1] = crc;
    spi_transaction_t transaction = {.length = total * 8, .tx_buffer = tx};
    return spi_device_polling_transmit(spi_device, &transaction) == ESP_OK ? DWT_SUCCESS : DWT_ERROR;
}

static void spi_slow(void) {
    (void)spi_set_speed(UWB_SPI_SLOW_HZ);
}
static void spi_fast(void) {
    (void)spi_set_speed(UWB_SPI_FAST_HZ);
}

extern const struct dwt_driver_s dw3720_driver;
static const struct dwt_spi_s spi_functions = {
    .readfromspi = uwb_spi_read,
    .writetospi = uwb_spi_write,
    .writetospiwithcrc = uwb_spi_write_crc,
    .setslowrate = spi_slow,
    .setfastrate = spi_fast,
};
static const struct dwt_driver_s *driver_list[] = {&dw3720_driver};
const struct dwt_probe_s uwb_probe_interface = {
    .dw = NULL,
    .spi = (void *)&spi_functions,
    .wakeup_device_with_io = uwb_port_wakeup,
    .driver_list = (struct dwt_driver_s **)driver_list,
    .dw_driver_num = 1,
};

decaIrqStatus_t decamutexon(void) {
    portENTER_CRITICAL(&driver_mutex);
    return 0;
}
void decamutexoff(decaIrqStatus_t status) {
    (void)status;
    portEXIT_CRITICAL(&driver_mutex);
}
void deca_sleep(unsigned int time_ms) {
    vTaskDelay(pdMS_TO_TICKS(time_ms));
}
void deca_usleep(unsigned long time_us) {
    ets_delay_us(time_us);
}
void wakeup_device_with_io(void) {
    uwb_port_wakeup();
}

int uwb_port_init(const uwb_port_config_t *config) {
    port_config = *config;

    uart_driver_delete(UART_NUM_0);
    periph_module_reset(PERIPH_UART0_MODULE);
    gpio_reset_pin(port_config.mosi);
    gpio_reset_pin(port_config.miso);
    gpio_reset_pin(port_config.clock);
    gpio_reset_pin(port_config.cs);

    gpio_config_t input_config = {
        .pin_bit_mask = (1ULL << port_config.irq) | (1ULL << port_config.reset),
        .mode = GPIO_MODE_INPUT,
    };
    esp_err_t error = gpio_config(&input_config);
    if (error != ESP_OK) {
        return error;
    }
    gpio_config_t output_config = {
        .pin_bit_mask = 1ULL << port_config.wakeup,
            .mode = GPIO_MODE_OUTPUT,
    };
    if (gpio_config(&output_config) != ESP_OK || gpio_set_level(port_config.wakeup, 0) != ESP_OK) {
        return ESP_FAIL;
    }

    spi_bus_config_t bus_config = {
        .mosi_io_num = port_config.mosi,
        .miso_io_num = port_config.miso,
        .sclk_io_num = port_config.clock,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = UWB_MAX_TRANSFER,
        .flags = SPICOMMON_BUSFLAG_MASTER,
    };
    error = spi_bus_initialize(UWB_SPI_HOST, &bus_config, SPI_DMA_CH_AUTO);
    if (error != ESP_OK) {
        return error;
    }
    bus_initialized = true;
    return spi_set_speed(UWB_SPI_SLOW_HZ);
}

void uwb_port_reset(void) {
    gpio_set_direction(port_config.reset, GPIO_MODE_OUTPUT);
    gpio_set_level(port_config.reset, 0);
    vTaskDelay(pdMS_TO_TICKS(1));
    gpio_set_level(port_config.reset, 1);
    vTaskDelay(pdMS_TO_TICKS(2));
    gpio_set_direction(port_config.reset, GPIO_MODE_INPUT);
    vTaskDelay(pdMS_TO_TICKS(100));
}

void uwb_port_wakeup(void) {
    gpio_set_level(port_config.wakeup, 1);
    ets_delay_us(600);
    gpio_set_level(port_config.wakeup, 0);
    vTaskDelay(pdMS_TO_TICKS(1));
}

void uwb_port_deinit(void) {
    if (spi_device != NULL) {
        spi_bus_remove_device(spi_device);
        spi_device = NULL;
    }
    if (bus_initialized) {
        spi_bus_free(UWB_SPI_HOST);
        bus_initialized = false;
    }
    gpio_reset_pin(port_config.irq);
    gpio_reset_pin(port_config.wakeup);
    gpio_reset_pin(port_config.reset);
    gpio_reset_pin(port_config.mosi);
    gpio_reset_pin(port_config.miso);
    gpio_reset_pin(port_config.clock);
    gpio_reset_pin(port_config.cs);
}

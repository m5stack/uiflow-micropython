#include "uiflow_utility.h"

static const char *TAG = "UIFLOW_UTILITY";

// NVS Read/Write Helpers
bool nvs_read_str_helper(char *ns, char *key, char *value, size_t *_len) {
    nvs_handle_t nvs_handle;
    esp_err_t ret = nvs_open(ns, NVS_READONLY, &nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Read
    ret = nvs_get_str(nvs_handle, key, value, _len);

    // Close
    nvs_close(nvs_handle);

    ESP_LOGI(TAG, "Read String Key: %s Value: %s", key, value);
    return ret == ESP_OK ? true : false;
}

bool nvs_write_str_helper(char *ns, char *key, char *value) {
    nvs_handle_t nvs_handle;
    esp_err_t ret = nvs_open(ns, NVS_READWRITE, &nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Write
    ret = nvs_set_str(nvs_handle, key, value);
    if (ret != ESP_OK) {
        return false;
    }

    // Commit
    ret = nvs_commit(nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Close
    nvs_close(nvs_handle);

    ESP_LOGI(TAG, "Write String Key: %s Value: %s", key, value);
    return ret == ESP_OK ? true : false;
}

bool nvs_read_u8_helper(char *ns, char *key, uint8_t *value) {
    nvs_handle_t nvs_handle;
    esp_err_t ret = nvs_open(ns, NVS_READONLY, &nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Read
    ret = nvs_get_u8(nvs_handle, key, value);

    // Close
    nvs_close(nvs_handle);

    ESP_LOGI(TAG, "Read U8 Key: %s Value: %d", key, *value);
    return ret == ESP_OK ? true : false;
}

bool nvs_write_u8_helper(char *ns, char *key, uint8_t value) {
    nvs_handle_t nvs_handle;
    esp_err_t ret = nvs_open(ns, NVS_READWRITE, &nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Write
    ret = nvs_set_u8(nvs_handle, key, value);
    if (ret != ESP_OK) {
        return false;
    }

    // Commit
    ret = nvs_commit(nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Close
    nvs_close(nvs_handle);

    ESP_LOGI(TAG, "Write U8 Key: %s Value: %d", key, value);
    return ret == ESP_OK ? true : false;
}

bool nvs_read_u32_helper(char *ns, char *key, uint32_t *value) {
    nvs_handle_t nvs_handle;
    esp_err_t ret = nvs_open(ns, NVS_READONLY, &nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Read
    ret = nvs_get_u32(nvs_handle, key, value);

    // Close
    nvs_close(nvs_handle);

    ESP_LOGI(TAG, "Read U32 Key: %s Value: %d", key, *value);
    return ret == ESP_OK ? true : false;
}

bool nvs_write_u32_helper(char *ns, char *key, uint32_t value) {
    nvs_handle_t nvs_handle;
    esp_err_t ret = nvs_open(ns, NVS_READWRITE, &nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Write
    ret = nvs_set_u32(nvs_handle, key, value);
    if (ret != ESP_OK) {
        return false;
    }

    // Commit
    ret = nvs_commit(nvs_handle);
    if (ret != ESP_OK) {
        return false;
    }

    // Close
    nvs_close(nvs_handle);

    ESP_LOGI(TAG, "Write U32 Key: %s Value: %d", key, value);
    return ret == ESP_OK ? true : false;
}

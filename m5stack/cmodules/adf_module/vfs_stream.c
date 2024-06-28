/*
 * ESPRESSIF MIT License
 *
 * Copyright (c) 2019 <ESPRESSIF SYSTEMS (SHANGHAI) CO., LTD>
 *
 * Permission is hereby granted for use on all ESPRESSIF SYSTEMS products, in which case,
 * it is free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the Software is furnished
 * to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or
 * substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 * FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
 * COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
 * IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 *
 */

#include "errno.h"
#include <string.h>

#include "audio_element.h"
#include "audio_error.h"
#include "audio_mem.h"

#include "esp_log.h"
#include "vfs_stream.h"
#include "wav_head.h"

#include <extmod/vfs.h>
#include <extmod/vfs_lfs.h>
#include "extmod/vfs_fat.h"
#include "lib/littlefs/lfs2.h"
#include "lib/oofatfs/ff.h"
#include "py/builtin.h"
#include "py/objstr.h"
#include "py/runtime.h"
#include "py/stream.h"

#define FILE_WAV_SUFFIX_TYPE   "wav"
#define FILE_OPUS_SUFFIX_TYPE  "opus"
#define FILE_AMR_SUFFIX_TYPE   "amr"
#define FILE_AMRWB_SUFFIX_TYPE "Wamr"

static const char *TAG = "VFS_STREAM";

typedef enum {
    STREAM_TYPE_UNKNOW,
    STREAM_TYPE_WAV,
    STREAM_TYPE_OPUS,
    STREAM_TYPE_AMR,
    STREAM_TYPE_AMRWB,
} wr_stream_type_t;

typedef struct _mp_obj_vfs_lfs2_t {
    mp_obj_base_t base;
    mp_vfs_blockdev_t blockdev;
    bool enable_mtime;
    vstr_t cur_dir;
    struct lfs2_config config;
    lfs2_t lfs;
} mp_obj_vfs_lfs2_t;

typedef struct vfs_stream {
    audio_stream_type_t type;
    int block_size;
    bool is_open;
    wr_stream_type_t w_type;
    FATFS *fatfs;
    lfs2_t *lfs2;
    union {
        FIL fat_file;
        lfs2_file_t *lfs2_file;
    } file;
} vfs_stream_t;


static esp_err_t _vfs_open(audio_element_handle_t self);
static esp_err_t _vfs_close(audio_element_handle_t self);
static int _vfs_process(audio_element_handle_t self, char *in_buffer, int in_len);
static esp_err_t _vfs_destroy(audio_element_handle_t self);
static int _vfs_write(audio_element_handle_t self, char *buffer, int len, TickType_t ticks_to_wait, void *context);
static int _vfs_read(audio_element_handle_t self, char *buffer, int len, TickType_t ticks_to_wait, void *context);

static wr_stream_type_t get_type(const char *str);


audio_element_handle_t vfs_stream_init(vfs_stream_cfg_t *config) {
    audio_element_handle_t el;
    vfs_stream_t *vfs = audio_calloc(1, sizeof(vfs_stream_t));

    AUDIO_MEM_CHECK(TAG, vfs, return NULL);

    // esp_vfs_littlefs_conf_t conf = {
    //     .base_path = "/flash",
    //     .partition_label = "vfs",
    //     .format_if_mount_failed = false,
    //     .dont_mount = true,
    // };

    // esp_vfs_littlefs_register(&conf);

    const char *path_out;
    mp_vfs_mount_t *existing_mount = mp_vfs_lookup_path("/flash", &path_out);
    if (existing_mount == MP_VFS_NONE || existing_mount == MP_VFS_ROOT) {
        ESP_LOGE(TAG, "No vfs mount");
        goto _vfs_init_exit;
    }
    // fs_user_mount_t *user_mount = MP_OBJ_TO_PTR(existing_mount->obj);
    // if (user_mount == NULL) {
    //     ESP_LOGE(TAG, "No user mount");
    //     goto _vfs_init_exit;
    // }
    vfs->lfs2 = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(existing_mount->obj))->lfs;

    audio_element_cfg_t cfg = DEFAULT_AUDIO_ELEMENT_CONFIG();
    cfg.open = _vfs_open;
    cfg.close = _vfs_close;
    cfg.process = _vfs_process;
    cfg.destroy = _vfs_destroy;
    cfg.task_stack = config->task_stack;
    cfg.task_prio = config->task_prio;
    cfg.task_core = config->task_core;
    cfg.out_rb_size = config->out_rb_size;
    cfg.buffer_len = config->buf_sz;
    if (cfg.buffer_len == 0) {
        cfg.buffer_len = VFS_STREAM_BUF_SIZE;
    }

    cfg.tag = "file";
    vfs->type = config->type;

    if (config->type == AUDIO_STREAM_WRITER) {
        cfg.write = _vfs_write;
    } else {
        cfg.read = _vfs_read;
    }
    el = audio_element_init(&cfg);

    AUDIO_MEM_CHECK(TAG, el, goto _vfs_init_exit);
    audio_element_setdata(el, vfs);
    return el;
_vfs_init_exit:
    audio_free(vfs);
    return NULL;
}


static wr_stream_type_t get_type(const char *str) {
    char *relt = strrchr(str, '.');
    if (relt != NULL) {
        relt++;
        ESP_LOGD(TAG, "result = %s", relt);
        if (strncasecmp(relt, FILE_WAV_SUFFIX_TYPE, 3) == 0) {
            return STREAM_TYPE_WAV;
        } else if (strncasecmp(relt, FILE_OPUS_SUFFIX_TYPE, 4) == 0) {
            return STREAM_TYPE_OPUS;
        } else if (strncasecmp(relt, FILE_AMR_SUFFIX_TYPE, 3) == 0) {
            return STREAM_TYPE_AMR;
        } else if (strncasecmp(relt, FILE_AMRWB_SUFFIX_TYPE, 4) == 0) {
            return STREAM_TYPE_AMRWB;
        } else {
            return STREAM_TYPE_UNKNOW;
        }
    } else {
        return STREAM_TYPE_UNKNOW;
    }
}


static esp_err_t _vfs_open(audio_element_handle_t self) {
    vfs_stream_t *vfs = (vfs_stream_t *)audio_element_getdata(self);

    char *uri = audio_element_get_uri(self);
    if (uri == NULL) {
        ESP_LOGE(TAG, "Error, uri is not set");
        return ESP_FAIL;
    }
    ESP_LOGI(TAG, "_vfs_open, uri:%s", uri);
    char *path = strstr(uri, "file:/");
    if (path == NULL) {
        ESP_LOGE(TAG, "Error, need file path to open");
        return ESP_FAIL;
    }
    if (vfs->is_open) {
        ESP_LOGE(TAG, "already opened");
        return ESP_FAIL;
    }
    path += strlen("file:/");

    const char *path_out;
    mp_vfs_mount_t *existing_mount = mp_vfs_lookup_path(path, &path_out);
    if (existing_mount == MP_VFS_NONE || existing_mount == MP_VFS_ROOT) {
        ESP_LOGE(TAG, "No vfs mount");
        return ESP_FAIL;
    }
    // fs_user_mount_t *user_mount = MP_OBJ_TO_PTR(existing_mount->obj);
    // if (user_mount == NULL) {
    //     ESP_LOGE(TAG, "No user mount");
    //     goto _vfs_init_exit;
    // }
    if (strstr(uri, "flash")) {
        vfs->lfs2 = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(existing_mount->obj))->lfs;
    } else if (strstr(uri, "sdcard")) {
        vfs->fatfs = &((fs_user_mount_t *)MP_OBJ_TO_PTR(existing_mount->obj))->fatfs;
    }

    ESP_LOGI(TAG, "_vfs_open, path:%s", path_out);

    audio_element_info_t info;
    audio_element_getinfo(self, &info);

    if (vfs->lfs2) {
        if (vfs->type == AUDIO_STREAM_READER) {

            struct lfs2_file_config config;
            memset(&config, 0x00, sizeof(config));
            // TODO
            config.buffer = malloc(vfs->lfs2->cfg->cache_size * sizeof(uint8_t));
            vfs->file.lfs2_file = (lfs2_file_t *)malloc(1 * sizeof(lfs2_file_t));
            int res = lfs2_file_opencfg(vfs->lfs2, vfs->file.lfs2_file, path_out, LFS2_O_RDONLY, &config);

            if (res == LFS2_ERR_OK) {
                struct lfs2_info fno;
                lfs2_stat(vfs->lfs2, path_out, &fno);
                info.total_bytes = fno.size;
                ESP_LOGI(TAG, "File size: %d byte, file position: %d", (int)fno.size, (int)info.byte_pos);
                if (info.byte_pos > 0) {
                    if (lfs2_file_seek(vfs->lfs2, vfs->file.lfs2_file, info.byte_pos, LFS2_SEEK_SET) < 0) {
                        ESP_LOGE(TAG, "Error seek file. Error message: %s, line: %d", strerror(errno), __LINE__);
                        return ESP_FAIL;
                    }
                }
            } else {
                ESP_LOGE(TAG, "failed to open %s(%d)", path_out, res);
                return ESP_FAIL;
            }
        } else if (vfs->type == AUDIO_STREAM_WRITER) {

            struct lfs2_file_config config;
            memset(&config, 0x00, sizeof(config));
            // TODO
            config.buffer = malloc(vfs->lfs2->cfg->cache_size * sizeof(uint8_t));
            vfs->file.lfs2_file = (lfs2_file_t *)malloc(1 * sizeof(lfs2_file_t));
            int res = lfs2_file_opencfg(vfs->lfs2, vfs->file.lfs2_file, path_out, LFS2_O_RDWR | LFS2_O_CREAT | LFS2_O_TRUNC, &config);

            if (res == LFS2_ERR_OK) {
                vfs->w_type = get_type(path_out);
                UINT bw = 0;
                if ((STREAM_TYPE_WAV == vfs->w_type)) {
                    wav_header_t info = {0};
                    lfs2_file_write(vfs->lfs2, vfs->file.lfs2_file, &info, sizeof(wav_header_t));
                    lfs2_file_sync(vfs->lfs2, vfs->file.lfs2_file);
                } else if ((STREAM_TYPE_AMR == vfs->w_type)) {
                    lfs2_file_write(vfs->lfs2, vfs->file.lfs2_file, "#!AMR\n", 6);
                    lfs2_file_sync(vfs->lfs2, vfs->file.lfs2_file);
                } else if ((STREAM_TYPE_AMRWB == vfs->w_type)) {
                    lfs2_file_write(vfs->lfs2, vfs->file.lfs2_file, "#!AMR-WB\n", 9);
                    lfs2_file_sync(vfs->lfs2, vfs->file.lfs2_file);
                }
            } else {
                ESP_LOGE(TAG, "failed to open %s", path_out);
                return ESP_FAIL;
            }
        } else {
            ESP_LOGE(TAG, "vfs must be Reader or Writer");
            return ESP_FAIL;
        }
    } else if (vfs->fatfs) {
        if (vfs->type == AUDIO_STREAM_READER) {
            FRESULT ret = f_open(vfs->fatfs, &vfs->file.fat_file, path, FA_READ);
            if (ret == FR_OK) {
                FILINFO fno = { 0 };
                f_stat(vfs->fatfs, path, &fno);
                info.total_bytes = fno.fsize;
                ESP_LOGI(TAG, "File size: %d byte, file position: %d", (int)fno.fsize, (int)info.byte_pos);
                if (info.byte_pos > 0) {
                    if (f_lseek(&vfs->file.fat_file, info.byte_pos) < 0) {
                        ESP_LOGE(TAG, "Error seek file. Error message: %s, line: %d", strerror(errno), __LINE__);
                        return ESP_FAIL;
                    }
                }
            } else {
                ESP_LOGE(TAG, "failed to open %s(%d)", path_out, ret);
                return ESP_FAIL;
            }
        } else if (vfs->type == AUDIO_STREAM_WRITER) {
            FRESULT ret = f_open(vfs->fatfs, &vfs->file.fat_file, path, FA_WRITE | FA_CREATE_ALWAYS);
            if (ret == FR_OK) {
                vfs->w_type = get_type(path_out);
                UINT bw = 0;
                if ((STREAM_TYPE_WAV == vfs->w_type)) {
                    wav_header_t info = {0};
                    f_write(&vfs->file.fat_file, &info, sizeof(wav_header_t), &bw);
                    f_sync(&vfs->file.fat_file);
                } else if ((STREAM_TYPE_AMR == vfs->w_type)) {
                    f_write(&vfs->file.fat_file, "#!AMR\n", 6, &bw);
                    f_sync(&vfs->file.fat_file);
                } else if ((STREAM_TYPE_AMRWB == vfs->w_type)) {
                    f_write(&vfs->file.fat_file, "#!AMR-WB\n", 9, &bw);
                    f_sync(&vfs->file.fat_file);
                }
            } else {
                ESP_LOGE(TAG, "failed to open %s", path_out);
                return ESP_FAIL;
            }
        } else {
            ESP_LOGE(TAG, "vfs must be Reader or Writer");
            return ESP_FAIL;
        }
    }

    vfs->is_open = true;
    int ret = audio_element_set_total_bytes(self, info.total_bytes);
    return ret;
}


static int _vfs_read(audio_element_handle_t self, char *buffer, int len, TickType_t ticks_to_wait, void *context) {
    vfs_stream_t *vfs = (vfs_stream_t *)audio_element_getdata(self);
    audio_element_info_t info;
    audio_element_getinfo(self, &info);

    ESP_LOGI(TAG, "read len=%d, pos=%d/%d", len, (int)info.byte_pos, (int)info.total_bytes);

    if (vfs->lfs2) {
        UINT rlen = 0;
        rlen = lfs2_file_read(vfs->lfs2, vfs->file.lfs2_file, buffer, len);
        if (rlen <= 0) {
            ESP_LOGW(TAG, "No more data,ret:%d", rlen);
            rlen = 0;
        } else {
            info.byte_pos += rlen;
            audio_element_setinfo(self, &info);
        }
        return rlen;
    } else if (vfs->fatfs) {
        UINT rlen = 0;
        FRESULT ret = f_read(&vfs->file.fat_file, buffer, len, &rlen);
        if (ret != FR_OK) {
            ESP_LOGW(TAG, "No more data,ret:%d", ret);
            rlen = 0;
        } else {
            info.byte_pos += rlen;
            audio_element_setinfo(self, &info);
        }
        return rlen;
    }
    return 0;
}


static int _vfs_write(audio_element_handle_t self, char *buffer, int len, TickType_t ticks_to_wait, void *context) {
    vfs_stream_t *vfs = (vfs_stream_t *)audio_element_getdata(self);
    audio_element_info_t info;
    audio_element_getinfo(self, &info);
    UINT wlen = 0;

    if (vfs->lfs2) {
        wlen = lfs2_file_write(vfs->lfs2, vfs->file.lfs2_file, buffer, len);
        lfs2_file_sync(vfs->lfs2, vfs->file.lfs2_file);
    } else if (vfs->fatfs) {
        f_write(&vfs->file.fat_file, buffer, len, &wlen);
        f_sync(&vfs->file.fat_file);
    }

    ESP_LOGI(TAG, "mp_stream_posix_write,%d, errno:%d,pos:%d", wlen, errno, (int)info.byte_pos);
    if (wlen > 0) {
        info.byte_pos += wlen;
        audio_element_setinfo(self, &info);
    }
    return wlen;
}


static int _vfs_process(audio_element_handle_t self, char *in_buffer, int in_len) {
    int r_size = audio_element_input(self, in_buffer, in_len);
    int w_size = 0;
    if (r_size > 0) {
        w_size = audio_element_output(self, in_buffer, r_size);
    } else {
        w_size = r_size;
    }
    return w_size;
}


static esp_err_t _vfs_close(audio_element_handle_t self) {
    vfs_stream_t *vfs = (vfs_stream_t *)audio_element_getdata(self);

    if (vfs->lfs2) {
        if (
            AUDIO_STREAM_WRITER == vfs->type
            && STREAM_TYPE_WAV == vfs->w_type
            ) {
            wav_header_t *wav_info = (wav_header_t *)audio_malloc(sizeof(wav_header_t));

            AUDIO_MEM_CHECK(TAG, wav_info, return ESP_ERR_NO_MEM);

            lfs2_file_seek(vfs->lfs2, vfs->file.lfs2_file, 0, LFS2_SEEK_SET);
            audio_element_info_t info;
            UINT bw = 0;
            audio_element_getinfo(self, &info);
            wav_head_init(wav_info, info.sample_rates, info.bits, info.channels);
            wav_head_size(wav_info, (uint32_t)info.byte_pos);
            lfs2_file_write(vfs->lfs2, vfs->file.lfs2_file, wav_info, sizeof(wav_header_t));
            lfs2_file_sync(vfs->lfs2, vfs->file.lfs2_file);
            lfs2_file_close(vfs->lfs2, vfs->file.lfs2_file);
            audio_free(wav_info);
        }

        if (vfs->is_open) {
            lfs2_file_close(vfs->lfs2, vfs->file.lfs2_file);
            free(vfs->file.lfs2_file);
            vfs->is_open = false;
        }
    } else if (vfs->fatfs) {
        if (
            AUDIO_STREAM_WRITER == vfs->type
            && STREAM_TYPE_WAV == vfs->w_type
            ) {
            wav_header_t *wav_info = (wav_header_t *)audio_malloc(sizeof(wav_header_t));

            AUDIO_MEM_CHECK(TAG, wav_info, return ESP_ERR_NO_MEM);

            f_lseek(&vfs->file.fat_file, 0);
            audio_element_info_t info;
            UINT bw = 0;
            audio_element_getinfo(self, &info);
            wav_head_init(wav_info, info.sample_rates, info.bits, info.channels);
            wav_head_size(wav_info, (uint32_t)info.byte_pos);
            f_write(&vfs->file.fat_file, wav_info, sizeof(wav_header_t), &bw);
            f_sync(&vfs->file.fat_file);
            f_close(&vfs->file.fat_file);
            audio_free(wav_info);
        }

        if (vfs->is_open) {
            f_close(&vfs->file.fat_file);
            vfs->is_open = false;
        }
    }

    if (AEL_STATE_PAUSED != audio_element_get_state(self)) {
        audio_element_report_info(self);
        audio_element_info_t info = { 0 };
        audio_element_getinfo(self, &info);
        info.byte_pos = 0;
        audio_element_setinfo(self, &info);
    }

    vfs->lfs2 = NULL;
    vfs->fatfs = NULL;

    return ESP_OK;
}


static esp_err_t _vfs_destroy(audio_element_handle_t self) {
    vfs_stream_t *vfs = (vfs_stream_t *)audio_element_getdata(self);
    audio_free(vfs);
    return ESP_OK;
}


void log_file(char *buffer, size_t len) {
    const char *path_out;
    mp_vfs_mount_t *existing_mount = mp_vfs_lookup_path("/flash/output", &path_out);
    if (existing_mount == MP_VFS_NONE || existing_mount == MP_VFS_ROOT) {
        ESP_LOGE(TAG, "No vfs mount");
        return;
    }
    lfs2_t *log_lfs = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(existing_mount->obj))->lfs;

    struct lfs2_file_config config;
    memset(&config, 0x00, sizeof(config));

    config.buffer = malloc(log_lfs->cfg->cache_size * sizeof(uint8_t));
    lfs2_file_t *file = (lfs2_file_t *)malloc(1 * sizeof(lfs2_file_t));
    int res = lfs2_file_opencfg(log_lfs, file, "/output", LFS2_O_RDWR | LFS2_O_CREAT | LFS2_O_APPEND, &config);
    lfs2_file_write(log_lfs, file, buffer, len);
    lfs2_file_sync(log_lfs, file);
    lfs2_file_close(log_lfs, file);

    free(config.buffer);
    free(file);
}

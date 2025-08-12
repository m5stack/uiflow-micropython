/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#include <esp_log.h>
#include "py/runtime.h"
#include "py/stream.h"

#include <extmod/vfs.h>
#include <extmod/vfs_lfs.h>
#include "extmod/vfs_fat.h"
#include "lib/littlefs/lfs2.h"
#include "lib/oofatfs/ff.h"
#include "_vfs_stream.h"
#include <string.h>
#include <stdlib.h>

static const char *TAG = "VFS";

// micropython/extmod/vfs_lfs.c line: 115
typedef struct _mp_obj_vfs_lfs2_t {
    mp_obj_base_t base;
    mp_vfs_blockdev_t blockdev;
    bool enable_mtime;
    vstr_t cur_dir;
    struct lfs2_config config;
    lfs2_t lfs;
} mp_obj_vfs_lfs2_t;

typedef struct vfs_stream_t {
    bool is_open;
    FATFS *fatfs;
    lfs2_t *lfs2;
    struct lfs2_file_config lfs2_file_conf;
    union {
        FIL fat_file;
        lfs2_file_t *lfs2_file;
    } file;
} vfs_stream_t;


static int lfs2_get_mode(int flags) {
    int ret = 0;
    ret |= flags & VFS_READ ? LFS2_O_RDONLY : 0;
    ret = flags & VFS_WRITE ? LFS2_O_WRONLY : 0;
    ret |= flags & VFS_APPEND ? LFS2_O_APPEND : 0;
    ret |= flags & VFS_CREATE ? LFS2_O_CREAT | LFS2_O_TRUNC: 0;

    return ret;
}


static int fatfs_get_mode(int flags) {
    int ret = 0;

    ret |= flags & VFS_READ ? FA_READ : 0;
    ret |= flags & VFS_WRITE ? FA_WRITE : 0;
    ret |= flags & VFS_APPEND ? FA_OPEN_APPEND : 0;
    ret |= flags & VFS_CREATE ? FA_CREATE_ALWAYS : 0;

    return flags;
}


void *vfs_stream_open(const char *path, int flags) {
    ESP_LOGI(TAG, "vfs_stream_open: path=%s, mode=%d", path, flags);

    vfs_stream_t *vfs = calloc(1, sizeof(vfs_stream_t));

    const char *path_out = {'\0'};
    mp_vfs_mount_t *existing_mount = mp_vfs_lookup_path(path, &path_out);
    if (existing_mount == MP_VFS_NONE || existing_mount == MP_VFS_ROOT) {
        ESP_LOGE(TAG, "No vfs mount");
        goto _vfs_init_exit;
    }

    if (strstr(path_out, "flash")) {
        ESP_LOGD(TAG, "in flash");
        vfs->lfs2 = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(existing_mount->obj))->lfs;
    } else if (strstr(path_out, "system")) {
        ESP_LOGD(TAG, "in system");
        vfs->lfs2 = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(existing_mount->obj))->lfs;
    } else if (strstr(path_out, "sd")) {
        ESP_LOGD(TAG, "in sd");
        vfs->fatfs = &((fs_user_mount_t *)MP_OBJ_TO_PTR(existing_mount->obj))->fatfs;
    } else {
        ESP_LOGI(TAG, "default in flash");
        vfs->lfs2 = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(existing_mount->obj))->lfs;
    }

    if (vfs->lfs2) {
        vfs->lfs2_file_conf.buffer = calloc(vfs->lfs2->cfg->cache_size, sizeof(uint8_t));
        if (vfs->lfs2_file_conf.buffer == NULL) {
            ESP_LOGE(TAG, "failed to allocate buffer");
            goto _vfs_init_exit;
        }
        vfs->file.lfs2_file = (lfs2_file_t *)calloc(1, sizeof(lfs2_file_t));
        if (vfs->file.lfs2_file == NULL) {
            ESP_LOGE(TAG, "failed to allocate lfs2_file");
            goto _vfs_init_exit;
        }
        flags = lfs2_get_mode(flags);
        ESP_LOGD(TAG, "lfs2_get_mode: %d", flags);
        int res = lfs2_file_opencfg(vfs->lfs2, vfs->file.lfs2_file, path_out, flags, &vfs->lfs2_file_conf);
        if (res != LFS2_ERR_OK) {
            ESP_LOGE(TAG, "failed to open %s(%d)", path_out, res);
            goto _vfs_init_exit;
        }
    } else if (vfs->fatfs) {
        BYTE fmode = fatfs_get_mode(flags);
        FRESULT ret = f_open(vfs->fatfs, &vfs->file.fat_file, path_out, fmode);
        if (ret != FR_OK) {
            ESP_LOGE(TAG, "failed to open %s(%d)", path_out, ret);
            goto _vfs_init_exit;
        }
    }

    return vfs;
_vfs_init_exit:
    if (vfs->lfs2_file_conf.buffer) {
        free(vfs->lfs2_file_conf.buffer);
    }
    if (vfs->file.lfs2_file) {
        free(vfs->file.lfs2_file);
    }
    free(vfs);

    return NULL;
}


int32_t vfs_stream_read(void *file_p, void *buf, uint32_t btr) {
    vfs_stream_t *vfs = file_p;
    int32_t br = 0;

    if (vfs->lfs2) {
        br = lfs2_file_read(vfs->lfs2, vfs->file.lfs2_file, (uint8_t *)buf, btr);
    } else if (vfs->fatfs) {
        FRESULT res = f_read(&vfs->file.fat_file, buf, btr, (UINT *)&br);
        if (res != FR_OK) {
            return -1;
        }
    }

    ESP_LOGD(TAG, "vfs_stream_read: %ld bytes read", br);

    return br;
}


ssize_t vfs_stream_write(void *file_p, const void *buf, size_t len) {
    vfs_stream_t *vfs = file_p;
    ssize_t out_sz = 0;

    if (vfs->lfs2) {
        out_sz = lfs2_file_write(vfs->lfs2, vfs->file.lfs2_file, buf, len);
        lfs2_file_sync(vfs->lfs2, vfs->file.lfs2_file);
    } else if (vfs->fatfs) {
        FRESULT res = f_write(&vfs->file.fat_file, buf, (UINT)len, (UINT *)&out_sz);
        if (res != FR_OK) {
            return -1;
        }
        f_sync(&vfs->file.fat_file);
    }
    return out_sz;
}


int32_t vfs_stream_seek(void *file_p, uint32_t pos, int whence) {
    vfs_stream_t *vfs = file_p;
    int32_t offset = 0;

    if (vfs->lfs2) {
        offset = lfs2_file_seek(vfs->lfs2, vfs->file.lfs2_file, pos, whence);
    } else if (vfs->fatfs) {
        FRESULT res = FR_INT_ERR;
        switch (whence) {
            case SEEK_SET:
                res = f_lseek(&vfs->file.fat_file, pos);
                break;
            case SEEK_CUR:
                res = f_lseek(&vfs->file.fat_file, f_tell((FIL *)&vfs->file.fat_file) + pos);
                break;
            case SEEK_END:
                res = f_lseek(&vfs->file.fat_file, f_size((FIL *)&vfs->file.fat_file) + pos);
                break;
            default:
                break;
        }
        if (res != FR_OK) {
            ESP_LOGE(TAG, "f_lseek failed %d", res);
            return -1;
        }
        offset = f_tell(&vfs->file.fat_file);
    }

    return offset;
}


int32_t vfs_stream_tell(void *file_p) {
    vfs_stream_t *vfs = file_p;
    int32_t offset = 0;

    if (vfs->lfs2) {
        offset = lfs2_file_tell(vfs->lfs2, vfs->file.lfs2_file);
    } else if (vfs->fatfs) {
        offset = f_tell((FIL *)&vfs->file.fat_file);
    }

    return offset;
}


void vfs_stream_close(void *file_p) {
    vfs_stream_t *vfs = file_p;

    if (vfs == NULL) {
        return;
    }

    if (vfs->lfs2) {
        lfs2_file_close(vfs->lfs2, vfs->file.lfs2_file);
        free(vfs->file.lfs2_file);
        free(vfs->lfs2_file_conf.buffer);
    } else if (vfs->fatfs) {
        f_close(&vfs->file.fat_file);
    }
}

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

#include "lvgl/lvgl.h"
#include "./../../cmodules/lv_binding_micropython/driver/include/common.h"
#include "string.h"

static const char *TAG = "lv_utils";

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


static void *lv_utils_fs_open_cb(lv_fs_drv_t *drv, const char *path, lv_fs_mode_t mode) {
    LV_UNUSED(drv);
    lv_fs_res_t res = LV_FS_RES_NOT_IMP;

    ESP_LOGI("lv_utils", "fs_open_cb: path=%s, mode=%d\n", path, mode);

    vfs_stream_t *vfs = lv_malloc(sizeof(vfs_stream_t));

    const char *path_out;
    mp_vfs_mount_t *existing_mount = mp_vfs_lookup_path(path, &path_out);
    if (existing_mount == MP_VFS_NONE || existing_mount == MP_VFS_ROOT) {
        ESP_LOGE(TAG, "No vfs mount");
        goto _vfs_init_exit;
    }
    if (strstr(path, "flash")) {
        ESP_LOGD(TAG, "in flash");
        vfs->lfs2 = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(existing_mount->obj))->lfs;
    } else if (strstr(path, "system")) {
        ESP_LOGD(TAG, "in system");
        vfs->lfs2 = &((mp_obj_vfs_lfs2_t *)MP_OBJ_TO_PTR(existing_mount->obj))->lfs;
    } else if (strstr(path, "sd")) {
        ESP_LOGD(TAG, "in sd");
        vfs->fatfs = &((fs_user_mount_t *)MP_OBJ_TO_PTR(existing_mount->obj))->fatfs;
    }

    if (vfs->lfs2) {
        vfs->lfs2_file_conf.buffer = lv_malloc(vfs->lfs2->cfg->cache_size * sizeof(uint8_t));
        vfs->file.lfs2_file = (lfs2_file_t *)lv_malloc(1 * sizeof(lfs2_file_t));
        int flags = 0;
        if (mode == LV_FS_MODE_WR) {
            flags = LFS2_O_WRONLY;
        } else if (mode == LV_FS_MODE_RD) {
            flags = LFS2_O_RDONLY;
        } else if (mode == (LV_FS_MODE_WR | LV_FS_MODE_RD)) {
            flags = LFS2_O_RDWR;
        }
        int res = lfs2_file_opencfg(vfs->lfs2, vfs->file.lfs2_file, path_out, flags, &vfs->lfs2_file_conf);
        if (res != LFS2_ERR_OK) {
            ESP_LOGE(TAG, "failed to open %s(%d)", path_out, res);
            goto _vfs_init_exit;
        }
    } else if (vfs->fatfs) {
        BYTE fmode = 0;
        if (mode == LV_FS_MODE_WR) {
            fmode = FA_WRITE;
        } else if (mode == LV_FS_MODE_RD) {
            fmode = FA_READ;
        } else if (mode == (LV_FS_MODE_WR | LV_FS_MODE_RD)) {
            fmode = FA_OPEN_ALWAYS;
        }
        FRESULT ret = f_open(vfs->fatfs, &vfs->file.fat_file, path_out, fmode);
        if (ret != FR_OK) {
            ESP_LOGE(TAG, "failed to open %s(%d)", path_out, ret);
            goto _vfs_init_exit;
        }
    }

    return vfs;
_vfs_init_exit:
    if (vfs->lfs2_file_conf.buffer) {
        lv_free(vfs->lfs2_file_conf.buffer);
    }
    if (vfs->file.lfs2_file) {
        lv_free(vfs->file.lfs2_file);
    }
    lv_free(vfs);

    return NULL;
}
DEFINE_PTR_OBJ(lv_utils_fs_open_cb);


static lv_fs_res_t lv_utils_fs_read_cb(lv_fs_drv_t *drv, void *file_p, void *buf, uint32_t btr, uint32_t *br) {
    LV_UNUSED(drv);
    vfs_stream_t *vfs = file_p;

    if (vfs->lfs2) {
        *br = lfs2_file_read(vfs->lfs2, vfs->file.lfs2_file, (uint8_t *)buf, btr);
        return (int32_t)(*br) < 0 ? LV_FS_RES_UNKNOWN : LV_FS_RES_OK;
    } else if (vfs->fatfs) {
        FRESULT res = f_read(&vfs->file.fat_file, buf, btr, (UINT *)br);
        return res == FR_OK ? LV_FS_RES_OK : LV_FS_RES_UNKNOWN;
    }

    return LV_FS_RES_UNKNOWN;
}
DEFINE_PTR_OBJ(lv_utils_fs_read_cb);


static lv_fs_res_t lv_utils_fs_write_cb(lv_fs_drv_t *drv, void *file_p, const void *buf, uint32_t btw, uint32_t *bw) {
    LV_UNUSED(drv);
    vfs_stream_t *vfs = file_p;

    if (vfs->lfs2) {
        *bw = lfs2_file_write(vfs->lfs2, vfs->file.lfs2_file, (uint8_t *)buf, btw);
        lfs2_file_sync(vfs->lfs2, vfs->file.lfs2_file);
    } else if (vfs->fatfs) {
        f_write(&vfs->file.fat_file, (uint8_t *)buf, btw, (UINT *)bw);
        f_sync(&vfs->file.fat_file);
    }
    return (int32_t)(*bw) < 0 ? LV_FS_RES_UNKNOWN : LV_FS_RES_OK;
}
DEFINE_PTR_OBJ(lv_utils_fs_write_cb);


static lv_fs_res_t lv_utils_fs_seek_cb(lv_fs_drv_t *drv, void *file_p, uint32_t pos, lv_fs_whence_t whence) {
    LV_UNUSED(drv);
    vfs_stream_t *vfs = file_p;

    if (vfs->lfs2) {
        int mode = 0;
        if (whence == LV_FS_SEEK_SET) {
            mode = LFS2_SEEK_SET;
        } else if (whence == LV_FS_SEEK_CUR) {
            mode = LFS2_SEEK_CUR;
        } else if (whence == LV_FS_SEEK_END) {
            mode = LFS2_SEEK_END;
        }

        int rc = lfs2_file_seek(vfs->lfs2, vfs->file.lfs2_file, pos, mode);
        return rc < 0 ? LV_FS_RES_UNKNOWN : LV_FS_RES_OK;
    } else if (vfs->fatfs) {
        FRESULT res = FR_INT_ERR;
        switch (whence) {
            case LV_FS_SEEK_SET:
                res = f_lseek(&vfs->file.fat_file, pos);
                break;
            case LV_FS_SEEK_CUR:
                res = f_lseek(&vfs->file.fat_file, f_tell((FIL *)&vfs->file.fat_file) + pos);
                break;
            case LV_FS_SEEK_END:
                res = f_lseek(&vfs->file.fat_file, f_size((FIL *)&vfs->file.fat_file) + pos);
                break;
            default:
                break;
        }
        return res == FR_OK ? LV_FS_RES_OK : LV_FS_RES_UNKNOWN;
    }

    return LV_FS_RES_UNKNOWN;
}
DEFINE_PTR_OBJ(lv_utils_fs_seek_cb);


static lv_fs_res_t lv_utils_fs_tell_cb(lv_fs_drv_t *drv, void *file_p, uint32_t *pos_p) {
    LV_UNUSED(drv);
    vfs_stream_t *vfs = file_p;

    if (vfs->lfs2) {
        *pos_p = lfs2_file_tell(vfs->lfs2, vfs->file.lfs2_file);
    } else if (vfs->fatfs) {
        *pos_p = f_tell((FIL *)&vfs->file.fat_file);
    }

    return (int32_t)(*pos_p) < 0 ? LV_FS_RES_UNKNOWN : LV_FS_RES_OK;
}
DEFINE_PTR_OBJ(lv_utils_fs_tell_cb);

static lv_fs_res_t lv_utils_fs_close_cb(lv_fs_drv_t *drv, void *file_p) {
    LV_UNUSED(drv);
    vfs_stream_t *vfs = file_p;

    if (vfs->lfs2) {
        lfs2_file_close(vfs->lfs2, vfs->file.lfs2_file);
        lv_free(vfs->file.lfs2_file);
        lv_free(vfs->lfs2_file_conf.buffer);
    } else if (vfs->fatfs) {
        f_close(&vfs->file.fat_file);
    }

    return LV_FS_RES_OK;
}
DEFINE_PTR_OBJ(lv_utils_fs_close_cb);


static const mp_rom_map_elem_t lv_utils_module_globals_table[] = {
    /* *FORMAT-OFF* */
    { MP_ROM_QSTR(MP_QSTR___name__),    MP_ROM_QSTR(MP_QSTR__lv_utils)             },
    { MP_ROM_QSTR(MP_QSTR_fs_open_cb),  MP_ROM_PTR(&PTR_OBJ(lv_utils_fs_open_cb))  },
    { MP_ROM_QSTR(MP_QSTR_fs_read_cb),  MP_ROM_PTR(&PTR_OBJ(lv_utils_fs_read_cb))  },
    { MP_ROM_QSTR(MP_QSTR_fs_write_cb), MP_ROM_PTR(&PTR_OBJ(lv_utils_fs_write_cb)) },
    { MP_ROM_QSTR(MP_QSTR_fs_seek_cb),  MP_ROM_PTR(&PTR_OBJ(lv_utils_fs_seek_cb))  },
    { MP_ROM_QSTR(MP_QSTR_fs_tell_cb),  MP_ROM_PTR(&PTR_OBJ(lv_utils_fs_tell_cb))  },
    { MP_ROM_QSTR(MP_QSTR_fs_close_cb), MP_ROM_PTR(&PTR_OBJ(lv_utils_fs_close_cb)) },
    /* *FORMAT-ON* */
};

static MP_DEFINE_CONST_DICT(lv_utils_module_globals, lv_utils_module_globals_table);

const mp_obj_module_t lv_utils_module = {
    .base = {&mp_type_module},
    .globals = (mp_obj_dict_t *)&lv_utils_module_globals,
};

MP_REGISTER_MODULE(MP_QSTR__lv_utils, lv_utils_module);

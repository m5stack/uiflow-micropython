#include <stdio.h>
#include <string.h>
#include <getopt.h>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include "littlefs/lfs2.h"
#include "littlefs/lfs2_util.h"

static struct lfs2_config cfg;
static lfs2_t lfs2;
static uint8_t *image;
static int verbose = 0;

/* input hex string, format: 0xAA111 or AA111 or abc11 */
int ahextoi(char *p) {
    int n = 0;
    char *q = p;

    /* reach its tail */
    while (*q) {
        q++;
    }

    if (*p == '0' && *(p + 1) != 0) { /* skip "0x" or "0X" */
        p += 2;
    }

    while (*p) {
        int c;
        if (*p >= '0' && *p <= '9') {
            c = *p - '0';
        } else if (*p >= 'A' && *p <= 'F') {
            c = *p - 'A' + 0xA;
        } else if (*p >= 'a' && *p <= 'f') {
            c = *p - 'a' + 0xA;
        } else {
            /* invalid char */
            return 0;
        }

        n += c << ((int)(q - p - 1) * 4);
        p++;
    }
    return n;
}

static int lfs2_read(const struct lfs2_config *c, lfs2_block_t block,
    lfs2_off_t off, void *buffer, lfs2_size_t size) {
    memcpy(buffer, image + (block * c->block_size) + off, size);
    return 0;
}

static int lfs2_prog(const struct lfs2_config *c, lfs2_block_t block,
    lfs2_off_t off, const void *buffer, lfs2_size_t size) {
    memcpy(image + (block * c->block_size) + off, buffer, size);
    return 0;
}

static int lfs2_erase(const struct lfs2_config *c, lfs2_block_t block) {
    memset(image + (block * c->block_size), 0, c->block_size);
    return 0;
}

static int lfs2_sync(const struct lfs2_config *c) {
    return 0;
}

static void image_initialize(uint32_t fs_size) {
    cfg.read = lfs2_read;
    cfg.prog = lfs2_prog;
    cfg.erase = lfs2_erase;
    cfg.sync = lfs2_sync;

    cfg.block_size = 4096U;
    cfg.read_size = 128U;
    cfg.prog_size = 128U;
    cfg.block_count = fs_size / cfg.block_size;
    cfg.lookahead_size = 256;
    cfg.cache_size = 4 * 128;
    cfg.block_cycles = 100;

    image = (uint8_t *)calloc(sizeof(uint8_t), fs_size);
    memset(image, 0xff, fs_size);
    lfs2_format(&lfs2, &cfg);
}

int cpt_scan_files(const char *basePath, char (*file_path)[257],
    uint16_t *file_count) {
    DIR *dir;
    struct dirent *ptr;

    if ((dir = opendir(basePath)) == NULL) {
        printf("[ Cpt Scan ] Open dir '%s' failed... \r\n", basePath);
        exit(1);
    }

    while ((ptr = readdir(dir)) != NULL) {
        if (strcmp(ptr->d_name, ".") == 0 ||
            strcmp(ptr->d_name, "..") == 0) { /// current dir OR parrent dir
            continue;
        } else if (ptr->d_type == 8) { /// file
            sprintf(&file_path[*file_count][0], "%s/%s", basePath, ptr->d_name);
            *file_count += 1;
            if (*file_count == 255) {
                printf("[ Cpt Scan ] File count than %d, failed \r\n", 255);
            }
        } else if (ptr->d_type == 4) {
            char path_new[300] = {0x00};
            sprintf(path_new, "%s/%s", basePath, ptr->d_name);
            sprintf(&file_path[*file_count][0], "%s/.", path_new);
            *file_count += 1;
            cpt_scan_files(path_new, file_path, file_count);
        }
    }

    closedir(dir);
    return 1;
}

int16_t write_file(lfs2_t *fs, const char *path, const char *data,
    uint32_t len) {
    int16_t res;

    lfs2_file_t dstf;
    lfs2_dir_t lfs_dir;

    char *split_ptr = NULL;
    uint16_t split_pos = 0;
    char path_dir[256] = {0x00};
    sprintf(path_dir, "%s", path);

    for (;;) {
        split_ptr = strchr(&path_dir[split_pos + 1], '/');
        if (split_ptr == NULL) {
            break;
        }
        split_pos = split_ptr - path_dir;
        *split_ptr = '\0';

        if (lfs2_dir_open(fs, &lfs_dir, path_dir) != LFS2_ERR_OK) {
            res = lfs2_mkdir(fs, path_dir);
            if (res != LFS2_ERR_OK) {
                return res;
            }
        } else {
            lfs2_dir_close(fs, &lfs_dir);
        }
        *split_ptr = '/';
    }
    if (path[strlen(path) - 1] == '.') {
        return LFS2_ERR_OK;
    }
    lfs2_file_open(&lfs2, &dstf, path, LFS2_O_WRONLY | LFS2_O_CREAT);
    if (lfs2_file_write(&lfs2, &dstf, data, len) != len) {
        printf("[ LFS2 Pack ] File(%s) write error\r\n", path);
        return LFS2_ERR_NOMEM;
    }
    lfs2_file_close(&lfs2, &dstf);
    return LFS2_ERR_OK;
}

void save_fs_image(const char *path, const uint32_t image_size) {
    FILE *fp = NULL;
    char file_path[200];
    fp = fopen(path, "w+");
    if (fp == NULL) {
        printf("[ FS Image ] Save path '%s' failed \r\n", path);
        exit(1);
    }
    fwrite(image, sizeof(uint8_t), image_size, fp);
    fclose(fp);
}

int create_fs_image(const char *path, const uint32_t size,
    const char *image_path) {
    int32_t file_size = 0;
    int64_t total_size = 0;
    uint8_t *read_buff;
    FILE *ff;

    if (size % 4096) {
        printf("[ LFS2 Pack ] image size must multiple sector size\r\n");
        exit(1);
    }

    image_initialize(size);

    if (lfs2_mount(&lfs2, &cfg) != LFS2_ERR_OK) {
        printf("[ LFS2 Pack ] file system mount failed\r\n");
        exit(1);
    }

    char file_path[255][257];
    int16_t file_count = 0;
    cpt_scan_files(path, file_path, &file_count);

    for (size_t i = 0; i < file_count; i++) {
        if (file_path[i][strlen(file_path[i]) - 1] == '.') {
            if (write_file(&lfs2, &file_path[i][strlen(path) + 1], read_buff,
                file_size) != LFS2_ERR_OK) {
                printf("[ LFS2 Pack ] file too large, pack failed \r\n");
                exit(1);
            }
            continue;
        }

        ff = fopen(&file_path[i][0], "r");
        fseek(ff, 0, SEEK_END);
        file_size = ftell(ff);
        rewind(ff);
        read_buff = (uint8_t *)calloc(file_size, sizeof(uint8_t));
        if (fread(read_buff, sizeof(uint8_t), file_size, ff) != file_size) {
            printf("[ LFS2 Pack ] file '%s' read failed\r\n", &file_path[i][0]);
            exit(1);
        }
        if (write_file(&lfs2, &file_path[i][strlen(path) + 1], read_buff,
            file_size) != LFS2_ERR_OK) {
            printf("[ LFS2 Pack ] file too large, pack failed \r\n");
            exit(1);
        }
        total_size += file_size;
        if (verbose) {
            printf("[ LFS2 Pack ] Add -> %s\r\n", &file_path[i][strlen(path) + 1]);
        }
        free(read_buff);
    }
    lfs2_unmount(&lfs2);
    save_fs_image(image_path, size);

    printf("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\r\n");
    printf("[ LFS2 Pack ] vfs size: 0x%x bytes\r\n", size);
    printf("[ LFS2 Pack ] vfs used: 0x%06lx bytes  %f%%\r\n", total_size, (double)((double)total_size / (double)size) * 100.0);
    printf("[ LFS2 Pack ] save path: %s\r\n", image_path);
    printf("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n");
}

uint8_t is_int_string(char *str) {
    for (uint16_t i = 0; i < strlen(str); i++) {
        if (str[i] < '0' || str[i] > '9') {
            return 0;
        }
    }
    return 1;
}

int main(int argc, char *argv[]) {
    static int lopt = -1;
    static const struct option param_option[] = {
        {"create", no_argument, &lopt, 0},
        {"unpack", no_argument, &lopt, 1},
        {"verbose", no_argument, &verbose, 0},
        {"input", required_argument, NULL, 'i'},
        {"size", required_argument, NULL, 's'},
        {"output", required_argument, NULL, 'o'},
    };

    static int opt = 0;
    static uint32_t size = 0;
    static char *input = NULL;
    static char *output = NULL;

    while ((opt = getopt_long(argc, argv, "cuvi:s:o:", param_option, NULL)) !=
           -1) {
        switch (opt) {
            case 'i':
                input = optarg;
                // printf("input: %s\r\n", input);
                break;
            case 's':
                size = ahextoi(optarg);
                // printf("size: %d\r\n", size);
                break;
            case 'o':
                output = optarg;
                // printf("output: %s\r\n", output);
                break;
            case 'c':
                lopt = 0;
                break;
            case 'u':
                lopt = 1;
                break;
            case 'v':
                verbose = 1;
                break;
        }
    }

    if (lopt == 0) {
        assert(size != 0);
        assert(input != NULL);
        assert(output != NULL);
        create_fs_image(input, size, output);
    } else if (lopt == 1) {
        assert(input != NULL);
        assert(output != NULL);
        if (input != NULL && output != NULL) {
        }
    }

    return 0;
}

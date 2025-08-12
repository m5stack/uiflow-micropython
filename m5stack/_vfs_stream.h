/*
 * SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
 *
 * SPDX-License-Identifier: MIT
 */

#ifndef _VFS_STREAM_H_
#define _VFS_STREAM_H_

#include <stdint.h>
#include <unistd.h>

#ifndef SEEK_SET
#define SEEK_SET    0    /* seek relative to beginning of file */
#endif

#ifndef SEEK_CUR
#define SEEK_CUR    1    /* seek relative to current file position */
#endif

#ifndef SEEK_END
#define SEEK_END    2    /* seek relative to end of file */
#endif

#define VFS_READ 0x01
#define VFS_WRITE 0x02
#define VFS_APPEND 0x04
#define VFS_CREATE 0x08

void *vfs_stream_open(const char *path, int flags);
int32_t vfs_stream_read(void *file_p, void *buf, uint32_t btr);
ssize_t vfs_stream_write(void *file_p, const void *buf, size_t len);
int32_t vfs_stream_seek(void *file_p, uint32_t pos, int whence);
int32_t vfs_stream_tell(void *file_p);
void vfs_stream_close(void *file_p);

#endif

# Resource Files and Paths

## User Resources

UiFlow2 normally starts user programs with `os.getcwd() == "/flash"`.
In that working directory, `res/img/photo.jpg` and
`/flash/res/img/photo.jpg` identify the same file. `res/` is a relative
directory name, not a separate read-only partition. Changing the working
directory changes the meaning of a relative path; absolute paths avoid this.
Paths and filenames are case-sensitive.

| Path | Purpose |
| --- | --- |
| `/flash/res/img` | User images uploaded to this device. |
| `/flash/res/font` | User font files; supported formats depend on the rendering API. |
| `/flash/res/audio` | User audio files. Create this directory before recording or uploading. |
| `/system` | Firmware-supplied files on boards with a separate system partition. |
| `/sd` | SD storage, available only after a supported card has been mounted. |

Store application files under `/flash`. The `/system` directory contains
firmware-managed resources. Some small-flash builds package these resources
under `/flash/res` instead.

Fresh filesystem setup creates `res`, `res/img` and `res/font`;
it does not create every application subdirectory. Neither `open()` nor
recording creates missing parent directories. Prepare directories first:

```python
import os
import errno

for directory in ("/flash/res", "/flash/res/audio"):
    try:
        os.mkdir(directory)
    except OSError as exc:
        if exc.args[0] != errno.EEXIST:
            raise
        if not os.stat(directory)[0] & 0x4000:
            raise
```
## Uploading Files

**USB / WebTerminal:** Connect the selected device, stop the running program
with Ctrl+C, and open the WebTerminal file manager (`File`). Enter the
destination directory, such as `/flash/res/img`, then use
`Send File to Here` to upload the local file. Check the destination listing
and exact filename before running the program. See
[USB Mode](usb-mode.md). A file transferred this way is stored on that
device; it is not automatically saved in the cloud project or copied to
another device.

**Wi-Fi / cloud project:** Connect an online device in UiFlow2 Web IDE and
upload the resource through the project's file manager. Select that project
resource in the UI editor. When running/downloading the project, wait for
resource synchronization to finish, then check the file on the device.
Uploading directly through the *device* file manager is distinct from adding
a resource to the *cloud project*. Running a project does not upload existing
device files back to the cloud. Consult the
[UiFlow2 file manager guide](https://docs.m5stack.com/en/uiflow2/projects/file_manager)
for the current IDE workflow.

The firmware resource synchronizer reads `/flash/res/res.json` and downloads
the listed `devicePath` files; copying a Python script alone does not
provide its images, fonts or audio. Keep your own recordings separate from
project-managed resource files, which a later project sync may replace or
remove. Create any custom parent directories before downloading into them.

**Custom firmware images:** Repository developers can place user assets in
`m5stack/fs/user/res` or a board's `files/user/res` before building its
filesystem. `make -C m5stack BOARD=<board> fs` produces filesystem images;
`pack_all` includes the user filesystem while `pack` normally excludes it.
Small-flash builds use a different layout. A Python frozen-manifest entry
does not upload a JPG or WAV to the device. Flashing a user filesystem image
replaces user data; use the file manager for ordinary resource updates.

## Passing a Path to an API

- `open()`, `M5.Lcd.drawJpgFile()`, `M5.Widgets.Image()` and
  `M5.Speaker.playWavFile()` use filesystem paths. Prefer absolute paths.
- `m5ui.M5Image(path=...)` and `set_image(path)` take a plain absolute
  path, such as `/flash/res/img/photo.jpg` or `/sd/photo.png`. M5UI adds
  the LVGL `S:` driver prefix internally; do not add it yourself.
- A bare `lv.image.set_src()` using the registered filesystem driver uses
  `S:/flash/res/img/photo.jpg`. This LVGL prefix is not part of an
  `open()` path and does not belong in `M5Image`'s `path` argument.
- The ADF `audio.Player` / `audio.Recorder` API uses URI strings such as
  `file://flash/res/audio/test.wav`. This URI is not interchangeable with
  the VFS path `/flash/res/audio/test.wav`. Check board support before
  selecting the ADF API; see [Board Capabilities](board-capabilities.md).

Upload the referenced resources before running an example. To inspect a file:

```python
import os

path = "/flash/res/img/photo.jpg"
try:
    print("cwd:", os.getcwd())
    print("file bytes:", os.stat(path)[6])
    with open(path, "rb") as resource:
        print("header:", resource.read(16))
except OSError as exc:
    print("Resource unavailable:", path, exc)
```
## Missing Files and Other Failures

- Python `open()` / `os.stat()` normally raise `OSError(ENOENT)` for a
  missing file or parent directory. Check spelling, letter case, cwd,
  destination directory and upload/sync completion.
- A failed image decode may produce an empty image (including size 0 x 0)
  without a Python exception. Verify file existence, nonzero size, format
  and the API's return value or resulting image dimensions.
- `OSError(EROFS)` indicates an actual read-only mount/media condition;
  removing `/flash` from a path does not change filesystem permissions.
- `ENOSPC` means storage is full. `gc.collect()` frees RAM, not flash.
  Check `os.statvfs("/flash")` and remove only files you no longer need.

## SD Card Paths

Initialize and mount the card with the target board/base's documented pins
before accessing `/sd`; see the
[Atomic TFCard Base](../base/tfcard.md) example. Use absolute paths such
as `/sd/photo.png` or `/sd/recording.wav` for files stored on the card.

# UiFlow2 MicroPython 开发说明

## 准备环境

固件工程位于 `m5stack/`，板卡配置位于 `m5stack/boards/<BOARD>/`。
编译需要 ESP-IDF 5.5.x、Python、Git 子模块和 LittleFS 工具。
先进入已安装的 ESP-IDF 环境，再准备依赖：

```sh
source /path/to/esp-idf/export.sh
cd uiflow_micropython/m5stack
make submodules
make patch
make littlefs
make mpy-cross
```

## 编译与烧录

`BOARD` 使用 Makefile 定义的板卡名，例如 `M5STACK_Basic`。
`build` 编译应用、bootloader 和分区表；`pack_all` 还打包系统及用户文件系统，
生成 `build-<BOARD>/uiflow-<git-sha>.bin`。

```sh
make BOARD=M5STACK_Basic build
make BOARD=M5STACK_Basic pack_all
make BOARD=M5STACK_Basic pack_all flash_all PORT=/dev/ttyACM0 BAUD=1500000
```

按实际设备替换板卡名和串口；Windows 可使用 `PORT=COM343`。
`flash_all` 将完整镜像写入设备。`flash` 使用不包含用户文件系统的 `pack` 目标。
仅更新应用分区前，应确认现有分区表和系统资源与新应用匹配。

## 修改与提交

1. 从目标基线创建功能分支，记录 `git status` 和 `git submodule status`。
2. 修改后运行对应模块的检查。通用显示和 REPL 回归命令为：

   ```sh
   python3 tests/runtime/test_repl_paste_echo.py --sanitize
   python3 tests/lvgl/test_configure.py
   python3 tests/m5ui/test_draw_buffers.py
   ```

3. 执行 `git diff --check`，确认未加入构建产物或无关子模块修改。
4. 在目标板卡上确认启动、网络、资源挂载和相关功能。
5. 使用 `git commit -s`，通过仓库提交钩子后推送功能分支。

出现系统资源缺失或 `No vfs mount` 时，核对分区表、系统文件系统和用户文件系统，
必要时重新执行匹配板卡的完整打包与烧录。

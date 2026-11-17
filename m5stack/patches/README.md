# 补丁编号说明

- 0000 - 0999 这个范围的补丁 id, 用于分配给 micropython 相关的补丁。
- 1000 - 1999 这个范围的补丁 id, 用于分配给 esp-idf 相关的补丁。
- 2000 - 2999 这个范围的补丁 id, 用于分配给 M5Unified 相关的补丁。
- 3000 - 3999 这个范围的补丁 id, 用于分配给 esp-adf 相关的补丁。
- 4000 - 4999 这个范围的补丁 id, 用于分配给 M5GFX 相关的补丁。
- 5000 - 5999 这个范围的补丁 id, 用于分配给 esp32-camera 相关的补丁。
- 6000 - 6999 这个范围的补丁 id, 用于分配给 lv_binding_micropython 相关的补丁。

## MicroPython 1.27.0 的 REPL 与内存补丁

以下补丁以仓库固定的 MicroPython v1.27.0 子模块为基线。
应用顺序由 [Makefile](../Makefile) 的 `MICROPYTHON_PATCH_SERIES` 定义；编号用于识别，不应自行按文件名重排、跳过已有补丁或对同一工作区重复应用。
使用仓库现有的 prepare/quilt 流程维护补丁状态。已有补丁栈新增补丁时，应先检查当前已应用列表与 series，避免重复导入或同时使用其他方式再次修改同一段源码。

| 补丁 | 作用 |
| --- | --- |
| [0033-release-repl-source](0033-micropython-1.27.0-release-repl-source.patch) | 在 friendly REPL 等待下一条命令前释放旧输入存储，避免旧粘贴缓冲的容量继续占住附加 GC 区域。 |
| [0034-bound-split-heap-growth](0034-micropython-1.27.0-bound-split-heap-growth.patch) | 对无 PSRAM 配置的 split heap 推测增长设置可由板级覆盖的上限，较大的单次申请仍按实际需求处理。 |
| [0035-silent-internal-paste](0035-micropython-1.27.0-silent-internal-paste.patch) | 提供可由端口覆盖的静默粘贴判断，普通粘贴保持默认交互。 |
| [0040-native-internal-paste](0040-micropython-1.27.0-native-internal-paste.patch) | 在 friendly REPL 边界为端口识别的完整命令提供原生执行入口，避免额外 Python 包装函数在原生操作期间持有 GC 引用。 |
| [0041-detect-heap-memory](0041-micropython-1.27.0-detect-heap-memory.patch) | 在共用 ESP32 端口按实际可用 PSRAM 选择初始堆与增长策略，覆盖所有板型及编译启用但实际没有 PSRAM 的情况。 |

0040 针对当前补丁栈中的 `shared/runtime/pyexec.c` 和 `pyexec.h` 制作，应在 series 中已有的 0033、0035 等补丁之后应用；当前 series 将其放在 0036 之后。
更新 MicroPython 基线或重排相关补丁时，需要重新检查上下文、源码缓冲所有权和 REPL 异常处理，并构建验证，不能只以补丁文本能套用作为兼容依据。

### 0040 原生粘贴接口

`pyexec_friendly_repl_native_paste(source, len, fun, arg)` 是可由端口覆盖的弱函数，默认返回 `false`。
未被端口识别的输入继续使用普通 friendly paste 的解析、编译和执行流程；raw REPL 路径不由该 hook 接管。

端口在识别完整输入后返回原生回调及整数参数。识别阶段不能依赖输入缓冲在后续执行时仍然存在，也不应保留其中的指针。
REPL 在调用原生回调前清空并释放输入缓冲，然后通过原生执行器运行回调；只有端口明确识别的输入会选择此流程。

原生执行器沿用 REPL 的中断开关、待处理异常和回调处理、异常输出、`SystemExit`/强制退出、可选 VM abort 及板级执行前后 hook。
这样原生入口可以避免额外 Python 包装层，同时保持普通输入和软复位所需的退出语义。
修改此补丁后应验证普通 friendly paste、raw-paste、Ctrl-C、异常退出以及软复位后的后续执行。

### 0041 全设备堆能力检测

该补丁位于 0040 之后，建立在 0034 的有界增长接口上。默认策略按已经初始化的、可按字节寻址的 PSRAM 容量选择，不把 `CONFIG_SPIRAM` 当作实际容量。
没有可用 PSRAM 时，初始堆默认为 36 KiB，推测增长上限为 2 KiB；有可用 PSRAM 时保留原有初始堆和正常增长方式。显式板级配置优先，较大单次申请仍按实际需求处理。
BASIC 的专用增长宏已移除，所有使用该端口的板型共用判断。可使用 `python3 tools/tests/test_heap_memory_policy.py -v` 验证芯片、配置开关、实际容量及板级覆盖组合；需要先应用完整补丁栈。

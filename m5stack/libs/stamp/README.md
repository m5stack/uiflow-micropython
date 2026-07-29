# StampUWB API

`StampUWB` 是 Stamp 主机使用 QM33120/DW3720 UWB 芯片的板级包装类。它根据当前
Stamp 型号选择引脚并创建底层 `uwb.UWB` 对象，适合在 Python 中实现 DS-TWR 等测距协议。

当前在 `M5StampS3Mini`、`M5StampC6` 和 `M5StampC5` 固件中启用。驱动使用全局单设备模型，
同一时间只能创建一个活动实例。

## 更新日志

| 更新日期 | 更新人 | 更新说明 | 状态 |
| --- | --- | --- | --- |
| 2026.07.21 | luoweiyuan | 初稿 | 未发布 |

## 模块引用

```python
import uwb
from stamp import StampUWB, StampUWBAngle
```

`StampUWB` 提供板级引脚选择和底层 API 转发。PHY、收发模式和状态常量由 `uwb` 模块提供。

## 支持硬件与引脚

StampS3Mini 默认映射如下：

| StampS3Mini | QM33120/DW3720 | 用途 |
| --- | --- | --- |
| G21 | IRQ | 中断输入 |
| G39 | WAKEUP | 唤醒 |
| G40 | RESET | 复位 |
| G42 | MOSI | SPI MOSI |
| G41 | MISO | SPI MISO |
| G44 | CLK | SPI 时钟 |
| G43 | CS | SPI片选 |
| G38 | GP7/SYNC | 当前 DS-TWR 不使用 |
| 3V3 | 3V3 | 电源 |
| GND | GND | 地 |

StampC6 默认映射如下：

| StampC6 | QM33120/DW3720 | 用途 |
| --- | --- | --- |
| G0 | IRQ | 中断输入 |
| G18 | WAKE/BUSY | 唤醒 |
| G19 | RESET | 复位 |
| G21 | SPI_MOSI | SPI MOSI |
| G20 | SPI_MISO | SPI MISO |
| G23 | SPI_CLK | SPI 时钟 |
| G22 | SPI_CS | SPI片选 |
| G8 | GPIO/SW | 当前 DS-TWR 不使用的 GP7/SYNC |

StampC5 默认映射如下：

| StampC5 | QM33120/DW3720 | 用途 |
| --- | --- | --- |
| G0 | IRQ | 中断输入 |
| G24 | WAKE/BUSY | 唤醒 |
| G25 | RESET | 复位 |
| G27 | SPI_MOSI | SPI MOSI |
| G26 | SPI_MISO | SPI MISO |
| G12 | SPI_CLK | SPI 时钟 |
| G11 | SPI_CS | SPI片选 |
| G23 | GPIO/SW | 当前 DS-TWR 不使用的 GP7/SYNC |

初始化底层 SPI 前会复位 UART0，并释放实际传入的 SPI GPIO。StampS3Mini 固件使用 USB CDC
作为 REPL。

## 初始化

推荐直接使用当前板型的默认引脚：

```python
from stamp import StampUWB

radio = StampUWB()
```

也可以按关键字覆盖底层使用的七个引脚：

```python
radio = StampUWB(
    irq=21,
    wakeup=39,
    reset=40,
    mosi=42,
    miso=41,
    clock=44,
    cs=43,
)
```

| 参数 | 类型 | StampS3Mini 默认值 | 含义 |
| --- | --- | --- | --- |
| `irq` | `int` | `21` | QM33120 IRQ 输出连接的主机 GPIO；当前状态等待采用 SPI 轮询，但仍保留 IRQ 硬件连接 |
| `wakeup` | `int` | `39` | 主机输出到 QM33120 WAKEUP 的 GPIO，用于从低功耗状态唤醒芯片 |
| `reset` | `int` | `40` | 主机连接 QM33120 RESET 的 GPIO；构造和 `reset()` 时使用 |
| `mosi` | `int` | `42` | 主机发送、QM33120 接收的 SPI 数据线 |
| `miso` | `int` | `41` | QM33120 发送、主机接收的 SPI 数据线 |
| `clock` | `int` | `44` | SPI 时钟线 |
| `cs` | `int` | `43` | SPI 片选线，低电平选中 QM33120 |

包装层不限制引脚编号范围。不同 Stamp 主机应在 `iomap` 中提供各自的默认映射；调用者显式
传入的引脚值会原样交给对应主机的底层端口驱动检查。

`SYNC`（StampS3Mini G38、StampC6 G8、StampC5 G23）仅记录在板级 `iomap` 中，当前不会传给
底层驱动。

构造函数会依次初始化 SPI、硬件复位、探测设备并执行驱动初始化。正常的 QM33120/DW3720
设备 ID 为 `0xDECA0314`：

```python
print("0x%08x" % radio.device_id())
```

## DS-TWR 基础配置

以下配置与 StampS3Mini UWB 测距示例一致：

```python
import uwb
from stamp import StampUWB

radio = StampUWB()
radio.configure(
    preamble_length=128,
    pac=8,
    tx_code=9,
    rx_code=9,
    sfd_type=uwb.SFD_DW_8,
    data_rate=uwb.BR_6M8,
    phr_mode=uwb.PHR_STD,
    phr_rate=uwb.PHR_RATE_STD,
    sfd_timeout=129,
)
radio.configure_tx_rf(
    pg_delay=0x34,
    tx_power=0xFEFEFEFE,
    pg_count=0,
)
radio.set_antenna_delay(tx=16385, rx=16385)
radio.set_lna_pa(lna=True, pa=True)
```

## 配置 API

### `configure(...)`

配置 UWB PHY。`StampUWB` 固定使用 CH9，因此 `configure()` 不提供 `channel` 参数。其余参数
均有默认值。下面明确列出当前 DS-TWR 验证配置：

```python
radio.configure(
    preamble_length=128,
    pac=8,
    tx_code=9,
    rx_code=9,
    sfd_type=uwb.SFD_DW_8,
    data_rate=uwb.BR_6M8,
    phr_mode=uwb.PHR_STD,
    phr_rate=uwb.PHR_RATE_STD,
    sfd_timeout=129,
)
```

Tag 的 TX 参数必须能被 Anchor 的 RX 参数识别，反向发送同理；当前示例在两端使用完全
相同的 PHY 配置。

| 参数 | 默认值 | 合法范围 | 含义和影响 | 对端要求 |
| --- | --- | --- | --- | --- |
| `preamble_length` | `128` | `32`, `64`, `72`, `128`, `256`, `512`, `1024`, `1536`, `2048`, `4096` | PHY preamble 的 symbol 数。更长通常更易检测、覆盖更远，但占空时间和耗电更高 | TX/RX 配置应匹配 |
| `pac` | `8` | `4`, `8`, `16`, `32` | Preamble Acquisition Chunk，每次相关检测使用的 preamble symbol 数；PLEN 128 通常配 PAC8 | RX 参数，双方建议相同 |
| `tx_code` | `9` | `9`-`12` | CH9 发送 preamble code | 必须匹配对端 `rx_code` |
| `rx_code` | `9` | `9`-`12` | CH9 接收时搜索的 preamble code | 必须匹配对端 `tx_code` |
| `sfd_type` | `uwb.SFD_DW_8` | 当前只支持默认值 | Start Frame Delimiter 类型；使用 Decawave 8-symbol SFD | 必须相同 |
| `data_rate` | `uwb.BR_6M8` | 当前只支持默认值 | PHY payload data rate，当前为 6.8 Mbps | 必须相同 |
| `phr_mode` | `uwb.PHR_STD` | 当前只支持默认值 | 标准 PHY Header；最大为 125-byte payload 加 2-byte FCS | 必须相同 |
| `phr_rate` | `uwb.PHR_RATE_STD` | 当前只支持默认值 | PHY Header 的标准传输速率模式 | 必须相同 |
| `sfd_timeout` | `129` | `0`-`65535` symbols | RX 搜索 preamble/SFD 的 timeout；默认值按 `128 + 1 + 8 - 8` 计算 | 本机 RX 参数，需覆盖对端前导码 |
`StampUWB` 内部固定关闭 STS 并使用 PDoA mode 0。可选的 `preamble_length` 为 `32`, `64`,
`72`, `128`, `256`, `512`, `1024`, `1536`, `2048`, `4096`；`pac` 为 `4`, `8`, `16`,
`32`。

配置失败时抛出 `OSError("UWB configure failed")`。非法 preamble、PAC、preamble code 或
SFD timeout 抛出 `ValueError`。

### `configure_tx_rf(pg_delay, tx_power, pg_count)`

配置 TX RF 参数。

| 参数 | 默认值 | 合法范围 | 含义和影响 |
| --- | --- | --- | --- |
| `pg_delay` | `0x34` | `0x00`-`0xFF` | Pulse Generator delay，用于调整 TX pulse spectrum；该值与 channel 和射频硬件有关 |
| `tx_power` | `0xFEFEFEFE` | `0x00000000`-`0xFFFFFFFF` | 32-bit TX power register 配置。四个 byte 控制不同发送条件下的功率设置；更高值不代表可以忽略当地 UWB 发射法规 |
| `pg_count` | `0` | `0x00`-`0xFF` | Pulse Generator calibration 参数；当前 QM33120/DW3720 板卡使用已验证值 `0` |

这三个参数只配置本机发射链路，不需要与对端数值相同。修改它们会影响发射功率、频谱、
接收距离和法规符合性；没有重新进行射频验证时应保持示例值。

### `set_antenna_delay(tx, rx)`

设置本机 TX/RX antenna delay，单位为 DW device time unit。它补偿芯片时间戳参考点到
天线实际发射/接收点之间的固定延迟，直接影响最终距离偏移。示例默认 TX 和 RX 均为
`16385`，量产或高精度应用应逐台标定；对端不要求使用相同数值。

### `set_lna_pa(*, lna=True, pa=True)`

启用或关闭接收 Low Noise Amplifier 和发送 Power Amplifier 控制。QM33120 模块需要使用
LNA/PA 时保持两者为 `True`；该配置只影响本机射频前端。

### `set_rx_after_tx_delay(delay_uus)`

设置发送完成到自动开启接收之间的延迟，单位为 UWB microsecond（uus）。用于跳过对端尚未
可能响应的时间，减少无效 RX 时间；设置过大可能错过对端响应。当前 Python 示例使用 `0`，
发送后立即接收。

### `set_rx_timeout(timeout_uus)`

设置 RX frame timeout，单位为 uus，从 RX 开启后开始计时。值为 `0` 时禁用 frame timeout。
它应大于对端 turnaround time、空中传输时间和 Python 调度余量；过短会产生
`uwb.STATUS_RX_TIMEOUT`，过长会降低错误恢复速度。示例使用 `30000` uus。

### `set_preamble_timeout(timeout)`

设置 preamble detection timeout，单位为 PAC。接收器在指定数量的 PAC 内找不到 preamble
便退出接收；值为 `0` 时禁用。它与 `sfd_timeout` 不同：前者限制 preamble 检测阶段，后者
限制 preamble/SFD 搜索过程。当前示例使用 `0`。

## 帧收发 API

### `write_tx_frame(data, *, ranging=True)`

把 `bytes`、`bytearray` 或其他 buffer 对象写入 TX buffer。Python payload 最大为 125 bytes；
驱动自动把 2-byte FCS 长度加入 TX frame control，调用者不应在 `data` 末尾追加 FCS。

### `set_delayed_trx_time(device_time)`

设置 delayed TX/RX 时间。参数格式与 Decawave `dwt_setdelayedtrxtime()` 一致，即 40-bit
设备时间右移 8 位后的值：

```python
delayed_time = (radio.rx_timestamp() + delay_uus * 63898) >> 8
radio.set_delayed_trx_time(delayed_time)
```

### `start_tx(mode)`

启动发送。模式可用按位或组合：

```python
radio.start_tx(uwb.TX_IMMEDIATE)
radio.start_tx(uwb.TX_IMMEDIATE | uwb.RESPONSE_EXPECTED)
radio.start_tx(uwb.TX_DELAYED)
```

delayed TX 时间已经过去时抛出 `OSError("UWB delayed TX is too late")`。

### `rx_enable(mode)`

启动接收，使用 `uwb.RX_IMMEDIATE` 或 `uwb.RX_DELAYED`。启动失败时抛出 `OSError`。

### `frame_length()`

返回最近接收帧的硬件长度，包含 2-byte FCS。

### `read_rx_frame()`

读取最近接收的 frame，返回已经移除 2-byte FCS 的 `bytes`。无效帧长度抛出 `OSError`。

## 状态 API

### `wait_status(mask, timeout_ms=-1)`

轮询并返回第一个命中 `mask` 的原始状态值。`timeout_ms` 单位为毫秒；默认 `-1` 表示一直
等待。等待期间会运行 MicroPython event poll hook，因此支持 `KeyboardInterrupt`。

```python
status = radio.wait_status(uwb.STATUS_RX_ALL, 50)
if status & uwb.STATUS_RX_GOOD:
    frame = radio.read_rx_frame()
elif status & uwb.STATUS_RX_TIMEOUT:
    print("RX timeout")
elif status & uwb.STATUS_RX_ERROR:
    print("RX error")
```

软件等待超时抛出 `OSError(ETIMEDOUT)`。硬件 RX timeout 或 RX error 会作为状态位返回，
不会自动抛出异常。

### `read_status()`

返回当前低 32-bit 系统状态寄存器。

### `clear_status(mask)`

清除指定状态位。通常在处理完 TX/RX 事件后调用。

### `force_trx_off()`

立即关闭当前 TX/RX 操作。发生 timeout、错误帧或准备下一轮测距时可用于恢复到空闲状态。

## 时间戳 API

| 方法 | 返回值 |
| --- | --- |
| `tx_timestamp()` | 最近一次发送的完整 40-bit TX 时间戳 |
| `rx_timestamp()` | 最近一次接收的完整 40-bit RX 时间戳 |
| `system_timestamp()` | 当前完整 40-bit 系统时间戳 |

时间戳为 QM33120/DW3720 device time unit，不是微秒或毫秒。示例使用：

```python
UUS_TO_DWT_TIME = 63898
DWT_TIME_UNITS = 1.0 / (499.2e6 * 128.0)
```

40-bit 时间戳会回绕。DS-TWR frame 中使用低 32 位时，应使用无符号 32-bit 差值：

```python
def u32_delta(later, earlier):
    return (later - earlier) & 0xFFFFFFFF
```

## 设备生命周期 API

| 方法 | 说明 |
| --- | --- |
| `device_id()` | 返回设备 ID，QM33120/DW3720 预期为 `0xDECA0314` |
| `reset()` | 关闭 TRX，硬件复位并重新 probe/initialise |
| `wakeup()` | 通过 WAKEUP 引脚唤醒设备 |
| `deinit()` | 幂等关闭 TRX 并释放 SPI 和 GPIO 资源 |

建议使用 `try/finally` 释放设备：

```python
radio = StampUWB()
try:
    # Configure and use the radio.
    pass
finally:
    radio.deinit()
```

对象 finaliser 也会调用清理逻辑，但不应依赖垃圾回收决定硬件资源释放时间。调用 `deinit()`
后，该对象的其他 API 会抛出 `OSError(ENODEV)`；随后可以重新创建一个实例。

## 双天线 Angle

`StampUWBAngle` 继承 `StampUWB`，用于 QM33120 双天线 PDoA 测角。它固定使用以下已验证配置：

```text
CH9
STS_MODE_1 | STS_MODE_SDC
STS length 256
PDOA_M3
```

初始化时必须填写实际产品的双天线中心距和零度 PDoA offset。`0.012 m` 仅来自当前
UWB-Pro Angle 硬件，不是所有双天线产品的通用值：

```python
from stamp import StampUWBAngle

radio = StampUWBAngle(
    antenna_baseline_m=0.012,
    pdoa_offset=0,
)
radio.configure()
radio.configure_tx_rf()
radio.set_antenna_delay()
radio.set_lna_pa()
```

收到 `uwb.STATUS_RX_GOOD` 后，必须在下一次 TX/RX 前立即读取 Angle 结果：

```python
result = radio.read_angle()
if result is not None:
    angle_deg, pdoa_raw, tdoa, sts_quality = result
```

`read_angle()` 依次检查 STS validity、TDoA 是否不超过
`StampUWBAngle.VALID_TDOA_LIMIT`，然后减去零度 offset、执行相位环绕，并使用 CH9 波长和天线
中心距计算 `asin()`。任何一步无效均返回 `None`，避免输出伪角度。

| API | 默认值或返回值 | 说明 |
| --- | --- | --- |
| `StampUWBAngle(antenna_baseline_m=0.012, pdoa_offset=0, **pins)` | Angle 对象 | 初始化双天线参数和可选主机引脚 |
| `configure()` | Angle PHY 默认值 | 固定 STS mode 1 + SDC、STS 256、PDoA M3 |
| `set_angle_calibration(pdoa_offset=0)` | `None` | 设置软件零度 PDoA offset |
| `pdoa_to_angle(pdoa_raw)` | `float` 或 `None` | 将校准后的 raw PDoA 换算成角度 |
| `read_angle()` | `(angle, raw, tdoa, sts_quality)` 或 `None` | 读取并校验最近 RX frame 的角度 |
| `read_pdoa()` | signed raw PDoA | 读取 s[1:-11] radians 原始相位差 |
| `read_tdoa_pdoa(index=0)` | `(tdoa, pdoa)` | 读取 PDoA/TDoA 诊断结果 |
| `read_sts_quality()` | `(valid, quality)` | 读取 STS 有效性和质量 |
| `set_pdoa_offset(offset=0)` | `None` | 设置芯片的 16-bit PDoA offset 寄存器 |
| `read_pdoa_offset()` | `int` | 读取芯片 PDoA offset 寄存器 |

Angle 零度标定应把 Tag 放在双天线机械中心法线方向，采集多次有效 `pdoa_raw` 并使用环形
平均值。天线中心距、外壳材料、天线走线和安装方向改变后必须重新标定。

## `uwb` 模块常量

### PHY 配置

| 常量 | 说明 |
| --- | --- |
| `uwb.SFD_DW_8` | Decawave 8-symbol SFD |
| `uwb.BR_6M8` | 6.8 Mbps data rate |
| `uwb.PHR_STD` | Standard PHR mode |
| `uwb.PHR_RATE_STD` | Standard PHR rate |
| `uwb.STS_OFF` | 关闭 STS |
| `uwb.STS_MODE_1` | STS mode 1 |
| `uwb.STS_MODE_SDC` | Super Deterministic Code，可与 `STS_MODE_1` 按位或组合 |
| `uwb.PDOA_M0` | PDoA mode 0 |
| `uwb.PDOA_M1` | PDoA mode 1 |
| `uwb.PDOA_M3` | 双 STS/双天线 PDoA mode 3 |
| `uwb.VALID_TDOA_LIMIT` | Angle sample 的有效 TDoA 绝对值上限 |

### TX/RX 模式

| 常量 | 说明 |
| --- | --- |
| `uwb.TX_IMMEDIATE` | 立即发送 |
| `uwb.TX_DELAYED` | 在 delayed TRX time 发送 |
| `uwb.RESPONSE_EXPECTED` | TX 后自动进入 RX |
| `uwb.RX_IMMEDIATE` | 立即接收 |
| `uwb.RX_DELAYED` | 在 delayed TRX time 接收 |
| `uwb.IDLE_ON_DELAY_ERROR` | delayed 操作失败时保持 idle |

### 状态位

| 常量 | 说明 |
| --- | --- |
| `uwb.STATUS_TX_DONE` | TX frame sent |
| `uwb.STATUS_RX_GOOD` | RX frame CRC good |
| `uwb.STATUS_RX_TIMEOUT` | 所有 RX timeout 状态位掩码 |
| `uwb.STATUS_RX_ERROR` | 所有 RX error 状态位掩码 |
| `uwb.STATUS_RX_ALL` | RX good、timeout 和 error 的组合掩码 |

## 异常与限制

- 当前为 StampS3Mini、StampC6 和 StampC5 构建该模块。
- 同一时间只允许一个活动 UWB 实例；重复构造抛出 `OSError(EBUSY)`。
- 不支持大于 125 bytes 的 Python TX payload。
- `configure()`、probe、SPI、RX enable 和 delayed TX 失败会抛出 `OSError` 或 `ValueError`。
- `wait_status()` 的软件 timeout 与硬件 RX timeout 是两种不同结果，应分别处理。
- GP7/SYNC 当前不参与 DS-TWR，也未暴露同步控制 API。
- 天线延迟、TX power 和 DS-TWR turnaround time 需要根据实际硬件和协议对端标定。

## DS-TWR 示例

- [单 Anchor Tag](../../../examples/stamp/uwb/stamps3mini_uwb_tag_example.py)
- [Anchor](../../../examples/stamp/uwb/stamps3mini_uwb_anchor_example.py)
- [多 Anchor Tag](../../../examples/stamp/uwb/stamps3mini_uwb_multi_anchor_tag_example.py)
- [Angle Tag](../../../examples/stamp/uwb/stamps3mini_uwb_angle_tag_example.py)
- [Angle Anchor](../../../examples/stamp/uwb/stamps3mini_uwb_angle_anchor_example.py)

示例默认使用 CH9、Pair ID `6666`、Anchor ID 从 `1` 开始。多块 Anchor 应分别配置唯一的
`ANCHOR_ID`，且所有设备的 PHY、Pair ID 和天线延迟必须一致。

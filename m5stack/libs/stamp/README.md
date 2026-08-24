# Stamp 扩展支持

`stamp` 包为通过 Stamp Series FPC12 接口连接的扩展提供主机引脚映射和高层驱动。
当前支持以下主机：

- StampC5
- StampC6
- StampS3Mini

本目录不是主机板支持实现，不负责板型识别、启动流程或固件目标定义。

## 包内容

| 文件 | 公开接口 | 说明 |
| --- | --- | --- |
| `f12.py` | `StampF12` | 根据当前 Stamp 主机把 FPC12 物理位置转换为 GPIO |
| `lora1262.py` | `StampLoRa1262` | Stamp LoRa-1262（S014）SX1262 LoRa 驱动 |
| `uwb.py` | `StampUWB`、`StampUWBAngle` | QM33120/DW3720 UWB 与双天线测角包装 |
| `uwb.py` | `UWBIO`、`iomap` | 为现有 UWB 代码保留的兼容接口 |

主要类通过惰性导出使用：

```python
from stamp import StampF12, StampLoRa1262, StampUWB, StampUWBAngle
```

## Stamp Series FPC12

`StampF12` 只描述 FPC12 物理位置，不包含 `SW`、`IRQ`、`BUSY` 等具体扩展的信号语义。
同一位置在不同扩展上可以有不同用途。

| 位置 | StampC5 | StampC6 | StampS3Mini |
| ---: | --- | --- | --- |
| 1 | 3V3 | 3V3 | 3V3 |
| 2 | 3V3 | 3V3 | 3V3 |
| 3 | G23 | G8 | G38 |
| 4 | G0 | G0 | G21 |
| 5 | G24 | G18 | G39 |
| 6 | G25 | G19 | G40 |
| 7 | GND | GND | GND |
| 8 | G26 | G20 | G41 |
| 9 | G27 | G21 | G42 |
| 10 | G11 | G22 | G43 |
| 11 | GND | GND | GND |
| 12 | G12 | G23 | G44 |

按位置取得当前主机 GPIO：

```python
from stamp import StampF12

f12 = StampF12()
gpio = f12.pin(4)
```

`pin(position)` 使用从 1 开始的位置编号。位置 1、2、7、11 不是 GPIO，会抛出
`ValueError`；超出 1-12 同样抛出 `ValueError`。不支持的主机在创建 `StampF12` 时抛出
`NotImplementedError`。

## Stamp LoRa-1262

`StampLoRa1262` 使用 `lora.SX1262`，默认通过 SPI1 工作。驱动在初始化时把 `SW` 拉高以
使能射频天线开关，并为 DIO3 TCXO 配置 3.0 V。S014 支持的频率范围为
`868000-923000 kHz`，默认频率为 `868000 kHz`。

### FPC12 信号

| 位置 | Stamp LoRa-1262 信号 |
| ---: | --- |
| 1 | 3V3 |
| 2 | 3V3 |
| 3 | SW |
| 4 | IRQ |
| 5 | BUSY |
| 6 | RST |
| 7 | GND |
| 8 | MISO |
| 9 | MOSI |
| 10 | CS |
| 11 | GND |
| 12 | CLK |

LoRa 驱动在自己的模块内维护以上信号与位置的关系，不向 `StampF12` 添加外设专用常量。
模块的 `SHUT_DOWN` 信号不属于 FPC12，因此驱动不控制该信号。

### 初始化和收发

支持的 Stamp 主机可以直接使用默认映射：

```python
from stamp import StampLoRa1262

radio = StampLoRa1262()
radio.send("hello")
packet = radio.recv(timeout_ms=1000)
if packet is not None:
    print(packet.decode())
```

构造函数允许覆盖 `sw`、`irq`、`busy`、`reset`、`miso`、`mosi`、`cs`、`clock` 和
`spi_id`。在其他主机上使用时必须提供全部八个信号引脚。

主要方法：

- 配置：`set_freq`、`set_sf`、`set_bw`、`set_coding_rate`、`set_syncword`、
  `set_preamble_len`、`set_output_power`
- 收发：`send`、`recv`、`start_recv`、`set_irq_callback`
- 状态与生命周期：`standby`、`sleep`、`irq_triggered`、`deinit`

示例：

- `examples/stamp/lora1262/stamp_lora1262_sender_example.py`
- `examples/stamp/lora1262/stamp_lora1262_receiver_example.py`

在线 API 文档：`docs/source/stamp/lora1262.rst`

## Stamp UWB

`StampUWB` 和 `StampUWBAngle` 继续使用相同的 FPC12 主机映射。UWB 模块在内部定义自己的
位置语义：

| 位置 | UWB 信号 |
| ---: | --- |
| 3 | GP7/SYNC |
| 4 | IRQ |
| 5 | WAKEUP |
| 6 | RESET |
| 8 | MISO |
| 9 | MOSI |
| 10 | CS |
| 12 | CLK |

现有代码仍可导入 `UWBIO` 和当前主机的 `iomap`。调用者显式传入的 UWB 引脚会覆盖默认
映射，接口行为保持兼容。

```python
from stamp import StampUWB

radio = StampUWB()
print("0x%08x" % radio.device_id())
```

UWB 的完整配置、DS-TWR、时间戳和 PDoA API 见 `docs/source/stamp/uwb.rst`。

## 打包与文档

`manifest.py` 将以下模块冻结到支持的 Stamp 固件：

- `stamp/f12.py`
- `stamp/lora1262.py`
- `stamp/uwb.py`

Stamp 在线文档入口为 `docs/source/stamp/index.rst`。

## 测试

主机模拟测试覆盖三套 FPC12 映射、LoRa 默认与覆盖引脚、SW 高电平、TCXO 电压、参数校验、
收发转发、IRQ 调度，以及 UWB 映射兼容性：

```console
python -m unittest tests/stamp/test_f12_lora1262.py -v
python -m ruff check m5stack/libs/stamp tests/stamp
python -m sphinx -E -W --keep-going -b html docs/source build/docs
```

自动化构建和模拟测试不能替代实物验证。Stamp LoRa-1262 的 TX/RX 互通、接收灵敏度、输出
功率和天线匹配仍需在目标硬件上测试。

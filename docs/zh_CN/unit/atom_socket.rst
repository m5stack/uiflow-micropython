ATOM Socket Unit
================

.. include:: ../refs/unit.atom_socket.ref

`ATOMSocketUnit` 是一个智能电源插座，适配ATOM主控。它内置HLW8032高精度电能表IC，能够测量负载的电压、电流、功率和能量。此外，它还可以作为智能插座，控制负载的通断，适用于智能家居、工业控制和能源管理等场景。

支持以下产品:

|ATOMSocketUnit|      

Micropython 示例::

    from machine import I2C
    from atom_socket import ATOMSocketUnit

    atomsocket = ATOMSocketUnit(1, (22, 33), 23) # 对于ATOM Lite
    # 获取数据
    print(atomsocket.get_data()) # 输出 (230.4192, 0.02074951, 0.8106091, 0.0)
    atomsocket.set_relay(True)   # 打开继电器
    atomsocket.set_relay(False)  # 关闭继电器
    # 读取各项指标
    print("电压:", atomsocket.get_voltage(), "V")
    print("电流:", atomsocket.get_current(), "A")
    print("功率:", atomsocket.get_power(), "W")
    print("功率因数:", atomsocket.get_power_factor())
    print("累计电量:", atomsocket.get_kwh(), "kWh")
    # 非阻塞模式接收数据
    def callback(voltage, current, power, kwh):
        print(voltage, current, power, kwh)
    atomsocket.receive_none_block(callback)
    # 停止接收数据
    atomsocket.stop_receive_data()

UIFLOW2 示例:

    |example.svg|

.. only:: builder_html

ATOMSocketUnit 类
-----------------

构造函数
---------

.. class:: ATOMSocketUnit(_id: Literal[0, 1, 2], port: list | tuple, relay: int = 23)

    初始化ATOM Socket。

    - ``_id``: 串口ID，对这个Unit没有实际用途。
    - ``port``: UART引脚号。
    - ``relay``: 继电器引脚号。
    
方法
----

.. method:: set_relay(state: bool) -> None

    设置ATOM Socket的继电器状态。

    - ``state``: 继电器的状态（True=开启，False=关闭）。

.. method:: get_data(timeout=3000) -> tuple

    获取ATOM Socket的数据。

    - ``timeout``: 函数的超时时间。

    返回ATOM Socket的数据：Tuple(电压(V), 电流(A), 功率(W), 总能量(KWh))。如果超时，则返回None。

.. method:: get_voltage() -> float

    获取ATOM Socket的电压，单位V。

.. method:: get_current() -> float

    获取ATOM Socket的电流，单位A。

.. method:: get_power() -> float

    获取ATOM Socket的功率，单位W。

.. method:: get_pf() -> int

    获取ATOM Socket的功率因数。

.. method:: get_inspecting_power() -> float

    获取ATOM Socket的检测功率，单位W。

.. method:: get_power_factor() -> float

    获取ATOM Socket的功率因数。

.. method:: get_kwh() -> float

    获取ATOM Socket的累计电量(KWh)。

.. method:: stop_receive_data() -> None

    停止从ATOM Socket接收数据。

.. method:: receive_none_block(receive_callback) -> None

    以非阻塞模式从ATOM Socket接收数据。

    - ``receive_callback``: 接收到数据时的回调函数，回调函数接收4个参数：voltage, current, power, kwh。

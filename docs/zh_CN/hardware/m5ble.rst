M5 BLE
======

.. include:: ../refs/library.m5ble.ref

M5 BLE是M5Stack基于Micropython的Low Level BLE进行二次封装的库，提供了更加简单易用的API。

Micropython示例::
    # clinet
    UUID_SERVICE1 = "6E400011-B5A3-F393-E0A9-E50E24DCCA9E"
    UUID_SERVICE1_WR = "6E400012-B5A3-F393-E0A9-E50E24DCCA9E"
    UUID_SERVICE1_RD = "6E400013-B5A3-F393-E0A9-E50E24DCCA9E"

    UUID_SERVICE2 = "6E400021-B5A3-F393-E0A9-E50E24DCCA9E"
    UUID_SERVICE2_WR = "6E400022-B5A3-F393-E0A9-E50E24DCCA9E"
    UUID_SERVICE2_RD = "6E400023-B5A3-F393-E0A9-E50E24DCCA9E"

    connected = False
    def on_connected(client):
        global connected
        print(client._service_handle_map)
        connected = True
        ble.client.set_mtu(128)

    def on_disconnected(client, conn_handle, addr_type, addr):
        global connected
        connected = False

    ble = M5BLE.Device(verbose=True)
    ble.client.scan(target_name_prefix="M5")
    ble.client.on_connected(on_connected)

    try:
        while True:
            if connected:
                ble.client.write("Hello Service 1", UUID_SERVICE1_WR, UUID_SERVICE1)
                ble.client.write("Hello Service 2", UUID_SERVICE2_WR, UUID_SERVICE2)
                time.sleep(0.1)
                print(ble.client.read(UUID_SERVICE1_RD, UUID_SERVICE1))
                print(ble.client.read(UUID_SERVICE2_RD, UUID_SERVICE2))
            time.sleep(1)
    except KeyboardInterrupt:
        gc.collect()
        print("\nExiting...")

    # server
    UUID_SERVICE1 = "6E400011-B5A3-F393-E0A9-E50E24DCCA9E"
    UUID_SERVICE1_WR = "6E400012-B5A3-F393-E0A9-E50E24DCCA9E"
    UUID_SERVICE1_RD = "6E400013-B5A3-F393-E0A9-E50E24DCCA9E"

    UUID_SERVICE2 = "6E400021-B5A3-F393-E0A9-E50E24DCCA9E"
    UUID_SERVICE2_WR = "6E400022-B5A3-F393-E0A9-E50E24DCCA9E"
    UUID_SERVICE2_RD = "6E400023-B5A3-F393-E0A9-E50E24DCCA9E"

    def onReceive(server, client):
        print("onReceive")
        if client.any(UUID_SERVICE1_WR):
            client.write(client.read(UUID_SERVICE1_WR), UUID_SERVICE1_RD)
        if client.any(UUID_SERVICE2_WR):
            client.write(client.read(UUID_SERVICE2_WR), UUID_SERVICE2_RD)

    ble = M5BLE.Device(verbose=True)
    ble.server.add_service(UUID_SERVICE1, [
        ble.server.create_characteristic(UUID_SERVICE1_RD, notify=True, read=True),
        ble.server.create_characteristic(UUID_SERVICE1_WR, write=True),
    ])
    ble.server.add_service(UUID_SERVICE2, [
        ble.server.create_characteristic(UUID_SERVICE2_RD, notify=True, read=True),
        ble.server.create_characteristic(UUID_SERVICE2_WR, write=True),
    ])
    ble.server.start()
    ble.server.on_receive(onReceive)
    while True:
        pass
    


UIFLOW2示例:

    |example.svg|

.. only:: builder_html

M5BLE
--------------

构造函数
---------------------------
.. class:: M5BLE.Device(name)

    创建一个M5BLE对象。

    - ``name`` BLE的广播名称，用于设备查找和发现。
 
    UIFLOW2:

        |init.svg|


Device方法
----------------------

.. method:: M5BLE.Device.get_mtu()

    获取BLE连接的最大传输单元（MTU），单位是字节。

    UIFLOW2:

        |get_mtu.svg|

.. method:: M5BLE.Device.deinit()

    关闭BLE连接，释放资源

    UIFLOW2:

        |deinit.svg|

client方法
----------------------

.. method:: M5BLE.Device.client.on_connected(callback)

    设置BLE连接成功的回调函数。

    - ``callback`` 连接成功的回调函数，参数为callback(M5BLE.Client)。

    UIFLOW2:

        |client_on_connected.svg|

.. method:: M5BLE.Device.client.on_disconnected(callback)
    
    设置BLE断开连接的回调函数。

    - ``callback`` 断开连接的回调函数，参数为callback(M5BLE.Client, conn_handle, addr_type, addr)。

    UIFLOW2:

        |client_on_disconnected.svg|

.. method:: M5BLE.Device.client.on_server_found(callback)

    设置BLE服务发现的回调函数。

    - ``callback`` 服务发现的回调函数，参数为callback(M5BLE.Client, (name, addr_type, addr, adv_type, rssi, adv_data))。

    UIFLOW2:

        |client_on_server_found.svg|

.. method:: M5BLE.Device.client.on_scan_finished(callback)

    设置BLE扫描结束的回调函数。

    - ``callback`` 扫描结束的回调函数，参数为callback(M5BLE.Client, scan_result=[])。

    UIFLOW2:

        |client_on_scan_finished.svg|

.. method:: M5BLE.Device.client.on_read_complete(callback)

    设置BLE读取完成的回调函数。

    - ``callback`` 读取完成的回调函数，参数为callback(M5BLE.Client, conn_handle, value_handle, char_data)。

    UIFLOW2:

        |client_on_read_complete.svg|

.. method:: M5BLE.Device.client.on_notify(callback)

    设置BLE通知的回调函数。

    - ``callback`` 通知的回调函数，参数为callback(M5BLE.Client)。

    UIFLOW2:

        |client_on_notify.svg|

.. method:: M5BLE.Device.client.scan(timeout=2000, connect_on_found=True, target_name_prefix='M5UiFlow', target_uuid=None)

    扫描BLE设备。

    - ``timeout`` 扫描超时时间，单位是毫秒，默认是2000ms。
    - ``connect_on_found`` 扫描到设备后是否自动连接，默认是True。
    - ``target_name_prefix`` 扫描目标设备的名称前缀，默认是'M5UiFlow'。
    - ``target_uuid`` 扫描目标设备的UUID。

    UIFLOW2:

        |client_scan.svg|

.. method:: M5BLE.Device.client.connect(addr_type, addr)
    
    连接BLE设备。

    - ``addr_type`` 设备地址类型。
    - ``addr`` 设备地址。

    UIFLOW2:

        |client_connect.svg|

.. method:: M5BLE.Device.client.set_current_service_uuid(service_uuid)

    设置当前服务的UUID，设置该参数后在使用any,read,write时可省略service_uuid参数。

    - ``service_uuid`` 服务的UUID。

    UIFLOW2:

        |client_set_current_service_uuid.svg|

.. method:: M5BLE.Device.client.any(char_uuid, service_uuid=None)

    检查是否有数据可读，如果有则返回缓冲区的字节数。

    - ``char_uuid`` 特征的UUID。
    - ``service_uuid`` 服务的UUID。

    UIFLOW2:

        |client_any.svg|

.. method:: M5BLE.Device.client.read(char_uuid, service_uuid=None, sz=None)

    读取BLE设备的数据。

    - ``char_uuid`` 特征的UUID。
    - ``service_uuid`` 服务的UUID。
    - ``sz`` 读取的字节数，为None则读取全部字节。

    UIFLOW2:

        |client_read.svg|

.. method:: M5BLE.Device.client.write(data, char_uuid, service_uuid=None)

    写入数据到BLE设备。

    - ``data`` 写入的数据。
    - ``char_uuid`` 特征的UUID。
    - ``service_uuid`` 服务的UUID。

    UIFLOW2:

        |client_write.svg|

.. method:: M5BLE.Device.client.close()

    关闭BLE连接。

    UIFLOW2:

        |client_close.svg|

.. method:: M5BLE.Device.client.get_services()

    获取BLE服务列表。

    UIFLOW2:

        |client_get_services.svg|

.. method:: M5BLE.Device.client.get_characteristics(service_uuid)
    
    获取BLE服务的特征列表。

    - ``service_uuid`` 服务的UUID。

    UIFLOW2:

        |client_get_characteristics.svg|

.. method:: M5BLE.Device.client.set_mtu(mtu)

    设置BLE连接的最大传输单元（MTU），单位是字节。

    - ``mtu`` 传输单元大小，单位是字节，范围是23-517，请注意不是所有设备都支持大于23的MTU。

    UIFLOW2:

        |set_mtu.svg|


server方法
----------------------

.. method:: M5BLE.Device.server.clear_services()

    清除已添加的服务。

    UIFLOW2:

        |server_clear_services.svg|

.. method:: M5BLE.Device.server.add_service(uuid, characteristics)

    添加一个服务

    - ``uuid`` 服务的UUID
    - ``characteristics`` 该服务所包含的特征列表，需要使用create_characteristic创建

    UIFLOW2:

        |server_add_service.svg|

.. method:: M5BLE.Device.server.该服务所包含的特征列表，需要使用create_characteristic创建(uuid, read, write, notify)

    创建一个特征

    - ``uuid`` 特征的UUID
    - ``read`` 该特征是否可读
    - ``write``  该特征是否可写
    - ``notify``  该特征是否可通知
    
    UIFLOW2:

        |server_create_characteristic.svg|

.. method:: M5BLE.Device.server.start(interval_us)

    启动BLE服务

    - ``interval_us`` 广播间隔时间，单位是微秒，默认是500000us。

    UIFLOW2:

        |server_start.svg|

.. method:: M5BLE.Device.server.on_receive(callback)

    设置BLE接收数据的回调函数。

    - ``callback`` 接收数据的回调函数，参数为callback(M5BLE.Client, connected_client_handle)。

    UIFLOW2:

        |server_on_receive.svg|

.. method:: M5BLE.Device.server.on_connected(callback)
    
        设置BLE设备连接成功的回调函数。
    
        - ``callback`` 设备连接成功时的回调函数，参数为callback(M5BLE.Client, connected_client_handle)。
    
        UIFLOW2:
    
            |server_on_connected.svg|


.. method:: M5BLE.Device.server.on_disconnected(callback)

    设置BLE设备断开连接的回调函数。

    - ``callback`` 设备断开连接时的回调函数，参数为callback(M5BLE.Client, connected_client_handle)。

    UIFLOW2:

        |server_on_disconnected.svg|

.. method:: M5BLE.Device.server.get_client(index)
    
        获取连接的客户端
    
        - ``index`` 客户端的索引
    
        UIFLOW2:
    
            |server_get_client.svg|

.. method:: M5BLE.Device.server.get_clients()

    获取连接的客户端列表

    UIFLOW2:

        |server_get_clients.svg|

server - connected_client_handle方法
----------------------

connected_client_handle 是由回调函数的参数传递，或使用get_client获取的已连接客户端的句柄。


.. method:: connected_client_handle.any(uuid)

    检查是否有数据可读，如果有则返回缓冲区的字节数。

    - ``uuid`` 特征的UUID。

    UIFLOW2:

        |client_any.svg|

.. method:: connected_client_handle.read(uuid, sz=None)

    读取BLE设备的数据。

    - ``uuid`` 特征的UUID。
    - ``sz`` 读取的字节数，为None则读取全部字节。

    UIFLOW2:

        |client_read.svg|

.. method:: connected_client_handle.write(data, uuid)

    写入数据到BLE设备。

    - ``data`` 写入的数据。
    - ``uuid`` 特征的UUID。

    UIFLOW2:

        |client_write.svg|

.. method:: connected_client_handle.close()

    断开链接

    UIFLOW2:

        |client_close.svg|
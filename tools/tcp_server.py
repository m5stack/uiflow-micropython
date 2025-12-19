#!/usr/bin/env python3
import socket
import threading
import time
import sys

# 存储连接的客户端: {client_id: (socket, address)}
clients = {}
client_id_counter = 0
clients_lock = threading.Lock()

def handle_client(client_socket, client_address, client_id):
    print(f"\n[+] 新连接来自: {client_address} (ID: {client_id})")
    print("Server> ", end="", flush=True)
    
    try:
        while True:
            # 接收数据
            try:
                data = client_socket.recv(1024)
            except OSError:
                break

            if not data:
                break
            
            try:
                message = data.decode('utf-8')
                print(f"\n[{client_address} ID:{client_id}] 收到: {message}")
                print("Server> ", end="", flush=True)
                
                # 自动回显 (可选，这里注释掉以便手动控制发送)
                # response = f"Server received: {message}"
                # client_socket.send(response.encode('utf-8'))
            except UnicodeDecodeError:
                print(f"\n[{client_address} ID:{client_id}] 收到二进制数据: {data}")
                print("Server> ", end="", flush=True)
                
    except ConnectionResetError:
        print(f"\n[-] 连接重置: {client_address} (ID: {client_id})")
    except Exception as e:
        print(f"\n[-] 错误 {client_address} (ID: {client_id}): {e}")
    finally:
        with clients_lock:
            if client_id in clients:
                del clients[client_id]
        try:
            client_socket.close()
        except:
            pass
        print(f"\n[-] 连接关闭: {client_address} (ID: {client_id})")
        print("Server> ", end="", flush=True)

def server_console():
    print("\n=== 服务器控制台 ===")
    print("可用命令:")
    print("  list              - 列出所有连接的客户端")
    print("  send <id> <msg>   - 发送消息给指定客户端")
    print("  close <id>        - 断开指定客户端")
    print("  broadcast <msg>   - 广播消息给所有客户端")
    print("  quit              - 停止服务器")
    print("==================\n")

    while True:
        try:
            cmd_line = input("Server> ").strip()
            if not cmd_line:
                continue
            
            parts = cmd_line.split(maxsplit=2)
            cmd = parts[0].lower()
            
            if cmd == 'list':
                with clients_lock:
                    if not clients:
                        print("当前没有连接的客户端")
                    else:
                        print(f"当前连接数: {len(clients)}")
                        for cid, (sock, addr) in clients.items():
                            print(f"  ID: {cid} | 地址: {addr}")
            
            elif cmd == 'send':
                if len(parts) < 3:
                    print("用法: send <id> <message>")
                    continue
                try:
                    target_id = int(parts[1])
                    msg = parts[2]
                    with clients_lock:
                        if target_id in clients:
                            sock, _ = clients[target_id]
                            sock.send(msg.encode('utf-8'))
                            print(f"已发送到 ID {target_id}")
                        else:
                            print(f"未找到 ID 为 {target_id} 的客户端")
                except ValueError:
                    print("ID 必须是数字")
                except Exception as e:
                    print(f"发送失败: {e}")

            elif cmd == 'close':
                if len(parts) < 2:
                    print("用法: close <id>")
                    continue
                try:
                    target_id = int(parts[1])
                    with clients_lock:
                        if target_id in clients:
                            sock, _ = clients[target_id]
                            sock.close()
                            # 从字典中移除将在 handle_client 的 finally 块中处理
                            # 但为了立即生效，我们也可以在这里移除，或者等待线程结束
                            # 这里只关闭 socket，让线程自然退出
                            print(f"已请求断开 ID {target_id}")
                        else:
                            print(f"未找到 ID 为 {target_id} 的客户端")
                except ValueError:
                    print("ID 必须是数字")
                except Exception as e:
                    print(f"操作失败: {e}")

            elif cmd == 'broadcast':
                if len(parts) < 2:
                    print("用法: broadcast <message>")
                    continue
                msg = cmd_line.split(maxsplit=1)[1]
                count = 0
                with clients_lock:
                    for cid, (sock, _) in clients.items():
                        try:
                            sock.send(msg.encode('utf-8'))
                            count += 1
                        except:
                            pass
                print(f"已广播给 {count} 个客户端")

            elif cmd == 'quit':
                print("正在停止服务器...")
                import os
                os._exit(0)
            
            else:
                print("未知命令")

        except EOFError:
            break
        except Exception as e:
            print(f"控制台错误: {e}")

def start_server(host='0.0.0.0', port=8080):
    global client_id_counter
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((host, port))
        server.listen(5)
        print(f"[*] TCP 服务器正在监听 {host}:{port}")
        
        # 启动控制台线程
        console_thread = threading.Thread(target=server_console)
        console_thread.daemon = True
        console_thread.start()
        
        while True:
            client_sock, client_addr = server.accept()
            
            with clients_lock:
                client_id_counter += 1
                current_id = client_id_counter
                clients[current_id] = (client_sock, client_addr)
            
            client_handler = threading.Thread(
                target=handle_client,
                args=(client_sock, client_addr, current_id)
            )
            client_handler.daemon = True
            client_handler.start()
            
    except KeyboardInterrupt:
        print("\n[*] 服务器正在停止...")
    except Exception as e:
        print(f"[!] 服务器错误: {e}")
    finally:
        server.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='增强版 TCP 测试服务器')
    parser.add_argument('--host', default='0.0.0.0', help='监听地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8080, help='监听端口 (默认: 8080)')
    
    args = parser.parse_args()
    
    start_server(args.host, args.port)

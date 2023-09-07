import socket
from communication import *

# 服务器的主机名和端口号
host = 'localhost'
port = 9000

# 创建一个套接字对象
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定主机名和端口号
server_socket.bind((host, port))

# 监听连接
server_socket.listen(1)
print("服务器启动，等待连接...")

# 接受客户端连接
client_socket, client_address = server_socket.accept()
print("客户端连接成功:", client_address)

safe_socket = EncryptedSocket(client_socket,client_address)
public_key = safe_socket.key
print(public_key)

while True:
    # 接收客户端消息
    message = safe_socket.recv_decrypt().decode('utf-8', errors='ignore')

    # 打印客户端消息
    print("客户端消息:", message)

    # 检查是否应该结束对话
    if message.lower() == 'bye':
        break

    # 从服务器端获取消息
    response = input("请输入服务器响应: ")

    # 发送响应到客户端
    safe_socket.send_encrypt(response.encode())

# 关闭客户端连接
del safe_socket
import socket
from communication import *

# 服务器的主机名和端口号
host = 'localhost'
port = 9000

# 创建一个套接字对象
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到服务器
client_socket.connect((host, port))

#safe_socket = EncryptedSocket(server_socket,client_address,port = None)
safe_socket = EncryptedSocket(client_socket)
public_key = safe_socket.key
print(public_key)

while True:
    # 从用户输入中获取消息
    message = input("请输入消息: ")

    # 发送消息到服务器
    safe_socket.send_encrypt(message.encode())

    # 接收服务器的响应
    response = safe_socket.recv_decrypt().decode('utf-8', errors='ignore')

    # 打印服务器的响应
    print("服务器响应:", response)
    
    # 检查是否应该结束对话
    if message.lower() == 'bye':
        break

# 关闭套接字连接
del safe_socket
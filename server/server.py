#服务器端代码
import socket
import threading
import os
from config import *
from message_type import *
dirPath = SERVER_PATH

def client_handle(client_socket, client_address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if message:
                print(f"收到来自 {client_address} 的消息: {message}")
                '''
                message_return = input('请输入你想回复的消息:')
                send_back(client_socket,message_return)
                '''
                #对于消息去解析其类型和参数
                message_parts = message.split('|') #用split函数把其分割成一个字典
                message_type = message_parts[0]
                print(message_type)
                if message_type == 'register':
                    username = message_parts[1]
                    password = message_parts[2]
                    email = message_parts[3]
                    phone = message_parts[4]
                    message_return = register(username,password,email,phone)
                    send_back(client_socket,str(message_return))
                elif message_type == 'login_password':
                    username = message_parts[1]
                    password = message_parts[2]
                    #print(username,password)
                    message_return = login_password(username,password)
                    send_back(client_socket,str(message_return))
                elif message_type == 'get_email_code':
                    email = message_parts[1]
                    message_return = get_email_code(email)
                    send_back(client_socket,str(message_return))
                elif message_type == 'login_email':
                    email = message_parts[1]
                    auth_code = message_parts[2]
                    message_return = login_email(email,auth_code)
                    send_back(client_socket,str(message_return))
                elif message_type == 'get_phone_code':
                    phone = message_parts[1]
                    message_return = get_phone_code(phone)
                    send_back(client_socket,str(message_return))
                elif message_type == 'change_password':
                    phone = message_parts[1]
                    auth_code = message_parts[2]
                    old_password = message_parts[3]
                    new_password = message_parts[4]
                    message_return = change_password(phone,auth_code,old_password,new_password) 
                    send_back(client_socket,str(message_return))      
        except:
            print(f"'{client_address}'断开连接")
            client_socket.close()
            break
        
def send_back(client_socket, message_return):
    client_socket.send(message_return.encode())

#定义服务器函数，函数运行
def server_run():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((SERVER_IP,SERVER_PORT))  #此处要记得改成config文件里的参数
    server.listen(5)
    print("服务器运行中...")

    while True:
        client_socket, client_address = server.accept()
        print(f"客户端 {client_address} 连接成功")
        
        # 创建新线程处理客户端连接
        client_thread = threading.Thread(target=client_handle, args=(client_socket, client_address))
        client_thread.start()

if __name__ == '__main__':
    server_run()
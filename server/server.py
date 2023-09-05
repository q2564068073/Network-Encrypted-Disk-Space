#服务器端代码
import socket
import threading
import os
from config import *
from message_type import *
from protocol.communication import *

dirPath = SERVER_PATH

def client_handle(client_socket, client_address):
    safe_socket = EncryptedSocket(client_socket,client_address)
    #public_key = safe_socket.key
    while True:
        try:
            message = safe_socket.recv_decrypt().decode('utf-8',errors = 'ignore')
            if message:
                print(f"收到来自 {client_address} 的消息: {message}")
                #对于消息去解析其类型和参数
                message_parts = message.split('|') #用split函数把其分割成一个字典
                message_type = message_parts[0]
                #print(message_type)
                if message_type == 'register':
                    username = message_parts[1]
                    password = message_parts[2]
                    email = message_parts[3]
                    phone = message_parts[4]
                    message_return = register(username,password,email,phone)
                    send_back(safe_socket,str(message_return))
                elif message_type == 'login_password':
                    username = message_parts[1]
                    password = message_parts[2]
                    #print(username,password)
                    message_return = login_password(username,password)
                    print(message_return)
                    send_back(safe_socket,str(message_return))
                elif message_type == 'get_email_code':
                    email = message_parts[1]
                    message_return = get_email_code(email)
                    send_back(safe_socket,str(message_return))
                elif message_type == 'login_email':
                    email = message_parts[1]
                    auth_code = message_parts[2]
                    message_return = login_email(email,auth_code)
                    send_back(safe_socket,str(message_return))
                elif message_type == 'get_phone_code':
                    phone = message_parts[1]
                    message_return = get_phone_code(phone)
                    send_back(safe_socket,str(message_return))
                elif message_type == 'change_password':
                    phone = message_parts[1]
                    auth_code = message_parts[2]
                    old_password = message_parts[3]
                    new_password = message_parts[4]
                    message_return = change_password(phone,auth_code,old_password,new_password) 
                    send_back(safe_socket,str(message_return))
                elif message_type == 'upload':
                    username = message_parts[1]
                    filename = message_parts[2]
                    key_hash = message_parts[3]
                    #message_return = save_file(username, filename,key_hash)
                    message_return_ok = save_file_check(username,filename,key_hash)
                    send_back(safe_socket,str(message_return_ok))
                    #记得写个数据库函数把前面的三个关键词入表
                    if message_return_ok == 'ok':
                        file = safe_socket.recv_decrypt() #收到加密后的文件
                        save_file(username,filename,file)
                        print(file)
                    #存储加密文件，记得用filename命名
                elif message_type == 'download':
                    username = message_parts[1]
                    filename = message_parts[2]
                    key_hash = message_parts[3]
                    #message_return = send_file(username, filename, key_hash)
                    send_back(safe_socket,str(message_return))    
                elif message_type == 'get_list':
                    username = message_parts[1]
                    message_return = find_file(username)
                    if message_return == 0:
                        send_back(safe_socket,'没有文件')
                    else:
                        send_back(safe_socket,str(message_return))
        except:
            print(f"'{client_address}'断开连接")
            client_socket.close()
            break
        
def send_back(safe_socket, message_return):
    safe_socket.send_encrypt(message_return.encode())

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
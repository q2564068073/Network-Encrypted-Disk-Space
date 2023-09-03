import sys

from ..server.server import*
from encryption_utils import*

class encrypted_socket:
    def __init__(self,socket,address = None,port = None):
        self.socket = socket
        self.address = address
        self.port = port
        self.key = None

        if self.address:
            self.server_shakehands()
        else:
            self.client_shakehands()

    def server_shakehands(self):
        key_first = None
        key_second = None
        key_third = None
        s_key = c_key = None

        while True:
            message = self.socket.recv(1024).decode()
            try:
                if message:
                    message_parts: str = message.split('|')  # 用split函数把其分割成一个字典
                    if  message_parts[0] == 'Client_Hello':
                        key_first = message_parts[1]
                        s_key, c_key = create_rsa_key()
                        key_second = get_random_number()
                        server_response = 'Server_Hello' + '|' + key_second + '|' + c_key
                        self.socket.send(server_response.encode('utf-8'))

                    elif message_parts[0] == 'client_shakehands_done':
                        key_third = rsa_decrypt(message_parts[1].encode('utf-8'),  s_key.encode('utf-8'))
                        self.key = key_first+key_second+key_third

                        server_response = 'server_shakehands_done'
                        self.socket.send(server_response.encode('utf-8'))
                        break
            except:
                # 处理异常，例如客户端断开连接
                print(f"{self.address} 断开连接")
                self.socket.close()
                break

    def client_shakehands(self):
        key_first = get_random_number()
        key_second = None
        key_third = None

        client_hello = 'Client_Hello'+'|'+key_first
        self.socket.send(client_hello.encode('utf-8'))
        while True:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    # 对于消息去解析其类型和参数
                    message_parts: str = message.split('|')  # 用split函数把其分割成一个字典
                    message_type = message_parts[0]
                    if message_type == 'Server_Hello':
                        key_second = message_parts[1]
                        if message_parts[2]:
                            raise Exception("网站验证失败！")
                        client_key = message_parts[3]

                        key_third = rc4_encrypt(get_random_number().encode('utf-8'), client_key.encode('utf-8'))
                        self.key = key_first + key_second + key_third
                        client_response = 'client_shakehands_done'+'|'+ key_third
                        self.socket.send(client_response.encode('utf-8'))

                    elif message_type == 'server_shakehands_done':
                        break
            except:
                    # 处理异常，例如客户端断开连接
                    print(f"连接已断开")
                    self.socket.close()
                    break

        return 0

    def send_back(self,data):
        text = rc4_encrypt(data, self.key.encode('utf-8'))
        self.socket.send(text.encode('utf-8'))


    def recv(self):
        text = self.socket.recv(1024).decode()
        response = rc4_decrypt(text.encode('utf-8'), self.key.encode('utf-8'))
        return response


    def certificate_permit(self,certificate):
        if certificate:
            return False
        return True


#from ..server.server import *
from protocol.encryption_utils import *
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.x509.oid import NameOID
from config import *
import os
import datetime

#with open('./certificate/cert.pem', 'rb') as f:
    #cert = f.read()

class EncryptedSocket:
    """
    方法：
    利用现有套接字建立安全信道
    服务器端的握手操作
    客户端的握手操作
    建立完信道之后 通信时调用send和recv进行发送和接受的预处理
    tls中的安全证书的验证
    """
    def __init__(self, socket, address=None, port=None):
        self.socket = socket
        self.address = address
        self.port = port
        self.key = None

        if self.address:
            self.server_shakehands()
        else:
            self.client_shakehands()

    def server_shakehands(self):
        print("我进来了")
        key_first = None
        key_second = None
        key_third = None
        pub_key, priv_key = create_rsa_key()  # 类似tls安全信道的设计 会话密钥由三部分组成 k1k2是两个随机数

        while True:
            message: str = self.socket.recv(8192).decode('utf-8', errors='ignore')
            print(message)
            print("原神启动")
            try:
                if message != '':
                    message_parts = message.split('|')  # 用split函数把其分割成一个字典
                    if message_parts[0] == 'Client_Hello':
                        key_first: str = message_parts[1]
                        #s_key, c_key = create_rsa_key()   #公钥  私钥
                        key_second: str = get_random_number() #第二随机数
                        
                        # cert_file = "./certificate.pem"#数字证书
                        # if os.path.exists(cert_file):
                        with open('C:\\Users\\29923\\Desktop\\testing\\server\\protocol\\certificate.pem', "rb") as cert_file:
                            cert_data = cert_file.read()

                        server_response = 'Server_Hello' + '|' + key_second + '|' + cert_data.decode() + '|'
                        self.socket.send(server_response.encode()+pub_key)
                        # print("三国杀启动")

                    elif message_parts[0] == 'client_shakehands_done':
                        # print("二阶段")
                        # print(priv_key)
                        key_third: bytes = rsa_decrypt(message_parts[1].encode(), priv_key)
                        self.key = key_first + key_second + key_third.decode()
                
                        server_response = 'server_shakehands_done'
                        self.socket.send(server_response.encode())
                        break
            except Exception as e:
                # 处理异常，例如客户端断开连接
                print(e)
                print(f"{self.address} 断开连接")
                self.socket.close()
                break

    def client_shakehands(self):
        key_first = get_random_number()
        print(key_first)
        key_second = None
        key_third = None
        client_hello = 'Client_Hello' + '|' + key_first
        print(client_hello)
        self.socket.send(client_hello.encode())
        print("11111")
        while True:
            try:
                message: str = self.socket.recv(8192).decode('utf-8', errors='ignore')# 长度应该大于1024字节
                if message:
                    # 对于消息去解析其类型和参数
                    message_parts = message.split('|')  # 用split函数把其分割成一个字典
                    message_type = message_parts[0]
                    if message_type == 'Server_Hello':
                        print("22222")
                        key_second: str = message_parts[1]
                        certificate: str = message_parts[2]
                        if certificate:
                            print('开始验证网站！')
                            print(message_parts[2])
                            if self.certificate_permit(certificate):
                                # 检验证书
                                print("网站验证失败！")
                                raise Exception("网站验证失败！")
                            server_pub_key: str = message_parts[3]
                        #print(key_second)
                        #print(client_key)
                        print("server_pub_key:", server_pub_key)
                        # print(rsa_encrypt(b"111",server_pub_key.encode()))
                        key_third = get_random_number().encode()
                        self.key = key_first + key_second + key_third.decode()
                        print("key_third:", key_third)
                        key_third = rsa_encrypt(key_third, server_pub_key.encode())
                        print("self.key:", self.key)
                        client_response = b'client_shakehands_done|'+ key_third
                        self.socket.send(client_response)

                    elif message_type == 'server_shakehands_done':
                        break
            except Exception as e:
                # 处理异常，例如客户端断开连接
                print(e)
                print(f"连接已断开")
                self.socket.close()
                break

        return 0

    def send_encrypt(self, data:bytes):
        length=len(data)

        key=self.key # str类型
        s_box=rc4_key_schedule(key)
        key_stream=generate_rc4_keystream(s_box,length)

        text=rc4_en_de_crypt(data, key_stream)
        text = base64.b64encode(text)
        self.socket.send(text)

        """file_to_send, key_hash=rc4_file(path,key) # 加密后的文件和密钥的hash值(字节流)

        data_hash=get_hash(data)  # 字符串格式的hash"""

        # 加密后的文件 密钥的hash 文件的hash
        # 发送时 使用信道上的会话密钥作为种子密钥 产生rc4密钥流进行加密 用来实现对文件的一次一密
        """text = rc4_encrypt(data.decode('utf-8'), self.key.decode('utf-8'))
        self.socket.send(text)"""

    def recv_decrypt(self):
        text = self.socket.recv(819200).decode()
        text = base64.b64decode(text)
        length = len(text)

        key = self.key  # str类型
        s_box = rc4_key_schedule(key)
        key_stream = generate_rc4_keystream(s_box, length)

        text=rc4_en_de_crypt(text, key_stream)#

        return text# bytes格式


    def certificate_permit(self, cert_data):
        # 读取证书文件
        certificate_data = cert_data.encode()

        # 读取私钥文件
        with open('C:\\Users\\29923\\Desktop\\testing\\server\\protocol\\private_key.pem', "rb") as private_key_file:
            private_key_data = private_key_file.read()

        # 将证书数据加载为X.509证书对象
        certificate = x509.load_pem_x509_certificate(certificate_data, default_backend())

        # 将私钥数据加载为私钥对象
        private_key = serialization.load_pem_private_key(private_key_data, password=None, backend=default_backend())

        # 验证证书是否有效
        current_time = datetime.datetime.utcnow()

        if current_time < certificate.not_valid_before or current_time > certificate.not_valid_after:
            print("证书已过期或尚未生效")
        else:
            try:
                certificate.public_key().verify(
                    certificate.signature,
                    certificate.tbs_certificate_bytes,
                    padding.PKCS1v15(),
                    certificate.signature_hash_algorithm,
                )
                print("证书验证成功！")
                print("颁发给：", certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value)
                print("颁发者：", certificate.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value)
                print("有效期自：", certificate.not_valid_before)
                print("有效期至：", certificate.not_valid_after)
            except Exception as e:
                print("证书验证失败:", e)


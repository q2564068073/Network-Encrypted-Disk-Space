from ..server.server import*
from encryption_utils import*
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.hashes import SHA256

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
        key_first = None
        key_second = None
        key_third = None
        s_key = c_key = None  # 类似tls安全信道的设计 会话密钥由三部分组成 k1k2是两个随机数

        while True:
            message = self.socket.recv(1024).decode()
            try:
                if message:
                    message_parts = message.split('|')  # 用split函数把其分割成一个字典
                    if message_parts[0] == 'Client_Hello':
                        key_first = message_parts[1]
                        s_key, c_key = create_rsa_key()
                        key_second = get_random_number()
                        server_response = 'Server_Hello' + '|' + key_second + '|' + SERVER_CERTIFICATE + '|' + c_key
                        self.socket.send(server_response)

                    elif message_parts[0] == 'client_shakehands_done':
                        key_third = rsa_decrypt(message_parts[1].decode('utf8'), s_key.decode('utf-8'))
                        self.key = str(key_first) + str(key_second) + str(key_third)

                        server_response = 'server_shakehands_done'
                        self.socket.send(server_response)
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

        client_hello = 'Client_Hello' + '|' + key_first
        self.socket.send(client_hello)
        while True:
            try:
                message = self.socket.recv(1024).decode()
                if message:
                    # 对于消息去解析其类型和参数
                    message_parts = message.split('|')  # 用split函数把其分割成一个字典
                    message_type = message_parts[0]
                    if message_type == 'Server_Hello':
                        key_second = message_parts[1]
                        if message_parts[2]:
                            #检验证书
                            raise Exception("网站验证失败！")
                        client_key = message_parts[3]

                        key_third = rsa_encrypt(get_random_number().decode('utf8'), client_key)
                        self.key = str(key_first) + str(key_second) + str(key_third)
                        client_response = 'client_shakehands_done' + '|' + key_third
                        self.socket.send(client_response)

                    elif message_type == 'server_shakehands_done':
                        break
            except:
                # 处理异常，例如客户端断开连接
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

        self.socket.send(text)

        """file_to_send, key_hash=rc4_file(path,key) # 加密后的文件和密钥的hash值(字节流)

        data_hash=get_hash(data)  # 字符串格式的hash"""

        # 加密后的文件 密钥的hash 文件的hash
        # 发送时 使用信道上的会话密钥作为种子密钥 产生rc4密钥流进行加密 用来实现对文件的一次一密
        """text = rc4_encrypt(data.decode('utf-8'), self.key.decode('utf-8'))
        self.socket.send(text)"""

    def recv_decrypt(self):
        text = self.socket.recv(1024).decode()
        length = len(text)

        key = self.key  # str类型
        s_box = rc4_key_schedule(key)
        key_stream = generate_rc4_keystream(s_box, length)

        text=rc4_en_de_crypt(text, key_stream)#

        return text# bytes格式


    def certificate_permit(self, certificate):
        with open("private.pem", "rb") as private:
            cert_data = certificate
            private_key = private.read()

        # 加载私钥
        private_key = serialization.load_pem_private_key(private_key, password=None, backend=default_backend())

        # 提取公钥
        public_key = private_key.public_key()
        
        # 解析证书
        cert = x509.load_pem_x509_certificate(cert_data, default_backend())

        # 提取证书中的签名
        signature = cert.signature

        # 提取证书中的数据
        data = cert.tbs_certificate_bytes

        # 加载公钥
        public_key = serialization.load_pem_public_key(public_key, default_backend())

        # 验证签名
        try:
            public_key.verify(
                signature,
                data,
                padding.PKCS1v15(),
                SHA256()
            )
            print("数字证书验证成功！")
            return False
        except Exception as e:
            print(f"数字证书验证失败: {e}")
            return True


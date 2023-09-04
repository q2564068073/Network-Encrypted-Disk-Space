import base64
import hashlib
from Crypto.Cipher import ARC4
from Crypto.Random import get_random_bytes
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def create_rsa_key():
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    pub_key = key.publickey().exportKey()
    priv_key = key.exportKey()
    return pub_key.decode('utf-8'), priv_key.decode('utf-8')

def rsa_encrypt(data: bytes, pub_key: bytes) -> str:
    key = RSA.importKey(pub_key)
    cipher = PKCS1_cipher.new(key)
    data = cipher.encrypt(data).decode('utf-8')
    return data

def rsa_decrypt(data: bytes, priv_key: bytes) -> str:
    key = RSA.importKey(priv_key)
    cipher = PKCS1_cipher.new(key)
    data = cipher.decrypt(data, 0).decode('utf-8')
    return data

def rc4_key_schedule(seed_key_str):
    """
    传入一个字符串类型的种子密钥
    返回rc4的S盒
    """
    s_box = list(range(256))
    j = 0
    seed_key_bytes = seed_key_str.encode()

    seed_key = [int(byte) for byte in seed_key_bytes]

    for i in range(256):
        j = (j + s_box[i] + seed_key[i % len(seed_key)]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]

    return s_box


def generate_rc4_keystream(S: list, data_length: int):
    """
    传入S盒和需加密的文件长度
    返回生成的密钥流
    之后按位异或
    """

    i = 0
    j = 0

    keystream = []
    for _ in range(data_length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        keystream_byte = S[t]
        keystream.append(keystream_byte)

    return bytes(keystream)

"""
rc4负责文件的加密和信道的加密
"""

def rc4_en_de_crypt(data: bytes, key: bytes):
    result = bytes([a ^ b for a, b in zip(data, key)])
    return result


def rc4_file(file_path, seed_key:str):
    """
    给定要发送的文件路径以及加解密密码，返回加密后的文件字节流和加解密密码的hash值
    """
    # 文件转字节流
    with open(file_path, 'rb') as file:
        # 读取文件内容到字节流
        file_byte_stream = file.read()
    file_len = len(file_byte_stream)

    key_hash=get_hash(seed_key.encode("utf-8"))


    s_box = rc4_key_schedule(seed_key)
    keystream = generate_rc4_keystream(s_box, file_len)
    file_to_send = rc4_en_de_crypt(file_byte_stream, keystream)

    return file_to_send,key_hash.encode("utf-8")

def rc4_encrypt(data: bytes, key: bytes) -> str:
    cipher = ARC4.new(key)
    return cipher.encrypt(data).decode('utf-8')

def rc4_decrypt(data: bytes, key: bytes) -> str:
    cipher = ARC4.new(key)
    return cipher.decrypt(data).decode('utf-8')

def get_key_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def create_signature(data: bytes, priv_key: bytes) -> str:
    h = SHA256.new(data)
    key = RSA.importKey(priv_key)
    signer = pkcs1_15.new(key).sign(h)
    signature = base64.b64encode(signer).decode('utf-8')
    return signature

def verify_signature(data: bytes, signature: bytes, pub_key: bytes):
    h = SHA256.new(data)
    key = RSA.importKey(pub_key)
    try:
        pkcs1_15.new(key).verify(h, base64.b64decode(signature))
        print("验证通过,签名有效")
    except (ValueError, TypeError):
        print("验证失败,签名无效")

def get_random_number() -> str:
    return get_random_bytes(16).decode('utf-8')

def create_session_key(a: str, b: str, c: str):
    return a + b + c

def verify_certificate(certificate) -> bool:
    pass
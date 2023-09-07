import base64
import hashlib
import random
from Crypto.Cipher import ARC4
from Crypto.Random import get_random_bytes
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def create_rsa_key():
    # RSA有特殊的编码方式，encode和decode会改变其编码方式 会崩溃 
    # 返回值是utf-8编码格式的字节流
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    pub_key = key.public_key().export_key()
    priv_key = key.export_key()
    return pub_key, priv_key

def rsa_encrypt(data: bytes, pub_key: bytes):
    # 返回的是RSA特有编码格式的密文 不可decode（） 就看作一种字节流 解密后才能看铭文
    key = RSA.import_key(pub_key)
    cipher = PKCS1_cipher.new(key)
    data = cipher.encrypt(data)
    return data

def rsa_decrypt(data: bytes, priv_key: bytes) -> str:
    key = RSA.import_key(priv_key)
    cipher = PKCS1_cipher.new(key)
    data = cipher.decrypt(data, 0).decode('utf-8')
    return data

a,b=create_rsa_key()

print(type(a))
en=rsa_encrypt(b"111",a)
de=rsa_decrypt(en,b)
print(en)
print(de)

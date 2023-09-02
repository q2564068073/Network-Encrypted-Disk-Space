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
    return pub_key, priv_key

def rsa_encrypt(data: bytes, pub_key: bytes):
    key = RSA.importKey(pub_key)
    cipher = PKCS1_cipher.new(key)
    data = cipher.encrypt(data)
    return data

def rsa_decrypt(data: bytes, priv_key: bytes):
    key = RSA.importKey(priv_key)
    cipher = PKCS1_cipher.new(key)
    str_data = cipher.decrypt(data).decode('utf-8')
    return str_data

def create_rc4_key():
    return get_random_bytes(16)

def rc4_encrypt(data: bytes, key: bytes):
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def rc4_decrypt(data: bytes, key: bytes):
    cipher = ARC4.new(key)
    return cipher.decrypt(data)

def get_hash(data: bytes):
    return hashlib.sha256(data).hexdigest()

def create_signature(data: bytes, priv_key: bytes):
    h = SHA256.new(data)
    key = RSA.importKey(priv_key)
    signer = pkcs1_15.new(key).sign(h)
    signature = base64.b64encode(signer)
    return signature

def verify_signature(data: bytes, signature: bytes, pub_key: bytes):
    h = SHA256.new(data)
    key = RSA.importKey(pub_key)
    try:
        pkcs1_15.new(key).verify(h, base64.b64decode(signature))
        print("验证通过,签名有效")
    except (ValueError, TypeError):
        print("验证失败,签名无效")
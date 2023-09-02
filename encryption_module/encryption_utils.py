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
    str_data = cipher.decrypt(data, 0).decode('utf-8')
    return str_data

def rc4_key_schedule(seed: bytes):
    S = list(range(256))
    T = [ord(seed[i % len(seed)]) for i in range(256)]

    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]

    return S

def generate_rc4_keystream(S: list, data_length: int):
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

    return bytes(''.join(keystream))

def rc4_encrypt(data: bytes, key: bytes):
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def rc4_decrypt(data: bytes, key: bytes):
    cipher = ARC4.new(key)
    return cipher.decrypt(data)

def get_key_hash(data: bytes):
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

def get_random_number():
    return int(get_random_bytes(16))

def create_session_key(a: bytes, b: bytes, c: bytes):
    return a + b + c
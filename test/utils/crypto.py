# -*- coding: utf-8 -*-
"""加密/混淆工具"""

import base64
import hashlib
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

def xor_obfuscate(data: bytes, key: bytes) -> bytes:
    """XOR混淆"""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def xor_deobfuscate(data: bytes, key: bytes) -> bytes:
    return xor_obfuscate(data, key)  # XOR对称

def derive_key(password: str, salt: bytes = None) -> bytes:
    if salt is None:
        salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return kdf.derive(password.encode())

# -*- coding: utf-8 -*-
"""加密工具（纯标准库，无第三方依赖）"""

import base64
import hashlib
import os

def xor_obfuscate(data: bytes, key: bytes) -> bytes:
    """XOR 混淆/去混淆"""
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def derive_key(password: str, salt: bytes = None) -> bytes:
    """使用 PBKDF2 派生密钥（标准库实现）"""
    if salt is None:
        salt = os.urandom(16)
    # 使用 hashlib.pbkdf2_hmac（Python 3.4+ 内置）
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000, dklen=32)

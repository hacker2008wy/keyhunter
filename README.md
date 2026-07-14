# KeyHunter - 轻量级密钥泄漏扫描器

KeyHunter 是一款基于 Python 标准库编写的密钥泄漏扫描工具，帮助开发者在代码提交前发现硬编码的 API 密钥、凭证和 Token。它零依赖、即拷即用，特别适合在 Termux、容器或受限环境中使用。

---

# KeyHunter - Lightweight Secret Leak Scanner

KeyHunter is a secret scanning tool written in pure Python standard library, helping developers find hardcoded API keys, credentials, and tokens before committing code. Zero dependencies, copy-and-run, especially suitable for Termux, containers, or restricted environments.

---

## 功能特点 / Features

- 内置 20+ 种常见密钥模式：OpenAI、Claude、DeepSeek、AWS、GitHub、Google、Azure、Slack、JWT 等。
- 支持自定义规则：可通过命令行 JSON 字符串或外部文件添加新规则。
- 递归扫描目录，自动排除版本控制、缓存、依赖等干扰目录（如 .git, node_modules）。
- 支持按文件扩展名过滤扫描范围。
- 输出格式支持纯文本（可供人阅读）和 JSON（便于程序处理）。
- 所有错误信息均友好提示，不暴露内部路径或堆栈跟踪，适合终端交互。

- Built-in 20+ common secret patterns: OpenAI, Claude, DeepSeek, AWS, GitHub, Google, Azure, Slack, JWT, etc.
- Support custom rules: add new rules via command-line JSON string or external file.
- Recursively scan directories, automatically exclude version control, cache, and dependency directories (e.g., .git, node_modules).
- Support filtering scan scope by file extension.
- Output formats: plain text (human-readable) and JSON (machine-friendly).
- All errors are displayed as friendly messages, no internal paths or stack traces exposed, suitable for terminal interaction.

---

## 安装与运行 / Installation & Usage

### 系统要求 / System Requirements
- Python 3.7 或更高版本（仅需标准库，无需额外安装包）
- Python 3.7 or higher (standard library only, no extra packages required)

### 获取代码 / Get the Code
```bash
git clone https://github.com/hacker2008wy/keyhunter.git
cd keyhunter
或直接下载源码包并解压。
Or download the source package and extract it.
---

基本用法 / Basic Usage
bash
'''# 扫描当前目录（默认只扫描常见代码文件）
# Scan current directory (default: common code files)
python keyhunter.py scan

# 扫描指定目录
# Scan specific directory
python keyhunter.py scan /path/to/your/project

# 输出 JSON 格式报告
# Output JSON format report
python keyhunter.py scan /path --output json

# 自定义扩展名（只扫描 .py 和 .env 文件）
# Custom extensions (only scan .py and .env files)
python keyhunter.py scan --extensions .py,.env

# 排除额外目录（例如排除 test 和 docs）
# Exclude additional directories (e.g., test and docs)
python keyhunter.py scan --exclude test,docs

# 使用自定义规则（JSON 字符串）
# Use custom rules (JSON string)
python keyhunter.py scan --patterns '[{"pattern":"sk-[a-zA-Z0-9]{32}","name":"CustomKey","severity":"HIGH"}]'

# 查看帮助
# View help
python keyhunter.py -h
'''
---

攻击测试模块 / Penetration Testing Modules
bash 
'''# 列出所有可用的攻击模块
# List all available attack modules
python keyhunter.py list

# 执行 OAuth 同意钓鱼攻击
# Execute OAuth consent phishing attack
python keyhunter.py attack --module oauth_consent --target victim@example.com

# 生成恶意 npm 后门包
# Generate malicious npm backdoor package
python keyhunter.py attack --module npm_backdoor --output ./evil_package

# 生成恶意 IDE 插件
# Generate malicious IDE plugin
python keyhunter.py attack --module ide_plugin --output ./evil_plugin

# 生成 AI Agent 提示词注入 payload
# Generate AI Agent prompt injection payload
python keyhunter.py attack --module prompt_injection --target https://github.com/org/repo
'''

---

自定义规则详解 / Custom Rules

规则格式为 JSON 数组，每个对象包含三个字段：

· pattern：正则表达式字符串（大小写不敏感匹配）。
· name：规则名称（描述性文字）。
· severity：风险等级，可选 HIGH, MEDIUM, LOW。

Rules are JSON arrays, each object contains three fields:

· pattern: regex string (case-insensitive).
· name: rule name (descriptive text).
· severity: risk level, one of HIGH, MEDIUM, LOW.

示例规则文件 my_patterns.json / Example rule file my_patterns.json:

[
    {"pattern": "xox[baprs]-[0-9a-zA-Z]{10,}", "name": "Slack Token", "severity": "HIGH"},
    {"pattern": "AIza[0-9A-Za-z_-]{35}", "name": "Google API Key", "severity": "HIGH"}
]

使用方式 / Usage:
python keyhunter.py scan --patterns-file my_patterns.json

若同时指定 --no-default-rules，则只使用自定义规则，忽略内置规则。
If --no-default-rules is also specified, only custom rules are used, ignoring built-in rules.

---

输出示例（文本格式）/ Output Example (Text Format)
KeyHunter Scan Report - /home/user/project
==================================================
Total findings: 3
--------------------------------------------------

[1] File: /home/user/project/src/config.py:42
    Severity: HIGH
    Pattern: OpenAI API Key
    Match: OPENAI_API_KEY = "sk-abc123def456..."
    Context (surrounding lines):
        # Load environment
        OPENAI_API_KEY = "sk-abc123def456..."
        model = "gpt-4"
    ------------------------------

[2] File: /home/user/project/.env:5
    Severity: HIGH
    Pattern: AWS Access Key ID
    Match: AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
    Context:
        DB_PASS=secret
        AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
        AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
    ------------------------------

---

常见问题 / FAQ

Q: 为什么扫描不到某些文件？
A: 请检查文件扩展名是否在默认扫描列表中（可通过 --extensions 添加），或文件是否被排除目录过滤。

Q: Why are some files not scanned?
A: Check if the file extension is in the default scan list (can be added via --extensions), or if the file is filtered by excluded directories.

---

Q: 扫描结果中包含很多误报怎么办？
A: 你可以通过 --exclude 排除特定目录，或修改 config/settings.py 中的 DEFAULT_EXTENSIONS 和 DEFAULT_EXCLUDE_DIRS 来调整。另外，也可以使用自定义规则替换内置规则。

Q: What if the scan results contain many false positives?
A: You can exclude specific directories via --exclude, or modify DEFAULT_EXTENSIONS and DEFAULT_EXCLUDE_DIRS in config/settings.py. Alternatively, use custom rules to replace built-in rules.

---

Q: 扫描过程中出现权限错误？
A: KeyHunter 会静默跳过无法读取的文件，不会中断扫描。若持续遇到问题，请确保你有读取目标文件的权限。

Q: Permission errors during scanning?
A: KeyHunter silently skips unreadable files without interrupting the scan. If problems persist, ensure you have read permissions for the target files.

---

贡献与反馈 / Contributing & Feedback

欢迎提交 Issue 和 Pull Request。详见 CONTRIBUTING.md。

Issues and Pull Requests are welcome. See CONTRIBUTING.md for details.

---

许可证 / License

本项目采用 MIT 许可证，详情见 LICENSE 文件。

This project is licensed under the MIT License. See the LICENSE file for details.

---

渗透测试模块 / Penetration Testing Modules

test/ 目录包含用于授权红队行动的攻击性安全模块。

The test/ directory contains offensive security modules for authorized red team operations.

详细说明请见 test/README.md。

See test/README.md for details.


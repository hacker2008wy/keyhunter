# KeyHunter - 轻量级密钥泄漏扫描器

KeyHunter 是一款基于 Python 标准库编写的密钥泄漏扫描工具，帮助开发者在代码提交前发现硬编码的 API 密钥、凭证和 Token。它零依赖、即拷即用，特别适合在 Termux、容器或受限环境中使用。

## 功能特点

- 内置 20+ 种常见密钥模式：OpenAI、Claude、DeepSeek、AWS、GitHub、Google、Azure、Slack、JWT 等。
- 支持自定义规则：可通过命令行 JSON 字符串或外部文件添加新规则。
- 递归扫描目录，自动排除版本控制、缓存、依赖等干扰目录（如 .git, node_modules）。
- 支持按文件扩展名过滤扫描范围。
- 输出格式支持纯文本（人类可读）和 JSON（便于程序处理）。
- 所有错误信息均友好提示，不暴露内部路径或堆栈跟踪，适合终端交互。

## 安装与运行

### 系统要求
- Python 3.7 或更高版本（仅需标准库，无需额外安装包）

### 获取代码
```bash
git clone https://github.com/hacker2008wy/keyhunter.git
cd keyhunter
或直接下载源码包并解压。

基本用法
# 扫描当前目录（默认只扫描常见代码文件）
python keyhunter.py

# 扫描指定目录
python keyhunter.py /path/to/your/project

# 输出 JSON 格式报告
python keyhunter.py /path --output json

# 自定义扩展名（只扫描 .py 和 .env 文件）
python keyhunter.py --extensions .py,.env

# 排除额外目录（例如排除 test 和 docs）
python keyhunter.py --exclude test,docs

# 使用自定义规则（JSON 字符串）
python keyhunter.py --patterns '[{"pattern":"sk-[a-zA-Z0-9]{32}","name":"CustomKey","severity":"HIGH"}]'

帮助命令

python keyhunter.py -h

自定义规则详解

规则格式为 JSON 数组，每个对象包含三个字段：

· pattern：正则表达式字符串（大小写不敏感匹配）。
· name：规则名称（描述性文字）。
· severity：风险等级，可选 HIGH, MEDIUM, LOW。

示例规则文件 my_patterns.json：
[
    {"pattern": "xox[baprs]-[0-9a-zA-Z]{10,}", "name": "Slack Token", "severity": "HIGH"},
    {"pattern": "AIza[0-9A-Za-z_-]{35}", "name": "Google API Key", "severity": "HIGH"}
]

使用方式：

python keyhunter.py --patterns-file my_patterns.json

若同时指定 --no-default-rules，则只使用自定义规则，忽略内置规则。

输出示例（文本格式）：

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

常见问题

Q: 为什么扫描不到某些文件？
A: 请检查文件扩展名是否在默认扫描列表中（可通过 --extensions 添加），或文件是否被排除目录过滤。

Q: 扫描结果中包含很多误报怎么办？
A: 你可以通过 --exclude 排除特定目录，或修改 config/settings.py 中的 DEFAULT_EXTENSIONS 和 DEFAULT_EXCLUDE_DIRS 来调整。另外，也可以使用自定义规则替换内置规则。

Q: 扫描过程中出现权限错误？
A: KeyHunter 会静默跳过无法读取的文件，不会中断扫描。若持续遇到问题，请确保你有读取目标文件的权限。

贡献与反馈

欢迎提交 Issue 和 Pull Request。详见 CONTRIBUTING.md。

许可证

本项目采用 MIT 许可证，详情见 LICENSE 文件。

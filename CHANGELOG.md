# 更新日志 / Changelog

## [2.0.0] - 2026-07-14

### 新增 / Added
- 二次发布。
- 支持扫描 20+ 种常见密钥模式。
- 支持自定义规则（命令行 JSON 或外部文件）。
- 支持扩展名过滤、目录排除。
- 支持文本和 JSON 两种报告输出。
- 友好的错误提示，不暴露内部路径或堆栈信息。
- 完整的命令行帮助（-h/--help）。
- 新增 `keyhunter.py` 统一入口，整合扫描与攻击测试。
- 新增渗透测试模块：OAuth 同意钓鱼、npm 供应链投毒、IDE 插件凭证收割、AI Agent 提示词注入。

### 已知限制 / Known Limitations
- 不支持二进制文件扫描（仅文本文件）。
- 未实现并行扫描，大项目扫描速度可能较慢。
- 未提供自动化测试套件。

### 计划 / Planned
- 暂无，欢迎贡献者提出建议和 PR。

---

## [2.0.0] - 2026-07-14

### Added
- Seacond release.
- Support scanning 20+ common secret patterns.
- Support custom rules (JSON string or file).
- Support extension filtering and directory exclusion.
- Support text and JSON report output.
- Friendly error messages, no internal paths or stack traces exposed.
- Complete command-line help (-h/--help).
- New unified entry `keyhunter.py` integrating scanning and attack testing.
- Added penetration testing modules: OAuth consent phishing, npm supply chain backdoor, IDE plugin credential harvesting, AI Agent prompt injection.

### Known Limitations
- Cannot scan binary files (text files only).
- No parallel scanning, may be slow on large projects.
- No automated test suite.

### Planned
- None at the moment, contributions welcome.

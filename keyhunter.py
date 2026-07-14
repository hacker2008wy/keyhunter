#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KeyHunter - 轻量级密钥泄漏扫描器
-------学生的第一个项目--------
----Student's first project----
Usage: python keyhunter.py [path] [--output json] [--extensions .py,.env] [--exclude .git,node_modules] [--patterns '{"pattern":"regex","name":"Name","severity":"HIGH"}'] [--patterns-file patterns.json]
"""

import sys
import argparse
import json
from pathlib import Path

# 将项目根目录加入 sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.scanner import KeyHunter
from utils.reporter import Reporter
from config import settings


def parse_extension_list(raw: str):
    """解析用户输入的扩展名列表，确保以点开头"""
    if not raw:
        return []
    items = [x.strip() for x in raw.split(',') if x.strip()]
    return ['.' + x if not x.startswith('.') else x for x in items]


def parse_exclude_list(raw: str):
    """解析用户输入的排除目录列表"""
    if not raw:
        return []
    return [x.strip() for x in raw.split(',') if x.strip()]


def load_custom_patterns_from_string(raw: str):
    """从 JSON 字符串加载自定义规则，格式: [{"pattern":"regex","name":"Name","severity":"HIGH"}, ...]"""
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"无效的 JSON 格式: {e}")
    if not isinstance(data, list):
        raise ValueError("规则必须是一个列表")
    compiled = []
    for item in data:
        if not isinstance(item, dict):
            raise ValueError("每条规则必须是字典")
        if 'pattern' not in item or 'name' not in item or 'severity' not in item:
            raise ValueError("每条规则必须包含 'pattern', 'name', 'severity' 字段")
        import re
        pattern = re.compile(item['pattern'], re.IGNORECASE)
        severity = item['severity'].upper()
        if severity not in ('HIGH', 'MEDIUM', 'LOW'):
            raise ValueError("severity 必须为 HIGH/MEDIUM/LOW")
        compiled.append((pattern, item['name'], severity))
    return compiled


def load_custom_patterns_from_file(filepath: str):
    """从文件加载自定义规则（JSON 格式）"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return load_custom_patterns_from_string(content)
    except FileNotFoundError:
        raise ValueError(f"文件不存在: {filepath}")
    except Exception as e:
        raise ValueError(f"读取规则文件失败: {e}")


def main():
    parser = argparse.ArgumentParser(
        description='KeyHunter - 轻量级密钥泄漏扫描器（纯标准库）',
        epilog='示例: python keyhunter.py ~/myproject --output json --patterns \'[{"pattern":"sk-.*","name":"Custom Key","severity":"HIGH"}]\''
    )
    parser.add_argument('path', nargs='?', default='.', help='要扫描的目录（默认当前目录）')
    parser.add_argument('--output', '-o', choices=['text', 'json'], default='text', help='报告格式')
    parser.add_argument('--extensions', '-e', help='指定扫描扩展名，逗号分隔，如 .py,.env')
    parser.add_argument('--exclude', help='指定排除目录，逗号分隔，如 .git,node_modules')
    parser.add_argument('--no-default-exts', action='store_true', help='不使用默认扩展名，只使用 --extensions 指定的')
    parser.add_argument('--patterns', help='自定义规则 JSON 字符串，格式: [{"pattern":"regex","name":"Name","severity":"HIGH"}]')
    parser.add_argument('--patterns-file', help='从文件加载自定义规则 JSON')
    parser.add_argument('--no-default-rules', action='store_true', help='不使用内置规则，只使用自定义规则')
    args = parser.parse_args()

    # 加载自定义规则
    custom_patterns = []
    if args.patterns and args.patterns_file:
        print("Error: 不能同时使用 --patterns 和 --patterns-file", file=sys.stderr)
        sys.exit(1)
    try:
        if args.patterns:
            custom_patterns = load_custom_patterns_from_string(args.patterns)
        elif args.patterns_file:
            custom_patterns = load_custom_patterns_from_file(args.patterns_file)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # 确定扩展名
    if args.extensions:
        exts = parse_extension_list(args.extensions)
    elif args.no_default_exts:
        exts = []
    else:
        exts = settings.DEFAULT_EXTENSIONS

    # 确定排除目录
    if args.exclude:
        excludes = parse_exclude_list(args.exclude)
    else:
        excludes = settings.DEFAULT_EXCLUDE_DIRS

    # 创建扫描器
    try:
        hunter = KeyHunter(
            root_dir=args.path,
            exclude_dirs=excludes,
            extensions=exts,
            custom_patterns=custom_patterns,
            use_default_rules=not args.no_default_rules
        )
    except Exception as e:
        print(f"Error: 初始化扫描器失败 - {e}", file=sys.stderr)
        sys.exit(1)

    # 执行扫描
    try:
        hunter.scan()
    except KeyboardInterrupt:
        print("\n[!] 用户中断扫描", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: 扫描过程中发生错误 - {e}", file=sys.stderr)
        sys.exit(1)

    # 生成报告
    reporter = Reporter(hunter.findings)
    if args.output == 'json':
        print(reporter.to_json())
    else:
        print(reporter.to_text(root_path=args.path))


if __name__ == '__main__':
    main()

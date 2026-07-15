#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KeyHunter - 统一入口（扫描 + 攻击测试）
-------学生的第一个项目--------
----Student's first project----
Usage:
    python keyhunter.py scan [path] [options]
    python keyhunter.py attack [module] [options]
    python keyhunter.py list
"""

import sys
import argparse
import json
from pathlib import Path

# 禁用 traceback 打印
sys.tracebacklimit = 0

# 添加项目根目录到 sys.path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

def print_banner():
    banner = """
╔═══════════════════════════════════════════════╗
║  KeyHunter - 密钥泄漏扫描 & 渗透测试套件     ║
║  版本 1.0.0 (2026)                           ║
║  WARNING: 仅限授权测试使用，非法使用必究      ║
╚═══════════════════════════════════════════════╝
"""
    print(banner)

def cmd_scan(args):
    """调用 check 模块进行扫描"""
    try:
        from check.check import main as scan_main
    except ImportError as e:
        print(f"[ERROR] 未找到 check 模块: {e}")
        print("请确保 check/check.py 存在且结构完整。")
        sys.exit(1)
    # 构造 sys.argv
    sys.argv = ['check.py']
    if args.path:
        sys.argv.append(args.path)
    if args.output:
        sys.argv.extend(['--output', args.output])
    if args.extensions:
        sys.argv.extend(['--extensions', args.extensions])
    if args.exclude:
        sys.argv.extend(['--exclude', args.exclude])
    if args.no_default_exts:
        sys.argv.append('--no-default-exts')
    if args.patterns:
        sys.argv.extend(['--patterns', args.patterns])
    if args.patterns_file:
        sys.argv.extend(['--patterns-file', args.patterns_file])
    if args.no_default_rules:
        sys.argv.append('--no-default-rules')
    try:
        scan_main()
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        print(f"[ERROR] 扫描失败: {e}")
        sys.exit(1)

def cmd_attack(args):
    """调用 test 模块进行攻击测试"""
    try:
        from test.test import main as attack_main
    except ImportError as e:
        print(f"[ERROR] 无法加载 test 模块: {e}")
        print("请确保 test/ 目录结构完整，包含 test/test.py 和 test/modules/ 等。")
        print("可参考项目文档创建 test 目录。")
        sys.exit(1)
    # 构造 sys.argv
    sys.argv = ['test.py']
    if args.module:
        sys.argv.extend(['--module', args.module])
    if args.target:
        sys.argv.extend(['--target', args.target])
    if args.output:
        sys.argv.extend(['--output', args.output])
    if args.params:
        sys.argv.extend(['--params', args.params])
    if args.list_modules:
        sys.argv.append('--list')
    try:
        attack_main()
    except SystemExit as e:
        sys.exit(e.code)
    except Exception as e:
        print(f"[ERROR] 攻击模块执行失败: {e}")
        sys.exit(1)

def cmd_list(args):
    """列出所有攻击模块（直接扫描文件，不依赖 __all__）"""
    modules_dir = PROJECT_ROOT / "test" / "modules"
    if not modules_dir.is_dir():
        print("[ERROR] test/modules 目录不存在")
        print("请创建 test/modules/ 目录并放入攻击模块文件（如 oauth_consent.py 等）。")
        sys.exit(1)
    # 收集所有 .py 文件（排除 __init__.py）
    py_files = [f.stem for f in modules_dir.glob("*.py") if f.stem != "__init__"]
    if not py_files:
        print("[WARN] test/modules 目录下未找到任何模块文件")
        print("请至少添加一个模块文件，例如 oauth_consent.py。")
    else:
        print("可用攻击模块列表:")
        for name in sorted(py_files):
            print(f"  - {name}")
        print("\n使用方式: keyhunter.py attack --module <name> --target ...")

def main():
    parser = argparse.ArgumentParser(
        description="KeyHunter - 密钥扫描与渗透测试统一入口",
        epilog="请使用子命令: scan, attack, list"
    )
    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # scan 子命令
    scan_parser = subparsers.add_parser('scan', help='扫描目录中的密钥泄漏')
    scan_parser.add_argument('path', nargs='?', default='.', help='要扫描的目录')
    scan_parser.add_argument('--output', '-o', choices=['text', 'json'], default='text', help='输出格式')
    scan_parser.add_argument('--extensions', '-e', help='指定扫描扩展名，逗号分隔')
    scan_parser.add_argument('--exclude', help='排除目录，逗号分隔')
    scan_parser.add_argument('--no-default-exts', action='store_true', help='不使用默认扩展名')
    scan_parser.add_argument('--patterns', help='自定义规则 JSON 字符串')
    scan_parser.add_argument('--patterns-file', help='从文件加载自定义规则')
    scan_parser.add_argument('--no-default-rules', action='store_true', help='不使用内置规则')

    # attack 子命令
    attack_parser = subparsers.add_parser('attack', help='执行攻击测试模块')
    attack_parser.add_argument('--module', '-m', required=True, help='攻击模块名称')
    attack_parser.add_argument('--target', '-t', help='目标（邮箱、URL等）')
    attack_parser.add_argument('--output', '-o', help='输出目录或文件')
    attack_parser.add_argument('--params', help='额外 JSON 参数')
    attack_parser.add_argument('--list-modules', action='store_true', help='列出所有模块（已弃用，请使用 list 命令）')

    # list 子命令
    list_parser = subparsers.add_parser('list', help='列出所有可用的攻击模块')

    args = parser.parse_args()

    print_banner()

    if args.command == 'scan':
        cmd_scan(args)
    elif args.command == 'attack':
        cmd_attack(args)
    elif args.command == 'list':
        cmd_list(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INFO] 用户中断")
        sys.exit(0)
    except Exception:
        # 全局兜底，不显示 traceback
        print("[FATAL] 发生未预期的错误，请检查输入参数或查看日志。")
        sys.exit(1)

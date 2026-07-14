#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KeyHunter - 统一入口（扫描 + 攻击测试）
Usage:
    python keyhunter.py scan [path] [options]
    python keyhunter.py attack [module] [options]
    python keyhunter.py list
"""

import sys
import argparse
import json
import traceback
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

# 禁用 traceback 打印
sys.tracebacklimit = 0

def safe_import(module_name):
    """安全导入模块，捕获所有异常"""
    try:
        return __import__(module_name, fromlist=[''])
    except Exception as e:
        print(f"[ERROR] Failed to import {module_name}: {e}")
        sys.exit(1)

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
    except ImportError:
        print("[ERROR] 未找到 check 模块，请确保 check/check.py 存在")
        sys.exit(1)
    # 构造 sys.argv 以复用 check 的命令行
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
        # 正常退出
        sys.exit(e.code)
    except Exception as e:
        print(f"[ERROR] 扫描失败: {e}")
        # 不打印 traceback
        sys.exit(1)

def cmd_attack(args):
    """调用 test 模块进行攻击测试"""
    try:
        from test.test import main as attack_main
    except ImportError:
        print("[ERROR] 未找到 test 模块，请确保 test/test.py 存在")
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
    """列出所有攻击模块"""
    try:
        from test.modules import __all__ as module_list
    except ImportError:
        print("[ERROR] 无法加载 test 模块")
        sys.exit(1)
    print("Available attack modules:")
    for name in module_list:
        print(f"  - {name}")
    print("\nUse: keyhunter.py attack --module <name> --target ...")

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
        print("[FATAL] 发生未预期的错误，请检查输入参数。")
        sys.exit(1)

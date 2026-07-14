#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KeyHunter - 渗透测试攻击模块套件
Usage: python test.py --list
       python test.py --module oauth_consent --target victim@example.com
       python test.py --module npm_backdoor --output ./backdoor_package

WARNING: This tool is designed for authorized penetration testing only.
Unauthorized use is illegal. Use at your own risk.
"""

import sys
import argparse
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules import (
    OAuthConsentAttack,
    NpmBackdoorGenerator,
    IdePluginGenerator,
    PromptInjectionGenerator
)
from config.settings import BANNER, DISCLAIMER
from utils.logger import get_logger

logger = get_logger("test_main")

MODULE_MAP = {
    "oauth_consent": OAuthConsentAttack,
    "npm_backdoor": NpmBackdoorGenerator,
    "ide_plugin": IdePluginGenerator,
    "prompt_injection": PromptInjectionGenerator
}


def print_banner():
    print(BANNER)
    print(DISCLAIMER)
    print("-" * 60)


def main():
    print_banner()

    parser = argparse.ArgumentParser(
        description="KeyHunter Penetration Testing Modules",
        epilog="Example: python test.py --module npm_backdoor --output ./evil_package"
    )
    parser.add_argument("--list", action="store_true", help="List all available attack modules")
    parser.add_argument("--module", "-m", choices=MODULE_MAP.keys(), help="Module to execute")
    parser.add_argument("--target", "-t", help="Target email, URL, or other identifier")
    parser.add_argument("--output", "-o", help="Output directory or file path")
    parser.add_argument("--params", help="Additional JSON parameters for the module")
    args = parser.parse_args()

    if args.list:
        print("Available modules:")
        for name, cls in MODULE_MAP.items():
            doc = cls.__doc__ or "No description"
            print(f"  - {name}: {doc.strip()}")
        return

    if not args.module:
        parser.print_help()
        return

    # Load module
    module_cls = MODULE_MAP[args.module]
    params = {}
    if args.params:
        try:
            params = json.loads(args.params)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in --params")
            sys.exit(1)

    # Instantiate and run
    try:
        if args.module == "oauth_consent":
            if not args.target:
                logger.error("--target required for oauth_consent (victim email)")
                sys.exit(1)
            module = module_cls(target_email=args.target, **params)
        elif args.module == "npm_backdoor":
            output_dir = args.output or "./backdoor_package"
            module = module_cls(output_dir=output_dir, **params)
        elif args.module == "ide_plugin":
            output_dir = args.output or "./evil_plugin"
            module = module_cls(output_dir=output_dir, **params)
        elif args.module == "prompt_injection":
            if not args.target:
                logger.error("--target required for prompt_injection (target AI agent URL)")
                sys.exit(1)
            module = module_cls(target_url=args.target, **params)
        else:
            logger.error("Unsupported module")
            sys.exit(1)

        result = module.execute()
        print(json.dumps(result, indent=2))
    except Exception as e:
        logger.error(f"Module execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

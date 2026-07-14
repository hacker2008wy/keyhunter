# -*- coding: utf-8 -*-
"""
配置文件 - 存放默认扩展名、排除目录等
"""

# 默认扫描的文件扩展名
DEFAULT_EXTENSIONS = [
    '.py', '.js', '.jsx', '.ts', '.tsx',
    '.json', '.env', '.txt',
    '.yml', '.yaml', '.conf', '.cfg', '.ini',
    '.properties', '.xml', '.html', '.css', '.vue',
    '.sh', '.bash', '.zsh', '.ps1',
]

# 默认排除的目录
DEFAULT_EXCLUDE_DIRS = [
    '.git', '__pycache__', 'venv', 'env', 'node_modules',
    '.idea', '.vscode', 'dist', 'build', 'coverage',
    '.pytest_cache', '.mypy_cache', '.tox',
]

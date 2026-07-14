# -*- coding: utf-8 -*-
"""
扫描引擎 - 递归遍历目录，匹配密钥规则
"""

import re
from pathlib import Path

from .rules import DEFAULT_PATTERNS


class KeyHunter:
    def __init__(self, root_dir='.', exclude_dirs=None, extensions=None, custom_patterns=None, use_default_rules=True):
        self.root = Path(root_dir).resolve()
        self.exclude_dirs = exclude_dirs or []
        self.extensions = extensions or []
        self.findings = []
        self.patterns = []
        if use_default_rules:
            self.patterns.extend(DEFAULT_PATTERNS)
        if custom_patterns:
            self.patterns.extend(custom_patterns)

    def scan(self):
        """递归扫描目录下的所有文件"""
        self.findings = []
        if not self.root.is_dir():
            raise NotADirectoryError(f"目录不存在: {self.root}")
        for filepath in self.root.rglob('*'):
            if filepath.is_dir():
                continue
            # 检查是否在排除目录中
            if any(excl in filepath.parts for excl in self.exclude_dirs):
                continue
            # 检查扩展名
            if self.extensions:
                if filepath.suffix.lower() not in self.extensions:
                    continue
            self._scan_file(filepath)

    def _scan_file(self, filepath):
        """扫描单个文件，提取匹配项"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except (IOError, PermissionError, UnicodeDecodeError):
            return

        for line_num, line in enumerate(lines, start=1):
            line_stripped = line.strip()
            if not line_stripped:
                continue
            for pattern, name, severity in self.patterns:
                if pattern.search(line):
                    start = max(0, line_num - 4)
                    end = min(len(lines), line_num + 3)
                    context = ''.join(lines[start:end])
                    self.findings.append({
                        'file': str(filepath),
                        'line': line_num,
                        'match': line_stripped,
                        'pattern_name': name,
                        'severity': severity,
                        'context': context
                    })
                    break

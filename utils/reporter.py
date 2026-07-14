# -*- coding: utf-8 -*-
"""
报告生成器 - 支持文本和 JSON 格式
"""

import json


class Reporter:
    def __init__(self, findings):
        self.findings = findings

    def to_text(self, root_path='.'):
        """生成人类可读的文本报告"""
        if not self.findings:
            return f"KeyHunter Scan Report - {root_path}\n" + "="*50 + "\nNo secrets found."

        lines = [
            f"KeyHunter Scan Report - {root_path}",
            "="*50,
            f"Total findings: {len(self.findings)}",
            "-"*50
        ]

        for idx, f in enumerate(self.findings, start=1):
            lines.append(f"\n[{idx}] File: {f['file']}:{f['line']}")
            lines.append(f"    Severity: {f['severity']}")
            lines.append(f"    Pattern: {f['pattern_name']}")
            lines.append(f"    Match: {f['match']}")
            lines.append("    Context (surrounding lines):")
            context_lines = f['context'].splitlines()
            for c in context_lines:
                lines.append(f"        {c}")
            lines.append("-"*30)

        return '\n'.join(lines)

    def to_json(self):
        """生成 JSON 格式报告"""
        return json.dumps(self.findings, indent=2, ensure_ascii=False)

# -*- coding: utf-8 -*-
"""
密钥正则规则库 - 内置常用规则
"""

import re

# 内置规则列表
DEFAULT_PATTERNS = [
    # AI API Keys
    (re.compile(r'sk-[a-zA-Z0-9]{48,}', re.IGNORECASE), 'OpenAI API Key', 'HIGH'),
    (re.compile(r'sk-proj-[a-zA-Z0-9]{32,}', re.IGNORECASE), 'OpenAI Project Key', 'HIGH'),
    (re.compile(r'xai-[a-zA-Z0-9]{48,}', re.IGNORECASE), 'XAI (Grok) Key', 'HIGH'),
    (re.compile(r'claude-[a-zA-Z0-9]{48,}', re.IGNORECASE), 'Anthropic Claude Key', 'HIGH'),
    (re.compile(r'deepseek-[a-zA-Z0-9]{32,}', re.IGNORECASE), 'DeepSeek API Key', 'HIGH'),
    (re.compile(r'mistral-[a-zA-Z0-9]{32,}', re.IGNORECASE), 'Mistral API Key', 'HIGH'),
    (re.compile(r'cohere-[a-zA-Z0-9]{32,}', re.IGNORECASE), 'Cohere API Key', 'HIGH'),
    # Cloud Providers
    (re.compile(r'AKIA[0-9A-Z]{16}', re.IGNORECASE), 'AWS Access Key ID', 'HIGH'),
    (re.compile(r'ASIA[0-9A-Z]{16}', re.IGNORECASE), 'AWS Temporary Access Key', 'HIGH'),
    (re.compile(r'AIza[0-9A-Za-z_-]{35}', re.IGNORECASE), 'Google API Key', 'HIGH'),
    (re.compile(r'AccountKey=[a-zA-Z0-9+/]+=', re.IGNORECASE), 'Azure Storage Account Key', 'HIGH'),
    # Git Hosting
    (re.compile(r'gh[pousr]_[a-zA-Z0-9]{36,}', re.IGNORECASE), 'GitHub Token', 'HIGH'),
    (re.compile(r'github_pat_[a-zA-Z0-9]{22,}', re.IGNORECASE), 'GitHub Personal Access Token', 'HIGH'),
    (re.compile(r'glpat-[a-zA-Z0-9\-_]{20,}', re.IGNORECASE), 'GitLab Personal Access Token', 'HIGH'),
    (re.compile(r'gitlab_pat_[a-zA-Z0-9]{20,}', re.IGNORECASE), 'GitLab PAT', 'HIGH'),
    # Messaging
    (re.compile(r'xox[baprs]-[0-9a-zA-Z]{10,}', re.IGNORECASE), 'Slack Token', 'HIGH'),
    (re.compile(r'sk-[a-z]{2,}-[a-zA-Z0-9]{20,}', re.IGNORECASE), 'SendGrid API Key', 'HIGH'),
    # JWT
    (re.compile(r'eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+', re.IGNORECASE), 'JWT Token', 'MEDIUM'),
    # Generic Secrets
    (re.compile(r'(api|secret|token|key|auth)[\s]*[:=][\s]*["\']?([a-zA-Z0-9_\-/+=]{32,})', re.IGNORECASE), 'Generic Secret Key', 'MEDIUM'),
    # Passwords
    (re.compile(r'password[\s]*[:=][\s]*["\']?([^"\'\s]{8,})', re.IGNORECASE), 'Potential Password', 'LOW'),
    # Database URLs
    (re.compile(r'(postgresql|mysql|mongodb|redis|sqlite)://[a-zA-Z0-9_]+:[^@]+@', re.IGNORECASE), 'Database Connection String', 'HIGH'),
]

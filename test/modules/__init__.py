# -*- coding: utf-8 -*-
"""渗透测试模块集合"""

from .oauth_consent import OAuthConsentAttack
from .npm_backdoor import NpmBackdoorGenerator
from .ide_plugin import IdePluginGenerator
from .prompt_injection import PromptInjectionGenerator

__all__ = [
    'OAuthConsentAttack',
    'NpmBackdoorGenerator',
    'IdePluginGenerator',
    'PromptInjectionGenerator'
]

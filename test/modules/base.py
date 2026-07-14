# -*- coding: utf-8 -*-
"""模块基类"""

import json
from abc import ABC, abstractmethod
from datetime import datetime

from utils.logger import get_logger


class AttackModule(ABC):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.logger = get_logger(self.__class__.__name__)
        self.timestamp = datetime.utcnow().isoformat()
        self.result = {
            "module": self.__class__.__name__,
            "timestamp": self.timestamp,
            "success": False,
            "data": {},
            "error": None
        }

    @abstractmethod
    def execute(self):
        """执行攻击，返回结果字典"""
        pass

    def _log(self, level, msg):
        getattr(self.logger, level)(msg)

    def _dump_result(self):
        return self.result

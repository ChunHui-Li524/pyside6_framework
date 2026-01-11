# -*- coding: utf-8 -*-
"""
日志管理器模块
"""
import logging
import os
import time
from logging.handlers import RotatingFileHandler
from typing import Optional, Dict

from PySide6.QtCore import QObject

from .qt_handler import QtLogHandler


class LogManager:
    """日志管理器，负责管理不同类型的日志器"""
    
    def __init__(self, log_dir: Optional[str] = None):
        """初始化日志管理器
        
        Args:
            log_dir: 日志目录，默认为None，会使用默认目录
        """
        super().__init__()
        
        # 设置日志目录
        if log_dir is None:
            log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        self.log_dir = log_dir
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 初始化Qt日志处理器
        self.qt_handler = QtLogHandler()
        
        # 存储测试日志器
        self.test_loggers: Dict[str, logging.Logger] = {}
        
        # 配置主日志
        self.main_logger = self._setup_main_logger()
    
    def _setup_main_logger(self) -> logging.Logger:
        """设置主日志器
        
        Returns:
            logging.Logger: 主日志器
        """
        logger = logging.getLogger('main')
        logger.setLevel(logging.DEBUG)
        
        # 清除现有的处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 添加控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # 添加文件处理器（轮转）
        main_log_path = os.path.join(self.log_dir, 'main.log')
        file_handler = RotatingFileHandler(
            main_log_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,  # 保留5个备份
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # 添加Qt处理器
        logger.addHandler(self.qt_handler)
        
        return logger
    
    def get_test_logger(self, test_name: str) -> logging.Logger:
        """获取测试日志器
        
        Args:
            test_name: 测试名称
        
        Returns:
            logging.Logger: 测试日志器
        """
        if test_name in self.test_loggers:
            return self.test_loggers[test_name]
        
        logger = logging.getLogger(f'test.{test_name}')
        logger.setLevel(logging.DEBUG)
        
        # 清除现有的处理器
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 创建测试日志目录
        test_log_dir = os.path.join(self.log_dir, 'tests')
        os.makedirs(test_log_dir, exist_ok=True)
        
        # 添加文件处理器（每个测试一个文件）
        test_log_path = os.path.join(test_log_dir, f'{test_name}_{time.strftime("%Y%m%d_%H%M%S")}.log')
        file_handler = RotatingFileHandler(
            test_log_path,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=3,  # 保留3个备份
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # 添加Qt处理器
        logger.addHandler(self.qt_handler)
        
        self.test_loggers[test_name] = logger
        return logger
    
    def get_main_logger(self) -> logging.Logger:
        """获取主日志器
        
        Returns:
            logging.Logger: 主日志器
        """
        return self.main_logger

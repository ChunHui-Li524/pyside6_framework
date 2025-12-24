import logging
import os
from datetime import datetime
import sys
from utils.singleton import SingletonBase

class LogManager(SingletonBase):
    """
    日志管理器，用于统一管理应用程序的日志输出
    支持控制台和文件输出，可配置日志级别
    """
    
    def __init__(self):
        """初始化日志管理器"""
        if hasattr(self, 'initialized'):
            return
            
        self.logger = logging.getLogger('PySide6Framework')
        self.logger.setLevel(logging.DEBUG)  # 默认设置为DEBUG级别
        
        # 创建logs目录
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'logs')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        
        # 清除已有的handler
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)
        
        # 添加控制台handler
        self._add_console_handler()
        
        # 添加文件handler
        self._add_file_handler()
        
        self.initialized = True
    
    def _add_console_handler(self):
        """添加控制台输出handler"""
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)  # 控制台默认显示INFO及以上级别
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        
        self.logger.addHandler(console_handler)
    
    def _add_file_handler(self):
        """添加文件输出handler"""
        # 生成日志文件名（按日期）
        today = datetime.now().strftime('%Y%m%d')
        log_file = os.path.join(self.log_dir, f'app_{today}.log')
        
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)  # 文件记录所有级别的日志
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(message)s')
        file_handler.setFormatter(formatter)
        
        self.logger.addHandler(file_handler)
    
    def set_level(self, level):
        """设置日志级别
        
        Args:
            level: 日志级别，可以是字符串('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')或对应的数值
        """
        if isinstance(level, str):
            level = level.upper()
            level_map = {
                'DEBUG': logging.DEBUG,
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'WARN': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL
            }
            level = level_map.get(level, logging.INFO)
        
        self.logger.setLevel(level)
    
    def debug(self, message):
        """记录DEBUG级别日志"""
        self.logger.debug(message)
    
    def info(self, message):
        """记录INFO级别日志"""
        self.logger.info(message)
    
    def warning(self, message):
        """记录WARNING级别日志"""
        self.logger.warning(message)
    
    def error(self, message):
        """记录ERROR级别日志"""
        self.logger.error(message)
    
    def critical(self, message):
        """记录CRITICAL级别日志"""
        self.logger.critical(message)

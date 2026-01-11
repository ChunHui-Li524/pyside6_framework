# Log Manager模块初始化文件
"""
日志管理器模块，提供自定义的日志管理功能
"""

from .qt_handler import QtLogHandler
from .log_manager import LogManager

# 创建全局日志管理器实例
log_manager = LogManager()


def connect_log_text_signal(slot: callable) -> None:
    """连接日志文本信号到槽函数
    
    Args:
        slot: 槽函数，接收一个字符串参数
    """
    log_manager.qt_handler.connect_log_text_signal(slot)


def connect_log_record_signal(slot: callable) -> None:
    """连接日志记录信号到槽函数
    
    Args:
        slot: 槽函数，接收一个LogRecord参数
    """
    log_manager.qt_handler.connect_log_record_signal(slot)


def get_main_logger() -> logging.Logger:
    """获取主日志器
    
    Returns:
        logging.Logger: 主日志器
    """
    return log_manager.get_main_logger()


def get_test_logger(test_name: str) -> logging.Logger:
    """获取测试日志器
    
    Args:
        test_name: 测试名称
    
    Returns:
        logging.Logger: 测试日志器
    """
    return log_manager.get_test_logger(test_name)

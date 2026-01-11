# -*- coding: utf-8 -*-
"""
Qt日志处理器模块
"""
import logging
from typing import Optional

from PySide6.QtCore import QObject, Signal


class QLogSignals(QObject):
    """Qt日志信号类"""
    logRecordEmitted = Signal(logging.LogRecord)
    logTextEmitted = Signal(str)


class QtLogHandler(logging.Handler):
    """Qt日志处理器，通过信号发送日志"""
    
    def __init__(self, formatter: Optional[logging.Formatter] = None):
        """初始化Qt日志处理器
        
        Args:
            formatter: 日志格式化器，默认为None
        """
        logging.Handler.__init__(self)
        if formatter is None:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.setFormatter(formatter)
        self.signals = QLogSignals()
    
    def emit(self, record: logging.LogRecord) -> None:
        """处理日志记录，通过信号发送出去
        
        Args:
            record: 日志记录对象
        """
        # 发送完整的LogRecord对象
        self.signals.logRecordEmitted.emit(record)
        # 发送格式化后的日志文本
        log_text = self.format(record)
        self.signals.logTextEmitted.emit(log_text)

    def connect_log_text_signal(self, slot: callable) -> None:
        """连接日志文本信号到槽函数
        
        Args:
            slot: 槽函数，接收一个字符串参数
        """
        self.signals.logTextEmitted.connect(slot)

    def connect_log_record_signal(self, slot: callable) -> None:
        """连接日志记录信号到槽函数
        
        Args:
            slot: 槽函数，接收一个LogRecord参数
        """
        self.signals.logRecordEmitted.connect(slot)

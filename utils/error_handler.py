import traceback
from core.log_manager import LogManager
from utils.singleton import SingletonBase

class ErrorHandler(SingletonBase):
    """
    错误处理器，用于统一处理应用程序的异常和错误
    提供错误捕获、日志记录和异常转换功能
    """
    
    def __init__(self):
        """初始化错误处理器"""
        if hasattr(self, 'initialized'):
            return
            
        self.logger = LogManager()
        self.initialized = True
    
    def handle_exception(self, exception, context="", show_traceback=True):
        """处理异常
        
        Args:
            exception: 异常对象
            context: 异常上下文描述
            show_traceback: 是否显示完整堆栈跟踪
            
        Returns:
            格式化的错误消息
        """
        error_type = exception.__class__.__name__
        error_message = str(exception)
        
        # 构建错误消息
        if context:
            full_message = f"{context} - {error_type}: {error_message}"
        else:
            full_message = f"{error_type}: {error_message}"
        
        # 记录错误日志
        self.logger.error(full_message)
        
        # 如果需要，记录堆栈跟踪
        if show_traceback:
            traceback_str = traceback.format_exc()
            self.logger.error(f"堆栈跟踪:\n{traceback_str}")
        
        return full_message
    
    def catch_exception(self, func):
        """异常捕获装饰器
        
        Args:
            func: 要装饰的函数
            
        Returns:
            装饰后的函数
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                context = f"执行 {func.__name__} 时出错"
                self.handle_exception(e, context)
                # 返回None或默认值，取决于函数的预期返回值
                return None
        
        # 保留原函数的元数据
        wrapper.__name__ = func.__name__
        wrapper.__doc__ = func.__doc__
        wrapper.__module__ = func.__module__
        
        return wrapper
    
    def create_custom_error(self, message, error_type="CustomError"):
        """创建自定义错误
        
        Args:
            message: 错误消息
            error_type: 错误类型名称
            
        Returns:
            自定义异常类
        """
        CustomErrorClass = type(error_type, (Exception,), {})
        return CustomErrorClass(message)
    
    def format_error_details(self, exception):
        """格式化错误详情
        
        Args:
            exception: 异常对象
            
        Returns:
            包含详细错误信息的字典
        """
        return {
            'type': exception.__class__.__name__,
            'message': str(exception),
            'traceback': traceback.format_tb(exception.__traceback__)
        }
    
    def is_critical_error(self, exception):
        """判断是否为严重错误
        
        Args:
            exception: 异常对象
            
        Returns:
            是否为严重错误
        """
        # 定义严重错误类型列表
        critical_errors = [
            SystemExit,
            KeyboardInterrupt,
            MemoryError,
            ImportError,
            NameError,
            AttributeError,
            TypeError,
            ValueError
        ]
        
        for error_type in critical_errors:
            if isinstance(exception, error_type):
                return True
        
        return False
    
    def handle_ui_error(self, exception, parent_widget=None):
        """处理UI相关错误
        
        Args:
            exception: 异常对象
            parent_widget: 父窗口组件（用于显示错误对话框）
            
        Returns:
            格式化的错误消息
        """
        # 这里可以添加特定于UI的错误处理逻辑
        # 例如显示一个Qt错误对话框
        
        # 先调用通用错误处理
        error_message = self.handle_exception(exception, "UI操作错误")
        
        # 如果提供了父窗口组件，可以在这里添加显示对话框的逻辑
        # 由于这是工具模块，我们不直接导入Qt组件
        # 实际使用时可以在调用处处理对话框显示
        
        return error_message

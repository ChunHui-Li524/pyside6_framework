from core.log_manager import LogManager

class BaseService:
    """
    服务基类，所有服务都应继承此类
    提供通用的服务接口和日志功能
    """
    
    def __init__(self):
        """初始化基础服务"""
        self.logger = LogManager()
        self.logger.debug(f"初始化服务: {self.__class__.__name__}")
        
    def initialize(self):
        """服务初始化方法，子类可重写此方法进行初始化操作"""
        self.logger.debug(f"服务初始化: {self.__class__.__name__}")
        return True
    
    def shutdown(self):
        """服务关闭方法，子类可重写此方法进行清理操作"""
        self.logger.debug(f"服务关闭: {self.__class__.__name__}")
        return True
    
    def get_name(self):
        """获取服务名称"""
        return self.__class__.__name__

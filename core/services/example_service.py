from core.services.base_service import BaseService

class ExampleService(BaseService):
    """
    示例服务类，展示如何实现具体的业务逻辑服务
    """
    
    def __init__(self):
        """初始化示例服务"""
        super().__init__()
        self.data_cache = {}
        
    def initialize(self):
        """初始化示例服务"""
        super().initialize()
        # 进行服务特定的初始化操作
        self.logger.info("示例服务初始化完成")
        return True
    
    def get_data(self, key):
        """获取数据示例方法
        
        Args:
            key: 数据键
            
        Returns:
            获取的数据，如果不存在则返回None
        """
        self.logger.debug(f"获取数据: {key}")
        return self.data_cache.get(key)
    
    def set_data(self, key, value):
        """设置数据示例方法
        
        Args:
            key: 数据键
            value: 数据值
        """
        self.logger.debug(f"设置数据: {key} = {value}")
        self.data_cache[key] = value
        return True
    
    def clear_cache(self):
        """清空数据缓存"""
        self.logger.debug("清空数据缓存")
        self.data_cache.clear()
        return True
    
    def shutdown(self):
        """关闭示例服务"""
        self.clear_cache()
        super().shutdown()
        return True

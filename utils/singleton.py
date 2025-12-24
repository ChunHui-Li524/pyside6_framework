class SingletonMeta(type):
    """
    单例模式元类
    用于创建单例类的元类，确保类只有一个实例
    """
    
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        """
        当调用类创建实例时调用
        
        Args:
            cls: 类对象
            *args: 位置参数
            **kwargs: 关键字参数
            
        Returns:
            类的唯一实例
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class SingletonBase(metaclass=SingletonMeta):
    """
    单例模式基类
    所有需要使用单例模式的类都可以继承此类
    """
    
    def __init__(self):
        """
        初始化方法
        注意：单例类的__init__方法会在每次获取实例时调用，
        但只会创建一个实例对象
        """
        pass
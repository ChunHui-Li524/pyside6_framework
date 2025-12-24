from PySide6.QtCore import QObject, Signal
from core.log_manager import LogManager
from utils.singleton import SingletonBase

class SignalManager(QObject, SingletonBase):
    """
    信号管理器，提供全局的信号通信机制
    允许不同模块和组件之间通过信号进行通信，无需直接引用
    """
    
    def __init__(self):
        """初始化信号管理器"""
        if hasattr(self, 'initialized'):
            return
            
        super().__init__()
        self.logger = LogManager()
        self._custom_signals = {}
        self.logger.info("信号管理器初始化完成")
        self.initialized = True
        
        # 预定义的全局信号
        # UI相关信号
        self.ui_theme_changed = Signal(str)  # 主题变化信号
        self.ui_language_changed = Signal(str)  # 语言变化信号
        self.ui_font_size_changed = Signal(int)  # 字体大小变化信号
        
        # 应用程序相关信号
        self.app_initialized = Signal()  # 应用初始化完成信号
        self.app_shutdown = Signal()  # 应用关闭信号
        self.app_status_changed = Signal(str)  # 应用状态变化信号
        
        # 数据相关信号
        self.data_updated = Signal(str, object)  # 数据更新信号
        self.data_deleted = Signal(str, object)  # 数据删除信号
        self.data_loaded = Signal(str, object)  # 数据加载信号
        
        # 错误相关信号
        self.error_occurred = Signal(str, Exception)  # 错误发生信号
        self.warning_occurred = Signal(str, str)  # 警告发生信号
        
        # 用户操作相关信号
        self.user_logged_in = Signal(str)  # 用户登录信号
        self.user_logged_out = Signal()  # 用户登出信号
        self.user_permission_changed = Signal(list)  # 用户权限变化信号
    
    def register_signal(self, signal_name):
        """注册自定义信号
        
        Args:
            signal_name: 信号名称
            
        Returns:
            创建的信号对象，如果信号已存在则返回现有信号
        """
        if signal_name in self._custom_signals:
            self.logger.warning(f"信号已存在: {signal_name}")
            return self._custom_signals[signal_name]
        
        # 创建新的信号
        signal = Signal(object)
        self._custom_signals[signal_name] = signal
        self.logger.debug(f"注册自定义信号: {signal_name}")
        return signal
    
    def get_signal(self, signal_name):
        """获取信号
        
        Args:
            signal_name: 信号名称
            
        Returns:
            信号对象，如果信号不存在则返回None
        """
        if signal_name in self._custom_signals:
            return self._custom_signals[signal_name]
        
        # 检查是否为预定义信号
        if hasattr(self, signal_name):
            return getattr(self, signal_name)
        
        self.logger.warning(f"信号不存在: {signal_name}")
        return None
    
    def emit_signal(self, signal_name, data=None):
        """发射信号
        
        Args:
            signal_name: 信号名称
            data: 要传递的数据
            
        Returns:
            是否成功发射信号
        """
        signal = self.get_signal(signal_name)
        if signal:
            try:
                if data is not None:
                    signal.emit(data)
                else:
                    signal.emit()
                self.logger.debug(f"发射信号: {signal_name}, 数据: {data}")
                return True
            except Exception as e:
                self.logger.error(f"发射信号时出错: {signal_name}, 错误: {str(e)}")
                return False
        return False
    
    def connect_signal(self, signal_name, slot):
        """连接信号到槽函数
        
        Args:
            signal_name: 信号名称
            slot: 要连接的槽函数
            
        Returns:
            是否连接成功
        """
        signal = self.get_signal(signal_name)
        if signal:
            try:
                signal.connect(slot)
                self.logger.debug(f"连接信号: {signal_name} 到槽函数: {slot.__name__}")
                return True
            except Exception as e:
                self.logger.error(f"连接信号时出错: {signal_name}, 错误: {str(e)}")
                return False
        return False
    
    def disconnect_signal(self, signal_name, slot=None):
        """断开信号连接
        
        Args:
            signal_name: 信号名称
            slot: 要断开的槽函数，如果为None则断开所有连接
            
        Returns:
            是否断开成功
        """
        signal = self.get_signal(signal_name)
        if signal:
            try:
                if slot:
                    signal.disconnect(slot)
                    self.logger.debug(f"断开信号: {signal_name} 与槽函数: {slot.__name__} 的连接")
                else:
                    signal.disconnect()
                    self.logger.debug(f"断开信号: {signal_name} 的所有连接")
                return True
            except Exception as e:
                self.logger.error(f"断开信号时出错: {signal_name}, 错误: {str(e)}")
                return False
        return False
    
    def list_signals(self):
        """列出所有已注册的信号
        
        Returns:
            信号名称列表
        """
        # 获取预定义信号
        predefined_signals = []
        for attr_name in dir(self):
            if not attr_name.startswith('_') and isinstance(getattr(self, attr_name), Signal):
                predefined_signals.append(attr_name)
        
        # 获取自定义信号
        custom_signals = list(self._custom_signals.keys())
        
        return {
            'predefined_signals': predefined_signals,
            'custom_signals': custom_signals
        }
    
    def is_signal_registered(self, signal_name):
        """检查信号是否已注册
        
        Args:
            signal_name: 信号名称
            
        Returns:
            信号是否已注册
        """
        # 检查自定义信号
        if signal_name in self._custom_signals:
            return True
        
        # 检查预定义信号
        if hasattr(self, signal_name) and isinstance(getattr(self, signal_name), Signal):
            return True
        
        return False
    
    def unregister_signal(self, signal_name):
        """注销自定义信号
        
        Args:
            signal_name: 信号名称
            
        Returns:
            是否注销成功
        """
        if signal_name in self._custom_signals:
            try:
                # 断开所有连接
                signal = self._custom_signals[signal_name]
                try:
                    signal.disconnect()
                except:
                    pass  # 忽略可能的断开连接错误
                
                # 删除信号
                del self._custom_signals[signal_name]
                self.logger.debug(f"注销自定义信号: {signal_name}")
                return True
            except Exception as e:
                self.logger.error(f"注销信号时出错: {signal_name}, 错误: {str(e)}")
                return False
        
        # 不能注销预定义信号
        if hasattr(self, signal_name) and isinstance(getattr(self, signal_name), Signal):
            self.logger.warning(f"不能注销预定义信号: {signal_name}")
            return False
        
        self.logger.warning(f"信号不存在: {signal_name}")
        return False
    
    def shutdown(self):
        """关闭信号管理器，清理所有信号连接"""
        self.logger.info("信号管理器关闭中")
        
        # 断开所有自定义信号
        for signal_name in list(self._custom_signals.keys()):
            self.unregister_signal(signal_name)
        
        # 断开所有预定义信号
        for attr_name in dir(self):
            if not attr_name.startswith('_') and isinstance(getattr(self, attr_name), Signal):
                try:
                    signal = getattr(self, attr_name)
                    signal.disconnect()
                except:
                    pass  # 忽略可能的断开连接错误
        
        self.logger.info("信号管理器已关闭")

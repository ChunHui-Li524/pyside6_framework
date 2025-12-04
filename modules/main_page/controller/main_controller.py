from PySide6.QtCore import QObject, Signal, Slot
from core.log_manager import LogManager
from core.services import ExampleService

class MainController(QObject):
    """
    主页面控制器，负责处理主页面的业务逻辑
    使用MVC模式，连接视图和服务层
    """
    
    # 定义信号
    data_updated = Signal(str, object)  # 数据更新信号
    status_changed = Signal(str)        # 状态改变信号
    
    def __init__(self, view):
        """初始化主控制器
        
        Args:
            view: 主页面视图对象
        """
        super().__init__()
        self.view = view
        self.logger = LogManager()
        self.example_service = ExampleService()
        
        # 连接视图信号到控制器槽函数
        self.view.action_triggered.connect(self.handle_action)
        self.view.data_requested.connect(self.handle_data_request)
        
        # 连接控制器信号到视图槽函数
        self.data_updated.connect(self.view.update_data)
        self.status_changed.connect(self.view.update_status)
        
        # 初始化服务
        self.example_service.initialize()
        self.logger.info("主控制器初始化完成")
    
    @Slot(str, object)
    def handle_action(self, action_type, data=None):
        """处理视图触发的动作
        
        Args:
            action_type: 动作类型
            data: 相关数据
        """
        self.logger.debug(f"处理动作: {action_type}, 数据: {data}")
        
        try:
            if action_type == 'initialize':
                # 初始化操作
                self._initialize_page()
            elif action_type == 'save_data':
                # 保存数据
                if data and isinstance(data, dict) and 'key' in data and 'value' in data:
                    success = self.example_service.set_data(data['key'], data['value'])
                    if success:
                        self.status_changed.emit(f"数据已保存: {data['key']}")
                    else:
                        self.status_changed.emit("保存数据失败")
            elif action_type == 'clear_data':
                # 清除数据
                self.example_service.clear_cache()
                self.status_changed.emit("数据缓存已清除")
                self.data_updated.emit('all', None)
            else:
                self.logger.warning(f"未知的动作类型: {action_type}")
                self.status_changed.emit(f"未知操作: {action_type}")
        except Exception as e:
            self.logger.error(f"处理动作时出错: {str(e)}")
            self.status_changed.emit(f"错误: {str(e)}")
    
    @Slot(str)
    def handle_data_request(self, data_key):
        """处理数据请求
        
        Args:
            data_key: 请求的数据键
        """
        self.logger.debug(f"请求数据: {data_key}")
        
        try:
            if data_key == 'all':
                # 请求所有数据
                all_data = self.example_service.data_cache
                self.data_updated.emit('all', all_data)
            else:
                # 请求特定数据
                data = self.example_service.get_data(data_key)
                self.data_updated.emit(data_key, data)
        except Exception as e:
            self.logger.error(f"获取数据时出错: {str(e)}")
            self.status_changed.emit(f"获取数据失败: {str(e)}")
    
    def _initialize_page(self):
        """初始化页面数据"""
        self.logger.debug("初始化页面数据")
        # 设置一些初始数据
        self.example_service.set_data('app_name', 'PySide6 Framework')
        self.example_service.set_data('version', '1.0.0')
        self.example_service.set_data('author', 'Developer')
        
        # 更新视图
        self.status_changed.emit("页面初始化完成")
        self.handle_data_request('all')
    
    def shutdown(self):
        """关闭控制器，释放资源"""
        self.logger.info("主控制器关闭")
        self.example_service.shutdown()

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import QTranslator, Qt

# 导入框架模块
from core.log_manager import LogManager
from core.services import ExampleService
from modules.main_page import MainController, MainView
from utils.config_manager import ConfigManager
from utils.error_handler import ErrorHandler
from qt_enhance.signal_manager import SignalManager


class App(QMainWindow):
    """
    应用程序主窗口类
    管理整个应用程序的生命周期和UI
    """
    
    def __init__(self):
        super().__init__()
        
        # 初始化框架组件
        self.logger = LogManager()
        self.config_manager = ConfigManager()
        self.error_handler = ErrorHandler()
        self.signal_manager = SignalManager()
        
        # 记录应用启动日志
        self.logger.info("应用程序开始启动")
        
        # 设置窗口属性
        self.setWindowTitle("PySide6 框架应用")
        self.resize(1024, 768)
        
        # 初始化服务
        self.example_service = None
        
        # 初始化控制器和视图
        self.main_controller = None
        self.main_view = None
        
        # 设置应用样式
        self._setup_style()
        
        # 设置信号连接
        self._setup_signals()
        
        # 初始化UI
        self._init_ui()
        
        # 加载配置
        self._load_configuration()
        
        # 初始化服务
        self._init_services()
        
        # 初始化完成
        self.logger.info("应用程序初始化完成")
        self.signal_manager.emit_signal("app_initialized")
    
    def _setup_style(self):
        """设置应用程序样式"""
        try:
            # 设置默认样式
            app.setStyle("Fusion")
            
            # 可以在这里加载自定义样式表
            # self.setStyleSheet("...")
            
            self.logger.debug("应用样式设置完成")
        except Exception as e:
            self.logger.error(f"设置应用样式时出错: {str(e)}")
    
    def _setup_signals(self):
        """设置全局信号连接"""
        try:
            # 连接错误信号
            self.signal_manager.connect_signal("error_occurred", self._handle_error)
            
            # 连接状态变化信号
            self.signal_manager.connect_signal("app_status_changed", self._update_status)
            
            self.logger.debug("全局信号连接设置完成")
        except Exception as e:
            self.logger.error(f"设置全局信号时出错: {str(e)}")
    
    def _init_ui(self):
        """初始化用户界面"""
        try:
            # 创建中心部件
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            
            # 创建主布局
            main_layout = QVBoxLayout(central_widget)
            
            # 初始化主页面控制器和视图
            self.main_view = MainView()
            self.main_controller = MainController(self.main_view)
            
            # 添加主页面视图到布局
            main_layout.addWidget(self.main_view)
            main_layout.setContentsMargins(0, 0, 0, 0)
            
            self.logger.debug("UI初始化完成")
        except Exception as e:
            self.logger.error(f"初始化UI时出错: {str(e)}")
            raise
    
    def _load_configuration(self):
        """加载应用配置"""
        try:
            # 加载配置文件
            config_path = self.config_manager.get_config_path()
            self.logger.info(f"正在加载配置: {config_path}")
            
            # 尝试获取窗口大小配置
            window_size = self.config_manager.get("application.window_size")
            if window_size and len(window_size) == 2:
                self.resize(window_size[0], window_size[1])
            
            # 尝试获取窗口位置配置
            window_pos = self.config_manager.get("application.window_position")
            if window_pos and len(window_pos) == 2:
                self.move(window_pos[0], window_pos[1])
            
            # 尝试获取主题配置
            theme = self.config_manager.get("application.theme", "light")
            self.signal_manager.emit_signal("ui_theme_changed", theme)
            
            self.logger.debug("配置加载完成")
        except Exception as e:
            self.logger.error(f"加载配置时出错: {str(e)}")
            # 使用默认配置继续运行
    
    def _init_services(self):
        """初始化服务"""
        try:
            # 初始化示例服务
            self.example_service = ExampleService()
            self.logger.info("示例服务初始化完成")
            
            # 这里可以初始化其他服务
            
        except Exception as e:
            self.logger.error(f"初始化服务时出错: {str(e)}")
            raise
    
    def _handle_error(self, context, exception):
        """处理错误"""
        self.logger.error(f"应用错误 - 上下文: {context}, 错误: {str(exception)}")
        # 这里可以实现更复杂的错误处理逻辑，如显示错误对话框
    
    def _update_status(self, status):
        """更新应用状态"""
        self.logger.info(f"应用状态更新: {status}")
        # 可以在这里实现状态显示逻辑
    
    def closeEvent(self, event):
        """处理窗口关闭事件"""
        self.logger.info("应用程序开始关闭")
        
        # 保存配置
        try:
            # 保存窗口大小
            self.config_manager.set("application.window_size", [self.width(), self.height()])
            # 保存窗口位置
            self.config_manager.set("application.window_position", [self.x(), self.y()])
            # 保存配置到文件
            self.config_manager.save_config()
            self.logger.debug("配置保存完成")
        except Exception as e:
            self.logger.error(f"保存配置时出错: {str(e)}")
        
        # 关闭服务
        try:
            if self.example_service:
                self.example_service.shutdown()
            
            # 关闭信号管理器
            self.signal_manager.shutdown()
            
            self.logger.debug("服务关闭完成")
        except Exception as e:
            self.logger.error(f"关闭服务时出错: {str(e)}")
        
        # 发送应用关闭信号
        self.signal_manager.emit_signal("app_shutdown")
        
        # 记录应用关闭日志
        self.logger.info("应用程序关闭完成")
        
        # 允许窗口关闭
        event.accept()


def main():
    """主函数，应用程序入口"""
    
    # 创建全局异常处理器
    def excepthook(exctype, value, traceback):
        """全局异常处理"""
        # 记录异常信息
        logger = LogManager()
        logger.critical(f"未捕获的异常: {exctype.__name__}: {value}", exc_info=True)
        
        # 显示错误信息
        error_handler = ErrorHandler()
        error_handler.handle_exception(exctype, value, traceback)
        
        # 调用原始的异常处理器
        sys.__excepthook__(exctype, value, traceback)
    
    # 设置全局异常处理器
    sys.excepthook = excepthook
    
    # 创建应用实例
    global app
    app = QApplication(sys.argv)
    
    # 设置应用信息
    app.setApplicationName("PySide6 Framework")
    app.setApplicationVersion("1.0.0")
    
    # 尝试加载翻译文件
    try:
        translator = QTranslator()
        # 这里可以加载语言翻译文件
        # translator.load("translations/zh_CN.qm")
        # app.installTranslator(translator)
    except Exception as e:
        print(f"加载翻译文件时出错: {str(e)}")
    
    # 创建并显示主窗口
    window = App()
    window.show()
    
    # 运行应用
    sys.exit(app.exec())


if __name__ == "__main__":
    main()

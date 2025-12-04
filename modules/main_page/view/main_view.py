from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QGroupBox,
                             QFormLayout, QMessageBox)
from PySide6.QtCore import Signal, Slot, Qt
from core.log_manager import LogManager

class MainView(QWidget):
    """
    主页面视图类，负责展示UI界面
    使用PySide6组件构建界面，通过信号与控制器通信
    """
    
    # 定义信号
    action_triggered = Signal(str, object)  # 触发动作信号
    data_requested = Signal(str)            # 请求数据信号
    
    def __init__(self, parent=None):
        """初始化主页面视图
        
        Args:
            parent: 父窗口组件
        """
        super().__init__(parent)
        self.logger = LogManager()
        self.init_ui()
        self.logger.info("主视图初始化完成")
    
    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle("PySide6 Framework")
        self.setMinimumSize(800, 600)
        
        # 主布局
        main_layout = QVBoxLayout(self)
        
        # 标题区域
        title_label = QLabel("PySide6 框架示例")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        main_layout.addWidget(title_label)
        
        # 数据操作区域
        data_group = QGroupBox("数据操作")
        data_layout = QFormLayout()
        
        self.key_input = QLineEdit()
        self.value_input = QLineEdit()
        
        data_layout.addRow("键:", self.key_input)
        data_layout.addRow("值:", self.value_input)
        
        # 按钮布局
        buttons_layout = QHBoxLayout()
        
        self.save_button = QPushButton("保存数据")
        self.save_button.clicked.connect(self.on_save_clicked)
        
        self.load_button = QPushButton("加载数据")
        self.load_button.clicked.connect(self.on_load_clicked)
        
        self.clear_button = QPushButton("清除缓存")
        self.clear_button.clicked.connect(self.on_clear_clicked)
        
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.load_button)
        buttons_layout.addWidget(self.clear_button)
        
        data_layout.addRow(buttons_layout)
        data_group.setLayout(data_layout)
        main_layout.addWidget(data_group)
        
        # 数据显示区域
        display_group = QGroupBox("数据显示")
        display_layout = QVBoxLayout()
        
        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        self.data_display.setStyleSheet("font-family: Consolas, monospace;")
        
        display_layout.addWidget(self.data_display)
        display_group.setLayout(display_layout)
        main_layout.addWidget(display_group)
        
        # 状态区域
        self.status_label = QLabel("就绪")
        self.status_label.setAlignment(Qt.AlignLeft)
        self.status_label.setStyleSheet("color: blue;")
        main_layout.addWidget(self.status_label)
        
        # 设置布局
        self.setLayout(main_layout)
        
        # 发送初始化信号
        self.action_triggered.emit('initialize', None)
    
    @Slot()
    def on_save_clicked(self):
        """保存按钮点击事件"""
        key = self.key_input.text().strip()
        value = self.value_input.text().strip()
        
        if not key:
            QMessageBox.warning(self, "警告", "键不能为空")
            return
        
        data = {'key': key, 'value': value}
        self.action_triggered.emit('save_data', data)
        
        # 清空输入框
        self.key_input.clear()
        self.value_input.clear()
    
    @Slot()
    def on_load_clicked(self):
        """加载按钮点击事件"""
        self.data_requested.emit('all')
    
    @Slot()
    def on_clear_clicked(self):
        """清除按钮点击事件"""
        reply = QMessageBox.question(self, "确认", "确定要清除所有缓存数据吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.action_triggered.emit('clear_data', None)
    
    @Slot(str, object)
    def update_data(self, data_key, data):
        """更新数据显示
        
        Args:
            data_key: 数据键
            data: 数据值
        """
        self.logger.debug(f"更新数据显示: {data_key}")
        
        if data_key == 'all' and isinstance(data, dict):
            # 显示所有数据
            text = "当前缓存数据:\n\n"
            for key, value in data.items():
                text += f"{key}: {value}\n"
            self.data_display.setText(text)
        elif data is not None:
            # 显示单个数据
            self.data_display.setText(f"{data_key}: {data}")
        else:
            # 无数据
            self.data_display.setText("无数据")
    
    @Slot(str)
    def update_status(self, status):
        """更新状态信息
        
        Args:
            status: 状态文本
        """
        self.logger.debug(f"更新状态: {status}")
        self.status_label.setText(f"状态: {status}")
    
    def closeEvent(self, event):
        """窗口关闭事件"""
        self.logger.info("主视图关闭")
        event.accept()

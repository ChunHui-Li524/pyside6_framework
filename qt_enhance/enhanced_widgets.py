from PySide6.QtWidgets import QPushButton, QLineEdit, QTextEdit, QStyle
from PySide6.QtCore import Signal, Slot, Qt, QTimer
from PySide6.QtGui import QFont, QColor, QPalette
from core.log_manager import LogManager

class EnhancedButton(QPushButton):
    """
    增强的按钮组件
    提供额外的功能，如点击效果、加载状态、自定义样式等
    """
    
    # 自定义信号
    clicked_with_data = Signal(object)  # 带数据的点击信号
    double_clicked = Signal()           # 双击信号
    
    def __init__(self, text="", parent=None, **kwargs):
        """初始化增强按钮
        
        Args:
            text: 按钮文本
            parent: 父组件
            **kwargs: 额外参数
                - auto_disable: 点击后自动禁用
                - disable_duration: 禁用持续时间（毫秒）
                - hover_effect: 是否启用悬停效果
                - click_effect: 是否启用点击效果
        """
        super().__init__(text, parent)
        self.logger = LogManager()
        
        # 配置选项
        self.auto_disable = kwargs.get('auto_disable', False)
        self.disable_duration = kwargs.get('disable_duration', 1000)  # 默认1秒
        self.hover_effect = kwargs.get('hover_effect', True)
        self.click_effect = kwargs.get('click_effect', True)
        
        # 数据存储
        self._user_data = None
        self._original_text = text
        self._is_loading = False
        
        # 初始化样式
        self._original_style = self.styleSheet()
        
        # 连接信号
        self.clicked.connect(self._on_clicked)
        
        # 设置默认字体
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        
        # 设置最小尺寸
        self.setMinimumHeight(30)
        self.setMinimumWidth(80)
        
        self.logger.debug(f"创建增强按钮: {text}")
    
    def _on_clicked(self):
        """内部点击处理"""
        # 发送带数据的信号
        self.clicked_with_data.emit(self._user_data)
        
        # 点击效果
        if self.click_effect:
            self._apply_click_effect()
        
        # 自动禁用
        if self.auto_disable:
            self._disable_temporarily()
    
    def _apply_click_effect(self):
        """应用点击效果"""
        # 改变背景色，然后恢复
        original_palette = self.palette()
        
        # 创建临时的高亮调色板
        highlight_palette = QPalette(original_palette)
        highlight_palette.setColor(QPalette.Button, QColor("#D0D0D0"))
        
        self.setPalette(highlight_palette)
        
        # 立即更新显示
        self.repaint()
        
        # 定时器恢复原始样式
        QTimer.singleShot(100, lambda: self.setPalette(original_palette))
    
    def _disable_temporarily(self):
        """临时禁用按钮"""
        self.setEnabled(False)
        
        # 定时器恢复启用状态
        QTimer.singleShot(self.disable_duration, lambda: self.setEnabled(True))
    
    def set_user_data(self, data):
        """设置与按钮关联的用户数据
        
        Args:
            data: 要关联的数据
        """
        self._user_data = data
    
    def get_user_data(self):
        """获取与按钮关联的用户数据
        
        Returns:
            关联的用户数据
        """
        return self._user_data
    
    def set_loading(self, is_loading):
        """设置加载状态
        
        Args:
            is_loading: 是否处于加载状态
        """
        self._is_loading = is_loading
        
        if is_loading:
            self._original_text = self.text()
            self.setText("加载中...")
            self.setEnabled(False)
        else:
            self.setText(self._original_text)
            self.setEnabled(True)
    
    def is_loading(self):
        """检查是否处于加载状态
        
        Returns:
            是否处于加载状态
        """
        return self._is_loading
    
    def enterEvent(self, event):
        """鼠标进入事件"""
        if self.hover_effect and self.isEnabled():
            # 创建临时的高亮样式
            self.setStyleSheet(f"{self._original_style}\nQPushButton:hover {{ background-color: #F0F0F0; }}")
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """鼠标离开事件"""
        if self.hover_effect:
            # 恢复原始样式
            self.setStyleSheet(self._original_style)
        super().leaveEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """鼠标双击事件"""
        if event.button() == Qt.LeftButton:
            self.double_clicked.emit()
        super().mouseDoubleClickEvent(event)

class EnhancedLineEdit(QLineEdit):
    """
    增强的行编辑组件
    提供额外的功能，如输入验证、自动完成、占位文本等
    """
    
    # 自定义信号
    text_changed_delayed = Signal(str)  # 延迟的文本变化信号
    enter_pressed = Signal(str)        # 回车键按下信号
    validation_changed = Signal(bool)  # 验证状态变化信号
    
    def __init__(self, parent=None, **kwargs):
        """初始化增强行编辑
        
        Args:
            parent: 父组件
            **kwargs: 额外参数
                - placeholder_text: 占位文本
                - delay_ms: 文本变化延迟时间（毫秒）
                - validation_func: 验证函数
                - max_length: 最大长度
                - echo_mode: 回显模式
        """
        super().__init__(parent)
        self.logger = LogManager()
        
        # 配置选项
        self.delay_ms = kwargs.get('delay_ms', 300)
        self.validation_func = kwargs.get('validation_func', None)
        self._is_valid = True
        
        # 初始化定时器用于延迟信号
        self._delay_timer = QTimer(self)
        self._delay_timer.setSingleShot(True)
        self._delay_timer.timeout.connect(self._emit_delayed_signal)
        
        # 设置属性
        if 'placeholder_text' in kwargs:
            self.setPlaceholderText(kwargs['placeholder_text'])
        
        if 'max_length' in kwargs:
            self.setMaxLength(kwargs['max_length'])
        
        if 'echo_mode' in kwargs:
            self.setEchoMode(kwargs['echo_mode'])
        
        # 连接信号
        self.textChanged.connect(self._on_text_changed)
        
        # 设置默认字体
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)
        
        # 设置最小高度
        self.setMinimumHeight(28)
        
        self.logger.debug("创建增强行编辑")
    
    def _on_text_changed(self, text):
        """内部文本变化处理"""
        # 重置定时器
        self._delay_timer.stop()
        self._delay_timer.start(self.delay_ms)
        
        # 验证输入
        self._validate_input(text)
    
    def _emit_delayed_signal(self):
        """发送延迟的文本变化信号"""
        self.text_changed_delayed.emit(self.text())
    
    def _validate_input(self, text):
        """验证输入文本
        
        Args:
            text: 输入的文本
        """
        if self.validation_func:
            try:
                new_valid_state = self.validation_func(text)
                if new_valid_state != self._is_valid:
                    self._is_valid = new_valid_state
                    self.validation_changed.emit(new_valid_state)
                    # 更新样式以反映验证状态
                    self._update_validation_style()
            except Exception as e:
                self.logger.error(f"验证函数执行错误: {str(e)}")
    
    def _update_validation_style(self):
        """根据验证状态更新样式"""
        if not self._is_valid:
            self.setStyleSheet("QLineEdit { border: 1px solid red; }")
        else:
            self.setStyleSheet("")
    
    def keyPressEvent(self, event):
        """按键事件处理"""
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.enter_pressed.emit(self.text())
        super().keyPressEvent(event)
    
    def set_validation_function(self, func):
        """设置验证函数
        
        Args:
            func: 接受文本参数并返回布尔值的函数
        """
        self.validation_func = func
        # 立即验证当前文本
        self._validate_input(self.text())
    
    def is_input_valid(self):
        """检查输入是否有效
        
        Returns:
            输入是否有效
        """
        return self._is_valid
    
    def set_delay(self, ms):
        """设置文本变化延迟时间
        
        Args:
            ms: 延迟时间（毫秒）
        """
        self.delay_ms = ms
    
    def focusInEvent(self, event):
        """获得焦点事件"""
        super().focusInEvent(event)
        # 可以在这里添加获得焦点的效果
    
    def focusOutEvent(self, event):
        """失去焦点事件"""
        # 确保发送最后的延迟信号
        if self._delay_timer.isActive():
            self._delay_timer.stop()
            self._emit_delayed_signal()
        super().focusOutEvent(event)

class EnhancedTextEdit(QTextEdit):
    """
    增强的文本编辑组件
    提供额外的功能，如字数统计、自动缩进、语法高亮等
    """
    
    # 自定义信号
    text_changed_delayed = Signal(str)  # 延迟的文本变化信号
    text_changed_with_length = Signal(str, int)  # 带长度的文本变化信号
    cursor_position_changed = Signal(int, int)   # 光标位置变化信号
    
    def __init__(self, parent=None, **kwargs):
        """初始化增强文本编辑
        
        Args:
            parent: 父组件
            **kwargs: 额外参数
                - delay_ms: 文本变化延迟时间（毫秒）
                - auto_indent: 是否启用自动缩进
                - show_line_numbers: 是否显示行号
                - max_length: 最大长度
        """
        super().__init__(parent)
        self.logger = LogManager()
        
        # 配置选项
        self.delay_ms = kwargs.get('delay_ms', 500)
        self.auto_indent = kwargs.get('auto_indent', True)
        self.show_line_numbers = kwargs.get('show_line_numbers', False)
        self.max_length = kwargs.get('max_length', -1)  # -1表示无限长度
        
        # 初始化定时器用于延迟信号
        self._delay_timer = QTimer(self)
        self._delay_timer.setSingleShot(True)
        self._delay_timer.timeout.connect(self._emit_delayed_signal)
        
        # 连接信号
        self.textChanged.connect(self._on_text_changed)
        self.cursorPositionChanged.connect(self._on_cursor_position_changed)
        
        # 设置默认字体（等宽字体适合代码编辑）
        font = QFont("Consolas", 10)
        self.setFont(font)
        
        # 设置最小尺寸
        self.setMinimumHeight(100)
        
        self.logger.debug("创建增强文本编辑")
    
    def _on_text_changed(self):
        """内部文本变化处理"""
        # 限制最大长度
        if self.max_length > 0:
            current_text = self.toPlainText()
            if len(current_text) > self.max_length:
                # 保存光标位置
                cursor = self.textCursor()
                position = cursor.position()
                
                # 截断文本
                self.setPlainText(current_text[:self.max_length])
                
                # 恢复光标位置
                cursor.setPosition(min(position, self.max_length))
                self.setTextCursor(cursor)
                
                return
        
        # 重置定时器
        self._delay_timer.stop()
        self._delay_timer.start(self.delay_ms)
        
        # 发送带长度的变化信号
        current_text = self.toPlainText()
        self.text_changed_with_length.emit(current_text, len(current_text))
    
    def _emit_delayed_signal(self):
        """发送延迟的文本变化信号"""
        self.text_changed_delayed.emit(self.toPlainText())
    
    def _on_cursor_position_changed(self):
        """光标位置变化处理"""
        cursor = self.textCursor()
        line = cursor.blockNumber() + 1  # 行号从1开始
        column = cursor.columnNumber() + 1  # 列号从1开始
        
        self.cursor_position_changed.emit(line, column)
    
    def keyPressEvent(self, event):
        """按键事件处理"""
        # 处理自动缩进
        if self.auto_indent and event.key() == Qt.Key_Return:
            self._handle_auto_indent()
            return
        
        # 处理Tab键
        if event.key() == Qt.Key_Tab:
            # 插入4个空格而不是Tab字符
            self.insertPlainText("    ")
            return
        
        # 处理退格键（处理缩进）
        if event.key() == Qt.Key_Backspace:
            cursor = self.textCursor()
            # 检查光标前4个字符是否都是空格
            cursor.movePosition(cursor.Left, cursor.KeepAnchor, 4)
            selected_text = cursor.selectedText()
            if selected_text == "    ":
                cursor.removeSelectedText()
                return
        
        super().keyPressEvent(event)
    
    def _handle_auto_indent(self):
        """处理自动缩进"""
        cursor = self.textCursor()
        current_block = cursor.block()
        current_text = current_block.text()
        
        # 计算当前行的缩进级别
        indent_level = 0
        for char in current_text:
            if char == ' ':
                indent_level += 1
            else:
                break
        
        # 插入换行符
        self.insertPlainText("\n")
        
        # 插入相同级别的缩进
        self.insertPlainText(" " * indent_level)
    
    def get_text_length(self):
        """获取文本长度
        
        Returns:
            文本长度
        """
        return len(self.toPlainText())
    
    def get_line_count(self):
        """获取行数
        
        Returns:
            行数
        """
        return self.document().blockCount()
    
    def set_delay(self, ms):
        """设置文本变化延迟时间
        
        Args:
            ms: 延迟时间（毫秒）
        """
        self.delay_ms = ms
    
    def set_max_length(self, max_length):
        """设置最大长度
        
        Args:
            max_length: 最大长度，-1表示无限长度
        """
        self.max_length = max_length
        # 立即检查并截断当前文本
        self._on_text_changed()
    
    def focusInEvent(self, event):
        """获得焦点事件"""
        super().focusInEvent(event)
    
    def focusOutEvent(self, event):
        """失去焦点事件"""
        # 确保发送最后的延迟信号
        if self._delay_timer.isActive():
            self._delay_timer.stop()
            self._emit_delayed_signal()
        super().focusOutEvent(event)

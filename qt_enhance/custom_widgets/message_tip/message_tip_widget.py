# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2025-12-24
@Description: 
    消息提示框，非模态
"""
import time

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon

from qt_enhance.custom_widgets.message_tip.ui.MessageTip import Ui_MessageTip


RECORDER = {}


class QMessageTip(QWidget):
    _index = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MessageTip()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        QMessageTip._index += 1
        RECORDER[QMessageTip._index] = self

    def set_icon(self, icon):
        self.ui.pushButton.setIcon(icon)

    def set_text(self, text):
        self.ui.label.setText(text)

    def set_color(self, fg_color, bg_color):
        """
        设置背景色和前景色
        @param fg_color: 文字颜色
        @param bg_color: 背景颜色
        @return:
        """
        self.ui.frame.setStyleSheet(f"background-color: {bg_color}; border-radius: 8px;")
        self.ui.label.setStyleSheet(f"color: {fg_color};")

    def close_after_timer(self, interval):
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.close)
        self._timer.setSingleShot(True)
        self._timer.start(interval * 1000)

    def show(self):
        """
        显示提示框
        @return:
        """
        # 在用户当前屏幕居中显示
        x = (QApplication.primaryScreen().geometry().width() - self.width()) // 2
        y = (QApplication.primaryScreen().geometry().height() - self.height()) // 4
        # 获取坐标此处的widget
        widget = QApplication.widgetAt(x, y)
        while isinstance(widget, QMessageTip):
            y += widget.height() + 10
            widget = QApplication.widgetAt(x, y)
        self.move(x, y)
        super().show()

    def close(self):
        """
        关闭提示框
        @return:
        """
        self._timer.stop()
        super().close()
        del RECORDER[self._index]

    @staticmethod
    def information(text):
        """
        显示信息提示框（蓝色主题）
        @param text: 提示文本
        @return:
        """
        window = QMessageTip()
        window.show()
        window.set_text(text)
        window.set_icon(QIcon(":images/png/info.png"))
        # 深蓝色文字, 浅蓝色背景
        window.set_color("#003366", "#E6F2FF")
        window.close_after_timer(3)

    @staticmethod
    def warning(text):
        """
        显示警告提示框（橙黄色主题）
        @param text: 提示文本
        @return:
        """
        window = QMessageTip()
        window.show()
        window.set_text(text)
        window.set_icon(QIcon(":images/png/warn.png"))
        # 深橙黄色文字, 浅橙黄色背景
        window.set_color("#8C4200", "#FFF7E6")
        window.close_after_timer(3)

    @staticmethod
    def success(text):
        """
        显示成功提示框（绿色主题）
        @param text: 提示文本
        @return:
        """
        window = QMessageTip()
        window.show()
        window.set_text(text)
        window.set_icon(QIcon(":images/png/ok.png"))
        # 深绿色文字, 浅绿色背景
        window.set_color("#004D00", "#E6FFF2")
        window.close_after_timer(3)

    @staticmethod
    def error(text):
        """
        显示错误提示框（红色主题）
        @param text: 提示文本
        @return:
        """
        window = QMessageTip()
        window.show()
        window.set_text(text)
        window.set_icon(QIcon(":images/png/fail.png"))
        # 深红色文字, 浅红色背景
        window.set_color("#8C0000", "#FFF0F0")
        window.close_after_timer(3)


if __name__ == '__main__':
    from PySide6.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    QMessageTip.information("information")
    QApplication.processEvents()
    time.sleep(1)
    QMessageTip.warning("warning")
    QApplication.processEvents()
    time.sleep(1)
    QMessageTip.success("success")
    QApplication.processEvents()
    time.sleep(1)
    QMessageTip.error("error"+"123"*40)
    print("show")
    sys.exit(app.exec())

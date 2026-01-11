# -*- coding: utf-8 -*-
"""
@Author: Li ChunHui
@Date:   2026-01-11
@Description: 
    This is a brief description of what the script does.
"""
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QTableWidgetItem


def get_table_widget_item(text, font_color=None, background_color=None, alignment=None) -> QTableWidgetItem:
    """创建QTableWidgetItem，支持多种自定义选项

    Args:
        text: 显示的文本
        font_color: 字体颜色 (QColor 或 RGB元组)
        background_color: 背景颜色 (QColor 或 RGB元组)
        alignment: 对齐方式 (如 Qt.AlignCenter)

    Returns:
        QTableWidgetItem: 配置好的表格项
    """
    item = QTableWidgetItem(str(text))
    # 设置字体颜色
    if font_color:
        if isinstance(font_color, tuple):
            font_color = QColor(*font_color)
        item.setForeground(QBrush(font_color))

    # 设置背景颜色
    if background_color:
        if isinstance(background_color, tuple):
            background_color = QColor(*background_color)
        item.setBackground(QBrush(background_color))

    # 设置对齐方式
    if alignment:
        item.setTextAlignment(alignment)
    return item


def get_readonly_table_widget_item(text) -> QTableWidgetItem:
    """创建只读的QTableWidgetItem"""
    item = get_table_widget_item(text)
    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
    return item


def clickable_table_widget_item(text) -> QTableWidgetItem:
    """创建可点击的超链接QTableWidgetItem，显示为蓝色下划线"""
    item = get_table_widget_item(text)
    font = item.font()
    font.setUnderline(True)
    item.setFont(font)
    return item

"""系统托盘模块"""

from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon, QAction
from typing import Callable, Optional

from ..utils.logger import logger


class SystemTray:
    """系统托盘管理器"""
    
    def __init__(self, app, icon_path: Optional[str] = None):
        """
        初始化系统托盘
        
        Args:
            app: QApplication 实例
            icon_path: 图标路径
        """
        self.app = app
        self.tray_icon = QSystemTrayIcon(app)
        
        # 设置图标
        if icon_path:
            self.tray_icon.setIcon(QIcon(icon_path))
        
        # 创建菜单
        self.menu = QMenu()
        self.tray_icon.setContextMenu(self.menu)
        
        # 显示托盘图标
        self.tray_icon.show()
        
        logger.info("系统托盘已初始化")
    
    def add_action(self, text: str, callback: Callable):
        """
        添加菜单项
        
        Args:
            text: 菜单文本
            callback: 点击回调函数
        """
        action = QAction(text, self.menu)
        action.triggered.connect(callback)
        self.menu.addAction(action)
    
    def add_separator(self):
        """添加分隔符"""
        self.menu.addSeparator()
    
    def show_message(self, title: str, message: str, duration: int = 3000):
        """
        显示托盘消息
        
        Args:
            title: 消息标题
            message: 消息内容
            duration: 显示时长（毫秒）
        """
        self.tray_icon.showMessage(
            title,
            message,
            QSystemTrayIcon.MessageIcon.Information,
            duration
        )
    
    def set_tooltip(self, tooltip: str):
        """
        设置托盘提示
        
        Args:
            tooltip: 提示文本
        """
        self.tray_icon.setToolTip(tooltip)


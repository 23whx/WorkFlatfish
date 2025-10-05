"""任务栏标题显示模式"""

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt

from .base import DisplayMode
from ..core.title_slice import to_title_slice
from ..utils.logger import logger


class TaskbarTitleMode(DisplayMode):
    """任务栏标题显示模式"""
    
    def __init__(self, config: dict, app):
        """
        初始化任务栏标题模式
        
        Args:
            config: 配置字典
            app: QApplication 实例
        """
        super().__init__(config)
        self.app = app
        self.window: QWidget = None
        self.title_window = config.get("title_window", 40)
        
        taskbar_config = config.get("taskbar_title", {})
        self.min_size = taskbar_config.get("min_window_size", [1, 1])
        self.corner = taskbar_config.get("stick_to_corner", "bottom-left")
    
    def setup(self):
        """设置窗口"""
        # 创建一个小窗口
        self.window = QWidget()
        self.window.setWindowTitle("StealthNovel")
        
        # 设置窗口为最小尺寸
        self.window.setFixedSize(self.min_size[0], self.min_size[1])
        
        # 设置窗口标志：保持在任务栏，置顶
        self.window.setWindowFlags(
            Qt.WindowType.Window | 
            Qt.WindowType.WindowStaysOnTopHint
        )
        
        # 将窗口移到屏幕角落
        self._move_to_corner()
        
        logger.info("任务栏标题模式已初始化")
    
    def _move_to_corner(self):
        """将窗口移到屏幕角落"""
        screen = self.app.primaryScreen().geometry()
        
        if self.corner == "bottom-left":
            x = 0
            y = screen.height() - self.min_size[1]
        elif self.corner == "bottom-right":
            x = screen.width() - self.min_size[0]
            y = screen.height() - self.min_size[1]
        elif self.corner == "top-left":
            x = 0
            y = 0
        elif self.corner == "top-right":
            x = screen.width() - self.min_size[0]
            y = 0
        else:
            x = 0
            y = screen.height() - self.min_size[1]
        
        self.window.move(x, y)
    
    def render(self, text: str):
        """
        渲染文本到窗口标题
        
        Args:
            text: 要显示的文本
        """
        if not self.window:
            return
        
        # 切片文本以适应任务栏宽度
        sliced_text = to_title_slice(text, self.title_window)
        self.window.setWindowTitle(sliced_text)
        
        logger.debug(f"更新标题: {sliced_text}")
    
    def show(self):
        """显示窗口"""
        if self.window:
            self.window.show()
            # 确保窗口获得焦点
            self.window.activateWindow()
    
    def hide(self):
        """隐藏窗口"""
        if self.window:
            self.window.hide()
    
    def cleanup(self):
        """清理资源"""
        if self.window:
            self.window.close()
            self.window = None
        logger.info("任务栏标题模式已清理")


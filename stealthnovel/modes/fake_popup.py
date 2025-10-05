"""伪装弹窗显示模式"""

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer
from PySide6.QtGui import QFont

from .base import DisplayMode
from ..ui.theme import Theme
from ..utils.logger import logger


class FakePopupMode(DisplayMode):
    """伪装弹窗显示模式"""
    
    def __init__(self, config: dict, app):
        """
        初始化伪装弹窗模式
        
        Args:
            config: 配置字典
            app: QApplication 实例
        """
        super().__init__(config)
        self.app = app
        self.window: QWidget = None
        self.label: QLabel = None
        
        # 弹窗配置
        popup_config = config.get("fake_popup", {})
        self.width = popup_config.get("width", 360)
        self.height = popup_config.get("height", 120)
        self.margin = popup_config.get("margin", 16)
        self.rounded = popup_config.get("rounded", 14)
        self.shadow = popup_config.get("shadow", True)
        self.animate = popup_config.get("animate", True)
        
        # 主题
        self.theme = Theme(config.get("theme", {}))
    
    def setup(self):
        """设置弹窗窗口"""
        # 创建无边框窗口
        self.window = QWidget()
        self.window.setWindowTitle("StealthNovel Popup")
        
        # 设置窗口标志：无边框、置顶、工具窗口
        self.window.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        
        # 设置窗口大小
        self.window.setFixedSize(self.width, self.height)
        
        # 应用样式
        self.window.setStyleSheet(self.theme.get_popup_stylesheet(self.rounded))
        self.window.setWindowOpacity(self.theme.get_window_opacity())
        
        # 创建标签显示文本
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setWordWrap(True)
        
        # 设置字体
        font = QFont("Microsoft YaHei", 12)
        self.label.setFont(font)
        
        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.setContentsMargins(10, 10, 10, 10)
        self.window.setLayout(layout)
        
        # 定位到右下角
        self._move_to_corner()
        
        logger.info("伪装弹窗模式已初始化")
    
    def _move_to_corner(self):
        """将窗口移到屏幕右下角"""
        screen = self.app.primaryScreen().availableGeometry()
        x = screen.width() - self.width - self.margin
        y = screen.height() - self.height - self.margin
        self.window.move(x, y)
    
    def render(self, text: str):
        """
        渲染文本到弹窗
        
        Args:
            text: 要显示的文本
        """
        if not self.label:
            return
        
        # 限制显示的文本长度
        display_text = text[:200] if len(text) > 200 else text
        self.label.setText(display_text)
        
        logger.debug(f"更新弹窗内容: {display_text[:30]}...")
    
    def show(self):
        """显示弹窗（带动画）"""
        if not self.window:
            return
        
        if self.animate:
            # 淡入动画
            self.window.setWindowOpacity(0)
            self.window.show()
            
            animation = QPropertyAnimation(self.window, b"windowOpacity")
            animation.setDuration(300)
            animation.setStartValue(0)
            animation.setEndValue(self.theme.get_window_opacity())
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation.start()
            
            # 保存动画引用防止被垃圾回收
            self.window._fade_in_animation = animation
        else:
            self.window.show()
    
    def hide(self):
        """隐藏弹窗（带动画）"""
        if not self.window:
            return
        
        if self.animate:
            # 淡出动画
            animation = QPropertyAnimation(self.window, b"windowOpacity")
            animation.setDuration(300)
            animation.setStartValue(self.theme.get_window_opacity())
            animation.setEndValue(0)
            animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
            animation.finished.connect(self.window.hide)
            animation.start()
            
            # 保存动画引用
            self.window._fade_out_animation = animation
        else:
            self.window.hide()
    
    def cleanup(self):
        """清理资源"""
        if self.window:
            self.window.close()
            self.window = None
            self.label = None
        logger.info("伪装弹窗模式已清理")


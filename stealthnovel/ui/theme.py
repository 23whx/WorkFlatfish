"""主题配置模块"""

from typing import Dict


class Theme:
    """主题配置类"""
    
    def __init__(self, config: Dict[str, any] = None):
        """
        初始化主题
        
        Args:
            config: 主题配置字典
        """
        if config is None:
            config = {}
        
        self.text_color = config.get("text", "#000000")
        self.bg_color = config.get("bg", "#E6F4EA")
        self.accent_color = config.get("accent", "#F9D9D9")
        self.opacity = config.get("opacity", 0.92)
    
    def get_popup_stylesheet(self, rounded: int = 14) -> str:
        """
        获取弹窗样式表
        
        Args:
            rounded: 圆角半径
            
        Returns:
            CSS 样式表字符串
        """
        return f"""
            QWidget {{
                background-color: {self.bg_color};
                color: {self.text_color};
                border: 1px solid rgba(0, 0, 0, 0.2);
                border-radius: {rounded}px;
                font-family: "Microsoft YaHei", "SimHei", sans-serif;
                font-size: 14px;
            }}
            QLabel {{
                background-color: transparent;
                padding: 10px;
            }}
            .accent {{
                background-color: {self.accent_color};
            }}
        """
    
    def get_window_opacity(self) -> float:
        """
        获取窗口不透明度
        
        Returns:
            不透明度 (0.0-1.0)
        """
        return self.opacity


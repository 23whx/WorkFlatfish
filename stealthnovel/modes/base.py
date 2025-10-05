"""显示模式基类"""

from abc import ABC, abstractmethod
from typing import List, Optional


class DisplayMode(ABC):
    """显示模式抽象基类"""
    
    def __init__(self, config: dict):
        """
        初始化显示模式
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.lines: List[str] = []
        self.line_index = 0
        self.char_index = 0
    
    @abstractmethod
    def setup(self):
        """设置显示模式（创建窗口等）"""
        pass
    
    @abstractmethod
    def render(self, text: str):
        """
        渲染文本
        
        Args:
            text: 要显示的文本
        """
        pass
    
    @abstractmethod
    def show(self):
        """显示窗口"""
        pass
    
    @abstractmethod
    def hide(self):
        """隐藏窗口"""
        pass
    
    @abstractmethod
    def cleanup(self):
        """清理资源"""
        pass
    
    def load_text(self, lines: List[str], line_idx: int = 0, char_idx: int = 0):
        """
        加载文本
        
        Args:
            lines: 文本行列表
            line_idx: 起始行索引
            char_idx: 起始字符索引
        """
        self.lines = lines
        self.line_index = line_idx
        self.char_index = char_idx
    
    def get_current_text(self) -> str:
        """
        获取当前位置的文本
        
        Returns:
            当前文本片段
        """
        if not self.lines or self.line_index >= len(self.lines):
            return ""
        
        current_line = self.lines[self.line_index]
        
        if self.char_index >= len(current_line):
            if self.line_index + 1 < len(self.lines):
                return self.lines[self.line_index + 1]
            return ""
        
        return current_line[self.char_index:]


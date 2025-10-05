"""状态管理模块"""

import json
from pathlib import Path
from typing import Optional, Tuple

from ..utils.logger import logger


class ReadingState:
    """阅读状态管理类"""
    
    def __init__(self, state_file: str = "config/state.json"):
        """
        初始化状态管理器
        
        Args:
            state_file: 状态文件路径
        """
        self.state_file = Path(state_file)
        self.line_index = 0
        self.char_index = 0
        self.source_hash = ""
        
        self._ensure_state_file()
        self.load()
    
    def _ensure_state_file(self):
        """确保状态文件存在"""
        if not self.state_file.exists():
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            self.save()
    
    def load(self):
        """从文件加载状态"""
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.line_index = data.get("line_index", 0)
            self.char_index = data.get("char_index", 0)
            self.source_hash = data.get("source_hash", "")
            
            logger.info(f"加载状态: 行{self.line_index}, 字符{self.char_index}")
        except Exception as e:
            logger.error(f"加载状态失败: {e}")
            self.reset()
    
    def save(self):
        """保存状态到文件"""
        try:
            data = {
                "line_index": self.line_index,
                "char_index": self.char_index,
                "source_hash": self.source_hash
            }
            
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"保存状态: 行{self.line_index}, 字符{self.char_index}")
        except Exception as e:
            logger.error(f"保存状态失败: {e}")
    
    def reset(self):
        """重置状态"""
        self.line_index = 0
        self.char_index = 0
        self.save()
        logger.info("重置阅读进度")
    
    def check_source_changed(self, new_hash: str) -> bool:
        """
        检查文本来源是否改变
        
        Args:
            new_hash: 新文本的哈希值
            
        Returns:
            如果来源改变返回 True
        """
        if self.source_hash != new_hash:
            self.source_hash = new_hash
            self.reset()
            return True
        return False
    
    def get_position(self) -> Tuple[int, int]:
        """
        获取当前位置
        
        Returns:
            (行索引, 字符索引)
        """
        return self.line_index, self.char_index
    
    def set_position(self, line_idx: int, char_idx: int):
        """
        设置当前位置
        
        Args:
            line_idx: 行索引
            char_idx: 字符索引
        """
        self.line_index = line_idx
        self.char_index = char_idx
        self.save()
    
    def advance_char(self, lines: list) -> Tuple[int, int]:
        """
        前进一个字符
        
        Args:
            lines: 文本行列表
            
        Returns:
            新的 (行索引, 字符索引)
        """
        if self.line_index >= len(lines):
            return self.line_index, self.char_index
        
        current_line = lines[self.line_index]
        
        # 如果当前行还有字符
        if self.char_index + 1 < len(current_line):
            self.char_index += 1
        else:
            # 移到下一行
            if self.line_index + 1 < len(lines):
                self.line_index += 1
                self.char_index = 0
        
        self.save()
        return self.line_index, self.char_index
    
    def advance_line(self, lines: list) -> Tuple[int, int]:
        """
        前进一行
        
        Args:
            lines: 文本行列表
            
        Returns:
            新的 (行索引, 字符索引)
        """
        if self.line_index + 1 < len(lines):
            self.line_index += 1
            self.char_index = 0
        
        self.save()
        return self.line_index, self.char_index


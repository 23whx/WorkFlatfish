"""文本解析模块"""

from typing import List


def parse_text(text: str) -> List[str]:
    """
    解析文本为行列表
    
    Args:
        text: 原始文本
        
    Returns:
        清洗后的行列表
    """
    if not text:
        return []
    
    # 按行分割
    lines = text.split("\n")
    
    # 清洗：去除每行首尾空白，但保留空行
    cleaned_lines = [line.strip() for line in lines]
    
    return cleaned_lines


def get_current_text(lines: List[str], line_idx: int, char_idx: int) -> str:
    """
    获取当前位置的文本片段
    
    Args:
        lines: 文本行列表
        line_idx: 当前行索引
        char_idx: 当前字符索引
        
    Returns:
        从当前位置开始的文本片段
    """
    if not lines or line_idx >= len(lines):
        return ""
    
    current_line = lines[line_idx]
    
    # 如果字符索引超出当前行，返回空字符串
    if char_idx >= len(current_line):
        # 尝试返回下一行
        if line_idx + 1 < len(lines):
            return lines[line_idx + 1]
        return ""
    
    # 返回当前行从 char_idx 开始的部分
    return current_line[char_idx:]


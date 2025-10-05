"""标题切片模块"""


def to_title_slice(text: str, max_len: int = 40) -> str:
    """
    将文本切片为适合任务栏标题的长度
    使用滑动窗口策略，显示末尾的 N 个字符
    
    Args:
        text: 原始文本
        max_len: 最大长度
        
    Returns:
        切片后的文本
    """
    if not text:
        return ""
    
    if len(text) <= max_len:
        return text
    
    # 显示末尾的 max_len 个字符，前面加省略号
    return "…" + text[-(max_len - 1):]


def format_for_display(text: str, mode: str = "taskbar", max_len: int = 40) -> str:
    """
    根据显示模式格式化文本
    
    Args:
        text: 原始文本
        mode: 显示模式 (taskbar/popup)
        max_len: 最大长度（仅对 taskbar 模式有效）
        
    Returns:
        格式化后的文本
    """
    if not text:
        return ""
    
    if mode == "taskbar":
        return to_title_slice(text, max_len)
    elif mode == "popup":
        # 弹窗模式可以显示更多内容
        return text
    else:
        return text


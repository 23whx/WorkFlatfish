"""测试 title_slice 模块"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from stealthnovel.core.title_slice import to_title_slice, format_for_display


def test_to_title_slice_short():
    """测试短文本切片"""
    text = "短文本"
    result = to_title_slice(text, 40)
    assert result == "短文本"
    
    print("✓ test_to_title_slice_short 通过")


def test_to_title_slice_long():
    """测试长文本切片"""
    text = "这是一段很长的文本，用于测试标题切片功能是否正常工作。这段文本会超过最大长度限制。"
    result = to_title_slice(text, 20)
    
    # 应该以省略号开头，并且长度为 20
    assert result.startswith("…")
    assert len(result) == 20
    
    print("✓ test_to_title_slice_long 通过")


def test_format_for_display():
    """测试格式化显示"""
    text = "测试文本"
    
    # 任务栏模式
    result = format_for_display(text, "taskbar", 10)
    assert result == "测试文本"
    
    # 弹窗模式
    result = format_for_display(text, "popup")
    assert result == "测试文本"
    
    print("✓ test_format_for_display 通过")


if __name__ == "__main__":
    test_to_title_slice_short()
    test_to_title_slice_long()
    test_format_for_display()
    print("\n所有测试通过！")


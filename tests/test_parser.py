"""测试 parser 模块"""

import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from stealthnovel.core.parser import parse_text, get_current_text


def test_parse_text():
    """测试文本解析"""
    text = "第一行\n第二行\n第三行"
    lines = parse_text(text)
    
    assert len(lines) == 3
    assert lines[0] == "第一行"
    assert lines[1] == "第二行"
    assert lines[2] == "第三行"
    
    print("✓ test_parse_text 通过")


def test_parse_empty_text():
    """测试空文本解析"""
    text = ""
    lines = parse_text(text)
    
    assert len(lines) == 0
    
    print("✓ test_parse_empty_text 通过")


def test_get_current_text():
    """测试获取当前文本"""
    lines = ["第一行", "第二行", "第三行"]
    
    # 从第一行开头开始
    text = get_current_text(lines, 0, 0)
    assert text == "第一行"
    
    # 从第一行中间开始
    text = get_current_text(lines, 0, 1)
    assert text == "一行"
    
    # 从第二行开始
    text = get_current_text(lines, 1, 0)
    assert text == "第二行"
    
    print("✓ test_get_current_text 通过")


if __name__ == "__main__":
    test_parse_text()
    test_parse_empty_text()
    test_get_current_text()
    print("\n所有测试通过！")


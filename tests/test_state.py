"""测试 state 模块"""

import sys
import json
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from stealthnovel.core.state import ReadingState


def test_state_init():
    """测试状态初始化"""
    # 使用临时状态文件
    state_file = "tests/temp_state.json"
    state = ReadingState(state_file)
    
    assert state.line_index == 0
    assert state.char_index == 0
    
    # 清理
    Path(state_file).unlink(missing_ok=True)
    
    print("✓ test_state_init 通过")


def test_state_advance_char():
    """测试字符推进"""
    state_file = "tests/temp_state.json"
    state = ReadingState(state_file)
    
    lines = ["第一行", "第二行"]
    
    # 前进一个字符
    line_idx, char_idx = state.advance_char(lines)
    assert line_idx == 0
    assert char_idx == 1
    
    # 前进到行尾
    state.char_index = 2  # "第一行" 的最后一个字符
    line_idx, char_idx = state.advance_char(lines)
    assert line_idx == 1  # 应该移到下一行
    assert char_idx == 0
    
    # 清理
    Path(state_file).unlink(missing_ok=True)
    
    print("✓ test_state_advance_char 通过")


def test_state_advance_line():
    """测试行推进"""
    state_file = "tests/temp_state.json"
    state = ReadingState(state_file)
    
    lines = ["第一行", "第二行", "第三行"]
    
    # 前进一行
    line_idx, char_idx = state.advance_line(lines)
    assert line_idx == 1
    assert char_idx == 0
    
    # 再前进一行
    line_idx, char_idx = state.advance_line(lines)
    assert line_idx == 2
    assert char_idx == 0
    
    # 清理
    Path(state_file).unlink(missing_ok=True)
    
    print("✓ test_state_advance_line 通过")


def test_state_save_load():
    """测试状态保存和加载"""
    state_file = "tests/temp_state.json"
    
    # 创建并保存状态
    state1 = ReadingState(state_file)
    state1.line_index = 5
    state1.char_index = 10
    state1.source_hash = "test_hash"
    state1.save()
    
    # 加载状态
    state2 = ReadingState(state_file)
    assert state2.line_index == 5
    assert state2.char_index == 10
    assert state2.source_hash == "test_hash"
    
    # 清理
    Path(state_file).unlink(missing_ok=True)
    
    print("✓ test_state_save_load 通过")


if __name__ == "__main__":
    test_state_init()
    test_state_advance_char()
    test_state_advance_line()
    test_state_save_load()
    print("\n所有测试通过！")


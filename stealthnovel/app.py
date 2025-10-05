"""StealthNovel 主程序"""

import sys
import json
from pathlib import Path
from typing import Optional

from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox
from PySide6.QtCore import QTimer

from .utils.logger import logger
from .utils.files import load_text_from_source, compute_hash
from .core.state import ReadingState
from .core.parser import parse_text, get_current_text
from .core.hotkeys import HotkeyManager
from .ui.tray import SystemTray
from .modes.taskbar_title import TaskbarTitleMode
from .modes.fake_popup import FakePopupMode


class StealthNovelApp:
    """StealthNovel 主应用类"""
    
    def __init__(self):
        """初始化应用"""
        # 创建 Qt 应用
        self.app = QApplication(sys.argv)
        self.app.setQuitOnLastWindowClosed(False)
        
        # 加载配置
        self.config = self._load_config()
        
        # 初始化组件
        self.state = ReadingState()
        self.hotkey_manager = HotkeyManager()
        self.tray = SystemTray(self.app)
        
        # 显示模式
        self.current_mode = None
        self.mode_name = self.config.get("mode", "TaskbarTitle")
        
        # 文本数据
        self.lines = []
        self.text_content = ""
        
        # 自动推进定时器
        self.auto_timer: Optional[QTimer] = None
        self.auto_tick_enabled = self.config.get("auto_tick", False)
        self.auto_tick_interval = self.config.get("auto_tick_interval_ms", 0)
        
        # 初始化
        self._setup_mode()
        self._setup_tray()
        self._setup_hotkeys()
        self._load_initial_text()
        
        logger.info("StealthNovel 应用已启动")
    
    def _load_config(self) -> dict:
        """加载配置文件"""
        config_path = Path("config/settings.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            logger.info("配置已加载")
            return config
        except Exception as e:
            logger.error(f"加载配置失败: {e}")
            return {}
    
    def _setup_mode(self):
        """设置显示模式"""
        if self.current_mode:
            self.current_mode.cleanup()
        
        if self.mode_name == "TaskbarTitle":
            self.current_mode = TaskbarTitleMode(self.config, self.app)
        elif self.mode_name == "FakePopup":
            self.current_mode = FakePopupMode(self.config, self.app)
        else:
            logger.error(f"未知的显示模式: {self.mode_name}")
            self.current_mode = TaskbarTitleMode(self.config, self.app)
        
        self.current_mode.setup()
        self.current_mode.show()
        
        logger.info(f"显示模式已设置: {self.mode_name}")
    
    def _setup_tray(self):
        """设置系统托盘"""
        self.tray.set_tooltip("StealthNovel")
        
        # 添加菜单项
        self.tray.add_action(f"当前模式: {self.mode_name}", lambda: None)
        self.tray.add_separator()
        
        self.tray.add_action("切换显示模式", self.toggle_mode)
        self.tray.add_action("开/关自动推进", self.toggle_auto_advance)
        self.tray.add_separator()
        
        self.tray.add_action("加载本地文件", self.load_file_dialog)
        self.tray.add_action("从剪贴板加载", self.load_from_clipboard)
        self.tray.add_separator()
        
        self.tray.add_action("重置进度", self.reset_progress)
        self.tray.add_separator()
        
        self.tray.add_action("退出", self.quit)
        
        logger.info("系统托盘已设置")
    
    def _setup_hotkeys(self):
        """设置全局热键"""
        hotkey_config = self.config.get("hotkeys", {})
        
        callbacks = {
            "next_char": self.advance_char,
            "next_line": self.advance_line,
            "toggle_mode": self.toggle_mode,
            "toggle_auto": self.toggle_auto_advance,
            "reset_progress": self.reset_progress
        }
        
        self.hotkey_manager.register_from_config(hotkey_config, callbacks)
        
        logger.info("全局热键已设置")
    
    def _load_initial_text(self):
        """加载初始文本"""
        source_config = self.config.get("source", {})
        source_type = source_config.get("type", "file")
        path = source_config.get("path", "")
        url = source_config.get("url", "")
        
        text = load_text_from_source(source_type, path, url)
        
        if text:
            self.load_text(text)
        else:
            logger.warning("未能加载初始文本")
            self.tray.show_message("StealthNovel", "未能加载文本，请从托盘菜单加载")
    
    def load_text(self, text: str):
        """
        加载文本
        
        Args:
            text: 文本内容
        """
        if not text:
            logger.warning("文本为空")
            return
        
        # 解析文本
        self.text_content = text
        self.lines = parse_text(text)
        
        # 检查文本来源是否改变
        text_hash = compute_hash(text)
        if self.state.check_source_changed(text_hash):
            logger.info("检测到新文本，重置进度")
        
        # 加载到显示模式
        line_idx, char_idx = self.state.get_position()
        self.current_mode.load_text(self.lines, line_idx, char_idx)
        
        # 渲染当前文本
        self.render_current()
        
        logger.info(f"文本已加载，共 {len(self.lines)} 行")
    
    def render_current(self):
        """渲染当前位置的文本"""
        line_idx, char_idx = self.state.get_position()
        current_text = get_current_text(self.lines, line_idx, char_idx)
        self.current_mode.render(current_text)
    
    def advance_char(self):
        """前进一个字符"""
        self.state.advance_char(self.lines)
        self.render_current()
        logger.debug("前进一个字符")
    
    def advance_line(self):
        """前进一行"""
        self.state.advance_line(self.lines)
        self.render_current()
        logger.debug("前进一行")
    
    def toggle_mode(self):
        """切换显示模式"""
        if self.mode_name == "TaskbarTitle":
            self.mode_name = "FakePopup"
        else:
            self.mode_name = "TaskbarTitle"
        
        self._setup_mode()
        
        # 重新加载文本
        if self.lines:
            line_idx, char_idx = self.state.get_position()
            self.current_mode.load_text(self.lines, line_idx, char_idx)
            self.render_current()
        
        self.tray.show_message("StealthNovel", f"已切换到: {self.mode_name}")
        logger.info(f"切换显示模式: {self.mode_name}")
    
    def toggle_auto_advance(self):
        """开关自动推进"""
        self.auto_tick_enabled = not self.auto_tick_enabled
        
        if self.auto_tick_enabled:
            # 启动定时器
            if not self.auto_timer:
                self.auto_timer = QTimer()
                self.auto_timer.timeout.connect(self._auto_advance_tick)
            
            interval = self.auto_tick_interval if self.auto_tick_interval > 0 else 1000
            self.auto_timer.start(interval)
            
            self.tray.show_message("StealthNovel", f"自动推进已开启 ({interval}ms)")
            logger.info(f"自动推进已开启: {interval}ms")
        else:
            # 停止定时器
            if self.auto_timer:
                self.auto_timer.stop()
            
            self.tray.show_message("StealthNovel", "自动推进已关闭")
            logger.info("自动推进已关闭")
    
    def _auto_advance_tick(self):
        """自动推进定时器回调"""
        advance_by = self.config.get("advance_by", "char")
        if advance_by == "line":
            self.advance_line()
        else:
            self.advance_char()
    
    def reset_progress(self):
        """重置阅读进度"""
        self.state.reset()
        self.render_current()
        self.tray.show_message("StealthNovel", "进度已重置")
        logger.info("进度已重置")
    
    def load_file_dialog(self):
        """打开文件选择对话框"""
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "选择文本文件",
            "",
            "文本文件 (*.txt);;所有文件 (*.*)"
        )
        
        if file_path:
            from .utils.files import read_local_file
            text = read_local_file(file_path)
            if text:
                self.load_text(text)
                self.tray.show_message("StealthNovel", "文件已加载")
    
    def load_from_clipboard(self):
        """从剪贴板加载"""
        from .utils.files import read_from_clipboard
        text = read_from_clipboard()
        if text:
            self.load_text(text)
            self.tray.show_message("StealthNovel", "剪贴板内容已加载")
        else:
            self.tray.show_message("StealthNovel", "剪贴板为空")
    
    def quit(self):
        """退出应用"""
        # 保存状态
        self.state.save()
        
        # 清理资源
        self.hotkey_manager.unregister_all()
        if self.current_mode:
            self.current_mode.cleanup()
        
        logger.info("应用退出")
        self.app.quit()
    
    def run(self):
        """运行应用"""
        return self.app.exec()


def main():
    """主函数"""
    try:
        app = StealthNovelApp()
        sys.exit(app.run())
    except Exception as e:
        logger.error(f"应用运行错误: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()


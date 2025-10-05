"""全局热键管理模块"""

import keyboard
from typing import Callable, Dict, Optional

from ..utils.logger import logger


class HotkeyManager:
    """全局热键管理器"""
    
    def __init__(self):
        """初始化热键管理器"""
        self.registered_hotkeys: Dict[str, Callable] = {}
    
    def register(self, hotkey: str, callback: Callable, description: str = ""):
        """
        注册全局热键
        
        Args:
            hotkey: 热键字符串 (如 'right', 'ctrl+shift+m')
            callback: 回调函数
            description: 热键描述
        """
        try:
            keyboard.add_hotkey(hotkey, callback, suppress=False)
            self.registered_hotkeys[hotkey] = callback
            logger.info(f"注册热键: {hotkey} - {description}")
        except Exception as e:
            logger.error(f"注册热键失败 {hotkey}: {e}")
    
    def unregister(self, hotkey: str):
        """
        注销热键
        
        Args:
            hotkey: 热键字符串
        """
        try:
            if hotkey in self.registered_hotkeys:
                keyboard.remove_hotkey(hotkey)
                del self.registered_hotkeys[hotkey]
                logger.info(f"注销热键: {hotkey}")
        except Exception as e:
            logger.error(f"注销热键失败 {hotkey}: {e}")
    
    def unregister_all(self):
        """注销所有热键"""
        for hotkey in list(self.registered_hotkeys.keys()):
            self.unregister(hotkey)
    
    def register_from_config(self, config: dict, callbacks: dict):
        """
        从配置注册热键
        
        Args:
            config: 热键配置字典
            callbacks: 回调函数字典
        """
        for action, hotkey in config.items():
            if action in callbacks:
                self.register(hotkey, callbacks[action], action)


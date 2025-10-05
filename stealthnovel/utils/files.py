"""文件读取工具模块"""

import hashlib
from pathlib import Path
from typing import Optional

import requests
import pyperclip

from .logger import logger


def read_local_file(path: str) -> Optional[str]:
    """
    读取本地文本文件
    
    Args:
        path: 文件路径
        
    Returns:
        文件内容，读取失败返回 None
    """
    try:
        file_path = Path(path)
        if not file_path.exists():
            logger.error(f"文件不存在: {path}")
            return None
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        logger.info(f"成功读取本地文件: {path}")
        return content
    except Exception as e:
        logger.error(f"读取文件失败 {path}: {e}")
        return None


def read_from_url(url: str, timeout: int = 10) -> Optional[str]:
    """
    从 URL 读取文本
    
    Args:
        url: 文本 URL
        timeout: 超时时间（秒）
        
    Returns:
        文本内容，读取失败返回 None
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or "utf-8"
        
        logger.info(f"成功从 URL 读取: {url}")
        return response.text
    except Exception as e:
        logger.error(f"从 URL 读取失败 {url}: {e}")
        return None


def read_from_clipboard() -> Optional[str]:
    """
    从剪贴板读取文本
    
    Returns:
        剪贴板内容，读取失败返回 None
    """
    try:
        content = pyperclip.paste()
        if not content:
            logger.warning("剪贴板为空")
            return None
        
        logger.info("成功从剪贴板读取")
        return content
    except Exception as e:
        logger.error(f"从剪贴板读取失败: {e}")
        return None


def compute_hash(text: str) -> str:
    """
    计算文本的 SHA256 哈希值
    
    Args:
        text: 文本内容
        
    Returns:
        SHA256 哈希值（十六进制字符串）
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_text_from_source(source_type: str, path: str = "", url: str = "") -> Optional[str]:
    """
    根据来源类型加载文本
    
    Args:
        source_type: 来源类型 (file/clipboard/url)
        path: 文件路径（当 source_type 为 file 时）
        url: URL 地址（当 source_type 为 url 时）
        
    Returns:
        文本内容，加载失败返回 None
    """
    if source_type == "file":
        return read_local_file(path)
    elif source_type == "url":
        return read_from_url(url)
    elif source_type == "clipboard":
        return read_from_clipboard()
    else:
        logger.error(f"未知的来源类型: {source_type}")
        return None


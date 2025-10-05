"""PyInstaller 打包脚本"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


def clean_build():
    """清理构建目录"""
    dirs_to_clean = ['build', 'dist']
    for dir_name in dirs_to_clean:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"已清理: {dir_name}")


def build_exe():
    """使用 PyInstaller 构建可执行文件"""
    print("开始构建 StealthNovel.exe...")
    
    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name=StealthNovel',
        '--onefile',
        '--windowed',
        '--add-data=config;config',
        '--add-data=novel.txt;.',
        '--hidden-import=PySide6',
        '--hidden-import=keyboard',
        '--hidden-import=requests',
        '--hidden-import=pyperclip',
        '--icon=icon.png',  # 使用项目图标
        'stealthnovel/__main__.py'
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ 构建成功！")
        print(f"可执行文件位于: dist/StealthNovel.exe")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 构建失败: {e}")
        sys.exit(1)


def copy_resources():
    """复制必要资源到 dist 目录"""
    dist_dir = Path('dist')
    if not dist_dir.exists():
        return
    
    # 复制配置文件夹
    config_src = Path('config')
    config_dst = dist_dir / 'config'
    if config_src.exists():
        shutil.copytree(config_src, config_dst, dirs_exist_ok=True)
        print(f"已复制: config -> dist/config")
    
    # 复制示例文本
    novel_src = Path('novel.txt')
    novel_dst = dist_dir / 'novel.txt'
    if novel_src.exists():
        shutil.copy2(novel_src, novel_dst)
        print(f"已复制: novel.txt -> dist/novel.txt")
    
    # 复制 README
    readme_src = Path('README.md')
    readme_dst = dist_dir / 'README.txt'
    if readme_src.exists():
        shutil.copy2(readme_src, readme_dst)
        print(f"已复制: README.md -> dist/README.txt")


def main():
    """主函数"""
    print("=" * 50)
    print("StealthNovel 打包工具")
    print("=" * 50)
    
    # 清理旧的构建
    clean_build()
    
    # 构建可执行文件
    build_exe()
    
    # 复制资源
    copy_resources()
    
    print("\n" + "=" * 50)
    print("打包完成！")
    print("=" * 50)
    print("\n发布文件在 dist 目录中")


if __name__ == "__main__":
    main()


@echo off
REM 设置 UTF-8 编码，避免中文乱码
chcp 65001 >nul

title StealthNovel 启动器

echo.
echo ═══════════════════════════════════════
echo     📖 StealthNovel 隐蔽小说阅读器
echo ═══════════════════════════════════════
echo.
echo 正在启动...
echo.

REM 检查 Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误：未检测到 Python
    echo.
    echo 请先安装 Python 3.9 或更高版本
    echo 下载地址：https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM 检查 PySide6
python -c "import PySide6" 2>nul
if %errorlevel% neq 0 (
    echo ⏳ 首次运行，正在安装依赖...
    echo.
    pip install PySide6
    echo.
    if %errorlevel% neq 0 (
        echo ❌ 安装失败
        pause
        exit /b 1
    )
    echo ✓ 依赖安装完成
    echo.
)

echo ✓ 环境检查通过
echo ▶️ 启动程序...
echo.

REM 启动程序
python StealthNovel_Simple.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ 程序运行出错
    pause
)


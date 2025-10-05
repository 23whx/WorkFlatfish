@echo off
chcp 65001 >nul
echo ================================================
echo 启动 StealthNovel
echo ================================================
echo.

REM 检查虚拟环境
if exist .venv\Scripts\activate.bat (
    echo 使用虚拟环境...
    call .venv\Scripts\activate.bat
)

REM 检查依赖
python -c "import PySide6" 2>nul
if %errorlevel% neq 0 (
    echo PySide6 未安装，正在安装...
    pip install PySide6
)

echo 启动程序...
python StealthNovel_Simple.py

pause


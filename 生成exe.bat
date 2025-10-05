@echo off
chcp 65001 >nul
echo ================================================
echo StealthNovel 打包工具
echo ================================================
echo.

echo [1/3] 检查 PyInstaller...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller 未安装，正在安装...
    pip install pyinstaller
) else (
    echo PyInstaller 已安装
)
echo.

echo [2/3] 开始打包...
pyinstaller --noconfirm --onefile --windowed --name="StealthNovel" --icon=icon.png StealthNovel_Simple.py

if %errorlevel% equ 0 (
    echo.
    echo [3/3] 打包成功！
    echo.
    echo ================================================
    echo 可执行文件位置: dist\StealthNovel.exe
    echo ================================================
    echo.
    echo 双击 dist\StealthNovel.exe 运行程序
    echo.
    
    REM 打开 dist 文件夹
    explorer dist
) else (
    echo.
    echo [错误] 打包失败！
    echo.
)

pause


@echo off
chcp 65001 >nul
echo ================================================
echo 修复 Windows 终端中文乱码问题
echo ================================================
echo.
echo 正在设置终端编码为 UTF-8...
echo.

REM 设置当前会话
chcp 65001

echo.
echo ✓ 当前终端已设置为 UTF-8 编码
echo.
echo 注意：这个设置只对当前终端有效
echo 下次打开终端需要重新运行此脚本
echo.
echo 或者使用 "快速运行.bat" 自动设置编码
echo.

pause


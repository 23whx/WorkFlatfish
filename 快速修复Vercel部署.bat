@echo off
chcp 65001 >nul
echo ========================================
echo   修复 Vercel 部署 404 问题
echo ========================================
echo.

echo [检查] 检查 web 目录...
if not exist web\index.html (
    echo ❌ 错误：web\index.html 不存在！
    echo.
    echo 📝 请确保已运行项目代码创建了 web\index.html
    pause
    exit /b 1
) else (
    echo ✅ web\index.html 存在
)

echo.
echo [检查] 检查其他必需文件...

set missing=0

if not exist web\styles.css (
    echo ❌ web\styles.css 缺失
    set missing=1
) else (
    echo ✅ web\styles.css 存在
)

if not exist web\script.js (
    echo ❌ web\script.js 缺失
    set missing=1
) else (
    echo ✅ web\script.js 存在
)

if not exist web\icon.png (
    echo ❌ web\icon.png 缺失
    set missing=1
) else (
    echo ✅ web\icon.png 存在
)

if %missing%==1 (
    echo.
    echo ⚠️ 警告：某些文件缺失，可能影响网站显示
    echo.
)

echo.
echo [Git] 检查 Git 状态...
git status >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 当前目录不是 Git 仓库
    echo.
    echo 请先初始化 Git 仓库：
    echo   git init
    echo   git add .
    echo   git commit -m "Initial commit"
    pause
    exit /b 1
)

echo ✅ Git 仓库存在
echo.

echo [Git] 查看未提交的更改...
git status -s
echo.

echo ========================================
echo   准备提交并推送到 GitHub
echo ========================================
echo.
echo 即将执行以下操作：
echo   1. git add web/index.html
echo   2. git commit -m "修复：添加缺失的 index.html"
echo   3. git push
echo.

set /p confirm="确认继续？(Y/N): "
if /i not "%confirm%"=="Y" (
    echo 取消操作
    pause
    exit /b 0
)

echo.
echo [Git] 添加文件...
git add web/index.html web/styles.css web/script.js web/icon.png web/sitemap.xml web/robots.txt vercel.json

echo.
echo [Git] 提交更改...
git commit -m "修复：添加缺失的 index.html 和其他必需文件"

if %errorlevel% neq 0 (
    echo.
    echo ℹ️ 没有新的更改需要提交
) else (
    echo ✅ 提交成功
)

echo.
echo [Git] 推送到 GitHub...
git push

if %errorlevel% neq 0 (
    echo.
    echo ❌ 推送失败
    echo.
    echo 可能的原因：
    echo   1. 还没有设置远程仓库
    echo   2. 没有配置 Git 凭据
    echo   3. 网络问题
    echo.
    echo 请手动执行：
    echo   git remote add origin https://github.com/你的用户名/StealthNovel.git
    echo   git push -u origin main
    pause
    exit /b 1
)

echo.
echo ========================================
echo   ✅ 修复完成！
echo ========================================
echo.
echo Vercel 会在 1-2 分钟内自动重新部署
echo.
echo 请访问：https://vercel.com/dashboard
echo 查看部署状态
echo.
echo 部署完成后，访问你的网站：
echo   https://你的项目名.vercel.app
echo.

pause


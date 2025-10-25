@echo off
chcp 65001 >nul
echo.
echo ================================
echo   图标修复部署脚本
echo ================================
echo.

echo [1/5] 检查文件状态...
git status
echo.

echo [2/5] 添加所有修改的文件...
git add web/favicon.ico
git add web/favicon.png
git add web/apple-touch-icon.png
git add web/manifest.json
git add web/browserconfig.xml
git add web/icon-test.html
git add web/ICON_TEST.md
git add web/index.html
git add vercel.json
git add .vercelignore
git add ICON_FIX_SUMMARY.md
git add DEPLOYMENT_CHECKLIST.md
echo ✓ 文件添加完成
echo.

echo [3/5] 提交更改...
git commit -m "fix: 修复导航站图标显示问题

- 添加 favicon.ico、favicon.png、apple-touch-icon.png 多种图标格式
- 更新 HTML 元数据，使用绝对 URL 路径
- 完善 Open Graph 和社交媒体分享配置
- 添加 PWA manifest.json 和 browserconfig.xml
- 配置 CORS 跨域访问支持
- 创建图标测试页面 (icon-test.html)
- 添加详细的测试文档和部署清单

修复内容：
- 导航站现在可以正确获取网站图标
- 支持多种图标格式和尺寸
- 优化了 SEO 和社交媒体分享
- 添加了完整的测试和验证工具"

echo ✓ 提交完成
echo.

echo [4/5] 推送到 GitHub...
git push origin main
echo ✓ 推送完成
echo.

echo [5/5] 等待 Vercel 自动部署...
echo.
echo ================================
echo   部署流程完成！
echo ================================
echo.
echo 接下来请执行以下验证步骤：
echo.
echo 1. 等待 2-5 分钟让 Vercel 完成部署
echo 2. 访问测试页面: https://work-flatfish.vercel.app/icon-test.html
echo 3. 确认所有图标都能正常加载
echo 4. 访问图标文件: https://work-flatfish.vercel.app/favicon.ico
echo 5. 在导航站 (oumashu.top) 上重新添加或更新网站
echo 6. 等待 24-48 小时让导航站更新缓存
echo.
echo 详细的验证步骤请查看: DEPLOYMENT_CHECKLIST.md
echo.
pause


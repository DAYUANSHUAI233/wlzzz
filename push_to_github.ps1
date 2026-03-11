# 上传代码到 GitHub 的脚本（PowerShell）

Write-Host "=========================================" -ForegroundColor Green
Write-Host "上传代码到 GitHub" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# 仓库地址
$REPO_URL = "https://github.com/DAYUANSHUAI233/wlzzz.git"

# 初始化 Git 仓库
Write-Host "1. 初始化 Git 仓库..." -ForegroundColor Cyan
git init
Write-Host "✓ Git 仓库初始化完成" -ForegroundColor Green
Write-Host ""

# 添加所有文件
Write-Host "2. 添加文件到暂存区..." -ForegroundColor Cyan
git add .
Write-Host "✓ 文件已添加" -ForegroundColor Green
Write-Host ""

# 提交代码
Write-Host "3. 提交代码..." -ForegroundColor Cyan
git commit -m "Initial commit - 股票市场数据中转站"
Write-Host "✓ 代码已提交" -ForegroundColor Green
Write-Host ""

# 连接远程仓库
Write-Host "4. 连接远程仓库..." -ForegroundColor Cyan
git remote add origin $REPO_URL
Write-Host "✓ 远程仓库已连接" -ForegroundColor Green
Write-Host ""

# 推送代码
Write-Host "5. 推送代码到 GitHub..." -ForegroundColor Cyan
git push -u origin main
Write-Host ""

Write-Host "=========================================" -ForegroundColor Green
Write-Host "✓ 代码已成功推送到 GitHub！" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "仓库地址: https://github.com/DAYUANSHUAI233/wlzzz" -ForegroundColor Yellow
Write-Host ""
Write-Host "下一步: 访问 https://vercel.com/new 导入仓库" -ForegroundColor Yellow
Write-Host ""

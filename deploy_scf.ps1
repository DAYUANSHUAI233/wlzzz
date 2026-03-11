# 腾讯云函数部署脚本 (Windows PowerShell 版本)
# 需要先安装腾讯云 CLI 工具: pip install tencentcloud-sdk-python

Write-Host "=========================================" -ForegroundColor Green
Write-Host "开始部署股票数据中转站到腾讯云 SCF" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""

# 检查 Python 环境
Write-Host "1. 检查 Python 环境..." -ForegroundColor Cyan
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python 版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: 未检测到 Python 环境" -ForegroundColor Red
    exit 1
}

# 检查腾讯云 CLI
Write-Host "2. 检查腾讯云 CLI..." -ForegroundColor Cyan
try {
    $cliVersion = tcloud version 2>&1
    Write-Host "✓ 腾讯云 CLI 已安装" -ForegroundColor Green
} catch {
    Write-Host "错误: 未检测到腾讯云 CLI" -ForegroundColor Red
    Write-Host "请执行: pip install tencentcloud-sdk-python" -ForegroundColor Yellow
    exit 1
}

# 安装依赖
Write-Host "3. 安装 Python 依赖..." -ForegroundColor Cyan
if (Test-Path "package") {
    Remove-Item -Recurse -Force "package"
}
New-Item -ItemType Directory -Path "package" | Out-Null
python -m pip install -r requirements.txt -t ./package --no-user
Write-Host "✓ 依赖安装完成" -ForegroundColor Green

# 打包代码
Write-Host "4. 打包代码文件..." -ForegroundColor Cyan
Copy-Item scf_handler.py,requirements.txt,template.yaml -Destination package -Force
Compress-Archive -Path package\* -DestinationPath function.zip -Force
Write-Host "✓ 代码打包完成: function.zip" -ForegroundColor Green

# 显示部署说明
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "打包完成！请手动部署到腾讯云 SCF" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "步骤说明:" -ForegroundColor Yellow
Write-Host "1. 访问腾讯云 SCF 控制台: https://console.cloud.tencent.com/scf" -ForegroundColor White
Write-Host "2. 创建函数或更新现有函数" -ForegroundColor White
Write-Host "3. 上传 function.zip 文件" -ForegroundColor White
Write-Host "4. 配置 API 网关触发器" -ForegroundColor White
Write-Host "5. 获取访问地址并测试" -ForegroundColor White
Write-Host ""
Write-Host "函数配置:" -ForegroundColor Yellow
Write-Host "- 函数名称: stock-market-proxy" -ForegroundColor White
Write-Host "- 运行环境: Python 3.9" -ForegroundColor White
Write-Host "- 入口函数: scf_handler.handler" -ForegroundColor White
Write-Host "- 内存大小: 256 MB" -ForegroundColor White
Write-Host "- 超时时间: 30 秒" -ForegroundColor White
Write-Host ""

# 清理临时文件
Write-Host "5. 清理临时文件..." -ForegroundColor Cyan
if (Test-Path "package") {
    Remove-Item -Recurse -Force "package"
}
Write-Host "✓ 清理完成" -ForegroundColor Green

Write-Host ""
Write-Host "打包完成！" -ForegroundColor Green

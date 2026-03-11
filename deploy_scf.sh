#!/bin/bash
# 腾讯云函数部署脚本
# 需要先安装腾讯云 CLI 工具: pip install tencentcloud-sdk-python

set -e

echo "========================================="
echo "开始部署股票数据中转站到腾讯云 SCF"
echo "========================================="
echo ""

# 检查是否已登录
echo "1. 检查认证配置..."
if ! tcloud configure list > /dev/null 2>&1; then
    echo "错误: 未检测到腾讯云 CLI 认证配置"
    echo "请先执行: tcloud configure"
    exit 1
fi
echo "✓ 认证配置已就绪"
echo ""

# 安装依赖
echo "2. 安装 Python 依赖..."
pip install -r requirements.txt -t ./package
echo "✓ 依赖安装完成"
echo ""

# 打包代码
echo "3. 打包代码文件..."
cd package
zip -r ../function.zip . > /dev/null
cd ..
zip -g function.zip scf_handler.py requirements.txt template.yaml
echo "✓ 代码打包完成: function.zip"
echo ""

# 部署函数
echo "4. 部署到腾讯云 SCF..."
FUNCTION_NAME="stock-market-proxy"
REGION="ap-guangzhou"  # 可根据需要修改区域

# 检查函数是否存在
if tcloud scf ListFunctions --Region $REGION | grep -q $FUNCTION_NAME; then
    echo "函数已存在，更新代码..."
    tcloud scf UpdateFunctionCode \
        --Region $REGION \
        --FunctionName $FUNCTION_NAME \
        --CosBucketName your-bucket-name \
        --CosObjectName /function.zip \
        --ZipFile fileb://function.zip
    echo "✓ 函数代码已更新"
else
    echo "创建新函数..."
    tcloud scf CreateFunction \
        --Region $REGION \
        --FunctionName $FUNCTION_NAME \
        --Runtime Python3.9 \
        --Handler scf_handler.handler \
        --MemorySize 256 \
        --Timeout 30 \
        --Code FileBase64=$(base64 -w 0 function.zip)
    echo "✓ 函数创建成功"
fi
echo ""

# 配置 API 网关触发器
echo "5. 配置 API 网关..."
echo "请在腾讯云控制台手动配置 API 网关触发器："
echo "  1. 进入函数详情页"
echo "  2. 点击'触发器管理' → '创建触发器'"
echo "  3. 选择'API 网关'触发器"
echo "  4. 路径配置为: /*"
echo ""

# 清理临时文件
echo "6. 清理临时文件..."
rm -rf package function.zip
echo "✓ 清理完成"
echo ""

echo "========================================="
echo "部署完成！"
echo "========================================="
echo ""
echo "函数名称: $FUNCTION_NAME"
echo "所在区域: $REGION"
echo ""
echo "后续步骤:"
echo "1. 在腾讯云 SCF 控制台配置 API 网关触发器"
echo "2. 获取 API 网关访问地址"
echo "3. 测试访问: https://your-api-gateway-url.com/all"
echo ""

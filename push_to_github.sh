#!/bin/bash
# 上传代码到 GitHub 的脚本

echo "========================================="
echo "上传代码到 GitHub"
echo "========================================="
echo ""

# 仓库地址
REPO_URL="https://github.com/DAYUANSHUAI233/wlzzz.git"

# 初始化 Git 仓库
echo "1. 初始化 Git 仓库..."
git init
echo "✓ Git 仓库初始化完成"
echo ""

# 添加所有文件
echo "2. 添加文件到暂存区..."
git add .
echo "✓ 文件已添加"
echo ""

# 提交代码
echo "3. 提交代码..."
git commit -m "Initial commit - 股票市场数据中转站"
echo "✓ 代码已提交"
echo ""

# 连接远程仓库
echo "4. 连接远程仓库..."
git remote add origin $REPO_URL
echo "✓ 远程仓库已连接"
echo ""

# 推送代码
echo "5. 推送代码到 GitHub..."
git push -u origin main
echo ""

echo "========================================="
echo "✓ 代码已成功推送到 GitHub！"
echo "========================================="
echo ""
echo "仓库地址: https://github.com/DAYUANSHUAI233/wlzzz"
echo ""
echo "下一步: 访问 https://vercel.com/new 导入仓库"
echo ""

# 上传代码到 GitHub 并部署到 Vercel

## 快速上传步骤

### Windows 用户

打开 PowerShell，执行：

```powershell
cd c:\Users\dys\Desktop\网络中转站
.\push_to_github.ps1
```

### Linux/Mac 用户

```bash
cd ~/Desktop/网络中转站
chmod +x push_to_github.sh
./push_to_github.sh
```

---

## 手动上传步骤

如果脚本执行失败，可以手动执行以下步骤：

### 步骤 1: 打开终端

在项目目录打开 PowerShell 或 CMD

```bash
cd c:\Users\dys\Desktop\网络中转站
```

### 步骤 2: 初始化 Git 仓库

```bash
git init
```

### 步骤 3: 添加所有文件

```bash
git add .
```

### 步骤 4: 提交代码

```bash
git commit -m "Initial commit - 股票市场数据中转站"
```

### 步骤 5: 连接远程仓库

```bash
git remote add origin https://github.com/DAYUANSHUAI233/wlzzz.git
```

### 步骤 6: 推送代码

```bash
git push -u origin main
```

**注意**: 如果推送失败，尝试使用 `master` 分支：

```bash
git branch -M master
git push -u origin master
```

---

## 可能遇到的问题

### 问题 1: 提示 "fatal: not a git repository"

**解决**: 确保在正确的目录执行命令

```bash
cd c:\Users\dys\Desktop\网络中转站
git init
```

### 问题 2: 推送失败，提示 "remote: Permission denied"

**解决**: 需要配置 GitHub 认证

**方式 A**: 使用 GitHub Personal Access Token
1. 访问：https://github.com/settings/tokens
2. 生成新的 Token（勾选 `repo` 权限）
3. 复制 Token
4. 执行：
   ```bash
   git push https://YOUR_TOKEN@github.com/DAYUANSHUAI233/wlzzz.git main
   ```

**方式 B**: 使用 GitHub CLI
```bash
gh auth login
git push -u origin main
```

### 问题 3: 提示 "error: src refspec main does not match any"

**解决**: 使用 `master` 分支

```bash
git branch -M master
git push -u origin master
```

---

## 代码推送成功后

### 下一步：在 Vercel 导入项目

1. **访问 Vercel**: https://vercel.com/new

2. **选择 GitHub**
   - 点击 "Continue with GitHub"
   - 授权访问你的 GitHub 账号

3. **导入仓库**
   - 在仓库列表中找到 `wlzzz`
   - 点击 "Import"

4. **配置项目**
   - Project Name: `wlzzz`（或自定义）
   - Framework Preset: 自动检测（Python）
   - Root Directory: `./`
   - Build Command: 自动生成
   - Output Directory: 自动生成

5. **点击 Deploy**
   - 等待 1-2 分钟
   - 部署完成！

### 访问你的 API

部署成功后，Vercel 会显示访问地址：

```
https://wlzzz.vercel.app
```

测试接口：

```bash
# 聚合接口
https://wlzzz.vercel.app/all

# 板块排名
https://wlzzz.vercel.app/plates

# 市场情绪
https://wlzzz.vercel.app/market/mood
```

---

## 验证代码已上传

上传成功后，访问 GitHub 仓库查看：

https://github.com/DAYUANSHUAI233/wlzzz

确认文件列表包含：

- `api/index.py` - Vercel 函数代码
- `vercel.json` - Vercel 配置
- `requirements-vercel.txt` - 依赖文件
- `README.md` - 说明文档

---

## 下一步

代码上传成功后，继续在 Vercel 导入并部署项目。

详细部署步骤请查看：`DEPLOY_VERCEL.md`

---

**需要帮助？**

查看详细文档：`DEPLOY_VERCEL.md` 或 `QUICKSTART_VERCEL.md`

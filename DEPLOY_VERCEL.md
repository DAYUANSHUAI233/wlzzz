# Vercel 部署指南 - 股票市场数据中转站

本文档详细介绍如何将股票市场数据中转站部署到 Vercel 平台。

---

## 为什么选择 Vercel？

| 特性 | 说明 |
|------|------|
| **完全免费** | 无限请求，100GB 带宽/月 |
| **零配置** | 自动部署，无需手动配置 |
| **全球 CDN** | 自动部署到全球边缘节点 |
| **GitHub 集成** | 推送代码自动部署 |
| **自定义域名** | 支持绑定自己的域名 |
| **零运维** | 无需管理服务器 |

---

## 方法一：通过 Vercel CLI 部署（推荐）

### 步骤 1: 安装 Node.js

Vercel CLI 需要 Node.js 环境。

下载地址：https://nodejs.org/

验证安装：

```bash
node --version
npm --version
```

### 步骤 2: 安装 Vercel CLI

```bash
npm install -g vercel
```

### 步骤 3: 登录 Vercel

```bash
vercel login
```

选择登录方式（推荐使用 GitHub）：

1. 选择 "Continue with GitHub"
2. 在浏览器中授权
3. 回到终端确认登录成功

### 步骤 4: 准备项目文件

确保项目目录包含以下文件：

```
网络中转站/
├── api/
│   └── index.py
├── vercel.json
├── requirements-vercel.txt
└── README.md
```

### 步骤 5: 部署项目

在项目根目录执行：

```bash
cd c:\Users\dys\Desktop\网络中转站
vercel
```

按照提示操作：

```
? Set up and deploy "网络中转站"? [Y/n] Y
? Which scope do you want to deploy to? Your Name
? Link to existing project? [y/N] N
? What's your project's name? stock-market-proxy
? In which directory is your code located? ./
```

等待部署完成（约 1-2 分钟）。

### 步骤 6: 验证部署

部署成功后会显示：

```
✅ Production: https://stock-market-proxy.vercel.app
```

在浏览器中访问测试：

```
https://stock-market-proxy.vercel.app/all
```

---

## 方法二：通过 GitHub 部署（最简单）

### 步骤 1: 推送代码到 GitHub

```bash
# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit"

# 连接 GitHub 仓库
git remote add origin https://github.com/your-username/your-repo.git

# 推送代码
git push -u origin main
```

### 步骤 2: 在 Vercel 导入项目

1. 访问：https://vercel.com/new
2. 点击 "Import Git Repository"
3. 选择刚才创建的 GitHub 仓库
4. 点击 "Import"

### 步骤 3: 配置项目

Vercel 会自动检测项目配置，点击 **Deploy** 即可。

### 步骤 4: 等待部署

约 1-2 分钟后部署完成，访问：
```
https://your-repo.vercel.app
```

---

## 方法三：使用 Vercel 网页版（无需 CLI）

### 步骤 1: 创建项目

1. 访问：https://vercel.com/new
2. 点击 "Continue with GitHub"
3. 授权访问你的 GitHub 账号

### 步骤 2: 上传代码

由于网页版不支持直接上传代码，需要：

**选项 A**: 使用 GitHub（推荐）
- 将代码推送到 GitHub
- 按照"方法二"操作

**选项 B**: 使用 GitLab / Bitbucket
- 将代码推送到 GitLab 或 Bitbucket
- 在 Vercel 导入对应仓库

---

## 配置说明

### vercel.json 文件

```json
{
  "functions": {
    "api/**/*.py": {
      "maxDuration": 30
    }
  },
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/api/index.py"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Access-Control-Allow-Origin",
          "value": "*"
        }
      ]
    }
  ]
}
```

### 关键配置项

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `maxDuration` | 函数最大执行时间（秒） | 30 |
| `functions` | 函数配置对象 | 无 |
| `rewrites` | URL 重写规则 | 无 |
| `headers` | HTTP 头配置 | 无 |

### 修改执行时间

如果需要更长的执行时间，修改 `vercel.json`：

```json
"functions": {
  "api/**/*.py": {
    "maxDuration": 60  // 改为 60 秒
  }
}
```

---

## 环境变量

如果需要使用环境变量（如 API 密钥），在 Vercel 控制台配置：

1. 进入项目设置：Settings → Environment Variables
2. 添加环境变量：
   - Name: `API_KEY`
   - Value: `your-api-key`
   - Environment: Production / Preview / Development

在代码中读取：

```python
import os
api_key = os.getenv('API_KEY')
```

---

## 自定义域名

### 步骤 1: 添加域名

1. 进入项目：Settings → Domains
2. 点击 "Add Domain"
3. 输入你的域名，如 `api.yourdomain.com`

### 步骤 2: 配置 DNS

Vercel 会显示 DNS 配置信息：

```
Type: CNAME
Name: api.yourdomain.com
Value: cname.vercel-dns.com
```

在域名服务商添加对应的 DNS 记录。

### 步骤 3: 验证

DNS 生效后，访问自定义域名测试。

---

## 查看日志和监控

### 查看函数日志

1. 进入项目：Logs
2. 查看实时日志和历史日志
3. 筛选函数：`api/index.py`

### 查看监控数据

1. 进入项目：Analytics
2. 查看：
   - 请求数量
   - 响应时间
   - 错误率
   - 带宽使用

---

## 更新项目

### 方式一：使用 CLI

修改代码后执行：

```bash
vercel --prod
```

### 方式二：通过 GitHub

1. 修改代码
2. 提交并推送到 GitHub
3. Vercel 自动部署

---

## 回滚版本

如果新版本有问题，可以回滚到之前的版本：

1. 进入项目：Deployments
2. 找到之前的版本
3. 点击三个点 → "Promote to Production"
4. 选择 "Rollback to this deployment"

---

## 删除项目

如果需要删除项目：

1. 进入项目：Settings → General
2. 滚动到底部
3. 点击 "Delete Project"
4. 确认删除

---

## 常见问题

### Q1: 部署失败怎么办？

**A**: 检查以下几点：

1. 确认 `requirements-vercel.txt` 文件存在
2. 确认 `api/index.py` 文件存在
3. 查看部署日志定位具体错误

### Q2: 函数执行超时怎么办？

**A**: 增加执行时间：

```json
"functions": {
  "api/index.py": {
    "maxDuration": 60
  }
}
```

### Q3: 如何查看详细错误信息？

**A**: 在 Vercel 控制台查看：

1. 进入项目：Deployments
2. 点击失败的部署
3. 查看 "Build Log" 和 "Function Logs"

### Q4: 冷启动慢怎么办？

**A**: 这是正常现象。首次调用可能有 50-200ms 延迟，后续调用会更快。

### Q5: 如何配置多个环境？

**A**: 在 Vercel 中默认有三个环境：

- **Production**: 生产环境
- **Preview**: 预览环境（每次 PR 自动创建）
- **Development**: 开发环境（`vercel dev` 命令）

---

## 性能优化

### 1. 启用缓存

在代码中添加缓存逻辑，减少 API 调用：

```python
import time
from datetime import datetime

CACHE = {}

def get_with_cache(key, ttl=60):
    now = time.time()
    if key in CACHE and now - CACHE[key]['time'] < ttl:
        return CACHE[key]['data']

    data = fetch_data()
    CACHE[key] = {
        'data': data,
        'time': now
    }
    return data
```

### 2. 使用 CDN

Vercel 自动使用 CDN，无需额外配置。

### 3. 优化响应时间

- 减少 API 调用次数
- 使用并发请求（需要重构代码）
- 增加缓存时间

---

## 成本估算

| 项目 | 免费额度 | 实际使用（日均 1000 次） |
|------|----------|-------------------------|
| 请求次数 | 无限制 | 约 30,000 次/月 |
| 带宽 | 100GB/月 | 约 500MB/月 |
| 函数执行 | 100GB-Hours/月 | 约 0.5GB-Hours/月 |
| **成本** | **完全免费** | **$0** |

---

## 下一步

1. 测试所有 API 接口
2. 配置自定义域名（可选）
3. 设置环境变量（如果需要）
4. 配置监控告警（可选）
5. 优化性能（添加缓存等）

---

## 技术支持

- [Vercel 官方文档](https://vercel.com/docs)
- [Vercel 社区](https://vercel.com/community)
- [Vercel GitHub](https://github.com/vercel/vercel)

---

**恭喜！您已成功将股票数据中转站部署到 Vercel！** 🎉

访问您的 API：`https://your-project.vercel.app/all`

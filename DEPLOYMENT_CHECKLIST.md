# Vercel 部署检查清单

## ✅ 已完成的准备工作

- [x] 创建 Vercel 函数代码 (`api/index.py`)
- [x] 修复 Vercel handler 函数
- [x] 创建 Vercel 配置文件 (`vercel.json`)
- [x] 创建 Python 依赖文件 (`requirements-vercel.txt`)
- [x] 创建运行时配置 (`runtime.txt`)
- [x] 推送代码到 GitHub

## 📋 部署前检查

### GitHub 仓库检查

访问：https://github.com/DAYUANSHUAI233/wlzzz

确认以下文件存在：
- [ ] `api/index.py` - Vercel 函数代码
- [ ] `vercel.json` - Vercel 配置
- [ ] `requirements-vercel.txt` - Python 依赖
- [ ] `runtime.txt` - Python 版本配置
- [ ] `README.md` - 说明文档

### Vercel 账户检查

- [ ] 已注册 Vercel 账号
- [ ] 已连接 GitHub 账号

---

## 🚀 部署步骤

### 1. 访问 Vercel

打开：https://vercel.com/new

### 2. 连接 GitHub

1. 点击 **"Continue with GitHub"**
2. 在弹出的窗口中授权
3. 点击 **"Authorize Vercel"**

### 3. 导入仓库

1. 在仓库列表中找到 `DAYUANSHUAI233/wlzzz`
2. 点击 **"Import"**

### 4. 配置项目

确认以下配置：

| 配置项 | 值 | 状态 |
|--------|-----|------|
| **Project Name** | `wlzzz` | [ ] 已确认 |
| **Framework Preset** | Other | [ ] 已确认 |
| **Root Directory** | `./` | [ ] 已确认 |
| **Build Command** | （自动生成） | [ ] 已确认 |
| **Output Directory** | （自动生成） | [ ] 已确认 |
| **Install Command** | `pip install -r requirements-vercel.txt` | [ ] 已确认 |

### 5. 开始部署

点击 **"Deploy"** 按钮

### 6. 等待部署

等待 1-2 分钟，查看部署进度

### 7. 部署完成

看到以下信息表示成功：

```
✅ Production: https://wlzzz.vercel.app
```

---

## 🧪 部署后测试

### 基础测试

在浏览器中访问以下链接：

| 接口 | URL | 预期结果 |
|------|-----|----------|
| **聚合接口** | `https://wlzzz.vercel.app/all` | 返回 JSON 数据 |
| **板块排名** | `https://wlzzz.vercel.app/plates` | 返回板块列表 |
| **市场情绪** | `https://wlzzz.vercel.app/market/mood` | 返回情绪数据 |

### 详细测试

测试所有接口：

```bash
# 聚合接口
curl https://wlzzz.vercel.app/all

# 板块排名
curl https://wlzzz.vercel.app/plates

# 成分股
curl https://wlzzz.vercel.app/stocks/BK01234

# 市场数据
curl https://wlzzz.vercel.app/market/updown
curl https://wlzzz.vercel.app/market/retrace
curl https://wlzzz.vercel.app/market/volume
curl https://wlzzz.vercel.app/market/mood

# 日期相关（替换 YYYYMMDD）
curl https://wlzzz.vercel.app/market/loss/20260312
curl https://wlzzz.vercel.app/market/trend/20260312

# 默认交易日
curl https://wlzzz.vercel.app/market/days
```

---

## 🔍 故障排查

### 问题 1: 部署失败 - 构建错误

**症状**: Build Log 显示 Python 安装失败

**解决**:
1. 确认 `runtime.txt` 文件存在
2. 确认 `requirements-vercel.txt` 文件存在
3. 查看详细的 Build Log

### 问题 2: 部署失败 - 函数错误

**症状**: Function Log 显示错误

**解决**:
1. 查看 Function Log
2. 检查 `api/index.py` 语法
3. 确认所有依赖已安装

### 问题 3: 部署成功但访问 404

**症状**: 访问 URL 返回 404

**解决**:
1. 确认访问正确的 URL
2. 检查 `vercel.json` 路由配置
3. 查看 Vercel 控制台的 Deployments

### 问题 4: 函数超时

**症状**: 访问超时

**解决**:
1. 进入 Vercel 项目 → Settings → Functions
2. 增加 `maxDuration` 到 60 秒
3. 重新部署

### 问题 5: CORS 错误

**症状**: 浏览器控制台显示 CORS 错误

**解决**:
1. 确认 `vercel.json` 中配置了 CORS headers
2. 检查 `api/index.py` 中的 CORS 响应头
3. 确认前端请求的 origin 被允许

---

## 📊 监控和维护

### 查看日志

1. 进入 Vercel 项目 → Logs
2. 筛选函数：`api/index.py`
3. 查看实时日志和历史日志

### 查看分析

1. 进入 Vercel 项目 → Analytics
2. 查看：
   - 请求数量
   - 响应时间
   - 错误率
   - 带宽使用

### 更新代码

修改代码后：

```powershell
cd c:\Users\dys\Desktop\网络中转站
git add .
git commit -m "Update code"
git push
```

Vercel 会自动重新部署！

---

## 🎯 成功标准

### 部署成功

✅ Vercel 控制台显示部署成功
✅ 获得 `https://wlzzz.vercel.app` 访问地址

### 接口正常

✅ 访问 `/all` 返回完整数据
✅ 访问 `/plates` 返回板块排名
✅ 访问 `/market/mood` 返回市场情绪
✅ 所有接口返回 JSON 格式数据
✅ 响应时间 < 5 秒

### 成本控制

✅ 在免费额度内
✅ 无意外费用

---

## 📞 获取帮助

### 文档

- Vercel 官方文档: https://vercel.com/docs
- Vercel Python 运行时: https://vercel.com/docs/functions/runtimes/python

### 支持

- Vercel 社区: https://vercel.com/community
- Vercel GitHub: https://github.com/vercel/vercel

### 项目文档

- `README.md` - 项目说明
- `DEPLOY_VERCEL.md` - 详细部署指南
- `QUICKSTART_VERCEL.md` - 快速部署卡

---

## 🎉 完成部署后

部署成功后，您将拥有：

✅ 一个完全免费的股票数据 API 服务
✅ 全球 CDN 加速
✅ 自动扩缩容
✅ 零运维
✅ 自定义域名支持（可选）

### 下一步优化

1. 添加缓存层（减少 API 调用）
2. 配置自定义域名
3. 设置环境变量（如需要）
4. 配置监控告警
5. 优化性能

---

**现在开始部署吧！访问：https://vercel.com/new**

祝您部署成功！🚀

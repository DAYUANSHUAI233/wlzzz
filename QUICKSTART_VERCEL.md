# Vercel 快速部署卡 - 5 分钟完成部署

## 方法一：CLI 部署（推荐）

```bash
# 1. 安装 Vercel CLI
npm install -g vercel

# 2. 登录
vercel login

# 3. 部署
cd c:\Users\dys\Desktop\网络中转站
vercel
```

完成！访问：`https://your-project.vercel.app/all`

---

## 方法二：GitHub 部署（最简单）

```bash
# 1. 推送代码到 GitHub
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/repo.git
git push -u origin main
```

然后访问 https://vercel.com/new 导入仓库。

---

## API 接口测试

部署成功后，在浏览器访问：

| 接口 | 地址 |
|------|------|
| **聚合接口** | `https://your-project.vercel.app/all` |
| **板块排名** | `https://your-project.vercel.app/plates` |
| **市场情绪** | `https://your-project.vercel.app/market/mood` |
| **量能数据** | `https://your-project.vercel.app/market/volume` |

---

## 免费额度

✅ **无限请求**
✅ **100GB 带宽/月**
✅ **完全免费**

---

## 更新项目

```bash
# 修改代码后重新部署
vercel --prod
```

---

## 查看日志

访问 Vercel 控制台：https://vercel.com/dashboard

---

**详细文档请查看 `DEPLOY_VERCEL.md`** 📖

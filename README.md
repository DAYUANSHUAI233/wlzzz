# 股票市场数据中转站

基于 Vercel 部署的股票市场数据聚合 API 服务。

---

## 快速开始

### 1. 部署到 Vercel

#### 方法一：使用 Vercel CLI

```bash
# 安装 Vercel CLI
npm install -g vercel

# 登录 Vercel
vercel login

# 部署
vercel
```

#### 方法二：通过 GitHub 部署

1. 将代码推送到 GitHub 仓库
2. 访问 https://vercel.com/new
3. 导入 GitHub 仓库
4. 点击 **Deploy**

### 2. 访问接口

部署成功后，访问：
- `https://your-project.vercel.app/` - 聚合接口
- `https://your-project.vercel.app/plates` - 板块排名
- `https://your-project.vercel.app/market/mood` - 市场情绪

---

## API 接口

### 基础接口

| 路由 | 说明 |
|------|------|
| `/` | 获取板块排名 + TOP3 成分股 |
| `/plates` | 仅获取板块排名 |
| `/stocks/<plate_id>` | 获取指定板块成分股 |

### 市场数据接口

| 路由 | 说明 |
|------|------|
| `/market/updown` | 上涨下跌家数统计 |
| `/market/retrace` | 大幅回撤与综合强度 |
| `/market/volume` | 量能数据 |
| `/market/mood` | 市场情绪核心数据 |
| `/market/loss/<date>` | 大跌回撤统计 (YYYYMMDD) |
| `/market/trend/<date>` | 资金趋势数据 (YYYYMMDD) |
| `/market/days` | 获取默认交易日 |

### 聚合接口

| 路由 | 说明 |
|------|------|
| `/all` | 聚合所有市场数据 + 题材前 10 名 |

---

## 免费额度

- **请求次数**: 无限制
- **带宽**: 100GB/月
- **函数执行**: 100GB-Hours/月
- **成本**: 完全免费

---

## 项目结构

```
网络中转站/
├── api/
│   └── index.py           # Vercel Serverless Function
├── vercel.json            # Vercel 配置
├── requirements-vercel.txt # Python 依赖
├── .vercelignore          # 忽略文件
└── README.md              # 本文件
```

---

## 开发

### 本地测试

```bash
# 安装依赖
pip install -r requirements-vercel.txt

# 运行本地服务器
python -m http.server 8000
```

### 查看日志

访问 Vercel 控制台查看函数日志和监控数据。

---

## 注意事项

1. **函数超时**: 默认 30 秒，可在 `vercel.json` 中修改
2. **冷启动**: 首次调用可能有 50-200ms 延迟
3. **CORS**: 已配置允许跨域访问

---

## 技术支持

- [Vercel 文档](https://vercel.com/docs)
- [Vercel Python 运行时](https://vercel.com/docs/functions/runtimes/python)

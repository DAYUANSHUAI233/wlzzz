# 股票市场数据中转站 - 无服务器部署指南

## 项目概述

本项目将本地 Flask 应用转换为腾讯云无服务器函数（SCF），实现股票市场数据的聚合中转服务。

### 主要功能

- **板块排名**: 获取实时题材板块排名
- **成分股查询**: 查询指定板块的成分股列表
- **市场情绪**: 包含上涨下跌家数、大幅回撤、量能数据等
- **涨停统计**: 首板、二板、三板等连板数据
- **资金趋势**: 涨停排队资金、成交资金等
- **聚合接口**: `/all` 提供所有数据的统一返回

---

## 快速开始

### 前置要求

1. 腾讯云账号（已注册并开通云函数 SCF 服务）
2. Python 3.9+ 环境
3. Git（可选）

### 部署方式选择

本项目提供三种部署方式：

1. **控制台手动部署**（推荐新手）
2. **CLI 自动部署**（推荐有经验用户）
3. **Serverless Framework 部署**（推荐自动化场景）

---

## 方式一：腾讯云控制台手动部署

### 步骤 1: 准备代码包

#### Windows 用户

```powershell
# 1. 进入项目目录
cd c:\Users\dys\Desktop\网络中转站

# 2. 执行打包脚本
.\deploy_scf.ps1
```

#### Linux/Mac 用户

```bash
# 1. 进入项目目录
cd ~/Desktop/网络中转站

# 2. 执行打包脚本
chmod +x deploy_scf.sh
./deploy_scf.sh
```

### 步骤 2: 创建云函数

1. 访问 [腾讯云 SCF 控制台](https://console.cloud.tencent.com/scf)
2. 选择地区（推荐：广州/深圳/北京）
3. 点击 **新建** → **从头新建**
4. 配置函数信息：

   | 配置项 | 值 |
   |--------|-----|
   | 函数名称 | `stock-market-proxy` |
   | 运行环境 | Python 3.9 |
   | 部署方式 | 本地上传 zip 包 |
   | 函数代码 | 上传 `function.zip` |
   | 入口函数 | `scf_handler.handler` |
   | 内存大小 | 256 MB |
   | 执行超时 | 30 秒 |
   | 环境变量 | `TZ=Asia/Shanghai` |

5. 点击 **完成**

### 步骤 3: 配置 API 网关

1. 进入函数详情页，点击 **触发器管理** → **创建触发器**
2. 选择触发器类型：**API 网关**
3. 配置网关信息：

   | 配置项 | 值 |
   |--------|-----|
   | API 服务 | 新建/使用已有 |
   | 请求方法 | ANY |
   | 路径 | `/*` |
   | 集成响应 | 启用 |

4. 点击 **提交**

### 步骤 4: 获取访问地址

1. 在触发器列表中找到 API 网关触发器
2. 点击 **访问路径** 复制完整的访问地址
3. 示例：`https://service-xxxxx.gz.apigw.tencentcs.com/release/`

### 步骤 5: 测试接口

```bash
# 测试聚合接口
curl https://your-api-gateway-url.com/all

# 测试板块排名
curl https://your-api-gateway-url.com/plates

# 测试市场情绪
curl https://your-api-gateway-url.com/market/mood
```

---

## 方式二：CLI 自动部署

### 安装腾讯云 CLI

```bash
pip install tencentcloud-sdk-python
```

### 配置认证

```bash
# 创建配置文件
mkdir -p ~/.tcloud
cat > ~/.tcloud/configure << EOF
[default]
tcloud_secret_id = YOUR_SECRET_ID
tcloud_secret_key = YOUR_SECRET_KEY
tcloud_region = ap-guangzhou
EOF
```

获取密钥：访问 [腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)

### 执行部署

#### Windows

```powershell
.\deploy_scf.ps1
```

#### Linux/Mac

```bash
chmod +x deploy_scf.sh
./deploy_scf.sh
```

### 配置 API 网关

CLI 部署后，仍需在控制台手动配置 API 网关触发器（参考方式一步骤 3）。

---

## 方式三：Serverless Framework 部署

### 安装 Serverless Framework

```bash
npm install -g serverless
```

### 安装腾讯云插件

```bash
npm install --save-dev serverless-tencent-scf
```

### 部署

```bash
# 部署到生产环境
serverless deploy --stage prod

# 部署到测试环境
serverless deploy --stage test
```

### 查看函数信息

```bash
# 查看函数详情
serverless info --stage prod

# 查看日志
serverless logs -f --stage prod

# 查看监控
serverless metrics --stage prod
```

---

## API 接口文档

### 基础路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 获取板块排名 + TOP3 成分股 |
| `/plates` | GET | 仅获取板块排名 |
| `/stocks/<plate_id>` | GET | 获取指定板块成分股 |

### 市场数据路由

| 路由 | 方法 | 说明 |
|------|------|------|
| `/market/updown` | GET | 上涨下跌家数统计 |
| `/market/retrace` | GET | 大幅回撤与综合强度 |
| `/market/volume` | GET | 量能数据 |
| `/market/mood` | GET | 市场情绪核心数据 |
| `/market/loss/<date>` | GET | 大跌回撤统计 (日期格式: YYYYMMDD) |
| `/market/trend/<date>` | GET | 资金趋势数据 (日期格式: YYYYMMDD) |
| `/market/days` | GET | 获取默认交易日 |

### 聚合接口

| 路由 | 方法 | 说明 |
|------|------|------|
| `/all` | GET | 聚合所有市场数据 + 题材前 10 名 |

### 响应示例

```json
{
  "timestamp": "2026-03-12T14:30:00",
  "default_trade_date": "2026-03-12",
  "updown": {
    "上涨家数": 2500,
    "下跌家数": 1500,
    "总家数": 4000,
    "上涨占比": 62.5,
    "下跌占比": 37.5
  },
  "mood": {
    "首板": 30,
    "二板": 15,
    "三板": 8,
    "涨停": 100,
    "炸板率": 25.0
  },
  "top_themes": [
    {
      "名称": "人工智能",
      "热度": 95,
      "涨跌幅": 3.5,
      "股票列表": [...]
    }
  ]
}
```

---

## 成本估算

### 腾讯云 SCF 定价

| 资源 | 价格 |
|------|------|
| 函数调用 | 0.0000167 元/千次调用 |
| 执行时间 | 0.0000167 元/GBs |
| 函数内存 | 0.0000334 元/GBs |

### 预估费用（按日 1000 次调用）

- 调用费用：0.0167 元/天
- 执行费用：约 0.04 元/天（平均 100ms 执行时间）
- **月费用**: 约 1.7 元

---

## 性能优化建议

### 1. 缓存配置

对于不常变化的数据（如板块排名），建议配置缓存：

```python
# 在函数中添加缓存逻辑
import time
CACHE = {
    'data': None,
    'timestamp': 0,
    'ttl': 60  # 60秒缓存
}

def get_with_cache():
    now = time.time()
    if now - CACHE['timestamp'] < CACHE['ttl']:
        return CACHE['data']

    data = fetch_data()
    CACHE['data'] = data
    CACHE['timestamp'] = now
    return data
```

### 2. 并发限制

避免同时调用多个 API 导致超时，建议：

- 设置合理的超时时间（当前 30 秒）
- 限制并发请求数量
- 使用异步请求（需要重写代码）

### 3. 冷启动优化

- 启用预留并发
- 使用云函数预置实例
- 减少依赖包体积

---

## 监控与日志

### 查看函数日志

1. 进入 SCF 控制台
2. 选择函数 → **日志查询**
3. 查看实时日志和历史日志

### 配置告警

1. 进入 **云监控控制台**
2. 创建告警策略
3. 监控指标：
   - 函数错误率
   - 执行超时
   - 调用次数

---

## 常见问题

### Q1: 函数执行超时怎么办？

**A**: 修改超时时间至 60 秒，或优化代码逻辑，减少 API 调用时间。

### Q2: 如何配置 CORS？

**A**: 代码中已内置 CORS 响应头，无需额外配置。如需修改域名，修改 `Access-Control-Allow-Origin`。

### Q3: 如何回滚到旧版本？

**A**: SCF 支持版本管理，可在控制台选择历史版本发布。

### Q4: 数据源 API 限流怎么办？

**A**:
1. 增加缓存时间
2. 使用多个账号轮换
3. 考虑使用代理 IP 池

---

## 项目结构

```
网络中转站/
├── scf_handler.py          # 云函数主入口
├── requirements.txt        # Python 依赖
├── template.yaml           # SAM 模板
├── deploy_scf.sh           # Linux/Mac 部署脚本
├── deploy_scf.ps1          # Windows 部署脚本
├── README_DEPLOY.md        # 部署文档（本文件）
└── 豆包中转站.py           # 原本地 Flask 应用
```

---

## 技术支持

如有问题，请：

1. 查看腾讯云 SCF 官方文档
2. 检查函数日志定位问题
3. 提交 Issue 或联系技术支持

---

## 许可证

本项目仅供学习和个人使用，请勿用于商业用途。

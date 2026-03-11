# 快速开始 - 股票市场数据中转站

## 5 分钟快速部署

本文档帮助您在 5 分钟内完成本地 Flask 应用到云函数的部署。

---

## 前置检查

在开始之前，请确保您已具备：

- ✅ 腾讯云账号（免费注册：https://cloud.tencent.com/）
- ✅ Python 3.9+ 环境
- ✅ 项目文件已准备完毕

---

## 部署步骤（Windows）

### 步骤 1: 打包代码（1 分钟）

打开 PowerShell，执行：

```powershell
cd c:\Users\dys\Desktop\网络中转站
.\deploy_scf.ps1
```

执行完成后，会生成 `function.zip` 文件。

### 步骤 2: 创建云函数（2 分钟）

1. 访问：https://console.cloud.tencent.com/scf
2. 点击 **新建** → **从头新建**
3. 按下表配置：

   | 配置项 | 值 |
   |--------|-----|
   | 函数名称 | `stock-market-proxy` |
   | 运行环境 | Python 3.9 |
   | 部署方式 | 本地上传 zip 包 |
   | 函数代码 | 选择 `function.zip` |
   | 入口函数 | `scf_handler.handler` |
   | 内存大小 | 256 MB |
   | 执行超时 | 30 秒 |
   | 时区 | Asia/Shanghai |

4. 点击 **完成**

### 步骤 3: 配置 API 网关（1 分钟）

1. 在函数详情页，点击 **触发器管理** → **创建触发器**
2. 选择 **API 网关**，点击 **下一步**
3. 配置网关：

   | 配置项 | 值 |
   |--------|-----|
   | API 服务 | 新建（默认） |
   | 请求方法 | ANY |
   | 路径 | `/*` |
   | 集成响应 | 勾选 |

4. 点击 **提交**

### 步骤 4: 获取访问地址（1 分钟）

1. 在触发器列表中，找到 API 网关触发器
2. 点击 **访问路径**，复制完整地址
3. 示例：`https://service-xxxxx.gz.apigw.tencentcs.com/release/`

### 步骤 5: 测试接口（立即验证）

在浏览器或 curl 中访问：

```bash
# 聚合接口（推荐先测试这个）
https://your-api-gateway-url.com/all

# 板块排名
https://your-api-gateway-url.com/plates

# 市场情绪
https://your-api-gateway-url.com/market/mood
```

---

## 部署步骤（Linux/Mac）

### 步骤 1: 打包代码

```bash
cd ~/Desktop/网络中转站
chmod +x deploy_scf.sh
./deploy_scf.sh
```

### 步骤 2-5: 同 Windows 步骤

---

## 验证部署成功

在浏览器中访问聚合接口，应该看到类似以下 JSON 响应：

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
    "涨停": 100,
    "炸板率": 25.0
  },
  "top_themes": [...]
}
```

---

## 常见接口列表

| 接口 | 说明 | 示例 |
|------|------|------|
| `/all` | 所有数据聚合 | `/all` |
| `/plates` | 板块排名 | `/plates` |
| `/stocks/<id>` | 成分股 | `/stocks/BK01234` |
| `/market/mood` | 市场情绪 | `/market/mood` |
| `/market/volume` | 量能数据 | `/market/volume` |
| `/market/updown` | 上涨下跌 | `/market/updown` |

完整接口文档请查看 `README_DEPLOY.md`

---

## 故障排查

### 问题 1: 访问地址返回 404

**原因**: API 网关路径配置错误

**解决**: 检查 API 网关触发器的路径是否为 `/*`

### 问题 2: 函数执行超时

**原因**: 网络请求时间过长

**解决**: 在函数配置中增加超时时间至 60 秒

### 问题 3: 返回错误 "Not Found"

**原因**: 路由配置错误

**解决**: 检查 API 网关触发器是否配置为 `ANY` 方法

### 问题 4: CORS 错误

**原因**: 浏览器跨域请求被阻止

**解决**: 代码中已配置 CORS，检查 `Access-Control-Allow-Origin` 头

---

## 下一步

1. **查看详细文档**: `README_DEPLOY.md`
2. **了解迁移指南**: `MIGRATION_GUIDE.md`
3. **优化性能**: 添加缓存、配置 CDN
4. **监控告警**: 配置云监控告警规则

---

## 成本预估

部署后的月费用预估（按日均 1000 次调用）：

- 调用费用: 0.5 元/月
- 执行费用: 2.5 元/月
- API 网关: 0.3 元/月
- **总计: 约 3.3 元/月**

---

## 技术支持

如遇问题：

1. 查看函数日志：SCF 控制台 → 日志查询
2. 检查监控指标：云监控控制台
3. 提交工单：腾讯云控制台 → 工单系统

---

## 快捷命令

### 测试所有接口

```bash
# 批量测试
curl https://your-api-gateway-url.com/all
curl https://your-api-gateway-url.com/plates
curl https://your-api-gateway-url.com/market/mood
curl https://your-api-gateway-url.com/market/volume
```

### 查看函数日志

```bash
# 使用腾讯云 CLI
tcloud scf GetFunctionLogs \
  --FunctionName stock-market-proxy \
  --Region ap-guangzhou \
  --Limit 10
```

---

**恭喜！您已成功部署股票市场数据中转站到云端！** 🎉

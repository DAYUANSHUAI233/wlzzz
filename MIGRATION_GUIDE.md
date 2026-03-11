# 本地 Flask 应用迁移到云函数指南

## 迁移概述

本文档详细说明了从本地 Flask 应用迁移到腾讯云无服务器函数（SCF）的过程和注意事项。

---

## 主要差异对比

| 对比项 | 本地 Flask 版本 | 云函数 SCF 版本 |
|--------|----------------|-----------------|
| **运行环境** | 本地 Python 服务器 | 腾讯云 SCF Python 3.9 |
| **部署方式** | 直接运行 `python 豆包中转站.py` | 上传代码包到云函数 |
| **访问地址** | `http://127.0.0.1:5000` | API 网关 HTTPS 地址 |
| **费用模型** | 免费（但需服务器） | 按需付费，极低成本 |
| **运维成本** | 需要维护服务器 | 零运维，自动扩缩容 |
| **可访问性** | 仅限本地/局域网 | 全球可访问 |
| **并发能力** | 受限于服务器性能 | 自动扩展，理论上无限 |

---

## 代码改动详情

### 1. 路由处理方式

**Flask 版本（装饰器路由）**

```python
@app.route('/market/mood')
def market_mood():
    data = get_market_mood()
    return json_response({
        't': datetime.now().strftime('%m-%d %H:%M'),
        'data': data
    })
```

**SCF 版本（函数路由）**

```python
def handler(event, context):
    """云函数主入口"""
    path, query_params, http_method = parse_path(event)

    # 路由分发
    if path == '/market/mood':
        return handle_market_mood()
    # ... 其他路由
```

### 2. 响应格式

**Flask 版本（Flask Response 对象）**

```python
def json_response(data):
    json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return Response(json_str, mimetype='application/json; charset=utf-8')
```

**SCF 版本（字典格式）**

```python
def json_response(data):
    json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json_str
    }
```

### 3. CORS 支持

**SCF 版本新增 CORS 预检处理**

```python
def handler(event, context):
    # 处理 OPTIONS 预检请求
    if http_method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
            },
            'body': ''
        }
```

### 4. 路径参数解析

**Flask 版本**

```python
@app.route('/market/loss/<market_date>')
def market_loss(market_date):
    data = get_loss_stats(int(market_date))
```

**SCF 版本**

```python
def handle_market_loss(market_date):
    """大跌与回撤统计"""
    try:
        data = get_loss_stats(int(market_date))
    except ValueError:
        data = {'error': '日期格式错误，需要 YYYYMMDD 格式'}
    return json_response({
        'date': market_date,
        'data': data
    })

# 主函数中解析
elif path.startswith('/market/loss/'):
    market_date = path.split('/')[-1]
    return handle_market_loss(market_date)
```

---

## 部署流程对比

### 本地 Flask 版本

```bash
# 1. 安装依赖
pip install flask requests

# 2. 运行服务
python 豆包中转站.py

# 3. 访问服务
# 浏览器打开 http://127.0.0.1:5000
```

### 云函数 SCF 版本

#### 方式一：控制台部署

```bash
# 1. 打包代码（Windows）
.\deploy_scf.ps1

# 2. 登录腾讯云控制台
# 上传 function.zip 文件

# 3. 配置 API 网关触发器

# 4. 获取访问地址
curl https://your-api-gateway-url.com/all
```

#### 方式二：CLI 部署

```bash
# 1. 配置 CLI 认证
tcloud configure

# 2. 执行部署脚本
./deploy_scf.sh

# 3. 配置 API 网关（控制台操作）
```

---

## 性能对比

### 本地 Flask 版本

- **响应时间**: 200-500ms（取决于网络）
- **并发能力**: 受限于本地服务器 CPU 和内存
- **可用性**: 依赖本地网络和服务器稳定性

### 云函数 SCF 版本

- **冷启动**: 50-200ms（首次调用）
- **热调用**: 100-300ms
- **并发能力**: 自动扩展，可支持数千并发
- **可用性**: 99.95% SLA

---

## 成本分析

### 本地 Flask 版本

| 项目 | 费用 |
|------|------|
| 服务器租赁 | 50-200 元/月（云服务器） |
| 带宽费用 | 按流量计费 |
| 维护成本 | 人工维护 |

### 云函数 SCF 版本

假设日均调用 1000 次，平均执行时间 200ms：

| 项目 | 费用 |
|------|------|
| 调用费用 | 0.0167 元/天（0.0000167 × 1000） |
| 执行费用 | 0.08 元/天（256MB × 0.2s × 1000） |
| API 网关 | 约 0.01 元/天 |
| **月费用** | **约 3.3 元/月** |

**结论**: 云函数版本成本更低，且无需维护。

---

## 迁移优势

### 1. 成本优势

- **零基础设施成本**: 无需购买和维护服务器
- **按需付费**: 只为实际使用付费
- **自动优化**: 无需手动优化性能

### 2. 技术优势

- **自动扩缩容**: 根据流量自动调整资源
- **高可用性**: 多可用区部署，故障自动切换
- **安全性**: 腾讯云提供的安全防护

### 3. 运维优势

- **零运维**: 无需管理服务器和系统
- **监控告警**: 内置监控和日志系统
- **版本管理**: 支持快速回滚和灰度发布

---

## 注意事项

### 1. API 限流

- 本地版本无并发限制
- 云函数版本需要注意外部 API 限流
- 建议：增加缓存机制，减少 API 调用频率

### 2. 执行时间限制

- 云函数最大执行时间：15 分钟
- 当前设置为 30 秒，足够大多数场景
- 如遇超时，可调整超时时间或优化代码

### 3. 内存限制

- 当前设置：256 MB
- 如需处理大量数据，可增加到 512 MB 或 1 GB

### 4. 冷启动问题

- 首次调用会有 50-200ms 延迟
- 后续调用会更快（热调用）
- 可通过预热函数减少冷启动影响

---

## 推荐部署流程

### 步骤 1: 本地测试

```bash
# 测试云函数代码
python scf_handler.py
```

### 步骤 2: 打包代码

```bash
# Windows
.\deploy_scf.ps1

# Linux/Mac
./deploy_scf.sh
```

### 步骤 3: 部署到云函数

参考 `README_DEPLOY.md` 中的详细步骤

### 步骤 4: 配置 API 网关

在控制台配置触发器，设置路由为 `/*`

### 步骤 5: 测试验证

```bash
# 测试聚合接口
curl https://your-api-gateway-url.com/all

# 测试各个接口
curl https://your-api-gateway-url.com/market/mood
curl https://your-api-gateway-url.com/plates
```

---

## 回滚方案

如需回滚到本地版本：

```bash
# 1. 直接运行本地版本
python 豆包中转站.py

# 2. 停用云函数（如需要）
# 在控制台禁用函数或删除 API 网关触发器
```

---

## 后续优化建议

### 1. 添加缓存层

使用腾讯云 COS 或 Redis 缓存热点数据：

```python
import redis

redis_client = redis.Redis(host='your-redis-url', port=6379, db=0)

def get_cached_data(key, ttl=60):
    cached = redis_client.get(key)
    if cached:
        return json.loads(cached)

    data = fetch_data()
    redis_client.setex(key, ttl, json.dumps(data))
    return data
```

### 2. 配置 CDN 加速

为 API 网关配置 CDN，加速访问：

1. 在腾讯云 CDN 控制台创建加速域名
2. 源站类型选择"API 网关"
3. 配置缓存策略（动态接口不缓存）

### 3. 添加监控告警

- 配置函数错误率告警
- 配置执行超时告警
- 配置调用次数异常告警

---

## 总结

将本地 Flask 应用迁移到云函数 SCF 是一个明智的选择，主要优势包括：

1. **成本降低**: 从每月 50-200 元降至约 3 元
2. **运维简化**: 从需要维护服务器到零运维
3. **性能提升**: 自动扩缩容，支持高并发
4. **可靠性提升**: 99.95% SLA，高可用性

迁移过程简单，代码改动小，适合快速部署和迭代。

---

## 相关文档

- [README_DEPLOY.md](./README_DEPLOY.md) - 详细部署指南
- [template.yaml](./template.yaml) - 云函数模板配置
- [scf_handler.py](./scf_handler.py) - 云函数代码实现

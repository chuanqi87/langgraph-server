# Render 部署指南

## 部署前准备

### 1. 获取 Gemini API Key
1. 访问 [Google AI Studio](https://aistudio.google.com/)
2. 登录你的 Google 账户
3. 点击 "Create API Key"
4. 复制生成的 API Key

### 2. 准备代码
1. 确保所有文件都已提交到 Git 仓库
2. 推送到 GitHub 或其他 Git 托管服务

## 部署步骤

### 方法一：使用 render.yaml 自动部署 (推荐)

1. **创建 Render 账户**
   - 访问 [Render](https://render.com/)
   - 注册或登录账户

2. **创建 Web Service**
   - 点击 "New" > "Web Service"
   - 连接你的 GitHub 仓库
   - 选择包含代码的仓库

3. **配置服务**
   - Render 会自动检测 `render.yaml` 文件
   - 服务名称：`langgraph-agent-service`
   - 环境：`Python`
   - 构建命令：`pip install -r requirements.txt`
   - 启动命令：`python app.py`

4. **设置环境变量**
   - 在 Render 控制面板中，找到 "Environment"
   - 添加环境变量：
     - `GEMINI_API_KEY`: 你的 Gemini API Key
     - `ENVIRONMENT`: `production`

5. **部署**
   - 点击 "Deploy" 开始部署
   - 等待部署完成 (通常 5-10 分钟)

### 方法二：手动配置

1. **创建 Web Service**
   - 在 Render 中点击 "New" > "Web Service"
   - 连接你的 GitHub 仓库

2. **手动配置**
   - Name: `langgraph-agent-service`
   - Environment: `Python`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Instance Type: `Free` (或选择付费版本)

3. **环境变量设置**
   - 添加 `GEMINI_API_KEY`
   - 添加 `ENVIRONMENT=production`

4. **高级设置**
   - Health Check Path: `/health`
   - Auto-Deploy: `Yes`

## 部署验证

### 1. 检查部署状态
- 在 Render 控制面板中查看部署日志
- 确认服务状态为 "Live"

### 2. 运行验证脚本
```bash
# 本地运行验证脚本
python deploy_test.py https://your-app.onrender.com
```

### 3. 手动测试
- 访问 `https://your-app.onrender.com/health`
- 测试聊天接口：
```bash
curl -X POST https://your-app.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "你好", "session_id": "test"}'
```

## 常见问题

### 1. 部署失败
**症状**: 构建或启动失败
**解决方案**:
- 检查 `requirements.txt` 中的依赖版本
- 查看部署日志中的错误信息
- 确认 Python 版本兼容性

### 2. API Key 错误
**症状**: 500 错误，日志显示 API Key 相关错误
**解决方案**:
- 确认 `GEMINI_API_KEY` 环境变量正确设置
- 检查 API Key 是否有效
- 确认 API Key 有足够的配额

### 3. 超时错误
**症状**: 请求超时
**解决方案**:
- 检查网络连接
- 增加请求超时时间
- 检查 Gemini API 服务状态

### 4. 内存不足
**症状**: 应用崩溃，内存相关错误
**解决方案**:
- 升级到付费实例
- 优化代码，减少内存使用
- 检查内存泄漏

## 监控和维护

### 1. 日志查看
- 在 Render 控制面板中查看实时日志
- 监控错误和性能指标

### 2. 性能监控
- 设置健康检查
- 监控响应时间
- 检查资源使用情况

### 3. 自动重启
- Render 会自动重启崩溃的服务
- 配置适当的健康检查

## 扩展功能

### 1. 自定义域名
- 在 Render 中配置自定义域名
- 设置 SSL 证书

### 2. 数据库集成
- 添加 PostgreSQL 数据库
- 配置数据持久化

### 3. 缓存优化
- 添加 Redis 缓存
- 优化响应速度

## 成本优化

### 1. 免费版限制
- 服务会在空闲时休眠
- 有请求限制
- 适合开发和测试

### 2. 付费版优势
- 无休眠限制
- 更好的性能
- 更多资源
- 优先支持

## 安全建议

1. **API Key 管理**
   - 使用环境变量存储敏感信息
   - 定期轮换 API Key
   - 限制 API Key 权限

2. **访问控制**
   - 考虑添加身份验证
   - 实施速率限制
   - 监控异常访问

3. **HTTPS**
   - Render 默认提供 HTTPS
   - 确保所有通信都是加密的

## 支持

如果遇到问题：
1. 查看 Render 官方文档
2. 检查项目 README.md
3. 查看 GitHub Issues
4. 联系技术支持 
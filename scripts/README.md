# 工具脚本

这个目录包含了项目维护和测试所需的工具脚本。

## 📁 脚本说明

### `test_deployment.py`
**用途**: 完整的部署后服务测试工具

**功能**:
- 健康检查测试
- 聊天功能测试（多种场景）
- 错误处理测试
- 性能测试

**使用方法**:
```bash
pip install requests
python3 scripts/test_deployment.py [服务地址]
```

**默认测试地址**: `https://langgraph-server-84mc.onrender.com`

### `check_versions.py`
**用途**: 依赖版本兼容性检查工具

**功能**:
- 验证已安装包版本
- 检查导入兼容性
- 依赖冲突检测

**使用方法**:
```bash
python3 scripts/check_versions.py
```

## 🔧 开发建议

- 在部署前运行 `check_versions.py` 确保依赖兼容性
- 在部署后运行 `test_deployment.py` 验证服务功能
- 定期使用这些工具进行服务健康检查 
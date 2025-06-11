# You2API 项目概述

## 项目简介

You2API 是一个将 You.com 的 AI 服务转换为 OpenAI API 兼容接口的代理服务。它允许用户通过标准的 OpenAI API 格式与 You.com 的 AI 模型进行交互，包括支持图片分析功能（Vision API）。

## 核心功能

### 1. OpenAI API 兼容
- 提供 `/v1/chat/completions` 端点
- 支持标准的 OpenAI 请求格式
- 支持流式和非流式响应
- 兼容多种 AI 模型（gpt-4o, claude-3.5-sonnet 等）

### 2. 多模态支持（Vision API）
- 支持图片上传和分析
- 兼容 base64 编码的图片
- 支持图片 URL 引用
- 自动处理图片格式转换

### 3. 聊天历史管理
- 智能处理多轮对话
- 自动优化长消息（文件上传）
- 保持对话上下文

## 工作流程

### 基本文本对话流程

```
1. 接收 OpenAI 格式请求
   ↓
2. 解析消息和参数
   ↓
3. 构建聊天历史
   ↓
4. 调用 You.com API
   ↓
5. 处理响应并转换为 OpenAI 格式
   ↓
6. 返回结果
```

### 图片处理流程

```
1. 检测消息中的图片内容
   ↓
2. 提取图片数据（base64 或 URL）
   ↓
3. 创建临时图片文件
   ↓
4. 上传图片到 You.com
   ↓
5. 获取文件引用
   ↓
6. 构建包含图片引用的请求
   ↓
7. 调用 You.com Vision API
   ↓
8. 返回分析结果
```

## 技术架构

### 主要组件

1. **HTTP 服务器**
   - 基于 Go 标准库 `net/http`
   - 监听端口 12001
   - 处理 CORS 和认证

2. **消息处理器**
   - OpenAI 格式解析
   - 多模态内容检测
   - Token 计数和优化

3. **文件管理器**
   - 图片文件上传
   - 临时文件处理
   - 文件格式转换

4. **API 客户端**
   - You.com API 调用
   - 流式响应处理
   - 错误处理和重试

### 关键算法

1. **Token 计数**
   ```go
   func countTokensForMessages(messages []Message) (int, error)
   ```
   - 估算消息的 token 数量
   - 用于决定是否需要文件上传优化

2. **图片内容检测**
   ```go
   func hasImageContent(content interface{}) bool
   ```
   - 检测消息是否包含图片
   - 支持多种图片格式

3. **文件上传优化**
   - 长消息（>30 tokens）自动上传为文件
   - 减少 API 调用的数据量
   - 提高处理效率

## 配置和部署

### 环境变量
- `DS_TOKEN`: You.com 认证令牌（必需）
- `AGENT_MODEL_ID`: 指定 AI 模型（可选）

### 启动服务
```bash
cd api
go run main.go
```

### API 调用示例
```bash
curl -X POST http://localhost:12001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {"type": "text", "text": "描述这张图片"},
          {"type": "image_url", "image_url": {"url": "data:image/jpeg;base64,..."}}
        ]
      }
    ]
  }'
```

## 安全特性

1. **Token 验证**
   - 验证 You.com DS token 有效性
   - 防止未授权访问

2. **文件安全**
   - 临时文件自动清理
   - 安全的文件上传处理

3. **错误处理**
   - 详细的错误日志
   - 优雅的错误响应

## 测试和验证

### 功能测试
- 基本文本对话测试
- 图片上传和分析测试
- 多轮对话测试
- 流式响应测试

### 测试脚本
- `test_vision_example.py`: 完整的 Vision API 测试
- `test_real_upload.py`: 真实图片上传测试

## 性能特点

1. **高效的消息处理**
   - 智能 token 计数
   - 自动消息优化

2. **流式响应支持**
   - 实时数据传输
   - 低延迟响应

3. **资源管理**
   - 自动文件清理
   - 内存优化

## 兼容性

- **OpenAI SDK**: 完全兼容
- **多种编程语言**: 支持所有支持 HTTP 的语言
- **图片格式**: JPEG, PNG, GIF, WebP 等
- **模型支持**: GPT-4o, Claude-3.5-Sonnet, DeepSeek 等

## 未来扩展

1. **更多模型支持**
2. **批量请求处理**
3. **缓存机制**
4. **监控和日志**
5. **负载均衡**

---

这个项目为开发者提供了一个简单而强大的方式来集成 You.com 的 AI 能力，同时保持与 OpenAI API 的完全兼容性。
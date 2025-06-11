# You2API 项目概述

## 项目简介

You2API 是一个将 You.com 的 AI 服务转换为 OpenAI API 兼容接口的代理服务。它允许用户使用 You.com Pro 订阅来访问各种 AI 模型，包括 GPT、Claude、Gemini 等，同时提供与 OpenAI API 相同的接口格式。

## 核心功能

### 1. 模型代理
- 将 OpenAI 模型名称映射到 You.com 对应的模型
- 支持多种 AI 模型：GPT-4o、Claude、Gemini、Llama 等
- 自动处理模型选择和参数转换

### 2. 聊天完成 API
- 完全兼容 OpenAI Chat Completions API
- 支持流式和非流式响应
- 处理聊天历史和上下文管理

### 3. 图片上传与视觉分析 (新增)
- 支持 OpenAI Vision API 格式
- Base64 图片和图片 URL 处理
- 多模态消息支持
- 与 You.com 文件上传 API 集成

## 技术架构

### 后端 (Go)
```
api/main.go - 主要服务文件
├── HTTP 服务器 (端口 8080)
├── 路由处理
│   ├── /v1/chat/completions - 聊天 API
│   ├── /v1/models - 模型列表
│   └── /health - 健康检查
├── You.com API 集成
│   ├── streamingSearch - 聊天接口
│   └── upload - 文件上传接口
└── 数据结构
    ├── Message - 消息结构 (支持多模态)
    ├── ContentPart - 内容部分
    └── ImageURL - 图片 URL
```

### 关键组件

#### 1. 消息处理
```go
type Message struct {
    Role    string      `json:"role"`
    Content interface{} `json:"content"` // 支持 string 或 []ContentPart
}

type ContentPart struct {
    Type     string    `json:"type"`
    Text     string    `json:"text,omitempty"`
    ImageURL *ImageURL `json:"image_url,omitempty"`
}
```

#### 2. 图片处理流程
1. **检测图片内容** - `hasImageContent()`
2. **提取文本内容** - `extractTextContent()`
3. **处理图片** - `processImageContent()`
   - Base64 解码 - `decodeBase64Image()`
   - URL 下载 - `downloadImage()`
   - 上传到 You.com - 文件上传 API
4. **构建查询** - 包含图片引用的文本

#### 3. 模型映射
```go
var modelMap = map[string]string{
    "gpt-4o":                  "gpt_4o",
    "gpt-4o-mini":             "gpt_4o_mini",
    "claude-3.5-sonnet":       "claude_3_5_sonnet",
    "gemini-1.5-pro":          "gemini_1_5_pro",
    // ... 更多模型映射
}
```

## 工作流程

### 标准聊天流程
1. 接收 OpenAI 格式的请求
2. 提取并验证 DS token
3. 映射模型名称
4. 构建聊天历史
5. 调用 You.com streamingSearch API
6. 解析响应并转换为 OpenAI 格式
7. 返回结果

### 图片处理流程
1. 检测消息中是否包含图片
2. 如果有图片：
   - 处理 Base64 图片或下载 URL 图片
   - 上传图片到 You.com 服务器
   - 获取文件引用 ID
   - 在查询中添加图片引用
3. 继续标准聊天流程

## API 端点

### POST /v1/chat/completions
主要的聊天完成端点，支持：
- 文本消息
- 图片消息 (Base64 或 URL)
- 混合内容消息
- 流式响应
- 聊天历史

### GET /v1/models
返回支持的模型列表

### GET /health
健康检查端点

## 配置与部署

### 环境要求
- Go 1.21+
- 有效的 You.com Pro DS token

### 启动服务
```bash
cd api
go run main.go
# 或
go run start.go
```

### Docker 部署
```bash
docker build -t you2api .
docker run -p 8080:8080 you2api
```

## 安全考虑

1. **Token 安全** - DS token 通过 Authorization header 传递
2. **文件上传** - 图片临时存储，处理后删除
3. **输入验证** - 验证图片格式和大小
4. **错误处理** - 不暴露敏感信息

## 性能优化

1. **Token 计算** - 估算图片 token 数量 (85 tokens/图片)
2. **文件处理** - 流式处理大文件
3. **缓存** - 复用 HTTP 连接
4. **并发** - Go 协程处理请求

## 错误处理

常见错误类型：
- 401: 认证失败
- 413: 文件过大
- 415: 不支持的媒体类型
- 500: 内部处理错误

## 扩展性

### 添加新模型
1. 在 `modelMap` 中添加映射
2. 测试模型兼容性
3. 更新文档

### 添加新功能
1. 扩展消息结构
2. 实现处理逻辑
3. 添加相应的 API 端点

## 测试

### 单元测试
- 消息解析测试
- 图片处理测试
- 模型映射测试

### 集成测试
- 端到端 API 测试
- 真实 token 测试
- 多种图片格式测试

## 监控与日志

- 请求/响应日志
- 错误跟踪
- 性能指标
- 文件上传统计

## 未来规划

1. **更多模态支持** - 音频、视频处理
2. **缓存优化** - 图片和响应缓存
3. **负载均衡** - 多实例部署
4. **监控仪表板** - 实时状态监控

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 许可证

请参考项目根目录的 LICENSE 文件。
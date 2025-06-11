# You2API 图片上传功能使用指南

## 概述

You2API 现在支持 OpenAI Vision API 兼容的图片上传功能，允许用户在聊天消息中包含图片，并获得 AI 对视觉内容的分析。

## 功能特性

- ✅ **Base64 图片支持** - 直接在消息中嵌入 base64 编码的图片
- ✅ **图片 URL 支持** - 通过 URL 引用网络图片
- ✅ **多模态消息** - 在同一消息中混合文本和图片内容
- ✅ **多种模型支持** - GPT-4o、Claude、Gemini 等视觉模型
- ✅ **向后兼容** - 现有的纯文本 API 调用保持不变

## API 使用方法

### 1. Base64 图片上传

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "请分析这张图片的内容"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..."
          }
        }
      ]
    }
  ],
  "stream": false
}
```

### 2. 图片 URL

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "描述这张图片"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "https://example.com/image.jpg"
          }
        }
      ]
    }
  ]
}
```

### 3. 多张图片

```json
{
  "model": "gpt-4o",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "比较这两张图片的差异"
        },
        {
          "type": "image_url",
          "image_url": {"url": "data:image/png;base64,image1..."}
        },
        {
          "type": "image_url",
          "image_url": {"url": "https://example.com/image2.jpg"}
        }
      ]
    }
  ]
}
```

## 支持的图片格式

- PNG
- JPEG/JPG
- GIF
- WebP
- BMP

## 使用限制

- 图片大小建议不超过 20MB
- Base64 编码后的图片会增加约 33% 的大小
- 每张图片在 token 计算中约占 85 个 token

## 错误处理

常见错误及解决方案：

1. **401 Unauthorized** - 检查 DS token 是否有效
2. **413 Payload Too Large** - 图片文件过大，请压缩后重试
3. **415 Unsupported Media Type** - 图片格式不支持
4. **500 Internal Server Error** - 图片处理失败，检查图片是否损坏

## 示例代码

### Python 示例

```python
import requests
import base64

# 读取并编码图片
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

payload = {
    "model": "gpt-4o",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "这张图片显示了什么？"},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}}
        ]
    }]
}

headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_DS_TOKEN"
}

response = requests.post("http://localhost:8080/v1/chat/completions", 
                        json=payload, headers=headers)
```

### cURL 示例

```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_DS_TOKEN" \
  -d '{
    "model": "gpt-4o",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "text", "text": "分析这张图片"},
        {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
      ]
    }]
  }'
```

## 注意事项

1. **安全性** - 不要在代码中硬编码 DS token
2. **性能** - 大图片会增加处理时间
3. **成本** - 图片分析可能消耗更多 token
4. **隐私** - 上传的图片会被发送到 You.com 服务器

## 故障排除

如果遇到问题，请检查：

1. DS token 是否有效且具有 Pro 权限
2. 图片格式和大小是否符合要求
3. 网络连接是否正常
4. 服务器是否正在运行

更多技术细节请参考 `PROJECT_OVERVIEW.md`。
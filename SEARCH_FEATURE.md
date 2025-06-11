# You2API 搜索功能说明

## 功能概述

You2API 现在支持网络搜索功能！当您使用带有 `-search` 后缀的模型名称时，系统会自动启用 You.com 的网络搜索功能，让AI能够获取最新的网络信息来回答您的问题。

## 使用方法

### 1. 可用的搜索模型

所有基础模型都有对应的搜索版本，只需在模型名后添加 `-search` 后缀：

- `gpt-4o-search`
- `gpt-4o-mini-search`
- `claude-3.5-sonnet-search`
- `deepseek-chat-search`
- `gemini-1.5-pro-search`
- 等等...

### 2. API 调用示例

#### 普通聊天（无搜索）
```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_DS_TOKEN" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": "介绍一下人工智能"
      }
    ]
  }'
```

#### 启用搜索功能
```bash
curl -X POST http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_DS_TOKEN" \
  -d '{
    "model": "gpt-4o-search",
    "messages": [
      {
        "role": "user", 
        "content": "今天的最新科技新闻有哪些？"
      }
    ]
  }'
```

### 3. Python 客户端示例

```python
import openai

# 配置客户端
client = openai.OpenAI(
    api_key="YOUR_DS_TOKEN",
    base_url="http://localhost:8080/v1"
)

# 普通聊天
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": "什么是机器学习？"}
    ]
)

# 启用搜索的聊天
search_response = client.chat.completions.create(
    model="gpt-4o-search",
    messages=[
        {"role": "user", "content": "2024年最新的AI发展趋势是什么？"}
    ]
)
```

## 技术实现

### 工作原理

1. **模型检测**：系统检测到模型名包含 `-search` 后缀
2. **参数映射**：将 `gpt-4o-search` 映射为基础模型 `gpt-4o`
3. **搜索启用**：在向 You.com API 发送请求时添加搜索参数：
   - `selectedChatMode=default`
   - `use_search=true`
   - `search_focus=web`
   - `enable_web_results=true`
4. **响应处理**：保持原始模型名 `gpt-4o-search` 在响应中

### 关键代码修改

1. **模型检测函数**：
```go
func isSearchModel(modelID string) bool {
    return strings.HasSuffix(modelID, "-search")
}

func getBaseModelName(modelID string) string {
    if isSearchModel(modelID) {
        return strings.TrimSuffix(modelID, "-search")
    }
    return modelID
}
```

2. **搜索参数设置**：
```go
if isSearch {
    q.Add("selectedAiModel", mapModelName(baseModel))
    q.Add("selectedChatMode", "default")
    q.Add("use_search", "true")
    q.Add("search_focus", "web")
    q.Add("enable_web_results", "true")
}
```

## 适用场景

### 推荐使用搜索功能的场景：
- 获取最新新闻和时事
- 查询实时数据（股价、天气等）
- 了解最新的技术发展
- 搜索特定事件或人物的最新信息
- 获取产品价格和评价

### 推荐使用普通模式的场景：
- 一般知识问答
- 代码编写和调试
- 文本创作和编辑
- 逻辑推理和分析
- 不需要最新信息的任务

## 注意事项

1. **Token 要求**：需要有效的 You.com DS token
2. **响应时间**：搜索模式可能比普通模式稍慢，因为需要进行网络搜索
3. **搜索质量**：搜索结果的质量取决于 You.com 的搜索能力
4. **模型兼容性**：所有支持的基础模型都可以使用搜索功能

## 获取模型列表

您可以通过以下 API 获取所有可用的模型（包括搜索模型）：

```bash
curl http://localhost:8080/v1/models
```

这将返回包含所有基础模型和对应搜索模型的完整列表。
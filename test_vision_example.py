#!/usr/bin/env python3
"""
You2API Vision API 测试示例
注意：请使用您自己的DS token替换 YOUR_DS_TOKEN_HERE
"""

import requests
import json
import base64

# 请替换为您的真实DS token
DS_TOKEN = "YOUR_DS_TOKEN_HERE"

def test_vision_api():
    """测试Vision API功能"""
    
    # 示例：使用base64图片
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请描述这张图片的内容"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "data:image/png;base64,YOUR_BASE64_IMAGE_HERE"
                        }
                    }
                ]
            }
        ],
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DS_TOKEN}"
    }
    
    try:
        response = requests.post("http://localhost:8080/v1/chat/completions", 
                               json=payload, headers=headers, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            content = data.get('choices', [{}])[0].get('message', {}).get('content', '')
            print(f"AI响应: {content}")
        else:
            print(f"请求失败: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"请求异常: {e}")

def test_image_url():
    """测试图片URL功能"""
    
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "请分析这张图片"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://example.com/your-image.jpg"
                        }
                    }
                ]
            }
        ],
        "stream": False
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DS_TOKEN}"
    }
    
    # 实现类似的请求逻辑...

if __name__ == "__main__":
    print("请确保已设置正确的DS token")
    print("然后运行相应的测试函数")
    # test_vision_api()
    # test_image_url()
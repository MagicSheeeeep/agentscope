#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 配置示例
展示不同模型提供商的配置方式
"""

import agentscope
from agentscope.agents import DialogAgent

# 配置示例1: OpenAI模型
def config_openai():
    """OpenAI模型配置示例"""
    return {
        "config_name": "openai_config",
        "model_type": "openai_chat",
        "model_name": "gpt-3.5-turbo",
        "api_key": "your_openai_api_key_here",
        "organization": "your_org_id",  # 可选
        "temperature": 0.7,
        "max_tokens": 1000,
    }

# 配置示例2: 阿里云DashScope模型
def config_dashscope():
    """阿里云DashScope模型配置示例"""
    return {
        "config_name": "dashscope_config",
        "model_type": "dashscope_chat",
        "model_name": "qwen-max",
        "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
        "temperature": 0.7,
    }

# 配置示例3: 本地Ollama模型
def config_ollama():
    """本地Ollama模型配置示例"""
    return {
        "config_name": "ollama_config",
        "model_type": "ollama_chat",
        "model_name": "llama2",
        "host": "http://localhost:11434",
        "temperature": 0.7,
    }

# 配置示例4: 百度文心一言
def config_wenxin():
    """百度文心一言配置示例"""
    return {
        "config_name": "wenxin_config", 
        "model_type": "wenxin_chat",
        "model_name": "ernie-bot",
        "api_key": "your_wenxin_api_key",
        "secret_key": "your_wenxin_secret_key",
    }

def main():
    """主函数：演示不同模型配置"""
    
    # 选择要使用的配置（你可以根据需要修改）
    model_configs = [
        # config_openai(),      # OpenAI
        config_dashscope(),   # 阿里云DashScope（推荐中文用户）
        # config_ollama(),      # 本地Ollama
        # config_wenxin(),      # 百度文心一言
    ]
    
    # 初始化AgentScope，连接到Studio
    agentscope.init(
        model_configs=model_configs,
        studio_url="http://localhost:3000",  # 连接到AgentScope Studio
        project="AgentScope Demo",  # 项目名称
        save_dir="./runs",  # 保存运行日志的目录
    )
    
    print("🚀 AgentScope Studio 已连接！")
    print("📊 可视化界面地址: http://localhost:3000")
    print("💾 运行日志保存在: ./runs")
    print("=" * 50)
    
    # 创建代理（使用第一个配置）
    agent = DialogAgent(
        name="Assistant",
        model_config_name=model_configs[0]["config_name"],
        sys_prompt="你是一个有用的AI助手，请用中文回答问题。",
    )
    
    # 简单对话测试
    from agentscope.message import Msg
    
    test_messages = [
        "你好！",
        "请介绍一下AgentScope",
        "AgentScope Studio有什么功能？",
    ]
    
    print("🤖 开始测试对话:")
    print("-" * 30)
    
    for i, msg_content in enumerate(test_messages, 1):
        print(f"\n👤 用户 ({i}): {msg_content}")
        
        # 发送消息给代理
        msg = Msg("user", msg_content, "user")
        response = agent(msg)
        
        print(f"🤖 {agent.name}: {response.content}")
        
        # 添加一些延迟，便于在Studio中观察
        import time
        time.sleep(1)
    
    print("\n✅ 测试完成！请查看AgentScope Studio界面观察对话流程。")

if __name__ == "__main__":
    print("🎯 AgentScope Studio 配置示例")
    print("请确保:")
    print("1. AgentScope Studio 正在运行 (http://localhost:3000)")
    print("2. 已配置正确的API密钥")
    print("3. 网络连接正常")
    print("=" * 50)
    
    try:
        main()
    except Exception as e:
        print(f"❌ 运行出错: {e}")
        print("💡 请检查配置和网络连接") 
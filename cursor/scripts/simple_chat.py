#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope 纯命令行对话脚本
不依赖Studio，适合快速测试和日常使用
"""

import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg

# 阿里云DashScope配置
MODEL_CONFIG = [
    {
        "config_name": "qwen_turbo",
        "model_type": "dashscope_chat",
        "model_name": "qwen-turbo",
        "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
        "generate_args": {
            "temperature": 0.7,
            "max_tokens": 2000,
        }
    }
]

def main():
    """主函数：纯命令行对话"""
    print("🚀 AgentScope 纯命令行对话")
    print("=" * 50)
    print("💡 此版本不依赖Studio，适合快速使用")
    
    try:
        # 初始化AgentScope（不连接Studio）
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="纯命令行对话",
            save_api_invoke=False,    # 不保存API调用记录
            use_monitor=False,        # 不启用监控
            # 不设置studio_url，避免Studio连接
        )
        
        print("✅ AgentScope 初始化成功！")
        
        # 创建对话代理
        dialog_agent = DialogAgent(
            name="AI助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个友好的AI助手，请用中文简洁地回答问题。"
        )
        
        print("💬 开始对话（输入 'exit'、'quit' 或 '退出' 结束对话）")
        print("🤖 AI助手: 你好！我是通义千问，有什么可以帮助您的吗？")
        print("-" * 50)
        
        # 对话循环
        conversation_count = 0
        
        while True:
            try:
                # 用户输入
                user_input = input("\n👤 您: ").strip()
                
                # 检查退出条件
                if user_input.lower() in ["exit", "quit", "退出", "结束", "bye"]:
                    print("\n👋 感谢使用AgentScope，再见！")
                    break
                
                if not user_input:
                    print("⚠️ 请输入内容，或输入 'exit' 退出")
                    continue
                
                conversation_count += 1
                
                # 创建用户消息
                user_msg = Msg("user", user_input, "user")
                
                # AI回复
                print(f"🤖 AI助手正在思考...")
                response = dialog_agent(user_msg)
                print(f"🤖 AI助手: {response.content}")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print("\n\n👋 对话被中断，感谢使用AgentScope！")
                break
            except Exception as e:
                print(f"\n❌ 发生错误: {e}")
                print("💡 请检查网络连接和API密钥配置")
                break
        
        print(f"\n📊 本次对话共进行了 {conversation_count} 轮")
        print("💡 如需可视化功能，请使用: python3 cursor/scripts/chat_with_studio.py")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("\n🔧 可能的解决方案:")
        print("1. 检查API密钥是否正确")
        print("2. 确认网络连接正常")
        print("3. 检查账户余额是否充足")

if __name__ == "__main__":
    main() 
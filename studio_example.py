#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 连接示例
这个脚本展示了如何将AgentScope应用连接到本地可视化工具AgentScope Studio
"""

import agentscope
from agentscope.agents import DialogAgent, UserAgent
from agentscope.message import Msg

def main():
    """主函数：演示AgentScope Studio连接"""
    
    # 初始化AgentScope，连接到Studio
    agentscope.init(
        model_configs=[
            {
                "config_name": "my_config",
                "model_type": "openai_chat",  # 你可以根据需要修改模型类型
                "model_name": "gpt-3.5-turbo",  # 你可以根据需要修改模型名称
                "api_key": "your_api_key_here",  # 请替换为你的API密钥
            }
        ],
        studio_url="http://localhost:3000",  # 连接到AgentScope Studio
    )
    
    print("🚀 AgentScope Studio 已连接！")
    print("📊 可视化界面地址: http://localhost:3000")
    print("=" * 50)
    
    # 创建对话代理
    dialog_agent = DialogAgent(
        name="Friday",
        model_config_name="my_config",
        sys_prompt="你是一个名叫Friday的有用助手，请用中文回答问题。"
    )
    
    # 创建用户代理
    user_agent = UserAgent(name="user")
    
    print("💬 开始对话（输入 'exit' 退出）:")
    print("-" * 30)
    
    # 构建对话流程
    x = None
    while x is None or x.content != "exit":
        try:
            # 代理回复
            x = dialog_agent(x)
            print(f"🤖 {dialog_agent.name}: {x.content}")
            
            # 用户输入
            x = user_agent(x)
            if x.content == "exit":
                print("👋 对话结束！")
                break
                
        except KeyboardInterrupt:
            print("\n👋 对话被中断！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            break

def demo_multi_agent():
    """演示多代理对话"""
    
    # 初始化AgentScope，连接到Studio
    agentscope.init(
        model_configs=[
            {
                "config_name": "my_config", 
                "model_type": "openai_chat",
                "model_name": "gpt-3.5-turbo",
                "api_key": "your_api_key_here",
            }
        ],
        studio_url="http://localhost:3000",
    )
    
    from agentscope.pipelines import sequential_pipeline
    from agentscope import msghub
    
    # 创建三个代理
    friday = DialogAgent(
        name="Friday",
        model_config_name="my_config",
        sys_prompt="你是一个名叫Friday的助手，喜欢讲笑话"
    )
    
    saturday = DialogAgent(
        name="Saturday", 
        model_config_name="my_config",
        sys_prompt="你是一个名叫Saturday的助手，喜欢讲故事"
    )
    
    sunday = DialogAgent(
        name="Sunday",
        model_config_name="my_config", 
        sys_prompt="你是一个名叫Sunday的助手，喜欢分享知识"
    )
    
    print("🎭 多代理对话演示")
    print("📊 可视化界面地址: http://localhost:3000")
    print("=" * 50)
    
    # 创建聊天室，代理消息会广播给所有参与者
    with msghub(
        participants=[friday, saturday, sunday],
        announcement=Msg("user", "大家好！请每人介绍一下自己", "user"),
    ) as hub:
        # 按顺序发言
        sequential_pipeline([friday, saturday, sunday], x=None)

if __name__ == "__main__":
    print("🎯 AgentScope Studio 连接示例")
    print("请选择演示模式:")
    print("1. 单代理对话")
    print("2. 多代理对话")
    
    choice = input("请输入选择 (1/2): ").strip()
    
    if choice == "1":
        main()
    elif choice == "2":
        demo_multi_agent()
    else:
        print("❌ 无效选择，运行单代理对话演示")
        main() 
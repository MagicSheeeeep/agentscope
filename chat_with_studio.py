#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 可视化界面测试脚本
测试与本地可视化界面的连接和交互
"""

import agentscope
from agentscope.agents import DialogAgent, UserAgent
import requests
import time

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

def check_studio_status():
    """检查AgentScope Studio状态"""
    print("🔍 检查AgentScope Studio状态...")
    
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ AgentScope Studio 正在运行 (http://localhost:3000)")
            return True
        else:
            print(f"⚠️ Studio响应异常，状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到AgentScope Studio")
        print("💡 请确保Studio正在运行:")
        print("   命令: as_studio")
        print("   或者: npm install -g @agentscope/studio && as_studio")
        return False
    except Exception as e:
        print(f"❌ 检查Studio状态时出错: {e}")
        return False

def test_studio_connection():
    """测试Studio连接和可视化功能"""
    print("🚀 AgentScope Studio 可视化测试")
    print("=" * 60)
    
    # 检查Studio状态
    if not check_studio_status():
        return False
    
    try:
        print("\n🔧 初始化AgentScope并连接到Studio...")
        
        # 初始化AgentScope，连接到Studio
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="Studio可视化测试",
            save_api_invoke=True,              # 保存API调用记录
            studio_url="http://localhost:3000", # 连接到Studio
            use_monitor=True,                  # 启用监控
        )
        
        print("✅ AgentScope 初始化成功！")
        print("📊 已连接到Studio，可视化界面将显示对话过程")
        
        # 创建对话代理
        dialog_agent = DialogAgent(
            name="Studio测试助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是AgentScope Studio的测试助手，请简洁地回答问题，并说明这是在测试可视化界面。"
        )
        
        # 创建用户代理
        user_agent = UserAgent(name="测试用户")
        
        print(f"\n📱 Studio界面地址: http://localhost:3000")
        print("💡 请在浏览器中打开上述地址查看可视化效果")
        print("\n💬 开始测试对话（输入 'exit' 退出）:")
        print("🤖 Studio测试助手: 你好！我是AgentScope Studio测试助手，现在我们的对话会在可视化界面中实时显示。")
        print("-" * 60)
        
        # 对话循环
        x = None
        conversation_count = 0
        
        while True:
            try:
                # 用户输入
                x = user_agent(x)
                
                # 检查退出条件
                if x.content.lower() in ["exit", "quit", "退出", "结束"]:
                    print("\n👋 Studio测试结束！")
                    break
                
                conversation_count += 1
                print(f"\n[第{conversation_count}轮对话 - Studio可视化中]")
                
                # AI回复
                print("🤖 AI正在思考（请查看Studio界面的实时显示）...")
                x = dialog_agent(x)
                print(f"🤖 Studio测试助手: {x.content}")
                print("📊 此对话已同步到Studio可视化界面")
                print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 测试被中断！")
                break
            except Exception as e:
                print(f"\n❌ 对话过程中发生错误: {e}")
                break
        
        print(f"\n📊 测试统计:")
        print(f"   - 对话轮数: {conversation_count}")
        print(f"   - Studio连接: ✅ 成功")
        print(f"   - 可视化界面: http://localhost:3000")
        
        return True
        
    except Exception as e:
        print(f"❌ Studio连接测试失败: {e}")
        print("\n🔧 可能的解决方案:")
        print("1. 确保AgentScope Studio正在运行")
        print("2. 检查3000端口是否被占用")
        print("3. 重启Studio: as_studio")
        print("4. 检查API密钥配置")
        return False

def run_demo_conversation():
    """运行演示对话，展示Studio功能"""
    print("\n🎭 运行演示对话...")
    
    try:
        from agentscope.message import Msg
        
        # 创建对话代理
        dialog_agent = DialogAgent(
            name="演示助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个演示助手，请简短回答问题。"
        )
        
        # 模拟几轮对话
        demo_questions = [
            "你好，请介绍一下AgentScope",
            "AgentScope有什么特色功能？",
            "如何使用可视化界面？"
        ]
        
        for i, question in enumerate(demo_questions, 1):
            print(f"\n[演示对话 {i}/3]")
            print(f"👤 用户: {question}")
            
            # 创建消息并获取回复
            msg = Msg("user", question, "demo_user")
            response = dialog_agent(msg)
            
            print(f"🤖 演示助手: {response.content}")
            print("📊 请查看Studio界面中的可视化效果")
            
            # 短暂暂停，便于观察
            time.sleep(2)
        
        print("\n🎉 演示对话完成！请查看Studio界面中的完整对话流程图")
        
    except Exception as e:
        print(f"❌ 演示对话失败: {e}")

def main():
    """主函数"""
    print("🎯 AgentScope Studio 可视化测试工具")
    print("=" * 60)
    
    # 测试Studio连接
    if test_studio_connection():
        print("\n🎉 Studio连接测试成功！")
        
        # 询问是否运行演示
        try:
            choice = input("\n是否运行自动演示对话？(y/n): ").strip().lower()
            if choice in ['y', 'yes', '是']:
                run_demo_conversation()
        except KeyboardInterrupt:
            print("\n👋 测试结束")
    else:
        print("\n❌ Studio连接测试失败")
        print("请先启动AgentScope Studio，然后重新运行此脚本")

if __name__ == "__main__":
    main() 
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
        
        # 从最新的runs目录获取运行ID
        import os
        import glob
        runs_dir = "runs"
        if os.path.exists(runs_dir):
            run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
            if run_dirs:
                latest_run_dir = max(run_dirs, key=os.path.getmtime)
                run_id = os.path.basename(latest_run_dir)
                # 使用正确的 dashboard URL 格式
                studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
                dashboard_main = "http://localhost:3000/dashboard"
                
                print(f"\n🎯 重要：请访问以下正确的URL查看可视化界面：")
                print(f"📱 方式1 - 直接访问: {studio_url}")
                print(f"📱 方式2 - Dashboard: {dashboard_main}")
                print("⚠️  注意：使用 /dashboard 路径，避免重定向问题")
                print("💡 请复制上面的URL到浏览器中打开")
            else:
                studio_url = "http://localhost:3000/dashboard"
                print(f"\n📱 Studio界面地址: {studio_url}")
        else:
            studio_url = "http://localhost:3000/dashboard"
            print(f"\n📱 Studio界面地址: {studio_url}")
        
        # 创建对话代理
        dialog_agent = DialogAgent(
            name="通义千问助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是通义千问(qwen-turbo)，由阿里巴巴开发的大语言模型。你正在通过AgentScope框架运行，连接到阿里云DashScope API。当前正在测试AgentScope Studio的可视化功能。请诚实回答用户的问题。"
        )
        
        print("\n💬 开始测试对话（输入 'exit' 退出）:")
        print("🤖 Studio测试助手: 你好！我是AgentScope Studio测试助手，现在我们的对话会在可视化界面中实时显示。")
        print("-" * 60)
        
        # 对话循环
        from agentscope.message import Msg
        conversation_count = 0
        
        while True:
            try:
                # 用户输入
                user_input = input("\n👤 您: ").strip()
                
                # 检查退出条件
                if user_input.lower() in ["exit", "quit", "退出", "结束"]:
                    print("\n👋 Studio测试结束！")
                    break
                
                if not user_input:
                    print("⚠️ 请输入内容，或输入 'exit' 退出")
                    continue
                
                conversation_count += 1
                print(f"\n[第{conversation_count}轮对话 - Studio可视化中]")
                
                # 创建用户消息
                user_msg = Msg("user", user_input, "user")
                
                # AI回复
                print("🤖 AI正在思考（请查看Studio界面的实时显示）...")
                try:
                    response = dialog_agent(user_msg)
                    
                    # 处理可能的编码问题
                    if hasattr(response, 'content'):
                        response_text = str(response.content)
                        # 清理可能导致编码问题的字符
                        response_text = response_text.encode('utf-8', errors='replace').decode('utf-8')
                        # 移除代理字符
                        response_text = ''.join(char for char in response_text if ord(char) < 0xD800 or ord(char) > 0xDFFF)
                        print(f"🤖 Studio测试助手: {response_text}")
                    else:
                        print(f"🤖 Studio测试助手: {response}")
                        
                except Exception as e:
                    print(f"❌ AI回复时发生错误: {e}")
                    print("🤖 Studio测试助手: [AI回复出现问题，请重试]")
                
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
        print(f"   - 可视化界面: {studio_url}")
        print(f"💡 请确保访问带有run_id的专用URL查看可视化效果")
        
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
            msg = Msg("user", question, "user")
            response = dialog_agent(msg)
            
            # 处理可能的编码问题
            try:
                response_text = response.content
                response_text = response_text.encode('utf-8', errors='ignore').decode('utf-8')
                print(f"🤖 演示助手: {response_text}")
            except Exception as encoding_error:
                print(f"🤖 演示助手: [回复包含特殊字符，显示可能不完整]")
                print(f"   编码错误: {encoding_error}")
            
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
        print("\n🎉 Studio连接测试完成！")
    else:
        print("\n❌ Studio连接测试失败")
        print("请先启动AgentScope Studio，然后重新运行此脚本")

if __name__ == "__main__":
    main() 
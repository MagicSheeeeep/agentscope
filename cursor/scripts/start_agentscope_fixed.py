#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope 命令行交互脚本（修复版）
直接通过命令行与大模型对话
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
    """主函数：命令行对话"""
    print("🚀 AgentScope 命令行对话（修复版）")
    print("=" * 50)
    
    try:
        # 初始化AgentScope并连接到Studio
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="命令行对话",
            save_api_invoke=True,              # 保存API调用记录
            studio_url="http://localhost:3000", # 连接到Studio
            use_monitor=True,                  # 启用监控
        )
        
        print("✅ AgentScope 初始化成功！")
        print("📊 已连接到Studio，对话将在可视化界面中显示")
        
        # 创建对话代理
        dialog_agent = DialogAgent(
            name="AI助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个友好的AI助手，请用中文简洁地回答问题。"
        )
        
        print("💬 开始对话（输入 'exit'、'quit' 或 '退出' 结束对话）")
        print("🤖 AI助手: 你好！我是通义千问，有什么可以帮助您的吗？")
        
        # 显示Studio URL（在对话开始后，运行目录已创建）
        import os
        import glob
        import time
        time.sleep(1)  # 等待运行目录创建
        
        runs_dir = "runs"
        if os.path.exists(runs_dir):
            run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
            if run_dirs:
                latest_run_dir = max(run_dirs, key=os.path.getmtime)
                run_id = os.path.basename(latest_run_dir)
                studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
                print(f"🎯 可视化界面: {studio_url}")
                print("💡 请在浏览器中打开上述URL查看对话过程")
        
        print("-" * 50)
        
        # 对话循环
        conversation_count = 0
        
        while True:
            try:
                # 直接使用input()获取用户输入
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
        
        # 最终显示Studio URL
        if os.path.exists(runs_dir):
            run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
            if run_dirs:
                latest_run_dir = max(run_dirs, key=os.path.getmtime)
                run_id = os.path.basename(latest_run_dir)
                studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
                print(f"🎯 查看完整对话记录: {studio_url}")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        print("\n🔧 可能的解决方案:")
        print("1. 检查API密钥是否正确")
        print("2. 确认网络连接正常")
        print("3. 检查账户余额是否充足")
        print("4. 确保AgentScope Studio正在运行: as_studio")

if __name__ == "__main__":
    main() 
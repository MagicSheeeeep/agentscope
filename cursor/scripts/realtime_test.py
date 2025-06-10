#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实时测试AgentScope Studio显示
"""

import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
import time
import webbrowser
import glob
import os

# 阿里云DashScope配置
MODEL_CONFIG = [
    {
        "config_name": "qwen_turbo",
        "model_type": "dashscope_chat",
        "model_name": "qwen-turbo",
        "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
        "generate_args": {
            "temperature": 0.7,
            "max_tokens": 500,
        }
    }
]

def main():
    """实时对话测试"""
    print("🔴 AgentScope Studio 实时显示测试")
    print("=" * 60)
    
    try:
        # 初始化AgentScope
        print("🔧 初始化AgentScope...")
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="实时显示测试",
            save_api_invoke=True,
            studio_url="http://localhost:3000",
            use_monitor=True,
        )
        
        print("✅ AgentScope 初始化成功！")
        
        # 等待运行目录创建
        time.sleep(2)
        
        # 获取运行ID并打开浏览器
        runs_dir = "runs"
        if os.path.exists(runs_dir):
            run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
            if run_dirs:
                latest_run_dir = max(run_dirs, key=os.path.getmtime)
                run_id = os.path.basename(latest_run_dir)
                studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
                
                print(f"🎯 运行ID: {run_id}")
                print(f"📱 Studio URL: {studio_url}")
                print("🌐 正在打开浏览器...")
                
                try:
                    webbrowser.open(studio_url)
                    print("✅ 浏览器已打开")
                except:
                    print("⚠️ 无法自动打开浏览器，请手动访问上述URL")
        
        # 创建代理
        agent = DialogAgent(
            name="实时测试助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个测试助手，请简短回答问题。"
        )
        
        print("\n" + "="*60)
        print("🚀 开始实时对话测试")
        print("💡 请在浏览器中观察Studio界面的实时更新")
        print("="*60)
        
        # 自动发送测试消息
        test_messages = [
            "你好，这是第一条测试消息",
            "请告诉我当前时间",
            "AgentScope的主要功能是什么？",
            "谢谢你的回答"
        ]
        
        for i, msg_text in enumerate(test_messages, 1):
            print(f"\n🔄 第 {i}/{len(test_messages)} 轮对话")
            print(f"👤 用户: {msg_text}")
            
            # 创建用户消息
            user_msg = Msg("user", msg_text, "user")
            
            # 发送给AI
            print("🤖 AI正在思考...")
            response = agent(user_msg)
            
            print(f"🤖 AI回复: {response.content}")
            print("📊 请检查Studio界面是否实时更新了这条对话")
            
            # 等待用户确认
            if i < len(test_messages):
                input("👆 按回车键继续下一轮对话...")
        
        print(f"\n🎉 测试完成！")
        print(f"📱 请在Studio中查看完整的对话记录: {studio_url}")
        
        # 检查数据文件
        print(f"\n📊 数据检查:")
        chat_file = os.path.join(latest_run_dir, "logging.chat")
        if os.path.exists(chat_file):
            file_size = os.path.getsize(chat_file)
            print(f"✅ 聊天日志: {file_size} bytes")
            
            # 显示聊天日志内容
            with open(chat_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.strip().split('\n')
                print(f"✅ 消息数量: {len(lines)} 条")
        else:
            print("❌ 聊天日志文件不存在")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 
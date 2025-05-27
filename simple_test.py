#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试修复后的AgentScope配置
"""

import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
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

def test_fixed_configuration():
    """测试修复后的配置"""
    print("🧪 测试修复后的AgentScope配置")
    print("=" * 50)
    
    try:
        # 使用修复后的配置
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="修复测试",
            save_api_invoke=True,              # 保存API调用记录
            studio_url="http://localhost:3000", # 连接到Studio
            use_monitor=True,                  # 启用监控
        )
        
        print("✅ AgentScope 初始化成功！")
        print("📊 已连接到Studio，对话将在可视化界面中显示")
        
        # 创建代理
        agent = DialogAgent(
            name="修复测试助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个测试助手，请简短回答。"
        )
        
        # 发送测试消息
        print("\n💬 发送测试消息...")
        test_msg = Msg("user", "你好，这是修复后的测试", "user")
        response = agent(test_msg)
        
        print(f"🤖 收到回复: {response.content}")
        
        # 获取运行ID
        runs_dir = "runs"
        if os.path.exists(runs_dir):
            run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
            if run_dirs:
                latest_run_dir = max(run_dirs, key=os.path.getmtime)
                run_id = os.path.basename(latest_run_dir)
                studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
                
                print(f"\n🎯 可视化界面: {studio_url}")
                print("💡 请在浏览器中打开上述URL查看对话过程")
                
                # 检查文件
                chat_file = os.path.join(latest_run_dir, "logging.chat")
                if os.path.exists(chat_file):
                    file_size = os.path.getsize(chat_file)
                    print(f"✅ 聊天日志已保存: {file_size} bytes")
                else:
                    print("❌ 聊天日志未找到")
                
                return run_id
        
        return None
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return None

if __name__ == "__main__":
    run_id = test_fixed_configuration()
    if run_id:
        print(f"\n🎉 修复成功！现在start_agentscope.py应该能在Studio中显示数据了")
        print(f"📱 测试URL: http://localhost:3000/dashboard?run_id={run_id}")
    else:
        print(f"\n❌ 修复失败，请检查配置") 
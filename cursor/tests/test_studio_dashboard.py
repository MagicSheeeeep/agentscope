#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 AgentScope Studio Dashboard 数据显示
"""

import requests
import json
import time
import webbrowser

def test_dashboard_data():
    """测试Dashboard数据"""
    print("🔍 测试AgentScope Studio Dashboard数据显示")
    print("=" * 60)
    
    run_id = "run_20250527-121543_cj4mxk"
    dashboard_url = f"http://localhost:3000/dashboard?run_id={run_id}"
    
    print(f"🎯 测试URL: {dashboard_url}")
    
    try:
        # 测试页面访问
        response = requests.get(dashboard_url, timeout=10)
        print(f"✅ Dashboard页面响应: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Dashboard页面可以正常访问")
            
            # 检查页面内容是否包含运行ID
            if run_id in response.text:
                print(f"✅ 页面包含运行ID: {run_id}")
            else:
                print(f"⚠️ 页面不包含运行ID，可能需要等待数据加载")
            
            print(f"\n🌐 正在打开浏览器...")
            print(f"📱 请在浏览器中查看: {dashboard_url}")
            
            # 自动打开浏览器
            try:
                webbrowser.open(dashboard_url)
                print("✅ 浏览器已打开")
            except Exception as e:
                print(f"⚠️ 无法自动打开浏览器: {e}")
                print(f"请手动复制URL到浏览器: {dashboard_url}")
            
            print(f"\n💡 检查要点:")
            print(f"1. 页面左侧是否显示运行列表")
            print(f"2. 是否能看到运行ID: {run_id}")
            print(f"3. 点击运行ID后是否显示对话数据")
            print(f"4. 是否有消息流程图或对话记录")
            
            return True
        else:
            print(f"❌ Dashboard访问失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def create_test_conversation():
    """创建一个测试对话来验证实时数据"""
    print(f"\n🚀 创建测试对话来验证实时数据显示...")
    
    try:
        import agentscope
        from agentscope.agents import DialogAgent
        from agentscope.message import Msg
        
        # 模型配置
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
        
        print("🔧 初始化AgentScope...")
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="Dashboard测试",
            save_api_invoke=True,
            studio_url="http://localhost:3000",
            use_monitor=True,
        )
        
        # 创建代理
        agent = DialogAgent(
            name="Dashboard测试助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个测试助手，请用简短的话回答问题。"
        )
        
        # 发送几条测试消息
        test_messages = [
            "你好，这是第一条测试消息",
            "请告诉我AgentScope的主要功能",
            "谢谢你的回答"
        ]
        
        for i, msg_text in enumerate(test_messages, 1):
            print(f"\n💬 发送测试消息 {i}/3: {msg_text}")
            
            msg = Msg("user", msg_text, "user")
            response = agent(msg)
            
            print(f"🤖 收到回复: {response.content[:100]}...")
            print("📊 请检查Dashboard是否实时更新了这条对话")
            
            # 短暂暂停
            time.sleep(2)
        
        # 获取新的运行ID
        import glob
        import os
        runs_dir = "runs"
        run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
        if run_dirs:
            latest_run_dir = max(run_dirs, key=os.path.getmtime)
            new_run_id = os.path.basename(latest_run_dir)
            
            new_dashboard_url = f"http://localhost:3000/dashboard?run_id={new_run_id}"
            print(f"\n🎯 新的Dashboard URL: {new_dashboard_url}")
            
            # 打开新的URL
            try:
                webbrowser.open(new_dashboard_url)
                print("✅ 新的Dashboard已在浏览器中打开")
            except:
                print(f"请手动访问: {new_dashboard_url}")
            
            return new_run_id
        
    except Exception as e:
        print(f"❌ 创建测试对话失败: {e}")
        return None

def main():
    print("🧪 AgentScope Studio Dashboard 测试工具")
    print("=" * 60)
    
    # 检查Studio状态
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code != 200:
            print("❌ Studio未运行，请先启动: as_studio")
            return
        print("✅ Studio正在运行")
    except:
        print("❌ 无法连接到Studio，请先启动: as_studio")
        return
    
    print("\n选择测试方式:")
    print("1. 测试现有运行的Dashboard显示")
    print("2. 创建新对话并测试实时显示")
    
    choice = input("请选择 (1 或 2): ").strip()
    
    if choice == "1":
        test_dashboard_data()
    elif choice == "2":
        new_run_id = create_test_conversation()
        if new_run_id:
            print(f"\n✅ 测试完成！请检查Dashboard中的数据显示")
            print(f"🎯 URL: http://localhost:3000/dashboard?run_id={new_run_id}")
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 
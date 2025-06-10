#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 最终解决方案
确保可视化看板能正常显示数据
"""

import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
import time
import webbrowser
import glob
import os
import requests
import json

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

def restart_studio():
    """重启Studio"""
    print("🔄 重启AgentScope Studio...")
    
    # 这里我们只能提示用户手动重启
    print("💡 请手动重启Studio:")
    print("1. 在Studio终端按 Ctrl+C 停止")
    print("2. 运行: as_studio")
    print("3. 等待Studio启动完成")
    
    input("👆 Studio重启完成后，按回车键继续...")

def force_register_run(run_id, run_dir):
    """强制注册运行到Studio"""
    print(f"🔧 强制注册运行: {run_id}")
    
    # 读取配置
    config_file = os.path.join(run_dir, ".config")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    else:
        config = {}
    
    # 准备注册数据
    register_data = {
        "id": run_id,
        "project": config.get('project', 'AgentScope Project'),
        "name": config.get('name', 'default'),
        "timestamp": config.get('timestamp', time.strftime('%Y-%m-%d %H:%M:%S')),
        "run_dir": os.path.abspath(run_dir),
        "pid": config.get('pid', os.getpid()),
        "status": "running"  # 设置为运行中状态
    }
    
    try:
        response = requests.post(
            "http://localhost:3000/trpc/registerRun",
            json=register_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            print("✅ 运行强制注册成功")
            return True
        else:
            print(f"❌ 注册失败: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 注册请求失败: {e}")
        return False

def create_live_conversation():
    """创建实时对话"""
    print("🚀 创建实时对话测试")
    print("=" * 50)
    
    try:
        # 初始化AgentScope
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="最终测试",
            save_api_invoke=True,
            studio_url="http://localhost:3000",
            use_monitor=True,
        )
        
        print("✅ AgentScope 初始化成功")
        
        # 等待运行目录创建
        time.sleep(2)
        
        # 获取运行ID
        runs_dir = "runs"
        run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
        latest_run_dir = max(run_dirs, key=os.path.getmtime)
        run_id = os.path.basename(latest_run_dir)
        
        print(f"🎯 运行ID: {run_id}")
        
        # 强制注册
        force_register_run(run_id, latest_run_dir)
        
        # 创建代理
        agent = DialogAgent(
            name="最终测试助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个测试助手，请简短回答。"
        )
        
        # 生成Studio URL
        studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
        print(f"📱 Studio URL: {studio_url}")
        
        # 打开浏览器
        try:
            webbrowser.open(studio_url)
            print("✅ 浏览器已打开")
        except:
            print("⚠️ 请手动打开浏览器")
        
        print("\n" + "="*50)
        print("🔴 实时对话开始")
        print("💡 请在浏览器中观察Studio界面")
        print("="*50)
        
        # 交互式对话
        conversation_count = 0
        
        while True:
            try:
                user_input = input("\n👤 您 (输入'exit'退出): ").strip()
                
                if user_input.lower() in ["exit", "quit", "退出"]:
                    break
                
                if not user_input:
                    continue
                
                conversation_count += 1
                
                # 发送消息
                user_msg = Msg("user", user_input, "user")
                print("🤖 AI正在思考...")
                response = agent(user_msg)
                print(f"🤖 AI: {response.content}")
                
                print(f"📊 第{conversation_count}轮对话完成，请检查Studio界面")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ 错误: {e}")
                break
        
        print(f"\n🎉 对话结束，共{conversation_count}轮")
        print(f"📱 查看记录: {studio_url}")
        
        return run_id, studio_url
        
    except Exception as e:
        print(f"❌ 创建对话失败: {e}")
        return None, None

def main():
    print("🎯 AgentScope Studio 最终解决方案")
    print("=" * 60)
    
    # 检查Studio状态
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code != 200:
            print("❌ Studio未运行")
            restart_studio()
        else:
            print("✅ Studio正在运行")
    except:
        print("❌ 无法连接到Studio")
        restart_studio()
    
    print("\n选择解决方案:")
    print("1. 创建新的实时对话测试")
    print("2. 重启Studio并重新测试")
    print("3. 查看故障排除指南")
    
    choice = input("请选择 (1-3): ").strip()
    
    if choice == "1":
        run_id, studio_url = create_live_conversation()
        if run_id:
            print(f"\n🎯 测试完成！")
            print(f"📱 如果看板仍无数据，请:")
            print(f"1. 硬刷新浏览器 (Cmd+Shift+R)")
            print(f"2. 清除浏览器缓存")
            print(f"3. 使用无痕模式打开: {studio_url}")
    
    elif choice == "2":
        restart_studio()
        main()  # 重新开始
    
    elif choice == "3":
        print("\n🔧 故障排除指南:")
        print("=" * 40)
        print("1. 浏览器问题:")
        print("   - 硬刷新页面 (Cmd+Shift+R)")
        print("   - 清除浏览器缓存")
        print("   - 使用无痕模式")
        print("   - 尝试不同浏览器")
        
        print("\n2. Studio问题:")
        print("   - 重启Studio: Ctrl+C 然后 as_studio")
        print("   - 检查Studio版本: npm list -g @agentscope/studio")
        print("   - 更新Studio: npm update -g @agentscope/studio")
        
        print("\n3. 数据问题:")
        print("   - 确保save_api_invoke=True")
        print("   - 确保studio_url正确")
        print("   - 确保use_monitor=True")
        
        print("\n4. 网络问题:")
        print("   - 检查端口3000是否被占用")
        print("   - 检查防火墙设置")
        
        print(f"\n💡 如果问题仍然存在，请:")
        print(f"1. 重启整个系统")
        print(f"2. 重新安装AgentScope Studio")
        print(f"3. 检查AgentScope版本兼容性")

if __name__ == "__main__":
    main() 
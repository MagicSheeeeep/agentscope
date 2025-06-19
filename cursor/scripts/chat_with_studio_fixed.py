#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 可视化界面测试脚本 - 修复版
确保对话能正确同步到可视化界面
"""

import agentscope
from agentscope.agents import DialogAgent, UserAgent
from agentscope.message import Msg
import requests
import time
import glob
import os
import json
import uuid

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
            print("✅ AgentScope Studio 正在运行")
            return True
        else:
            print(f"⚠️ Studio响应异常，状态码: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到AgentScope Studio")
        print("💡 请确保Studio正在运行: as_studio")
        return False

def manual_register_run(run_id, project_name):
    """手动注册运行（确保Studio识别）"""
    register_data = {
        "id": run_id,
        "project": project_name,
        "name": run_id.split('_')[-1],
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "run_dir": os.path.abspath(f"runs/{run_id}"),
        "pid": os.getpid(),
        "status": "running"
    }
    
    try:
        response = requests.post(
            "http://localhost:3000/trpc/registerRun",
            json=register_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

def fix_config_file(config_file):
    """修复配置文件中的studio_url"""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        if config.get('studio_url') is None:
            config['studio_url'] = "http://localhost:3000"
            config['monitor']['use_monitor'] = True
            
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=4)
            print("🔧 配置文件已修复")
            return True
    except:
        pass
    return False

def main():
    """主函数"""
    print("🚀 AgentScope Studio 可视化测试 - 修复版")
    print("=" * 60)
    
    # 检查Studio状态
    if not check_studio_status():
        return False
    
    try:
        print("\n🔧 初始化AgentScope并连接到Studio...")
        
        # 清理之前的连接
        if hasattr(agentscope, '_manager') and agentscope._manager:
            agentscope._manager.flush()
        
        # 初始化AgentScope，使用修复的配置
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="Studio可视化测试-修复版",
            save_api_invoke=True,              # 必须启用
            save_log=True,                     # 必须启用
            studio_url="http://localhost:3000", # 必须设置
            use_monitor=True,                  # 必须启用
        )
        
        print("✅ AgentScope 初始化成功！")
        
        # 等待目录创建
        time.sleep(3)
        
        # 获取运行ID
        runs_dir = "runs"
        run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
        latest_run_dir = max(run_dirs, key=os.path.getmtime)
        run_id = os.path.basename(latest_run_dir)
        
        print(f"🎯 运行ID: {run_id}")
        
        # 修复配置文件
        config_file = os.path.join(latest_run_dir, ".config")
        fix_config_file(config_file)
        
        # 手动注册运行
        if manual_register_run(run_id, "Studio可视化测试-修复版"):
            print("✅ 运行已注册到Studio")
        
        # 生成正确的URL
        studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
        print(f"\n🎯 重要：请访问以下URL查看可视化界面：")
        print(f"📱 {studio_url}")
        print("💡 请现在就打开这个URL，然后继续对话测试")
        
        # 创建对话代理
        dialog_agent = DialogAgent(
            name="通义千问助手-修复版",
            model_config_name="qwen_turbo",
            sys_prompt="你是通义千问，正在测试修复版的AgentScope Studio可视化功能。请简短回答。"
        )
        
        print("\n💬 开始对话测试（输入 'exit' 退出）:")
        print("🤖 Studio测试助手: 你好！我是修复版的AgentScope Studio测试助手。")
        print("-" * 60)
        
        conversation_count = 0
        
        while True:
            try:
                # 用户输入
                user_input = input("\n👤 您: ").strip()
                
                # 检查退出条件
                if user_input.lower() in ["exit", "quit", "退出", "结束"]:
                    print("\n👋 测试结束！")
                    break
                
                if not user_input:
                    print("⚠️ 请输入内容，或输入 'exit' 退出")
                    continue
                
                conversation_count += 1
                print(f"\n[第{conversation_count}轮对话]")
                
                # 创建用户消息
                user_msg = Msg("user", user_input, "user")
                
                # AI回复
                print("🤖 AI正在思考...")
                try:
                    response = dialog_agent(user_msg)
                    response_text = str(response.content)
                    print(f"🤖 AI: {response_text}")
                    
                except Exception as e:
                    print(f"❌ AI回复失败: {e}")
                    continue
                
                print("📊 此对话应该已同步到Studio界面")
                print(f"🔄 请检查: {studio_url}")
                print("-" * 60)
                
            except KeyboardInterrupt:
                print("\n\n👋 测试被中断！")
                break
            except Exception as e:
                print(f"\n❌ 对话错误: {e}")
                break
        
        print(f"\n📊 测试统计:")
        print(f"   - 对话轮数: {conversation_count}")
        print(f"   - Studio连接: ✅ 成功")
        print(f"   - 可视化界面: {studio_url}")
        print(f"💡 如果看不到数据，请硬刷新浏览器 (Cmd+Shift+R)")
        
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

if __name__ == "__main__":
    main() 
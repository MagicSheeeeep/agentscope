#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修复 AgentScope Studio 运行注册问题
手动注册运行到Studio
"""

import os
import json
import requests
import glob
from datetime import datetime

def get_latest_run_info():
    """获取最新运行的信息"""
    runs_dir = "runs"
    if not os.path.exists(runs_dir):
        return None
    
    run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
    if not run_dirs:
        return None
    
    latest_run_dir = max(run_dirs, key=os.path.getmtime)
    run_id = os.path.basename(latest_run_dir)
    
    # 读取配置文件
    config_path = os.path.join(latest_run_dir, ".config")
    if not os.path.exists(config_path):
        return None
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        
        return {
            "run_id": run_id,
            "run_dir": latest_run_dir,
            "config": config_data
        }
    except Exception as e:
        print(f"❌ 读取配置文件失败: {e}")
        return None

def register_run_to_studio(run_info):
    """注册运行到Studio"""
    print(f"🔧 注册运行到Studio: {run_info['run_id']}")
    
    config = run_info['config']
    run_dir_abs = os.path.abspath(run_info['run_dir'])
    
    # 准备注册数据
    register_data = {
        "id": run_info['run_id'],
        "project": config.get('project', 'AgentScope Project'),
        "name": config.get('name', 'default'),
        "timestamp": config.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        "run_dir": run_dir_abs,
        "pid": config.get('pid', os.getpid()),
        "status": "done"  # 设置为已完成状态
    }
    
    print(f"📊 注册数据: {json.dumps(register_data, indent=2, ensure_ascii=False)}")
    
    try:
        # 发送注册请求
        response = requests.post(
            "http://localhost:3000/trpc/registerRun",
            json=register_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 注册响应状态: {response.status_code}")
        print(f"📝 响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 运行注册成功！")
            return True
        else:
            print(f"❌ 注册失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 注册请求失败: {e}")
        return False

def test_studio_access(run_id):
    """测试Studio访问"""
    print(f"\n🔍 测试Studio访问...")
    
    urls_to_test = [
        f"http://localhost:3000/dashboard?run_id={run_id}",
        "http://localhost:3000/dashboard",
        "http://localhost:3000"
    ]
    
    for url in urls_to_test:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url}: {response.status_code}")
        except Exception as e:
            print(f"❌ {url}: {e}")

def create_new_run_with_studio():
    """创建一个新的运行并正确连接到Studio"""
    print(f"\n🚀 创建新的运行并连接到Studio...")
    
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
                    "max_tokens": 1000,
                }
            }
        ]
        
        print("🔧 初始化AgentScope...")
        # 初始化AgentScope，确保Studio连接
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="Studio修复测试",
            save_api_invoke=True,
            studio_url="http://localhost:3000",
            use_monitor=True,
        )
        
        print("✅ AgentScope初始化成功")
        
        # 创建代理并发送一条测试消息
        agent = DialogAgent(
            name="测试助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个测试助手，请简短回答。"
        )
        
        print("💬 发送测试消息...")
        test_msg = Msg("user", "你好，这是一个测试消息", "user")
        response = agent(test_msg)
        
        print(f"✅ 收到回复: {response.content}")
        
        # 获取新的运行ID
        runs_dir = "runs"
        run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
        if run_dirs:
            latest_run_dir = max(run_dirs, key=os.path.getmtime)
            new_run_id = os.path.basename(latest_run_dir)
            print(f"🎯 新运行ID: {new_run_id}")
            
            studio_url = f"http://localhost:3000/dashboard?run_id={new_run_id}"
            print(f"📱 访问URL: {studio_url}")
            
            return new_run_id
        
    except Exception as e:
        print(f"❌ 创建新运行失败: {e}")
        return None

def main():
    print("🔧 AgentScope Studio 注册修复工具")
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
    
    print("\n选择修复方式:")
    print("1. 手动注册现有运行")
    print("2. 创建新的运行并自动连接")
    
    choice = input("请选择 (1 或 2): ").strip()
    
    if choice == "1":
        # 方式1：手动注册现有运行
        run_info = get_latest_run_info()
        if not run_info:
            print("❌ 未找到有效的运行数据")
            return
        
        print(f"📊 找到运行: {run_info['run_id']}")
        
        if register_run_to_studio(run_info):
            test_studio_access(run_info['run_id'])
            print(f"\n🎯 请访问: http://localhost:3000/dashboard?run_id={run_info['run_id']}")
        
    elif choice == "2":
        # 方式2：创建新运行
        new_run_id = create_new_run_with_studio()
        if new_run_id:
            print(f"\n🎯 请访问: http://localhost:3000/dashboard?run_id={new_run_id}")
    
    else:
        print("❌ 无效选择")

if __name__ == "__main__":
    main() 
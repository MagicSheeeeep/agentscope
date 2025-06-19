#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 实时同步测试脚本
解决Command+C状态同步和对话信息同步问题
"""

import agentscope
from agentscope.agents import DialogAgent, UserAgent
from agentscope.message import Msg
import requests
import time
import os
import glob
import json
import signal
import sys
import threading
import uuid
import atexit

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

# 全局变量
current_run_id = None
studio_url = "http://localhost:3000"
is_running = True

def safe_studio_request(method, endpoint, data=None, timeout=5):
    """安全的Studio API请求"""
    try:
        url = f"{studio_url}/trpc/{endpoint}"
        if method.upper() == "GET":
            response = requests.get(url, timeout=timeout)
        else:
            response = requests.post(url, json=data, 
                                   headers={"Content-Type": "application/json"}, 
                                   timeout=timeout)
        return response
    except Exception as e:
        print(f"⚠️ Studio API请求失败 ({endpoint}): {e}")
        return None

def update_run_status(run_id, status):
    """更新运行状态到Studio"""
    print(f"🔄 更新运行状态: {run_id} -> {status}")
    
    # 尝试多种可能的状态更新方法
    methods_to_try = [
        ("updateStatus", {"id": run_id, "status": status}),
        ("updateRun", {"id": run_id, "status": status}),
        ("setRunStatus", {"run_id": run_id, "status": status}),
        # 重新注册为完成状态
        ("registerRun", {
            "id": run_id,
            "status": status,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        })
    ]
    
    for method, data in methods_to_try:
        response = safe_studio_request("POST", method, data)
        if response and response.status_code == 200:
            print(f"✅ 状态更新成功 (方法: {method})")
            return True
        elif response:
            print(f"⚠️ 方法 {method} 失败: {response.text}")
    
    print("❌ 所有状态更新方法都失败了")
    return False

def push_message_to_studio(run_id, message, role="user"):
    """推送消息到Studio"""
    try:
        message_data = {
            "run_id": run_id,
            "message": {
                "id": str(uuid.uuid4()),
                "content": str(message),
                "role": role,
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "name": role
            }
        }
        
        # 尝试多种消息推送方法
        endpoints = ["pushMessage", "addMessage", "sendMessage", "message"]
        
        for endpoint in endpoints:
            response = safe_studio_request("POST", endpoint, message_data)
            if response and response.status_code == 200:
                print(f"✅ 消息推送成功 (方法: {endpoint})")
                return True
            elif response:
                print(f"⚠️ 推送方法 {endpoint} 失败: {response.text}")
        
        print("❌ 所有消息推送方法都失败了")
        return False
        
    except Exception as e:
        print(f"❌ 推送消息异常: {e}")
        return False

def graceful_shutdown():
    """优雅关闭，更新状态"""
    global current_run_id, is_running
    
    print("\n🔄 正在优雅关闭...")
    is_running = False
    
    if current_run_id:
        print(f"📝 更新运行状态为完成: {current_run_id}")
        update_run_status(current_run_id, "done")
        
        # 等待一下确保状态更新完成
        time.sleep(1)
    
    print("👋 程序已完成，状态已同步到Studio")

def signal_handler(signum, frame):
    """处理Ctrl+C信号"""
    print(f"\n🛑 收到信号 {signum}，正在优雅退出...")
    graceful_shutdown()
    sys.exit(0)

def heartbeat_thread(run_id):
    """心跳线程，定期更新运行状态"""
    global is_running
    
    while is_running:
        try:
            # 发送心跳，确认运行中状态
            heartbeat_data = {
                "id": run_id,
                "status": "running",
                "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
                "pid": os.getpid()
            }
            
            response = safe_studio_request("POST", "heartbeat", heartbeat_data)
            if not response:
                # 如果心跳失败，尝试重新注册
                safe_studio_request("POST", "registerRun", heartbeat_data)
            
            time.sleep(30)  # 每30秒发送一次心跳
        except Exception as e:
            print(f"⚠️ 心跳异常: {e}")
            time.sleep(30)

def check_studio_status():
    """检查Studio状态"""
    print("🔍 检查AgentScope Studio状态...")
    
    response = safe_studio_request("GET", "health")
    if not response:
        response = safe_studio_request("GET", "")
    
    if response and response.status_code == 200:
        print("✅ AgentScope Studio 正在运行")
        return True
    else:
        print("❌ 无法连接到AgentScope Studio")
        print("💡 请先启动Studio: as_studio")
        return False

def register_run_to_studio(run_id, config):
    """注册运行到Studio"""
    register_data = {
        "id": run_id,
        "project": config.get('project', 'Studio实时同步测试'),
        "name": run_id.split('_')[-1],
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S'),
        "run_dir": os.path.abspath(f"runs/{run_id}"),
        "pid": os.getpid(),
        "status": "running"
    }
    
    response = safe_studio_request("POST", "registerRun", register_data)
    if response and response.status_code == 200:
        print("✅ 运行已成功注册到Studio")
        return True
    else:
        print(f"⚠️ 运行注册失败")
        return False

def main():
    """主函数"""
    global current_run_id
    
    print("🚀 AgentScope Studio 实时同步测试")
    print("=" * 60)
    print("📋 此脚本将解决以下问题:")
    print("1. Command+C后状态同步问题")
    print("2. 对话信息实时同步问题")
    print("=" * 60)
    
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    atexit.register(graceful_shutdown)
    
    # 检查Studio状态
    if not check_studio_status():
        return False
    
    try:
        print("\n🔧 初始化AgentScope...")
        
        # 清理之前的连接
        if hasattr(agentscope, '_manager') and agentscope._manager:
            agentscope._manager.flush()
        
        # 初始化AgentScope
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="Studio实时同步测试",
            save_api_invoke=True,
            save_log=True,
            studio_url=studio_url,
            use_monitor=True,
        )
        
        print("✅ AgentScope 初始化成功！")
        
        # 等待目录创建
        time.sleep(3)
        
        # 获取运行ID
        runs_dir = "runs"
        if os.path.exists(runs_dir):
            run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
            if run_dirs:
                latest_run_dir = max(run_dirs, key=os.path.getmtime)
                current_run_id = os.path.basename(latest_run_dir)
                
                # 确保配置文件正确
                config_file = os.path.join(latest_run_dir, ".config")
                if os.path.exists(config_file):
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    
                    # 修复配置
                    config['studio_url'] = studio_url
                    config.setdefault('file', {})['save_api_invoke'] = True
                    config.setdefault('monitor', {})['use_monitor'] = True
                    
                    with open(config_file, 'w') as f:
                        json.dump(config, f, indent=4)
                    
                    print("🔧 配置文件已优化")
                    
                    # 注册到Studio
                    register_run_to_studio(current_run_id, config)
                    
                    # 启动心跳线程
                    heartbeat = threading.Thread(target=heartbeat_thread, args=(current_run_id,), daemon=True)
                    heartbeat.start()
                    print("💓 心跳线程已启动")
        
        if not current_run_id:
            print("❌ 无法获取运行ID")
            return False
        
        print(f"\n🎯 Studio Dashboard: {studio_url}/dashboard?run_id={current_run_id}")
        print("📱 请在浏览器中打开上述链接查看实时可视化界面")
        
        # 创建对话代理
        dialog_agent = DialogAgent(
            name="实时同步助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是AgentScope Studio实时同步测试助手。你的每条消息都会实时同步到可视化界面。请简洁地回答用户问题。"
        )
        
        print("\n💬 开始实时对话测试（输入 'exit' 退出）:")
        print("🤖 实时同步助手: 你好！现在开始测试实时同步功能。")
        print("-" * 60)
        
        # 推送欢迎消息到Studio
        push_message_to_studio(current_run_id, "你好！现在开始测试实时同步功能。", "assistant")
        
        conversation_count = 0
        
        while is_running:
            try:
                # 用户输入
                user_input = input("\n👤 您: ").strip()
                
                # 检查退出条件
                if user_input.lower() in ["exit", "quit", "退出", "结束"]:
                    break
                
                if not user_input:
                    continue
                
                conversation_count += 1
                print(f"\n[第{conversation_count}轮对话 - 实时同步中]")
                
                # 推送用户消息到Studio
                push_message_to_studio(current_run_id, user_input, "user")
                
                # 创建用户消息
                user_msg = Msg("user", user_input, "user")
                
                # AI回复
                print("🤖 AI正在思考（查看Studio实时显示）...")
                response = dialog_agent(user_msg)
                
                if hasattr(response, 'content'):
                    response_text = str(response.content)
                    print(f"🤖 实时同步助手: {response_text}")
                    
                    # 推送AI回复到Studio
                    push_message_to_studio(current_run_id, response_text, "assistant")
                    
                    print("✅ 消息已同步到Studio可视化界面")
                
            except EOFError:
                print("\n🔚 输入结束")
                break
            except KeyboardInterrupt:
                print("\n🛑 收到中断信号")
                break
            except Exception as e:
                print(f"❌ 对话异常: {e}")
                continue
        
        print(f"\n🎉 实时同步测试完成！")
        print(f"📊 共进行 {conversation_count} 轮对话")
        print(f"🔗 查看结果: {studio_url}/dashboard?run_id={current_run_id}")
        
    except Exception as e:
        print(f"❌ 程序异常: {e}")
    finally:
        graceful_shutdown()

if __name__ == "__main__":
    main() 
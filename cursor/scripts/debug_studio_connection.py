#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 连接问题诊断脚本
专门用于排查Dashboard数据不显示的问题
"""

import requests
import json
import time
import glob
import os
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg

# 测试配置
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

def check_studio_health():
    """检查Studio服务健康状态"""
    print("🏥 检查AgentScope Studio健康状态")
    print("=" * 50)
    
    checks = {
        "主页": "http://localhost:3000",
        "Dashboard": "http://localhost:3000/dashboard", 
        "API注册": "http://localhost:3000/trpc/registerRun",
        "推送消息": "http://localhost:3000/trpc/pushMessage",
        "模型调用": "http://localhost:3000/trpc/pushModelInvocation"
    }
    
    results = {}
    for name, url in checks.items():
        try:
            if "trpc" in url:
                # 对于API端点，使用HEAD请求
                response = requests.head(url, timeout=5)
            else:
                response = requests.get(url, timeout=5)
            
            status = "✅ 正常" if response.status_code in [200, 404, 405] else f"⚠️ {response.status_code}"
            results[name] = status
            print(f"  {name}: {status}")
            
        except requests.exceptions.ConnectionError:
            results[name] = "❌ 连接失败"
            print(f"  {name}: ❌ 连接失败")
        except Exception as e:
            results[name] = f"❌ {str(e)}"
            print(f"  {name}: ❌ {str(e)}")
    
    return results

def test_run_registration():
    """测试运行注册功能"""
    print("\n📝 测试运行注册功能")
    print("=" * 50)
    
    # 测试数据
    test_data = {
        "id": "test_run_debug",
        "project": "调试测试",
        "name": "debug_test",
        "timestamp": "2025-06-11 17:10:00",
        "run_dir": "/tmp/test_run",
        "pid": os.getpid(),
        "status": "running"
    }
    
    try:
        response = requests.post(
            "http://localhost:3000/trpc/registerRun",
            json=test_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 注册请求状态: {response.status_code}")
        print(f"📋 响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 运行注册功能正常")
            return True
        else:
            print(f"❌ 注册失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 注册请求异常: {e}")
        return False

def test_message_push():
    """测试消息推送功能"""
    print("\n💬 测试消息推送功能")
    print("=" * 50)
    
    # 测试消息数据
    test_message = {
        "runId": "test_run_debug",
        "replyId": "test_reply_123",
        "name": "test_reply_123",
        "role": "assistant",
        "msg": {
            "name": "test_agent",
            "content": "这是一条测试消息",
            "role": "assistant",
            "timestamp": "2025-06-11T17:10:00.000Z"
        }
    }
    
    try:
        response = requests.post(
            "http://localhost:3000/trpc/pushMessage",
            json=test_message,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 消息推送状态: {response.status_code}")
        print(f"📋 响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✅ 消息推送功能正常")
            return True
        else:
            print(f"❌ 消息推送失败: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ 消息推送异常: {e}")
        return False

def check_current_runs():
    """检查当前运行记录"""
    print("\n📁 检查当前运行记录")
    print("=" * 50)
    
    runs_dir = "runs"
    if not os.path.exists(runs_dir):
        print("❌ runs目录不存在")
        return None
    
    run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
    if not run_dirs:
        print("❌ 没有找到运行记录")
        return None
    
    # 按时间排序，显示最近的5个
    run_dirs.sort(key=os.path.getmtime, reverse=True)
    recent_runs = run_dirs[:5]
    
    print(f"📊 找到 {len(run_dirs)} 个运行记录，最近的5个：")
    
    for i, run_dir in enumerate(recent_runs, 1):
        run_id = os.path.basename(run_dir)
        mtime = os.path.getmtime(run_dir)
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
        
        print(f"  {i}. {run_id}")
        print(f"     时间: {formatted_time}")
        
        # 检查配置文件
        config_file = os.path.join(run_dir, ".config")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            studio_url = config.get('studio_url')
            save_api = config.get('file', {}).get('save_api_invoke', False)
            use_monitor = config.get('monitor', {}).get('use_monitor', False)
            
            print(f"     Studio URL: {studio_url}")
            print(f"     保存API调用: {save_api}")
            print(f"     启用监控: {use_monitor}")
            print(f"     项目: {config.get('project', 'N/A')}")
        print()
    
    return recent_runs[0] if recent_runs else None

def create_test_conversation():
    """创建测试对话并实时检查数据推送"""
    print("\n🧪 创建测试对话")
    print("=" * 50)
    
    try:
        print("🔧 初始化AgentScope...")
        
        # 重要：使用正确的配置
        agentscope.init(
            model_configs=MODEL_CONFIG,
            project="Studio连接调试",
            save_api_invoke=True,              # 必须启用
            studio_url="http://localhost:3000", # 必须设置
            use_monitor=True,                  # 必须启用
        )
        
        print("✅ AgentScope初始化成功")
        
        # 等待目录创建
        time.sleep(2)
        
        # 获取新创建的运行ID
        runs_dir = "runs"
        run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
        latest_run_dir = max(run_dirs, key=os.path.getmtime)
        run_id = os.path.basename(latest_run_dir)
        
        print(f"🎯 新运行ID: {run_id}")
        
        # 验证配置是否正确
        config_file = os.path.join(latest_run_dir, ".config")
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            print(f"✅ 配置验证:")
            print(f"   Studio URL: {config.get('studio_url')}")
            print(f"   保存API: {config.get('file', {}).get('save_api_invoke')}")
            print(f"   监控: {config.get('monitor', {}).get('use_monitor')}")
        
        # 创建智能体
        agent = DialogAgent(
            name="调试助手",
            model_config_name="qwen_turbo",
            sys_prompt="你是一个调试助手，请简短回答。"
        )
        
        print("\n💬 开始测试对话...")
        
        # 发送测试消息
        test_messages = [
            "你好，这是第一条测试消息",
            "请告诉我现在是什么时间",
            "测试完成"
        ]
        
        for i, user_input in enumerate(test_messages, 1):
            print(f"\n[测试 {i}/3]")
            print(f"👤 用户: {user_input}")
            
            # 创建用户消息
            user_msg = Msg("user", user_input, "user")
            
            try:
                # AI回复
                response = agent(user_msg)
                print(f"🤖 AI: {response.content}")
                print("📊 消息已发送到Studio")
                
                # 短暂等待
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ 对话失败: {e}")
                break
        
        # 生成访问URL
        studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
        print(f"\n🎯 测试完成！请访问:")
        print(f"📱 {studio_url}")
        
        return run_id
        
    except Exception as e:
        print(f"❌ 测试对话创建失败: {e}")
        return None

def check_dashboard_api(run_id):
    """检查Dashboard API数据"""
    print(f"\n🔍 检查Dashboard API数据 (run_id: {run_id})")
    print("=" * 50)
    
    # 检查是否有相关的API来获取运行数据
    api_endpoints = [
        f"http://localhost:3000/api/runs",
        f"http://localhost:3000/api/runs/{run_id}",
        f"http://localhost:3000/trpc/getRun?input=%7B%22runId%22%3A%22{run_id}%22%7D",
    ]
    
    for endpoint in api_endpoints:
        try:
            response = requests.get(endpoint, timeout=5)
            print(f"📡 {endpoint}")
            print(f"   状态: {response.status_code}")
            if response.status_code == 200:
                print(f"   数据: {response.text[:200]}...")
            else:
                print(f"   错误: {response.text}")
        except Exception as e:
            print(f"📡 {endpoint}")
            print(f"   异常: {e}")
        print()

def main():
    """主诊断流程"""
    print("🔧 AgentScope Studio 连接诊断工具")
    print("=" * 60)
    print("📋 此工具将帮您诊断为什么Dashboard不显示数据")
    print("=" * 60)
    
    # 1. 检查Studio健康状态
    health_results = check_studio_health()
    
    # 2. 检查当前运行记录
    latest_run = check_current_runs()
    
    # 3. 测试运行注册
    registration_ok = test_run_registration()
    
    # 4. 测试消息推送
    message_push_ok = test_message_push()
    
    # 5. 创建测试对话
    test_run_id = create_test_conversation()
    
    # 6. 检查Dashboard API
    if test_run_id:
        check_dashboard_api(test_run_id)
    
    # 7. 总结诊断结果
    print("\n📊 诊断结果总结")
    print("=" * 50)
    
    if all(health_results.values()):
        print("✅ Studio服务健康检查: 通过")
    else:
        print("❌ Studio服务健康检查: 失败")
        print("   请检查Studio是否正确启动")
    
    if registration_ok:
        print("✅ 运行注册功能: 正常")
    else:
        print("❌ 运行注册功能: 异常")
        print("   这可能是数据不显示的主要原因")
    
    if message_push_ok:
        print("✅ 消息推送功能: 正常")
    else:
        print("❌ 消息推送功能: 异常")
        print("   消息无法推送到Studio")
    
    if test_run_id:
        print(f"✅ 测试对话创建: 成功 ({test_run_id})")
        print(f"🎯 请访问: http://localhost:3000/dashboard?run_id={test_run_id}")
        print("   如果这个测试对话也看不到数据，说明是Studio前端问题")
    else:
        print("❌ 测试对话创建: 失败")
    
    print("\n💡 建议:")
    if not registration_ok or not message_push_ok:
        print("1. 重启AgentScope Studio: 在终端按Ctrl+C然后运行 as_studio")
        print("2. 检查端口3000是否被其他程序占用")
        print("3. 尝试更新AgentScope Studio: npm update -g @agentscope/studio")
    
    if test_run_id and registration_ok and message_push_ok:
        print("1. 清除浏览器缓存并硬刷新 (Cmd+Shift+R)")
        print("2. 尝试不同的浏览器")
        print("3. 检查浏览器开发者工具的控制台是否有JavaScript错误")

if __name__ == "__main__":
    main() 
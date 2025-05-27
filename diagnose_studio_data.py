#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 数据连接诊断脚本
检查为什么可视化看板没有数据
"""

import os
import sqlite3
import json
import requests
import glob
from datetime import datetime

def check_studio_status():
    """检查Studio服务状态"""
    print("🔍 检查AgentScope Studio服务状态...")
    
    try:
        # 检查主页
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"✅ Studio主页响应: {response.status_code}")
        
        # 检查dashboard页面
        dashboard_response = requests.get("http://localhost:3000/dashboard", timeout=5)
        print(f"✅ Dashboard页面响应: {dashboard_response.status_code}")
        
        # 检查API端点
        try:
            api_response = requests.get("http://localhost:3000/api/runs", timeout=5)
            print(f"✅ API端点响应: {api_response.status_code}")
            if api_response.status_code == 200:
                runs_data = api_response.json()
                print(f"📊 API返回的运行记录数量: {len(runs_data) if isinstance(runs_data, list) else 'N/A'}")
        except Exception as e:
            print(f"⚠️ API端点检查失败: {e}")
        
        return True
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到AgentScope Studio")
        return False
    except Exception as e:
        print(f"❌ Studio状态检查失败: {e}")
        return False

def check_run_data(run_id):
    """检查运行数据的完整性"""
    print(f"\n🔍 检查运行数据: {run_id}")
    
    run_dir = os.path.join("runs", run_id)
    if not os.path.exists(run_dir):
        print(f"❌ 运行目录不存在: {run_dir}")
        return False
    
    # 检查必要文件
    required_files = [".config", "agentscope.db", "logging.chat"]
    missing_files = []
    
    for file in required_files:
        file_path = os.path.join(run_dir, file)
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"✅ {file}: {file_size} bytes")
        else:
            missing_files.append(file)
            print(f"❌ {file}: 文件不存在")
    
    if missing_files:
        print(f"⚠️ 缺少文件: {missing_files}")
        return False
    
    # 检查配置文件
    config_path = os.path.join(run_dir, ".config")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.load(f)
        print(f"✅ 配置文件解析成功")
        print(f"   - 项目名: {config_data.get('project', 'N/A')}")
        print(f"   - 运行ID: {config_data.get('run_id', 'N/A')}")
        print(f"   - Studio URL: {config_data.get('studio_url', 'N/A')}")
    except Exception as e:
        print(f"❌ 配置文件解析失败: {e}")
        return False
    
    # 检查数据库
    db_path = os.path.join(run_dir, "agentscope.db")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 获取表列表
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"✅ 数据库表: {[table[0] for table in tables]}")
        
        # 检查消息表
        if ('message',) in tables:
            cursor.execute("SELECT COUNT(*) FROM message;")
            message_count = cursor.fetchone()[0]
            print(f"📊 消息数量: {message_count}")
            
            if message_count > 0:
                cursor.execute("SELECT * FROM message LIMIT 3;")
                sample_messages = cursor.fetchall()
                print(f"📝 示例消息: {len(sample_messages)} 条")
        
        conn.close()
    except Exception as e:
        print(f"❌ 数据库检查失败: {e}")
        return False
    
    return True

def test_studio_api_with_run_id(run_id):
    """测试Studio API是否能正确识别运行ID"""
    print(f"\n🔍 测试Studio API对运行ID的识别: {run_id}")
    
    try:
        # 测试获取特定运行的数据
        api_url = f"http://localhost:3000/api/runs/{run_id}"
        response = requests.get(api_url, timeout=5)
        print(f"📡 API请求: {api_url}")
        print(f"📊 响应状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功获取运行数据")
            print(f"   - 数据类型: {type(data)}")
            if isinstance(data, dict):
                print(f"   - 数据键: {list(data.keys())}")
        elif response.status_code == 404:
            print(f"❌ 运行ID未找到 - Studio可能没有正确注册这个运行")
        else:
            print(f"⚠️ 意外的响应状态码: {response.status_code}")
            print(f"   响应内容: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ API测试失败: {e}")

def check_studio_registration():
    """检查Studio是否正确注册了运行"""
    print(f"\n🔍 检查Studio运行注册状态...")
    
    try:
        # 获取所有注册的运行
        response = requests.get("http://localhost:3000/api/runs", timeout=5)
        if response.status_code == 200:
            runs = response.json()
            print(f"📊 Studio中注册的运行数量: {len(runs) if isinstance(runs, list) else 'N/A'}")
            
            if isinstance(runs, list) and runs:
                print("📝 注册的运行列表:")
                for run in runs[:5]:  # 只显示前5个
                    if isinstance(run, dict):
                        run_id = run.get('id', 'N/A')
                        status = run.get('status', 'N/A')
                        print(f"   - {run_id}: {status}")
            else:
                print("⚠️ 没有找到注册的运行")
        else:
            print(f"❌ 无法获取运行列表: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 检查注册状态失败: {e}")

def suggest_solutions():
    """提供解决方案建议"""
    print(f"\n💡 可能的解决方案:")
    print("1. 重启AgentScope Studio:")
    print("   - 停止当前Studio: Ctrl+C")
    print("   - 重新启动: as_studio")
    
    print("\n2. 清理并重新运行:")
    print("   - 删除旧的运行数据: rm -rf runs/*")
    print("   - 重新运行脚本: python3 chat_with_studio.py")
    
    print("\n3. 检查Studio版本:")
    print("   - 更新Studio: npm update -g @agentscope/studio")
    print("   - 或重新安装: npm uninstall -g @agentscope/studio && npm install -g @agentscope/studio")
    
    print("\n4. 手动注册运行到Studio:")
    print("   - 确保在运行脚本时Studio已经启动")
    print("   - 检查网络连接和端口占用")

def main():
    print("🔧 AgentScope Studio 数据连接诊断工具")
    print("=" * 60)
    
    # 1. 检查Studio服务状态
    if not check_studio_status():
        print("\n❌ Studio服务未正常运行，请先启动Studio")
        return
    
    # 2. 获取最新运行ID
    runs_dir = "runs"
    if not os.path.exists(runs_dir):
        print("\n❌ 未找到runs目录")
        return
    
    run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
    if not run_dirs:
        print("\n❌ 未找到任何运行记录")
        return
    
    latest_run_dir = max(run_dirs, key=os.path.getmtime)
    run_id = os.path.basename(latest_run_dir)
    print(f"\n🎯 检查最新运行: {run_id}")
    
    # 3. 检查运行数据
    if not check_run_data(run_id):
        print("\n❌ 运行数据不完整")
        suggest_solutions()
        return
    
    # 4. 测试Studio API
    test_studio_api_with_run_id(run_id)
    
    # 5. 检查Studio注册状态
    check_studio_registration()
    
    # 6. 提供解决方案
    suggest_solutions()
    
    print(f"\n🎯 建议的访问URL:")
    print(f"📱 http://localhost:3000/dashboard?run_id={run_id}")
    print(f"📱 http://localhost:3000/dashboard")

if __name__ == "__main__":
    main() 
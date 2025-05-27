#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AgentScope Studio 调试脚本
检查Studio前端显示问题
"""

import requests
import json
import time
import glob
import os

def check_studio_api():
    """检查Studio API状态"""
    print("🔍 检查Studio API状态")
    print("=" * 40)
    
    # 检查基本连接
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"✅ Studio主页: {response.status_code}")
    except Exception as e:
        print(f"❌ Studio主页连接失败: {e}")
        return False
    
    # 检查Dashboard页面
    try:
        response = requests.get("http://localhost:3000/dashboard", timeout=5)
        print(f"✅ Dashboard页面: {response.status_code}")
    except Exception as e:
        print(f"❌ Dashboard页面连接失败: {e}")
        return False
    
    return True

def test_studio_registration():
    """测试Studio运行注册"""
    print("\n🔧 测试Studio运行注册")
    print("=" * 40)
    
    # 获取最新运行
    runs_dir = "runs"
    if not os.path.exists(runs_dir):
        print("❌ runs目录不存在")
        return None
    
    run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
    if not run_dirs:
        print("❌ 没有找到运行记录")
        return None
    
    latest_run_dir = max(run_dirs, key=os.path.getmtime)
    run_id = os.path.basename(latest_run_dir)
    print(f"📊 最新运行: {run_id}")
    
    # 读取配置
    config_file = os.path.join(latest_run_dir, ".config")
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
        print(f"✅ 配置文件: {config.get('project', 'N/A')}")
    else:
        print("❌ 配置文件不存在")
        return None
    
    # 手动注册到Studio
    register_data = {
        "id": run_id,
        "project": config.get('project', 'Test Project'),
        "name": config.get('name', 'test'),
        "timestamp": config.get('timestamp', time.strftime('%Y-%m-%d %H:%M:%S')),
        "run_dir": os.path.abspath(latest_run_dir),
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
        print(f"📡 注册响应: {response.status_code}")
        if response.status_code == 200:
            print("✅ 运行注册成功")
        else:
            print(f"❌ 注册失败: {response.text}")
    except Exception as e:
        print(f"❌ 注册请求失败: {e}")
    
    return run_id

def check_browser_cache():
    """检查浏览器缓存问题"""
    print("\n🌐 浏览器缓存检查")
    print("=" * 40)
    
    print("💡 可能的解决方案:")
    print("1. 硬刷新浏览器页面 (Ctrl+F5 或 Cmd+Shift+R)")
    print("2. 清除浏览器缓存")
    print("3. 使用无痕/隐私模式打开")
    print("4. 尝试不同的浏览器")

def test_different_urls(run_id):
    """测试不同的URL格式"""
    print(f"\n🔗 测试不同URL格式")
    print("=" * 40)
    
    urls = [
        f"http://localhost:3000/dashboard?run_id={run_id}",
        f"http://localhost:3000/?run_id={run_id}",
        "http://localhost:3000/dashboard",
        "http://localhost:3000"
    ]
    
    for url in urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url}: {response.status_code}")
        except Exception as e:
            print(f"❌ {url}: {e}")

def check_studio_logs():
    """检查Studio日志"""
    print(f"\n📋 Studio状态检查")
    print("=" * 40)
    
    print("💡 请检查以下内容:")
    print("1. Studio控制台是否有错误信息")
    print("2. 浏览器开发者工具中的错误")
    print("3. 网络请求是否正常")
    print("4. 是否有JavaScript错误")

def main():
    print("🔧 AgentScope Studio 调试工具")
    print("=" * 60)
    
    # 1. 检查Studio API
    if not check_studio_api():
        print("\n❌ Studio API检查失败，请重启Studio")
        return
    
    # 2. 测试运行注册
    run_id = test_studio_registration()
    if not run_id:
        print("\n❌ 运行注册失败")
        return
    
    # 3. 测试不同URL
    test_different_urls(run_id)
    
    # 4. 检查浏览器缓存
    check_browser_cache()
    
    # 5. 检查Studio日志
    check_studio_logs()
    
    print(f"\n🎯 建议的测试步骤:")
    print(f"1. 打开: http://localhost:3000/dashboard?run_id={run_id}")
    print(f"2. 硬刷新页面 (Ctrl+F5)")
    print(f"3. 检查浏览器开发者工具的Console和Network标签")
    print(f"4. 如果还是看不到数据，尝试重启Studio")

if __name__ == "__main__":
    main() 
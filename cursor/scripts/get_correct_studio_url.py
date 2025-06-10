#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取正确的 AgentScope Studio 访问URL
解决重定向到 /home 的问题
"""

import os
import glob
from datetime import datetime

def get_latest_run_id():
    """获取最新的运行ID"""
    runs_dir = "runs"
    
    if not os.path.exists(runs_dir):
        print("❌ 未找到runs目录，请先运行AgentScope应用")
        return None
    
    # 获取所有运行目录
    run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
    
    if not run_dirs:
        print("❌ 未找到任何运行记录，请先运行AgentScope应用")
        return None
    
    # 按修改时间排序，获取最新的
    latest_run_dir = max(run_dirs, key=os.path.getmtime)
    run_id = os.path.basename(latest_run_dir)
    
    return run_id

def main():
    print("🔍 获取正确的 AgentScope Studio 访问URL")
    print("=" * 60)
    
    # 获取最新运行ID
    run_id = get_latest_run_id()
    
    if run_id:
        # 提供多种正确的访问方式
        dashboard_url = f"http://localhost:3000/dashboard?run_id={run_id}"
        dashboard_main = "http://localhost:3000/dashboard"
        
        print(f"✅ 找到最新运行记录: {run_id}")
        print(f"\n🎯 请使用以下正确的URL访问可视化界面：")
        print(f"\n📱 方式1 - 直接访问特定运行:")
        print(f"   {dashboard_url}")
        print(f"\n📱 方式2 - 访问Dashboard主页:")
        print(f"   {dashboard_main}")
        print(f"   然后在页面中选择运行记录: {run_id}")
        
        print(f"\n💡 使用说明：")
        print(f"   1. 确保AgentScope Studio正在运行 (as_studio)")
        print(f"   2. 复制上面的URL到浏览器")
        print(f"   3. 避免使用根路径 http://localhost:3000/?run_id=xxx")
        
        # 检查运行目录的详细信息
        run_dir = os.path.join("runs", run_id)
        if os.path.exists(run_dir):
            mtime = os.path.getmtime(run_dir)
            formatted_time = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
            print(f"\n📊 运行信息：")
            print(f"   - 运行ID: {run_id}")
            print(f"   - 最后更新: {formatted_time}")
            print(f"   - 目录路径: {run_dir}")
            
            # 检查运行目录中的文件
            files = os.listdir(run_dir)
            print(f"   - 包含文件: {', '.join(files)}")
    else:
        print("❌ 未找到运行记录")
        print("\n💡 解决方案：")
        print("   1. 先启动Studio: as_studio")
        print("   2. 运行AgentScope应用: python3 chat_with_studio.py")
        print("   3. 再次运行此脚本获取URL")

if __name__ == "__main__":
    main() 
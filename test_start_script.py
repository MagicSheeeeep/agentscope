#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的 start_agentscope.py 脚本
"""

import subprocess
import time
import requests
import glob
import os

def test_start_script():
    """测试start_agentscope.py脚本的Studio连接"""
    print("🧪 测试修复后的 start_agentscope.py 脚本")
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
    
    print("\n🚀 启动start_agentscope.py脚本进行测试...")
    print("💡 脚本将自动发送测试消息并退出")
    
    # 准备测试输入
    test_input = "你好，这是一个测试消息\nexit\n"
    
    try:
        # 运行脚本
        process = subprocess.Popen(
            ["python3", "start_agentscope.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # 发送测试输入
        stdout, stderr = process.communicate(input=test_input, timeout=30)
        
        print("📝 脚本输出:")
        print(stdout)
        
        if stderr:
            print("⚠️ 错误信息:")
            print(stderr)
        
        # 检查是否生成了新的运行
        runs_dir = "runs"
        if os.path.exists(runs_dir):
            run_dirs = glob.glob(os.path.join(runs_dir, "run_*"))
            if run_dirs:
                latest_run_dir = max(run_dirs, key=os.path.getmtime)
                run_id = os.path.basename(latest_run_dir)
                
                # 检查运行是否是最近创建的
                run_time = os.path.getmtime(latest_run_dir)
                current_time = time.time()
                
                if current_time - run_time < 60:  # 1分钟内创建的
                    print(f"\n✅ 检测到新的运行: {run_id}")
                    studio_url = f"http://localhost:3000/dashboard?run_id={run_id}"
                    print(f"🎯 可视化界面: {studio_url}")
                    
                    # 检查运行目录中的文件
                    config_file = os.path.join(latest_run_dir, ".config")
                    db_file = os.path.join(latest_run_dir, "agentscope.db")
                    chat_file = os.path.join(latest_run_dir, "logging.chat")
                    
                    print(f"\n📊 运行数据检查:")
                    print(f"   - 配置文件: {'✅' if os.path.exists(config_file) else '❌'}")
                    print(f"   - 数据库文件: {'✅' if os.path.exists(db_file) else '❌'}")
                    print(f"   - 聊天日志: {'✅' if os.path.exists(chat_file) else '❌'}")
                    
                    if os.path.exists(chat_file):
                        file_size = os.path.getsize(chat_file)
                        print(f"   - 聊天日志大小: {file_size} bytes")
                        
                        if file_size > 0:
                            print("✅ 聊天数据已保存，应该能在Studio中显示")
                        else:
                            print("⚠️ 聊天日志为空，可能没有保存对话数据")
                    
                    return run_id
                else:
                    print("⚠️ 没有检测到新的运行记录")
            else:
                print("❌ 没有找到任何运行记录")
        else:
            print("❌ runs目录不存在")
        
        return None
        
    except subprocess.TimeoutExpired:
        print("❌ 脚本运行超时")
        process.kill()
        return None
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return None

def main():
    run_id = test_start_script()
    
    if run_id:
        print(f"\n🎉 测试成功！")
        print(f"📱 请访问: http://localhost:3000/dashboard?run_id={run_id}")
        print(f"💡 现在start_agentscope.py脚本应该能在Studio中显示数据了")
    else:
        print(f"\n❌ 测试失败，请检查配置")

if __name__ == "__main__":
    main() 
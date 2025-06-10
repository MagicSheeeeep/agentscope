#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 start_agentscope.py 的交互功能
"""

import subprocess
import time
import threading
import sys

def test_interactive_script():
    """测试脚本的交互功能"""
    print("🧪 测试 start_agentscope.py 的交互功能")
    print("=" * 50)
    
    try:
        # 启动脚本
        process = subprocess.Popen(
            ["python3", "start_agentscope.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        def read_output():
            """读取脚本输出"""
            while True:
                line = process.stdout.readline()
                if line:
                    print(f"[脚本输出] {line.rstrip()}")
                else:
                    break
        
        # 启动输出读取线程
        output_thread = threading.Thread(target=read_output)
        output_thread.daemon = True
        output_thread.start()
        
        # 等待脚本初始化
        print("⏳ 等待脚本初始化...")
        time.sleep(5)
        
        # 发送测试消息
        test_message = "你好，这是一个测试消息\n"
        print(f"📤 发送测试消息: {test_message.strip()}")
        process.stdin.write(test_message)
        process.stdin.flush()
        
        # 等待回复
        print("⏳ 等待AI回复...")
        time.sleep(10)
        
        # 发送退出命令
        exit_command = "exit\n"
        print(f"📤 发送退出命令: {exit_command.strip()}")
        process.stdin.write(exit_command)
        process.stdin.flush()
        
        # 等待进程结束
        process.wait(timeout=10)
        
        print("✅ 脚本测试完成")
        return True
        
    except subprocess.TimeoutExpired:
        print("⚠️ 脚本运行超时，强制终止")
        process.kill()
        return False
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        return False

def simple_run_test():
    """简单运行测试"""
    print("\n🚀 简单运行测试")
    print("=" * 30)
    
    print("💡 请手动运行以下命令来测试脚本:")
    print("   python3 start_agentscope.py")
    print("\n📝 测试步骤:")
    print("1. 运行脚本后，应该看到初始化信息")
    print("2. 看到 '🎯 可视化界面:' 的URL")
    print("3. 看到提示 '请输入您的消息:'")
    print("4. 输入测试消息，如 '你好'")
    print("5. 等待AI回复")
    print("6. 输入 'exit' 退出")

if __name__ == "__main__":
    print("选择测试方式:")
    print("1. 自动测试（可能不稳定）")
    print("2. 手动测试指导")
    
    choice = input("请选择 (1 或 2): ").strip()
    
    if choice == "1":
        test_interactive_script()
    else:
        simple_run_test() 
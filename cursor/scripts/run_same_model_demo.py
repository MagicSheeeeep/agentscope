#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
同一模型多智能体快速演示脚本
"""

import os
import sys

def check_dependencies():
    """检查依赖"""
    try:
        import agentscope
        print("✅ AgentScope 已安装")
        return True
    except ImportError:
        print("❌ 请先安装 AgentScope: pip install agentscope")
        return False

def get_api_key():
    """获取API密钥"""
    # 首先检查环境变量
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if api_key:
        print("✅ 从环境变量获取到API密钥")
        return api_key
    
    # 手动输入
    print("🔑 请输入您的DashScope API密钥:")
    api_key = input("API Key: ").strip()
    if not api_key:
        print("❌ 未提供API密钥")
        return None
    
    return api_key

def run_simple_demo():
    """运行简单演示"""
    print("🚀 启动简单演示...")
    try:
        from simple_same_model_example import main
        main()
    except ImportError:
        print("❌ 找不到 simple_same_model_example.py 文件")
    except Exception as e:
        print(f"❌ 演示运行失败: {e}")

def run_advanced_demo():
    """运行高级演示"""
    print("🚀 启动高级演示...")
    try:
        import asyncio
        from same_model_multi_agents import demo_same_model_agents
        asyncio.run(demo_same_model_agents())
    except ImportError:
        print("❌ 找不到 same_model_multi_agents.py 文件")
    except Exception as e:
        print(f"❌ 演示运行失败: {e}")

def run_interactive_mode():
    """运行交互模式"""
    print("🎮 启动交互模式...")
    try:
        import asyncio
        from same_model_multi_agents import interactive_mode
        asyncio.run(interactive_mode())
    except ImportError:
        print("❌ 找不到 same_model_multi_agents.py 文件")
    except Exception as e:
        print(f"❌ 交互模式运行失败: {e}")

def show_menu():
    """显示菜单"""
    menu = """
🤖 同一模型多智能体演示

请选择运行模式:
1. 简单演示 - 三种基本实现方式
2. 高级演示 - 完整的多智能体系统
3. 交互模式 - 手动测试各种功能
4. 查看文档 - 显示使用说明
5. 退出

"""
    print(menu)

def show_documentation():
    """显示文档"""
    doc = """
📚 使用说明

## 三种实现方式

1. **共享模型配置**
   - 所有智能体使用同一个模型配置
   - 通过不同的系统提示创建不同角色
   - 最简单的实现方式

2. **不同参数配置**
   - 使用同一模型但配置不同参数（如temperature）
   - 创建不同风格的智能体（保守vs创意）
   - 适合需要不同生成风格的场景

3. **基于角色的提示**
   - 使用详细的角色系统提示
   - 创建专业化的智能体
   - 适合复杂的多角色协作场景

## 应用场景

- **团队协作模拟**: 产品经理、技术专家、设计师等
- **教育场景**: 老师、学生、助教等
- **咨询服务**: 法律、财务、健康等多领域专家
- **创意协作**: 作家、编辑、评论家等

## 优势

- 成本效益：只需一个API密钥
- 一致性：统一的语言模型基础
- 灵活性：通过提示工程创建多样化角色
- 简化管理：减少配置复杂性

按任意键返回主菜单...
"""
    print(doc)
    input()

def main():
    """主函数"""
    print("🤖 同一模型多智能体演示系统")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查API密钥
    api_key = get_api_key()
    if not api_key:
        return
    
    # 设置环境变量（如果还没有的话）
    if not os.getenv("DASHSCOPE_API_KEY"):
        os.environ["DASHSCOPE_API_KEY"] = api_key
    
    print("✅ 系统准备就绪")
    
    # 主循环
    while True:
        show_menu()
        choice = input("请选择 (1-5): ").strip()
        
        if choice == "1":
            run_simple_demo()
        elif choice == "2":
            run_advanced_demo()
        elif choice == "3":
            run_interactive_mode()
        elif choice == "4":
            show_documentation()
        elif choice == "5":
            print("👋 再见!")
            break
        else:
            print("❌ 无效选择，请重试")
        
        if choice in ["1", "2", "3"]:
            input("\n按回车键继续...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序异常: {e}") 
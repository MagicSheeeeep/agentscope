#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多模型编排系统启动脚本
快速配置和运行多模型编排系统
"""

import os
import sys
import asyncio
from typing import List

# 检查依赖
try:
    import agentscope
    from multi_model_orchestration import (
        MultiModelOrchestrator, 
        ModelConfig, 
        OrchestrationStrategy,
        MultiModelApplication
    )
except ImportError as e:
    print(f"❌ 导入错误: {e}")
    print("请确保已安装AgentScope: pip install agentscope")
    sys.exit(1)


def check_api_keys():
    """检查API密钥配置"""
    print("🔑 检查API密钥配置...")
    
    dashscope_key = os.getenv("DASHSCOPE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if not dashscope_key and not openai_key:
        print("⚠️  未检测到API密钥环境变量")
        print("请设置以下环境变量之一:")
        print("  export DASHSCOPE_API_KEY='your_key'")
        print("  export OPENAI_API_KEY='your_key'")
        
        # 提供手动输入选项
        choice = input("\n是否手动输入API密钥? (y/n): ").lower()
        if choice == 'y':
            return input_api_keys()
        else:
            return None
    
    return {
        "dashscope": dashscope_key,
        "openai": openai_key
    }


def input_api_keys():
    """手动输入API密钥"""
    keys = {}
    
    print("\n请输入API密钥 (直接回车跳过):")
    
    dashscope_key = input("DashScope API Key: ").strip()
    if dashscope_key:
        keys["dashscope"] = dashscope_key
    
    openai_key = input("OpenAI API Key: ").strip()
    if openai_key:
        keys["openai"] = openai_key
    
    if not keys:
        print("❌ 未提供任何API密钥")
        return None
    
    return keys


def create_model_configs(api_keys: dict) -> List[ModelConfig]:
    """根据可用的API密钥创建模型配置"""
    configs = []
    
    if "dashscope" in api_keys and api_keys["dashscope"]:
        configs.extend([
            ModelConfig(
                name="通用助手",
                config_name="general_assistant",
                model_type="dashscope_chat",
                model_name="qwen-max",
                api_key=api_keys["dashscope"],
                specialty="通用问题",
                weight=1.0,
                temperature=0.7
            ),
            ModelConfig(
                name="技术专家",
                config_name="tech_expert",
                model_type="dashscope_chat",
                model_name="qwen-turbo",
                api_key=api_keys["dashscope"],
                specialty="技术和编程",
                weight=1.2,
                temperature=0.5
            ),
            ModelConfig(
                name="创意助手",
                config_name="creative_assistant",
                model_type="dashscope_chat",
                model_name="qwen-plus",
                api_key=api_keys["dashscope"],
                specialty="创意和写作",
                weight=0.9,
                temperature=0.9
            )
        ])
    
    if "openai" in api_keys and api_keys["openai"]:
        configs.extend([
            ModelConfig(
                name="GPT-4助手",
                config_name="gpt4_assistant",
                model_type="openai_chat",
                model_name="gpt-4",
                api_key=api_keys["openai"],
                specialty="高级推理",
                weight=1.3,
                temperature=0.7
            ),
            ModelConfig(
                name="GPT-3.5助手",
                config_name="gpt35_assistant",
                model_type="openai_chat",
                model_name="gpt-3.5-turbo",
                api_key=api_keys["openai"],
                specialty="快速响应",
                weight=1.0,
                temperature=0.8
            )
        ])
    
    return configs


async def quick_test(orchestrator: MultiModelOrchestrator):
    """快速测试"""
    print("\n🧪 运行快速测试...")
    
    test_query = "请简单介绍一下人工智能"
    
    try:
        result = await orchestrator.orchestrate(
            test_query,
            OrchestrationStrategy.EXPERT_ROUTING
        )
        
        print(f"✅ 测试成功!")
        print(f"📝 查询: {test_query}")
        print(f"⏱️ 耗时: {result.execution_time:.2f}秒")
        print(f"📋 结果: {result.final_result[:150]}...")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False


def show_menu():
    """显示菜单"""
    menu = """
🎯 多模型编排系统

请选择运行模式:
1. 快速演示 - 自动测试各种策略
2. 交互模式 - 手动输入问题测试  
3. 简化示例 - 运行预设示例
4. 快速测试 - 验证系统配置
5. 退出

"""
    print(menu)


async def main():
    """主函数"""
    print("🚀 多模型编排系统启动器")
    print("=" * 50)
    
    # 检查API密钥
    api_keys = check_api_keys()
    if not api_keys:
        print("❌ 无法获取API密钥，程序退出")
        return
    
    # 创建模型配置
    model_configs = create_model_configs(api_keys)
    if not model_configs:
        print("❌ 无法创建模型配置，程序退出")
        return
    
    print(f"✅ 成功配置 {len(model_configs)} 个模型:")
    for config in model_configs:
        print(f"  - {config.name} ({config.model_name})")
    
    # 创建编排器
    try:
        orchestrator = MultiModelOrchestrator(model_configs)
        print("✅ 编排器初始化成功")
    except Exception as e:
        print(f"❌ 编排器初始化失败: {str(e)}")
        return
    
    # 主循环
    while True:
        show_menu()
        choice = input("请选择 (1-5): ").strip()
        
        if choice == "1":
            # 快速演示
            app = MultiModelApplication()
            app.orchestrator = orchestrator  # 使用我们配置的编排器
            await app.run_demo()
            
        elif choice == "2":
            # 交互模式
            app = MultiModelApplication()
            app.orchestrator = orchestrator
            await app.interactive_mode()
            
        elif choice == "3":
            # 简化示例
            from simple_orchestration_example import main as simple_main
            # 修改示例中的配置
            import simple_orchestration_example
            simple_orchestration_example.model_configs = model_configs
            await simple_main()
            
        elif choice == "4":
            # 快速测试
            success = await quick_test(orchestrator)
            if success:
                print("🎉 系统配置正常，可以正常使用!")
            else:
                print("⚠️  系统配置可能有问题，请检查API密钥和网络连接")
                
        elif choice == "5":
            print("👋 再见!")
            break
            
        else:
            print("❌ 无效选择，请重试")
        
        input("\n按回车键继续...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序异常: {str(e)}")
        print("请检查配置和网络连接") 
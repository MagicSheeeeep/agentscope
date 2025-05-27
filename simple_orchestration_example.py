#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的多模型编排示例
展示如何快速使用多模型编排功能
"""

import asyncio
from multi_model_orchestration import (
    MultiModelOrchestrator, 
    ModelConfig, 
    OrchestrationStrategy
)


async def quick_example():
    """快速示例"""
    print("🚀 多模型编排快速示例")
    print("=" * 40)
    
    # 配置模型（请替换为您的真实API密钥）
    model_configs = [
        ModelConfig(
            name="通用助手",
            config_name="general_assistant",
            model_type="dashscope_chat",
            model_name="qwen-max",
            api_key="sk-cc1605a341c4450489bd71ffc28238c0",  # 请替换为您的API密钥
            specialty="通用问题",
            weight=1.0,
            temperature=0.7
        ),
        ModelConfig(
            name="技术专家",
            config_name="tech_expert",
            model_type="dashscope_chat",
            model_name="qwen-turbo",
            api_key="sk-cc1605a341c4450489bd71ffc28238c0",  # 请替换为您的API密钥
            specialty="技术和编程",
            weight=1.2,
            temperature=0.5
        ),
        ModelConfig(
            name="创意助手",
            config_name="creative_assistant",
            model_type="dashscope_chat",
            model_name="qwen-plus",
            api_key="sk-cc1605a341c4450489bd71ffc28238c0",  # 请替换为您的API密钥
            specialty="创意和写作",
            weight=0.9,
            temperature=0.9
        )
    ]
    
    # 创建编排器
    orchestrator = MultiModelOrchestrator(model_configs)
    
    # 测试查询
    query = "请解释什么是机器学习，并给出一个简单的Python示例"
    
    print(f"📝 查询: {query}\n")
    
    # 测试不同的编排策略
    strategies = [
        (OrchestrationStrategy.EXPERT_ROUTING, "专家路由"),
        (OrchestrationStrategy.PARALLEL, "并行处理"),
        (OrchestrationStrategy.VOTING, "投票机制"),
        (OrchestrationStrategy.HIERARCHICAL, "分层处理")
    ]
    
    for strategy, description in strategies:
        print(f"🎯 测试策略: {description}")
        print("-" * 30)
        
        try:
            result = await orchestrator.orchestrate(query, strategy)
            
            print(f"⏱️ 执行时间: {result.execution_time:.2f}秒")
            print(f"📊 参与模型: {len(result.individual_results)}个")
            print(f"📋 结果预览: {result.final_result[:150]}...")
            print(f"🔍 策略详情: {result.metadata}")
            
        except Exception as e:
            print(f"❌ 执行失败: {str(e)}")
        
        print("\n" + "="*40 + "\n")


async def comparison_example():
    """对比示例 - 展示不同策略的差异"""
    print("🔍 策略对比示例")
    print("=" * 40)
    
    # 简化配置 - 只使用两个模型
    model_configs = [
        ModelConfig(
            name="分析师",
            config_name="analyst",
            model_type="dashscope_chat",
            model_name="qwen-max",
            api_key="sk-cc1605a341c4450489bd71ffc28238c0",
            specialty="数据分析",
            weight=1.0,
            temperature=0.3
        ),
        ModelConfig(
            name="顾问",
            config_name="advisor",
            model_type="dashscope_chat",
            model_name="qwen-turbo",
            api_key="sk-cc1605a341c4450489bd71ffc28238c0",
            specialty="商业建议",
            weight=1.0,
            temperature=0.7
        )
    ]
    
    orchestrator = MultiModelOrchestrator(model_configs)
    
    # 商业问题
    query = "如何提高电商网站的转化率？"
    
    print(f"📝 商业问题: {query}\n")
    
    # 对比并行处理和专家路由
    strategies_to_compare = [
        OrchestrationStrategy.PARALLEL,
        OrchestrationStrategy.EXPERT_ROUTING
    ]
    
    results = {}
    
    for strategy in strategies_to_compare:
        print(f"🔄 执行策略: {strategy.value}")
        result = await orchestrator.orchestrate(query, strategy)
        results[strategy.value] = result
        print(f"✅ 完成，耗时: {result.execution_time:.2f}秒\n")
    
    # 显示对比结果
    print("📊 结果对比:")
    print("=" * 40)
    
    for strategy_name, result in results.items():
        print(f"\n🎯 {strategy_name}:")
        print(f"⏱️ 时间: {result.execution_time:.2f}秒")
        print(f"📝 结果: {result.final_result[:200]}...")
        print(f"🔧 元数据: {result.metadata}")


async def custom_pipeline_example():
    """自定义流水线示例"""
    print("⚙️ 自定义流水线示例")
    print("=" * 40)
    
    model_configs = [
        ModelConfig(
            name="研究员",
            config_name="researcher",
            model_type="dashscope_chat",
            model_name="qwen-max",
            api_key="sk-cc1605a341c4450489bd71ffc28238c0",
            specialty="信息研究",
            temperature=0.5
        ),
        ModelConfig(
            name="分析师",
            config_name="analyst",
            model_type="dashscope_chat",
            model_name="qwen-turbo",
            api_key="sk-cc1605a341c4450489bd71ffc28238c0",
            specialty="数据分析",
            temperature=0.3
        ),
        ModelConfig(
            name="总结师",
            config_name="summarizer",
            model_type="dashscope_chat",
            model_name="qwen-plus",
            api_key="sk-cc1605a341c4450489bd71ffc28238c0",
            specialty="信息总结",
            temperature=0.6
        )
    ]
    
    orchestrator = MultiModelOrchestrator(model_configs)
    
    query = "人工智能在医疗领域的应用前景如何？"
    
    # 自定义流水线阶段
    custom_stages = [
        {
            "name": "信息收集",
            "prompt": "请收集关于以下主题的详细信息：{query}"
        },
        {
            "name": "深度分析", 
            "prompt": "基于以下信息进行深度分析：\n{previous_output}\n\n请分析趋势、挑战和机遇。"
        },
        {
            "name": "结论总结",
            "prompt": "基于以下分析，提供简洁明了的总结和建议：\n{previous_output}"
        }
    ]
    
    print(f"📝 查询: {query}")
    print(f"🔧 自定义阶段: {[stage['name'] for stage in custom_stages]}\n")
    
    result = await orchestrator.orchestrate(
        query, 
        OrchestrationStrategy.PIPELINE,
        stages=custom_stages
    )
    
    print(f"✅ 流水线执行完成")
    print(f"⏱️ 总耗时: {result.execution_time:.2f}秒")
    print(f"📋 最终结果:\n{result.final_result}")
    
    print(f"\n🔍 各阶段详情:")
    for i, stage_result in enumerate(result.individual_results, 1):
        print(f"\n--- 阶段 {i}: {stage_result['stage']} ---")
        print(f"模型: {stage_result['model']}")
        print(f"结果: {stage_result['response'][:150]}...")


async def main():
    """主函数"""
    print("🎯 选择示例:")
    print("1. 快速示例 - 基本功能演示")
    print("2. 对比示例 - 策略效果对比")
    print("3. 自定义流水线 - 高级用法")
    print("4. 全部运行")
    
    choice = input("\n请选择 (1-4): ").strip()
    
    if choice == "1":
        await quick_example()
    elif choice == "2":
        await comparison_example()
    elif choice == "3":
        await custom_pipeline_example()
    elif choice == "4":
        await quick_example()
        await comparison_example()
        await custom_pipeline_example()
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    print("🚀 多模型编排系统 - 简化示例")
    print("=" * 50)
    print("⚠️  请确保已安装AgentScope并配置了正确的API密钥")
    print("=" * 50)
    
    asyncio.run(main()) 
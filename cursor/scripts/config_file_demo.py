#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
演示如何从配置文件加载模型配置
展示 AgentScope 的两种配置方式对比
"""

import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
import os
import json

def demo_hardcoded_config():
    """方式1：硬编码配置（当前脚本使用的方式）"""
    print("🔧 方式1：硬编码配置")
    print("=" * 50)
    
    # 硬编码的配置
    hardcoded_config = [
        {
            "config_name": "demo_qwen",
            "model_type": "dashscope_chat",
            "model_name": "qwen-turbo",
            "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
            "generate_args": {
                "temperature": 0.7,
                "max_tokens": 1000,
            }
        }
    ]
    
    print("📝 配置内容：直接在代码中定义")
    print(f"🎯 配置名称：{hardcoded_config[0]['config_name']}")
    print(f"🤖 模型类型：{hardcoded_config[0]['model_type']}")
    
    # 初始化
    agentscope.init(
        model_configs=hardcoded_config,
        project="硬编码配置演示",
    )
    
    # 创建代理
    agent = DialogAgent(
        name="硬编码助手",
        model_config_name="demo_qwen",
        sys_prompt="你是使用硬编码配置的助手"
    )
    
    # 测试对话
    msg = Msg("user", "请简单介绍一下你自己", "user")
    response = agent(msg)
    print(f"🤖 回复：{response.content}")
    print("✅ 硬编码配置方式演示完成\n")

def demo_config_file():
    """方式2：从配置文件加载"""
    print("🔧 方式2：从配置文件加载")
    print("=" * 50)
    
    # 配置文件路径
    config_file_path = "cursor/configs/model_configs.json"
    
    if not os.path.exists(config_file_path):
        print(f"❌ 配置文件不存在：{config_file_path}")
        return
    
    print(f"📁 配置文件路径：{config_file_path}")
    
    # 查看配置文件内容
    with open(config_file_path, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    print(f"📝 配置文件包含 {len(config_data)} 个模型配置：")
    for i, config in enumerate(config_data[:3], 1):  # 只显示前3个
        print(f"   {i}. {config['config_name']} ({config['model_type']})")
    
    # 方式2A：直接传入文件路径
    print("\n🎯 方式2A：直接传入文件路径")
    try:
        agentscope.init(
            model_configs=config_file_path,  # 直接传入文件路径
            project="配置文件演示",
        )
        
        # 使用第一个配置
        first_config_name = config_data[0]['config_name']
        print(f"🤖 使用配置：{first_config_name}")
        
        agent = DialogAgent(
            name="配置文件助手",
            model_config_name=first_config_name,
            sys_prompt=f"你是使用配置文件中 {first_config_name} 配置的助手"
        )
        
        # 测试对话
        msg = Msg("user", "你的配置是从哪里加载的？", "user")
        response = agent(msg)
        print(f"🤖 回复：{response.content}")
        print("✅ 配置文件方式演示完成")
        
    except Exception as e:
        print(f"❌ 配置文件加载失败：{e}")

def demo_manual_json_loading():
    """方式3：手动加载JSON文件"""
    print("\n🔧 方式3：手动加载JSON并传入")
    print("=" * 50)
    
    config_file_path = "cursor/configs/model_configs.json"
    
    if not os.path.exists(config_file_path):
        print(f"❌ 配置文件不存在：{config_file_path}")
        return
    
    # 手动读取JSON文件
    with open(config_file_path, 'r', encoding='utf-8') as f:
        loaded_configs = json.load(f)
    
    print(f"📁 手动加载配置文件：{config_file_path}")
    print(f"📝 加载了 {len(loaded_configs)} 个配置")
    
    # 传入加载的配置
    agentscope.init(
        model_configs=loaded_configs,  # 传入加载的配置列表
        project="手动加载演示",
    )
    
    # 展示所有可用配置
    print("🎯 可用的模型配置：")
    for config in loaded_configs:
        print(f"   - {config['config_name']}: {config.get('model_name', 'N/A')}")
    
    print("✅ 手动加载方式演示完成")

def explain_config_loading_mechanism():
    """解释配置加载机制"""
    print("\n📚 AgentScope 配置加载机制详解")
    print("=" * 60)
    
    print("🔍 AgentScope 支持以下几种配置方式：")
    print()
    print("1️⃣ 硬编码字典：")
    print("   model_configs = [{'config_name': '...', ...}]")
    print("   agentscope.init(model_configs=model_configs)")
    print()
    print("2️⃣ 配置文件路径：")
    print("   agentscope.init(model_configs='path/to/config.json')")
    print()
    print("3️⃣ 手动加载JSON：")
    print("   with open('config.json') as f:")
    print("       configs = json.load(f)")
    print("   agentscope.init(model_configs=configs)")
    print()
    print("🚨 重要说明：")
    print("   - AgentScope 不会自动搜索配置文件")
    print("   - 必须明确指定配置文件路径或配置内容")
    print("   - cursor/configs/model_configs.json 不会被自动发现")
    print("   - 需要在代码中明确引用这个文件路径")
    print()
    print("💡 最佳实践：")
    print("   - 开发阶段：使用硬编码配置（快速测试）")
    print("   - 生产阶段：使用配置文件（便于管理）")
    print("   - 团队协作：使用配置文件（避免硬编码密钥）")

def main():
    """主函数"""
    print("🚀 AgentScope 配置加载方式演示")
    print("=" * 60)
    
    try:
        # 演示硬编码配置
        demo_hardcoded_config()
        
        # 演示配置文件加载
        demo_config_file()
        
        # 演示手动JSON加载
        demo_manual_json_loading()
        
        # 解释机制
        explain_config_loading_mechanism()
        
        print("\n✅ 演示完成！")
        print("💡 现在你了解了 AgentScope 如何读取配置的完整机制")
        
    except Exception as e:
        print(f"❌ 演示过程中发生错误：{e}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的同一模型多智能体示例
展示三种不同的实现方式
"""

import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg


def method1_shared_config():
    """方法1：共享模型配置"""
    print("🔧 方法1：使用共享的模型配置")
    
    # 1. 定义一个共享的模型配置
    model_config = {
        "config_name": "shared_qwen",
        "model_type": "dashscope_chat",
        "model_name": "qwen-max",
        "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",  # 请替换为您的API密钥
        "generate_args": {
            "temperature": 0.7
        }
    }
    
    # 2. 初始化AgentScope
    agentscope.init(model_configs=[model_config])
    
    # 3. 创建多个智能体，都使用同一个模型配置
    teacher = DialogAgent(
        name="老师",
        sys_prompt="你是一位经验丰富的老师，善于解释复杂概念。",
        model_config_name="shared_qwen"
    )
    
    student = DialogAgent(
        name="学生",
        sys_prompt="你是一位好奇的学生，喜欢提问和学习。",
        model_config_name="shared_qwen"
    )
    
    assistant = DialogAgent(
        name="助教",
        sys_prompt="你是一位助教，帮助协调师生互动。",
        model_config_name="shared_qwen"
    )
    
    # 4. 测试对话
    question = "什么是机器学习？"
    
    # 老师回答
    teacher_msg = Msg("user", f"请解释：{question}", "user")
    teacher_response = teacher(teacher_msg)
    print(f"\n👨‍🏫 {teacher.name}: {teacher_response.content[:150]}...")
    
    # 学生提问
    student_msg = Msg("user", f"关于'{question}'，我还想知道它的实际应用有哪些？", "user")
    student_response = student(student_msg)
    print(f"\n🎓 {student.name}: {student_response.content[:150]}...")
    
    # 助教总结
    assistant_msg = Msg("user", "请总结一下机器学习的要点", "user")
    assistant_response = assistant(assistant_msg)
    print(f"\n👨‍💼 {assistant.name}: {assistant_response.content[:150]}...")


def method2_different_temperatures():
    """方法2：同一模型，不同参数"""
    print("\n\n🔧 方法2：同一模型，不同temperature参数")
    
    # 创建多个配置，使用同一模型但不同参数
    model_configs = [
        {
            "config_name": "conservative_qwen",
            "model_type": "dashscope_chat",
            "model_name": "qwen-max",
            "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
            "generate_args": {"temperature": 0.1}  # 保守，更确定性
        },
        {
            "config_name": "balanced_qwen",
            "model_type": "dashscope_chat",
            "model_name": "qwen-max",
            "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
            "generate_args": {"temperature": 0.7}  # 平衡
        },
        {
            "config_name": "creative_qwen",
            "model_type": "dashscope_chat",
            "model_name": "qwen-max",
            "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
            "generate_args": {"temperature": 0.9}  # 创意，更随机
        }
    ]
    
    agentscope.init(model_configs=model_configs)
    
    # 创建不同风格的智能体
    analyst = DialogAgent(
        name="分析师",
        sys_prompt="你是一位严谨的数据分析师，注重准确性和逻辑性。",
        model_config_name="conservative_qwen"
    )
    
    advisor = DialogAgent(
        name="顾问",
        sys_prompt="你是一位平衡的商业顾问，提供实用建议。",
        model_config_name="balanced_qwen"
    )
    
    creator = DialogAgent(
        name="创意师",
        sys_prompt="你是一位富有创意的设计师，思维发散。",
        model_config_name="creative_qwen"
    )
    
    # 测试同一问题的不同回答风格
    question = "如何提升品牌知名度？"
    
    for agent in [analyst, advisor, creator]:
        msg = Msg("user", question, "user")
        response = agent(msg)
        print(f"\n💭 {agent.name}: {response.content[:200]}...")


def method3_role_based_prompts():
    """方法3：基于角色的系统提示"""
    print("\n\n🔧 方法3：同一配置，不同角色提示")
    
    # 单一模型配置
    model_config = {
        "config_name": "role_qwen",
        "model_type": "dashscope_chat",
        "model_name": "qwen-max",
        "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
        "generate_args": {"temperature": 0.7}
    }
    
    agentscope.init(model_configs=[model_config])
    
    # 定义不同的角色提示
    roles = {
        "技术专家": """你是一位资深技术专家。特点：
- 专注技术细节和实现方案
- 用专业术语但保持清晰
- 提供具体的技术建议
- 考虑技术可行性和性能""",
        
        "产品经理": """你是一位产品经理。特点：
- 关注用户需求和商业价值
- 平衡技术和业务目标
- 注重用户体验和市场反馈
- 制定产品策略和路线图""",
        
        "设计师": """你是一位UI/UX设计师。特点：
- 关注用户体验和界面美观
- 考虑可用性和易用性
- 注重视觉设计和交互流程
- 追求创新和用户友好"""
    }
    
    # 创建角色智能体
    agents = {}
    for role_name, prompt in roles.items():
        agents[role_name] = DialogAgent(
            name=role_name,
            sys_prompt=prompt,
            model_config_name="role_qwen"
        )
    
    # 模拟产品讨论
    topic = "设计一个新的移动支付应用"
    print(f"\n📱 讨论主题: {topic}")
    
    for role_name, agent in agents.items():
        msg = Msg("user", f"关于'{topic}'，请从你的专业角度提供建议", "user")
        response = agent(msg)
        print(f"\n🎯 {role_name}的观点:")
        print(f"{response.content[:250]}...")


def interactive_demo():
    """交互式演示"""
    print("\n\n🎮 交互式演示")
    
    # 简单配置
    model_config = {
        "config_name": "demo_qwen",
        "model_type": "dashscope_chat",
        "model_name": "qwen-max",
        "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",
        "generate_args": {"temperature": 0.7}
    }
    
    agentscope.init(model_configs=[model_config])
    
    # 创建几个角色
    agents = {
        "医生": DialogAgent(
            name="医生",
            sys_prompt="你是一位专业医生，提供健康建议。",
            model_config_name="demo_qwen"
        ),
        "律师": DialogAgent(
            name="律师",
            sys_prompt="你是一位专业律师，提供法律建议。",
            model_config_name="demo_qwen"
        ),
        "厨师": DialogAgent(
            name="厨师",
            sys_prompt="你是一位专业厨师，分享烹饪技巧。",
            model_config_name="demo_qwen"
        )
    }
    
    print("可用角色:", list(agents.keys()))
    
    while True:
        role = input("\n选择角色 (或输入 'quit' 退出): ").strip()
        if role.lower() == 'quit':
            break
        
        if role in agents:
            question = input("请输入问题: ").strip()
            if question:
                msg = Msg("user", question, "user")
                response = agents[role](msg)
                print(f"\n💬 {role}: {response.content}")
        else:
            print("❌ 未找到该角色")


def main():
    """主函数"""
    print("🤖 同一模型多智能体示例")
    print("=" * 50)
    
    # 演示三种方法
    method1_shared_config()
    method2_different_temperatures()
    method3_role_based_prompts()
    
    # 交互式演示
    choice = input("\n是否进入交互模式? (y/n): ").lower()
    if choice == 'y':
        interactive_demo()
    
    print("\n✅ 演示完成！")
    print("\n💡 总结:")
    print("1. 方法1：多个智能体共享同一个模型配置")
    print("2. 方法2：同一模型使用不同参数（如temperature）")
    print("3. 方法3：同一配置通过不同系统提示创建不同角色")


if __name__ == "__main__":
    main() 
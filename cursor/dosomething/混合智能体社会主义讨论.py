#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
混合智能体对话示例：美国社会主义化的可行性讨论
使用三个不同的模型进行多角度分析
"""

import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
from agentscope.strategy import MixtureOfAgents
from agentscope import msghub
import time


def setup_models():
    """配置三个不同的模型"""
    model_configs = [
        # 本地ollama模型1 - llama3.2:3b (扮演经济学家)
        {
            "config_name": "llama_economist",
            "model_type": "ollama_chat",
            "model_name": "llama3.2:3b",
            "options": {
                "temperature": 0.7
            },
            "keep_alive": "5m"
        },
        
        # 本地ollama模型2 - deepseek-r1:8b (扮演政治学者)
        {
            "config_name": "deepseek_political",
            "model_type": "ollama_chat", 
            "model_name": "deepseek-r1:8b",
            "options": {
                "temperature": 0.8
            },
            "keep_alive": "5m"
        },
        
        # 阿里云千问模型 (扮演社会学家)
        {
            "config_name": "qwen_sociologist", 
            "model_type": "dashscope_chat",
            "model_name": "qwen-max",
            "api_key": "sk-cc1605a341c4450489bd71ffc28238c0",  # 请替换为您的真实API密钥
            "generate_args": {
                "temperature": 0.6
            }
        }
    ]
    
    return model_configs


def create_agents(model_configs):
    """创建三个不同角色的智能体"""
    
    # 初始化AgentScope
    agentscope.init(
        model_configs=model_configs,
        project="美国社会主义化可行性讨论"
    )
    
    # 经济学家智能体（使用llama3.2:3b）
    economist = DialogAgent(
        name="经济学家",
        sys_prompt="""你是一位资深的经济学家，专门研究经济制度和政策。你需要从经济学角度分析美国社会主义化的可行性。

你的特点：
- 注重数据和实证分析
- 熟悉各种经济制度的优缺点
- 关注经济效率、资源配置和市场机制
- 会引用历史经济数据和案例
- 客观理性，避免意识形态偏见

请用专业的经济学术语和理论分析问题，但保持表达通俗易懂。每次回答控制在200字以内。""",
        model_config_name="llama_economist"
    )
    
    # 政治学者智能体（使用qwen3:8b）
    political_scientist = DialogAgent(
        name="政治学者", 
        sys_prompt="""你是一位政治学教授，专门研究政治制度、民主理论和政府治理。你需要从政治学角度分析美国社会主义化的可行性。

你的特点：
- 深入了解美国政治体制和历史
- 熟悉各种政治理论和制度设计
- 关注政治可行性、制度变迁和权力结构
- 会分析政治动力学和利益集团影响
- 严谨客观，基于学术研究

请从政治制度角度分析，关注实施的政治障碍和可能路径。每次回答控制在200字以内。""",
        model_config_name="deepseek_political"
    )
    
    # 社会学家智能体（使用阿里云千问）
    sociologist = DialogAgent(
        name="社会学家",
        sys_prompt="""你是一位社会学教授，专门研究社会结构、文化变迁和社会运动。你需要从社会学角度分析美国社会主义化的可行性。

你的特点：
- 关注社会结构、阶级关系和文化因素
- 熟悉社会变迁理论和社会运动
- 分析社会心理、价值观念和集体行为
- 重视社会公平、社会凝聚力和文化适应性
- 注重实地调研和社会现象观察

请从社会文化角度分析，关注社会接受度和文化兼容性。每次回答控制在200字以内。""",
        model_config_name="qwen_sociologist"
    )
    
    return economist, political_scientist, sociologist


def run_discussion():
    """运行混合智能体讨论"""
    
    print("🎯 混合智能体对话：美国社会主义化的可行性")
    print("="*60)
    print("参与者：")
    print("🏛️ 经济学家 (llama3.2:3b)")
    print("🗳️ 政治学者 (qwen3:8b)")  
    print("👥 社会学家 (阿里云千问)")
    print("="*60)
    
    # 设置模型配置
    model_configs = setup_models()
    
    # 创建智能体
    economist, political_scientist, sociologist = create_agents(model_configs)
    
    # 讨论主题和问题
    topics = [
        "美国实施社会主义政策的经济可行性如何？需要考虑哪些经济因素？",
        "从政治制度角度看，美国推行社会主义化面临哪些主要障碍？",
        "美国社会文化对社会主义理念的接受度如何？什么因素影响社会认同？",
        "如果要在美国推进社会主义化，应该采取什么样的渐进策略？"
    ]
    
    # 开始讨论
    for i, topic in enumerate(topics, 1):
        print(f"\n📍 讨论话题 {i}: {topic}")
        print("-"*50)
        
        # 每个话题让三个智能体轮流发言
        msg = Msg("user", topic, "user")
        
        # 经济学家先发言
        print(f"\n💼 {economist.name}的观点:")
        economist_response = economist(msg)
        print(f"{economist_response.content}")
        
        time.sleep(1)  # 避免请求过快
        
        # 政治学者发言
        print(f"\n🏛️ {political_scientist.name}的观点:")
        political_response = political_scientist(msg)
        print(f"{political_response.content}")
        
        time.sleep(1)
        
        # 社会学家发言
        print(f"\n👥 {sociologist.name}的观点:")
        sociology_response = sociologist(msg)
        print(f"{sociology_response.content}")
        
        time.sleep(2)  # 话题间间隔
    
    print(f"\n{'='*60}")
    print("🎯 讨论总结")
    print("="*60)
    
    # 让三个智能体进行最终总结
    summary_prompt = """基于前面的讨论，请从你的专业角度对"美国社会主义化的可行性"给出一个简洁的总结性观点，包括主要机遇和挑战。控制在150字以内。"""
    
    summary_msg = Msg("user", summary_prompt, "user")
    
    print(f"\n💼 {economist.name}总结:")
    economist_summary = economist(summary_msg)
    print(f"{economist_summary.content}")
    
    time.sleep(1)
    
    print(f"\n🏛️ {political_scientist.name}总结:")
    political_summary = political_scientist(summary_msg)
    print(f"{political_summary.content}")
    
    time.sleep(1)
    
    print(f"\n👥 {sociologist.name}总结:")
    sociology_summary = sociologist(summary_msg)
    print(f"{sociology_summary.content}")
    
    print(f"\n{'='*60}")
    print("✅ 混合智能体讨论完成！")
    print("💡 本次讨论展示了如何使用不同模型（本地ollama + 云端API）")
    print("   从多个学科角度分析复杂的社会政治经济问题。")


def run_moa_analysis():
    """使用MoA(Mixture of Agents)进行深度分析"""
    
    print(f"\n{'='*60}")
    print("🤖 MoA 深度分析：美国社会主义化综合评估")
    print("="*60)
    
    # 设置模型配置
    model_configs = setup_models()
    agentscope.init(model_configs=model_configs, project="MoA分析")
    
    # 创建MoA实例，使用所有三个模型
    moa_module = MixtureOfAgents(
        main_model="qwen_sociologist",  # 使用阿里云千问作为主模型
        reference_models=["llama_economist", "deepseek_political", "qwen_sociologist"],
        show_internal=True,  # 显示内部推理过程
        rounds=1  # 使用1轮推理
    )
    
    # 创建使用MoA的智能体
    from agentscope.agents import AgentBase
    
    class MoAAnalyst(AgentBase):
        def __init__(self, moa_module):
            super().__init__(
                name="综合分析师",
                sys_prompt="你是一位综合分析师，需要整合经济学、政治学、社会学多个角度的观点。"
            )
            self.moa_module = moa_module
        
        def reply(self, x):
            response = self.moa_module(
                Msg("system", self.sys_prompt, role="system"),
                x
            )
            msg = Msg(self.name, response, role="assistant")
            self.speak(msg)
            return msg
    
    moa_analyst = MoAAnalyst(moa_module)
    
    # 进行综合分析
    analysis_question = """
请从经济学、政治学、社会学三个角度综合分析美国社会主义化的可行性：

1. 经济层面：评估实施社会主义政策对美国经济的潜在影响
2. 政治层面：分析美国政治体制下推行社会主义政策的现实障碍  
3. 社会层面：评估美国社会文化对社会主义理念的接受程度

请提供一个平衡、客观的综合评估，包括可行性评分（1-10分）和具体建议。
"""
    
    print("🔍 正在进行MoA综合分析...")
    msg = Msg("user", analysis_question, "user")
    result = moa_analyst(msg)
    
    print(f"\n📊 MoA综合分析结果:")
    print(f"{result.content}")


if __name__ == "__main__":
    try:
        # 运行多智能体讨论
        run_discussion()
        
        # 询问是否进行MoA分析
        print(f"\n{'='*60}")
        choice = input("是否进行MoA(Mixture of Agents)深度分析？(y/n): ").lower()
        if choice == 'y':
            run_moa_analysis()
        
        print("\n🎉 程序运行完成！")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ 程序被用户中断")
    except Exception as e:
        print(f"\n❌ 运行出错: {e}")
        print("请检查：")
        print("1. ollama服务是否正常运行")
        print("2. 阿里云API密钥是否正确")
        print("3. 网络连接是否正常") 
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用同一个大模型创建多智能体示例
展示如何用同一个DashScope模型创建不同角色的智能体
"""

import asyncio
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
from typing import List


class SameModelMultiAgents:
    """使用同一模型的多智能体系统"""
    
    def __init__(self, api_key: str, model_name: str = "qwen-max"):
        """
        初始化多智能体系统
        
        Args:
            api_key: DashScope API密钥
            model_name: 模型名称，默认qwen-max
        """
        self.api_key = api_key
        self.model_name = model_name
        self.agents = {}
        self._initialize_model()
        self._create_agents()
    
    def _initialize_model(self):
        """初始化模型配置"""
        # 使用同一个模型配置
        model_config = {
            "config_name": "shared_qwen",
            "model_type": "dashscope_chat",
            "model_name": self.model_name,
            "api_key": self.api_key,
            "generate_args": {
                "temperature": 0.7,
                "max_tokens": 2000
            }
        }
        
        # 初始化AgentScope
        agentscope.init(
            model_configs=[model_config],
            project="SameModelMultiAgents"
        )
    
    def _create_agents(self):
        """创建不同角色的智能体"""
        
        # 1. 技术专家
        self.agents["tech_expert"] = DialogAgent(
            name="技术专家",
            sys_prompt="""你是一位资深的技术专家，专门负责技术问题的分析和解答。
你的特点：
- 逻辑严谨，思维清晰
- 善于用简洁的语言解释复杂的技术概念
- 会提供具体的代码示例和最佳实践
- 关注技术的实用性和可行性
请用专业但易懂的方式回答技术问题。""",
            model_config_name="shared_qwen"
        )
        
        # 2. 产品经理
        self.agents["product_manager"] = DialogAgent(
            name="产品经理",
            sys_prompt="""你是一位经验丰富的产品经理，专门负责产品规划和用户需求分析。
你的特点：
- 以用户为中心，关注用户体验
- 善于平衡技术可行性和商业价值
- 能够将复杂的需求转化为清晰的产品方案
- 注重数据驱动的决策
请从产品角度分析问题，提供实用的产品建议。""",
            model_config_name="shared_qwen"
        )
        
        # 3. 创意设计师
        self.agents["creative_designer"] = DialogAgent(
            name="创意设计师",
            sys_prompt="""你是一位富有创意的设计师，专门负责创意构思和设计方案。
你的特点：
- 思维发散，富有想象力
- 关注美学和用户体验
- 善于将抽象概念可视化
- 追求创新和独特性
请用创意的角度思考问题，提供有趣且实用的设计建议。""",
            model_config_name="shared_qwen"
        )
        
        # 4. 商业分析师
        self.agents["business_analyst"] = DialogAgent(
            name="商业分析师",
            sys_prompt="""你是一位专业的商业分析师，专门负责商业模式和市场分析。
你的特点：
- 数据驱动，逻辑严密
- 关注商业价值和盈利模式
- 善于市场趋势分析和竞争分析
- 注重风险评估和投资回报
请从商业角度分析问题，提供有价值的商业洞察。""",
            model_config_name="shared_qwen"
        )
        
        # 5. 用户体验专家
        self.agents["ux_expert"] = DialogAgent(
            name="用户体验专家",
            sys_prompt="""你是一位用户体验专家，专门负责用户研究和体验优化。
你的特点：
- 以用户为中心，关注用户感受
- 善于用户行为分析和用户旅程设计
- 注重可用性和易用性
- 关注无障碍设计和包容性
请从用户体验角度分析问题，提供改善用户体验的建议。""",
            model_config_name="shared_qwen"
        )
    
    def get_agent(self, role: str) -> DialogAgent:
        """获取指定角色的智能体"""
        return self.agents.get(role)
    
    def list_agents(self) -> List[str]:
        """列出所有可用的智能体角色"""
        return list(self.agents.keys())
    
    async def single_agent_response(self, role: str, query: str) -> str:
        """获取单个智能体的回答"""
        agent = self.get_agent(role)
        if not agent:
            return f"未找到角色为 {role} 的智能体"
        
        msg = Msg("user", query, "user")
        response = agent(msg)
        return response.content
    
    async def multi_agent_discussion(self, topic: str, participants: List[str] = None) -> dict:
        """多智能体讨论"""
        if participants is None:
            participants = list(self.agents.keys())
        
        print(f"🎯 讨论主题: {topic}")
        print(f"👥 参与者: {[self.agents[role].name for role in participants]}")
        print("=" * 50)
        
        responses = {}
        
        for role in participants:
            agent = self.agents[role]
            
            # 构建讨论提示
            discussion_prompt = f"""
讨论主题：{topic}

请从你的专业角度分析这个主题，并提供你的观点和建议。
请保持你的角色特色，给出有价值的专业见解。
"""
            
            msg = Msg("user", discussion_prompt, "user")
            response = agent(msg)
            responses[role] = {
                "agent_name": agent.name,
                "response": response.content
            }
            
            print(f"\n💬 {agent.name}:")
            print(f"{response.content}")
            print("-" * 30)
        
        return responses
    
    async def collaborative_problem_solving(self, problem: str) -> dict:
        """协作解决问题"""
        print(f"🔍 问题: {problem}")
        print("🤝 开始协作解决...")
        print("=" * 50)
        
        # 第一轮：各自分析
        print("\n📋 第一轮：各角色独立分析")
        first_round = {}
        
        for role, agent in self.agents.items():
            analysis_prompt = f"""
问题：{problem}

请从你的专业角度分析这个问题：
1. 问题的核心是什么？
2. 你认为的关键挑战是什么？
3. 你有什么初步的解决思路？

请保持简洁，重点突出你的专业视角。
"""
            msg = Msg("user", analysis_prompt, "user")
            response = agent(msg)
            first_round[role] = response.content
            
            print(f"\n🔸 {agent.name}的分析:")
            print(f"{response.content[:200]}...")
        
        # 第二轮：综合讨论
        print(f"\n\n🔄 第二轮：综合讨论和方案制定")
        
        # 汇总所有观点
        all_perspectives = "\n\n".join([
            f"{self.agents[role].name}的观点：\n{analysis}"
            for role, analysis in first_round.items()
        ])
        
        # 让产品经理综合所有观点
        pm_agent = self.agents["product_manager"]
        synthesis_prompt = f"""
问题：{problem}

以下是团队各成员的分析：
{all_perspectives}

作为产品经理，请综合所有观点，制定一个完整的解决方案：
1. 问题总结
2. 解决方案
3. 实施步骤
4. 风险评估
5. 成功指标

请提供一个平衡各方观点的综合方案。
"""
        
        msg = Msg("user", synthesis_prompt, "user")
        final_solution = pm_agent(msg)
        
        print(f"\n✅ 最终解决方案 (by {pm_agent.name}):")
        print(f"{final_solution.content}")
        
        return {
            "problem": problem,
            "individual_analyses": first_round,
            "final_solution": final_solution.content
        }


async def demo_same_model_agents():
    """演示使用同一模型的多智能体"""
    
    # 请替换为您的真实API密钥
    api_key = "sk-cc1605a341c4450489bd71ffc28238c0"
    
    # 创建多智能体系统
    multi_agents = SameModelMultiAgents(api_key)
    
    print("🚀 同一模型多智能体系统演示")
    print("=" * 50)
    print(f"📊 已创建 {len(multi_agents.list_agents())} 个智能体:")
    for role in multi_agents.list_agents():
        agent = multi_agents.get_agent(role)
        print(f"  - {agent.name} ({role})")
    
    print("\n" + "="*50)
    
    # 演示1：单个智能体回答
    print("\n🎯 演示1：不同角色对同一问题的回答")
    query = "如何提高团队的工作效率？"
    print(f"问题: {query}")
    print("-" * 30)
    
    for role in ["tech_expert", "product_manager", "ux_expert"]:
        response = await multi_agents.single_agent_response(role, query)
        agent_name = multi_agents.get_agent(role).name
        print(f"\n💬 {agent_name}:")
        print(f"{response[:300]}...")
    
    print("\n" + "="*50)
    
    # 演示2：多智能体讨论
    print("\n🎯 演示2：多智能体讨论")
    await multi_agents.multi_agent_discussion(
        "如何设计一个成功的移动应用",
        ["product_manager", "creative_designer", "tech_expert"]
    )
    
    print("\n" + "="*50)
    
    # 演示3：协作解决问题
    print("\n🎯 演示3：协作解决复杂问题")
    await multi_agents.collaborative_problem_solving(
        "公司需要开发一个新的在线教育平台，如何确保项目成功？"
    )


async def interactive_mode():
    """交互模式"""
    api_key = input("请输入您的DashScope API密钥: ").strip()
    if not api_key:
        print("❌ 未提供API密钥")
        return
    
    multi_agents = SameModelMultiAgents(api_key)
    
    print("\n🎮 进入交互模式")
    print("可用命令:")
    print("  1. ask <角色> <问题> - 向指定角色提问")
    print("  2. discuss <主题> - 多智能体讨论")
    print("  3. solve <问题> - 协作解决问题")
    print("  4. list - 列出所有角色")
    print("  5. quit - 退出")
    
    while True:
        command = input("\n请输入命令: ").strip()
        
        if command.lower() == 'quit':
            break
        elif command.lower() == 'list':
            print("可用角色:")
            for role in multi_agents.list_agents():
                agent = multi_agents.get_agent(role)
                print(f"  - {role}: {agent.name}")
        elif command.startswith('ask '):
            parts = command.split(' ', 2)
            if len(parts) >= 3:
                role, question = parts[1], parts[2]
                if role in multi_agents.list_agents():
                    response = await multi_agents.single_agent_response(role, question)
                    agent_name = multi_agents.get_agent(role).name
                    print(f"\n💬 {agent_name}:")
                    print(response)
                else:
                    print(f"❌ 未找到角色: {role}")
            else:
                print("❌ 格式错误，请使用: ask <角色> <问题>")
        elif command.startswith('discuss '):
            topic = command[8:].strip()
            if topic:
                await multi_agents.multi_agent_discussion(topic)
            else:
                print("❌ 请提供讨论主题")
        elif command.startswith('solve '):
            problem = command[6:].strip()
            if problem:
                await multi_agents.collaborative_problem_solving(problem)
            else:
                print("❌ 请提供要解决的问题")
        else:
            print("❌ 未知命令，请输入 'help' 查看帮助")


async def main():
    """主函数"""
    print("🎯 选择模式:")
    print("1. 演示模式 - 自动演示各种功能")
    print("2. 交互模式 - 手动测试")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        await demo_same_model_agents()
    elif choice == "2":
        await interactive_mode()
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    print("🤖 使用同一模型创建多智能体系统")
    print("=" * 50)
    print("💡 本示例展示如何用一个DashScope模型创建多个不同角色的智能体")
    print("⚠️  请确保已安装AgentScope并配置了正确的API密钥")
    print("=" * 50)
    
    asyncio.run(main()) 
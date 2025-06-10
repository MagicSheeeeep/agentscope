#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多大模型编排系统
实现多种模型编排策略，包括并行处理、串行处理、投票机制、专家路由等
"""

import asyncio
import concurrent.futures
import json
import time
from typing import List, Dict, Any, Union, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import statistics

import agentscope
from agentscope.agents import DialogAgent, ReActAgentV2
from agentscope.message import Msg
from agentscope.strategy import MixtureOfAgents
from agentscope.models import ModelWrapperBase
from agentscope.manager import ModelManager
from agentscope.pipelines import sequential_pipeline


class OrchestrationStrategy(Enum):
    """编排策略枚举"""
    PARALLEL = "parallel"           # 并行处理
    SEQUENTIAL = "sequential"       # 串行处理
    VOTING = "voting"              # 投票机制
    EXPERT_ROUTING = "expert_routing"  # 专家路由
    MIXTURE_OF_AGENTS = "moa"      # 智能体混合
    HIERARCHICAL = "hierarchical"   # 分层处理
    PIPELINE = "pipeline"          # 流水线处理


@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    config_name: str
    model_type: str
    model_name: str
    api_key: str
    specialty: Optional[str] = None  # 专业领域
    weight: float = 1.0             # 权重
    temperature: float = 0.7
    max_tokens: Optional[int] = None


@dataclass
class OrchestrationResult:
    """编排结果"""
    final_result: str
    individual_results: List[Dict[str, Any]]
    strategy_used: str
    execution_time: float
    metadata: Dict[str, Any]


class MultiModelOrchestrator:
    """多模型编排器"""
    
    def __init__(self, model_configs: List[ModelConfig]):
        """
        初始化多模型编排器
        
        Args:
            model_configs: 模型配置列表
        """
        self.model_configs = model_configs
        self.models = {}
        self.agents = {}
        self._initialize_models()
        self._initialize_agents()
    
    def _initialize_models(self):
        """初始化模型"""
        # 准备AgentScope模型配置
        agentscope_configs = []
        for config in self.model_configs:
            agentscope_config = {
                "config_name": config.config_name,
                "model_type": config.model_type,
                "model_name": config.model_name,
                "api_key": config.api_key,
                "generate_args": {
                    "temperature": config.temperature
                }
            }
            if config.max_tokens:
                agentscope_config["generate_args"]["max_tokens"] = config.max_tokens
            
            agentscope_configs.append(agentscope_config)
        
        # 初始化AgentScope
        agentscope.init(
            model_configs=agentscope_configs,
            project="MultiModelOrchestration"
        )
        
        # 获取模型实例
        model_manager = ModelManager.get_instance()
        for config in self.model_configs:
            self.models[config.name] = model_manager.get_model_by_config_name(
                config.config_name
            )
    
    def _initialize_agents(self):
        """初始化智能体"""
        for config in self.model_configs:
            # 根据专业领域设置系统提示
            if config.specialty:
                sys_prompt = f"你是一个专门处理{config.specialty}问题的AI助手。请根据你的专业知识提供准确、详细的回答。"
            else:
                sys_prompt = "你是一个通用AI助手，请提供准确、有用的回答。"
            
            self.agents[config.name] = DialogAgent(
                name=config.name,
                sys_prompt=sys_prompt,
                model_config_name=config.config_name
            )
    
    async def orchestrate(
        self,
        query: str,
        strategy: OrchestrationStrategy,
        **kwargs
    ) -> OrchestrationResult:
        """
        执行多模型编排
        
        Args:
            query: 查询内容
            strategy: 编排策略
            **kwargs: 额外参数
            
        Returns:
            编排结果
        """
        start_time = time.time()
        
        if strategy == OrchestrationStrategy.PARALLEL:
            result = await self._parallel_processing(query, **kwargs)
        elif strategy == OrchestrationStrategy.SEQUENTIAL:
            result = await self._sequential_processing(query, **kwargs)
        elif strategy == OrchestrationStrategy.VOTING:
            result = await self._voting_mechanism(query, **kwargs)
        elif strategy == OrchestrationStrategy.EXPERT_ROUTING:
            result = await self._expert_routing(query, **kwargs)
        elif strategy == OrchestrationStrategy.MIXTURE_OF_AGENTS:
            result = await self._mixture_of_agents(query, **kwargs)
        elif strategy == OrchestrationStrategy.HIERARCHICAL:
            result = await self._hierarchical_processing(query, **kwargs)
        elif strategy == OrchestrationStrategy.PIPELINE:
            result = await self._pipeline_processing(query, **kwargs)
        else:
            raise ValueError(f"不支持的编排策略: {strategy}")
        
        execution_time = time.time() - start_time
        
        return OrchestrationResult(
            final_result=result["final_result"],
            individual_results=result["individual_results"],
            strategy_used=strategy.value,
            execution_time=execution_time,
            metadata=result.get("metadata", {})
        )
    
    async def _parallel_processing(self, query: str, **kwargs) -> Dict[str, Any]:
        """并行处理策略"""
        print(f"🔄 使用并行处理策略处理查询: {query}")
        
        async def process_model(config: ModelConfig) -> Dict[str, Any]:
            agent = self.agents[config.name]
            msg = Msg("user", query, "user")
            response = agent(msg)
            return {
                "model": config.name,
                "response": response.content,
                "specialty": config.specialty,
                "weight": config.weight
            }
        
        # 并行执行所有模型
        tasks = [process_model(config) for config in self.model_configs]
        individual_results = await asyncio.gather(*tasks)
        
        # 简单聚合：加权平均或选择最佳
        aggregation_method = kwargs.get("aggregation", "weighted_selection")
        
        if aggregation_method == "weighted_selection":
            # 选择权重最高的结果
            best_result = max(individual_results, key=lambda x: x["weight"])
            final_result = best_result["response"]
        else:
            # 简单拼接所有结果
            final_result = "\n\n".join([
                f"【{result['model']}】: {result['response']}"
                for result in individual_results
            ])
        
        return {
            "final_result": final_result,
            "individual_results": individual_results,
            "metadata": {"aggregation_method": aggregation_method}
        }
    
    async def _sequential_processing(self, query: str, **kwargs) -> Dict[str, Any]:
        """串行处理策略"""
        print(f"🔗 使用串行处理策略处理查询: {query}")
        
        individual_results = []
        current_query = query
        
        for config in self.model_configs:
            agent = self.agents[config.name]
            msg = Msg("user", current_query, "user")
            response = agent(msg)
            
            result = {
                "model": config.name,
                "input": current_query,
                "response": response.content,
                "specialty": config.specialty
            }
            individual_results.append(result)
            
            # 下一个模型的输入是前一个模型的输出
            refinement_prompt = kwargs.get("refinement_prompt", 
                "请基于以下内容进一步完善和扩展回答：\n{previous_response}\n\n原始问题：{original_query}")
            current_query = refinement_prompt.format(
                previous_response=response.content,
                original_query=query
            )
        
        # 最后一个模型的输出作为最终结果
        final_result = individual_results[-1]["response"]
        
        return {
            "final_result": final_result,
            "individual_results": individual_results,
            "metadata": {"processing_order": [r["model"] for r in individual_results]}
        }
    
    async def _voting_mechanism(self, query: str, **kwargs) -> Dict[str, Any]:
        """投票机制策略"""
        print(f"🗳️ 使用投票机制策略处理查询: {query}")
        
        # 首先并行获取所有模型的回答
        parallel_result = await self._parallel_processing(query, **kwargs)
        individual_results = parallel_result["individual_results"]
        
        # 创建一个评判智能体
        judge_config = kwargs.get("judge_model", self.model_configs[0].config_name)
        judge_agent = DialogAgent(
            name="Judge",
            sys_prompt="你是一个公正的评判者。请评估以下回答的质量，并选择最佳答案。评估标准包括准确性、完整性、清晰度和实用性。",
            model_config_name=judge_config
        )
        
        # 构建评判提示
        responses_text = "\n\n".join([
            f"回答{i+1}（来自{result['model']}）：\n{result['response']}"
            for i, result in enumerate(individual_results)
        ])
        
        judge_prompt = f"""
原始问题：{query}

以下是不同AI模型的回答：
{responses_text}

请评估这些回答，并选择最佳的一个。请说明你的选择理由，并可以对最佳答案进行适当的改进。

请按以下格式回答：
最佳答案编号：[编号]
选择理由：[理由]
改进后的答案：[改进的答案]
"""
        
        judge_msg = Msg("user", judge_prompt, "user")
        judge_response = judge_agent(judge_msg)
        
        return {
            "final_result": judge_response.content,
            "individual_results": individual_results,
            "metadata": {
                "voting_method": "expert_judge",
                "judge_model": judge_config
            }
        }
    
    async def _expert_routing(self, query: str, **kwargs) -> Dict[str, Any]:
        """专家路由策略"""
        print(f"🎯 使用专家路由策略处理查询: {query}")
        
        # 创建路由智能体
        router_config = kwargs.get("router_model", self.model_configs[0].config_name)
        router_agent = DialogAgent(
            name="Router",
            sys_prompt="你是一个智能路由器。根据用户问题的类型，选择最适合的专家来回答。",
            model_config_name=router_config
        )
        
        # 构建专家列表
        experts_info = "\n".join([
            f"- {config.name}: 专长于{config.specialty or '通用问题'}"
            for config in self.model_configs
        ])
        
        routing_prompt = f"""
用户问题：{query}

可用专家：
{experts_info}

请选择最适合回答这个问题的专家，并说明选择理由。
请只回答专家的名称，格式：专家名称: [名称]
"""
        
        routing_msg = Msg("user", routing_prompt, "user")
        routing_response = router_agent(routing_msg)
        
        # 解析路由结果
        selected_expert = None
        for config in self.model_configs:
            if config.name in routing_response.content:
                selected_expert = config.name
                break
        
        if not selected_expert:
            selected_expert = self.model_configs[0].name  # 默认选择第一个
        
        # 使用选定的专家处理问题
        expert_agent = self.agents[selected_expert]
        expert_msg = Msg("user", query, "user")
        expert_response = expert_agent(expert_msg)
        
        return {
            "final_result": expert_response.content,
            "individual_results": [{
                "model": selected_expert,
                "response": expert_response.content,
                "routing_reason": routing_response.content
            }],
            "metadata": {
                "selected_expert": selected_expert,
                "routing_decision": routing_response.content
            }
        }
    
    async def _mixture_of_agents(self, query: str, **kwargs) -> Dict[str, Any]:
        """智能体混合策略（MoA）"""
        print(f"🤖 使用智能体混合策略处理查询: {query}")
        
        # 选择主模型和参考模型
        main_model = kwargs.get("main_model", self.model_configs[0].config_name)
        reference_models = kwargs.get("reference_models", 
                                    [config.config_name for config in self.model_configs])
        
        # 创建MoA实例
        moa = MixtureOfAgents(
            main_model=main_model,
            reference_models=reference_models,
            rounds=kwargs.get("rounds", 1),
            show_internal=kwargs.get("show_internal", True)
        )
        
        # 处理查询
        msg = Msg("user", query, "user")
        result = moa(msg)
        
        return {
            "final_result": result,
            "individual_results": [{
                "model": "MixtureOfAgents",
                "response": result,
                "main_model": main_model,
                "reference_models": reference_models
            }],
            "metadata": {
                "main_model": main_model,
                "reference_models": reference_models,
                "rounds": kwargs.get("rounds", 1)
            }
        }
    
    async def _hierarchical_processing(self, query: str, **kwargs) -> Dict[str, Any]:
        """分层处理策略"""
        print(f"🏗️ 使用分层处理策略处理查询: {query}")
        
        # 第一层：问题分解
        decomposer_agent = DialogAgent(
            name="Decomposer",
            sys_prompt="你是一个问题分解专家。请将复杂问题分解为几个子问题，每个子问题应该清晰、具体。",
            model_config_name=self.model_configs[0].config_name
        )
        
        decompose_prompt = f"""
请将以下问题分解为3-5个子问题：
{query}

请按以下格式输出：
子问题1：[问题]
子问题2：[问题]
子问题3：[问题]
...
"""
        
        decompose_msg = Msg("user", decompose_prompt, "user")
        decompose_response = decomposer_agent(decompose_msg)
        
        # 解析子问题
        sub_questions = []
        for line in decompose_response.content.split('\n'):
            if '子问题' in line and '：' in line:
                sub_question = line.split('：', 1)[1].strip()
                if sub_question:
                    sub_questions.append(sub_question)
        
        # 第二层：并行处理子问题
        sub_results = []
        for i, sub_question in enumerate(sub_questions):
            if i < len(self.model_configs):
                agent = self.agents[self.model_configs[i].name]
                msg = Msg("user", sub_question, "user")
                response = agent(msg)
                sub_results.append({
                    "sub_question": sub_question,
                    "model": self.model_configs[i].name,
                    "response": response.content
                })
        
        # 第三层：结果整合
        synthesizer_agent = DialogAgent(
            name="Synthesizer",
            sys_prompt="你是一个信息整合专家。请将各个子问题的答案整合成一个完整、连贯的回答。",
            model_config_name=self.model_configs[-1].config_name
        )
        
        synthesis_content = f"原始问题：{query}\n\n"
        for result in sub_results:
            synthesis_content += f"子问题：{result['sub_question']}\n回答：{result['response']}\n\n"
        
        synthesis_content += "请基于以上信息，为原始问题提供一个完整、连贯的答案。"
        
        synthesis_msg = Msg("user", synthesis_content, "user")
        synthesis_response = synthesizer_agent(synthesis_msg)
        
        return {
            "final_result": synthesis_response.content,
            "individual_results": sub_results + [{
                "model": "Synthesizer",
                "response": synthesis_response.content,
                "type": "synthesis"
            }],
            "metadata": {
                "sub_questions": sub_questions,
                "decomposition": decompose_response.content
            }
        }
    
    async def _pipeline_processing(self, query: str, **kwargs) -> Dict[str, Any]:
        """流水线处理策略"""
        print(f"⚡ 使用流水线处理策略处理查询: {query}")
        
        # 定义流水线阶段
        stages = kwargs.get("stages", [
            {"name": "分析", "prompt": "请分析这个问题的核心要点：{query}"},
            {"name": "研究", "prompt": "基于以下分析，请深入研究相关信息：\n{previous_output}\n\n原问题：{query}"},
            {"name": "总结", "prompt": "请基于以下研究结果，提供最终答案：\n{previous_output}\n\n原问题：{query}"}
        ])
        
        individual_results = []
        current_output = query
        
        for i, stage in enumerate(stages):
            if i < len(self.model_configs):
                agent = self.agents[self.model_configs[i].name]
                
                # 构建当前阶段的提示
                stage_prompt = stage["prompt"].format(
                    query=query,
                    previous_output=current_output
                )
                
                msg = Msg("user", stage_prompt, "user")
                response = agent(msg)
                
                result = {
                    "stage": stage["name"],
                    "model": self.model_configs[i].name,
                    "input": stage_prompt,
                    "response": response.content
                }
                individual_results.append(result)
                
                current_output = response.content
        
        return {
            "final_result": current_output,
            "individual_results": individual_results,
            "metadata": {
                "stages": [stage["name"] for stage in stages],
                "pipeline_length": len(stages)
            }
        }


class MultiModelApplication:
    """多模型应用示例"""
    
    def __init__(self):
        """初始化应用"""
        # 配置多个不同的模型
        self.model_configs = [
            ModelConfig(
                name="通用助手",
                config_name="general_assistant",
                model_type="dashscope_chat",
                model_name="qwen-max",
                api_key="your_dashscope_api_key",
                specialty="通用问题",
                weight=1.0,
                temperature=0.7
            ),
            ModelConfig(
                name="技术专家",
                config_name="tech_expert",
                model_type="dashscope_chat", 
                model_name="qwen-turbo",
                api_key="your_dashscope_api_key",
                specialty="技术和编程",
                weight=1.2,
                temperature=0.5
            ),
            ModelConfig(
                name="创意助手",
                config_name="creative_assistant",
                model_type="dashscope_chat",
                model_name="qwen-plus",
                api_key="your_dashscope_api_key",
                specialty="创意和写作",
                weight=0.9,
                temperature=0.9
            )
        ]
        
        self.orchestrator = MultiModelOrchestrator(self.model_configs)
    
    async def run_demo(self):
        """运行演示"""
        print("🚀 多大模型编排系统演示")
        print("=" * 50)
        
        # 测试查询
        test_queries = [
            "请解释什么是人工智能，并分析其发展趋势",
            "如何用Python实现一个简单的机器学习模型？",
            "写一首关于春天的诗"
        ]
        
        strategies = [
            OrchestrationStrategy.PARALLEL,
            OrchestrationStrategy.VOTING,
            OrchestrationStrategy.EXPERT_ROUTING,
            OrchestrationStrategy.HIERARCHICAL
        ]
        
        for query in test_queries:
            print(f"\n📝 测试查询: {query}")
            print("-" * 30)
            
            for strategy in strategies:
                try:
                    result = await self.orchestrator.orchestrate(query, strategy)
                    
                    print(f"\n🎯 策略: {strategy.value}")
                    print(f"⏱️ 执行时间: {result.execution_time:.2f}秒")
                    print(f"📊 参与模型数: {len(result.individual_results)}")
                    print(f"📋 最终结果: {result.final_result[:200]}...")
                    
                except Exception as e:
                    print(f"❌ 策略 {strategy.value} 执行失败: {str(e)}")
            
            print("\n" + "="*50)
    
    async def interactive_mode(self):
        """交互模式"""
        print("🎮 进入交互模式")
        print("输入 'quit' 退出，输入 'help' 查看帮助")
        
        while True:
            query = input("\n请输入您的问题: ").strip()
            
            if query.lower() == 'quit':
                break
            elif query.lower() == 'help':
                self._show_help()
                continue
            elif not query:
                continue
            
            # 选择策略
            print("\n请选择编排策略:")
            for i, strategy in enumerate(OrchestrationStrategy, 1):
                print(f"{i}. {strategy.value}")
            
            try:
                choice = int(input("请输入策略编号 (1-7): ")) - 1
                strategy = list(OrchestrationStrategy)[choice]
                
                print(f"\n🔄 使用 {strategy.value} 策略处理中...")
                result = await self.orchestrator.orchestrate(query, strategy)
                
                print(f"\n✅ 处理完成 (耗时: {result.execution_time:.2f}秒)")
                print(f"📋 结果:\n{result.final_result}")
                
                # 显示详细信息
                show_details = input("\n是否显示详细信息? (y/n): ").lower() == 'y'
                if show_details:
                    self._show_detailed_results(result)
                    
            except (ValueError, IndexError):
                print("❌ 无效的选择，请重试")
            except Exception as e:
                print(f"❌ 处理失败: {str(e)}")
    
    def _show_help(self):
        """显示帮助信息"""
        help_text = """
🔧 多模型编排策略说明:

1. parallel - 并行处理: 所有模型同时处理，结果聚合
2. sequential - 串行处理: 模型依次处理，前一个输出作为后一个输入  
3. voting - 投票机制: 所有模型处理后，由评判模型选择最佳答案
4. expert_routing - 专家路由: 根据问题类型选择最适合的专家模型
5. moa - 智能体混合: 使用MoA算法融合多个模型的优势
6. hierarchical - 分层处理: 问题分解→并行处理→结果整合
7. pipeline - 流水线处理: 按阶段依次处理（分析→研究→总结）

💡 使用建议:
- 简单问题: 使用 expert_routing 或 parallel
- 复杂问题: 使用 hierarchical 或 pipeline  
- 需要高质量答案: 使用 voting 或 moa
- 需要快速响应: 使用 expert_routing
"""
        print(help_text)
    
    def _show_detailed_results(self, result: OrchestrationResult):
        """显示详细结果"""
        print(f"\n📊 详细结果信息:")
        print(f"策略: {result.strategy_used}")
        print(f"执行时间: {result.execution_time:.2f}秒")
        print(f"元数据: {json.dumps(result.metadata, ensure_ascii=False, indent=2)}")
        
        print(f"\n🔍 各模型结果:")
        for i, individual_result in enumerate(result.individual_results, 1):
            print(f"\n--- 结果 {i} ---")
            for key, value in individual_result.items():
                if key == "response" and len(str(value)) > 100:
                    print(f"{key}: {str(value)[:100]}...")
                else:
                    print(f"{key}: {value}")


async def main():
    """主函数"""
    app = MultiModelApplication()
    
    print("🎯 选择运行模式:")
    print("1. 演示模式 - 自动测试各种策略")
    print("2. 交互模式 - 手动输入问题测试")
    
    choice = input("请选择 (1/2): ").strip()
    
    if choice == "1":
        await app.run_demo()
    elif choice == "2":
        await app.interactive_mode()
    else:
        print("❌ 无效选择")


if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main()) 
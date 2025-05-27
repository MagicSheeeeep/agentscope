# 多大模型编排系统

基于AgentScope的多大模型编排系统，支持多种编排策略，实现智能化的模型协作和任务分配。

## 🌟 特性

### 📋 支持的编排策略

1. **并行处理 (Parallel)** - 所有模型同时处理，结果聚合
2. **串行处理 (Sequential)** - 模型依次处理，前一个输出作为后一个输入
3. **投票机制 (Voting)** - 所有模型处理后，由评判模型选择最佳答案
4. **专家路由 (Expert Routing)** - 根据问题类型选择最适合的专家模型
5. **智能体混合 (MoA)** - 使用MoA算法融合多个模型的优势
6. **分层处理 (Hierarchical)** - 问题分解→并行处理→结果整合
7. **流水线处理 (Pipeline)** - 按阶段依次处理（分析→研究→总结）

### 🔧 支持的模型类型

- **阿里云DashScope**: qwen-max, qwen-turbo, qwen-plus
- **OpenAI**: gpt-4, gpt-3.5-turbo
- **本地模型**: Ollama (llama2, mistral等)
- **其他**: 支持AgentScope的所有模型类型

## 🚀 快速开始

### 1. 安装依赖

```bash
# 安装AgentScope
pip install agentscope

# 或从源码安装
git clone https://github.com/modelscope/agentscope.git
cd agentscope
pip install -e .
```

### 2. 配置API密钥

在使用前，请确保配置了相应的API密钥：

```bash
# 阿里云DashScope
export DASHSCOPE_API_KEY="your_dashscope_api_key"

# OpenAI
export OPENAI_API_KEY="your_openai_api_key"
```

### 3. 基本使用

```python
import asyncio
from multi_model_orchestration import (
    MultiModelOrchestrator, 
    ModelConfig, 
    OrchestrationStrategy
)

# 配置模型
model_configs = [
    ModelConfig(
        name="通用助手",
        config_name="general_assistant",
        model_type="dashscope_chat",
        model_name="qwen-max",
        api_key="your_api_key",
        specialty="通用问题",
        weight=1.0
    ),
    ModelConfig(
        name="技术专家",
        config_name="tech_expert",
        model_type="dashscope_chat",
        model_name="qwen-turbo",
        api_key="your_api_key",
        specialty="技术和编程",
        weight=1.2
    )
]

# 创建编排器
orchestrator = MultiModelOrchestrator(model_configs)

# 执行查询
async def main():
    result = await orchestrator.orchestrate(
        "请解释什么是机器学习",
        OrchestrationStrategy.EXPERT_ROUTING
    )
    print(result.final_result)

asyncio.run(main())
```

## 📖 详细使用指南

### 策略选择建议

| 场景 | 推荐策略 | 说明 |
|------|----------|------|
| 简单问题，需要快速响应 | Expert Routing | 自动选择最适合的专家模型 |
| 需要高质量答案 | Voting 或 MoA | 多模型协作，质量更高 |
| 复杂问题需要深度分析 | Hierarchical | 问题分解，分层处理 |
| 需要多步骤处理 | Pipeline | 按阶段依次处理 |
| 对比不同观点 | Parallel | 获得多个不同的回答 |
| 逐步完善答案 | Sequential | 每个模型在前一个基础上改进 |

### 配置参数说明

#### ModelConfig 参数

```python
ModelConfig(
    name="模型名称",              # 显示名称
    config_name="配置名称",       # AgentScope配置名
    model_type="模型类型",        # 如 dashscope_chat
    model_name="具体模型",        # 如 qwen-max
    api_key="API密钥",           # 模型API密钥
    specialty="专业领域",         # 可选，专业领域描述
    weight=1.0,                  # 可选，模型权重
    temperature=0.7,             # 可选，生成温度
    max_tokens=2000              # 可选，最大token数
)
```

#### 编排参数

```python
# 并行处理参数
await orchestrator.orchestrate(
    query,
    OrchestrationStrategy.PARALLEL,
    aggregation="weighted_selection"  # 或 "concatenate"
)

# 串行处理参数
await orchestrator.orchestrate(
    query,
    OrchestrationStrategy.SEQUENTIAL,
    refinement_prompt="自定义改进提示模板"
)

# 投票机制参数
await orchestrator.orchestrate(
    query,
    OrchestrationStrategy.VOTING,
    judge_model="judge_config_name"
)

# MoA参数
await orchestrator.orchestrate(
    query,
    OrchestrationStrategy.MIXTURE_OF_AGENTS,
    main_model="main_config_name",
    reference_models=["ref1", "ref2"],
    rounds=2,
    show_internal=True
)

# 流水线参数
await orchestrator.orchestrate(
    query,
    OrchestrationStrategy.PIPELINE,
    stages=[
        {"name": "分析", "prompt": "分析提示模板"},
        {"name": "研究", "prompt": "研究提示模板"},
        {"name": "总结", "prompt": "总结提示模板"}
    ]
)
```

## 🎯 使用示例

### 示例1：技术问题处理

```python
# 配置技术专家团队
tech_configs = [
    ModelConfig(
        name="Python专家",
        config_name="python_expert",
        model_type="dashscope_chat",
        model_name="qwen-max",
        api_key="your_key",
        specialty="Python编程",
        temperature=0.3
    ),
    ModelConfig(
        name="架构师",
        config_name="architect",
        model_type="openai_chat",
        model_name="gpt-4",
        api_key="your_key",
        specialty="系统架构",
        temperature=0.5
    )
]

orchestrator = MultiModelOrchestrator(tech_configs)

# 使用专家路由
result = await orchestrator.orchestrate(
    "如何设计一个高并发的微服务架构？",
    OrchestrationStrategy.EXPERT_ROUTING
)
```

### 示例2：创意写作

```python
# 配置创意团队
creative_configs = [
    ModelConfig(
        name="故事家",
        config_name="storyteller",
        model_type="dashscope_chat",
        model_name="qwen-plus",
        api_key="your_key",
        specialty="故事创作",
        temperature=0.9
    ),
    ModelConfig(
        name="诗人",
        config_name="poet",
        model_type="openai_chat",
        model_name="gpt-3.5-turbo",
        api_key="your_key",
        specialty="诗歌创作",
        temperature=0.8
    )
]

# 使用并行处理获得不同风格的创作
result = await orchestrator.orchestrate(
    "写一个关于春天的短故事",
    OrchestrationStrategy.PARALLEL,
    aggregation="concatenate"
)
```

### 示例3：研究报告生成

```python
# 使用分层处理策略
result = await orchestrator.orchestrate(
    "分析人工智能在教育领域的应用现状和发展趋势",
    OrchestrationStrategy.HIERARCHICAL
)

# 或使用自定义流水线
custom_stages = [
    {
        "name": "现状调研",
        "prompt": "请调研并总结{query}的现状"
    },
    {
        "name": "趋势分析",
        "prompt": "基于以下现状，分析未来发展趋势：\n{previous_output}"
    },
    {
        "name": "报告撰写",
        "prompt": "基于调研和分析，撰写完整报告：\n{previous_output}"
    }
]

result = await orchestrator.orchestrate(
    query,
    OrchestrationStrategy.PIPELINE,
    stages=custom_stages
)
```

## 🔧 高级功能

### 自定义聚合策略

```python
class CustomOrchestrator(MultiModelOrchestrator):
    async def _custom_aggregation(self, query: str, **kwargs):
        """自定义聚合策略"""
        # 实现您的自定义逻辑
        pass
```

### 动态模型选择

```python
def select_models_by_query(query: str, available_configs: List[ModelConfig]):
    """根据查询内容动态选择模型"""
    if "代码" in query or "编程" in query:
        return [config for config in available_configs if "技术" in config.specialty]
    elif "创意" in query or "写作" in query:
        return [config for config in available_configs if "创意" in config.specialty]
    else:
        return available_configs
```

### 结果缓存

```python
import hashlib
import json

class CachedOrchestrator(MultiModelOrchestrator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache = {}
    
    async def orchestrate(self, query: str, strategy: OrchestrationStrategy, **kwargs):
        # 生成缓存键
        cache_key = hashlib.md5(
            f"{query}_{strategy.value}_{json.dumps(kwargs, sort_keys=True)}".encode()
        ).hexdigest()
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        result = await super().orchestrate(query, strategy, **kwargs)
        self.cache[cache_key] = result
        return result
```

## 📊 性能优化

### 1. 并发控制

```python
# 限制并发数量
import asyncio

semaphore = asyncio.Semaphore(3)  # 最多3个并发

async def process_with_limit(config: ModelConfig):
    async with semaphore:
        return await process_model(config)
```

### 2. 超时控制

```python
# 设置超时
try:
    result = await asyncio.wait_for(
        orchestrator.orchestrate(query, strategy),
        timeout=30.0  # 30秒超时
    )
except asyncio.TimeoutError:
    print("处理超时")
```

### 3. 错误处理

```python
async def robust_orchestrate(orchestrator, query, strategy):
    """带错误处理的编排"""
    try:
        return await orchestrator.orchestrate(query, strategy)
    except Exception as e:
        print(f"编排失败: {e}")
        # 降级到单模型处理
        return await fallback_single_model(query)
```

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   ```
   错误: Invalid API key
   解决: 检查API密钥是否正确配置
   ```

2. **模型不可用**
   ```
   错误: Model not found
   解决: 确认模型名称和类型是否正确
   ```

3. **内存不足**
   ```
   错误: Out of memory
   解决: 减少并发数量或使用更小的模型
   ```

4. **网络超时**
   ```
   错误: Request timeout
   解决: 增加超时时间或检查网络连接
   ```

### 调试技巧

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 显示内部处理过程
result = await orchestrator.orchestrate(
    query,
    OrchestrationStrategy.MIXTURE_OF_AGENTS,
    show_internal=True
)

# 检查各模型的详细结果
for i, individual_result in enumerate(result.individual_results):
    print(f"模型 {i+1}: {individual_result}")
```

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

本项目基于Apache 2.0许可证开源。

## 🙏 致谢

感谢AgentScope团队提供的优秀框架，使得多模型编排成为可能。 